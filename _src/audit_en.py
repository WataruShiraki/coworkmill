# 英語版（インバウンド版）MILL の点検ツール（2026-10-11 COWORKMILL で作成。他のMILLにもそのまま使う）
# 使い方: python3 _src/audit_en.py <サイトのルート> [英語データの visit_extra.json]
#   例: cd coworkmill && python3 _src/audit_en.py . _src/en/visit_extra.json
# 見るもの: タイトル60字・説明160字・OGP/canonical の抜け・サイト内リンク切れ・検索に載る日本語ページ・データの空欄
import sys, os, re, glob, json, html, collections
root = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(root)
SKIP = ('_src', 'journal', 'preview', 'node_modules', '.git')
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(SKIP)]
P = collections.defaultdict(list)
T = collections.Counter(); D = collections.Counter()
def g(p, h):
    m = re.search(p, h, re.S | re.I); return html.unescape(m.group(1)) if m else None
redirected = set()
if os.path.exists('vercel.json'):
    for r in json.load(open('vercel.json')).get('redirects', []):
        redirected.add(r['source'].lstrip('/'))
    for hd in json.load(open('vercel.json')).get('headers', []):
        if any(x.get('key', '').lower() == 'x-robots-tag' and 'noindex' in x.get('value', '') for x in hd.get('headers', [])):
            src = hd['source'].lstrip('/')
            redirected.update(f for f in files if f == src or (src.endswith(':path*') and f.startswith(src.replace(':path*', ''))))
for f in files:
    h = open(f, encoding='utf-8', errors='ignore').read()
    lang = g(r'<html[^>]*lang="(\w+)"', h) or '?'
    noindex = 'noindex' in h
    if lang != 'en':
        if not noindex and f not in redirected and not f.startswith('google'):
            P['日本語などで検索に載るページ（転送かnoindexを）'].append(f)
        continue
    t = g(r'<title>(.*?)</title>', h); d = g(r'<meta name="description" content="(.*?)"', h)
    if not t: P['タイトルなし'].append(f)
    else:
        T[t] += 1
        if len(t) > 60: P['タイトル60字超'].append(f'{len(t)} {f}')
    if not d: P['説明文なし'].append(f)
    else:
        D[d] += 1
        if len(d) > 160: P['説明文160字超'].append(f'{len(d)} {f}')
    for k, pat in [('og:title', r'og:title" content="'), ('og:image', r'og:image" content="'), ('og:url', r'og:url" content="'), ('canonical', r'rel="canonical"'), ('twitter:card', r'twitter:card')]:
        if not re.search(pat, h) and not noindex: P[f'{k} なし'].append(f)
    for u in re.findall(r'href="(/[^"#?]*)', h):
        p = u.lstrip('/'); t2 = p + 'index.html' if (not p or p.endswith('/')) else p
        if not os.path.exists(t2) and not os.path.exists(p + '.html') and p not in redirected:
            P['サイト内リンク切れ'].append(f'{f} -> {u}')
P['同じタイトル'] = [t for t, c in T.items() if c > 1]
P['同じ説明文'] = [d[:60] for d, c in D.items() if c > 1]
print(f'英語ページ {sum(1 for f in files if "lang=\"en\"" in open(f, errors="ignore").read()[:400])} / HTML {len(files)}')
for k, v in P.items():
    print(('× ' if v else '○ ') + f'{k}: {len(v)}' + (f'  例: {v[:3]}' if v else ''))
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
    X = json.load(open(sys.argv[2]))
    print(f'予約・支払い・英語などの情報（visit_extra）: {len(X)} 件')
