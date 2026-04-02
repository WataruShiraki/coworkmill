// coworkmill-features.js
// 掲載申請フォームのSupabase送信機能

const SB_URL = 'https://jakwntemjkwqwaqujffh.supabase.co';
const SB_KEY = 'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ';

document.addEventListener('DOMContentLoaded', function () {
  // Supabaseクライアント初期化
  const sb = window.supabase.createClient(SB_URL, SB_KEY);

  // 送信ボタンを探す（テキストで判定）
  const allButtons = document.querySelectorAll('button');
  let submitBtn = null;
  allButtons.forEach(btn => {
    if (btn.textContent.includes('申し込む') || btn.textContent.includes('送信') || btn.textContent.includes('審査')) {
      submitBtn = btn;
    }
  });

  if (!submitBtn) return;

  submitBtn.addEventListener('click', async function (e) {
    e.preventDefault();

    // 全inputとselectの値を収集
    const inputs = document.querySelectorAll('input, select, textarea');
    const formData = {};
    inputs.forEach(inp => {
      if (inp.name) formData[inp.name] = inp.value;
      else if (inp.id) formData[inp.id] = inp.value;
      else if (inp.placeholder) formData[inp.placeholder] = inp.value;
    });

    // よく使われるIDで施設名・メールを取得
    const spaceName =
      document.getElementById('spaceName')?.value ||
      document.getElementById('space_name')?.value ||
      document.getElementById('facilityName')?.value ||
      document.querySelector('input[placeholder*="ATELIER"], input[placeholder*="施設名"]')?.value || '';

    const contactEmail =
      document.getElementById('ownerEmail')?.value ||
      document.getElementById('contact_email')?.value ||
      document.getElementById('email')?.value ||
      document.querySelector('input[type="email"]')?.value || '';

    const ownerName =
      document.getElementById('ownerName')?.value ||
      document.getElementById('owner_name')?.value ||
      document.getElementById('contactName')?.value ||
      document.querySelector('input[placeholder*="山田"], input[placeholder*="担当者名"]')?.value || '';

    const area =
      document.getElementById('area')?.value ||
      document.getElementById('city')?.value ||
      document.querySelector('input[placeholder*="表参道"], input[placeholder*="エリア"]')?.value || '';

    const websiteUrl =
      document.getElementById('website')?.value ||
      document.getElementById('url')?.value ||
      document.getElementById('siteUrl')?.value ||
      document.querySelector('input[type="url"], input[placeholder*="https"]')?.value || '';

    // プラン取得
    const selectedPlan = document.querySelector('input[name="plan"]:checked')?.value ||
      window.selectedPlan || 'free';

    // バリデーション
    if (!spaceName || !contactEmail) {
      alert('施設名とメールアドレスは必須です。');
      return;
    }

    // ボタンを無効化
    submitBtn.disabled = true;
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '送信中...';

    // Supabaseに送信
    const { error } = await sb.from('registrations').insert([{
      space_name: spaceName,
      contact_email: contactEmail,
      owner_name: ownerName || null,
      area: area || null,
      website: websiteUrl || null,
      plan: selectedPlan,
      form_data: JSON.stringify(formData),
      status: 'pending',
      submitted_at: new Date().toISOString(),
    }]);

    if (error) {
      console.error('送信エラー:', error);
      alert('送信に失敗しました。しばらくしてから再度お試しください。\n' + error.message);
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      return;
    }

    // 成功時
    submitBtn.textContent = '✓ 送信完了';
    submitBtn.style.background = '#4ade80';
    submitBtn.style.color = '#000';

    // 成功メッセージ表示
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
      position:fixed; top:0; left:0; right:0; bottom:0;
      background:rgba(0,0,0,0.85); display:flex; align-items:center;
      justify-content:center; z-index:9999;
    `;
    successDiv.innerHTML = `
      <div style="background:#111; border:1px solid #222; border-radius:16px;
        padding:48px 40px; text-align:center; max-width:400px; margin:20px;">
        <div style="font-size:48px; margin-bottom:20px;">✓</div>
        <h2 style="color:#fff; font-size:20px; margin-bottom:12px; font-family:sans-serif;">
          お申し込みを受け付けました
        </h2>
        <p style="color:#888; font-size:13px; line-height:1.8; margin-bottom:24px; font-family:sans-serif;">
          2〜3営業日以内に<br>審査結果をメールにてお知らせします。
        </p>
        <a href="coworkmill.html" style="
          display:inline-block; padding:12px 28px;
          background:linear-gradient(135deg,#79F1A4,#2BB5C8);
          border-radius:8px; color:#000; text-decoration:none;
          font-size:13px; font-weight:600; font-family:sans-serif;">
          トップへ戻る
        </a>
      </div>
    `;
    document.body.appendChild(successDiv);
  });
});
