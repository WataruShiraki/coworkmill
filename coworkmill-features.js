(function() {
  // ---- CSS ----
  const css = document.createElement('style');
  css.textContent = `
    #plan-free, #plan-standard, #plan-pro { position:relative !important; cursor:default !important; }
    #plan-free.plan-selected, #plan-standard.plan-selected, #plan-pro.plan-selected {
      border:2px solid #2BB5C8 !important; background:rgba(43,181,200,0.06) !important;
    }
    .cwm-field-wrap { position:relative; }
    .cwm-input-ok   { border-color:#4ade80 !important; }
    .cwm-input-err  { border-color:#f87171 !important; }
    .cwm-err-msg {
      color:#f87171; font-size:11px; margin-top:5px;
      display:none; font-family:sans-serif;
    }
    .cwm-ok-icon {
      position:absolute; right:12px; top:50%; transform:translateY(-50%);
      color:#4ade80; font-size:14px; pointer-events:none;
    }
    .submit-btn:disabled {
      opacity:0.4 !important; cursor:not-allowed !important;
    }
  `;
  document.head.appendChild(css);

  // ---- プランリセット ----
  function resetPlans() {
    ['free','standard','pro'].forEach(function(p) {
      const el = document.getElementById('plan-' + p);
      if (!el) return;
      el.classList.remove('plan-selected');
      el.querySelectorAll('div').forEach(function(d) { if (d.textContent.trim()==='選択中') d.remove(); });
      let s = (el.getAttribute('style')||'').replace(/border\s*:[^;]+;?\s*/gi,'');
      el.setAttribute('style','border:1px solid #2a2a2a;'+s);
    });
    window.selectedPlan = 'free';
  }

  window.selectPlan = function(plan) {
    ['free','standard','pro'].forEach(function(p) {
      const el = document.getElementById('plan-'+p);
      if (!el) return;
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
    window.selectedPlan = plan;
  };

  if (document.readyState==='loading') {
    document.addEventListener('DOMContentLoaded', resetPlans);
  } else { resetPlans(); }

  // ---- Supabase + バリデーション ----
  const s = document.createElement('script');
  s.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';
  s.onload = function() {
    const sb = window.supabase.createClient(
      'https://jakwntemjkwqwaqujffh.supabase.co',
      'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ'
    );

    const inputs = document.querySelectorAll('input');
    const nameInput  = inputs[0]; // 施設名
    const urlInput   = inputs[1]; // 施設URL
    const ownerInput = inputs[2]; // 担当者名
    const emailInput = inputs[3]; // 担当者メール

    const btn = document.querySelector('button.submit-btn');
    if (!btn) return;
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
    newBtn.disabled = true;

    // バリデーションルール
    const rules = [
      { input: nameInput,  test: v => v.trim().length > 0,       msg: '施設名を入力してください' },
      { input: urlInput,   test: v => /^https?:\/\/.+\..+/.test(v.trim()), msg: 'URLは https:// から始まる形式で入力してください' },
      { input: ownerInput, test: v => v.trim().length > 0,       msg: '担当者名を入力してください' },
      { input: emailInput, test: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()), msg: '正しいメールアドレスを入力してください' },
    ];

    // 各inputにエラー表示用要素を追加
    rules.forEach(function(rule) {
      if (!rule.input) return;
      // ラッパーを作成
      const wrap = document.createElement('div');
      wrap.className = 'cwm-field-wrap';
      rule.input.parentNode.insertBefore(wrap, rule.input);
      wrap.appendChild(rule.input);
      // OKアイコン
      const ok = document.createElement('span');
      ok.className = 'cwm-ok-icon';
      ok.textContent = '✓';
      ok.style.display = 'none';
      wrap.appendChild(ok);
      rule.okIcon = ok;
      // エラーメッセージ
      const err = document.createElement('div');
      err.className = 'cwm-err-msg';
      err.textContent = rule.msg;
      wrap.parentNode.insertBefore(err, wrap.nextSibling);
      rule.errEl = err;
    });

    function validate(rule, showError) {
      const val = rule.input?.value || '';
      const ok = rule.test(val);
      if (showError || (rule.input && rule.input.dataset.touched)) {
        rule.input.classList.toggle('cwm-input-ok', ok);
        rule.input.classList.toggle('cwm-input-err', !ok && val.length > 0);
        rule.errEl.style.display = (!ok && (showError || val.length > 0)) ? 'block' : 'none';
        rule.okIcon.style.display = ok ? 'block' : 'none';
      }
      return ok;
    }

    function validateAll(showErrors) {
      const results = rules.map(function(r){ return validate(r, showErrors); });
      const allOk = results.every(Boolean);
      newBtn.disabled = !allOk;
      newBtn.style.opacity = allOk ? '1' : '0.4';
      return allOk;
    }

    // blur時にバリデーション
    rules.forEach(function(rule) {
      if (!rule.input) return;
      rule.input.addEventListener('blur', function() {
        rule.input.dataset.touched = '1';
        validate(rule, false);
        validateAll(false);
      });
      rule.input.addEventListener('input', function() {
        if (rule.input.dataset.touched) {
          validate(rule, false);
          validateAll(false);
        }
      });
    });

    newBtn.addEventListener('click', async function(e) {
      e.preventDefault();
      if (!validateAll(true)) return;

      const spaceName = nameInput?.value || '';
      const website   = urlInput?.value || '';
      const ownerName = ownerInput?.value || '';
      const email     = emailInput?.value || '';
      const plan      = window.selectedPlan || 'free';

      // 確認モーダル
      const confirm = document.createElement('div');
      confirm.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
      confirm.innerHTML = `
        <div style="background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:40px 32px;max-width:420px;width:90%;margin:20px;">
          <h2 style="color:#fff;font-size:18px;margin-bottom:24px;font-family:sans-serif;">この内容で送信しますか？</h2>
          <table style="width:100%;border-collapse:collapse;margin-bottom:28px;">
            <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;width:40%;font-family:sans-serif;">施設名</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">${spaceName}</td></tr>
            <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">施設URL</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;word-break:break-all;font-family:sans-serif;">${website}</td></tr>
            <tr><td style="color:#888;font-size:12px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">担当者名</td><td style="color:#fff;font-size:13px;padding:8px 0;border-bottom:1px solid #1a1a1a;font-family:sans-serif;">${ownerName}</td></tr>
            <tr><td style="color:#888;font-size:12px;padding:8px 0;font-family:sans-serif;">メール</td><td style="color:#fff;font-size:13px;padding:8px 0;font-family:sans-serif;">${email}</td></tr>
          </table>
          <div style="display:flex;gap:12px;">
            <button id="cwmCancel" style="flex:1;padding:12px;background:transparent;border:1px solid #333;border-radius:8px;color:#888;font-size:13px;cursor:pointer;font-family:sans-serif;">修正する</button>
            <button id="cwmOk" style="flex:2;padding:12px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border:none;border-radius:8px;color:#000;font-size:13px;font-weight:600;cursor:pointer;font-family:sans-serif;">送信する</button>
          </div>
        </div>`;
      document.body.appendChild(confirm);

      document.getElementById('cwmCancel').onclick = function(){ confirm.remove(); };
      document.getElementById('cwmOk').onclick = async function() {
        confirm.remove();
        newBtn.disabled = true;
        newBtn.textContent = '送信中...';
        const { error } = await sb.from('registrations').insert([{
          space_name: spaceName, website: website||null,
          owner_name: ownerName||null, contact_email: email,
          plan, status:'pending', submitted_at: new Date().toISOString()
        }]);
        if (error) {
          alert('送信に失敗しました。\n' + error.message);
          newBtn.disabled = false; newBtn.textContent = '審査を申し込む'; return;
        }
        newBtn.textContent = '✓ 送信完了';
        newBtn.style.background = '#4ade80';
        newBtn.style.color = '#000';
        const success = document.createElement('div');
        success.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);display:flex;align-items:center;justify-content:center;z-index:9999;';
        success.innerHTML = `<div style="background:#111;border:1px solid #2a2a2a;border-radius:16px;padding:48px 40px;text-align:center;max-width:400px;margin:20px;"><div style="font-size:48px;margin-bottom:20px;">✓</div><h2 style="color:#fff;font-size:20px;margin-bottom:12px;font-family:sans-serif;">お申し込みを受け付けました</h2><p style="color:#888;font-size:13px;line-height:1.8;margin-bottom:28px;font-family:sans-serif;">2〜3営業日以内に審査結果を<br>メールにてお知らせします。</p><a href="coworkmill.html" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border-radius:8px;color:#000;text-decoration:none;font-size:13px;font-weight:600;font-family:sans-serif;">トップへ戻る</a></div>`;
        document.body.appendChild(success);
      };
    });
  };
  document.head.appendChild(s);
})();
