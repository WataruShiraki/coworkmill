/* ==========================================================================
 * cwm-ops-auth.js
 * 運営管理画面 (admin-ops) 用の認証ヘルパー
 * - sessionStorage に保存された ops_token をチェック
 * - cwm-admin Edge Function への target=ops 呼び出しラッパー
 * - 401 を受けたらログインページへ自動リダイレクト
 * ========================================================================== */
(function () {
  'use strict';

  var SB_URL = 'https://jakwntemjkwqwaqujffh.supabase.co';
  var SB_KEY = 'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ';
  var FN_URL = SB_URL + '/functions/v1/cwm-admin';
  var LOGIN_PAGE = 'ops-login.html';

  function getToken() { return sessionStorage.getItem('cwm_ops_token'); }
  function getEmail() { return sessionStorage.getItem('cwm_ops_email'); }
  function getRole()  { return sessionStorage.getItem('cwm_ops_role'); }

  function clearAuth() {
    sessionStorage.removeItem('cwm_ops_token');
    sessionStorage.removeItem('cwm_ops_email');
    sessionStorage.removeItem('cwm_ops_role');
  }

  function redirectToLogin() {
    clearAuth();
    if (location.pathname.indexOf(LOGIN_PAGE) === -1) {
      location.href = LOGIN_PAGE;
    }
  }

  /**
   * ops_token が存在しなければログインページにリダイレクトする
   * admin-ops のページ読み込み直後に呼ぶ
   */
  function requireAuth() {
    if (!getToken()) {
      redirectToLogin();
      return false;
    }
    return true;
  }

  /**
   * Edge Function を target=ops で呼ぶ
   * @param {string} action - "list" | "invite" | "delete"
   * @param {object} [data] - action ごとのペイロード
   * @returns {Promise<object>} - レスポンスJSON
   */
  async function call(action, data) {
    var token = getToken();
    if (!token) {
      redirectToLogin();
      throw new Error('認証トークンがありません');
    }

    var body = { token: token, target: 'ops', action: action };
    if (data !== undefined) body.data = data;

    var res;
    try {
      res = await fetch(FN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SB_KEY,
          'Authorization': 'Bearer ' + SB_KEY
        },
        body: JSON.stringify(body)
      });
    } catch (e) {
      throw new Error('ネットワークエラー: ' + (e && e.message ? e.message : String(e)));
    }

    var json;
    try { json = await res.json(); } catch (_e) { json = {}; }

    if (res.status === 401) {
      // トークン失効 → ログインへ
      redirectToLogin();
      throw new Error(json.error || '認証が切れました。再ログインしてください。');
    }
    if (!res.ok) {
      throw new Error(json.error || ('リクエスト失敗 (HTTP ' + res.status + ')'));
    }
    return json;
  }

  /**
   * target=ops_db 汎用DBプロキシ呼び出し (内部用)
   * @returns {Promise<Response>} - 生のResponseオブジェクト
   */
  async function _opsDb(action, payload) {
    var token = getToken();
    if (!token) {
      redirectToLogin();
      throw new Error('認証トークンがありません');
    }
    var res;
    try {
      res = await fetch(FN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SB_KEY,
          'Authorization': 'Bearer ' + SB_KEY
        },
        body: JSON.stringify({ token: token, target: 'ops_db', action: action, data: payload })
      });
    } catch (e) {
      throw new Error('ネットワークエラー: ' + (e && e.message ? e.message : String(e)));
    }
    if (res.status === 401) {
      redirectToLogin();
      throw new Error('認証が切れました。再ログインしてください。');
    }
    return res;
  }

  /** SELECT (REST GET相当) — path はテーブル+クエリ文字列 (例: 'accounts?select=*') */
  async function dbGet(path) {
    var r = await _opsDb('select', { path: path });
    try { return await r.json(); } catch (_e) { return null; }
  }
  /** INSERT */
  async function dbPost(table, body) {
    var r = await _opsDb('insert', { table: table, body: body });
    try { return await r.json(); } catch (_e) { return null; }
  }
  /** UPDATE */
  async function dbPatch(table, filter, body) {
    var r = await _opsDb('update', { table: table, filter: filter, body: body });
    try { return await r.json(); } catch (_e) { return null; }
  }
  /** DELETE — { ok: boolean } を返す (既存コードが res.ok を見ているため) */
  async function dbDelete(table, filter) {
    var r = await _opsDb('delete', { table: table, filter: filter });
    try { var j = await r.json(); return { ok: !!j.ok }; } catch (_e) { return { ok: r.ok }; }
  }
  /** RPC */
  async function dbRpc(name, body) {
    var r = await _opsDb('rpc', { rpc: name, body: body });
    return r; // 呼び出し側で .ok / .json() を見るため Response のまま返す
  }
  /** Supabase Auth /admin/invite のプロキシ */
  async function authInvite(email) {
    var r = await _opsDb('auth_invite', { email: email });
    return r;
  }

  /**
   * accounts_admin (target) 呼び出し
   * 掲載者アカウントを accounts テーブル + auth.users 両方で同期管理する
   * @param {'create'|'update'|'delete'} action
   * @param {object} payload - action ごとのデータ
   * @returns {Promise<object>} - 成功時 { ok: true, ...} / 失敗時 throw
   */
  async function accountsAdmin(action, payload) {
    var token = getToken();
    if (!token) {
      redirectToLogin();
      throw new Error('認証トークンがありません');
    }
    var res;
    try {
      res = await fetch(FN_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': SB_KEY,
          'Authorization': 'Bearer ' + SB_KEY
        },
        body: JSON.stringify({ token: token, target: 'accounts_admin', action: action, data: payload || {} })
      });
    } catch (e) {
      throw new Error('ネットワークエラー: ' + (e && e.message ? e.message : String(e)));
    }
    var json;
    try { json = await res.json(); } catch (_e) { json = {}; }
    if (res.status === 401) {
      redirectToLogin();
      throw new Error(json.error || '認証が切れました。再ログインしてください。');
    }
    if (!res.ok) {
      throw new Error(json.error || ('リクエスト失敗 (HTTP ' + res.status + ')'));
    }
    return json;
  }

  /**
   * ログアウト: ops_token + Supabase auth 両方をクリアしてログインへ
   */
  async function signOut() {
    clearAuth();
    // Supabase Auth セッションも削除（Google再ログインのため）
    try {
      if (window.supabase && window.supabase.createClient) {
        var sb = window.supabase.createClient(SB_URL, SB_KEY);
        await sb.auth.signOut();
      }
    } catch (_e) {}
    location.href = LOGIN_PAGE;
  }

  // グローバル公開
  window.cwmOpsAuth = {
    requireAuth: requireAuth,
    call: call,
    signOut: signOut,
    getEmail: getEmail,
    getRole: getRole,
    isOwner: function () { return getRole() === 'owner'; },
    dbGet: dbGet,
    dbPost: dbPost,
    dbPatch: dbPatch,
    dbDelete: dbDelete,
    dbRpc: dbRpc,
    authInvite: authInvite,
    accountsAdmin: accountsAdmin
  };
})();
