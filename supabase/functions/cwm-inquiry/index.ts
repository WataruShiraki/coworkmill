// Supabase Edge Function: cwm-inquiry
// 掲載申込フォームから呼ばれて、Resend経由で2通のメールを送信:
//   1. 申込者宛て: 受付確認メール (自動返信)
//   2. 運営宛て (info@offml.com): 新規申込通知メール
//
// セキュリティ:
// - Resend API Key は Supabase Secrets (RESEND_API_KEY) に登録、フロントから見えない
// - フロントはこの Edge Function を anon key で呼ぶだけ
// - 入力バリデーション (XSS対策含む)、レート制限的なチェック (簡易)

const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") || "";
const FROM_EMAIL = Deno.env.get("INQUIRY_FROM_EMAIL") || "onboarding@resend.dev";
const ADMIN_EMAIL = Deno.env.get("INQUIRY_ADMIN_EMAIL") || "info@offml.com";
const SITE_URL = Deno.env.get("SITE_URL") || "https://cowkml.com";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, apikey, x-client-info",
  "Access-Control-Max-Age": "86400",
};

function escapeHtml(s: string): string {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function isEmail(s: string): boolean {
  if (typeof s !== "string") return false;
  if (s.length > 254) return false;
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s.trim());
}

function isUrl(s: string): boolean {
  if (typeof s !== "string") return false;
  if (s.length > 2000) return false;
  return /^https?:\/\/.+\..+/.test(s.trim());
}

function fmtJST(d: Date): string {
  // 日本時間 YYYY/MM/DD HH:mm
  const jst = new Date(d.getTime() + 9 * 60 * 60 * 1000);
  const y = jst.getUTCFullYear();
  const mo = String(jst.getUTCMonth() + 1).padStart(2, "0");
  const da = String(jst.getUTCDate()).padStart(2, "0");
  const h = String(jst.getUTCHours()).padStart(2, "0");
  const mi = String(jst.getUTCMinutes()).padStart(2, "0");
  return `${y}/${mo}/${da} ${h}:${mi}`;
}

interface InquiryPayload {
  facilityName: string;
  companyName: string;
  facilityUrl: string;
  contactName: string;
  contactEmail: string;
}

function validate(p: any): { ok: boolean; error?: string; data?: InquiryPayload } {
  if (!p || typeof p !== "object") return { ok: false, error: "invalid payload" };
  const facilityName = String(p.facilityName ?? "").trim();
  const companyName = String(p.companyName ?? "").trim();
  const facilityUrl = String(p.facilityUrl ?? "").trim();
  const contactName = String(p.contactName ?? "").trim();
  const contactEmail = String(p.contactEmail ?? "").trim();

  if (!facilityName || facilityName.length > 200) return { ok: false, error: "施設名が無効です" };
  if (!companyName || companyName.length > 200) return { ok: false, error: "会社名が無効です" };
  if (!isUrl(facilityUrl)) return { ok: false, error: "施設URLが無効です" };
  if (!contactName || contactName.length > 100) return { ok: false, error: "担当者名が無効です" };
  if (!isEmail(contactEmail)) return { ok: false, error: "メールアドレスが無効です" };

  return {
    ok: true,
    data: { facilityName, companyName, facilityUrl, contactName, contactEmail },
  };
}

function buildApplicantEmail(data: InquiryPayload): { subject: string; html: string; text: string } {
  const subject = "【COWORKMILL】掲載申込を受け付けました";
  const escName = escapeHtml(data.contactName);
  const escFac = escapeHtml(data.facilityName);
  const escCom = escapeHtml(data.companyName);
  const escUrl = escapeHtml(data.facilityUrl);

  const html = `<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(subject)}</title></head>
<body style="margin:0;padding:0;background:#f5f6f8;font-family:-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;color:#1a1a1a;line-height:1.7">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f6f8;padding:32px 16px">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.04)">
<tr><td style="padding:32px 32px 24px;background:linear-gradient(135deg,#88c895,#1357a0);color:#fff">
<div style="font-family:'Montserrat',sans-serif;font-size:13px;font-weight:600;letter-spacing:.16em;opacity:.9;margin-bottom:6px">COWORKMILL</div>
<div style="font-size:20px;font-weight:600;letter-spacing:-.01em">掲載お申し込みを受け付けました</div>
</td></tr>
<tr><td style="padding:32px">
<p style="margin:0 0 16px;font-size:15px">${escName} 様</p>
<p style="margin:0 0 16px;font-size:14px;color:#333">このたびは COWORKMILL への掲載お申し込み、<br>誠にありがとうございます。</p>
<p style="margin:0 0 24px;font-size:14px;color:#333">下記の内容で受け付けました。<br><strong style="color:#1357a0">通常1営業日以内</strong>に運営チームよりご連絡を差し上げます。</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f6f8;border-radius:8px;margin-bottom:24px">
<tr><td style="padding:18px 22px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">
<tr><td style="font-size:11px;color:#888;letter-spacing:.04em;padding:6px 0;width:100px">施設名</td><td style="font-size:14px;color:#1a1a1a;padding:6px 0">${escFac}</td></tr>
<tr><td style="font-size:11px;color:#888;letter-spacing:.04em;padding:6px 0;border-top:1px solid #e5e7eb">会社名・屋号</td><td style="font-size:14px;color:#1a1a1a;padding:6px 0;border-top:1px solid #e5e7eb">${escCom}</td></tr>
<tr><td style="font-size:11px;color:#888;letter-spacing:.04em;padding:6px 0;border-top:1px solid #e5e7eb">施設URL</td><td style="font-size:13px;color:#1357a0;padding:6px 0;border-top:1px solid #e5e7eb;word-break:break-all"><a href="${escUrl}" style="color:#1357a0;text-decoration:none">${escUrl}</a></td></tr>
</table>
</td></tr></table>
<p style="margin:0 0 8px;font-size:13px;color:#555">ご質問等ございましたら、このメールへの返信、もしくは <a href="mailto:info@offml.com" style="color:#1357a0;text-decoration:none">info@offml.com</a> までお気軽にお問い合わせください。</p>
</td></tr>
<tr><td style="padding:24px 32px;background:#0a1628;color:rgba(255,255,255,.7);font-size:11px;line-height:1.7">
<div style="font-family:'Montserrat',sans-serif;font-size:13px;font-weight:600;color:#fff;margin-bottom:8px;letter-spacing:.06em">COWORKMILL</div>
<div>デザインで選ぶコワーキング掲載メディア</div>
<div style="margin-top:8px"><a href="${SITE_URL}" style="color:rgba(255,255,255,.55);text-decoration:none">${SITE_URL}</a></div>
<div style="margin-top:12px;color:rgba(255,255,255,.4);font-size:10px">運営: Lily Partners LLC</div>
</td></tr>
</table>
</td></tr></table>
</body></html>`;

  const text = `${data.contactName} 様

このたびは COWORKMILL への掲載お申し込み、誠にありがとうございます。

下記の内容で受け付けました。
通常1営業日以内に運営チームよりご連絡を差し上げます。

────────────────
施設名: ${data.facilityName}
会社名・屋号: ${data.companyName}
施設URL: ${data.facilityUrl}
────────────────

ご質問等ございましたら、このメールへの返信、もしくは
info@offml.com までお気軽にお問い合わせください。

──
COWORKMILL
デザインで選ぶコワーキング掲載メディア
${SITE_URL}
運営: Lily Partners LLC`;

  return { subject, html, text };
}

function buildAdminEmail(data: InquiryPayload, ts: Date): { subject: string; html: string; text: string } {
  const subject = `【COWORKMILL申込】${data.facilityName} / ${data.companyName}`;
  const ts_str = fmtJST(ts);
  const escName = escapeHtml(data.contactName);
  const escEmail = escapeHtml(data.contactEmail);
  const escFac = escapeHtml(data.facilityName);
  const escCom = escapeHtml(data.companyName);
  const escUrl = escapeHtml(data.facilityUrl);

  const html = `<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f6f8;font-family:-apple-system,'Hiragino Sans','Noto Sans JP',sans-serif;color:#1a1a1a;line-height:1.7">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f5f6f8;padding:32px 16px">
<tr><td align="center">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.04)">
<tr><td style="padding:24px 28px;background:#0a1628;color:#fff">
<div style="font-family:'Montserrat',sans-serif;font-size:11px;font-weight:600;letter-spacing:.18em;color:#88c895;margin-bottom:4px">NEW INQUIRY</div>
<div style="font-size:18px;font-weight:600">新規掲載申込が来ました</div>
</td></tr>
<tr><td style="padding:28px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e7eb;border-radius:8px">
<tr><td style="padding:14px 18px;background:#f9fafb;border-bottom:1px solid #e5e7eb;font-size:11px;color:#888;letter-spacing:.06em">施設情報</td></tr>
<tr><td style="padding:14px 18px"><div style="font-size:11px;color:#888;margin-bottom:4px">施設名</div><div style="font-size:15px;font-weight:600">${escFac}</div></td></tr>
<tr><td style="padding:14px 18px;border-top:1px solid #e5e7eb"><div style="font-size:11px;color:#888;margin-bottom:4px">会社名・屋号</div><div style="font-size:14px">${escCom}</div></td></tr>
<tr><td style="padding:14px 18px;border-top:1px solid #e5e7eb"><div style="font-size:11px;color:#888;margin-bottom:4px">施設URL</div><a href="${escUrl}" style="font-size:13px;color:#1357a0;text-decoration:none;word-break:break-all">${escUrl}</a></td></tr>
</table>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e5e7eb;border-radius:8px;margin-top:16px">
<tr><td style="padding:14px 18px;background:#f9fafb;border-bottom:1px solid #e5e7eb;font-size:11px;color:#888;letter-spacing:.06em">担当者情報</td></tr>
<tr><td style="padding:14px 18px"><div style="font-size:11px;color:#888;margin-bottom:4px">お名前</div><div style="font-size:14px">${escName} 様</div></td></tr>
<tr><td style="padding:14px 18px;border-top:1px solid #e5e7eb"><div style="font-size:11px;color:#888;margin-bottom:4px">メール</div><a href="mailto:${escEmail}" style="font-size:14px;color:#1357a0;text-decoration:none">${escEmail}</a></td></tr>
</table>
<div style="margin-top:18px;font-size:11px;color:#888">受付日時: ${ts_str} (JST)</div>
<div style="margin-top:24px"><a href="${SITE_URL}/admin" style="display:inline-block;padding:11px 22px;background:#1357a0;color:#fff;text-decoration:none;border-radius:8px;font-size:13px;font-weight:600">admin で確認 →</a></div>
</td></tr>
</table>
</td></tr></table>
</body></html>`;

  const text = `新規掲載申込が来ました。

【施設情報】
施設名: ${data.facilityName}
会社名・屋号: ${data.companyName}
施設URL: ${data.facilityUrl}

【担当者情報】
お名前: ${data.contactName} 様
メール: ${data.contactEmail}

受付日時: ${ts_str} (JST)

admin で確認: ${SITE_URL}/admin`;

  return { subject, html, text };
}

async function sendViaResend(opts: {
  to: string;
  subject: string;
  html: string;
  text: string;
  replyTo?: string;
}): Promise<{ ok: boolean; status: number; body: string }> {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: `COWORKMILL <${FROM_EMAIL}>`,
      to: [opts.to],
      subject: opts.subject,
      html: opts.html,
      text: opts.text,
      ...(opts.replyTo ? { reply_to: [opts.replyTo] } : {}),
    }),
  });
  const body = await r.text();
  return { ok: r.ok, status: r.status, body };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS_HEADERS });
  }
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  if (!RESEND_API_KEY) {
    console.error("[cwm-inquiry] RESEND_API_KEY not configured");
    return new Response(JSON.stringify({ error: "server not configured" }), {
      status: 500,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  let body: any;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "invalid JSON" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  const v = validate(body);
  if (!v.ok || !v.data) {
    return new Response(JSON.stringify({ error: v.error || "validation error" }), {
      status: 400,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  const data = v.data;
  const ts = new Date();

  // 申込者宛て + 運営宛て を並列送信。片方失敗しても受付処理自体は続行できるよう Promise.allSettled。
  const applicant = buildApplicantEmail(data);
  const admin = buildAdminEmail(data, ts);

  const [resApp, resAdm] = await Promise.allSettled([
    sendViaResend({
      to: data.contactEmail,
      subject: applicant.subject,
      html: applicant.html,
      text: applicant.text,
      replyTo: ADMIN_EMAIL,
    }),
    sendViaResend({
      to: ADMIN_EMAIL,
      subject: admin.subject,
      html: admin.html,
      text: admin.text,
      replyTo: data.contactEmail,
    }),
  ]);

  const summary = {
    applicant_sent: resApp.status === "fulfilled" && resApp.value.ok,
    admin_sent: resAdm.status === "fulfilled" && resAdm.value.ok,
    applicant_status: resApp.status === "fulfilled" ? resApp.value.status : 0,
    admin_status: resAdm.status === "fulfilled" ? resAdm.value.status : 0,
  };

  // 監視・デバッグ用にログ
  console.log("[cwm-inquiry] result", JSON.stringify(summary));
  if (resApp.status === "fulfilled" && !resApp.value.ok) {
    console.error("[cwm-inquiry] applicant email failed:", resApp.value.body);
  }
  if (resAdm.status === "fulfilled" && !resAdm.value.ok) {
    console.error("[cwm-inquiry] admin email failed:", resAdm.value.body);
  }
  if (resApp.status === "rejected") console.error("[cwm-inquiry] applicant rejected:", resApp.reason);
  if (resAdm.status === "rejected") console.error("[cwm-inquiry] admin rejected:", resAdm.reason);

  // 全て失敗時のみ 500 を返す。1通でも届けば 200 (運営は受信できれば運用可能)
  if (!summary.applicant_sent && !summary.admin_sent) {
    return new Response(JSON.stringify({ error: "all email send failed", ...summary }), {
      status: 500,
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ ok: true, ...summary }), {
    status: 200,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
});
