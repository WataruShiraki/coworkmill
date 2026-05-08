// Supabase Edge Function: cwm-login
// Login endpoint that supports both Owner (accounts) and Manager (account_managers).
// Issues HMAC-SHA256 JWT compatible with cwm-admin verification.

import { createClient } from "npm:@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;

function resolveServiceKey(): string {
  const secretKeysJson = Deno.env.get("SUPABASE_SECRET_KEYS");
  if (secretKeysJson) {
    try {
      const dict = JSON.parse(secretKeysJson);
      if (dict && typeof dict === "object") {
        const v = dict.default ?? Object.values(dict)[0];
        if (typeof v === "string" && v.length > 0) return v;
      }
    } catch (_e) {}
  }
  const sbSecretDefault = Deno.env.get("SUPABASE_SECRET_DEFAULT_KEY");
  if (sbSecretDefault) return sbSecretDefault;
  return Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || Deno.env.get("SUPABASE_SERVICE_KEY") || "";
}
const SUPABASE_SERVICE_KEY = resolveServiceKey();
const JWT_SECRET = Deno.env.get("CWM_JWT_SECRET")!;

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

async function getKey(s: string) {
  return crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(s),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"]
  );
}

function b64url(obj: any) {
  const json = typeof obj === "string" ? obj : JSON.stringify(obj);
  return btoa(json).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function issueToken(payload: Record<string, unknown>): Promise<string> {
  const now = Math.floor(Date.now() / 1000);
  const fullPayload = { ...payload, iat: now, exp: now + 30 * 24 * 3600 };
  const header = { alg: "HS256", typ: "JWT" };
  const dataPart = b64url(header) + "." + b64url(fullPayload);
  const key = await getKey(JWT_SECRET);
  const sig = await crypto.subtle.sign(
    { name: "HMAC", hash: "SHA-256" },
    key,
    new TextEncoder().encode(dataPart)
  );
  const sigB64 = btoa(String.fromCharCode(...new Uint8Array(sig)))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  return dataPart + "." + sigB64;
}

// Rate limiter
const rateLimitWindow = new Map<string, number[]>();
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX = 10;

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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });

  try {
    const body = await req.json().catch(() => ({}));
    const action = body.action;

    if (action !== "login") {
      return jsonResponse({ error: "未対応のactionです" }, 400);
    }

    const cleanEmail = ((body.email || "") + "").toLowerCase().trim();
    const cleanPass = (body.password || "") + "";

    if (!cleanEmail || !cleanPass) {
      return jsonResponse({ error: "メールアドレスとパスワードを入力してください" }, 400);
    }

    if (!checkRateLimit("login:" + cleanEmail)) {
      return jsonResponse(
        { error: "短時間に多くのログイン試行が行われました。しばらくお待ちください。" },
        429
      );
    }

    const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    // ----- Step 1: Owner (accounts) でログイン試行 -----
    const { data: ownerRpc, error: ownerErr } = await sb.rpc("verify_owner_login", {
      p_email: cleanEmail,
      p_password: cleanPass,
    });

    if (!ownerErr && ownerRpc && (ownerRpc as any).ok) {
      const r = ownerRpc as any;
      const token = await issueToken({ id: r.account_id, kind: "owner" });
      return jsonResponse({
        ok: true,
        token,
        account: {
          id: r.account_id,
          company: r.company,
          email: r.email,
          plan: r.plan,
          status: r.status,
          kind: "owner",
        },
      });
    }

    // ----- Step 2: Manager (account_managers) でログイン試行 -----
    const { data: mgrRpc, error: mgrErr } = await sb.rpc("verify_manager_login", {
      p_email: cleanEmail,
      p_password: cleanPass,
    });

    if (!mgrErr && mgrRpc && (mgrRpc as any).ok) {
      const m = mgrRpc as any;
      // 親 account 情報取得
      const { data: ownerAcc } = await sb
        .from("accounts")
        .select("id, company, email, plan, status")
        .eq("id", m.account_id)
        .single();

      if (!ownerAcc) {
        return jsonResponse({ error: "親アカウントが見つかりません" }, 401);
      }
      if (ownerAcc.status !== "active") {
        return jsonResponse({ error: "親アカウントが無効化されています" }, 403);
      }

      const token = await issueToken({
        id: m.account_id,
        kind: "manager",
        manager_id: m.manager_id,
        role: m.role,
      });

      return jsonResponse({
        ok: true,
        token,
        account: {
          id: ownerAcc.id,
          company: ownerAcc.company,
          email: ownerAcc.email,
          plan: ownerAcc.plan,
          status: ownerAcc.status,
          kind: "manager",
          manager_id: m.manager_id,
          manager_email: cleanEmail,
          manager_role: m.role,
        },
      });
    }

    return jsonResponse({ error: "メールアドレスまたはパスワードが正しくありません" }, 401);
  } catch (e) {
    return jsonResponse({ error: "サーバーエラー: " + (e?.message || String(e)) }, 500);
  }
});
