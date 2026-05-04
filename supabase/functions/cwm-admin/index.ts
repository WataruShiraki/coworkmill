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

        return jsonResponse({ error: "不明なアクション: " + action }, 400);
      } catch (e) {
        return jsonResponse({ error: "プロキシ処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
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
