// Supabase Edge Function: cwm-admin
// Verified-write proxy. Receives a cwm_token, verifies HMAC-SHA256 with
// CWM_JWT_SECRET, runs ownership checks, then writes via service_role.
// Anon key NEVER has UPDATE/DELETE/INSERT permission on protected tables.

import { createClient } from "npm:@supabase/supabase-js@2";

// === djwt verify 代替 (Web Crypto API only, no remote deps) ===
function _b64urlDecode(s: string): Uint8Array {
  const pad = s.length % 4;
  const b64 = (s + (pad ? "=".repeat(4 - pad) : "")).replace(/-/g, "+").replace(/_/g, "/");
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
async function verify(jwt: string, key: CryptoKey, _alg?: any): Promise<any> {
  const parts = jwt.split(".");
  if (parts.length !== 3) throw new Error("invalid jwt format");
  const [h, p, s] = parts;
  const sig = _b64urlDecode(s);
  const data = new TextEncoder().encode(h + "." + p);
  const ok = await crypto.subtle.verify({ name: "HMAC", hash: "SHA-256" }, key, sig, data);
  if (!ok) throw new Error("invalid signature");
  const payload = JSON.parse(new TextDecoder().decode(_b64urlDecode(p)));
  if (payload.exp && Date.now() / 1000 > payload.exp) throw new Error("expired");
  return payload;
}
// === end djwt replacement ===

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;

// === 鍵取得: 新形式 SUPABASE_SECRET_KEYS (sb_secret_*) を優先、Legacy JWT を fallback ===
// Legacy HS256 JWT は revoke 後無効化されるため、新形式優先で安全に移行
function resolveServiceKey(): string {
  // 1) 新形式: SUPABASE_SECRET_KEYS = JSON dict, e.g. {"default":"sb_secret_..."}
  const secretKeysJson = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (secretKeysJson) {
    try {
      const dict = JSON.parse(secretKeysJson);
      if (dict && typeof dict === "object") {
        // "default" キー優先、なければ最初の値
        const v = dict.default ?? Object.values(dict)[0];
        if (typeof v === "string" && v.length > 0) return v;
      }
    } catch (_e) {
      // JSON parse 失敗は無視して fallback へ
    }
  }
  // 2) 新形式 (個別 env): SUPABASE_SECRET_DEFAULT_KEY
  const sbSecretDefault = Deno.env.get("SUPABASE_SECRET_DEFAULT_KEY");
  if (sbSecretDefault) return sbSecretDefault;
  // 3) Legacy fallback: revoke 前まで動作させる
  return Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || Deno.env.get("SUPABASE_SERVICE_KEY") || "";
}
const SUPABASE_SERVICE_KEY = resolveServiceKey();

const JWT_SECRET = Deno.env.get("CWM_JWT_SECRET")!;
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") || "";
const INVITE_FROM_EMAIL = Deno.env.get("INQUIRY_FROM_EMAIL") || "onboarding@resend.dev";
const SITE_URL = Deno.env.get("SITE_URL") || "https://cowkml.com";

// 招待メール送信
async function sendInviteEmail(toEmail: string, displayName: string | null, company: string, role: string, token: string): Promise<{ ok: boolean; error?: string }> {
  if (!RESEND_API_KEY) {
    console.error("[cwm-admin] RESEND_API_KEY not configured");
    return { ok: false, error: "RESEND_API_KEY not configured" };
  }
  const inviteUrl = `${SITE_URL}/invite?t=${encodeURIComponent(token)}`;
  const safeName = displayName ? displayName : "ご担当者";
  const roleLabel = role === "viewer" ? "閲覧のみ" : "編集可";
  const subject = `【COWORKMILL】${company} から管理画面への招待が届いています`;
  const text = `${safeName} 様

${company} の管理画面にあなたを ${roleLabel} 担当者として招待しました。

下記のリンクから 7日以内 にパスワードを設定してご利用を開始してください。

▼ パスワード設定リンク
${inviteUrl}

※ このメールに心当たりがない場合は、 このメールを破棄してください。
※ リンクの有効期限は 7日間 です。 期限切れの場合は招待元に再送を依頼してください。

----
COWORKMILL（コワークミル）
${SITE_URL}
`;
  const html = `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>${subject}</title>
</head>
<body style="margin:0;padding:0;background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic',sans-serif;color:#333">
<div style="max-width:560px;margin:auto;padding:24px;background:#fff">
<h2 style="color:#2BB5C8;font-size:18px;margin:0 0 16px">COWORKMILL 管理画面への招待</h2>
<p>${safeName} 様</p>
<p><strong>${company}</strong> の管理画面にあなたを <strong>${roleLabel}</strong> 担当者として招待しました。</p>
<p>下記のボタンから <strong>7日以内</strong> にパスワードを設定してご利用を開始してください。</p>
<p style="text-align:center;margin:32px 0">
  <a href="${inviteUrl}" style="display:inline-block;padding:14px 32px;background:#2BB5C8;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:600">パスワードを設定する</a>
</p>
<p style="font-size:12px;color:#888">またはこのリンクをコピー: <br><span style="word-break:break-all">${inviteUrl}</span></p>
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
<p style="font-size:11px;color:#888">※ このメールに心当たりがない場合は破棄してください。<br>※ リンクの有効期限は 7日間 です。</p>
<p style="font-size:11px;color:#888">— COWORKMILL（コワークミル）</p>
</div>
</body>
</html>`;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: `COWORKMILL <${INVITE_FROM_EMAIL}>`,
        to: [toEmail],
        subject,
        html,
        text,
      }),
    });
    if (!r.ok) {
      const errText = await r.text().catch(() => "");
      console.error("[cwm-admin] Resend error:", r.status, errText);
      return { ok: false, error: `email send failed (${r.status})` };
    }
    return { ok: true };
  } catch (e) {
    console.error("[cwm-admin] sendInviteEmail exception:", e);
    return { ok: false, error: "email send exception" };
  }
}

// 施設承認 + 招待メール送信 (新規account作成時)
async function sendOwnerApprovalEmail(
  toEmail: string,
  applicantName: string | null,
  spaceName: string,
  spaceSlug: string,
  token: string
): Promise<{ ok: boolean; error?: string }> {
  if (!RESEND_API_KEY) return { ok: false, error: "RESEND_API_KEY not configured" };
  const inviteUrl = `${SITE_URL}/invite?t=${encodeURIComponent(token)}`;
  const publicUrl = spaceSlug ? `${SITE_URL}/space/${encodeURIComponent(spaceSlug)}` : SITE_URL;
  const safeName = applicantName ? applicantName : "ご担当者";
  const subject = `【COWORKMILL】${spaceName} の掲載準備が整いました ✨`;
  const text = `${safeName} 様

このたびは COWORKMILL への施設掲載をご検討いただき、 誠にありがとうございます。
施設の確認が取れましたので、 ぜひご掲載のほどよろしくお願い申し上げます。
御社の素敵な施設を、 多くの方にご覧いただければ幸いです。

▼ 公開ページ
${publicUrl}

▼ 管理画面のパスワードを設定する (有効期限: 7日間)
${inviteUrl}

パスワード設定後、 ${SITE_URL}/admin からログインして、
施設情報や写真の編集などをご利用いただけます。

掲載内容や運用についてご不明点・ご相談などございましたら、
お気軽に info@offml.com までご連絡ください。

今後ともどうぞよろしくお願いいたします。

----
COWORKMILL（コワークミル）
${SITE_URL}
`;
  const html = `<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>${subject}</title></head>
<body style="margin:0;padding:0;background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic',sans-serif;color:#333;line-height:1.7">
<div style="max-width:560px;margin:auto;padding:24px;background:#fff">
<h2 style="color:#2BB5C8;font-size:18px;margin:0 0 16px">✨ ${spaceName} の掲載準備が整いました</h2>
<p>${safeName} 様</p>
<p>このたびは COWORKMILL への施設掲載をご検討いただき、 誠にありがとうございます。<br>施設の確認が取れましたので、 ぜひご掲載のほどよろしくお願い申し上げます。<br>御社の素敵な施設を、 多くの方にご覧いただければ幸いです。</p>
<p style="margin:24px 0"><a href="${publicUrl}" style="color:#2BB5C8">▼ 公開ページを確認する</a><br><span style="font-size:11px;color:#888;word-break:break-all">${publicUrl}</span></p>
<p style="text-align:center;margin:32px 0">
  <a href="${inviteUrl}" style="display:inline-block;padding:14px 32px;background:#2BB5C8;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:600">管理画面のパスワードを設定する</a>
</p>
<p style="font-size:12px;color:#888">またはこのリンクをコピー: <br><span style="word-break:break-all">${inviteUrl}</span></p>
<p style="font-size:13px">パスワード設定後、 <a href="${SITE_URL}/admin">${SITE_URL}/admin</a> からログインして、 施設情報や写真の編集などをご利用いただけます。</p>
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
<p style="font-size:13px;color:#444">掲載内容や運用についてご不明点・ご相談などございましたら、 お気軽に <a href="mailto:info@offml.com" style="color:#2BB5C8">info@offml.com</a> までご連絡ください。</p>
<p style="font-size:13px;color:#444">今後ともどうぞよろしくお願いいたします。</p>
<p style="font-size:11px;color:#888;margin-top:24px">※ パスワード設定リンクの有効期限は 7日間 です。</p>
<p style="font-size:11px;color:#888">— COWORKMILL（コワークミル）</p>
</div>
</body></html>`;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: `COWORKMILL <${INVITE_FROM_EMAIL}>`,
        to: [toEmail], subject, html, text
      }),
    });
    if (!r.ok) {
      const errText = await r.text().catch(() => "");
      console.error("[cwm-admin] sendOwnerApprovalEmail Resend error:", r.status, errText);
      return { ok: false, error: `email send failed (${r.status})` };
    }
    return { ok: true };
  } catch (e) {
    console.error("[cwm-admin] sendOwnerApprovalEmail exception:", e);
    return { ok: false, error: "email send exception" };
  }
}

// 施設承認 通知のみ (既存account/既にパス設定済み)
async function sendOwnerApprovalNotice(
  toEmail: string,
  applicantName: string | null,
  spaceName: string,
  spaceSlug: string
): Promise<{ ok: boolean; error?: string }> {
  if (!RESEND_API_KEY) return { ok: false, error: "RESEND_API_KEY not configured" };
  const publicUrl = spaceSlug ? `${SITE_URL}/space/${encodeURIComponent(spaceSlug)}` : SITE_URL;
  const safeName = applicantName ? applicantName : "ご担当者";
  const subject = `【COWORKMILL】${spaceName} の掲載準備が整いました ✨`;
  const text = `${safeName} 様

このたびは COWORKMILL への施設掲載をご検討いただき、 ありがとうございます。
施設の確認が取れましたので、 ぜひご掲載のほどよろしくお願い申し上げます。
御社の素敵な施設を、 多くの方にご覧いただければ幸いです。

▼ 公開ページ
${publicUrl}

施設情報の編集は、 既存の管理画面からご利用いただけます。
${SITE_URL}/admin

掲載内容や運用についてご不明点・ご相談などございましたら、
お気軽に info@offml.com までご連絡ください。

今後ともどうぞよろしくお願いいたします。

----
COWORKMILL（コワークミル）
${SITE_URL}
`;
  const html = `<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>${subject}</title></head>
<body style="margin:0;padding:0;background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic',sans-serif;color:#333;line-height:1.7">
<div style="max-width:560px;margin:auto;padding:24px;background:#fff">
<h2 style="color:#2BB5C8;font-size:18px;margin:0 0 16px">✨ ${spaceName} の掲載準備が整いました</h2>
<p>${safeName} 様</p>
<p>このたびは COWORKMILL への施設掲載をご検討いただき、 ありがとうございます。<br>施設の確認が取れましたので、 ぜひご掲載のほどよろしくお願い申し上げます。<br>御社の素敵な施設を、 多くの方にご覧いただければ幸いです。</p>
<p style="margin:24px 0"><a href="${publicUrl}" style="color:#2BB5C8">▼ 公開ページを確認する</a></p>
<p style="font-size:13px">施設情報の編集は、 既存の管理画面からご利用いただけます。<br><a href="${SITE_URL}/admin">${SITE_URL}/admin</a></p>
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
<p style="font-size:13px;color:#444">掲載内容や運用についてご不明点・ご相談などございましたら、 お気軽に <a href="mailto:info@offml.com" style="color:#2BB5C8">info@offml.com</a> までご連絡ください。</p>
<p style="font-size:13px;color:#444">今後ともどうぞよろしくお願いいたします。</p>
<p style="font-size:11px;color:#888;margin-top:24px">— COWORKMILL（コワークミル）</p>
</div>
</body></html>`;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: `COWORKMILL <${INVITE_FROM_EMAIL}>`,
        to: [toEmail], subject, html, text
      }),
    });
    if (!r.ok) {
      const errText = await r.text().catch(() => "");
      console.error("[cwm-admin] sendOwnerApprovalNotice Resend error:", r.status, errText);
      return { ok: false, error: `email send failed (${r.status})` };
    }
    return { ok: true };
  } catch (e) {
    console.error("[cwm-admin] sendOwnerApprovalNotice exception:", e);
    return { ok: false, error: "email send exception" };
  }
}

// 施設却下 通知メール (LINE公式風の淡々とした文面)
async function sendOwnerRejectEmail(
  toEmail: string,
  applicantName: string | null
): Promise<{ ok: boolean; error?: string }> {
  if (!RESEND_API_KEY) return { ok: false, error: "RESEND_API_KEY not configured" };
  const safeName = applicantName ? applicantName : "ご担当者";
  const subject = `【COWORKMILL】掲載お申込みの審査結果のご案内`;
  const text = `${safeName} 様

このたびは COWORKMILL への掲載をお申込みいただき、 誠にありがとうございました。
お申込みいただきました内容の審査が完了いたしましたのでご案内申し上げます。

▼ 審査結果
審査結果: 非承認
理由: 弊社の掲載基準に抵触するため

ご申請いただきました施設の掲載は、 今回見送らせていただきます。
なお、 審査内容や個別のご質問につきましては、 回答を差し控えさせていただいております。
何卒ご了承いただけますようお願い申し上げます。

----
COWORKMILL（コワークミル）
${SITE_URL}

※ 本メールは送信専用アドレスから配信されております。
　ご返信いただいても内容を確認できませんので、 予めご了承ください。
`;
  const html = `<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>${subject}</title></head>
<body style="margin:0;padding:0;background:#fafafa;font-family:-apple-system,BlinkMacSystemFont,'Hiragino Sans','Yu Gothic',sans-serif;color:#333;line-height:1.7">
<div style="max-width:560px;margin:auto;padding:24px;background:#fff">
<h2 style="color:#333;font-size:17px;margin:0 0 16px;border-bottom:1px solid #eee;padding-bottom:12px">掲載お申込みの審査結果のご案内</h2>
<p>${safeName} 様</p>
<p>このたびは COWORKMILL への掲載をお申込みいただき、 誠にありがとうございました。<br>お申込みいただきました内容の審査が完了いたしましたのでご案内申し上げます。</p>
<div style="margin:24px 0;padding:16px;background:#f7f7f7;border-radius:6px">
  <div style="font-size:13px;color:#666;margin-bottom:8px">▼ 審査結果</div>
  <div style="font-size:14px;line-height:2"><strong>審査結果:</strong> 非承認<br><strong>理由:</strong> 弊社の掲載基準に抵触するため</div>
</div>
<p>ご申請いただきました施設の掲載は、 今回見送らせていただきます。<br>なお、 審査内容や個別のご質問につきましては、 回答を差し控えさせていただいております。<br>何卒ご了承いただけますようお願い申し上げます。</p>
<hr style="border:none;border-top:1px solid #eee;margin:24px 0">
<p style="font-size:11px;color:#888">COWORKMILL（コワークミル）<br><a href="${SITE_URL}" style="color:#888">${SITE_URL}</a></p>
<p style="font-size:11px;color:#aaa;margin-top:16px">※ 本メールは送信専用アドレスから配信されております。<br>　ご返信いただいても内容を確認できませんので、 予めご了承ください。</p>
</div>
</body></html>`;
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": `Bearer ${RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        from: `COWORKMILL <${INVITE_FROM_EMAIL}>`,
        to: [toEmail], subject, html, text
      }),
    });
    if (!r.ok) {
      const errText = await r.text().catch(() => "");
      console.error("[cwm-admin] sendOwnerRejectEmail Resend error:", r.status, errText);
      return { ok: false, error: `email send failed (${r.status})` };
    }
    return { ok: true };
  } catch (e) {
    console.error("[cwm-admin] sendOwnerRejectEmail exception:", e);
    return { ok: false, error: "email send exception" };
  }
}

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

async function getKey(s: string) {
  return crypto.subtle.importKey("raw", new TextEncoder().encode(s),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// ============ Phase 5: Rate Limiting ============
// In-memory sliding window rate limiter (60s window, 30 req per account+target).
// Edge Function instances are short-lived so this is per-instance, but it covers
// the realistic burst-attack window. For stronger protection add a Redis-backed
// limiter or use Supabase Database Functions.
const rateLimitWindow = new Map<string, number[]>();
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX = 30;

function checkRateLimit(key: string): boolean {
  const now = Date.now();
  const arr = rateLimitWindow.get(key) || [];
  const recent = arr.filter((t) => now - t < RATE_LIMIT_WINDOW_MS);
  if (recent.length >= RATE_LIMIT_MAX) {
    rateLimitWindow.set(key, recent);
    return false;
  }
  recent.push(now);
  rateLimitWindow.set(key, recent);
  return true;
}

// ============ Phase 5: Audit Log ============
async function writeAuditLog(
  sb: ReturnType<typeof createClient>,
  accountId: string,
  target: string,
  action: string,
  recordId: string | null,
  status: "ok" | "denied" | "error",
  detail: string | null,
  ip: string | null,
) {
  try {
    await sb.from("audit_logs").insert({
      account_id: accountId,
      target,
      action,
      record_id: recordId,
      status,
      detail,
      ip,
    });
  } catch (_e) {
    // Audit log must never break the main action
  }
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim()
    ?? req.headers.get("cf-connecting-ip")
    ?? null;

  try {
    const body = await req.json();
    const { token, target, action, id, data } = body;

    if (!target) return jsonResponse({ error: "操作対象が指定されていません" }, 400);
    if (!action) return jsonResponse({ error: "操作内容が指定されていません" }, 400);

    // ============================================================
    // target=ops: 運営管理画面 (admin-ops) 用の認証・ユーザー管理
    // 別系統のため accounts テーブル経由の認証は通さない
    // ============================================================
    if (target === "ops") {
      const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

      // ----- ops:login : Google経由のSupabase JWT検証 → ops_token発行 -----
      if (action === "login") {
        const supabaseJwt = body.supabase_jwt;
        if (!supabaseJwt) return jsonResponse({ error: "Supabase JWT が必要です" }, 400);

        // Supabase Auth に問い合わせて JWT 検証 + email 取得
        const userRes = await fetch(SUPABASE_URL + "/auth/v1/user", {
          headers: {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": "Bearer " + supabaseJwt
          }
        });
        if (!userRes.ok) {
          return jsonResponse({ error: "Google認証情報が無効です（再ログインしてください）" }, 401);
        }
        const userInfo = await userRes.json();
        const email = (userInfo.email || "").toLowerCase().trim();
        if (!email) return jsonResponse({ error: "メールアドレスが取得できませんでした" }, 401);

        // 簡易レート制限: email単位
        if (!checkRateLimit("ops:login:" + email)) {
          return jsonResponse({ error: "短時間に多くのログイン試行が行われました。しばらくお待ちください。" }, 429);
        }

        // 許可リストに存在するか確認
        const { data: allowed, error: allowedErr } = await sb
          .from("ops_allowed_users")
          .select("email,role")
          .eq("email", email)
          .maybeSingle();
        if (allowedErr) {
          return jsonResponse({ error: "許可リストの照会に失敗しました" }, 500);
        }
        if (!allowed) {
          return jsonResponse({ error: "このメールアドレスにはアクセス権限がありません。管理者にお問い合わせください。" }, 403);
        }

        // last_login_at 更新（失敗してもログインは通す）
        try {
          await sb.from("ops_allowed_users").update({ last_login_at: new Date().toISOString() }).eq("email", email);
        } catch (_e) {}

        // ops_token (HMAC-SHA256 JWT) を発行: 8時間有効
        const now = Math.floor(Date.now() / 1000);
        const opsPayload = { sub: email, role: allowed.role, kind: "ops", iat: now, exp: now + 8 * 3600 };
        const header = { alg: "HS256", typ: "JWT" };
        const b64url = (obj: any) => {
          const json = typeof obj === "string" ? obj : JSON.stringify(obj);
          return btoa(json).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
        };
        const dataPart = b64url(header) + "." + b64url(opsPayload);
        const key = await getKey(JWT_SECRET);
        const sig = await crypto.subtle.sign({ name: "HMAC", hash: "SHA-256" }, key, new TextEncoder().encode(dataPart));
        const sigB64 = btoa(String.fromCharCode(...new Uint8Array(sig))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
        const opsToken = dataPart + "." + sigB64;

        return jsonResponse({ ok: true, ops_token: opsToken, email, role: allowed.role });
      }

      // ----- 以降の操作 (list/invite/delete) は ops_token 必須 -----
      if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
      let opsPayload: any;
      try {
        const key = await getKey(JWT_SECRET);
        opsPayload = await verify(token, key);
      } catch (_e) {
        return jsonResponse({ error: "認証トークンが無効または期限切れです（再ログインしてください）" }, 401);
      }
      if (opsPayload.kind !== "ops") {
        return jsonResponse({ error: "このトークンは運営管理画面用ではありません" }, 401);
      }
      const opsEmail = (opsPayload.sub || "").toLowerCase();
      const opsRole = opsPayload.role;
      if (!opsEmail) return jsonResponse({ error: "トークンにメールアドレスが含まれていません" }, 401);

      // 念のため、現在も許可リストに存在するか再確認
      const { data: stillAllowed } = await sb
        .from("ops_allowed_users").select("email,role").eq("email", opsEmail).maybeSingle();
      if (!stillAllowed) {
        return jsonResponse({ error: "アクセス権限が削除されています。再ログインしてください。" }, 403);
      }

      if (!checkRateLimit("ops:" + opsEmail + ":" + action)) {
        return jsonResponse({ error: "短時間に多くの操作を行いました。しばらくお待ちください。" }, 429);
      }

      // ----- ops:list : 許可ユーザー一覧取得 -----
      if (action === "list") {
        const { data: list, error } = await sb
          .from("ops_allowed_users")
          .select("email,role,invited_by,invited_at,last_login_at,notes")
          .order("invited_at", { ascending: true });
        if (error) return jsonResponse({ error: "一覧の取得に失敗しました" }, 500);
        return jsonResponse({ ok: true, users: list || [], current_email: opsEmail, current_role: opsRole });
      }

      // ----- ops:invite : 新規招待（owner のみ）-----
      if (action === "invite") {
        if (opsRole !== "owner") return jsonResponse({ error: "招待は owner のみ実行できます" }, 403);
        const inviteEmail = (data?.email || "").toLowerCase().trim();
        const inviteRole = data?.role === "owner" ? "owner" : "staff";
        const inviteNotes = (data?.notes || "").substring(0, 500);

        if (!inviteEmail) return jsonResponse({ error: "メールアドレスを指定してください" }, 400);
        if (!/^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/.test(inviteEmail) || inviteEmail.length > 254) {
          return jsonResponse({ error: "メールアドレスの形式が正しくありません" }, 400);
        }

        // 既存チェック
        const { data: exists } = await sb.from("ops_allowed_users").select("email").eq("email", inviteEmail).maybeSingle();
        if (exists) return jsonResponse({ error: "このメールアドレスは既に登録されています" }, 409);

        const { error: insErr } = await sb.from("ops_allowed_users").insert({
          email: inviteEmail,
          role: inviteRole,
          invited_by: opsEmail,
          notes: inviteNotes || null
        });
        if (insErr) return jsonResponse({ error: "登録に失敗しました: " + insErr.message }, 500);

        try { await writeAuditLog(sb, opsEmail, "ops", "invite", inviteEmail, "ok", "role=" + inviteRole, ip); } catch(_e){}
        return jsonResponse({ ok: true });
      }

      // ----- ops:delete : 削除（owner のみ、自分は削除不可、最後の owner も削除不可）-----
      if (action === "delete") {
        if (opsRole !== "owner") return jsonResponse({ error: "削除は owner のみ実行できます" }, 403);
        const targetEmail = (data?.email || "").toLowerCase().trim();
        if (!targetEmail) return jsonResponse({ error: "削除対象のメールアドレスが指定されていません" }, 400);
        if (targetEmail === opsEmail) return jsonResponse({ error: "自分自身は削除できません" }, 400);

        // 削除対象を取得して、対象が owner で、かつ owner が他にいるか確認
        const { data: targetUser } = await sb
          .from("ops_allowed_users").select("email,role").eq("email", targetEmail).maybeSingle();
        if (!targetUser) return jsonResponse({ error: "対象のユーザーが見つかりません" }, 404);

        if (targetUser.role === "owner") {
          const { count } = await sb
            .from("ops_allowed_users").select("email", { count: "exact", head: true }).eq("role", "owner");
          if ((count || 0) <= 1) {
            return jsonResponse({ error: "最後の owner は削除できません" }, 400);
          }
        }

        const { error: delErr } = await sb.from("ops_allowed_users").delete().eq("email", targetEmail);
        if (delErr) return jsonResponse({ error: "削除に失敗しました" }, 500);

        try { await writeAuditLog(sb, opsEmail, "ops", "delete", targetEmail, "ok", null, ip); } catch(_e){}
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============================================================
    // target=ops_db: 運営管理画面用の汎用 DB プロキシ
    // ops_token を検証し、SERVICE_ROLE_KEY で REST API を中継する
    // ============================================================
    if (target === "ops_db") {
      if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
      let opsPayload2: any;
      try {
        const key = await getKey(JWT_SECRET);
        opsPayload2 = await verify(token, key);
      } catch (_e) {
        return jsonResponse({ error: "認証トークンが無効または期限切れです（再ログインしてください）" }, 401);
      }
      if (opsPayload2.kind !== "ops") {
        return jsonResponse({ error: "このトークンは運営管理画面用ではありません" }, 401);
      }
      const opsEmail2 = (opsPayload2.sub || "").toLowerCase();
      if (!opsEmail2) return jsonResponse({ error: "トークンにメールアドレスが含まれていません" }, 401);

      const sb2 = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
      // 念のため、現在も許可リストに存在するか再確認
      const { data: stillAllowed2 } = await sb2
        .from("ops_allowed_users").select("email").eq("email", opsEmail2).maybeSingle();
      if (!stillAllowed2) {
        return jsonResponse({ error: "アクセス権限が削除されています。再ログインしてください。" }, 403);
      }

      if (!checkRateLimit("ops_db:" + opsEmail2)) {
        return jsonResponse({ error: "短時間に多くの操作を行いました。しばらくお待ちください。" }, 429);
      }

      const restBase = SUPABASE_URL + "/rest/v1/";
      const proxyHeaders: Record<string, string> = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
      };

      const d = data || {};
      // パス整形 (URLインジェクション防止: 先頭スラッシュやプロトコルを禁止)
      const sanitize = (s: any) => {
        if (typeof s !== "string") return "";
        if (s.indexOf("/") === 0 || s.indexOf("://") !== -1) return "";
        return s;
      };

      try {
        if (action === "select") {
          const path = sanitize(d.path);
          if (!path) return jsonResponse({ error: "path が無効です" }, 400);
          const r = await fetch(restBase + path, { headers: proxyHeaders });
          const text = await r.text();
          return new Response((r.status === 204 || r.status === 205 || r.status === 304) ? null : text, { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
        }

        if (action === "insert") {
          const table = sanitize(d.table);
          if (!table) return jsonResponse({ error: "table が無効です" }, 400);
          const r = await fetch(restBase + table, {
            method: "POST",
            headers: { ...proxyHeaders, "Prefer": "return=representation" },
            body: JSON.stringify(d.body || {})
          });
          const text = await r.text();
          await writeAuditLog(sb2, opsEmail2, "ops_db", "insert", table, r.ok ? "ok" : "error", null, ip);
          return new Response((r.status === 204 || r.status === 205 || r.status === 304) ? null : text, { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
        }

        if (action === "update") {
          const table = sanitize(d.table);
          if (!table) return jsonResponse({ error: "table が無効です" }, 400);
          const filter = typeof d.filter === "string" ? d.filter : "";
          const r = await fetch(restBase + table + (filter ? "?" + filter : ""), {
            method: "PATCH",
            headers: { ...proxyHeaders, "Prefer": "return=representation" },
            body: JSON.stringify(d.body || {})
          });
          const text = await r.text();
          await writeAuditLog(sb2, opsEmail2, "ops_db", "update", table, r.ok ? "ok" : "error", null, ip);
          return new Response((r.status === 204 || r.status === 205 || r.status === 304) ? null : text, { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
        }

        if (action === "delete") {
          const table = sanitize(d.table);
          if (!table) return jsonResponse({ error: "table が無効です" }, 400);
          const filter = typeof d.filter === "string" ? d.filter : "";
          if (!filter) return jsonResponse({ error: "filter が必須です（全件削除を防ぐため）" }, 400);
          const r = await fetch(restBase + table + "?" + filter, {
            method: "DELETE",
            headers: proxyHeaders
          });
          await writeAuditLog(sb2, opsEmail2, "ops_db", "delete", table, r.ok ? "ok" : "error", filter.substring(0, 200), ip);
          return jsonResponse({ ok: r.ok, status: r.status }, r.ok ? 200 : r.status);
        }

        if (action === "rpc") {
          const rpcName = sanitize(d.rpc);
          if (!rpcName) return jsonResponse({ error: "rpc が無効です" }, 400);
          const r = await fetch(restBase + "rpc/" + rpcName, {
            method: "POST",
            headers: proxyHeaders,
            body: JSON.stringify(d.body || {})
          });
          const text = await r.text();
          await writeAuditLog(sb2, opsEmail2, "ops_db", "rpc:" + rpcName, null, r.ok ? "ok" : "error", null, ip);
          return new Response((r.status === 204 || r.status === 205 || r.status === 304) ? null : text, { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
        }

        if (action === "auth_invite") {
          // Supabase Auth admin/invite (掲載者用 magic link 招待)
          const inviteEmail2 = (d.email || "").toLowerCase().trim();
          if (!inviteEmail2 || !/^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/.test(inviteEmail2)) {
            return jsonResponse({ error: "メールアドレスの形式が正しくありません" }, 400);
          }
          const r = await fetch(SUPABASE_URL + "/auth/v1/admin/invite", {
            method: "POST",
            headers: proxyHeaders,
            body: JSON.stringify({ email: inviteEmail2 })
          });
          const text = await r.text();
          await writeAuditLog(sb2, opsEmail2, "ops_db", "auth_invite", inviteEmail2, r.ok ? "ok" : "error", null, ip);
          return new Response((r.status === 204 || r.status === 205 || r.status === 304) ? null : text, { status: r.status, headers: { ...cors, "Content-Type": "application/json" } });
        }

        // ============ approve_space (施設承認 + 招待メール送信) ============
        if (action === "approve_space") {
          const spaceId = ((d.space_id || "") + "").trim();
          if (!spaceId) return jsonResponse({ error: "space_id が必要です" }, 400);

          // RPC実行: spaces承認 + accounts作成/紐づけ + 招待token発行
          const { data: rpcRes, error: rpcErr } = await sb2.rpc("approve_space_with_invite", {
            p_space_id: spaceId
          });
          if (rpcErr) {
            await writeAuditLog(sb2, opsEmail2, "ops_db", "approve_space", spaceId, "error", rpcErr.message, ip);
            return jsonResponse({ error: "承認処理に失敗しました: " + rpcErr.message }, 500);
          }
          const r = rpcRes as {
            ok?: boolean;
            error?: string;
            space_id?: string;
            space_name?: string;
            space_slug?: string;
            applicant_email?: string;
            applicant_name?: string | null;
            account_id?: string;
            invite_token?: string | null;
            is_new_account?: boolean;
          };
          if (!r?.ok) {
            await writeAuditLog(sb2, opsEmail2, "ops_db", "approve_space", spaceId, "denied", r?.error || "unknown", ip);
            const errorMap: Record<string, string> = {
              "space not found": "施設が見つかりません",
              "no contact_email": "申込者のメールアドレスが未設定です"
            };
            return jsonResponse({ error: errorMap[r?.error || ""] || r?.error || "承認に失敗しました" }, 400);
          }

          // 招待メール送信 (新規招待 or 再発行の場合のみ)
          let mailResult: { ok: boolean; error?: string } = { ok: true };
          if (r.is_new_account && r.invite_token && r.applicant_email) {
            mailResult = await sendOwnerApprovalEmail(
              r.applicant_email,
              r.applicant_name || null,
              r.space_name || "ご申請の施設",
              r.space_slug || "",
              r.invite_token
            );
          } else if (r.applicant_email) {
            // 既存accountの場合: 「掲載しました」 通知のみ
            mailResult = await sendOwnerApprovalNotice(
              r.applicant_email,
              r.applicant_name || null,
              r.space_name || "ご申請の施設",
              r.space_slug || ""
            );
          }

          await writeAuditLog(sb2, opsEmail2, "ops_db", "approve_space", spaceId, mailResult.ok ? "ok" : "mail_failed", mailResult.ok ? null : (mailResult.error || null), ip);

          return jsonResponse({
            ok: true,
            space_id: r.space_id,
            account_id: r.account_id,
            is_new_account: r.is_new_account,
            mail_sent: mailResult.ok,
            mail_warning: mailResult.ok ? null : "施設は承認されましたが、 通知メールの送信に失敗しました"
          });
        }

        // ============ reject_space (施設却下 + 通知メール送信) ============
        if (action === "reject_space") {
          const spaceId = ((d.space_id || "") + "").trim();
          const rejectReason = ((d.reject_reason || "") + "").trim();
          if (!spaceId) return jsonResponse({ error: "space_id が必要です" }, 400);

          const { data: rpcRes, error: rpcErr } = await sb2.rpc("reject_space_with_email", {
            p_space_id: spaceId,
            p_reject_reason: rejectReason || null
          });
          if (rpcErr) {
            await writeAuditLog(sb2, opsEmail2, "ops_db", "reject_space", spaceId, "error", rpcErr.message, ip);
            return jsonResponse({ error: "却下処理に失敗しました: " + rpcErr.message }, 500);
          }
          const r = rpcRes as {
            ok?: boolean;
            error?: string;
            space_id?: string;
            applicant_email?: string;
            applicant_name?: string | null;
            has_email?: boolean;
          };
          if (!r?.ok) {
            await writeAuditLog(sb2, opsEmail2, "ops_db", "reject_space", spaceId, "denied", r?.error || "unknown", ip);
            const errorMap: Record<string, string> = {
              "space not found": "施設が見つかりません",
              "already rejected": "既に却下済みです",
              "cannot reject a live space": "公開済みの施設は却下できません (一旦非公開にしてください)"
            };
            return jsonResponse({ error: errorMap[r?.error || ""] || r?.error || "却下に失敗しました" }, 400);
          }

          // 通知メール送信 (contact_emailがある場合のみ)
          let mailResult: { ok: boolean; error?: string } = { ok: true };
          if (r.has_email && r.applicant_email) {
            mailResult = await sendOwnerRejectEmail(
              r.applicant_email,
              r.applicant_name || null
            );
          }

          await writeAuditLog(sb2, opsEmail2, "ops_db", "reject_space", spaceId, mailResult.ok ? "ok" : "mail_failed", mailResult.ok ? null : (mailResult.error || null), ip);

          return jsonResponse({
            ok: true,
            space_id: r.space_id,
            mail_sent: mailResult.ok,
            mail_warning: mailResult.ok ? null : "却下処理は完了しましたが、 通知メールの送信に失敗しました"
          });
        }

        return jsonResponse({ error: "不明なアクション: " + action }, 400);
      } catch (e) {
        return jsonResponse({ error: "プロキシ処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
      }
    }

    // ============================================================
    // target=accounts_admin: 運営管理画面用のアカウント管理
    // accounts テーブル(独自JWT認証)と auth.users(Supabase Auth) を同期する
    // /ops でパスワード変更すると /login(Supabase Auth) と /admin(独自) 両方でログイン可能になる
    // ============================================================
    if (target === "accounts_admin") {
      if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
      let opsPayloadA: any;
      try {
        const key = await getKey(JWT_SECRET);
        opsPayloadA = await verify(token, key);
      } catch (_e) {
        return jsonResponse({ error: "認証トークンが無効または期限切れです(再ログインしてください)" }, 401);
      }
      if (opsPayloadA.kind !== "ops") {
        return jsonResponse({ error: "このトークンは運営管理画面用ではありません" }, 401);
      }
      const opsEmailA = (opsPayloadA.sub || "").toLowerCase();
      if (!opsEmailA) return jsonResponse({ error: "トークンにメールアドレスが含まれていません" }, 401);

      const sbA = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
      const { data: stillAllowedA } = await sbA
        .from("ops_allowed_users").select("email").eq("email", opsEmailA).maybeSingle();
      if (!stillAllowedA) {
        return jsonResponse({ error: "アクセス権限が削除されています。再ログインしてください。" }, 403);
      }

      if (!checkRateLimit("accounts_admin:" + opsEmailA + ":" + action)) {
        return jsonResponse({ error: "短時間に多くの操作を行いました。しばらくお待ちください。" }, 429);
      }

      const authHeadersA: Record<string, string> = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
      };
      const restBaseA = SUPABASE_URL + "/rest/v1/";
      const emailReA = /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/;

      // ヘルパー: メールで auth.users を検索 (filter は部分一致なので exact match を JS で確認)
      const findAuthUserByEmailA = async (email: string): Promise<{ id: string; email: string } | null> => {
        try {
          const r = await fetch(SUPABASE_URL + "/auth/v1/admin/users?filter=" + encodeURIComponent(email) + "&per_page=50", {
            headers: authHeadersA
          });
          if (!r.ok) return null;
          const j = await r.json();
          const users = j.users || [];
          const lower = email.toLowerCase();
          return users.find((u: any) => (u.email || "").toLowerCase() === lower) || null;
        } catch (_e) {
          return null;
        }
      };

      const dA = data || {};

      try {
        // -------- accounts_admin:create --------
        if (action === "create") {
          const email = ((dA.email || "") + "").toLowerCase().trim();
          const password = (dA.password || "") + "";
          const company = ((dA.company || "") + "").trim();
          const plan = (dA.plan || "free") + "";
          const note = dA.note ? ((dA.note || "") + "") : null;

          if (!emailReA.test(email) || email.length > 254) {
            return jsonResponse({ error: "メールアドレスの形式が正しくありません" }, 400);
          }
          if (password.length < 8 || password.length > 200) {
            return jsonResponse({ error: "パスワードは8〜200文字で入力してください" }, 400);
          }
          if (!company || company.length > 200) {
            return jsonResponse({ error: "会社名を入力してください(200文字以内)" }, 400);
          }
          if (!["free", "standard", "pro"].includes(plan)) {
            return jsonResponse({ error: "plan は free/standard/pro のいずれかです" }, 400);
          }

          // 1) auth.users 既存チェック
          const existingAuth = await findAuthUserByEmailA(email);
          if (existingAuth) {
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "create", null, "error", "auth user already exists: " + email, ip);
            return jsonResponse({ error: "このメールアドレスは既に Supabase Auth に登録されています" }, 409);
          }

          // 2) auth.users を作成 (email_confirm: true で /login 即可能に)
          const authCreateRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users", {
            method: "POST",
            headers: authHeadersA,
            body: JSON.stringify({ email, password, email_confirm: true })
          });
          const authCreated = await authCreateRes.json().catch(() => ({}));
          if (!authCreateRes.ok || !authCreated.id) {
            const errMsg = authCreated.msg || authCreated.message || authCreated.error_description || ("HTTP " + authCreateRes.status);
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "create", null, "error", "auth create failed: " + (errMsg + "").substring(0, 200), ip);
            return jsonResponse({ error: "Supabase Auth ユーザー作成に失敗しました: " + errMsg }, 500);
          }

          // 3) accounts に挿入 (既存 RPC を使用 → password ハッシュ化等の既存ロジックを活かす)
          const rpcRes = await fetch(restBaseA + "rpc/create_account", {
            method: "POST",
            headers: authHeadersA,
            body: JSON.stringify({
              p_company: company,
              p_email: email,
              p_password: password,
              p_plan: plan,
              p_note: note
            })
          });
          const rpcText = await rpcRes.text();
          if (!rpcRes.ok) {
            // ロールバック: auth.users を削除
            await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + authCreated.id, {
              method: "DELETE",
              headers: authHeadersA
            }).catch(() => {});
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "create", null, "error", "accounts insert failed (rolled back auth): " + rpcText.substring(0, 200), ip);
            return jsonResponse({ error: "accounts テーブル作成に失敗しました: " + rpcText.substring(0, 200) }, 500);
          }

          await writeAuditLog(sbA, opsEmailA, "accounts_admin", "create", email, "ok", null, ip);
          return jsonResponse({ ok: true, auth_id: authCreated.id, accounts_result: rpcText });
        }

        // -------- accounts_admin:update --------
        if (action === "update") {
          const id = (dA.id || "") + "";
          if (!id) return jsonResponse({ error: "id が必要です" }, 400);

          const company = dA.company !== undefined ? ((dA.company || "") + "").trim() : null;
          const newEmailRaw = dA.email !== undefined ? ((dA.email || "") + "").toLowerCase().trim() : null;
          const password = dA.password ? ((dA.password || "") + "") : "";
          const plan = dA.plan !== undefined ? ((dA.plan || "") + "") : null;
          const note = dA.note !== undefined ? (dA.note ? ((dA.note || "") + "") : null) : null;

          if (newEmailRaw !== null && newEmailRaw && (!emailReA.test(newEmailRaw) || newEmailRaw.length > 254)) {
            return jsonResponse({ error: "メールアドレスの形式が正しくありません" }, 400);
          }
          if (password && (password.length < 8 || password.length > 200)) {
            return jsonResponse({ error: "パスワードは8〜200文字で入力してください" }, 400);
          }
          if (plan && !["free", "standard", "pro"].includes(plan)) {
            return jsonResponse({ error: "plan は free/standard/pro のいずれかです" }, 400);
          }

          // 現在の accounts を取得 (旧 email を取得するため)
          const curRes = await fetch(restBaseA + "accounts?id=eq." + encodeURIComponent(id) + "&select=email", {
            headers: authHeadersA
          });
          const curData = await curRes.json().catch(() => []);
          if (!Array.isArray(curData) || curData.length === 0) {
            return jsonResponse({ error: "対象のアカウントが見つかりません" }, 404);
          }
          const oldEmail = ((curData[0].email || "") + "").toLowerCase();
          const targetEmail = newEmailRaw || oldEmail;

          // 1) accounts を更新 (既存 RPC)
          const rpcRes = await fetch(restBaseA + "rpc/update_account", {
            method: "POST",
            headers: authHeadersA,
            body: JSON.stringify({
              p_id: id,
              p_company: company,
              p_email: newEmailRaw,
              p_plan: plan,
              p_password: password || null,
              p_note: note
            })
          });
          const rpcText = await rpcRes.text();
          if (!rpcRes.ok) {
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "update", id, "error", "accounts update failed: " + rpcText.substring(0, 200), ip);
            return jsonResponse({ error: "accounts テーブル更新に失敗しました: " + rpcText.substring(0, 200) }, 500);
          }

          // 2) auth.users を同期
          // 旧 email でユーザーを探す
          const authUser = await findAuthUserByEmailA(oldEmail);
          let authSyncWarning: string | null = null;

          if (authUser) {
            // 既存ユーザーを更新
            const authBody: any = {};
            if (newEmailRaw && newEmailRaw !== oldEmail) {
              authBody.email = newEmailRaw;
              authBody.email_confirm = true;
            }
            if (password) {
              authBody.password = password;
            }
            if (Object.keys(authBody).length > 0) {
              const upRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + authUser.id, {
                method: "PUT",
                headers: authHeadersA,
                body: JSON.stringify(authBody)
              });
              if (!upRes.ok) {
                const errText = await upRes.text();
                authSyncWarning = "Supabase Auth 更新に失敗しました: " + errText.substring(0, 200);
              }
            }
          } else {
            // auth.users に存在しない (旧来のレガシーアカウント等)
            // password がある場合のみ新規作成する
            if (password) {
              const authCreateRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users", {
                method: "POST",
                headers: authHeadersA,
                body: JSON.stringify({ email: targetEmail, password, email_confirm: true })
              });
              if (!authCreateRes.ok) {
                const errText = await authCreateRes.text();
                authSyncWarning = "Supabase Auth ユーザー作成に失敗しました: " + errText.substring(0, 200);
              }
            } else {
              authSyncWarning = "Supabase Auth に該当ユーザーが存在しません。/login でログイン可能にするにはパスワードを設定して再保存してください。";
            }
          }

          if (authSyncWarning) {
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "update", id, "error", "auth sync: " + authSyncWarning.substring(0, 200), ip);
            return jsonResponse({ ok: true, warning: authSyncWarning });
          }

          await writeAuditLog(sbA, opsEmailA, "accounts_admin", "update", id, "ok", null, ip);
          return jsonResponse({ ok: true });
        }

        // -------- accounts_admin:delete --------
        if (action === "delete") {
          const id = (dA.id || "") + "";
          if (!id) return jsonResponse({ error: "id が必要です" }, 400);

          // 現在の accounts を取得 (email 取得のため)
          const curRes = await fetch(restBaseA + "accounts?id=eq." + encodeURIComponent(id) + "&select=email", {
            headers: authHeadersA
          });
          const curData = await curRes.json().catch(() => []);
          if (!Array.isArray(curData) || curData.length === 0) {
            return jsonResponse({ error: "対象のアカウントが見つかりません" }, 404);
          }
          const targetEmailDel = ((curData[0].email || "") + "").toLowerCase();

          // 1) accounts を削除
          const delRes = await fetch(restBaseA + "accounts?id=eq." + encodeURIComponent(id), {
            method: "DELETE",
            headers: authHeadersA
          });
          if (!delRes.ok) {
            const errText = await delRes.text();
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "delete", id, "error", "accounts delete failed: " + errText.substring(0, 200), ip);
            return jsonResponse({ error: "accounts テーブル削除に失敗しました: " + errText.substring(0, 200) }, 500);
          }

          // 2) auth.users を削除 (見つからなくてもエラーにしない)
          let authDelWarning: string | null = null;
          if (targetEmailDel) {
            const authUserDel = await findAuthUserByEmailA(targetEmailDel);
            if (authUserDel) {
              const aDelRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + authUserDel.id, {
                method: "DELETE",
                headers: authHeadersA
              });
              if (!aDelRes.ok) {
                const errText = await aDelRes.text();
                authDelWarning = "Supabase Auth ユーザー削除に失敗しました: " + errText.substring(0, 200);
              }
            }
          }

          if (authDelWarning) {
            await writeAuditLog(sbA, opsEmailA, "accounts_admin", "delete", id, "error", "auth sync: " + authDelWarning.substring(0, 200), ip);
            return jsonResponse({ ok: true, warning: authDelWarning });
          }

          await writeAuditLog(sbA, opsEmailA, "accounts_admin", "delete", id, "ok", null, ip);
          return jsonResponse({ ok: true });
        }

        return jsonResponse({ error: "不明なアクション: " + action }, 400);
      } catch (e) {
        return jsonResponse({ error: "処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
      }
    }

    // ============================================================
    // target=writer_admin: 運営管理画面用のジャーナルライター管理
    // (target=writer は掲載者JWT専用なので /ops からは使えない。こちらは ops_token で動く)
    // ============================================================
    if (target === "writer_admin") {
      if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
      let opsPayloadW: any;
      try {
        const key = await getKey(JWT_SECRET);
        opsPayloadW = await verify(token, key);
      } catch (_e) {
        return jsonResponse({ error: "認証トークンが無効または期限切れです(再ログインしてください)" }, 401);
      }
      if (opsPayloadW.kind !== "ops") {
        return jsonResponse({ error: "このトークンは運営管理画面用ではありません" }, 401);
      }
      const opsEmailW = (opsPayloadW.sub || "").toLowerCase();
      if (!opsEmailW) return jsonResponse({ error: "トークンにメールアドレスが含まれていません" }, 401);

      const sbW = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
      const { data: stillAllowedW } = await sbW
        .from("ops_allowed_users").select("email").eq("email", opsEmailW).maybeSingle();
      if (!stillAllowedW) {
        return jsonResponse({ error: "アクセス権限が削除されています。再ログインしてください。" }, 403);
      }

      if (!checkRateLimit("writer_admin:" + opsEmailW + ":" + action)) {
        return jsonResponse({ error: "短時間に多くの操作を行いました。しばらくお待ちください。" }, 429);
      }

      const authHeadersW: Record<string, string> = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
        "Content-Type": "application/json",
      };
      const emailReW = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
      const dW = data || {};

      try {
        // -------- writer_admin:list --------
        if (action === "list") {
          const { data: writers, error } = await sbW
            .from("journal_writers")
            .select("id,user_id,display_name,bio,role,status,created_at,last_login_at")
            .order("created_at", { ascending: false });
          if (error) {
            await writeAuditLog(sbW, opsEmailW, "writer_admin", "list", null, "error", error.message, ip);
            return jsonResponse({ error: error.message }, 500);
          }
          const enriched = [];
          for (const w of writers || []) {
            try {
              const userRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + w.user_id, {
                headers: authHeadersW
              });
              const user = await userRes.json();
              enriched.push({ ...w, email: user?.email || null });
            } catch (_e) {
              enriched.push({ ...w, email: null });
            }
          }
          return jsonResponse({ ok: true, data: enriched });
        }

        // -------- writer_admin:create --------
        if (action === "create") {
          if (!dW.email || typeof dW.email !== "string" || !emailReW.test(dW.email) || dW.email.length > 254) {
            return jsonResponse({ error: "正しいメールアドレスを入力してください" }, 400);
          }
          if (!dW.password || typeof dW.password !== "string" || dW.password.length < 8 || dW.password.length > 200) {
            return jsonResponse({ error: "パスワードは8〜200文字で入力してください" }, 400);
          }
          if (!dW.display_name || typeof dW.display_name !== "string" || dW.display_name.length < 1 || dW.display_name.length > 100) {
            return jsonResponse({ error: "表示名は1〜100文字で入力してください" }, 400);
          }
          if (dW.bio && (typeof dW.bio !== "string" || dW.bio.length > 1000)) {
            return jsonResponse({ error: "bio は1000文字以内で入力してください" }, 400);
          }
          const createRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users", {
            method: "POST",
            headers: authHeadersW,
            body: JSON.stringify({
              email: dW.email,
              password: dW.password,
              email_confirm: true,
              user_metadata: { display_name: dW.display_name, role: "writer" }
            })
          });
          const created = await createRes.json();
          if (!createRes.ok || !created.id) {
            await writeAuditLog(sbW, opsEmailW, "writer_admin", "create", null, "error", created.msg || created.message || "auth create failed", ip);
            return jsonResponse({ error: created.msg || created.message || "ユーザー作成に失敗しました" }, createRes.status || 500);
          }
          const { data: writer, error } = await sbW.from("journal_writers").insert({
            user_id: created.id,
            display_name: dW.display_name,
            bio: dW.bio || null,
            role: "writer",
            status: "active",
            invited_by: opsEmailW
          }).select().single();
          if (error) {
            // ロールバック
            await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + created.id, {
              method: "DELETE",
              headers: authHeadersW
            }).catch(() => {});
            await writeAuditLog(sbW, opsEmailW, "writer_admin", "create", null, "error", error.message, ip);
            return jsonResponse({ error: error.message }, 500);
          }
          await writeAuditLog(sbW, opsEmailW, "writer_admin", "create", created.id, "ok", null, ip);
          return jsonResponse({ ok: true, data: writer });
        }

        // -------- writer_admin:update --------
        if (action === "update") {
          if (!id) return jsonResponse({ error: "id が必要です" }, 400);
          const updateData: any = {};
          if (dW.display_name !== undefined) {
            if (typeof dW.display_name !== "string" || dW.display_name.length < 1 || dW.display_name.length > 100) {
              return jsonResponse({ error: "表示名は1〜100文字で入力してください" }, 400);
            }
            updateData.display_name = dW.display_name;
          }
          if (dW.bio !== undefined) {
            if (dW.bio !== null && (typeof dW.bio !== "string" || dW.bio.length > 1000)) {
              return jsonResponse({ error: "bio は1000文字以内で入力してください" }, 400);
            }
            updateData.bio = dW.bio;
          }
          if (dW.status !== undefined) {
            if (!["active", "suspended"].includes(dW.status)) {
              return jsonResponse({ error: "status は active か suspended のいずれか" }, 400);
            }
            updateData.status = dW.status;
          }
          if (Object.keys(updateData).length === 0) {
            return jsonResponse({ error: "更新するフィールドがありません" }, 400);
          }
          const { data: updated, error } = await sbW.from("journal_writers").update(updateData).eq("id", id).select().single();
          if (error) {
            await writeAuditLog(sbW, opsEmailW, "writer_admin", "update", id, "error", error.message, ip);
            return jsonResponse({ error: error.message }, 500);
          }
          await writeAuditLog(sbW, opsEmailW, "writer_admin", "update", id, "ok", null, ip);
          return jsonResponse({ ok: true, data: updated });
        }

        // -------- writer_admin:reset_password --------
        if (action === "reset_password") {
          if (!id) return jsonResponse({ error: "id が必要です" }, 400);
          if (!dW.new_password || typeof dW.new_password !== "string" || dW.new_password.length < 8 || dW.new_password.length > 200) {
            return jsonResponse({ error: "新しいパスワードは8〜200文字" }, 400);
          }
          const { data: writer, error: wErr } = await sbW.from("journal_writers").select("user_id").eq("id", id).single();
          if (wErr || !writer) {
            return jsonResponse({ error: "ライターが見つかりません" }, 404);
          }
          const updateRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + writer.user_id, {
            method: "PUT",
            headers: authHeadersW,
            body: JSON.stringify({ password: dW.new_password })
          });
          if (!updateRes.ok) {
            const err = await updateRes.text();
            await writeAuditLog(sbW, opsEmailW, "writer_admin", "reset_password", id, "error", err.substring(0, 200), ip);
            return jsonResponse({ error: "パスワード変更に失敗しました" }, 500);
          }
          await writeAuditLog(sbW, opsEmailW, "writer_admin", "reset_password", id, "ok", null, ip);
          return jsonResponse({ ok: true });
        }

        // -------- writer_admin:delete --------
        if (action === "delete") {
          if (!id) return jsonResponse({ error: "id が必要です" }, 400);
          const { data: writer, error: wErr } = await sbW.from("journal_writers").select("user_id").eq("id", id).single();
          if (wErr || !writer) {
            return jsonResponse({ error: "ライターが見つかりません" }, 404);
          }
          await sbW.from("articles").update({ author_user_id: null }).eq("author_user_id", writer.user_id);
          await sbW.from("journal_writers").delete().eq("id", id);
          await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + writer.user_id, {
            method: "DELETE",
            headers: authHeadersW
          }).catch(() => {});
          await writeAuditLog(sbW, opsEmailW, "writer_admin", "delete", id, "ok", null, ip);
          return jsonResponse({ ok: true });
        }

        return jsonResponse({ error: "不明なアクション: " + action }, 400);
      } catch (e) {
        return jsonResponse({ error: "処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
      }
    }

    // ============================================================
    // 以降は既存の accounts テーブル経由 (掲載者向け) の処理
    // ============================================================
    if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);

    let payload: any;
    try {
      const key = await getKey(JWT_SECRET);
      payload = await verify(token, key);
    } catch (_e) {
      return jsonResponse({ error: "認証トークンが無効または期限切れです（再ログインしてください）" }, 401);
    }

    const accountId = payload.id;
    if (!accountId) return jsonResponse({ error: "トークンにアカウントIDが含まれていません" }, 401);

    // Rate limit: per-account + target+action combo
    const rateKey = `${accountId}:${target}:${action}`;
    if (!checkRateLimit(rateKey)) {
      return jsonResponse({ error: "短時間に多くの操作を行いました。しばらくお待ちください。" }, 429);
    }

    const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    const { data: ac, error: acErr } = await sb
      .from("accounts").select("id,status").eq("id", accountId).single();
    if (acErr || !ac) return jsonResponse({ error: "アカウントが見つかりません" }, 401);
    if (ac.status !== "active") return jsonResponse({ error: "アカウントが無効化されています" }, 403);


    // ============ account_self (施設運営者本人のアカウント情報変更) ============
    if (target === "account_self") {
      const dS = data || {};

      // -------- account_self:change_password --------
      if (action === "change_password") {
        const oldPass = (dS.old_password || "") + "";
        const newPass = (dS.new_password || "") + "";
        if (!oldPass || !newPass) {
          return jsonResponse({ error: "現在のパスワードと新しいパスワードを入力してください" }, 400);
        }
        if (newPass.length < 8 || newPass.length > 200) {
          return jsonResponse({ error: "新しいパスワードは8〜200文字で入力してください" }, 400);
        }
        if (oldPass === newPass) {
          return jsonResponse({ error: "新しいパスワードは現在のパスワードと異なるものにしてください" }, 400);
        }
        const { data: rpcRes, error: rpcErr } = await sb.rpc("change_account_password", {
          p_account_id: accountId,
          p_old_pass: oldPass,
          p_new_pass: newPass
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, null, "error", rpcErr.message, ip);
          return jsonResponse({ error: "パスワード変更に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string };
        if (!r?.ok) {
          await writeAuditLog(sb, accountId, target, action, null, "denied", r?.error || "unknown", ip);
          if (r?.error === "invalid current password") {
            return jsonResponse({ error: "現在のパスワードが正しくありません" }, 401);
          }
          return jsonResponse({ error: r?.error || "パスワード変更に失敗しました" }, 400);
        }
        await writeAuditLog(sb, accountId, target, action, null, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      // -------- account_self:change_email --------
      if (action === "change_email") {
        const oldPass = (dS.old_password || "") + "";
        const newEmail = ((dS.new_email || "") + "").toLowerCase().trim();
        if (!oldPass || !newEmail) {
          return jsonResponse({ error: "現在のパスワードと新しいメールアドレスを入力してください" }, 400);
        }
        if (newEmail.length > 254 || !/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(newEmail)) {
          return jsonResponse({ error: "メールアドレスの形式が正しくありません" }, 400);
        }
        const { data: rpcRes, error: rpcErr } = await sb.rpc("change_account_email", {
          p_account_id: accountId,
          p_old_pass: oldPass,
          p_new_email: newEmail
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, null, "error", rpcErr.message, ip);
          return jsonResponse({ error: "メールアドレス変更に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string };
        if (!r?.ok) {
          await writeAuditLog(sb, accountId, target, action, null, "denied", r?.error || "unknown", ip);
          if (r?.error === "invalid current password") {
            return jsonResponse({ error: "現在のパスワードが正しくありません" }, 401);
          }
          if (r?.error === "email already in use") {
            return jsonResponse({ error: "このメールアドレスは既に他のアカウントで使用されています" }, 409);
          }
          return jsonResponse({ error: r?.error || "メールアドレス変更に失敗しました" }, 400);
        }
        await writeAuditLog(sb, accountId, target, action, null, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "account_self では change_password または change_email を指定してください" }, 400);
    }

    // ============ account_managers (Owner: 担当者管理) ============
    if (target === "account_managers") {
      const dM = data || {};

      // Owner権限チェック (manager は担当者管理不可)
      if (payload.kind && payload.kind !== "owner") {
        return jsonResponse({ error: "担当者管理は管理者(Owner)のみ実行可能です" }, 403);
      }

      // -------- list --------
      if (action === "list") {
        const { data: list, error } = await sb
          .from("account_managers")
          .select("id, email, display_name, role, status, created_at, last_login_at")
          .eq("account_id", accountId)
          .order("created_at", { ascending: false });
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: "担当者一覧の取得に失敗しました" }, 500);
        }
        return jsonResponse({ ok: true, managers: list || [] });
      }

      // -------- create (招待メール送信) --------
      if (action === "create") {
        const mEmail = ((dM.email || "") + "").toLowerCase().trim();
        const mDisplayName = dM.display_name ? (((dM.display_name || "") + "").trim() || null) : null;
        const mRole = ((dM.role || "manager") + "") as string;

        if (!mEmail) {
          return jsonResponse({ error: "メールアドレスは必須です" }, 400);
        }
        if (!["manager", "viewer"].includes(mRole)) {
          return jsonResponse({ error: "権限は manager / viewer のいずれかで指定してください" }, 400);
        }

        // 招待レコード作成（pending status, token発行）
        const { data: rpcRes, error: rpcErr } = await sb.rpc("create_account_manager_invite", {
          p_account_id: accountId,
          p_email: mEmail,
          p_display_name: mDisplayName,
          p_role: mRole
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, null, "error", rpcErr.message, ip);
          return jsonResponse({ error: "招待の作成に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string; id?: string; invite_token?: string };
        if (!r?.ok) {
          const errorMap: Record<string, string> = {
            "invalid email format": "メールアドレスの形式が正しくありません",
            "invalid role": "権限の指定が正しくありません",
            "account not found": "アカウントが見つかりません",
            "email already in use": "このメールアドレスは既に使用されています"
          };
          await writeAuditLog(sb, accountId, target, action, null, "denied", r?.error || "unknown", ip);
          return jsonResponse({ error: errorMap[r?.error || ""] || r?.error || "招待の作成に失敗しました" }, 400);
        }

        // company名取得 (メール本文用)
        const { data: acc } = await sb.from("accounts").select("company").eq("id", accountId).single();
        const company = (acc?.company || "管理者") as string;

        // 招待メール送信
        const mailRes = await sendInviteEmail(mEmail, mDisplayName, company, mRole, r.invite_token!);

        await writeAuditLog(sb, accountId, target, action, r.id || null, mailRes.ok ? "ok" : "mail_failed", mailRes.ok ? null : mailRes.error || null, ip);

        if (!mailRes.ok) {
          return jsonResponse({
            ok: true,
            id: r.id,
            mail_warning: "招待は作成されましたが、メール送信に失敗しました。一覧の「招待メール再送」ボタンから再送してください。"
          });
        }
        return jsonResponse({ ok: true, id: r.id });
      }

      // -------- resend_invite (招待メール再送) --------
      if (action === "resend_invite") {
        const managerId = ((dM.manager_id || "") + "").trim();
        if (!managerId) return jsonResponse({ error: "manager_id が必要です" }, 400);

        // token再生成
        const { data: rpcRes, error: rpcErr } = await sb.rpc("regenerate_manager_invite", {
          p_account_id: accountId,
          p_manager_id: managerId
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, managerId, "error", rpcErr.message, ip);
          return jsonResponse({ error: "再送に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string; invite_token?: string; email?: string; display_name?: string | null; role?: string };
        if (!r?.ok) {
          const errorMap: Record<string, string> = {
            "manager not found in this account": "対象の担当者が見つかりません",
            "manager already activated": "この担当者は既にパスワード設定済みです"
          };
          await writeAuditLog(sb, accountId, target, action, managerId, "denied", r?.error || "unknown", ip);
          return jsonResponse({ error: errorMap[r?.error || ""] || r?.error || "再送に失敗しました" }, 400);
        }

        const { data: acc } = await sb.from("accounts").select("company").eq("id", accountId).single();
        const company = (acc?.company || "管理者") as string;

        const mailRes = await sendInviteEmail(r.email!, r.display_name || null, company, r.role || "manager", r.invite_token!);

        await writeAuditLog(sb, accountId, target, action, managerId, mailRes.ok ? "ok" : "mail_failed", mailRes.ok ? null : mailRes.error || null, ip);

        if (!mailRes.ok) {
          return jsonResponse({ error: "メール送信に失敗しました。RESEND_API_KEYを確認してください。" }, 500);
        }
        return jsonResponse({ ok: true });
      }

      // -------- change_role (権限変更) --------
      if (action === "change_role") {
        const managerId = ((dM.manager_id || "") + "").trim();
        const newRole = ((dM.role || "") + "").trim();
        if (!managerId) return jsonResponse({ error: "manager_id が必要です" }, 400);
        if (!["manager", "viewer"].includes(newRole)) {
          return jsonResponse({ error: "権限は manager / viewer のいずれかで指定してください" }, 400);
        }

        const { data: rpcRes, error: rpcErr } = await sb.rpc("change_manager_role", {
          p_account_id: accountId,
          p_manager_id: managerId,
          p_new_role: newRole
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, managerId, "error", rpcErr.message, ip);
          return jsonResponse({ error: "権限変更に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string; unchanged?: boolean };
        if (!r?.ok) {
          const errorMap: Record<string, string> = {
            "invalid role": "権限の指定が正しくありません",
            "manager not found in this account": "対象の担当者が見つかりません"
          };
          await writeAuditLog(sb, accountId, target, action, managerId, "denied", r?.error || "unknown", ip);
          return jsonResponse({ error: errorMap[r?.error || ""] || r?.error || "権限変更に失敗しました" }, 400);
        }
        await writeAuditLog(sb, accountId, target, action, managerId, r.unchanged ? "no_change" : "ok", null, ip);
        return jsonResponse({ ok: true, unchanged: !!r.unchanged });
      }

      // -------- delete --------
      if (action === "delete") {
        const managerId = ((dM.manager_id || "") + "").trim();
        if (!managerId) return jsonResponse({ error: "manager_id が必要です" }, 400);

        const { data: rpcRes, error: rpcErr } = await sb.rpc("delete_account_manager", {
          p_account_id: accountId,
          p_manager_id: managerId
        });
        if (rpcErr) {
          await writeAuditLog(sb, accountId, target, action, managerId, "error", rpcErr.message, ip);
          return jsonResponse({ error: "担当者削除に失敗しました" }, 500);
        }
        const r = rpcRes as { ok?: boolean; error?: string };
        if (!r?.ok) {
          await writeAuditLog(sb, accountId, target, action, managerId, "denied", r?.error || "unknown", ip);
          return jsonResponse({ error: r?.error === "manager not found in this account" ? "対象の担当者が見つかりません" : r?.error || "担当者削除に失敗しました" }, 400);
        }
        await writeAuditLog(sb, accountId, target, action, managerId, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "account_managers では list / create / resend_invite / change_role / delete を指定してください" }, 400);
    }

    // ============ voice (利用者の声) ============
    if (target === "voice") {
      if (!id) return jsonResponse({ error: "voice IDが必要です" }, 400);
      const { data: voice } = await sb.from("voices").select("id,space_id").eq("id", id).single();
      if (!voice) return jsonResponse({ error: "対象のレビューが見つかりません" }, 404);
      const { data: vSp } = await sb.from("spaces").select("id,account_id").eq("id", voice.space_id).single();
      if (!vSp) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      if (vSp.account_id !== accountId) {
        await writeAuditLog(sb, accountId, target, action, id, "denied", "ownership_check_failed", ip);
        return jsonResponse({ error: "権限がありません" }, 403);
      }

      if (action === "approve") {
        const { data: u, error } = await sb.from("voices").update({ status: "approved" }).eq("id", id).select();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, voice: u?.[0] });
      } else if (action === "reject") {
        const { data: u, error } = await sb.from("voices").update({ status: "rejected" }).eq("id", id).select();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, voice: u?.[0] });
      } else if (action === "delete") {
        const { error } = await sb.from("voices").delete().eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============ space (施設) ============
    if (target === "space") {
      if (action === "insert") {
        const insertData = { ...(data || {}), account_id: accountId };
        delete insertData.id;
        const { data: _acctPlan } = await sb.from("accounts").select("plan").eq("id", accountId).single();
        if (_acctPlan && _acctPlan.plan) insertData.plan = _acctPlan.plan;
        const { data: created, error } = await sb.from("spaces").insert(insertData).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, created.id, "ok", null, ip);
        return jsonResponse({ ok: true, space: created });
      }

      if (!id) return jsonResponse({ error: "space IDが必要です" }, 400);
      const { data: space } = await sb.from("spaces").select("id,account_id").eq("id", id).single();
      if (!space) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      if (space.account_id !== accountId) {
        await writeAuditLog(sb, accountId, target, action, id, "denied", "ownership_check_failed", ip);
        return jsonResponse({ error: "権限がありません" }, 403);
      }

      if (action === "update") {
        const updateData = { ...(data || {}) };
        delete updateData.account_id;
        delete updateData.id;
        delete updateData.plan; // plan の改ざんを防止(Stripe Webhook 経由でのみ変更可能)
        const { data: u, error } = await sb.from("spaces").update(updateData).eq("id", id).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, space: u });
      } else if (action === "delete") {
        await sb.from("voices").delete().eq("space_id", id);
        await sb.from("space_images").delete().eq("space_id", id);
        const { error } = await sb.from("spaces").delete().eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============ space_image (施設写真) ============
    if (target === "space_image") {
      if (action === "insert") {
        const spaceId = data?.space_id;
        if (!spaceId) return jsonResponse({ error: "space_id が必要です" }, 400);
        const { data: spChk } = await sb.from("spaces").select("id,account_id").eq("id", spaceId).single();
        if (!spChk) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
        if (spChk.account_id !== accountId) {
          await writeAuditLog(sb, accountId, target, action, null, "denied", "ownership_check_failed", ip);
          return jsonResponse({ error: "権限がありません" }, 403);
        }
        const insertData = { ...(data || {}) };
        delete insertData.id;
        const { data: created, error } = await sb.from("space_images").insert(insertData).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, created.id, "ok", null, ip);
        return jsonResponse({ ok: true, image: created });
      }

      if (!id) return jsonResponse({ error: "space_image IDが必要です" }, 400);
      const { data: img } = await sb.from("space_images").select("id,space_id").eq("id", id).single();
      if (!img) return jsonResponse({ error: "対象画像が見つかりません" }, 404);
      const { data: iSp } = await sb.from("spaces").select("id,account_id").eq("id", img.space_id).single();
      if (!iSp) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      if (iSp.account_id !== accountId) {
        await writeAuditLog(sb, accountId, target, action, id, "denied", "ownership_check_failed", ip);
        return jsonResponse({ error: "権限がありません" }, 403);
      }

      if (action === "update") {
        const updateData = { ...(data || {}) };
        delete updateData.id; delete updateData.space_id;
        const { data: u, error } = await sb.from("space_images").update(updateData).eq("id", id).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, image: u });
      } else if (action === "delete") {
        const { error } = await sb.from("space_images").delete().eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============ Phase 3: architect (建築家) ============
    if (target === "architect") {
      // architects は account に紐づかず、運営側のマスタデータ。
      // 当面は登録済みユーザーなら誰でも追加できる(申請ベース)。
      // 将来的に super_admin 権限へ移行予定。
      if (action === "insert") {
        const insertData = { ...(data || {}) };
        delete insertData.id;
        // 入力バリデーション
        if (!insertData.name || typeof insertData.name !== "string" || insertData.name.length > 100) {
          return jsonResponse({ error: "建築家名が無効です(1〜100文字)" }, 400);
        }
        if (insertData.url && (typeof insertData.url !== "string" || insertData.url.length > 500)) {
          return jsonResponse({ error: "URLが無効です" }, 400);
        }
        // contact_status はホワイトリスト
        const allowedStatus = ["pending", "contacted", "approved", "declined"];
        if (insertData.contact_status && !allowedStatus.includes(insertData.contact_status)) {
          insertData.contact_status = "pending";
        }
        const { data: created, error } = await sb.from("architects").insert(insertData).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, created.id, "ok", null, ip);
        return jsonResponse({ ok: true, architect: created });
      }

      if (!id) return jsonResponse({ error: "architect IDが必要です" }, 400);
      const { data: arch } = await sb.from("architects").select("id").eq("id", id).single();
      if (!arch) return jsonResponse({ error: "対象建築家が見つかりません" }, 404);

      if (action === "update") {
        const updateData = { ...(data || {}) };
        delete updateData.id;
        if (updateData.name && (typeof updateData.name !== "string" || updateData.name.length > 100)) {
          return jsonResponse({ error: "建築家名が無効です" }, 400);
        }
        if (updateData.url && (typeof updateData.url !== "string" || updateData.url.length > 500)) {
          return jsonResponse({ error: "URLが無効です" }, 400);
        }
        const { data: u, error } = await sb.from("architects").update(updateData).eq("id", id).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, architect: u });
      } else if (action === "delete") {
        const { error } = await sb.from("architects").delete().eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============== article (COWORKMILL journal) ==============
    if (target === "article") {
      // 記事は account に紐づかず、運営マスターデータ。JWT を通れば編集可能。
      // 複数ライター(account 別 ownership)は Phase 5 で対応予定。
      if (!data && action !== "delete" && action !== "publish" && action !== "unpublish") {
        return jsonResponse({ error: "data が必要です" }, 400);
      }

      if (action === "list") {
        // status フィルタ可能。指定なければ全部返す。
        const filterStatus = (data && data.status) || null;
        let query = sb.from("articles").select("id,slug,title,subtitle,category,status,published_at,updated_at,tags,is_pr,reading_minutes,author_name,excerpt").order("updated_at", { ascending: false }).limit(200);
        if (filterStatus && ["draft","scheduled","live","archived"].includes(filterStatus)) {
          query = query.eq("status", filterStatus);
        }
        const { data: list, error } = await query;
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, data: list });
      }

      if (action === "get") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { data: row, error } = await sb.from("articles").select("*").eq("id", id).single();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, data: row });
      }

      if (action === "insert") {
        const insertData: any = { ...(data || {}) };
        delete insertData.id;
        delete insertData.created_at;
        delete insertData.view_count;
        delete insertData.published_at;
        delete insertData.body_html;

        if (!insertData.slug || typeof insertData.slug !== "string" || !/^[a-z0-9-]{1,100}$/.test(insertData.slug)) {
          return jsonResponse({ error: "slug が無効です(英小文字/数字/ハイフン、1〜100文字)" }, 400);
        }
        if (!insertData.title || typeof insertData.title !== "string" || insertData.title.length < 1 || insertData.title.length > 200) {
          return jsonResponse({ error: "タイトルが無効です(1〜200文字)" }, 400);
        }
        if (insertData.subtitle && (typeof insertData.subtitle !== "string" || insertData.subtitle.length > 300)) {
          return jsonResponse({ error: "サブタイトルが長すぎます(300文字以内)" }, 400);
        }
        if (!insertData.category || !["interview","trend","news","other"].includes(insertData.category)) {
          return jsonResponse({ error: "カテゴリが無効です" }, 400);
        }
        if (insertData.body_md && (typeof insertData.body_md !== "string" || insertData.body_md.length > 100000)) {
          return jsonResponse({ error: "本文が長すぎます(10万文字以内)" }, 400);
        }
        if (insertData.excerpt && (typeof insertData.excerpt !== "string" || insertData.excerpt.length > 500)) {
          return jsonResponse({ error: "概要が長すぎます(500文字以内)" }, 400);
        }
        if (insertData.tags && (!Array.isArray(insertData.tags) || insertData.tags.length > 20)) {
          return jsonResponse({ error: "タグは20個以内です" }, 400);
        }
        if (insertData.author_name && (typeof insertData.author_name !== "string" || insertData.author_name.length > 100)) {
          return jsonResponse({ error: "著者名が長すぎます(100文字以内)" }, 400);
        }
        if (insertData.hero_image && (typeof insertData.hero_image !== "string" || insertData.hero_image.length > 2000)) {
          return jsonResponse({ error: "hero_image URL が長すぎます" }, 400);
        }
        if (insertData.is_pr && !insertData.pr_disclosure) {
          return jsonResponse({ error: "PR記事には pr_disclosure が必須です" }, 400);
        }

        // 強制設定
        insertData.status = "draft"; // 新規は必ず draft
        if (!insertData.author_name) insertData.author_name = "COWORKMILL journal 編集部";

        const { data: created, error } = await sb.from("articles").insert(insertData).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, created.id, "ok", null, ip);
        return jsonResponse({ ok: true, data: created });
      }

      if (action === "update") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const updateData: any = { ...(data || {}) };
        delete updateData.id;
        delete updateData.created_at;
        delete updateData.view_count;
        delete updateData.body_html;

        if (updateData.slug !== undefined && !/^[a-z0-9-]{1,100}$/.test(updateData.slug)) {
          return jsonResponse({ error: "slug が無効です" }, 400);
        }
        if (updateData.title !== undefined && (typeof updateData.title !== "string" || updateData.title.length > 200)) {
          return jsonResponse({ error: "タイトルが無効です" }, 400);
        }
        if (updateData.category !== undefined && !["interview","trend","news","other"].includes(updateData.category)) {
          return jsonResponse({ error: "カテゴリが無効です" }, 400);
        }
        if (updateData.body_md !== undefined && updateData.body_md.length > 100000) {
          return jsonResponse({ error: "本文が長すぎます" }, 400);
        }
        if (updateData.status !== undefined && !["draft","scheduled","live","archived"].includes(updateData.status)) {
          return jsonResponse({ error: "status が無効です" }, 400);
        }
        if (updateData.tags !== undefined && (!Array.isArray(updateData.tags) || updateData.tags.length > 20)) {
          return jsonResponse({ error: "タグは20個以内です" }, 400);
        }

        const { data: updated, error } = await sb.from("articles").update(updateData).eq("id", id).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, data: updated });
      }

      if (action === "publish") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { error } = await sb.from("articles").update({
          status: "live",
          published_at: new Date().toISOString()
        }).eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      if (action === "unpublish") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { error } = await sb.from("articles").update({ status: "draft" }).eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      if (action === "delete") {
        // soft delete: status=archived(履歴を残すため hard delete はしない)
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { error } = await sb.from("articles").update({ status: "archived" }).eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "不明な操作: " + action }, 400);
    }

    // ============== media (記事画像、出所必須) ==============
    if (target === "media") {
      if (action === "insert") {
        const insertData: any = { ...(data || {}) };
        delete insertData.id;
        delete insertData.uploaded_at;

        if (!insertData.url || typeof insertData.url !== "string" || insertData.url.length > 2000) {
          return jsonResponse({ error: "url が無効です" }, 400);
        }
        if (!insertData.alt_text || typeof insertData.alt_text !== "string" || insertData.alt_text.length < 1 || insertData.alt_text.length > 500) {
          return jsonResponse({ error: "alt_text は必須です(1〜500文字、アクセシビリティ要件)" }, 400);
        }
        if (!insertData.source_type || !["own","facility","stock","ai","cc"].includes(insertData.source_type)) {
          return jsonResponse({ error: "source_type は必須です(own/facility/stock/ai/cc)" }, 400);
        }
        // 著作権周りの整合性チェック
        if (insertData.source_type === "facility" && !insertData.permission_note) {
          return jsonResponse({ error: "施設写真は permission_note(掲載許諾の記録)が必要です" }, 400);
        }
        if (insertData.source_type === "stock" && !insertData.source_name) {
          return jsonResponse({ error: "ストック写真は source_name(Unsplash 等)が必要です" }, 400);
        }
        if (insertData.source_url && (typeof insertData.source_url !== "string" || insertData.source_url.length > 2000)) {
          return jsonResponse({ error: "source_url が長すぎます" }, 400);
        }

        const { data: created, error } = await sb.from("media_assets").insert(insertData).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, created.id, "ok", null, ip);
        return jsonResponse({ ok: true, data: created });
      }

      if (action === "delete") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { error } = await sb.from("media_assets").delete().eq("id", id);
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "不明な操作: " + action }, 400);
    }


    // ============== writer (運営による journal ライター管理) ==============
    if (target === "writer") {
      if (action === "list") {
        const { data: writers, error } = await sb
          .from("journal_writers")
          .select("id,user_id,display_name,bio,role,status,created_at,last_login_at")
          .order("created_at", { ascending: false });
        if (error) {
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        const enriched = [];
        for (const w of writers || []) {
          try {
            const userRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + w.user_id, {
              headers: {
                "apikey": SUPABASE_SERVICE_KEY,
                "Authorization": "Bearer " + SUPABASE_SERVICE_KEY
              }
            });
            const user = await userRes.json();
            enriched.push({ ...w, email: user?.email || null });
          } catch (e) {
            enriched.push({ ...w, email: null });
          }
        }
        return jsonResponse({ ok: true, data: enriched });
      }

      if (action === "create") {
        const d = data || {};
        const emailRe = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!d.email || typeof d.email !== "string" || !emailRe.test(d.email) || d.email.length > 254) {
          return jsonResponse({ error: "正しいメールアドレスを入力してください" }, 400);
        }
        if (!d.password || typeof d.password !== "string" || d.password.length < 8 || d.password.length > 200) {
          return jsonResponse({ error: "パスワードは8〜200文字で入力してください" }, 400);
        }
        if (!d.display_name || typeof d.display_name !== "string" || d.display_name.length < 1 || d.display_name.length > 100) {
          return jsonResponse({ error: "表示名は1〜100文字で入力してください" }, 400);
        }
        if (d.bio && (typeof d.bio !== "string" || d.bio.length > 1000)) {
          return jsonResponse({ error: "bio は1000文字以内で入力してください" }, 400);
        }
        const createRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users", {
          method: "POST",
          headers: {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: d.email,
            password: d.password,
            email_confirm: true,
            user_metadata: { display_name: d.display_name, role: "writer" }
          })
        });
        const created = await createRes.json();
        if (!createRes.ok || !created.id) {
          await writeAuditLog(sb, accountId, target, action, null, "error", created.msg || created.message || "auth create failed", ip);
          return jsonResponse({ error: created.msg || created.message || "ユーザー作成に失敗しました" }, createRes.status || 500);
        }
        const { data: writer, error } = await sb.from("journal_writers").insert({
          user_id: created.id,
          display_name: d.display_name,
          bio: d.bio || null,
          role: "writer",
          status: "active",
          invited_by: accountId
        }).select().single();
        if (error) {
          await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + created.id, {
            method: "DELETE",
            headers: {
              "apikey": SUPABASE_SERVICE_KEY,
              "Authorization": "Bearer " + SUPABASE_SERVICE_KEY
            }
          });
          await writeAuditLog(sb, accountId, target, action, null, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, writer.id, "ok", null, ip);
        return jsonResponse({ ok: true, data: { ...writer, email: d.email } });
      }

      if (action === "update") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const d = data || {};
        const updateData: any = {};
        if (d.display_name !== undefined) {
          if (typeof d.display_name !== "string" || d.display_name.length < 1 || d.display_name.length > 100) {
            return jsonResponse({ error: "表示名は1〜100文字" }, 400);
          }
          updateData.display_name = d.display_name;
        }
        if (d.bio !== undefined) {
          if (d.bio !== null && (typeof d.bio !== "string" || d.bio.length > 1000)) {
            return jsonResponse({ error: "bio は1000文字以内" }, 400);
          }
          updateData.bio = d.bio;
        }
        if (d.status !== undefined) {
          if (!["active","suspended","deleted"].includes(d.status)) {
            return jsonResponse({ error: "status が無効です" }, 400);
          }
          updateData.status = d.status;
        }
        if (Object.keys(updateData).length === 0) {
          return jsonResponse({ error: "更新するフィールドがありません" }, 400);
        }
        const { data: updated, error } = await sb.from("journal_writers").update(updateData).eq("id", id).select().single();
        if (error) {
          await writeAuditLog(sb, accountId, target, action, id, "error", error.message, ip);
          return jsonResponse({ error: error.message }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true, data: updated });
      }

      if (action === "reset_password") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const d = data || {};
        if (!d.new_password || typeof d.new_password !== "string" || d.new_password.length < 8 || d.new_password.length > 200) {
          return jsonResponse({ error: "新しいパスワードは8〜200文字" }, 400);
        }
        const { data: writer, error: wErr } = await sb.from("journal_writers").select("user_id").eq("id", id).single();
        if (wErr || !writer) {
          return jsonResponse({ error: "ライターが見つかりません" }, 404);
        }
        const updateRes = await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + writer.user_id, {
          method: "PUT",
          headers: {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": "Bearer " + SUPABASE_SERVICE_KEY,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ password: d.new_password })
        });
        if (!updateRes.ok) {
          const err = await updateRes.text();
          await writeAuditLog(sb, accountId, target, action, id, "error", err.substring(0, 200), ip);
          return jsonResponse({ error: "パスワード変更に失敗しました" }, 500);
        }
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      if (action === "delete") {
        if (!id) return jsonResponse({ error: "id が必要です" }, 400);
        const { data: writer, error: wErr } = await sb.from("journal_writers").select("user_id").eq("id", id).single();
        if (wErr || !writer) {
          return jsonResponse({ error: "ライターが見つかりません" }, 404);
        }
        await sb.from("articles").update({ author_user_id: null }).eq("author_user_id", writer.user_id);
        await sb.from("journal_writers").delete().eq("id", id);
        await fetch(SUPABASE_URL + "/auth/v1/admin/users/" + writer.user_id, {
          method: "DELETE",
          headers: {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": "Bearer " + SUPABASE_SERVICE_KEY
          }
        });
        await writeAuditLog(sb, accountId, target, action, id, "ok", null, ip);
        return jsonResponse({ ok: true });
      }

      return jsonResponse({ error: "不明な操作: " + action }, 400);
    }


    return jsonResponse({ error: "不明な操作対象: " + target }, 400);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return jsonResponse({ error: msg }, 500);
  }
});
