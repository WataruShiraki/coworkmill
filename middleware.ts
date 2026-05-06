// Vercel Edge Middleware: /admin と /ops 配下にベーシック認証を要求
//
// 目的: Stripe審査のセキュリティ要件「管理者画面のIPアドレス制限または
//       ベーシック認証」を満たすため。
//
// 認証情報は Vercel の環境変数で管理:
//   BASIC_AUTH_USER : ベーシック認証ユーザー名
//   BASIC_AUTH_PASS : ベーシック認証パスワード
//
// 認証成功 → そのまま通常の admin.html / ops.html を返す
// 認証失敗 → 401 + WWW-Authenticate ヘッダーでブラウザが認証ダイアログを表示

export const config = {
  // Vercel cleanUrls により /admin と /admin.html 両方が来る可能性があるため両方マッチ
  // /admin, /admin.html, /admin/...,  /admin-ops, /ops, /ops.html, /ops/... も含める
  matcher: [
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
  ],
};

export default function middleware(request: Request): Response | undefined {
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
