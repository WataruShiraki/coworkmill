# ★2026-09-29 画像サイトマップ。build_mill.py の最後で実行される（単体でも OUT_DIR=<出力先>/ python3 imgsitemap.py で動く）。
# sitemap.xml の各ページの HTML から、施設の写真（<img class="ph">）と og:image を拾い、<image:image> を足す。
# ロゴ・バナー（/assets/ 以下）は入れない。1ページ最大20枚。
import os, re, html
OUT = os.environ.get('OUT_DIR', '')
def _run(out):
    sm = os.path.join(out, 'sitemap.xml')
    if not os.path.exists(sm): return
    s = open(sm, encoding='utf-8').read()
    if 'xmlns:image' in s: return
    locs = re.findall(r'<url><loc>([^<]+)</loc>(<lastmod>[^<]*</lastmod>)?</url>', s)
    rows = []; total = 0
    for loc, lm in locs:
        path = re.sub(r'^https?://[^/]+/?', '', loc)
        f = os.path.join(out, path)
        if path == '' or path.endswith('/'): f = os.path.join(f, 'index.html')
        imgs = []
        if os.path.exists(f):
            h = open(f, encoding='utf-8', errors='ignore').read()
            m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
            cand = ([m.group(1)] if m else []) + re.findall(r'<img[^>]*class="ph"[^>]*src="([^"]+)"', h) + re.findall(r'<img[^>]*src="([^"]+)"[^>]*class="ph"', h)
            for u in cand:
                u = html.unescape(u)
                if not u.startswith('http') or '/assets/' in u and loc.split('/')[2] in u: continue
                if u not in imgs: imgs.append(u)
            imgs = imgs[:20]
        total += len(imgs)
        esc = lambda x: x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        rows.append(f'<url><loc>{loc}</loc>{lm}' + ''.join(f'<image:image><image:loc>{esc(u)}</image:loc></image:image>' for u in imgs) + '</url>\n')
    out_s = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + ''.join(rows) + '</urlset>\n'
    open(sm, 'w', encoding='utf-8').write(out_s)
    print('imgsitemap:', len(locs), 'pages,', total, 'images')
_run(OUT)
