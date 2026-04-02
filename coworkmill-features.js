(function() {
  const css = document.createElement('style');
  css.textContent = `
    #plan-free, #plan-standard, #plan-pro { position: relative !important; cursor: default !important; }
    #plan-free.plan-selected,
    #plan-standard.plan-selected,
    #plan-pro.plan-selected {
      border: 2px solid #2BB5C8 !important;
      background: rgba(43,181,200,0.06) !important;
    }
  `;
  document.head.appendChild(css);

  function resetAll() {
    ['free','standard','pro'].forEach(function(p) {
      const el = document.getElementById('plan-' + p);
      if (!el) return;
      el.classList.remove('plan-selected');
      el.querySelectorAll('div').forEach(function(d) {
        if (d.textContent.trim() === '選択中') d.remove();
      });
      let s = (el.getAttribute('style') || '').replace(/border\s*:[^;]+;?\s*/gi, '');
      el.setAttribute('style', 'border:1px solid #2a2a2a;' + s);
    });
    window.selectedPlan = 'free';
  }

  window.selectPlan = function(plan) {
    ['free','standard','pro'].forEach(function(p) {
      const el = document.getElementById('plan-' + p);
      if (!el) return;
      el.querySelectorAll('div').forEach(function(d) {
        if (d.textContent.trim() === '選択中') d.remove();
      });
      el.classList.remove('plan-selected');
      let s = (el.getAttribute('style') || '').replace(/border\s*:[^;]+;?\s*/gi, '');
      if (p === plan) {
        el.classList.add('plan-selected');
        el.setAttribute('style', 'border:2px solid #2BB5C8;' + s);
        const b = document.createElement('div');
        b.textContent = '選択中';
        b.style.cssText = 'position:absolute;top:10px;right:10px;font-size:8px;font-weight:600;padding:3px 8px;background:#2BB5C8;color:#000;border-radius:4px;z-index:10;';
        el.appendChild(b);
      } else {
        el.setAttribute('style', 'border:1px solid #2a2a2a;' + s);
      }
    });
    window.selectedPlan = plan;
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', resetAll);
  } else {
    resetAll();
  }

  const s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
  s.onload = function() {
    const sb = window.supabase.createClient(
      'https://jakwntemjkwqwaqujffh.supabase.co',
      'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ'
    );
    const btn = document.querySelector('button.submit-btn');
    if (!btn) return;
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    newBtn.addEventListener('click', async function(e) {
      e.preventDefault();
      const inputs = document.querySelectorAll('input');
      // エリア削除後の順番：施設名, 施設URL, 担当者名, 担当者メール
      const spaceName = inputs[0]?.value || '';
      const website   = inputs[1]?.value || '';
      const ownerName = inputs[2]?.value || '';
      const email     = inputs[3]?.value || '';
      const plan      = window.selectedPlan || 'free';

      if (!spaceName || !email) { alert('施設名とメールアドレスは必須です。'); return; }
      newBtn.disabled = true;
      newBtn.textContent = '送信中...';
      const { error } = await sb.from('registrations').insert([{
        space_name: spaceName, website: website||null,
        owner_name: ownerName||null, contact_email: email,
        plan, status: 'pending', submitted_at: new Date().toISOString()
      }]);
      if (error) {
        alert('送信に失敗しました。\n' + error.message);
        newBtn.disabled = false; newBtn.textContent = '審査を申し込む'; return;
      }
      newBtn.textContent = '✓ 送信完了';
      newBtn.style.background = '#4ade80';
      newBtn.style.color = '#000';
      const overlay = document.createElement('div');
      overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
      overlay.innerHTML = `<div style="background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:48px 40px;text-align:center;max-width:400px;margin:20px;"><div style="font-size:48px;margin-bottom:20px;">✓</div><h2 style="color:#fff;font-size:20px;margin-bottom:12px;font-family:sans-serif;">お申し込みを受け付けました</h2><p style="color:#888;font-size:13px;line-height:1.8;margin-bottom:28px;font-family:sans-serif;">2〜3営業日以内に審査結果を<br>メールにてお知らせします。</p><a href="coworkmill.html" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border-radius:8px;color:#000;text-decoration:none;font-size:13px;font-weight:600;font-family:sans-serif;">トップへ戻る</a></div>`;
      document.body.appendChild(overlay);
    });
  };
  document.head.appendChild(s);
})();
