// Vercel Edge Function: /api/journal-sitemap
// Supabase の journal_articles テーブルから live 記事を取得して動的に sitemap.xml を生成する
// vercel.json の rewrites で /journal/sitemap.xml -> /api/journal-sitemap に書き換え

export const config = { runtime: 'edge' };

const SUPABASE_URL = 'https://jakwntemjkwqwaqujffh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ';
const SITE = 'https://coworkmill.vercel.app';

const STATIC_URLS = [
  { loc: SITE + '/journal/', changefreq: 'daily', priority: '0.9' }
];

const CATEGORIES = ['interview', 'trend', 'news', 'other'];

function escXml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

function urlEntry(loc, lastmod, changefreq, priority) {
  let xml = '  <url>\n    <loc>' + escXml(loc) + '</loc>\n';
  if (lastmod) xml += '    <lastmod>' + escXml(lastmod) + '</lastmod>\n';
  if (changefreq) xml += '    <changefreq>' + changefreq + '</changefreq>\n';
  if (priority) xml += '    <priority>' + priority + '</priority>\n';
  xml += '  </url>\n';
  return xml;
}

export default async function handler() {
  let articles = [];
  try {
    const res = await fetch(
      SUPABASE_URL + '/rest/v1/journal_articles?status=eq.live&select=slug,published_at,updated_at&order=published_at.desc&limit=2000',
      { headers: { apikey: SUPABASE_KEY, Authorization: 'Bearer ' + SUPABASE_KEY } }
    );
    if (res.ok) {
      articles = await res.json();
    } else {
      console.warn('[journal-sitemap] Supabase fetch failed:', res.status);
    }
  } catch (e) {
    console.warn('[journal-sitemap] fetch error:', e && e.message);
  }

  let body = '<?xml version="1.0" encoding="UTF-8"?>\n';
  body += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';

  for (const u of STATIC_URLS) {
    body += urlEntry(u.loc, null, u.changefreq, u.priority);
  }
  for (const cat of CATEGORIES) {
    body += urlEntry(SITE + '/journal/?cat=' + cat, null, 'weekly', '0.7');
  }
  for (const a of articles) {
    if (!a || !a.slug) continue;
    const loc = SITE + '/journal/' + encodeURIComponent(a.slug);
    const lastmod = (a.updated_at || a.published_at || '').slice(0, 10);
    body += urlEntry(loc, lastmod, 'monthly', '0.8');
  }

  body += '</urlset>\n';

  return new Response(body, {
    status: 200,
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      // 1時間キャッシュ + stale-while-revalidate でほぼ常時 CDN ヒット
      'Cache-Control': 'public, max-age=3600, s-maxage=3600, stale-while-revalidate=86400'
    }
  });
}
