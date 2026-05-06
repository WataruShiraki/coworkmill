// Supabase Edge Function: cwm-checkout
// 施設運営者がアップグレード時にStripe Checkout Sessionを発行する。
//
// フロー:
//  1. admin.html から POST { token, space_id, plan: "standard"|"pro" } で呼ばれる
//  2. JWT を verify → account_id 取得
//  3. spaces テーブルから space を取得 → account_id と一致確認
//  4. stripe_customers テーブルから既存 Customer を探す or 新規作成
//  5. Stripe Checkout Session を作成 (subscription mode)
//  6. URL を返す → フロントが redirect

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const STRIPE_SECRET_KEY = Deno.env.get("STRIPE_SECRET_KEY") || "";
const STRIPE_PRICE_STANDARD = Deno.env.get("STRIPE_PRICE_STANDARD") || "";
const STRIPE_PRICE_PRO = Deno.env.get("STRIPE_PRICE_PRO") || "";
const SITE_URL = Deno.env.get("SITE_URL") || "https://cowkml.com";
const JWT_SECRET = Deno.env.get("CWM_JWT_SECRET") || "";

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

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, apikey, x-client-info",
};

function jsonResponse(body: any, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

// JWT verify (HMAC SHA-256)
function _b64urlDecode(s: string): Uint8Array {
  const pad = s.length % 4;
  const b64 = (s + (pad ? "=".repeat(4 - pad) : "")).replace(/-/g, "+").replace(/_/g, "/");
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
async function getKey(secret: string): Promise<CryptoKey> {
  return await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"]
  );
}
async function verifyJwt(jwt: string, key: CryptoKey): Promise<any> {
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

// Stripe API helper (form-urlencoded)
async function stripePost(path: string, params: Record<string, string>): Promise<any> {
  const body = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) body.append(k, v);
  const r = await fetch(`https://api.stripe.com/v1${path}`, {
    method: "POST",
    headers: {
      "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: body.toString(),
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`Stripe ${path}: ${j?.error?.message || r.status}`);
  return j;
}

// Supabase REST helper (service_role)
async function sbFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = {
    "apikey": SERVICE_KEY,
    "Authorization": "Bearer " + SERVICE_KEY,
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };
  return await fetch(SUPABASE_URL + "/rest/v1" + path, { ...init, headers });
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS_HEADERS });
  if (req.method !== "POST") return jsonResponse({ error: "Method not allowed" }, 405);

  if (!STRIPE_SECRET_KEY) return jsonResponse({ error: "STRIPE_SECRET_KEY not set" }, 500);
  if (!JWT_SECRET) return jsonResponse({ error: "CWM_JWT_SECRET not set" }, 500);
  if (!SERVICE_KEY) return jsonResponse({ error: "SERVICE_KEY not set" }, 500);

  let body: any;
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "invalid JSON" }, 400);
  }

  const { token, space_id, plan } = body;
  if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
  if (!space_id || typeof space_id !== "string") return jsonResponse({ error: "space_id が必要です" }, 400);
  if (plan !== "standard" && plan !== "pro") return jsonResponse({ error: "plan は 'standard' か 'pro' のみ" }, 400);

  // JWT verify
  let payload: any;
  try {
    const key = await getKey(JWT_SECRET);
    payload = await verifyJwt(token, key);
  } catch {
    return jsonResponse({ error: "認証トークンが無効または期限切れです" }, 401);
  }
  const accountId = payload.id;
  if (!accountId) return jsonResponse({ error: "トークンにアカウントIDが含まれていません" }, 401);

  try {
    // 1. account 取得 (email用)
    const acR = await sbFetch(`/accounts?id=eq.${encodeURIComponent(accountId)}&select=id,email,name,status`);
    const acs = await acR.json();
    if (!Array.isArray(acs) || acs.length === 0) return jsonResponse({ error: "アカウントが見つかりません" }, 404);
    const ac = acs[0];
    if (ac.status !== "active") return jsonResponse({ error: "アカウントが無効化されています" }, 403);

    // 2. space 取得 + 所有確認
    const spR = await sbFetch(`/spaces?id=eq.${encodeURIComponent(space_id)}&select=id,name,account_id,plan,status,stripe_subscription_id`);
    const sps = await spR.json();
    if (!Array.isArray(sps) || sps.length === 0) return jsonResponse({ error: "施設が見つかりません" }, 404);
    const sp = sps[0];
    if (sp.account_id !== accountId) return jsonResponse({ error: "この施設の所有者ではありません" }, 403);
    if (sp.stripe_subscription_id) return jsonResponse({ error: "既にサブスクリプションが設定されています" }, 400);

    // 3. Stripe Customer を検索 or 作成
    let stripeCustomerId: string;
    const cuR = await sbFetch(`/stripe_customers?account_id=eq.${encodeURIComponent(accountId)}&select=stripe_customer_id`);
    const cus = await cuR.json();
    if (Array.isArray(cus) && cus.length > 0 && cus[0].stripe_customer_id) {
      stripeCustomerId = cus[0].stripe_customer_id;
    } else {
      const customer = await stripePost("/customers", {
        email: ac.email || "",
        name: ac.name || "",
        "metadata[account_id]": accountId,
      });
      stripeCustomerId = customer.id;
      await sbFetch("/stripe_customers", {
        method: "POST",
        headers: { "Prefer": "return=minimal" },
        body: JSON.stringify({
          account_id: accountId,
          stripe_customer_id: stripeCustomerId,
          email: ac.email || null,
        }),
      });
    }

    // 4. Checkout Session 作成
    const priceId = plan === "standard" ? STRIPE_PRICE_STANDARD : STRIPE_PRICE_PRO;
    if (!priceId) return jsonResponse({ error: `STRIPE_PRICE_${plan.toUpperCase()} not set` }, 500);

    const session = await stripePost("/checkout/sessions", {
      mode: "subscription",
      customer: stripeCustomerId,
      "line_items[0][price]": priceId,
      "line_items[0][quantity]": "1",
      success_url: `${SITE_URL}/admin?checkout=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${SITE_URL}/admin?checkout=cancel`,
      "metadata[account_id]": accountId,
      "metadata[space_id]": space_id,
      "metadata[plan]": plan,
      "subscription_data[metadata][account_id]": accountId,
      "subscription_data[metadata][space_id]": space_id,
      "subscription_data[metadata][plan]": plan,
      // 日本のクレカ決済に必要な3DSecure設定
      payment_method_types: "card",
      locale: "ja",
    });

    return jsonResponse({ ok: true, url: session.url, session_id: session.id });
  } catch (e) {
    console.error("[cwm-checkout]", e);
    return jsonResponse({ error: "処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
  }
});
