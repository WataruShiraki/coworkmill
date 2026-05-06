// Supabase Edge Function: cwm-stripe-webhook
// Stripeからのwebhookを受けて、subscription状態をDBに反映する。
//
// 処理イベント:
//  - checkout.session.completed: 決済完了 → spaces を Pro/Standard に更新
//  - customer.subscription.updated: プラン変更や状態変化を反映
//  - customer.subscription.deleted: 解約 → spaces を Free に戻す
//  - invoice.payment_succeeded: 請求成功 (期限延長)
//  - invoice.payment_failed: 請求失敗 (要対応フラグ)

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const STRIPE_SECRET_KEY = Deno.env.get("STRIPE_SECRET_KEY") || "";
const STRIPE_WEBHOOK_SECRET = Deno.env.get("STRIPE_WEBHOOK_SECRET") || "";
const STRIPE_PRICE_STANDARD = Deno.env.get("STRIPE_PRICE_STANDARD") || "";
const STRIPE_PRICE_PRO = Deno.env.get("STRIPE_PRICE_PRO") || "";

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
      current_period_end: sub.current_period_end ? new Date(sub.current_period_end * 1000).toISOString() : null,
      subscription_canceled_at: null,
    };
  } else {
    // canceled or paused: free に戻す
    updateBody = {
      plan: "free",
      stripe_subscription_id: null,
      stripe_price_id: null,
      subscription_status: sub.status,
      current_period_end: sub.current_period_end ? new Date(sub.current_period_end * 1000).toISOString() : null,
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
          }
        }
        break;
      }
      case "customer.subscription.updated":
      case "customer.subscription.created": {
        const sub = event.data.object;
        const active = ["active", "trialing"].includes(sub.status);
        await updateSpaceFromSubscription(sub, { active });
        break;
      }
      case "customer.subscription.deleted": {
        const sub = event.data.object;
        await updateSpaceFromSubscription(sub, { active: false });
        break;
      }
      case "invoice.payment_succeeded":
      case "invoice.payment_failed": {
        // 必要なら subscription_status だけ更新
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
