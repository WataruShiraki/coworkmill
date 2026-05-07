// Vercel Edge Middleware
//
// 役割:
//  ① /admin, /ops 配下にベーシック認証を要求
//     (Stripe審査の「管理者画面のIPアドレス制限またはベーシック認証」要件のため)
//  ② /space/[slug] のOGPメタタグを動的に生成
//     (X/Facebook/LINEクローラー向けに、施設のメイン写真をOGPに反映)
//
// 認証情報は Vercel 環境変数で管理:
//   BASIC_AUTH_USER : ベーシック認証ユーザー名
//   BASIC_AUTH_PASS : ベーシック認証パスワード

export const config = {
  matcher: [
    // ① Basic認証
    '/admin',
    '/admin.html',
    '/admin/:path*',
    '/admin-ops',
    '/admin-ops.html',
    '/ops',
    '/ops.html',
    '/ops/:path*',
    '/ops-login',
    '/ops-login.html',
    // ② OGP動的化
    '/space/:slug',
  ],
};

const SUPABASE_URL = 'https://jakwntemjkwqwaqujffh.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ';

export default async function middleware(request: Request): Promise<Response | undefined> {
  const url = new URL(request.url);

  // ② /space/[slug] のOGP動的化
  if (url.pathname.startsWith('/space/')) {
    return await handleSpaceOgp(request);
  }

  // ① /admin, /ops のベーシック認証
  return handleBasicAuth(request);
}

// ============================================================
// ① ベーシック認証
// ============================================================
function handleBasicAuth(request: Request): Response | undefined {
  const expectedUser = (globalThis as any).process?.env?.BASIC_AUTH_USER;
  const expectedPass = (globalThis as any).process?.env?.BASIC_AUTH_PASS;

  // 環境変数が設定されていない場合は通す (設定漏れで詰まらないよう)
  if (!expectedUser || !expectedPass) {
    return undefined;
  }

  const auth = request.headers.get('authorization');

  // 認証ヘッダーがない or Basic 形式じゃない → 401
  if (!auth || !auth.startsWith('Basic ')) {
    return new Response('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="COWORKMILL Admin"',
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });
  }

  // base64デコードして user:pass に分解
  let user = '';
  let pass = '';
  try {
    const decoded = atob(auth.slice(6));
    const idx = decoded.indexOf(':');
    if (idx >= 0) {
      user = decoded.slice(0, idx);
      pass = decoded.slice(idx + 1);
    }
  } catch {
    return new Response('Invalid credentials format', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="COWORKMILL Admin"',
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });
  }

  // 認証情報チェック
  if (user !== expectedUser || pass !== expectedPass) {
    return new Response('Invalid credentials', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="COWORKMILL Admin"',
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });
  }

  // 認証成功 → undefinedを返してそのまま通す
  return undefined;
}

// ============================================================
// ② OGP動的化
// ============================================================
async function handleSpaceOgp(request: Request): Promise<Response | undefined> {
  const url = new URL(request.url);
  const slug = decodeURIComponent(url.pathname.replace(/^\/space\//, '').replace(/\/$/, ''));

  if (!slug) return undefined;

  try {
    // Supabaseから施設情報取得
    const sbRes = await fetch(
      `${SUPABASE_URL}/rest/v1/spaces?slug=eq.${encodeURIComponent(slug)}&status=eq.live&select=name,description,image_main,prefecture,area,architect_name`,
      {
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        },
      }
    );

    if (!sbRes.ok) return undefined;

    const data = await sbRes.json();
    if (!Array.isArray(data) || data.length === 0) return undefined;

    const space = data[0];

    // detail.html を取得
    const htmlRes = await fetch(`${url.origin}/detail`);
    if (!htmlRes.ok) return undefined;

    let html = await htmlRes.text();

    // OGP用の値を組み立て
    const title = `${space.name} — COWORKMILL`;
    const descParts: string[] = [];
    if (space.prefecture) descParts.push(space.prefecture);
    if (space.area && space.area !== space.prefecture) descParts.push(space.area);
    if (space.architect_name) descParts.push(`設計: ${space.architect_name}`);
    const locationLine = descParts.length > 0 ? `${descParts.join(' / ')}。` : '';
    const rawDesc = (space.description || '').replace(/\s+/g, ' ').trim();
    const description = (locationLine + rawDesc).slice(0, 160) || '建築家・設計事務所が手がけたコワーキングスペース | COWORKMILL';
    const image = space.image_main || `${url.origin}/ogp.png`;
    const pageUrl = url.href;

    // メタタグ書き換え
    html = html.replace(/<title>[^<]*<\/title>/, `<title>${escapeHtml(title)}</title>`);
    html = html.replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${escapeHtml(description)}">`);
    html = html.replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${escapeHtml(title)}">`);
    html = html.replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${escapeHtml(description)}">`);
    html = html.replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${escapeHtml(pageUrl)}">`);
    html = html.replace(/<meta property="og:image" content="[^"]*">/, `<meta property="og:image" content="${escapeHtml(image)}">`);
    html = html.replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${escapeHtml(title)}">`);
    html = html.replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${escapeHtml(description)}">`);
    html = html.replace(/<meta name="twitter:image" content="[^"]*">/, `<meta name="twitter:image" content="${escapeHtml(image)}">`);
    html = html.replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${escapeHtml(pageUrl)}">`);

    return new Response(html, {
      status: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=300, s-maxage=600, stale-while-revalidate=1800',
        'X-OGP-Source': 'middleware',
      },
    });
  } catch (e) {
    // エラー時はrewritesに任せる
    return undefined;
  }
}

function escapeHtml(s: string): string {
  return String(s || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
