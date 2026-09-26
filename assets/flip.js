(function(){
  // 一覧カードの写真めくり（2026-09-26 わたるさん）
  // PC：カーソルの位置で写真が決まる。左端が1枚目、右端が最後。離れると1枚目に戻る
  // スマホ：カーソルが無いので、カードが画面の真ん中に来たら0.7秒ごとにめくる
  function setup(card){
    var img = card.querySelector('img.ph'); var extra = (card.getAttribute('data-ph') || '').split('|').filter(Boolean);
    if (!img || !extra.length) return;
    var list = [img.getAttribute('src')].concat(extra), ready = [true], cur = 0, loaded = false, timer = null;
    function load(){ if (loaded) return; loaded = true; extra.forEach(function(u, k){ var p = new Image(); p.onload = function(){ ready[k + 1] = true; }; p.src = u; }); }
    function show(n){ if (n !== cur && ready[n]) { cur = n; img.src = list[n]; } }
    function reset(){ cur = 0; img.src = list[0]; }
    card.addEventListener('mouseenter', load);
    card.addEventListener('mousemove', function(e){
      var r = img.getBoundingClientRect(); if (e.clientY > r.bottom) return;
      var n = Math.floor((e.clientX - r.left) / r.width * list.length);
      show(Math.max(0, Math.min(list.length - 1, n)));
    });
    card.addEventListener('mouseleave', function(){ if (cur) reset(); });
    card._auto = {
      start: function(){ load(); if (!timer) timer = setInterval(function(){ var n = cur; do { n = (n + 1) % list.length; } while (!ready[n] && n !== cur); show(n); }, 700); },
      stop: function(){ clearInterval(timer); timer = null; if (cur) reset(); }
    };
  }
  var cards = document.querySelectorAll('.card[data-ph]'); cards.forEach(setup);
  if (!window.matchMedia('(hover:hover)').matches && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){ es.forEach(function(e){ var a = e.target._auto; if (a) (e.isIntersecting ? a.start : a.stop)(); }); }, { rootMargin: '-40% 0px -40% 0px' });
    cards.forEach(function(c){ if (c._auto) io.observe(c); });
  }
})();
