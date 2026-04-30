/* COWORKMILL shared security helpers - 2026-04-30 - escape helpers for safe innerHTML usage */
(function(global){
  var cwm = global.cwm = global.cwm || {};
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
})(window);
