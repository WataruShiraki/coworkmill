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

  const s=document.createElement('script');
  s.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
  s.onload=function(){
    const sb=window.supabase.createClient('https://jakwntemjkwqwaqujffh.supabase.co','sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ');

    const inputs=document.querySelectorAll('input');
    const nameInput=inputs[0], companyInput=inputs[1], urlInput=inputs[2], ownerInput=inputs[3], emailInput=inputs[4];

    const btn=document.querySelector('button.submit-btn');
    if(!btn) return;
    const newBtn=btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn,btn);
    newBtn.disabled=true;

    const rules=[
      {input:nameInput,    test:v=>v.trim().length>0,                       msg:'施設名を入力してください'},
      {input:companyInput, test:v=>v.trim().length>0,                       msg:'会社名・屋号を入力してください'},
      {input:urlInput,     test:v=>/^https?:\/\/.+\..+/.test(v.trim()),     msg:'https:// から始まるURLを入力してください'},
      {input:ownerInput,   test:v=>v.trim().length>0,                       msg:'担当者名を入力してください'},
      {input:emailInput,   test:v=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), msg:'正しいメールアドレスを入力してください'},
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
      const ok=rule.test(val);
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
  };
  document.head.appendChild(s);


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

})();
