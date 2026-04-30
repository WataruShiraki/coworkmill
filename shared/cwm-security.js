/* COWORKMILL shared security helpers - 2026-04-30
 * - Escape helpers for safe innerHTML usage
 * - Input validation helpers for forms (length / format / blacklist)
 * Updated 2026-05-01: added cwm.validate.* family
 */
(function(global){
  var cwm = global.cwm = global.cwm || {};

  // ========== Escape ==========
  cwm.esc = function(s) {
    if (s === null || s === undefined) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  };
  cwm.escAttr = cwm.esc;
  cwm.safeUrl = function(url) {
    if (!url) return "";
    var s = String(url).trim();
    if (/^(javascript|data|vbscript|file):/i.test(s)) return "";
    return cwm.esc(s);
  };
  cwm.escMultiline = function(s) {
    return cwm.esc(s).replace(/\n/g, "<br>");
  };

  // ========== Validation ==========
  // Each validator returns { ok: boolean, error: string|null, value: cleaned-value }
  // Validators trim by default and never throw — they always return a result object.

  cwm.validate = {
    // Generic string with length bounds
    string: function(s, opts) {
      opts = opts || {};
      var min = opts.min || 0;
      var max = opts.max || 1000;
      var label = opts.label || "値";
      var allowEmpty = opts.allowEmpty !== false && min === 0;
      if (s === null || s === undefined) s = "";
      var v = String(s).trim();
      if (!v) {
        if (allowEmpty) return { ok: true, error: null, value: "" };
        return { ok: false, error: label + "を入力してください", value: "" };
      }
      if (v.length < min) return { ok: false, error: label + "は" + min + "文字以上で入力してください", value: v };
      if (v.length > max) return { ok: false, error: label + "は" + max + "文字以内で入力してください", value: v };
      return { ok: true, error: null, value: v };
    },

    // Email — basic RFC-5322 lite, length capped at 254 (RFC 5321 hard cap)
    email: function(s, opts) {
      opts = opts || {};
      var label = opts.label || "メールアドレス";
      if (s === null || s === undefined) s = "";
      var v = String(s).trim();
      if (!v) {
        if (opts.allowEmpty) return { ok: true, error: null, value: "" };
        return { ok: false, error: label + "を入力してください", value: "" };
      }
      if (v.length > 254) return { ok: false, error: label + "が長すぎます", value: v };
      // Practical pattern: local@domain.tld with no spaces, single @
      if (!/^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/.test(v)) {
        return { ok: false, error: label + "の形式が正しくありません", value: v };
      }
      return { ok: true, error: null, value: v };
    },

    // URL — http/https only, max 2000 chars
    url: function(s, opts) {
      opts = opts || {};
      var label = opts.label || "URL";
      var allowEmpty = opts.allowEmpty !== false;
      if (s === null || s === undefined) s = "";
      var v = String(s).trim();
      if (!v) {
        if (allowEmpty) return { ok: true, error: null, value: "" };
        return { ok: false, error: label + "を入力してください", value: "" };
      }
      if (v.length > 2000) return { ok: false, error: label + "が長すぎます", value: v };
      // Reject scheme-relative & protocol-relative; require http(s)
      if (!/^https?:\/\//i.test(v)) return { ok: false, error: label + "は http:// または https:// で始めてください", value: v };
      // No control characters
      if (/[\x00-\x1f\x7f<>\"]/.test(v)) return { ok: false, error: label + "に使用できない文字が含まれています", value: v };
      try {
        var u = new URL(v);
        if (!/^https?:$/.test(u.protocol)) return { ok: false, error: label + "のスキームが不正です", value: v };
      } catch (e) {
        return { ok: false, error: label + "の形式が正しくありません", value: v };
      }
      return { ok: true, error: null, value: v };
    },

    // Phone — Japanese phones (digits, hyphens, parens, leading +)
    phone: function(s, opts) {
      opts = opts || {};
      var label = opts.label || "電話番号";
      var allowEmpty = opts.allowEmpty !== false;
      if (s === null || s === undefined) s = "";
      var v = String(s).trim();
      if (!v) {
        if (allowEmpty) return { ok: true, error: null, value: "" };
        return { ok: false, error: label + "を入力してください", value: "" };
      }
      if (v.length > 30) return { ok: false, error: label + "が長すぎます", value: v };
      if (!/^[0-9+\-() ]+$/.test(v)) return { ok: false, error: label + "は半角数字とハイフンで入力してください", value: v };
      var digits = v.replace(/[^0-9]/g, "");
      if (digits.length < 7) return { ok: false, error: label + "が短すぎます", value: v };
      return { ok: true, error: null, value: v };
    },

    // Plain text from a textarea — strip ASCII control chars, length bound
    multiline: function(s, opts) {
      opts = opts || {};
      var min = opts.min || 0;
      var max = opts.max || 5000;
      var label = opts.label || "本文";
      var allowEmpty = opts.allowEmpty !== false && min === 0;
      if (s === null || s === undefined) s = "";
      // Normalize newlines, strip control chars except newline+tab
      var v = String(s).replace(/\r\n/g, "\n").replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/g, "");
      var trimmed = v.trim();
      if (!trimmed) {
        if (allowEmpty) return { ok: true, error: null, value: "" };
        return { ok: false, error: label + "を入力してください", value: "" };
      }
      if (trimmed.length < min) return { ok: false, error: label + "は" + min + "文字以上で入力してください", value: trimmed };
      if (trimmed.length > max) return { ok: false, error: label + "は" + max + "文字以内で入力してください", value: trimmed };
      return { ok: true, error: null, value: trimmed };
    },

    // Whitelist enum
    oneOf: function(s, allowed, opts) {
      opts = opts || {};
      var label = opts.label || "値";
      if (allowed.indexOf(s) === -1) return { ok: false, error: label + "が不正です", value: s };
      return { ok: true, error: null, value: s };
    },

    // Reject obvious script-injection attempts in any text input.
    // Used as a defensive last-line check before submitting.
    safeText: function(s, opts) {
      opts = opts || {};
      var label = opts.label || "入力";
      if (s === null || s === undefined) return { ok: true, error: null, value: "" };
      var v = String(s);
      // Forbid raw script tags / event handlers / javascript: scheme.
      // We let the escape layer handle display, but at submit time these are almost always abuse.
      if (/<\s*script\b/i.test(v) ||
          /\bjavascript\s*:/i.test(v) ||
          /\bon[a-z]+\s*=/i.test(v)) {
        return { ok: false, error: label + "に使用できない文字列が含まれています", value: v };
      }
      return { ok: true, error: null, value: v };
    },

    // Run a list of validators and return the first failure, or { ok: true, values: [...] }.
    all: function(checks) {
      var values = [];
      for (var i = 0; i < checks.length; i++) {
        var r = checks[i];
        if (!r.ok) return { ok: false, error: r.error, index: i, value: r.value };
        values.push(r.value);
      }
      return { ok: true, error: null, values: values };
    }
  };
})(window);
