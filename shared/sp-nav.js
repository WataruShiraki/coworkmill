/* COWORKMILL Common SP Navigation Script */
(function(){
  'use strict';
  
  /**
   * Safely create the mobile nav overlay using DOM API (no innerHTML).
   * Prevents XSS vectors in case any content is ever derived from URL params.
   */
  function buildOverlay() {
    var ov = document.createElement('div');
    ov.className = 'cwm-mob-nav-overlay';
    ov.id = 'cwm-mob-nav';
    ov.setAttribute('role', 'dialog');
    ov.setAttribute('aria-label', 'モバイルナビゲーション');
    ov.setAttribute('aria-modal', 'true');
    ov.addEventListener('click', function(e){
      if (e.target === ov) window.cwmCloseMobileNav();
    });
    
    var brand = document.createElement('div');
    brand.className = 'cwm-mob-nav-brand';
    brand.textContent = 'COWORKMILL';
    ov.appendChild(brand);
    
    var closeBtn = document.createElement('button');
    closeBtn.className = 'cwm-mob-nav-close';
    closeBtn.setAttribute('aria-label', '閉じる');
    closeBtn.textContent = '\u00D7';
    closeBtn.addEventListener('click', function(){ window.cwmCloseMobileNav(); });
    ov.appendChild(closeBtn);
    
    var inner = document.createElement('div');
    inner.className = 'cwm-mob-nav-inner';
    
    var links = [
      { href: 'coworkmill.html', text: 'トップ' },
      { href: 'coworkmill-spaces.html', text: 'コワーキングを探す' },
      { href: 'coworkmill-architects.html', text: '建築家から探す' },
      { href: 'coworkmill-photos.html', text: '写真から探す' },
      { href: 'coworkmill-register.html', text: 'コワーキング登録', cta: true }
    ];
    
    links.forEach(function(l){
      var a = document.createElement('a');
      a.href = l.href;
      a.textContent = l.text;
      if (l.cta) a.className = 'cta';
      inner.appendChild(a);
    });
    
    ov.appendChild(inner);
    return ov;
  }
  
  function init() {
    var nav = document.querySelector('nav');
    if (!nav || document.querySelector('.cwm-hamburger')) return;
    
    var bt = document.createElement('button');
    bt.className = 'cwm-hamburger';
    bt.type = 'button';
    bt.setAttribute('aria-label', 'メニュー');
    bt.setAttribute('aria-expanded', 'false');
    bt.setAttribute('aria-controls', 'cwm-mob-nav');
    
    for (var i = 0; i < 3; i++) {
      bt.appendChild(document.createElement('span'));
    }
    
    bt.addEventListener('click', function(){ window.cwmToggleMobileNav(); });
    
    var navRight = nav.querySelector('.nav-right');
    if (navRight) navRight.appendChild(bt);
    else nav.appendChild(bt);
    
    if (!document.getElementById('cwm-mob-nav')) {
      document.body.appendChild(buildOverlay());
    }
  }
  
  window.cwmToggleMobileNav = function() {
    var ov = document.getElementById('cwm-mob-nav');
    var bt = document.querySelector('.cwm-hamburger');
    if (!ov || !bt) return;
    var willOpen = !ov.classList.contains('open');
    ov.classList.toggle('open', willOpen);
    bt.classList.toggle('open', willOpen);
    bt.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    document.body.style.overflow = willOpen ? 'hidden' : '';
  };
  
  window.cwmCloseMobileNav = function() {
    var ov = document.getElementById('cwm-mob-nav');
    var bt = document.querySelector('.cwm-hamburger');
    if (ov) ov.classList.remove('open');
    if (bt) {
      bt.classList.remove('open');
      bt.setAttribute('aria-expanded', 'false');
    }
    document.body.style.overflow = '';
  };
  
  // ESC キーで閉じる(アクセシビリティ向上)
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' || e.keyCode === 27) {
      var ov = document.getElementById('cwm-mob-nav');
      if (ov && ov.classList.contains('open')) {
        window.cwmCloseMobileNav();
      }
    }
  });
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();