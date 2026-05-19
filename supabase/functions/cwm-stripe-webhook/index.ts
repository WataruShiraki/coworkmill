// Supabase Edge Function: cwm-stripe-webhook
// Stripeからのwebhookを受けて、subscription状態をDBに反映 + Resendでメール通知。
//
// 処理イベント:
//  - checkout.session.completed: 決済完了 → spaces を Pro/Standard に更新
//      → ① オーナーへ「ご利用開始」メール
//      → ④ 運営へ「新規契約」メール
//  - customer.subscription.updated: プラン変更や状態変化を反映
//  - customer.subscription.created: 新規作成を反映
//  - customer.subscription.deleted: 解約 → spaces を Free に戻す
//      → ③ オーナーへ「解約承り」メール
//      → ④ 運営へ「解約」メール
//  - invoice.payment_succeeded: 請求成功 (期限延長)
//  - invoice.payment_failed: 請求失敗 (要対応フラグ)
//      → ② オーナーへ「お支払い失敗」メール
//      → ⑤ 運営へ「決済失敗通知」メール
//
// 必要な環境変数 (Supabase Secrets):
//  - SUPABASE_URL
//  - SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_SECRET_KEYS)
//  - STRIPE_SECRET_KEY
//  - STRIPE_WEBHOOK_SECRET
//  - STRIPE_PRICE_STANDARD
//  - STRIPE_PRICE_PRO
//  - RESEND_API_KEY                    [追加機能で利用 / 既存と共通]
//  - INQUIRY_FROM_EMAIL                [追加機能で利用 / 既存と共通]
//  - INQUIRY_ADMIN_EMAIL               [追加機能で利用 / 既存と共通]
//  - SITE_URL                          [追加機能で利用 / 既存と共通]

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const STRIPE_SECRET_KEY = Deno.env.get("STRIPE_SECRET_KEY") || "";
const STRIPE_WEBHOOK_SECRET = Deno.env.get("STRIPE_WEBHOOK_SECRET") || "";
const STRIPE_PRICE_STANDARD = Deno.env.get("STRIPE_PRICE_STANDARD") || "";
const STRIPE_PRICE_PRO = Deno.env.get("STRIPE_PRICE_PRO") || "";

// ===== メール用環境変数 (cwm-inquiry と共通) =====
const RESEND_API_KEY = Deno.env.get("RESEND_API_KEY") || "";
const FROM_EMAIL = Deno.env.get("INQUIRY_FROM_EMAIL") || "info@cowkml.com";
const ADMIN_EMAIL = Deno.env.get("INQUIRY_ADMIN_EMAIL") || "ws@offml.com";
const SITE_URL = Deno.env.get("SITE_URL") || "https://cowkml.com";

function resolveServiceKey(): string {
  const json = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (json) {
    try {
      const d = JSON.parse(json);
      const v = d?.default ?? Object.values(d || {})[0];
      if (typeof v === "string" && v) return v;
    } catch {}
  }
  return Deno.env.get("SUPABASE_SECRET_DEFAULT_KEY") || Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
}
const SERVICE_KEY = resolveServiceKey();

async function sbFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = {
    "apikey": SERVICE_KEY,
    "Authorization": "Bearer " + SERVICE_KEY,
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };
  return await fetch(SUPABASE_URL + "/rest/v1" + path, { ...init, headers });
}

// Stripe webhook signature verify (HMAC SHA-256)
async function verifyStripeSignature(
  payload: string,
  sigHeader: string,
  secret: string,
  toleranceSec = 300
): Promise<boolean> {
  if (!sigHeader || !secret) return false;
  const parts: Record<string, string> = {};
  for (const kv of sigHeader.split(",")) {
    const [k, v] = kv.split("=");
    if (k && v) parts[k.trim()] = v.trim();
  }
  const t = parts["t"];
  const v1 = parts["v1"];
  if (!t || !v1) return false;

  // tolerance check
  const ts = parseInt(t, 10);
  if (isNaN(ts)) return false;
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - ts) > toleranceSec) return false;

  // verify
  const data = `${t}.${payload}`;
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  const sigHex = Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  // constant-time compare
  if (sigHex.length !== v1.length) return false;
  let diff = 0;
  for (let i = 0; i < sigHex.length; i++) diff |= sigHex.charCodeAt(i) ^ v1.charCodeAt(i);
  return diff === 0;
}

function planFromPriceId(priceId: string): "standard" | "pro" | null {
  if (priceId === STRIPE_PRICE_STANDARD) return "standard";
  if (priceId === STRIPE_PRICE_PRO) return "pro";
  return null;
}

// ===== ここからメール送信ヘルパー =====

function esc(s: any): string {
  if (s === null || s === undefined) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function planLabel(plan: string): string {
  if (plan === "pro") return "Pro";
  if (plan === "standard") return "Standard";
  if (plan === "free") return "Free";
  return plan;
}

function jstDate(unixSec?: number | null): string {
  if (!unixSec) return "";
  const d = new Date(unixSec * 1000);
  const fmt = new Intl.DateTimeFormat("ja-JP", {
    timeZone: "Asia/Tokyo",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
  return fmt.format(d);
}

async function sendEmail(to: string, subject: string, html: string): Promise<boolean> {
  if (!RESEND_API_KEY) {
    console.warn("[webhook][mail] RESEND_API_KEY not set, skipping email to", to);
    return false;
  }
  if (!to) {
    console.warn("[webhook][mail] empty 'to', skipping");
    return false;
  }
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + RESEND_API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: `COWORKMILL <${FROM_EMAIL}>`,
        to: [to],
        subject,
        html,
      }),
    });
    if (!r.ok) {
      const txt = await r.text();
      console.error("[webhook][mail] resend failed", r.status, txt);
      return false;
    }
    console.log("[webhook][mail] sent", to, "subject:", subject);
    return true;
  } catch (e) {
    console.error("[webhook][mail] sendEmail error", e);
    return false;
  }
}

interface SpaceContext {
  space_id: string;
  space_name: string;
  account_id: string;
  account_email: string;
  account_name: string;
  account_company: string;
}

async function getSpaceContext(spaceId: string): Promise<SpaceContext | null> {
  try {
    const spR = await sbFetch(
      `/spaces?id=eq.${encodeURIComponent(spaceId)}&select=id,name,account_id`
    );
    const sps = await spR.json();
    if (!Array.isArray(sps) || sps.length === 0) return null;
    const space = sps[0];
    if (!space.account_id) return null;

    const acR = await sbFetch(
      `/accounts?id=eq.${encodeURIComponent(space.account_id)}&select=email,name,company`
    );
    const acs = await acR.json();
    const ac = Array.isArray(acs) && acs.length > 0 ? acs[0] : {};

    return {
      space_id: space.id,
      space_name: space.name || "（施設名未登録）",
      account_id: space.account_id,
      account_email: ac.email || "",
      account_name: ac.name || ac.company || "ご担当者",
      account_company: ac.company || "",
    };
  } catch (e) {
    console.error("[webhook][mail] getSpaceContext error", e);
    return null;
  }
}

// ===== メールテンプレート =====

function emailLayout(opts: {
  pillLabel: string;
  pillColor: string;
  title: string;
  bodyHtml: string;
  ctaUrl?: string;
  ctaLabel?: string;
}): string {
  const { pillLabel, pillColor, title, bodyHtml, ctaUrl, ctaLabel } = opts;
  const cta = ctaUrl
    ? `<div style="text-align:center;margin-top:24px"><a href="${esc(
        ctaUrl
      )}" style="display:inline-block;background:#0a1628;color:#ffffff;text-decoration:none;padding:12px 32px;border-radius:6px;font-size:13px;font-weight:600;letter-spacing:0.02em">${esc(
        ctaLabel || "確認する"
      )} →</a></div>`
    : "";
  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title>
</head>
<body style="margin:0;padding:0;background:#f5f7fa;font-family:'Helvetica Neue',Arial,'ヒラギノ角ゴ ProN',sans-serif;color:#1a2332;line-height:1.7">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06)">
    <div style="background:#0a1628;padding:28px 28px 32px;color:#ffffff">
      <div style="display:inline-block;padding:4px 10px;background:${esc(
        pillColor
      )};color:#ffffff;font-size:10px;font-weight:600;letter-spacing:0.08em;border-radius:3px;margin-bottom:14px">${esc(
    pillLabel
  )}</div>
      <div style="font-size:20px;font-weight:600;line-height:1.4">${esc(title)}</div>
    </div>
    <div style="padding:24px 28px">
      ${bodyHtml}
      ${cta}
    </div>
    <div style="background:#fafbfc;padding:18px 28px;border-top:1px solid #e8ecef;text-align:center;font-size:11px;color:#9ca3af">
      <div style="font-weight:600;color:#6b7280">COWORKMILL</div>
      <div style="margin-top:4px">運営: Lily Partners, Inc.</div>
      <div style="margin-top:6px"><a href="${esc(
        SITE_URL
      )}" style="color:#9ca3af;text-decoration:none">${esc(SITE_URL)}</a></div>
    </div>
  </div>
</body>
</html>`;
}

function row(label: string, value: string, isStrong = false): string {
  return `<div style="padding:12px 14px;border-bottom:1px solid #f0f2f5">
    <div style="font-size:11px;color:#9ca3af;margin-bottom:4px;letter-spacing:0.04em">${esc(
      label
    )}</div>
    <div style="font-size:14px;${
      isStrong ? "font-weight:600;" : ""
    }color:#1a2332">${esc(value)}</div>
  </div>`;
}

function rowsBox(rowsHtml: string): string {
  return `<div style="border:1px solid #e8ecef;border-radius:6px;overflow:hidden;background:#ffffff">${rowsHtml}</div>`;
}

// ① オーナーへ「ご利用開始」
function tplWelcomeOwner(d: {
  account_name: string;
  space_name: string;
  plan: string;
  period_end?: string;
}): string {
  const pl = planLabel(d.plan);
  return emailLayout({
    pillLabel: "NEW SUBSCRIPTION",
    pillColor: "#22c55e",
    title: "ご利用開始ありがとうございます",
    bodyHtml: `
      <p style="margin:0 0 16px;font-size:14px;color:#1a2332">${esc(d.account_name)} 様</p>
      <p style="margin:0 0 20px;font-size:14px;color:#4b5563">この度は COWORKMILL の有料プランにお申込みいただき、誠にありがとうございます。下記の通りご契約を承りました。</p>
      ${rowsBox(`
        ${row("施設名", d.space_name)}
        ${row("プラン", pl + " プラン", true)}
        ${d.period_end ? row("次回更新日", d.period_end) : ""}
      `)}
      <p style="margin:20px 0 0;font-size:13px;color:#6b7280">プランの変更・解約は管理画面からいつでも可能です。ご不明点がございましたら本メールへご返信ください。</p>
    `,
    ctaUrl: SITE_URL + "/admin",
    ctaLabel: "管理画面を開く",
  });
}

// ② オーナーへ「お支払い失敗」
function tplPaymentFailedOwner(d: {
  account_name: string;
  space_name: string;
  plan: string;
}): string {
  const pl = planLabel(d.plan);
  return emailLayout({
    pillLabel: "PAYMENT FAILED",
    pillColor: "#ef4444",
    title: "お支払いを確認できませんでした",
    bodyHtml: `
      <p style="margin:0 0 16px;font-size:14px;color:#1a2332">${esc(d.account_name)} 様</p>
      <p style="margin:0 0 20px;font-size:14px;color:#4b5563">恐れ入りますが、下記契約のお支払いを確認することができませんでした。お手数ですが管理画面からお支払い情報をご確認のうえ、ご対応をお願いいたします。</p>
      ${rowsBox(`
        ${row("施設名", d.space_name)}
        ${row("プラン", pl + " プラン")}
      `)}
      <p style="margin:20px 0 0;font-size:13px;color:#6b7280">数回お試しのうえ決済が完了しない場合、サービスが一時停止される場合がございます。ご不明な点がございましたら、本メールへご返信ください。</p>
    `,
    ctaUrl: SITE_URL + "/admin",
    ctaLabel: "お支払い情報を確認する",
  });
}

// ③ オーナーへ「ご解約承り」
function tplCancelOwner(d: {
  account_name: string;
  space_name: string;
  plan: string;
}): string {
  const pl = planLabel(d.plan);
  return emailLayout({
    pillLabel: "CANCELED",
    pillColor: "#64748b",
    title: "ご解約を承りました",
    bodyHtml: `
      <p style="margin:0 0 16px;font-size:14px;color:#1a2332">${esc(d.account_name)} 様</p>
      <p style="margin:0 0 20px;font-size:14px;color:#4b5563">${esc(pl)} プランのご解約を承りました。本日より Free プランでのご利用となります。</p>
      ${rowsBox(`
        ${row("施設名", d.space_name)}
        ${row("変更後のプラン", "Free プラン", true)}
      `)}
      <p style="margin:20px 0 0;font-size:13px;color:#6b7280">これまでご利用いただきありがとうございました。またのご利用を心よりお待ちしております。</p>
    `,
    ctaUrl: SITE_URL + "/admin",
    ctaLabel: "管理画面を開く",
  });
}

// ④ 運営へ「プラン変更通知」
function tplPlanChangeAdmin(d: {
  changeType: string;
  account_name: string;
  account_email: string;
  account_company: string;
  space_name: string;
  oldPlan: string;
  newPlan: string;
}): string {
  return emailLayout({
    pillLabel: "PLAN CHANGE",
    pillColor: "#3b82f6",
    title: d.changeType,
    bodyHtml: `
      ${rowsBox(`
        ${row("オーナー名", d.account_name)}
        ${d.account_company ? row("会社名", d.account_company) : ""}
        ${row("メール", d.account_email)}
        ${row("施設名", d.space_name)}
        ${row("変更前", d.oldPlan)}
        ${row("変更後", d.newPlan, true)}
      `)}
    `,
    ctaUrl: SITE_URL + "/admin-ops",
    ctaLabel: "運営管理画面を開く",
  });
}

// ⑤ 運営へ「決済失敗通知」
function tplPaymentFailedAdmin(d: {
  account_name: string;
  account_email: string;
  account_company: string;
  space_name: string;
  plan: string;
}): string {
  const pl = planLabel(d.plan);
  return emailLayout({
    pillLabel: "PAYMENT FAILED",
    pillColor: "#ef4444",
    title: "決済失敗が発生しました",
    bodyHtml: `
      ${rowsBox(`
        ${row("オーナー名", d.account_name)}
        ${d.account_company ? row("会社名", d.account_company) : ""}
        ${row("メール", d.account_email)}
        ${row("施設名", d.space_name)}
        ${row("プラン", pl + " プラン")}
      `)}
      <p style="margin:20px 0 0;font-size:13px;color:#6b7280">オーナー様には自動でお支払い再確認のご案内メールを送信しました。</p>
    `,
    ctaUrl: "https://dashboard.stripe.com/",
    ctaLabel: "Stripe Dashboard を開く",
  });
}

// ===== ここまでメール送信ヘルパー =====

async function updateSpaceFromSubscription(sub: any, opts: { active: boolean }): Promise<void> {
  // metadata から space_id を取得 (subscription metadata 優先, なければ customer metadata)
  const space_id = sub?.metadata?.space_id;
  if (!space_id) {
    console.warn("[webhook] subscription has no space_id metadata", sub.id);
    return;
  }

  const item = sub?.items?.data?.[0];
  const priceId = item?.price?.id || "";
  const plan = planFromPriceId(priceId);

  let updateBody: any;
  if (opts.active && plan) {
    // active: plan を更新
    updateBody = {
      plan,
      stripe_subscription_id: sub.id,
      stripe_price_id: priceId,
      subscription_status: sub.status,
      current_period_end: (item?.current_period_end ?? sub.current_period_end) ? new Date((item?.current_period_end ?? sub.current_period_end) * 1000).toISOString() : null,
      subscription_canceled_at: null,
    };
  } else {
    // canceled or paused: free に戻す
    updateBody = {
      plan: "free",
      stripe_subscription_id: null,
      stripe_price_id: null,
      subscription_status: sub.status,
      current_period_end: (item?.current_period_end ?? sub.current_period_end) ? new Date((item?.current_period_end ?? sub.current_period_end) * 1000).toISOString() : null,
      subscription_canceled_at: new Date().toISOString(),
    };
  }

  const r = await sbFetch(`/spaces?id=eq.${encodeURIComponent(space_id)}`, {
    method: "PATCH",
    headers: { "Prefer": "return=minimal" },
    body: JSON.stringify(updateBody),
  });
  if (!r.ok) {
    const txt = await r.text();
    console.error("[webhook] failed to update space", space_id, r.status, txt);
    return;
  }
  console.log("[webhook] space updated", space_id, "→", updateBody.plan, "(", sub.status, ")");

  // ===== account.plan を再計算 =====
  // metadata から account_id を取得 (なければ space から取得)
  let accountId: string | null = sub?.metadata?.account_id || null;
  if (!accountId) {
    try {
      const spR = await sbFetch(`/spaces?id=eq.${encodeURIComponent(space_id)}&select=account_id`);
      const sps = await spR.json();
      if (Array.isArray(sps) && sps.length > 0) accountId = sps[0].account_id;
    } catch {}
  }
  if (!accountId) {
    console.warn("[webhook] could not resolve account_id for space", space_id);
    return;
  }

  // その account の全 spaces の plan を取得 → 最上位を計算
  try {
    const allR = await sbFetch(`/spaces?account_id=eq.${encodeURIComponent(accountId)}&select=plan`);
    const all = await allR.json();
    if (!Array.isArray(all)) {
      console.warn("[webhook] failed to list spaces for account", accountId);
      return;
    }
    const rank = (p: string): number => p === "pro" ? 3 : p === "standard" ? 2 : 1;
    let topPlan: "free" | "standard" | "pro" = "free";
    for (const s of all) {
      const p = (s.plan || "free") as "free" | "standard" | "pro";
      if (rank(p) > rank(topPlan)) topPlan = p;
    }
    const accR = await sbFetch(`/accounts?id=eq.${encodeURIComponent(accountId)}`, {
      method: "PATCH",
      headers: { "Prefer": "return=minimal" },
      body: JSON.stringify({ plan: topPlan }),
    });
    if (!accR.ok) {
      const txt = await accR.text();
      console.error("[webhook] failed to update account.plan", accountId, accR.status, txt);
    } else {
      console.log("[webhook] account.plan updated", accountId, "→", topPlan);
    }
  } catch (e) {
    console.error("[webhook] error recalculating account.plan", e);
  }
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") return new Response("ok", { status: 405 });

  if (!STRIPE_WEBHOOK_SECRET) return new Response("STRIPE_WEBHOOK_SECRET not set", { status: 500 });
  if (!SERVICE_KEY) return new Response("SERVICE_KEY not set", { status: 500 });

  const sig = req.headers.get("stripe-signature") || "";
  const payload = await req.text();

  // 署名検証
  const valid = await verifyStripeSignature(payload, sig, STRIPE_WEBHOOK_SECRET);
  if (!valid) {
    console.error("[webhook] invalid signature");
    return new Response("invalid signature", { status: 400 });
  }

  let event: any;
  try {
    event = JSON.parse(payload);
  } catch {
    return new Response("invalid JSON", { status: 400 });
  }

  console.log("[webhook] event:", event.type);

  try {
    switch (event.type) {
      case "checkout.session.completed": {
        // session.subscription を取得して反映
        const session = event.data.object;
        if (session.mode === "subscription" && session.subscription) {
          // GET /v1/subscriptions/:id で詳細取得
          const r = await fetch(`https://api.stripe.com/v1/subscriptions/${session.subscription}`, {
            headers: { "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":") },
          });
          if (r.ok) {
            const sub = await r.json();
            // metadata が空なら session.metadata からコピー
            if (!sub.metadata?.space_id && session.metadata?.space_id) {
              sub.metadata = { ...sub.metadata, ...session.metadata };
            }
            await updateSpaceFromSubscription(sub, { active: true });

            // ===== メール送信: ① オーナーへ + ④ 運営へ =====
            const space_id = sub?.metadata?.space_id;
            const item = sub?.items?.data?.[0];
            const priceId = item?.price?.id || "";
            const plan = planFromPriceId(priceId) || "standard";
            const periodEnd = jstDate(sub?.current_period_end);

            if (space_id) {
              const ctx = await getSpaceContext(space_id);
              if (ctx) {
        // ① オーナー宛（accounts 未登録なら Stripe Checkout のメールをfallback）
        const ownerEmail = ctx.account_email || (session.customer_email as string) || (session.customer_details && session.customer_details.email) || "";
        if (ownerEmail && !ctx.account_email && ctx.account_id) {
          try {
            await sbFetch(`/accounts?id=eq.${ctx.account_id}`, {
              method: "PATCH",
              body: JSON.stringify({ email: ownerEmail }),
            });
            console.log("[webhook] account.email backfilled", ctx.account_id);
          } catch (e) {
            console.error("[webhook] account.email backfill failed", e);
          }
        }
        if (ownerEmail) {
          await sendEmail(
            ownerEmail,
            "【COWORKMILL】ご利用開始ありがとうございます",
            tplWelcomeOwner({
              account_name: ctx.account_name,
              space_name: ctx.space_name,
              plan,
              period_end: periodEnd,
            })
          );
        }
                // ④ 運営宛
                await sendEmail(
                  ADMIN_EMAIL,
                  `【COWORKMILL運営】新規プラン契約: ${ctx.space_name}`,
                  tplPlanChangeAdmin({
                    changeType: `新規プラン契約 (${planLabel(plan)})`,
                    account_name: ctx.account_name,
                    account_email: ctx.account_email,
                    account_company: ctx.account_company,
                    space_name: ctx.space_name,
                    oldPlan: "Free",
                    newPlan: planLabel(plan) + " プラン",
                  })
                );
              }
            }
          }
        }
        break;
      }
      case "customer.subscription.updated":
      case "customer.subscription.created": {
        const sub = event.data.object;
        const active = ["active", "trialing"].includes(sub.status);
        await updateSpaceFromSubscription(sub, { active });
        // (updated/created 単独でのメール送信はしない: checkout.session.completed と invoice 系で十分)
        break;
      }
      case "customer.subscription.deleted": {
        const sub = event.data.object;

        // 削除前のプラン情報を取得 (active: false で更新する前)
        const item = sub?.items?.data?.[0];
        const priceId = item?.price?.id || "";
        const oldPlan = planFromPriceId(priceId) || "standard";
        const space_id = sub?.metadata?.space_id;

        await updateSpaceFromSubscription(sub, { active: false });

        // ===== メール送信: ③ オーナーへ + ④ 運営へ =====
        if (space_id) {
          const ctx = await getSpaceContext(space_id);
          if (ctx) {
        // ③ オーナー宛（accounts に email なければ Stripe Customer API から fallback）
        let cxlEmail: string = ctx.account_email || "";
        if (!cxlEmail && sub.customer) {
          try {
            const cr = await fetch(`https://api.stripe.com/v1/customers/${sub.customer as string}`, {
              headers: { "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":") },
            });
            if (cr.ok) {
              const customer = await cr.json();
              cxlEmail = customer.email || "";
            }
          } catch (e) {
            console.error("[webhook] failed to fetch customer for cancel email", e);
          }
        }
        if (cxlEmail) {
          await sendEmail(
            cxlEmail,
            "【COWORKMILL】ご解約を承りました",
            tplCancelOwner({
              account_name: ctx.account_name,
              space_name: ctx.space_name,
              plan: oldPlan,
            })
          );
        }
        if (cxlEmail) {
          await sendEmail(
            cxlEmail,
            "【COWORKMILL】ご解約を承りました",
            tplCancelOwner({
              account_name: ctx.account_name,
              space_name: ctx.space_name,
              plan: oldPlan,
            })
          );
        }
            // ④ 運営宛
            await sendEmail(
              ADMIN_EMAIL,
              `【COWORKMILL運営】プラン解約: ${ctx.space_name}`,
              tplPlanChangeAdmin({
                changeType: `プラン解約 (${planLabel(oldPlan)} → Free)`,
                account_name: ctx.account_name,
                account_email: ctx.account_email,
                account_company: ctx.account_company,
                space_name: ctx.space_name,
                oldPlan: planLabel(oldPlan) + " プラン",
                newPlan: "Free プラン",
              })
            );
          }
        }
        break;
      }
      case "invoice.payment_succeeded": {
        // 必要なら subscription_status だけ更新 (メールは送らない)
        const inv = event.data.object;
        if (inv.subscription) {
          const r = await fetch(`https://api.stripe.com/v1/subscriptions/${inv.subscription}`, {
            headers: { "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":") },
          });
          if (r.ok) {
            const sub = await r.json();
            const active = ["active", "trialing"].includes(sub.status);
            await updateSpaceFromSubscription(sub, { active });
          }
        }
        break;
      }
      case "invoice.payment_failed": {
        const inv = event.data.object;
        if (inv.subscription) {
          const r = await fetch(`https://api.stripe.com/v1/subscriptions/${inv.subscription}`, {
            headers: { "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":") },
          });
          if (r.ok) {
            const sub = await r.json();
            const active = ["active", "trialing"].includes(sub.status);
            await updateSpaceFromSubscription(sub, { active });

            // ===== メール送信: ② オーナーへ + ⑤ 運営へ =====
            const space_id = sub?.metadata?.space_id;
            const item = sub?.items?.data?.[0];
            const priceId = item?.price?.id || "";
            const plan = planFromPriceId(priceId) || "standard";

            if (space_id) {
              const ctx = await getSpaceContext(space_id);
              if (ctx) {
                // ② オーナー宛
                if (ctx.account_email) {
                  await sendEmail(
                    ctx.account_email,
                    "【COWORKMILL】お支払いを確認できませんでした",
                    tplPaymentFailedOwner({
                      account_name: ctx.account_name,
                      space_name: ctx.space_name,
                      plan,
                    })
                  );
                }
                // ⑤ 運営宛
                await sendEmail(
                  ADMIN_EMAIL,
                  `【COWORKMILL運営】決済失敗: ${ctx.space_name}`,
                  tplPaymentFailedAdmin({
                    account_name: ctx.account_name,
                    account_email: ctx.account_email,
                    account_company: ctx.account_company,
                    space_name: ctx.space_name,
                    plan,
                  })
                );
              }
            }
          }
        }
        break;
      }
      default:
        console.log("[webhook] unhandled event:", event.type);
    }
    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  } catch (e) {
    console.error("[webhook] error processing event", event.type, e);
    return new Response("error: " + (e instanceof Error ? e.message : String(e)), { status: 500 });
  }
});

