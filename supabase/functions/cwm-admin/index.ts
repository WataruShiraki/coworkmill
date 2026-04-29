// Supabase Edge Function: cwm-admin
// admin write operations gated by cwm_token JWT
// Currently supports: voice.approve, voice.delete
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { verify } from "https://deno.land/x/djwt@v3.0.2/mod.ts";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const JWT_SECRET = Deno.env.get("CWM_JWT_SECRET")!;

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

async function getKey(s: string) {
  return crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(s),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"]
  );
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" }
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const body = await req.json();
    const { token, action, voice_id } = body;

    if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);

    // JWT verify
    let payload: Record<string, unknown>;
    try {
      const key = await getKey(JWT_SECRET);
      payload = await verify(token, key) as Record<string, unknown>;
    } catch (_e) {
      return jsonResponse({ error: "認証トークンが無効または期限切れです" }, 401);
    }

    const accountId = payload.id as string | undefined;
    if (!accountId) return jsonResponse({ error: "アカウント情報が不正です" }, 401);

    const sb = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

    // === voices.approve / voices.delete ===
    if (action === "voice.approve" || action === "voice.delete") {
      if (!voice_id) return jsonResponse({ error: "voice_idが必要です" }, 400);

      // 1) 対象voiceを取得 (space_idを得る)
      const { data: voiceData, error: voiceErr } = await sb
        .from("voices")
        .select("id,space_id")
        .eq("id", voice_id)
        .single();

      if (voiceErr || !voiceData) {
        return jsonResponse({ error: "対象のレビューが見つかりません" }, 404);
      }

      // 2) その施設のowner確認
      const { data: spaceData, error: spaceErr } = await sb
        .from("spaces")
        .select("id,account_id")
        .eq("id", voiceData.space_id)
        .single();

      if (spaceErr || !spaceData) {
        return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      }

      if (spaceData.account_id !== accountId) {
        return jsonResponse({ error: "このレビューを操作する権限がありません" }, 403);
      }

      // 3) 実行
      if (action === "voice.approve") {
        const { error } = await sb.from("voices")
          .update({ status: "approved" })
          .eq("id", voice_id);
        if (error) return jsonResponse({ error: "承認に失敗: " + error.message }, 500);
      } else {
        const { error } = await sb.from("voices")
          .delete()
          .eq("id", voice_id);
        if (error) return jsonResponse({ error: "削除に失敗: " + error.message }, 500);
      }

      return jsonResponse({ ok: true });
    }

    return jsonResponse({ error: "Unknown action: " + action }, 400);

  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return jsonResponse({ error: "サーバーエラー: " + msg }, 500);
  }
});
