// coworkmill-features.js

const SB_URL = 'https://jakwntemjkwqwaqujffh.supabase.co';
const SB_KEY = 'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ';

function initFeatures() {
  if (!window.supabase) {
    setTimeout(initFeatures, 100);
    return;
  }

  const sb = window.supabase.createClient(SB_URL, SB_KEY);

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

    const spaceName =
      document.getElementById('spaceName')?.value ||
      document.querySelector('input[placeholder*="ATELIER"], input[placeholder*="施設名"]')?.value || '';

    const contactEmail =
      document.getElementById('ownerEmail')?.value ||
      document.getElementById('contact_email')?.value ||
      document.querySelector('input[type="email"]')?.value || '';

    const ownerName =
      document.getElementById('ownerName')?.value ||
      document.querySelector('input[placeholder*="山田"], input[placeholder*="担当者名"]')?.value || '';

    const area =
      document.getElementById('area')?.value ||
      document.querySelector('input[placeholder*="表参道"], input[placeholder*="エリア"]')?.value || '';

    const websiteUrl =
      document.getElementById('website')?.value ||
      document.querySelector('input[type="url"], input[placeholder*="https"]')?.value || '';

    const selectedPlan = document.querySelector('input[name="plan"]:checked')?.value || 'free';

    if (!spaceName || !contactEmail) {
      alert('施設名とメールアドレスは必須です。');
      return;
    }

    submitBtn.disabled = true;
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '送信中...';

    const { error } = await sb.from('registrations').insert([{
      space_name: spaceName,
      contact_email: contactEmail,
      owner_name: ownerName || null,
      area: area || null,
      website: websiteUrl || null,
      plan: selectedPlan,
      status: 'pending',
      submitted_at: new Date().toISOString(),
    }]);

    if (error) {
      alert('送信に失敗しました。\n' + error.message);
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
      return;
    }

    submitBtn.textContent = '✓ 送信完了';
    submitBtn.style.background = '#4ade80';
    submitBtn.style.color = '#000';

    const successDiv = document.createElement('div');
    successDiv.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);display:flex;align-items:center;justify-content:center;z-index:9999;';
    successDiv.innerHTML = `
      <div style="background:#111;border:1px solid #222;border-radius:16px;padding:48px 40px;text-align:center;max-width:400px;margin:20px;">
        <div style="font-size:48px;margin-bottom:20px;">✓</div>
        <h2 style="color:#fff;font-size:20px;margin-bottom:12px;font-family:sans-serif;">お申し込みを受け付けました</h2>
        <p style="color:#888;font-size:13px;line-height:1.8;margin-bottom:24px;font-family:sans-serif;">2〜3営業日以内に<br>審査結果をメールにてお知らせします。</p>
        <a href="coworkmill.html" style="display:inline-block;padding:12px 28px;background:linear-gradient(135deg,#79F1A4,#2BB5C8);border-radius:8px;color:#000;text-decoration:none;font-size:13px;font-weight:600;font-family:sans-serif;">トップへ戻る</a>
      </div>`;
    document.body.appendChild(successDiv);
  });
}

initFeatures();
