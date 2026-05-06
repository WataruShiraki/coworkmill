// Supabase Edge Function: cwm-portal
// 施設運営者用の Stripe Customer Portal セッションを発行する。
// admin.html から呼ばれ、返ってきた URL に遷移すると、
// 顧客が請求書履歴・カード変更・解約・住所更新等を自分で管理できる。

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const STRIPE_SECRET_KEY = Deno.env.get("STRIPE_SECRET_KEY") || "";
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

  const { token } = body;
  if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);

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
    // stripe_customers から該当アカウントの customer ID を取得
    const cuR = await sbFetch(`/stripe_customers?account_id=eq.${encodeURIComponent(accountId)}&select=stripe_customer_id`);
    const cus = await cuR.json();
    if (!Array.isArray(cus) || cus.length === 0 || !cus[0].stripe_customer_id) {
      return jsonResponse({
        error: "まだ有料プランをご利用されていないため、請求情報がありません。",
        no_customer: true
      }, 404);
    }
    const stripeCustomerId = cus[0].stripe_customer_id;

    // Customer Portal Session 作成
    const r = await fetch("https://api.stripe.com/v1/billing_portal/sessions", {
      method: "POST",
      headers: {
        "Authorization": "Basic " + btoa(STRIPE_SECRET_KEY + ":"),
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        customer: stripeCustomerId,
        return_url: SITE_URL + "/admin",
      }).toString(),
    });
    const j = await r.json();
    if (!r.ok) {
      console.error("[cwm-portal] portal session failed", j);
      return jsonResponse({ error: "ポータル準備に失敗しました: " + (j?.error?.message || "unknown") }, 500);
    }
    return jsonResponse({ ok: true, url: j.url });
  } catch (e) {
    console.error("[cwm-portal]", e);
    return jsonResponse({ error: "処理に失敗しました: " + (e instanceof Error ? e.message : String(e)) }, 500);
  }
});
