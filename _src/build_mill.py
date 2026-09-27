# COWORKMILL / CAFEMILL のビルド（2026-09-26）
# OFFISNAP の _src/build_site.py をそのまま読み込み、ブランドに関わる部分だけ差し替えて実行する。
# 使い方: BRAND=cowork OUT_DIR=<出力先>/ python3 build_mill.py   /  BRAND=cafe OUT_DIR=<出力先>/ python3 build_mill.py
# 依存（OFFISNAP の build_site.py と WALL の style.css / index.html）は _src/deps/ に写しがあるので、このリポジトリだけで動く
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
OFF = os.environ.get('OFF_SRC', os.path.join(HERE, 'deps', 'off'))  # OFFISNAP の build_site.py の写し（deps/README.md）
os.environ.setdefault('WALL_DIR', os.path.join(HERE, 'deps', 'wall') + os.sep)  # WALL の style.css / index.html の写し
exec(open(os.path.join(HERE, 'brands.py'), encoding='utf-8').read())
B = BRANDS[os.environ['BRAND']]
os.environ['OUT_DIR'] = os.environ.get('OUT_DIR', f'/mnt/user-data/outputs/{B["utm"]}-site/')
sys.path.insert(0, OFF); os.chdir(OFF)  # banner/ や WALL の style.css を OFFISNAP と同じ相対パスで読むため

src = open('build_site.py', encoding='utf-8').read()
L = src.split('\n')
def find(prefix):
    for i, l in enumerate(L):
        if l.startswith(prefix): return i
    raise KeyError(prefix)

# 1) 記事の読み込み（写真のURL表・articles20/30・写真の差し替え）を、施設データ1本に置き換える
i0 = find('def load(name):'); i1 = find('# ---- ロゴ ----')
loader = f'''
exec(open({json.dumps(os.path.join(HERE, B["facilities"]))}, encoding='utf-8').read())
A = sorted(A30, key=lambda a: a.get('added', ''), reverse=True)  # 2026-09-27 新着順＝掲載日の新しい順（後から足した施設が下に入っていた）
IMG20 = dict(IMG30); KANA20 = dict(KANA30); COUNTRY20 = dict(COUNTRY30); ED = dict(ED30); ED20 = {{}}
exec(open({json.dumps(os.path.join(HERE, "collections_" + os.environ["BRAND"] + ".py"))}, encoding='utf-8').read())
A_by = {{a['slug']: a for a in A}}
for _a in A:
    _h = _a['hero'][0]
    _a['steps'] = [st[:3] + ([(n, c) for n, c in st[3] if n != _h],) for st in _a['steps']]
SEC_NAME = {json.dumps(B["sec"])}; KIND_WORD = {json.dumps(B["kind"])}; SITE_NAME = {json.dumps(B["name"])}; UTM = {json.dumps(B["utm"])}
QA_TITLE = {json.dumps(B["subj"] + "の Q&A")}
QA_LEAD = {json.dumps("日本の" + B["subj"] + "について、よく聞かれる質問に短く答えます。答えはすべて、掲載している" + B["kind"] + "の公式情報から書いています。")}
_qp = {json.dumps(os.path.join(HERE, "questions_" + os.environ["BRAND"] + ".py"))}
if os.path.exists(_qp): exec(open(_qp, encoding='utf-8').read())
def url(slug, n): return IMG30.get(slug, {{}}).get(str(n))
def purl(a, n): return url(a['slug'], n)
'''
L[i0:i1] = loader.split('\n')

# 2) ロゴ：実物の SVG を使う（白版は塗りを白に）
i0 = find('def logo_svg('); i1 = find("open(OUT + 'assets/logo-white.svg'") + 1
logo_code = f'''
_LOGO = open({json.dumps(B["logo"])}, encoding='utf-8').read()
_LOGO = re.sub(r'<\\?xml[^>]*>\\s*', '', _LOGO).replace('<!-- Generator: Adobe Illustrator 30.2.1, SVG Export Plug-In . SVG Version: 2.1.1 Build 1)  -->', '')
_LOGO = _LOGO.replace('<svg ', '<svg role="img" aria-label="{B["name"]}" ', 1)
def logo_svg(fill=None):
    if not fill: return _LOGO
    return _LOGO.replace('<defs>', '<defs><style>.st0,.st1,.st2,.st3,.st4,.st5,.st6,.st7,.st8,.st9,path,polygon,rect{{fill:' + fill + ' !important}}</style>', 1) if '<defs>' in _LOGO else _LOGO.replace('>', '><style>path,polygon,rect{{fill:' + fill + ' !important}}</style>', 1)
open(OUT + 'assets/logo.svg', 'w').write(logo_svg())
open(OUT + 'assets/logo-white.svg', 'w').write(logo_svg('#FFFFFF'))
'''
L[i0:i1] = logo_code.split('\n')
src = '\n'.join(L)

# 3) 色：OFFISNAP の紺・水色 → ブランドの色
for a, b in [('#1F6FB2', B['dark']), ('#12A5C4', B['mid']), ('#EAF2FA', B['light']), ('#F0F5FA', B['light2']), ('#F4F8FC', B['light3']),
             ('#CADCEE', B['line']), ('#1E2A78', B['c2']), ('#2B84C6', B['c1'])]:
    src = src.replace(a, b)

# 4) 記事セクション名・言葉・ブランド名
src = src.replace('オフィス環境ならOFFICEMILL', '§OMTXT§').replace('OFFICEMILL', '§OM§').replace('offml.com', '§OMD§')
src = src.replace("utm_source=offisnap", f"utm_source={B['utm']}")
src = src.replace("'offices'", f"'{B['sec']}'").replace('offices/', f'{B["sec"]}/').replace("'offices", f"'{B['sec']}")
src = src.replace('海外の有名企業の最新オフィス', f'日本のかっこいい{B["subj"]}').replace('海外の有名企業のオフィス', f'日本のかっこいい{B["subj"]}')
src = src.replace('海外の有名企業', f'日本の{B["subj"]}').replace('有名企業の', '').replace('有名企業', B['subj'])
src = src.replace('海外オフィス', B['subj']).replace('海外の', '日本の').replace('海外', '日本')
src = src.replace('のオフィス・本社の内装', f'の{B["subj"]}の内装').replace('本社・内装写真', '内装写真').replace('の本社', '').replace('本社', B['kind'])
src = src.replace('受付から執務フロア、会議室、食堂、福利厚生の場所へと', B['about_lead'].split('。')[1].split('へと')[0] + 'へと')
src = src.replace('掲載企業', f'掲載{B["kind"]}').replace('各社の公式', f'各{B["kind"]}の公式').replace('各企業', f'各{B["kind"]}')
src = src.replace('1社ごとに', f'1{B["kind"]}ごとに').replace('1社ずつ', f'1{B["kind"]}ずつ').replace('社数', f'{B["kind"]}数')
src = src.replace('オフィスを取材・紹介する', f'{B["subj"]}を取材・紹介する').replace('オフィス一覧', f'{B["subj"]}一覧').replace('オフィスを探す', f'{B["subj"]}を探す')
src = src.replace("('offices', 'オフィス')", f"('{B['sec']}', '{B['subj_s']}')").replace("('§SEC§', 'オフィス')", '')
src = src.replace("('spaces', 'オフィス')", f"('spaces', '{B['subj_s']}')").replace("('cafes', 'オフィス')", f"('cafes', '{B['subj_s']}')")
src = src.replace('いま多く読まれている12社', 'いま多く読まれている12' + B['kind']).replace('人気のオフィス', f'人気の{B["subj_s"]}').replace('オフィスの内装', f'{B["subj_s"]}の内装').replace('のオフィス｜', f'の{B["subj_s"]}｜').replace('のオフィスを、', f'の{B["subj_s"]}を、')
src = src.replace('記事（オフィス）', f'記事（{B["subj_s"]}）').replace('articleSection":"§', 'articleSection":"§')
src = src.replace('会社名・都市・キーワードで探す', f'{B["kind"]}名・街・キーワードで探す').replace('最新のオフィス', f'最新の{B["subj_s"]}')
src = re.sub(r"BAND = '[^']*'", 'BAND = ' + json.dumps('日本で最も優れた' + B['subj_s'] + 'を、見に行こう。', ensure_ascii=False), src).replace('世界の日本の', '日本の')
src = src.replace('offisnap.com', B['domain']).replace('オフィスナップ', B['kana']).replace('OFFISNAP', B['name'])
src = src.replace('§OMTXT§', 'オフィス環境ならOFFICEMILL').replace('§OM§', 'OFFICEMILL').replace('§OMD§', 'offml.com')
src = src.replace("GA_ID = 'G-69FCWMYT6Y'", f"GA_ID = {json.dumps(B['ga'])}")
src = re.sub(r"<meta name=\"google-site-verification\"[^>]*>", '', src)
src = src.replace('｜オフィス・施設の内装を写真で紹介', '｜日本のかっこいい' + B['subj'] + 'を写真で紹介').replace('｜オフィス・店の内装を写真で紹介', '｜日本のかっこいい' + B['subj'] + 'を写真で紹介')
# サイトごとの文言（トップの帯・About・タグライン）
src = src.replace('日本の最新オフィス紹介', B['tag'])
if B.get('coll_lead'): src = src.replace('国も業種も違うオフィスを、共通のテーマで見比べる特集です。', B['coll_lead'])
if B.get('coll_desc'): src = src.replace(re.search(r"'植物、階段[^']*特集。'", src).group(0), json.dumps(B['coll_desc'], ensure_ascii=False).replace('"', "'"))
# 特集・人気・Q&A・翻訳表（OFFISNAP 固有）を無効化
src = src.replace("exec(open('tokushu.py', encoding='utf-8').read())", '')
src = src.replace("exec(open('popular.py', encoding='utf-8').read())", "POPULAR = [a['slug'] for a in A]")
src = src.replace("exec(open('articles_ja.py', encoding='utf-8').read())", 'J = {}')
src = src.replace("exec(open('site.py', encoding='utf-8').read())", '').replace("exec(open('editorial.py', encoding='utf-8').read())", '')
# GA を空にしたときはタグを出さない
src = src.replace("GA = (f'<script async", "GA = '' if not GA_ID else (f'<script async")
# アイコン：ブランドの favicon（build_mill.py が icons_<brand>/ に作る）
src = src.replace("shutil.copy(f'icons/", f"shutil.copy(f'{HERE}/icons_{os.environ['BRAND']}/")
src = src.replace("os.listdir('icons')", f"os.listdir('{HERE}/icons_{os.environ['BRAND']}')").replace("shutil.copy('icons/' + _f", f"shutil.copy('{HERE}/icons_{os.environ['BRAND']}/' + _f")
# 送客バナー：_src/banner/ にあればそれを使う（本番に置いてある実物）
if os.path.isdir(os.path.join(HERE, 'banner')): src = src.replace("shutil.copy(f'banner/", f"shutil.copy(f'{HERE}/banner/")

# 5) OFFISNAP 固有のスラッグ参照
src = src.replace("enumerate(['apple', 'swatch', 'nvidia', 'dyson', 'siemens', 'google-bay-view'])", "enumerate([a['slug'] for a in A[:6]])")
src = src.replace("og = og or purl(A_by['spotify'], 7)", "og = og or purl(A[0], A[0]['hero'][0])")
src = re.sub(r"OFFICIAL = \{.*?\n(?=OFFICIAL\.update)", "OFFICIAL = {}\n", src, flags=re.S)
src = re.sub(r"LOC = \{.*?\n(?=LOC\.update)", "LOC = {}\n", src, flags=re.S)
src = re.sub(r"KANA = \{.*?\n(?=KANA\.update)", "KANA = {}\n", src, flags=re.S)
src = re.sub(r"COUNTRY = \{\*\*COUNTRY20.*?\}", "COUNTRY = dict(COUNTRY20)", src)

# 6) 「日本のかっこいい」系の残りを、決めた一言（日本で最も優れた○○を厳選紹介）に合わせる。OFFISNAP 固有の社名の列挙も消す
src = src.replace('日本のかっこいい' + B['subj'] + 'を写真で紹介', '日本で最も優れた' + B['subj_s'] + 'を厳選紹介')
src = src.replace('日本のかっこいい' + B['subj'] + 'を、見に行こう。', '日本で最も優れた' + B['subj_s'] + 'を、見に行こう。')
src = src.replace('日本のかっこいい' + B['subj'], '日本で最も優れた' + B['subj_s'])
src = re.sub(r"Apple・Google・Amazon・Spotify・Dyson など\{len\(A\)\}社の内装、デザイン、働き方を日本語で。", "{len(A)}" + B['kind'] + "の内装とデザインを、初めて訪れた人が歩く順番で。", src)
src = src.replace('Apple・Google・Amazon・Spotify・Dyson など', '')

# 7) 掲載のご相談（フォームの文言）
for _w in ['オフィスを紹介してほしい', '紹介してほしいオフィスの場所', 'オフィスの写真', 'オフィスのことが分かる資料']:
    src = src.replace(_w, _w.replace('オフィス', B['subj_s']))
src = src.replace('会社名と、紹介してほしい', B['owner'] + '名と、紹介してほしい').replace('会社名・オフィスの場所', B['owner'] + '名・' + B['subj_s'] + 'の場所')

# 8) 2026-09-26 後半のコミット分（メタタイトル・構造化データ・絞り込み・一言の確定・OGP）。データは seo_<brand>.py
_seo = os.path.join(HERE, f'seo_{os.environ["BRAND"]}.py')
src = src.replace("if os.path.exists(_qp): exec(open(_qp, encoding='utf-8').read())",
                  "if os.path.exists(_qp): exec(open(_qp, encoding='utf-8').read())\n"
                  f"exec(open({json.dumps(_seo)}, encoding='utf-8').read())\n"
                  "F2_LABEL = 'テーマ'\n"
                  "def F2_OF(a): return [c['title'] for c in COLLECTIONS if any(x[0] == a['slug'] for x in c['items'])]\n")
# 一言の確定：「内装デザインが最も優れた○○を厳選紹介」／帯だけ「日本で」入り
src = src.replace('日本で最も優れた' + B['subj_s'] + 'を、見に行こう。', '§BAND§')
src = src.replace('日本で最も優れた' + B['subj_s'], '内装デザインが最も優れた' + B['subj_s'])
src = src.replace('§BAND§', '内装デザインが日本で最も優れた' + B['subj_s'] + 'を、見に行こう。')
# 街チップ：「渋谷（東京）」→「渋谷」
src = src.replace("def AREA_OF(a):\n", "def AREA_OF(a):\n    return a['city'].split('（')[0]\n", 1)
# head()：twitter:title/description を足す。og 画像を渡さないページは assets/og.png（1200×630）
src = src.replace("    og = og or purl(A[0], A[0]['hero'][0])", "    _ogdef = og is None; og = og or (SITE + '/assets/og.png')")
src = src.replace('<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{E(og)}">',
                  '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{E(og)}">')
src = src.replace("    _ogdef = og is None; og = og or (SITE + '/assets/og.png')", "    _ogdef = og is None; og = og or (SITE + '/assets/og.png'); _ogwh = '<meta property=\"og:image:width\" content=\"1200\"><meta property=\"og:image:height\" content=\"630\">' if _ogdef else ''")
src = src.replace('<meta property="og:image:alt" content="{E(title)}">\'', '<meta property="og:image:alt" content="{E(title)}">{_ogwh}\'')
# メタタイトル・description：施設ごとに seo_<brand>.py の SEO を使う
src = src.replace("def meta_title(a):\n", "def meta_title(a):\n    if a['slug'] in SEO: return SEO[a['slug']][0] + ' | ' + SITE_NAME\n", 1)
src = src.replace("def meta_desc(a):\n", "def meta_desc(a):\n    if a['slug'] in SEO: return SEO[a['slug']][1]\n", 1)
# トップと一覧のタイトル・description
src = re.sub(r"top = \(head\('[^']*', f'[^']*'", "top = (head(INDEX_TITLE, INDEX_DESC", src, count=1)
src = re.sub(r"lst = \(head\(f'[^']*', f'[^']*'", "lst = (head(LIST_TITLE + ' | ' + SITE_NAME, LIST_DESC", src, count=1)
# パンくず：「オフィス」→ 施設の種類
src = src.replace('<div class="crumb">オフィス › ', '<div class="crumb">' + B['subj_s'] + ' › ')
src = src.replace('{"@type":"ListItem","position":2,"name":"オフィス","item":SITE+"/' + B['sec'] + '/index.html"}', '{"@type":"ListItem","position":2,"name":"' + B['subj_s'] + '","item":SITE+"/' + B['sec'] + '/index.html"}')
# 構造化データ：施設ページに LocalBusiness／CafeOrCoffeeShop（住所は PLACE）
_ptype = 'CafeOrCoffeeShop' if os.environ['BRAND'] == 'cafe' else 'LocalBusiness'
src = src.replace('        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"' + B['name'] + '","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"' + B['subj_s'] + '"',
                  '        _pl = PLACE.get(a["slug"])\n'
                  '        if _pl:\n'
                  '            _d = {"@context":"https://schema.org","@type":"' + _ptype + '","@id":u+"#place","name":a["company"],"url":OFFICIAL.get(a["slug"], src),"sameAs":OFFICIAL.get(a["slug"], src),"image":purl(a, a["hero"][0]),"description":a["card"]}\n'
                  '            if KANA.get(a["slug"]): _d["alternateName"] = KANA[a["slug"]]\n'
                  '            _d["address"] = {"@type":"PostalAddress","streetAddress":_pl["streetAddress"],"addressLocality":_pl["addressLocality"],"addressRegion":_pl["addressRegion"],"addressCountry":"JP"}\n'
                  '            if _pl.get("openingHours"): _d["openingHours"] = _pl["openingHours"]\n'
                  '            _d["subjectOf"] = {"@id":u+"#article"}\n'
                  '            ld.append(_d)\n'
                  '        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"' + B['name'] + '","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"' + B['subj_s'] + '"', 1)
# 旧スラッグからの転送ページ
src = src.replace("open(OUT + 'site.webmanifest', 'w'", "for _old, _new in REDIRECTS.items():\n    open(OUT + f'{SEC_NAME}/{_old}.html', 'w', encoding='utf-8').write(f'<!doctype html><meta charset=\"utf-8\"><title>Redirecting</title><meta http-equiv=\"refresh\" content=\"0;url=/{SEC_NAME}/{_new}.html\"><meta name=\"robots\" content=\"noindex\"><link rel=\"canonical\" href=\"{SITE}/{SEC_NAME}/{_new}.html\">')\nopen(OUT + 'site.webmanifest', 'w'", 1)

# 2026-09-27 キーワードに残っていた「オフィス」を消す
src = re.sub(r"a\['industry'\], 'オフィス', '([^']*)',", r"a['industry'], '\1',", src)
open(os.path.join(HERE, f'_generated_{os.environ["BRAND"]}.py'), 'w', encoding='utf-8').write(src)
exec(compile(src, f'build_{os.environ["BRAND"]}.py', 'exec'))
