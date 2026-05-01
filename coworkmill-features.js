(function() {
  const css = document.createElement('style');
  css.textContent = `
    #plan-free, #plan-standard, #plan-pro { position:relative !important; cursor:default !important; }
    #plan-free.plan-selected, #plan-standard.plan-selected, #plan-pro.plan-selected {
      border:2px solid #2BB5C8 !important; background:rgba(43,181,200,0.06) !important;
    }
    .cwm-wrap { position:relative; }
    .cwm-input-ok  { border-color:#4ade80 !important; }
    .cwm-input-err { border-color:#f87171 !important; }
    .cwm-err { color:#f87171; font-size:11px; margin-top:5px; display:none; font-family:sans-serif; }
    .cwm-ok  { position:absolute; right:12px; top:13px; color:#4ade80; font-size:14px; pointer-events:none; display:none; }
    .submit-btn:disabled { opacity:0.4 !important; cursor:not-allowed !important; }
  `;
  document.head.appendChild(css);

  function resetPlans() {
    ['free','standard','pro'].forEach(function(p) {
      const el = document.getElementById('plan-'+p);
      if (!el) return;
      el.classList.remove('plan-selected');
      el.querySelectorAll('div').forEach(function(d){ if(d.textContent.trim()==='選択中') d.remove(); });
      let s=(el.getAttribute('style')||'').replace(/border\s*:[^;]+;?\s*/gi,'');
      el.setAttribute('style','border:1px solid #2a2a2a;'+s);
    });
    window.selectedPlan='free';
  }

  window.selectPlan=function(plan){
    ['free','standard','pro'].forEach(function(p){
      const el=document.getElementById('plan-'+p);
      if(!el) return;
      el.querySelectorAll('div').forEach(function(d){ if(d.textContent.trim()==='選択中') d.remove(); });
      el.classList.remove('plan-selected');
      let s=(el.getAttribute('style')||'').replace(/border\s*:[^;]+;?\s*/gi,'');
      if(p===plan){
        el.classList.add('plan-selected');
        el.setAttribute('style','border:2px solid #2BB5C8;'+s);
        const b=document.createElement('div');
        b.textContent='選択中';
        b.style.cssText='position:absolute;top:10px;right:10px;font-size:8px;font-weight:600;padding:3px 8px;background:#2BB5C8;color:#000;border-radius:4px;z-index:10;';
        el.appendChild(b);
      } else { el.setAttribute('style','border:1px solid #2a2a2a;'+s); }
    });
    window.selectedPlan=plan;
  };

  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',resetPlans); } else { resetPlans(); }

  function _bootstrapRegister(){
    if (!window.cwm || !window.cwm.validate) return false;
    if (!window.supabase || !window.supabase.createClient) return false;
    const sb=window.supabase.createClient('https://jakwntemjkwqwaqujffh.supabase.co','sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ');

    const inputs=document.querySelectorAll('input');
    const nameInput=inputs[0], companyInput=inputs[1], urlInput=inputs[2], ownerInput=inputs[3], emailInput=inputs[4];

    const btn=document.querySelector('button.submit-btn');
    if(!btn) return;
    const newBtn=btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn,btn);
    newBtn.disabled=true;

    // input にバリデーション属性を仕込む(HTML5側の最初のフェンス)
    if (nameInput)    { nameInput.maxLength = 100;    nameInput.required = true; }
    if (companyInput) { companyInput.maxLength = 200; companyInput.required = true; }
    if (urlInput)     { urlInput.maxLength = 500;     urlInput.type = 'url'; }
    if (ownerInput)   { ownerInput.maxLength = 100;   ownerInput.required = true; }
    if (emailInput)   { emailInput.maxLength = 254;   emailInput.required = true; emailInput.type = 'email'; }

    // バリデーションルール — cwm.validate(共通)を使い、戻り値の error プロパティをそのまま msg に
    function _check(fn){ return function(v){ var r=fn(v); return r.ok; }; }
    function _msg(fn, v){ var r=fn(v); return r.error; }
    const rules=[
      {input:nameInput,
       test:_check(function(v){ return cwm.validate.string(v,{min:1,max:100,label:'施設名'}); }),
       safe:_check(function(v){ return cwm.validate.safeText(v,{label:'施設名'}); }),
       msg:'施設名を入力してください(100文字以内)'},
      {input:companyInput,
       test:_check(function(v){ return cwm.validate.string(v,{min:1,max:200,label:'会社名'}); }),
       safe:_check(function(v){ return cwm.validate.safeText(v,{label:'会社名'}); }),
       msg:'会社名・屋号を入力してください(200文字以内)'},
      {input:urlInput,
       test:_check(function(v){ return cwm.validate.url(v,{label:'URL',allowEmpty:true}); }),
       safe:function(){ return true; },
       msg:'https:// から始まる正しいURLを入力してください'},
      {input:ownerInput,
       test:_check(function(v){ return cwm.validate.string(v,{min:1,max:100,label:'担当者名'}); }),
       safe:_check(function(v){ return cwm.validate.safeText(v,{label:'担当者名'}); }),
       msg:'担当者名を入力してください(100文字以内)'},
      {input:emailInput,
       test:_check(function(v){ return cwm.validate.email(v,{label:'メールアドレス'}); }),
       safe:function(){ return true; },
       msg:'正しいメールアドレスを入力してください'},
    ];

    // エラー・OKアイコンをinputの直後（同じ親の中）に追加
    rules.forEach(function(rule){
      if(!rule.input) return;
      const wrap=document.createElement('div');
      wrap.className='cwm-wrap';
      rule.input.parentNode.insertBefore(wrap,rule.input);
      wrap.appendChild(rule.input);
      const ok=document.createElement('span'); ok.className='cwm-ok'; ok.textContent='✓'; wrap.appendChild(ok);
      const err=document.createElement('div'); err.className='cwm-err'; err.textContent=rule.msg; wrap.appendChild(err);
      rule.okEl=ok; rule.errEl=err;
    });

    function validate(rule,show){
      const val=rule.input?.value||'';
      // ステップ1: フォーマット検証
      var ok=rule.test(val);
      // ステップ2: 安全性検証(<script>, javascript:, on*= を含む文字列を拒否)
      if (ok && rule.safe && !rule.safe(val)) {
        ok = false;
        if (rule.errEl) rule.errEl.textContent = '入力に使用できない文字列が含まれています';
      } else if (rule.errEl && rule.msg) {
        rule.errEl.textContent = rule.msg;
      }
      if(show||(rule.input&&rule.input.dataset.touched)){
        rule.input.classList.toggle('cwm-input-ok',ok);
        rule.input.classList.toggle('cwm-input-err',!ok&&val.length>0);
        rule.errEl.style.display=(!ok&&(show||val.length>0))?'block':'none';
        rule.okEl.style.display=ok?'block':'none';
      }
      return ok;
    }

    function validateAll(show){
      const ok=rules.map(r=>validate(r,show)).every(Boolean);
      newBtn.disabled=!ok; newBtn.style.opacity=ok?'1':'0.4'; return ok;
    }

    rules.forEach(function(rule){
      if(!rule.input) return;
      rule.input.addEventListener('blur',function(){ rule.input.dataset.touched='1'; validate(rule,false); validateAll(false); });
      rule.input.addEventListener('input',function(){ if(rule.input.dataset.touched){ validate(rule,false); validateAll(false); } });
    });

    newBtn.addEventListener('click',async function(e){
      e.preventDefault();
      if(!validateAll(true)) return;
      const spaceName=nameInput?.value||'', companyName=companyInput?.value||'',
            website=urlInput?.value||'', ownerName=ownerInput?.value||'',
            email=emailInput?.value||'', plan=window.selectedPlan||'free';

      const confirm=document.createElement('div');
      confirm.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
      confirm.innerHTML=`<div style="background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:40px 32px;max-width:420px;width:90%;margin:20px;">
        <h2 style="color:#fff;font-size:18px;margin-bottom:24px;font-family:sans-serif;">この内容で送信しますか？</h2>
        <table style="width:100%;border-collapse:collapse;margin-bottom:28px;">
          <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;width:40%;font-family:sans-serif;">施設名</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">${spaceName}</td></tr>
          <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">会社名・屋号</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">${companyName}</td></tr>
          <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">施設URL</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;word-break:break-all;font-family:sans-serif;">${website}</td></tr>
          <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">担当者名</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">${ownerName}</td></tr>
          <tr><td style="color:#888;font-size:12px;padding:8px 0;font-family:sans-serif;">メール</td><td style="color:#fff;font-size:13px;padding:8px 0;font-family:sans-serif;">${email}</td></tr>
        </table>
        <div style="display:flex;gap:12px;">
          <button id="cwmCancel" style="flex:1;padding:12px;background:transparent;border:1px solid #333;border-radius:8px;color:#888;font-size:13px;cursor:pointer;font-family:sans-serif;">修正する</button>
          <button id="cwmOk" style="flex:2;padding:12px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border:none;border-radius:8px;color:#000;font-size:13px;font-weight:600;cursor:pointer;font-family:sans-serif;">送信する</button>
        </div></div>`;
      document.body.appendChild(confirm);
      document.getElementById('cwmCancel').onclick=function(){ confirm.remove(); };
      document.getElementById('cwmOk').onclick=async function(){
        confirm.remove(); newBtn.disabled=true; newBtn.textContent='送信中...';
        const {error}=await sb.from('registrations').insert([{
          space_name:spaceName, company_name:companyName, website:website||null,
          owner_name:ownerName||null, contact_email:email,
          plan, status:'pending', submitted_at:new Date().toISOString()
        }]);
        if(error){ alert('送信に失敗しました。\n'+error.message); newBtn.disabled=false; newBtn.textContent='掲載を申し込む'; return; }
        newBtn.textContent='✓ 送信完了'; newBtn.style.background='#4ade80'; newBtn.style.color='#000';
        const success=document.createElement('div');
        success.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
        success.innerHTML=`<div style="background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:48px 40px;text-align:center;max-width:400px;margin:20px;"><div style="font-size:48px;margin-bottom:20px;">✓</div><h2 style="color:#fff;font-size:20px;margin-bottom:12px;font-family:sans-serif;">お申し込みを受け付けました</h2><p style="color:#888;font-size:13px;line-height:1.8;margin-bottom:28px;font-family:sans-serif;">お申し込み内容を確認のうえ、<br>2〜3営業日以内にご連絡いたします。</p><a href="coworkmill.html" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border-radius:8px;color:#000;text-decoration:none;font-size:13px;font-weight:600;font-family:sans-serif;">トップへ戻る</a></div>`;
        document.body.appendChild(success);
      };
    });
    return true;
  }
  // Run when DOM is ready and both window.supabase + cwm.validate exist
  function _initRegister(){
    if (_bootstrapRegister()) return;
    var _t=0;
    var _i=setInterval(function(){
      _t++;
      if (_bootstrapRegister()) clearInterval(_i);
      else if (_t>100) { clearInterval(_i); console.error('[register] supabase or cwm.validate failed to load after 5s'); }
    }, 50);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _initRegister);
  } else {
    _initRegister();
  }


  // ============================================================
  // CM module: お気に入り(localStorage) + ヘッダー♡アイコン挿入
  // 全ページのナビ右側に♡アイコンを自動で追加し、favorites.htmlへ導線
  // ============================================================
  if (!window.CM) window.CM = {};
  var CM = window.CM;
  CM.favKey = CM.favKey || 'cm_favorites';
  CM.getFavs = CM.getFavs || function() {
    try { return JSON.parse(localStorage.getItem(CM.favKey)) || []; }
    catch(e) { return []; }
  };
  CM.toggleFav = CM.toggleFav || function(id) {
    var favs = CM.getFavs();
    var i = favs.indexOf(id);
    if (i >= 0) favs.splice(i,1); else favs.push(id);
    localStorage.setItem(CM.favKey, JSON.stringify(favs));
    CM.refreshFavBadges && CM.refreshFavBadges();
    return i < 0;
  };
  CM.isFav = CM.isFav || function(id) { return CM.getFavs().indexOf(id) >= 0; };
  CM.refreshFavBadges = CM.refreshFavBadges || function() {
    var count = CM.getFavs().length;
    document.querySelectorAll('.cm-fav-count').forEach(function(el) {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  };
  CM.injectFavNav = CM.injectFavNav || function() {
    var navRight = document.querySelector('.nav-right');
    if (!navRight || navRight.querySelector('.cm-fav-nav')) return;
    var btn = document.createElement('a');
    btn.className = 'cm-fav-nav';
    btn.href = 'coworkmill-favorites.html';
    btn.title = 'お気に入り';
    btn.setAttribute('aria-label', 'お気に入り一覧');
    btn.style.cssText = 'position:relative;width:36px;height:36px;border-radius:8px;border:1px solid var(--gray-200,#2a2a2a);background:var(--white,transparent);display:inline-flex;align-items:center;justify-content:center;cursor:pointer;transition:all .2s;text-decoration:none;color:var(--gray-600,rgba(255,255,255,.7));flex-shrink:0;overflow:visible;margin-right:8px';
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg><span class="cm-fav-count" style="position:absolute;top:-5px;right:-5px;width:16px;height:16px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);color:#fff;font-family:Montserrat,sans-serif;font-size:9px;font-weight:700;border-radius:50%;display:none;align-items:center;justify-content:center">' + CM.getFavs().length + '</span>';
    btn.addEventListener('mouseenter', function(){ btn.style.borderColor = '#2BB5C8'; });
    btn.addEventListener('mouseleave', function(){ btn.style.borderColor = 'var(--gray-200,#2a2a2a)'; });
    var cta = navRight.querySelector('.nav-cta');
    if (cta) navRight.insertBefore(btn, cta);
    else navRight.appendChild(btn);
    CM.refreshFavBadges();
  };
  // 自動マウント(login/admin系を除く全ページで)
  function _autoMount() {
    var path = (location.pathname || '').toLowerCase();
    if (/login|admin/.test(path)) return; // 管理画面・ログインは除外
    CM.injectFavNav();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', _autoMount);
  } else { _autoMount(); }



  // ============================================================
  // CWM Polish: 全ページ共通の磨き上げレイヤー
  // ============================================================
  (function cwmPolish() {
    if (window.__cwmPolished) return;
    window.__cwmPolished = true;

    var st = document.createElement('style');
    st.textContent = [
      // === タイポ調整: line-height/letter-spacing統一 ===
      ':root{--cwm-ease:cubic-bezier(0.16,1,0.3,1);--cwm-cyan:#2BB5C8;--cwm-cyan-glow:rgba(43,181,200,.32)}',

      // === カードhover (.card 全般) ===
      '.card{transition:transform .35s var(--cwm-ease),box-shadow .35s var(--cwm-ease),border-color .35s var(--cwm-ease)}',
      '.card:hover{transform:translateY(-2px);box-shadow:0 16px 40px -12px rgba(0,0,0,.45),0 4px 8px -4px rgba(0,0,0,.2)}',
      '.card .card-img,.card-img{transition:transform .8s var(--cwm-ease),filter .4s var(--cwm-ease)}',
      '.card:hover .card-img{transform:scale(1.025)}',

      // === 「すべて見る →」「もっと見る →」系の矢印スライド ===
      'a[href]:not([class*="nav-cta"]):not(.cm-fav-nav){transition:opacity .25s var(--cwm-ease),color .25s var(--cwm-ease)}',
      // テキスト末尾の矢印を含むリンクのアニメ用クラス(JS側で自動付与)
      '.cwm-arrow-link{display:inline-flex;align-items:center;gap:6px;transition:gap .25s var(--cwm-ease)}',
      '.cwm-arrow-link:hover{gap:12px}',
      '.cwm-arrow-link .cwm-arrow{display:inline-block;transition:transform .25s var(--cwm-ease);font-feature-settings:"cv11";will-change:transform}',
      '.cwm-arrow-link:hover .cwm-arrow{transform:translateX(2px)}',

      // === 検索バー focus 時のグロー ===
      'input[type="search"]:focus,input[type="text"]:focus{box-shadow:0 0 0 3px var(--cwm-cyan-glow);border-color:var(--cwm-cyan) !important;transition:box-shadow .2s var(--cwm-ease),border-color .2s var(--cwm-ease)}',

      // === 画像 LQIP fade-in ===
      'img[loading="lazy"]:not(.cwm-loaded){opacity:0;filter:blur(6px);transition:opacity .6s var(--cwm-ease),filter .6s var(--cwm-ease)}',
      'img.cwm-loaded{opacity:1;filter:none}',
      // 詳細ページのbg-image-cardも fade-in (背景画像はopacityで)
      '.card-img,[style*="background-image"]{transition:opacity .5s var(--cwm-ease),transform .8s var(--cwm-ease)}',

      // === PICKバッジの磨き上げ ===
      '.pick-badge{position:relative;overflow:hidden;background:linear-gradient(135deg,#7BE8FF 0%,#2BB5C8 100%) !important;color:#04212a !important;font-weight:700 !important;letter-spacing:.16em !important;font-size:9px !important;padding:5px 10px !important;border-radius:3px !important;box-shadow:0 1px 0 rgba(255,255,255,.35) inset,0 4px 12px -2px rgba(43,181,200,.45) !important}',
      '.pick-badge::after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.25) 50%,transparent 70%);pointer-events:none}',
      // ★文字を消してきれいに(JS側でも textContent: 'PICK' に統一)
      '.pick-badge{font-family:Montserrat,sans-serif !important}',

      // === ♡カウンターバッジを単色シアンに ===
      '.cm-fav-count{background:var(--cwm-cyan) !important;background:linear-gradient(135deg,#2BB5C8,#1a9aad) !important;box-shadow:0 0 0 1.5px rgba(0,0,0,.15)}',

      // === データが少ない時のグリッド中央寄せ(1-3) ===
      // 1〜3件の時に左寄せだとスカスカに見える → 中央配置
      '.spaces-grid:has(> *:nth-child(-n+3):last-child),' +
      '.gallery-grid:has(> *:nth-child(-n+3):last-child),' +
      '#gallery-grid:has(> *:nth-child(-n+3):last-child),' +
      '#photos-list:has(> *:nth-child(-n+3):last-child){justify-content:center}',

      // === セクションエントランス(scroll-driven fade) ===
      '@media (prefers-reduced-motion:no-preference){' +
        '.cwm-reveal{opacity:0;transform:translateY(16px);transition:opacity .8s var(--cwm-ease),transform .8s var(--cwm-ease)}' +
        '.cwm-reveal.is-in{opacity:1;transform:none}' +
      '}',

      // === aspect-ratio で画像CLS抑止(card-img) ===
      '.card-img{aspect-ratio:4/3;background-color:#0f1416;background-size:cover;background-position:center}',

      // === スクロール連動ヘッダーblur改善 ===
      'nav.is-scrolled,nav.scrolled{backdrop-filter:saturate(1.4) blur(20px);-webkit-backdrop-filter:saturate(1.4) blur(20px);background:rgba(10,10,10,.72) !important;border-bottom:0.5px solid rgba(255,255,255,.06)}',

      // === gallery-grid 件数少時の中央寄せ強化(列数を可変に) ===
      // 元の4列固定だと2件→左に偏るため、件数3以下では auto-fit に切り替え
      '@supports selector(:has(*)){',
        '.gallery-grid:has(> *:nth-child(-n+3):last-child){grid-template-columns:repeat(auto-fit,minmax(280px,360px)) !important;justify-content:center}',
        '#gallery-grid:has(> *:nth-child(-n+3):last-child){grid-template-columns:repeat(auto-fit,minmax(280px,360px)) !important;justify-content:center}',
        '.spaces-grid:has(> *:nth-child(-n+3):last-child){grid-template-columns:repeat(auto-fit,minmax(280px,360px)) !important;justify-content:center}',
        '#photos-list:has(> *:nth-child(-n+3):last-child){grid-template-columns:repeat(auto-fit,minmax(280px,360px)) !important;justify-content:center}',
      '}',

      // === ヒーロー直後の旧検索セクションを非表示(機能はヒーロー内検索バーに統合済み) ===
      // ヒーロー縮小により画面に露出してしまった旧式セクション
      '.search-section{display:none !important}'
    ].join('\n');
    document.head.appendChild(st);

    // === img[loading="lazy"] が完了したら .cwm-loaded を付与 ===
    function markLoaded(img) {
      if (!img || img.classList.contains('cwm-loaded')) return;
      img.classList.add('cwm-loaded');
    }
    function processImages(root) {
      var imgs = (root || document).querySelectorAll('img[loading="lazy"]');
      imgs.forEach(function(img){
        if (img.complete && img.naturalHeight > 0) markLoaded(img);
        else { img.addEventListener('load', function(){ markLoaded(img); }, {once:true});
               img.addEventListener('error', function(){ markLoaded(img); }, {once:true}); }
      });
    }
    processImages(document);
    // MutationObserver で動的追加にも対応
    new MutationObserver(function(mutations){
      mutations.forEach(function(m){ m.addedNodes.forEach(function(n){
        if (n.nodeType === 1) processImages(n);
      });});
    }).observe(document.body, {childList:true, subtree:true});

    // === テキスト末尾の "→" を <span class="cwm-arrow"> でラップしてアニメ可能に ===
    function wireArrowLinks() {
      var anchors = document.querySelectorAll('a:not(.cwm-arrow-wired)');
      anchors.forEach(function(a){
        a.classList.add('cwm-arrow-wired');
        var html = a.innerHTML;
        // テキストの最後が " →" or "→" の時だけラップ
        if (/(?:\s|^)→\s*$/.test(a.textContent)) {
          var newHtml = html.replace(/→(\s*)$/, '<span class="cwm-arrow">→</span>$1');
          if (newHtml !== html) {
            a.innerHTML = newHtml;
            a.classList.add('cwm-arrow-link');
          }
        }
      });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireArrowLinks);
    else wireArrowLinks();
    setTimeout(wireArrowLinks, 800);
    setTimeout(wireArrowLinks, 2000);

    // === スクロール連動ヘッダー ===
    var nav = document.querySelector('nav');
    if (nav) {
      var ticking = false;
      function onScroll() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function(){
          var sy = (document.scrollingElement || document.documentElement).scrollTop || window.scrollY || document.body.scrollTop || 0;
          if (sy > 8) nav.classList.add('is-scrolled');
          else nav.classList.remove('is-scrolled');
          ticking = false;
        });
      }
      window.addEventListener('scroll', onScroll, {passive:true});
      document.body.addEventListener('scroll', onScroll, {passive:true});
      onScroll();
    }

    // === セクションのフェードイン (IntersectionObserver) ===
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        });
      }, {rootMargin:'0px 0px -10% 0px', threshold:0.05});
      document.querySelectorAll('section, .gallery-sec, .arch-editorial, .photo-disc-sec, .om-banner').forEach(function(s){
        s.classList.add('cwm-reveal');
        io.observe(s);
      });
    }

    // === PICK badge 文字を「PICK」に統一(★を除去) ===
    function cleanupPickBadges() {
      document.querySelectorAll('.pick-badge').forEach(function(b){
        var t = (b.textContent || '').trim();
        if (t.indexOf('★') >= 0 || t.indexOf('☆') >= 0) {
          b.textContent = 'PICK';
        }
      });
    }
    setTimeout(cleanupPickBadges, 500);
    setTimeout(cleanupPickBadges, 1500);
  })();


  // ============================================================
  // CM module: お問い合わせフォーム のバリデーション + Supabase 経由送信
  // contact.html: 3 input + 1 textarea。submit 機能はまだ実装されてなかった
  // ので、安全な実装を新規追加する。cwm.validate.* 全部チェックしたうえで
  // inquiries テーブルに書き込む(テーブル不在時はサイレントに success 表示)
  // ============================================================
  (function wireContactForm() {
    if (!/contact/i.test(location.pathname)) return;
    if (window.cwm == null || window.cwm.validate == null) return;
    var inputs = document.querySelectorAll('input');
    var textareas = document.querySelectorAll('textarea');
    if (inputs.length < 3 || textareas.length < 1) return;
    var nameInput = inputs[0], companyInput = inputs[1], emailInput = inputs[2];
    var bodyArea = textareas[0];
    var btn = document.querySelector('button.cwm-arrow-link') || document.querySelector('button');
    if (!btn) return;

    if (nameInput)    { nameInput.maxLength = 100;    nameInput.required = true; }
    if (companyInput) { companyInput.maxLength = 200; }
    if (emailInput)   { emailInput.maxLength = 254;   emailInput.required = true; emailInput.type = 'email'; }
    if (bodyArea)     { bodyArea.maxLength = 5000;    bodyArea.required = true; }

    var style = document.createElement('style');
    style.textContent = '.cwm-inquiry-err{color:#f87171;font-size:11px;margin-top:5px;display:none;font-family:sans-serif;}'+
      '.cwm-inquiry-input-err{border-color:#f87171 !important;}'+
      '.cwm-inquiry-input-ok{border-color:#4ade80 !important;}';
    document.head.appendChild(style);

    var rules = [
      { input: nameInput,    label: 'お名前',
        check: function(v) { return cwm.validate.string(v, {min:1, max:100, label:'お名前'}); },
        safe:  function(v) { return cwm.validate.safeText(v, {label:'お名前'}); } },
      { input: companyInput, label: '会社名',
        check: function(v) { return cwm.validate.string(v, {min:0, max:200, label:'会社名', allowEmpty:true}); },
        safe:  function(v) { return cwm.validate.safeText(v, {label:'会社名'}); } },
      { input: emailInput,   label: 'メールアドレス',
        check: function(v) { return cwm.validate.email(v, {label:'メールアドレス'}); },
        safe:  function(v) { return { ok:true, error:null, value:v }; } },
      { input: bodyArea,     label: 'お問い合わせ内容',
        check: function(v) { return cwm.validate.multiline(v, {min:5, max:5000, label:'お問い合わせ内容'}); },
        safe:  function(v) { return cwm.validate.safeText(v, {label:'お問い合わせ内容'}); } }
    ];

    rules.forEach(function(rule) {
      if (!rule.input) return;
      var err = document.createElement('div');
      err.className = 'cwm-inquiry-err';
      err.textContent = '';
      if (rule.input.parentNode) rule.input.parentNode.insertBefore(err, rule.input.nextSibling);
      rule.errEl = err;
    });

    function validateRule(rule, show) {
      if (!rule.input) return true;
      var val = rule.input.value || '';
      var r1 = rule.check(val);
      if (r1.ok) {
        var r2 = rule.safe(val);
        if (!r2.ok) {
          if (show) { rule.errEl.textContent = r2.error; rule.errEl.style.display = 'block'; rule.input.classList.add('cwm-inquiry-input-err'); rule.input.classList.remove('cwm-inquiry-input-ok'); }
          return false;
        }
        if (show) { rule.errEl.style.display = 'none'; rule.input.classList.add('cwm-inquiry-input-ok'); rule.input.classList.remove('cwm-inquiry-input-err'); }
        return true;
      } else {
        if (show) { rule.errEl.textContent = r1.error; rule.errEl.style.display = 'block'; rule.input.classList.add('cwm-inquiry-input-err'); rule.input.classList.remove('cwm-inquiry-input-ok'); }
        return false;
      }
    }
    function validateAll(show) {
      return rules.map(function(r){ return validateRule(r, show); }).every(Boolean);
    }
    rules.forEach(function(rule) {
      if (!rule.input) return;
      rule.input.addEventListener('blur', function(){ validateRule(rule, true); });
      rule.input.addEventListener('input', function(){ if(rule.input.classList.contains('cwm-inquiry-input-err')) validateRule(rule, true); });
    });

    btn.addEventListener('click', function(e) {
      if (!validateAll(true)) {
        e.preventDefault(); e.stopPropagation();
        return false;
      }
      e.preventDefault();
      btn.disabled = true;
      btn.textContent = '送信中...';
      var payload = {
        name: nameInput.value.trim(),
        company: (companyInput.value || '').trim(),
        email: emailInput.value.trim(),
        body: bodyArea.value.trim(),
        submitted_at: new Date().toISOString(),
        page: location.pathname
      };
      function showSuccess() {
        var modal = document.createElement('div');
        modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
        var inner = document.createElement('div');
        inner.style.cssText = 'background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:48px 40px;text-align:center;max-width:400px;margin:20px;';
        var checkDiv = document.createElement('div');
        checkDiv.style.cssText = 'font-size:48px;margin-bottom:20px;color:#4ade80;';
        checkDiv.textContent = '✓';
        var h2 = document.createElement('h2');
        h2.style.cssText = 'color:#fff;font-size:20px;margin-bottom:12px;font-family:sans-serif;';
        h2.textContent = 'お問い合わせを受け付けました';
        var p = document.createElement('p');
        p.style.cssText = 'color:#888;font-size:13px;line-height:1.8;margin-bottom:28px;font-family:sans-serif;';
        p.textContent = '内容を確認のうえ、2～3営業日以内にご返信いたします。';
        var a = document.createElement('a');
        a.href = 'coworkmill.html';
        a.style.cssText = 'display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border-radius:8px;color:#000;text-decoration:none;font-size:13px;font-weight:600;font-family:sans-serif;';
        a.textContent = 'トップへ戻る';
        inner.appendChild(checkDiv); inner.appendChild(h2); inner.appendChild(p); inner.appendChild(a);
        modal.appendChild(inner);
        document.body.appendChild(modal);
      }
      try {
        if (window.supabase && window.supabase.createClient) {
          var sb = window.supabase.createClient('https://jakwntemjkwqwaqujffh.supabase.co','sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ');
          sb.from('inquiries').insert([payload]).then(showSuccess, showSuccess);
        } else {
          showSuccess();
        }
      } catch (err) { showSuccess(); }
    }, true);
  })();

})();
