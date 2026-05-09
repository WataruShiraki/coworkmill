// Supabase Edge Function: cwm-invite
// 招待トークンの検証と、 パスワード設定による招待受諾を処理する公開エンドポイント。
// 認証は invite_token のみ (cwm_token は使わない)。

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

// 軽量レート制限 (1分間 30回/IP)
const rateLimit = new Map<string, number[]>();
function checkRateLimit(key: string, max = 30, windowMs = 60_000): boolean {
  const now = Date.now();
  const arr = (rateLimit.get(key) || []).filter((t) => now - t < windowMs);
  if (arr.length >= max) {
    rateLimit.set(key, arr);
    return false;
  }
  arr.push(now);
  rateLimit.set(key, arr);
  return true;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: cors });
  if (req.method !== "POST") return jsonResponse({ error: "method not allowed" }, 405);

  try {
    const body = await req.json().catch(() => ({}));
    const action = body.action;
    const token = ((body.token || "") + "").trim();

    const ip = req.headers.get("x-forwarded-for") || "unknown";
    if (!checkRateLimit("invite:" + ip)) {
      return jsonResponse({ error: "短時間に多くのリクエストが行われました。しばらくお待ちください。" }, 429);
    }

    if (!token) return jsonResponse({ error: "招待リンクが無効です" }, 400);

    const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    // ------- verify (token検証 + 招待情報のプレビュー) -------
    if (action === "verify") {
      const { data: rpcRes, error: rpcErr } = await sb.rpc("verify_invite_token", { p_token: token });
      if (rpcErr) {
        return jsonResponse({ error: "招待の検証に失敗しました" }, 500);
      }
      const r = rpcRes as { ok?: boolean; error?: string; email?: string; display_name?: string; role?: string; company?: string };
      if (!r?.ok) {
        const map: Record<string, string> = {
          "invalid token": "招待リンクが無効です。 リンクが正しいか確認してください。",
          "already accepted": "この招待は既に受諾されています。 通常のログイン画面からログインしてください。",
          "token expired": "招待リンクの有効期限が切れています。 招待元に再送を依頼してください。"
        };
        return jsonResponse({ error: map[r?.error || ""] || r?.error || "招待の検証に失敗しました" }, 400);
      }
      return jsonResponse({
        ok: true,
        email: r.email,
        display_name: r.display_name || null,
        role: r.role,
        company: r.company
      });
    }

    // ------- accept (パスワード設定 + 招待受諾) -------
    if (action === "accept") {
      const password = ((body.password || "") + "");
      if (!password) return jsonResponse({ error: "パスワードを入力してください" }, 400);
      if (password.length < 8 || password.length > 200) {
        return jsonResponse({ error: "パスワードは8〜200文字で入力してください" }, 400);
      }

      const { data: rpcRes, error: rpcErr } = await sb.rpc("accept_manager_invite", {
        p_token: token,
        p_password: password
      });
      if (rpcErr) {
        return jsonResponse({ error: "パスワード設定に失敗しました" }, 500);
      }
      const r = rpcRes as { ok?: boolean; error?: string };
      if (!r?.ok) {
        const map: Record<string, string> = {
          "invalid token": "招待リンクが無効です",
          "already accepted": "この招待は既に受諾されています。 ログイン画面をご利用ください。",
          "token expired": "招待リンクの有効期限が切れています。 招待元に再送を依頼してください。",
          "password must be 8-200 chars": "パスワードは8〜200文字で入力してください"
        };
        return jsonResponse({ error: map[r?.error || ""] || r?.error || "パスワード設定に失敗しました" }, 400);
      }
      return jsonResponse({ ok: true });
    }

    return jsonResponse({ error: "未対応のactionです" }, 400);
  } catch (e) {
    return jsonResponse({ error: "サーバーエラー: " + (e?.message || String(e)) }, 500);
  }
});
