# COWORKMILL 英語版の生成器（2026-10-10）
# わたるさん「MILLをインバウンド・外国企業向けに全部切り替える」「全部英語」「基本は英語で表示、海外サイトっぽく」
# 形は承認済みの見本（preview/en-top.html・preview/en-toranomon-hills-arch.html）のとおり。
# 使い方: cd _src && OUT_DIR=/どこか/out/ BASE= python3 build_en.py
#   BASE='' で本番（/ 直下）、BASE='/preview/en' で非公開の確認用（noindex）
# データ: 日本語の施設データ（写真・住所・公式URL）＋ en/b*.json（英訳本文）＋ en/collections.json ＋ en/questions.json
import os, re, json, html, glob, shutil, datetime, collections
from urllib.parse import quote
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('OUT_DIR', '/tmp/claude-0/cw-en/')
BASE = os.environ.get('BASE', '')
PREVIEW = bool(BASE)
SITE = 'https://cowkml.com'
NAME = 'COWORKMILL'
TAG = "Japan's best-designed coworking spaces"
GA_ID = 'G-P6CZCM6K18'
ADS = 'ca-pub-1379037925480740'
E = lambda s: html.escape(str(s), quote=True)

# ---------- データ ----------
g = {'__file__': os.path.join(HERE, 'x')}
exec(open(os.path.join(HERE, 'cowork_facilities.py'), encoding='utf-8').read(), g)
g['A'] = sorted(g['A30'], key=lambda a: a.get('added', ''), reverse=True); g['A_by'] = {a['slug']: a for a in g['A']}
for f in ('seo_cowork.py', 'popular_cowork.py'):
    exec(open(os.path.join(HERE, f), encoding='utf-8').read(), g)
JA = g['A_by']; IMG = g['IMG30']; OFFICIAL = g['OFFICIAL30']; PLACE = g['PLACE']; POPULAR = g['POPULAR']
EN = {}
for f in sorted(glob.glob(os.path.join(HERE, 'en', 'b*.json'))):
    for d in json.load(open(f, encoding='utf-8')): EN[d['slug']] = d
ORDER = [a['slug'] for a in g['A'] if a['slug'] in EN]  # 新着順
COLS = json.load(open(os.path.join(HERE, 'en', 'collections.json'), encoding='utf-8'))
QS = json.load(open(os.path.join(HERE, 'en', 'questions.json'), encoding='utf-8'))
assert len(ORDER) == len(JA) == len(EN), (len(ORDER), len(JA), len(EN))

def photo(slug, n): return IMG.get(slug, {}).get(str(n))
def official(slug):
    if slug in OFFICIAL: return OFFICIAL[slug]
    for k, v in JA[slug]['credits']:
        if k == '出典URL': return v
    return ''
def jp_address(slug):
    p = PLACE.get(slug)
    if p and p.get('streetAddress'): return p['streetAddress']
    for k, v in JA[slug]['facts']:
        if k in ('場所', '住所'):
            v = re.sub(r'（.*?）$', '', v).strip()
            if re.match(r'(北海道|東京都|(?:京都|大阪)府|\S{2,3}県)', v): return v
    return ''
def town(e): return e['area'].split(',')[0].strip()
# 2026-10-10 わたるさん「英語表記もあった方よくね？」：英訳本文の「on the 5th floor of the ◯◯ Building」から建物と階を取り、街・県とあわせて英語の住所にする（番地のローマ字は推測になるので書かない）
_FLOOR = re.compile(r"on the ((?:\d+(?:st|nd|rd|th))|ground|basement|second basement) floors? (?:and [^ ]+ floors? )?of (?:the )?([A-Z0-9][^,;]*?)(?:,| in | near | directly | a | —|(?<!No)\.(?: |$))")
def en_address(e):
    m = _FLOOR.search(e['lead']); t = town(e); pr = pref(e)
    place = t if t == pr else f'{t}, {pr}'
    if not m: return f'{place}, Japan'
    fl = {'ground': 'Ground floor', 'basement': 'Basement', 'second basement': '2nd basement'}.get(m.group(1), m.group(1) + ' floor')
    return f'{m.group(2).strip()}, {fl}, {place}, Japan' 
def pref(e): return (e['area'].split(',')[1] if ',' in e['area'] else e['area']).strip()
def fact(e, *keys):
    for k, v in e['facts']:
        if k in keys: return v
    return ''

# 写真：表紙 → 各章の写真（重複なし・実在するものだけ）
def photos(slug):
    e = EN[slug]; ja = JA[slug]; out = []; seen = set()
    h = ja['hero'][0]
    if photo(slug, h): out.append((h, e['hero_cap'])); seen.add(h)
    for st in e['steps']:
        for n, c in st[3]:
            if n not in seen and photo(slug, n): out.append((n, c)); seen.add(n)
    return out

# 旅行者向けのしるし（公式情報から作った facts だけで判定。推測では付けない）
# 2026-10-10 わたるさん「支払い方法とか、英語対応可能かとかちゃんと入ってるか？」：公式サイトで確かめた予約・支払い・英語対応（en/visit_extra.json、人気の上位から順に追加）
VX = json.load(open(os.path.join(HERE, 'en', 'visit_extra.json'), encoding='utf-8'))
def traits(slug):
    e = EN[slug]; t = []; vx = VX.get(slug, {})
    txt = ' '.join(v for k, v in e['facts']).lower(); allf = json.dumps(e, ensure_ascii=False).lower()
    members_only = 'no drop-in' in txt or 'corporate membership only' in txt or 'members only' in txt or 'members only' in vx.get('Booking', '').lower() or 'membership only' in vx.get('Booking', '').lower()
    if not members_only and re.search(r'drop-in|per hour|/hour|an hour|per day|/day|a day', fact(e, 'Drop-in', 'Prices', 'Price').lower()): t.append('Day pass')
    h = fact(e, 'Hours', 'Access hours').lower(); c = fact(e, 'Closed').lower()
    if vx.get('day') and not members_only and 'Day pass' not in t: t.append('Day pass')
    if vx.get('English') and 'in Japanese' not in vx['English']: t.append('English website')
    if '24 hours' in h: t.append('24-hour access')
    h2 = re.sub(r'\([^)]*(member|support|tenant|office|reception)[^)]*\)', '', h); h2 = re.sub(r'/ *[^/]*(members|tenants|serviced offices|private rooms|offices)[^/]*', '', h2)
    _wk = re.search(r'weekend|sat|sun|every day|mon–sun|365 days|daily', h2) and not re.search(r'closed (on )?(weekends|saturdays|sundays|sat)', h) and not re.match(r'24 hours', h)
    if (_wk or re.match(r'(every day|daily)', h)) and 'weekend' not in c and 'saturday' not in c and 'sunday' not in c: t.append('Open weekends')
    if re.search(r'–(2[2-4]|0[0-5]):\d\d', h): t.append('Open late')
    if members_only: t.append('Members only')
    if 'linked to' in allf and 'station' in allf and ('directly linked' in fact(e, 'Access').lower() or 'directly linked' in e['lead'].lower()): t.append('Station-linked')
    return t
TRAIT = {s: traits(s) for s in ORDER}

# ---------- 共通部品 ----------
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter+Tight:wght@400;500;600;700&family=Zen+Kaku+Gothic+New:wght@500;700&display=swap">')
GA = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}",{{anonymize_ip:true}});</script>') if not PREVIEW else ''
def U(path): return BASE + '/' + path  # サイト内リンク

def head(title, desc, path, og=None, otype='website', ld=None):
    u = SITE + '/' + path.replace('index.html', '')
    og = og or SITE + '/assets/og.png'
    robots = 'noindex,nofollow' if PREVIEW else 'index,follow,max-image-preview:large'
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="{robots}"><title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            f'<link rel="canonical" href="{E(u)}"><meta property="og:url" content="{E(u)}"><meta property="og:site_name" content="{NAME}">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="{otype}">'
            f'<meta property="og:image" content="{E(og)}"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{E(og)}">'
            '<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">'
            '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#2F6A98">'
            f'<meta name="google-adsense-account" content="{ADS}">{FONTS}<link rel="stylesheet" href="{U("assets/en.css")}">{GA}{lds}</head><body>')

def nav(cur=''):
    items = [('spaces/', 'Spaces'), ('collections/', 'Collections'), ('questions/', 'Q&amp;A'), ('about/', 'About')]
    li = ''.join(f'<li><a href="{U(k)}"{" aria-current=\"page\"" if k.startswith(cur) and cur else ""}>{v}</a></li>' for k, v in items)
    return (f'<header class="wrap"><div class="nav"><a class="wm" href="{U("")}"><img src="/assets/logo.svg" alt="{NAME}" width="120" height="30"><small>{TAG.upper()}</small></a>'
            f'<ul>{li}</ul><div class="r"><a href="{U("contact/")}?topic=listing">List your space</a></div></div></header>')

def foot():
    return (f'<footer class="wrap"><nav><a href="{U("about/")}">About {NAME}</a><a href="{U("spaces/")}">All spaces</a><a href="{U("collections/")}">Collections</a><a href="{U("questions/")}">Q&amp;A</a>'
            f'<a href="{U("about/privacy.html")}">Privacy</a><a href="{U("about/terms.html")}">Terms</a><a href="{U("contact/")}">Contact</a></nav>'
            f'<p>© 2026 {NAME} — a guide to {TAG}. Facts and photos come from each space\'s official website; photos remain the property of their owners.</p></footer>'
            '<dialog id="lb"><img id="lbimg" alt=""><div class="bar"><span id="lbcap"></span><span><button type="button" id="lbprev" aria-label="Previous">‹</button> <button type="button" id="lbnext" aria-label="Next">›</button> <button type="button" id="lbclose">Close</button></span></div></dialog>'
            f'<script src="{U("assets/en.js")}" defer></script></body></html>')

def card(slug, i=None, sub=None):
    e = EN[slug]; ja = JA[slug]; img = photo(slug, ja['hero'][0])
    no = f'<span class="no">{i}</span>' if i else ''
    tr = ''.join(f'<span>{E(t)}</span>' for t in TRAIT[slug][:3])
    return (f'<a class="card" href="{U("spaces/" + slug + ".html")}" data-q="{E((e["name"] + " " + e["area"] + " " + e["card"]).lower())}" data-p="{E(pref(e))}" data-t="{E("|".join(TRAIT[slug]))}">'
            f'<div class="ph">{f"""<img src="{E(img)}" alt="{E(e["hero_cap"])}" loading="lazy">""" if img else ""}</div>'
            f'<div class="k">{E(e["area"])}</div><b>{no}{E(e["name"])}</b><p>{E(sub or e["card"])}</p>'
            + (f'<div class="chips">{tr}</div>' if tr else '') + '</a>')

# ---------- 施設ページ ----------
VISIT_KEYS = [('Who', ('Use', 'Format')), ('Price', ('Prices', 'Price', 'Drop-in', 'Monthly', 'Free desk', 'Entry fee')), ('Hours', ('Hours', 'Access hours')), ('Closed', ('Closed',)), ('Train', ('Access',))]
def space_page(slug):
    e = EN[slug]; ja = JA[slug]; off = official(slug); adr = jp_address(slug); ph = photos(slug)
    P = [[photo(slug, n), c] for n, c in ph]
    idx = {n: i for i, (n, c) in enumerate(ph)}
    nm = f'<a href="{E(off)}" target="_blank" rel="noopener">{E(e["name"])}</a>' if off else E(e['name'])
    tail = e['title'].split(' — ', 1)[1] if ' — ' in e['title'] else e['card']
    # 写真の並び（見本：大1＋小4、押すと全部）
    gal = ''
    if P:
        pick = list(range(min(5, len(P))))
        gal = '<div class="gal' + (' n' + str(len(pick)) if len(pick) < 5 else '') + '">' + ''.join(
            f'<figure data-i="{i}"><img src="{E(P[i][0])}" alt="{E(P[i][1])}"{" loading=\"lazy\"" if i else ""}></figure>' for i in pick)
        if len(P) > 1: gal += f'<button type="button" class="all" data-i="0">View all {len(P)} photos</button>'
        gal += '</div>'
        _ph = next((v for k, v in e['credits'] if k == 'Photos'), '')
        gal += f'<p class="cap">{len(P)} photo{"s" if len(P) > 1 else ""}{(" · " + E(_ph)) if _ph else ""} · Tap any photo to view it full size</p>'
    _vk = {k for _, ks in VISIT_KEYS for k in ks}  # 2026-10-10 Plan your visit と同じ項目は下に繰り返さない
    facts = ''.join(f'<span>{E(k)}<b>{E(v)}</b></span>' for k, v in e['facts'] if k not in ('Space',) and k not in _vk)
    body = f'<section class="step"><p class="no">Introduction</p><h2>{E(e["concept"][0])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in e['concept'][1]) + '</section>'
    for st in e['steps']:
        figs = [(idx[n], c) for n, c in st[3] if n in idx and n != ja['hero'][0]]
        fh = ''
        if figs:
            fh = f'<div class="pair{" one" if len(figs) == 1 else ""}">' + ''.join(f'<figure data-i="{i}"><img src="{E(P[i][0])}" alt="{E(c)}" loading="lazy"><figcaption>{E(c)}</figcaption></figure>' for i, c in figs[:4]) + '</div>'
        body += f'<section class="step"><p class="no">{E(st[0])}</p><h2>{E(st[1])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in st[2]) + fh + '</section>'
    w = e['word']
    body += f'<div class="word"><p><b>{E(w["title"])}</b></p>' + ''.join(f'<p>{E(x)}</p>' for x in w['body']) + '</div>'
    cred = ''.join(f'<div><b>{E(k)}</b>{(f"""<a href="{E(off)}" target="_blank" rel="noopener">{E(v)}</a>""" if k == "Operator" and off else E(v))}</div>' for k, v in e['credits'])
    # Plan your visit
    rows = ''
    used = set()
    for lab, keys in VISIT_KEYS:
        for k, v in e['facts']:
            if k in keys and (k, v) not in used:
                used.add((k, v))
                if lab == 'Train':
                    li = ''.join(f'<li>{E(x.strip())}</li>' for x in v.split(' / '))
                    rows += f'<div class="row"><span>{lab}</span><ul>{li}</ul></div>'
                else:
                    rows += f'<div class="row"><span>{lab}</span><div>{E(v)}</div></div>'
    if 'Members only' in TRAIT[slug] and not any(k in ('Use',) for k, v in e['facts']):
        rows = f'<div class="row"><span>Who</span><div>Members only — not a drop-in space.</div></div>' + rows
    vx = VX.get(slug, {})
    if vx.get('Who') and 'Who</span>' not in rows:
        rows = f'<div class="row"><span>Who</span><div>{E(vx["Who"])}</div></div>' + rows
    if not any(k in ('Prices', 'Price', 'Drop-in', 'Monthly', 'Free desk', 'Entry fee') for k, v in e['facts']):
        pr = (f'<div class="row"><span>Price</span><div>{E(vx["Price"])}</div></div>' if vx.get('Price') else
              '<div class="row"><span>Price</span><div>Not published here <small>— check the official website</small></div></div>')
        i = rows.find('</div></div>') + 12 if rows.startswith('<div class="row"><span>Who</span>') else 0
        rows = rows[:i] + pr + rows[i:]
    _pt = ' '.join(v for k, v in e['facts'] if k in ('Prices', 'Price', 'Drop-in', 'Monthly', 'Free desk', 'Entry fee')).lower()
    if vx.get('Price') and _pt and not re.search(r'drop-in|one-time|/hour|per hour|/day|per day|half day', _pt):
        _r = f'<div class="row"><span>Price</span><div>{E(vx["Price"])}</div></div>'
        _i = rows.find('<div class="row"><span>Price</span>')
        _i = rows.find('</div></div>', _i) + 12 if _i >= 0 else len(rows)
        rows = rows[:_i] + _r + rows[_i:]
    for lab in ('Booking', 'Payment', 'English'):
        if vx.get(lab):
            rows += f'<div class="row"><span>{"How" if lab == "Booking" else "Pay" if lab == "Payment" else lab}</span><div>{E(vx[lab])}</div></div>'
    if vx:
        rows += '<p class="chk">Checked on the official website, October 2026</p>'
    taxi = ''
    if adr:
        taxi = (f'<div class="taxi"><p>Show this to your taxi driver</p><div class="ja" lang="ja">{E(adr)}<br>{E(ja["company"])}</div><div class="en">{E(en_address(e))}</div>'
                f'<div class="tb"><button type="button" class="cp" data-t="{E(adr + " " + ja["company"])}">Copy address</button>'
                f'<a href="https://www.google.com/maps/search/?api=1&amp;query={quote(adr + " " + ja["company"])}" target="_blank" rel="noopener">Open in Google Maps</a></div></div>')
    cta = f'<a class="cta" href="{E(off)}" target="_blank" rel="noopener">Visit the official website<small>Booking and contact are on the operator\'s site, often in Japanese</small></a>' if off else ''
    visit = f'<aside class="visit"><h3>Plan your visit</h3>{rows}{taxi}{cta}</aside>'
    # 構造化データ
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": e['title'][:110], "inLanguage": "en", "image": P[0][0] if P else None,
           "author": {"@type": "Organization", "name": NAME}, "publisher": {"@type": "Organization", "name": NAME}, "mainEntityOfPage": SITE + '/spaces/' + slug + '.html'},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": NAME, "item": SITE + '/'},
              {"@type": "ListItem", "position": 2, "name": "Spaces", "item": SITE + '/spaces/'},
              {"@type": "ListItem", "position": 3, "name": e['name'], "item": SITE + '/spaces/' + slug + '.html'}]}]
    pl = PLACE.get(slug)
    if pl:
        lb = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": e['name'], "url": off or None, "image": P[0][0] if P else None, "description": e['card'],
              "address": {"@type": "PostalAddress", "streetAddress": pl['streetAddress'], "addressLocality": pl.get('addressLocality'), "addressRegion": pl.get('addressRegion'), "addressCountry": "JP"}}
        ld.append({k: v for k, v in lb.items() if v})
    rel = [s for s in ORDER if s != slug and pref(EN[s]) == pref(e) and town(EN[s]) == town(e)][:4]
    rel += [s for s in POPULAR if s != slug and s not in rel and s in EN and pref(EN[s]) == pref(e)][:4 - len(rel)]
    relh = f'<section class="sec"><div class="sh"><div><h2>More spaces nearby</h2><p>{E(town(e))} and around</p></div><a href="{U("spaces/")}?q={quote(town(e).lower())}">See all in {E(town(e))} →</a></div><div class="cards">' + ''.join(card(s) for s in rel) + '</div></section>' if rel else ''
    title = f'{e["name"]}, {town(e)} — photos and how to visit | {NAME}'
    desc = (e['card'] + '. ' + e['lead'])[:155].rsplit(' ', 1)[0] + '…'
    return (head(title, desc, f'spaces/{slug}.html', P[0][0] if P else None, 'article', ld) + nav('spaces/') +
            f'<main class="wrap"><div class="crumb"><a href="{U("spaces/")}">Spaces</a> › {E(e["area"])} › {E(e["name"])}</div>'
            f'<div class="head"><p class="tag">{E(e["area"])}</p><h1>{nm} — {E(tail)}</h1><p class="lead">{E(e["lead"])}</p></div>'
            f'{gal}<div class="grid"><article>{("<div class=facts>" + facts + "</div>") if facts else ""}{body}<div class="cred">{cred}</div></article>{visit}</div>{relh}</main>'
            f'<script type="application/json" id="photos">{json.dumps(P, ensure_ascii=False)}</script>' + foot())

# ---------- 一覧 ----------
def prefs_count(slugs):
    c = collections.Counter(pref(EN[s]) for s in slugs)
    return sorted(c.items(), key=lambda kv: (kv[0] != 'Tokyo', -kv[1], kv[0]))
TFILTERS = ['Day pass', 'Open weekends', 'Open late', '24-hour access', 'Station-linked', 'English website']
def list_page():
    pc = prefs_count(ORDER)
    chips = f'<button type="button" data-p="" class="on">All<small>{len(ORDER)}</small></button>' + ''.join(f'<button type="button" data-p="{E(k)}">{E(k)}<small>{n}</small></button>' for k, n in pc)
    tf = ''.join(f'<button type="button" data-t="{E(t)}" aria-pressed="false">{E(t)}<small>{sum(1 for s in ORDER if t in TRAIT[s])}</small></button>' for t in TFILTERS)
    cards = ''.join(card(s) for s in ORDER)
    title = f'All {len(ORDER)} coworking spaces in Japan — by area | {NAME}'
    desc = f'Browse {len(ORDER)} of Japan\'s best-designed coworking spaces by prefecture and area, with day-pass, weekend and late-opening filters. Facts from each official website.'
    return (head(title, desc, 'spaces/index.html') + nav('spaces/') +
            f'<main class="wrap"><div class="head"><p class="tag">Spaces</p><h1>All {len(ORDER)} spaces</h1><p class="lead">Every space here was chosen for its interior. Filter by area, or by what matters on a short trip: a day pass, weekend hours, late opening.</p></div>'
            f'<div class="fbar"><form class="search" id="fs" role="search"><input type="search" id="fq" placeholder="Area, station or name — e.g. Shibuya" aria-label="Search spaces"><button type="submit">Search</button></form>'
            f'<div class="fchips" id="fp" role="group" aria-label="Prefecture">{chips}</div><div class="fchips tf" id="ft" role="group" aria-label="For travellers">{tf}</div>'
            f'<p class="fcount" id="fc">{len(ORDER)} spaces</p></div><div class="cards" id="list">{cards}</div><p class="fnone" id="fn" hidden>No spaces match. Try another area or clear a filter.</p></main>' + foot())

# ---------- TOP ----------
def top_page():
    hero_slug = next(s for s in POPULAR if s in EN and photo(s, JA[s]['hero'][0]))
    he = EN[hero_slug]; himg = photo(hero_slug, JA[hero_slug]['hero'][0])
    _hc = next((v for k, v in he['credits'] if k == 'Photos'), '')
    tc = collections.Counter(town(EN[s]) for s in ORDER if pref(EN[s]) == 'Tokyo')
    areas = ''.join(f'<a href="{U("spaces/")}?q={quote(t.lower())}">{E(t)}<span>{n}</span></a>' for t, n in tc.most_common(10))
    areas += ''.join(f'<a href="{U("spaces/")}?pref={quote(k)}">{E(k)}<span>{n}</span></a>' for k, n in prefs_count(ORDER) if k != 'Tokyo' and n >= 3)
    pop = [s for s in POPULAR if s in EN][:8]
    trav = [s for s in POPULAR if s in EN and 'Day pass' in TRAIT[s] and photo(s, JA[s]['hero'][0])][:4]
    tf = ''.join(f'<a href="{U("spaces/")}?t={quote(t)}">{E(t)}<small>{sum(1 for s in ORDER if t in TRAIT[s])}</small></a>' for t in TFILTERS)
    cols = ''.join(f'<a class="col" href="{U("collections/" + c["slug"] + ".html")}"><span class="n">{len(c["items"])}</span><b>{E(c["title"])}</b><p>{E(c["lead"])}</p></a>' for c in COLS[:6])
    title = f'{NAME} — {TAG}, in English'
    desc = f'{len(ORDER)} coworking spaces in Tokyo and across Japan, chosen for their interiors — with prices, hours, day passes and the Japanese address for your taxi. Every fact from the official website.'
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + '/', "inLanguage": "en",
           "potentialAction": {"@type": "SearchAction", "target": SITE + '/spaces/?q={q}', "query-input": "required name=q"}}]
    return (head(title, desc, 'index.html', himg, 'website', ld) + nav() +
            f'<main class="wrap"><div class="hero"><img src="{E(himg)}" alt="{E(he["hero_cap"])}"><span class="credit">{E(_hc)}</span><div class="in">'
            f'<h1>Japan\'s best-designed places to work</h1><p>{len(ORDER)} coworking spaces chosen for their interiors, from Shibuya hotel lounges to Marunouchi towers. Every fact comes from the space\'s official website.</p>'
            f'<form class="search" action="{U("spaces/")}" method="get" role="search"><input type="search" name="q" placeholder="Area, station or name — e.g. Shibuya" aria-label="Search coworking spaces"><button type="submit">Search</button></form></div></div>'
            f'<div class="areas" aria-label="Popular areas">{areas}</div>'
            f'<section class="sec"><div class="trav"><div><h3>In Japan for a few days?</h3><p>Find spaces you can use on the day. These labels come only from what each official website says.</p><div class="fl">{tf}</div></div>'
            f'<div class="tcards">' + ''.join(card(s) for s in trav[:2]) + '</div></div></section>'
            f'<section class="sec"><div class="sh"><div><h2>Popular spaces</h2><p>Most read this month</p></div><a href="{U("spaces/")}">All {len(ORDER)} spaces →</a></div><div class="cards">' + ''.join(card(s, i + 1) for i, s in enumerate(pop)) + '</div></section>'
            f'<section class="sec"><div class="sh"><div><h2>Collections</h2><p>Spaces grouped by area and theme</p></div><a href="{U("collections/")}">All {len(COLS)} collections →</a></div><div class="cols">{cols}</div></section>'
            f'<section class="sec"><div class="sh"><div><h2>New on {NAME}</h2><p>The latest spaces we have added</p></div><a href="{U("spaces/")}">See all →</a></div><div class="cards">' + ''.join(card(s) for s in ORDER[:8]) + '</div></section>'
            '<section class="sec"><div class="sh"><div><h2>How to read this site</h2><p>Three things we do on every page</p></div></div><div class="how">'
            '<div><b>Prices in yen, from the source</b><p>We list only the prices each space publishes. If a price is not public, we say so instead of guessing.</p></div>'
            '<div><b>Address in Japanese, too</b><p>Each page shows the address in Japanese — e.g. <span class="ja" lang="ja">東京都渋谷区渋谷3-27-1</span> — with a copy button and a Google Maps link for taxis.</p></div>'
            '<div><b>“Japanese only” when it matters</b><p>Booking forms and official websites are often only in Japanese. We tell you before you click.</p></div></div></section>'
            '</main>' + foot())

# ---------- 特集 ----------
def col_index():
    cols = ''.join(f'<a class="col" href="{U("collections/" + c["slug"] + ".html")}"><span class="n">{len(c["items"])}</span><b>{E(c["title"])}</b><p>{E(c["lead"])}</p></a>' for c in COLS)
    return (head(f'Collections — coworking in Japan by area and theme | {NAME}', f'{len(COLS)} collections of Japan\'s best-designed coworking spaces, grouped by area (Shibuya, Marunouchi, Shinjuku…) and theme (24 hours, hotels, rooftops…).', 'collections/index.html') + nav('collections/') +
            f'<main class="wrap"><div class="head"><p class="tag">Collections</p><h1>{len(COLS)} collections</h1><p class="lead">Spaces grouped by neighbourhood and by theme, so you can compare places that share something.</p></div><div class="cols">{cols}</div></main>' + foot())
def col_page(c):
    items = [(s, cap) for s, cap in c['items'] if s in EN]
    _i = COLS.index(c); _o = (COLS[_i + 1:] + COLS[:_i])[:3]
    others = ''.join(f'<a class="col" href="{U("collections/" + o["slug"] + ".html")}"><span class="n">{len(o["items"])}</span><b>{E(o["title"])}</b><p>{E(o["lead"])}</p></a>' for o in _o)
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "name": c['title'], "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + '/spaces/' + s + '.html', "name": EN[s]['name']} for i, (s, _) in enumerate(items)]}]
    img = photo(items[0][0], JA[items[0][0]]['hero'][0]) if items else None
    return (head(f'{c["title"]} — {len(items)} spaces | {NAME}', c['lead'][:155], f'collections/{c["slug"]}.html', img, 'article', ld) + nav('collections/') +
            f'<main class="wrap"><div class="crumb"><a href="{U("collections/")}">Collections</a> › {E(c["title"])}</div><div class="head"><p class="tag">{len(items)} spaces</p><h1>{E(c["title"])}</h1><p class="lead">{E(c["lead"])}</p></div>'
            '<div class="cards">' + ''.join(card(s, i + 1, cap) for i, (s, cap) in enumerate(items)) + '</div>'
            f'<section class="sec"><div class="sh"><div><h2>More collections</h2></div><a href="{U("collections/")}">All {len(COLS)} →</a></div><div class="cols">{others}</div></section></main>' + foot())

# ---------- Q&A ----------
def q_index():
    li = ''.join(f'<a class="qa" href="{U("questions/" + q["slug"] + ".html")}"><b>{E(q["q"])}</b><p>{E(q["a"])}</p></a>' for q in QS)
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in QS]}]
    return (head(f'Coworking in Japan: questions and answers | {NAME}', 'Short answers to common questions about coworking in Japan — drop-in, 24-hour access, prices, hotels, private rooms — from official information.', 'questions/index.html', None, 'website', ld) + nav('questions/') +
            f'<main class="wrap"><div class="head"><p class="tag">Q&amp;A</p><h1>Coworking in Japan, answered</h1><p class="lead">Short answers to the questions people ask most. Every answer is written from the official information of the spaces we list.</p></div><div class="qas">{li}</div></main>' + foot())
def q_page(q):
    body = ''
    for s, h, ps, phs in q['secs']:
        e = EN.get(s); figs = ''.join(f'<figure><img src="{E(photo(a, n))}" alt="{E(h)}" loading="lazy"></figure>' for a, n in phs if photo(a, n))
        body += (f'<section class="step"><p class="no"><a href="{U("spaces/" + s + ".html")}">{E(e["name"] if e else s)} →</a></p><h2>{E(h)}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in ps)
                 + (f'<div class="pair{" one" if figs.count("<figure") == 1 else ""}">{figs}</div>' if figs else '') + '</section>')
    if q.get('ctx'):
        body += f'<div class="word"><p><b>{E(q["ctx"]["title"])}</b></p>' + ''.join(f'<p>{E(x)}</p>' for x in q['ctx']['body']) + '</div>'
    others = ''.join(f'<a class="qa" href="{U("questions/" + o["slug"] + ".html")}"><b>{E(o["q"])}</b></a>' for o in QS if o is not q)[:]
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}}]}]
    return (head(f'{q["q"]} | {NAME}', q['desc'][:155], f'questions/{q["slug"]}.html', None, 'article', ld) + nav('questions/') +
            f'<main class="wrap"><div class="crumb"><a href="{U("questions/")}">Q&amp;A</a></div><div class="head"><p class="tag">Q&amp;A</p><h1>{E(q["q"])}</h1><p class="lead answer">{E(q["a"])}</p></div>'
            f'<div class="narrow">{body}</div><section class="sec"><div class="sh"><div><h2>Other questions</h2></div></div><div class="qas small">{others}</div></section></main>' + foot())

# ---------- About・規約・問い合わせ ----------
UPD = '10 October 2026'
def simple(path, title, desc, h1, inner, cur='about/'):
    return head(f'{title} | {NAME}', desc, path) + nav(cur) + f'<main class="wrap"><div class="page"><h1>{h1}</h1>{inner}</div></main>' + foot()
ABOUT = f'''<p class="lead">{NAME} is a guide to {TAG}, written in English for visitors, business travellers and companies coming to Japan.</p>
<h2>What we do</h2><p>We choose coworking spaces for the quality of their interiors and walk you through each one in the order a first-time visitor would see it: the entrance, the open seats, the meeting rooms, the lounge. Today we list {len(ORDER)} spaces in Tokyo and across Japan.</p>
<h2>Where the facts come from</h2><p>Every fact — prices, hours, seat counts, access — comes from the space's own official website or press materials, and each page names its sources. If something is not published, we say so rather than guess. Photos are the official images of each space, credited on every page.</p>
<h2>Made for visitors</h2><p>Each page shows the address in Japanese with a copy button and a Google Maps link, so you can show it to a taxi driver. We point out when a booking form or website is only in Japanese, and we explain Japanese terms such as <i>dejima</i> or <i>koagari</i> in plain English.</p>
<h2 id="ops">Who runs this site</h2><table class="ops"><tr><th>Site</th><td>{NAME} (cowkml.com)</td></tr><tr><th>Operator</th><td>The {NAME} team</td></tr><tr><th>Contact</th><td><a href="{U("contact/")}">Contact form</a></td></tr></table>
<h2 id="ads">Advertising</h2><p>This site may show advertising such as Google AdSense. Advertisers have no influence on which spaces we list or in what order.</p>
<h2 id="fix">Corrections</h2><p>If you find a mistake, please tell us through the <a href="{U("contact/")}">contact form</a> and we will fix it promptly. Operators are welcome to send updated information.</p>'''
PRIVACY = f'''<p class="upd">Last updated: {UPD}</p><p>This policy explains how {NAME} (“we”) handles personal information on cowkml.com.</p>
<h2>1. What we collect</h2><p><b>Information you send us.</b> Through the contact form we receive your topic, name, email address, company (optional) and message.</p><p><b>Technical information.</b> Like most websites, our hosting provider automatically records information such as IP address, browser type, pages viewed and time of access to keep the site secure.</p><p><b>Analytics and cookies.</b> We use Google Analytics (Google LLC) to understand how the site is used. It uses cookies to collect information such as pages viewed and time spent, in a form that does not identify you, and IP addresses are anonymised. See <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses this information</a>; you can opt out with your browser settings or the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">opt-out add-on</a>. If we show advertising such as Google AdSense, Google and its partners may use cookies to show ads based on your visits to this and other sites. You can manage this in <a href="https://adssettings.google.com/" target="_blank" rel="noopener">Google's Ad Settings</a>.</p>
<h2>2. How we use it</h2><ul><li>To reply to your enquiry</li><li>To run, secure and improve the site</li><li>To meet legal obligations</li></ul><p>We never sell personal information. We will ask for your consent before using it for any other purpose.</p>
<h2>3. Services we use</h2><p>We use the following providers; information may be processed outside Japan.</p><ul><li><b>Vercel</b> — hosting</li><li><b>Google Fonts</b> — typefaces</li><li><b>Google Analytics</b> — analytics</li><li><b>FormSubmit</b> — delivery of contact-form messages</li></ul>
<h2>4. How long we keep it</h2><p>We keep enquiries only as long as needed to respond and keep records, then delete them.</p>
<h2>5. Your rights</h2><p>To ask us to disclose, correct, delete or stop using personal information you have sent us, please use the <a href="{U("contact/")}">contact form</a>. We will respond within a reasonable time in line with Japan's Act on the Protection of Personal Information.</p>
<h2>6. Changes</h2><p>We may update this policy. The latest version, with its date, is always on this page.</p>'''
TERMS = f'''<p class="upd">Last updated: {UPD}</p><p>These terms apply to your use of cowkml.com, run by {NAME}. By using the site you agree to them.</p>
<h2>1. Content</h2><p>Our pages are written by the {NAME} team from the information each space publishes on its official website and in its news. We try hard to be accurate, but prices, hours and services change, so please check the official website before you go. Content is provided as is.</p>
<h2>2. Intellectual property</h2><p>Text, layout and logos belong to {NAME}. Photos belong to the spaces, designers and photographers credited on each page and are used with their sources stated. Please do not copy, republish or use them commercially without permission. Short quotations with a link to the original page are welcome.</p>
<h2>3. Requests from listed spaces</h2><p>If a listed space or rights holder asks us to correct or remove a photo or page, we will act promptly. Please use the <a href="{U("contact/")}">contact form</a>.</p>
<h2>4. Prohibited use</h2><ul><li>Anything that breaks the law or infringes others' rights</li><li>Automated mass access or anything that disrupts the site</li><li>Sending false, abusive or harmful content through the contact form</li><li>Misrepresenting a relationship with {NAME} or a listed space</li></ul>
<h2>5. Links and liability</h2><p>We are not responsible for the content of external sites we link to. To the extent permitted by law, we are not liable for loss arising from use of the site or its content.</p>
<h2>6. Governing law</h2><p>These terms are governed by Japanese law. The Tokyo District Court has exclusive jurisdiction in the first instance.</p>'''
FORM = 'https://formsubmit.co/d649df9aee3824d19c00adf93c140681'
CONTACT = f'''<p class="lead">Questions about a listing, corrections, partnerships or press — we reply within a week. You can write in English or Japanese.</p>
<form class="cform" action="{FORM}" method="POST"><label>Topic<select name="topic" id="topic" required><option value="listing">List my coworking space</option><option value="content">A correction or update to a page</option><option value="partner">Partnership or advertising</option><option value="media">Press</option><option value="other">Something else</option></select></label>
<div class="row2"><label>Name<input name="name" autocomplete="name" required></label><label>Email<input type="email" name="email" autocomplete="email" required></label></div>
<label>Company <small>(optional)</small><input name="company" autocomplete="organization"></label>
<div class="lst" id="listing-note" hidden><p><b>To have your space listed, please include:</b></p><ol><li>The operating company and the location of the space</li><li>Photos (a shared folder link, or the official page where the photos appear)</li><li>Links to information about the space (press releases, the designer's page)</li></ol><p>We use only official photos and information, with sources stated, and will reply about whether we can list it.</p></div>
<label>Message<textarea name="message" rows="7" required></textarea></label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="_next" value="{SITE}/contact/thanks.html"><input type="hidden" name="_subject" value="COWORKMILL contact (EN)"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table">
<p class="note">By sending, you agree to our <a href="{U("about/privacy.html")}">privacy policy</a>.</p><button type="submit">Send →</button></form>
<script>(function(){{var s=document.getElementById('topic'),n=document.getElementById('listing-note');function u(){{n.hidden=s.value!=='listing'}}try{{var t=new URLSearchParams(location.search).get('topic');if(t)s.value=t}}catch(e){{}}s.addEventListener('change',u);u()}})();</script>'''

# ---------- CSS / JS ----------
CSS = open(os.path.join(HERE, 'en', 'en.css'), encoding='utf-8').read()
JS = open(os.path.join(HERE, 'en', 'en.js'), encoding='utf-8').read()

# ---------- 書き出し ----------
def om_banner(where):
    return (f'<a class="omb" href="https://offml.com/?utm_source=coworkmill&amp;utm_medium=banner&amp;utm_campaign={where}" rel="noopener">'
            f'<img src="{U("assets/banner/officemill_728x90_en.webp")}" width="728" height="90" alt="OFFICEMILL — explore offices across Japan" loading="lazy"></a>')
def w(path, s):
    if path not in ('404.html', 'contact/thanks.html') and '</main>' in s:
        where = path.split('/')[0].replace('.html', '') or 'top'
        i = s.rfind('</main>'); s = s[:i] + om_banner(where) + s[i:]
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
w('assets/en.css', CSS); w('assets/en.js', JS)
w('index.html', top_page())
w('spaces/index.html', list_page())
for s in ORDER: w(f'spaces/{s}.html', space_page(s))
w('collections/index.html', col_index())
for c in COLS: w(f'collections/{c["slug"]}.html', col_page(c))
w('questions/index.html', q_index())
for q in QS: w(f'questions/{q["slug"]}.html', q_page(q))
w('about/index.html', simple('about/index.html', f'About {NAME}', f'About {NAME}, a guide to {TAG} in English, and who runs it.', f'About {NAME}', ABOUT))
w('about/privacy.html', simple('about/privacy.html', 'Privacy policy', f'How {NAME} handles personal information.', 'Privacy policy', PRIVACY))
w('about/terms.html', simple('about/terms.html', 'Terms of use', f'Terms of use for {NAME}.', 'Terms of use', TERMS))
w('contact/index.html', simple('contact/index.html', 'Contact', f'Contact the {NAME} team about listings, corrections or partnerships.', 'Contact us', CONTACT, 'contact/'))
w('contact/thanks.html', simple('contact/thanks.html', 'Message sent', 'Your message has been sent.', 'Thank you', f'<p class="lead">We have received your message and will reply within a week.</p><p><a href="{U("")}">Back to the home page →</a></p>', 'contact/'))
w('404.html', simple('404.html', 'Page not found', 'This page could not be found.', 'Page not found', f'<p class="lead">This page may have moved. Try the list of all spaces or search by area.</p><p><a href="{U("spaces/")}">See all {len(ORDER)} spaces →</a></p>', ''))
if not PREVIEW:
    today = datetime.date.today().isoformat()
    paths = [''] + ['spaces/'] + [f'spaces/{s}.html' for s in ORDER] + ['collections/'] + [f'collections/{c["slug"]}.html' for c in COLS] + ['questions/'] + [f'questions/{q["slug"]}.html' for q in QS] + ['about/', 'about/privacy.html', 'about/terms.html', 'contact/']
    imgs = {f'spaces/{s}.html': [p for p, c in [[photo(s, n), c] for n, c in photos(s)]][:10] for s in ORDER}
    sm = ''.join(f'<url><loc>{SITE}/{p}</loc><lastmod>{today}</lastmod>' + ''.join(f'<image:image><image:loc>{E(i)}</image:loc></image:image>' for i in imgs.get(p, [])) + '</url>\n' for p in paths)
    w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + sm + '</urlset>\n')
    w('site.webmanifest', json.dumps({"name": f"{NAME} — {TAG}", "short_name": NAME, "description": f"{TAG}, in English", "start_url": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#2F6A98", "lang": "en",
                                      "icons": [{"src": "/favicon-192x192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/favicon-512x512.png", "sizes": "512x512", "type": "image/png"}]}))
    w('llms.txt', f'# {NAME}\n\n> {TAG}, in English: {len(ORDER)} coworking spaces in Tokyo and across Japan chosen for their interiors, with prices, hours and access from each official website.\n\n## Pages\n' + ''.join(f'- [{EN[s]["name"]}]({SITE}/spaces/{s}.html): {EN[s]["card"]}\n' for s in ORDER))
print('ok', len(ORDER), 'spaces', len(COLS), 'collections', len(QS), 'questions', '->', OUT)
