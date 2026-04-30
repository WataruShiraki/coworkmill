// Supabase Edge Function: cwm-admin
// Verified-write proxy. Receives a cwm_token, verifies HMAC-SHA256 with
// CWM_JWT_SECRET, runs ownership checks, then writes via service_role.
// Anon key NEVER has UPDATE/DELETE/INSERT permission on protected tables.

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
  return crypto.subtle.importKey("raw", new TextEncoder().encode(s),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const body = await req.json();
    const { token, target, action, id, data } = body;

    if (!token) return jsonResponse({ error: "認証トークンが必要です" }, 401);
    if (!target) return jsonResponse({ error: "操作対象が指定されていません" }, 400);
    if (!action) return jsonResponse({ error: "操作内容が指定されていません" }, 400);

    let payload: any;
    try {
      const key = await getKey(JWT_SECRET);
      payload = await verify(token, key);
    } catch (_e) {
      return jsonResponse({ error: "認証トークンが無効または期限切れです（再ログインしてください）" }, 401);
    }

    const accountId = payload.id;
    if (!accountId) return jsonResponse({ error: "トークンにアカウントIDが含まれていません" }, 401);

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
      if (vSp.account_id !== accountId) return jsonResponse({ error: "権限がありません" }, 403);

      if (action === "approve") {
        const { data: u, error } = await sb.from("voices").update({ status: "approved" }).eq("id", id).select();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, voice: u?.[0] });
      } else if (action === "reject") {
        const { data: u, error } = await sb.from("voices").update({ status: "rejected" }).eq("id", id).select();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, voice: u?.[0] });
      } else if (action === "delete") {
        const { error } = await sb.from("voices").delete().eq("id", id);
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============ space (施設) ============
    if (target === "space") {
      if (action === "insert") {
        // 新規施設登録 - 必ず requestor の account_id にバインド
        const insertData = { ...(data || {}), account_id: accountId };
        delete insertData.id;
      // アカウントのplanを新規施設に継承(Pro/Standardアカウントの新規施設も自動的にPro/Standardになる)
      const { data: _acctPlan } = await sb.from("accounts").select("plan").eq("id", accountId).single();
      if (_acctPlan && _acctPlan.plan) insertData.plan = _acctPlan.plan; // クライアント側からの id 注入を防止
        const { data: created, error } = await sb.from("spaces").insert(insertData).select().single();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, space: created });
      }

      if (!id) return jsonResponse({ error: "space IDが必要です" }, 400);
      const { data: space } = await sb.from("spaces").select("id,account_id").eq("id", id).single();
      if (!space) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      if (space.account_id !== accountId) return jsonResponse({ error: "権限がありません" }, 403);

      if (action === "update") {
        // account_id の改ざんを防止
        const updateData = { ...(data || {}) };
        delete updateData.account_id;
        delete updateData.id;
        const { data: u, error } = await sb.from("spaces").update(updateData).eq("id", id).select().single();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, space: u });
      } else if (action === "delete") {
        await sb.from("voices").delete().eq("space_id", id);
        await sb.from("space_images").delete().eq("space_id", id);
        const { error } = await sb.from("spaces").delete().eq("id", id);
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    // ============ space_image (施設写真) ============
    if (target === "space_image") {
      if (action === "insert") {
        // INSERT時: data.space_id の owner check
        const spaceId = data?.space_id;
        if (!spaceId) return jsonResponse({ error: "space_id が必要です" }, 400);
        const { data: spChk } = await sb.from("spaces").select("id,account_id").eq("id", spaceId).single();
        if (!spChk) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
        if (spChk.account_id !== accountId) return jsonResponse({ error: "権限がありません" }, 403);
        const insertData = { ...(data || {}) };
        delete insertData.id;
        const { data: created, error } = await sb.from("space_images").insert(insertData).select().single();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, image: created });
      }

      if (!id) return jsonResponse({ error: "space_image IDが必要です" }, 400);
      const { data: img } = await sb.from("space_images").select("id,space_id").eq("id", id).single();
      if (!img) return jsonResponse({ error: "対象画像が見つかりません" }, 404);
      const { data: iSp } = await sb.from("spaces").select("id,account_id").eq("id", img.space_id).single();
      if (!iSp) return jsonResponse({ error: "対象施設が見つかりません" }, 404);
      if (iSp.account_id !== accountId) return jsonResponse({ error: "権限がありません" }, 403);

      if (action === "update") {
        const updateData = { ...(data || {}) };
        delete updateData.id; delete updateData.space_id;
        const { data: u, error } = await sb.from("space_images").update(updateData).eq("id", id).select().single();
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true, image: u });
      } else if (action === "delete") {
        const { error } = await sb.from("space_images").delete().eq("id", id);
        if (error) return jsonResponse({ error: error.message }, 500);
        return jsonResponse({ ok: true });
      }
      return jsonResponse({ error: "不明なアクション: " + action }, 400);
    }

    return jsonResponse({ error: "不明な操作対象: " + target }, 400);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return jsonResponse({ error: msg }, 500);
  }
});
