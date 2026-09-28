# COWORKMILL プレビュー：WALL の build.py が出す HTML と style.css をそのまま使い、色・ロゴ・言語だけ変える
import os, re, html, json, shutil
import omfont as o



W = os.environ.get('WALL_DIR', '/mnt/user-data/uploads/Downloads/offisnap-preview/_wall/wall-main/')
OUT = os.environ.get('OUT_DIR', '/mnt/user-data/outputs/offisnap-preview/')
shutil.rmtree(OUT, ignore_errors=True)
for d in ['', 'assets', 'spaces', 'collections', 'questions', 'about']:
    os.makedirs(OUT + d, exist_ok=True)


exec(open("/tmp/cwrepo/_src/cowork_facilities.py", encoding='utf-8').read())
A = sorted(A30, key=lambda a: a.get('added', ''), reverse=True)  # 2026-09-27 新着順＝掲載日の新しい順（後から足した施設が下に入っていた）
IMG20 = dict(IMG30); KANA20 = dict(KANA30); COUNTRY20 = dict(COUNTRY30); ED = dict(ED30); ED20 = {}
exec(open("/tmp/cwrepo/_src/collections_cowork.py", encoding='utf-8').read())
A_by = {a['slug']: a for a in A}
for _a in A:
    _h = _a['hero'][0]
    _a['steps'] = [st[:3] + ([(n, c) for n, c in st[3] if n != _h],) for st in _a['steps']]
SEC_NAME = "spaces"; KIND_WORD = "\u65bd\u8a2d"; SITE_NAME = "COWORKMILL"; UTM = "coworkmill"
QA_TITLE = "\u30b3\u30ef\u30fc\u30ad\u30f3\u30b0\u30b9\u30da\u30fc\u30b9\u306e Q&A"
QA_LEAD = "\u65e5\u672c\u306e\u30b3\u30ef\u30fc\u30ad\u30f3\u30b0\u30b9\u30da\u30fc\u30b9\u306b\u3064\u3044\u3066\u3001\u3088\u304f\u805e\u304b\u308c\u308b\u8cea\u554f\u306b\u77ed\u304f\u7b54\u3048\u307e\u3059\u3002\u7b54\u3048\u306f\u3059\u3079\u3066\u3001\u63b2\u8f09\u3057\u3066\u3044\u308b\u65bd\u8a2d\u306e\u516c\u5f0f\u60c5\u5831\u304b\u3089\u66f8\u3044\u3066\u3044\u307e\u3059\u3002"
_qp = "/tmp/cwrepo/_src/questions_cowork.py"
if os.path.exists(_qp): exec(open(_qp, encoding='utf-8').read())
exec(open("/tmp/cwrepo/_src/seo_cowork.py", encoding='utf-8').read())
F2_LABEL = 'テーマ'
def F2_OF(a): return [c['title'] for c in COLLECTIONS if any(x[0] == a['slug'] for x in c['items'])]

def url(slug, n): return IMG30.get(slug, {}).get(str(n))
def purl(a, n): return url(a['slug'], n)

# ---- ロゴ ----

_LOGO = open("/tmp/cwrepo/_src/logo_cowork.svg", encoding='utf-8').read()
_LOGO = re.sub(r'<\?xml[^>]*>\s*', '', _LOGO).replace('<!-- Generator: Adobe Illustrator 30.2.1, SVG Export Plug-In . SVG Version: 2.1.1 Build 1)  -->', '')
_LOGO = _LOGO.replace('<svg ', '<svg role="img" aria-label="COWORKMILL" ', 1)
def logo_svg(fill=None):
    if not fill: return _LOGO
    return _LOGO.replace('<defs>', '<defs><style>.st0,.st1,.st2,.st3,.st4,.st5,.st6,.st7,.st8,.st9,path,polygon,rect{fill:' + fill + ' !important}</style>', 1) if '<defs>' in _LOGO else _LOGO.replace('>', '><style>path,polygon,rect{fill:' + fill + ' !important}</style>', 1)
open(OUT + 'assets/logo.svg', 'w').write(logo_svg())
open(OUT + 'assets/logo-white.svg', 'w').write(logo_svg('#FFFFFF'))


# ---- CSS：WALL の style.css をそのまま。色だけ置換し、日本語用の書体を足す ----
css = open(W + 'assets/style.css', encoding='utf-8').read()
for a, b in [('#e2551b', '#2F6A98'), ('#E2551B', '#2F6A98'), ('#f2a93b', '#4F9DB0'), ('#fdf0e7', '#EEF6F1'), ('#fbf3ee', '#F3F8F4'),
             ('#fdf6f2', '#F6FAF7'), ('#f3d9c7', '#CFE3D8'), ('#c2440f', '#3B7DAE'), ('#E86A1F', '#7FC39A'), ('#C8400F', '#3B7DAE')]:
    css = css.replace(a, b)
css += '''
.lst{background:var(--ground);border-left:3px solid var(--accent);padding:14px 18px;margin:0 0 16px;font-size:14px;line-height:1.8}.lst ol{margin:6px 0 8px 20px;padding:0}.lst p{margin:0 0 6px}
.qidx{list-style:none;padding:0;margin:8px 0 48px;display:grid;gap:18px}.qidx li{margin:0}.qidx a{position:relative;display:grid;grid-template-columns:2fr 1fr 1fr;gap:3px;height:260px;text-decoration:none;overflow:hidden;background:#111;color:#fff}.qidx a img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}.qidx a:hover img{transform:scale(1.03)}.qidx a .qc{position:absolute;left:0;right:0;bottom:0;padding:56px 18px 16px;background:linear-gradient(transparent,rgba(0,0,0,.72))}.qidx a .qc b{display:block;font-size:22px;font-weight:700;line-height:1.35;font-family:var(--sans);color:#fff}.qidx a .qc span{display:block;margin-top:4px;font-size:13px;color:rgba(255,255,255,.85);line-height:1.6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qidx a .qq{position:absolute;left:0;top:0;background:var(--accent);color:#fff;font:700 11px/1 var(--sans);padding:6px 8px}@media(max-width:720px){.qidx a{grid-template-columns:1fr 1fr;grid-template-rows:150px 90px;height:auto}.qidx a img:first-of-type{grid-column:1/3}.qidx a .qc b{font-size:18px}}
.qmore{list-style:none;padding:0;margin:0}.qmore li{border-top:1px solid var(--line)}.qmore li:last-child{border-bottom:1px solid var(--line)}.qmore a{display:block;padding:14px 0;font-weight:600;text-decoration:none}.qmore a:hover{color:var(--accent)}
/* 2026-09-26 わたるさん「ページを狭くするとガタガタ」→ 長い社名で列の幅が変わらないように、列を等幅に固定 */
.cards{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-width:0}.card .co .kn{white-space:normal}
@media (max-width:900px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* COWORKMILL: 日本語の書体（欧文は WALL と同じ Cormorant / Inter Tight、和文は明朝とゴシック） */
:root{--serif:"Shippori Mincho B1","Hiragino Mincho ProN","Yu Mincho",serif;--sans:"Zen Kaku Gothic New","Hiragino Sans","Noto Sans JP",sans-serif;--jp:"Shippori Mincho B1","Hiragino Mincho ProN",serif}
body{font-family:var(--sans);font-feature-settings:"palt"}
.std,.step p,.ctx p{line-height:1.95}
.head h1,.step h2,.ctx h2,.sec-h h2,.cc h3,.hslider h1{letter-spacing:.02em;word-break:auto-phrase}
.ctx-h .hanko b{font-family:var(--serif);font-style:normal;font-weight:700;letter-spacing:.02em}
.ctx-h .hanko small{white-space:nowrap;font-family:var(--sans);font-style:normal;font-size:12px;letter-spacing:.08em}
.ctx-h.wide{padding-right:20px}.ctx-h.wide .hanko{position:static;display:block;text-align:left;margin:0 0 14px}
.edc{margin:0 0 34px;border-top:2px solid var(--ink);padding-top:16px}
.edc .lab{font-size:10.5px;letter-spacing:.2em;color:var(--accent);margin:0 0 8px}
.edc p{font-size:15px;line-height:1.95;color:var(--ink-2);margin:0 0 10px}
.edc .sig{font-size:12px;color:var(--mute);margin:0}
.draft{letter-spacing:.08em}
/* COWORKMILL 2026-09-25 デザイン改善：WALLの寸法に合わせ、和文を読みやすく */
/* 1. ロゴ：WALL（109×44）と同じ見た目の量に。COWORKMILLは8文字なので高さを30pxに */
header .wm{gap:12px}
header .wm img{height:30px}
header .wm small{font-size:10px;letter-spacing:.14em;margin-top:0;padding-left:12px;border-left:2px solid var(--accent)}
@media (max-width:700px){header .wm img{height:24px}header .wm small{border-left:0;padding-left:0}}
.foot .wm img{height:18px}
/* 2. 和文の詰め：本文はベタ組み（palt なし）、見出しだけ palt */
body{font-feature-settings:normal;letter-spacing:.01em}
h1,h2,h3,.sec-h h2,.card .co,.hanko b{font-feature-settings:"palt"}
/* 3. トップの大見出し：行間を和文向けに、1行の長さを抑える */
main>.hero h1,.hslider h1{font-size:clamp(28px,3.6vw,52px);line-height:1.32;letter-spacing:.03em;max-width:20em;font-weight:600}
main>.hero p.std,.hslider .std{font-size:16px;line-height:1.9;max-width:40em}
/* 4. 記事の見出し・本文 */
.head h1{font-size:clamp(24px,3vw,36px);line-height:1.45;letter-spacing:.03em;font-weight:600;text-wrap:balance}
.head .std{font-size:16px;line-height:1.9;max-width:40em}
.step .no{font-family:var(--sans);font-style:normal;font-size:12px;letter-spacing:.14em;font-weight:600}
.step h2,.ctx h2{font-size:22px;line-height:1.55;letter-spacing:.02em;font-weight:600}
.step h2{align-items:flex-start}.step h2::before{transform:translateY(12px)}
.step p,.ctx p,.edc p{font-size:16px;line-height:2;max-width:40em;margin:0 0 14px}
.cap{font-size:12px;line-height:1.7}
/* 5. 一覧カード：斜体をやめ、和文の行間に */
.card .cp{font-style:normal;font-weight:500;font-size:15px;line-height:1.6;letter-spacing:.01em}
.card .co{font-size:12.5px;letter-spacing:.08em}
.card .cr{letter-spacing:.06em}
.cc h3{line-height:1.5;letter-spacing:.02em}.ccs{line-height:1.7}
.sec-h h2{font-size:24px;letter-spacing:.04em}
.sec-h .sub{letter-spacing:.04em}
/* 6. 上部の帯・パンくず・目次 */
.draft{letter-spacing:.14em;font-size:11px}
.crumb{letter-spacing:.06em}
.toc{font-size:12px;line-height:1.7}.toc p{letter-spacing:.16em}
.foot p.fbang{font-size:15px;letter-spacing:.03em;line-height:1.6}
.foot{letter-spacing:.03em}
.nb{white-space:nowrap}
/* COWORKMILL 2026-09-25 その2：写真の並び・トップのスライド・パートナー欄・フッターと検索欄 */
/* A. 記事の写真：複数枚は横に並べる（3枚は3列、2枚は2列。スマホは2列）。キャプションは細い縦線つき */
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:6px 0 16px}
.grid3:has(> .fig:nth-child(2):last-child){grid-template-columns:1fr 1fr}
.grid3 .fig{margin:0}
.grid3 .ph{aspect-ratio:4/3;margin:0 0 6px}
@media (max-width:700px){.grid3{grid-template-columns:1fr 1fr;gap:8px}}
article .fig{margin:6px 0 18px}
article .fig .cap{font-size:12px;line-height:1.7;color:var(--mute);margin:-2px 0 0;padding-left:10px;border-left:2px solid var(--line)}
/* B. トップのスライド：暗くする帯を少し強くして文字を読みやすく。ラベルと「続きを読む」を整える */
main>.hero .cap{background:linear-gradient(transparent,rgba(0,0,0,.45) 35%,rgba(0,0,0,.82))}
.hslider .tag{font-size:11px;letter-spacing:.2em;opacity:.92}
.hslider h1{text-shadow:0 1px 10px rgba(0,0,0,.35)}
.hslider .std{text-shadow:0 1px 8px rgba(0,0,0,.5);opacity:.95}
.hslider .ctx-tag{font-size:12px;letter-spacing:.12em;padding:9px 18px;margin-top:16px;text-transform:none}
/* C. パートナー欄は公開まで非表示（2026-09-25 わたるさん）。トップの生成部分でセクションごと出さない */
/* D. 検索欄とフッター */
.tsearch input{font-size:15px;letter-spacing:.02em}
.tsearch button{font-size:12.5px;letter-spacing:.14em;padding:0 30px}
.foot{font-size:12.5px;padding:34px 0 28px;letter-spacing:.04em}
.foot .wrap{gap:22px 56px}
.foot ul{gap:8px}
.foot a{color:#d9d5ce}
.foot p.fbang{font-size:15px;letter-spacing:.04em;color:#fff;opacity:.9}
.foot .copy{margin-top:12px;font-size:11px;letter-spacing:.06em}
/* スマホの手直し（2026-09-25 通し確認）：3枚目は幅いっぱい、トップのリード文は3行まで、章見出しの折り返しを揃える */
@media (max-width:700px){.grid3 .fig:nth-child(3):last-child{grid-column:1/-1}.grid3 .fig:nth-child(3):last-child .ph{aspect-ratio:3/2}
.hslider .std{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.step h2{text-wrap:balance}
/* 社名を主役に（2026-09-25） */
.card .co{font-family:var(--serif);font-size:19px;font-weight:600;letter-spacing:.02em;margin:10px 0 3px;font-feature-settings:"palt";line-height:1.3;text-wrap:balance}
.card .cp{font-family:var(--sans);font-size:14px;font-weight:400;color:var(--ink-2);line-height:1.6;margin-top:2px}
@media (max-width:700px){.card .co{font-size:17px}}
/* 一覧カードの余白（2026-09-25 スマホ指摘）：WALL の特集用 .cr（線と上下28px）がカードの .cr に当たっていたのを外す。読みは折り返さない */
.card .cr{display:block;padding:0;border-top:0;margin-top:6px;line-height:1.6}
.card .co .kn{white-space:nowrap;font-size:.86em}
@media (max-width:700px){.card .co{font-size:15px;line-height:1.35;margin:8px 0 2px}.card .cp{font-size:13px;line-height:1.55}.cards{gap:22px 14px}}
/* 案A（2026-09-25 わたるさん選択）：見出しもゴシック。スマホで明朝の見出しが浮いて見える違和感をなくす。太さだけで本文と差をつける */
:root{--serif:"Zen Kaku Gothic New","Hiragino Sans","Noto Sans JP",sans-serif;--jp:"Zen Kaku Gothic New","Hiragino Sans",sans-serif}
h1,h2,h3,.head h1,.step h2,.ctx h2,.sec-h h2,.cc h3,.hslider h1,main>.hero h1,.card .co,.ctx-h .hanko b{font-family:var(--sans);font-weight:700;letter-spacing:.01em}
.draft{letter-spacing:.08em;font-size:12px}
@media (max-width:700px){.draft{letter-spacing:.05em;font-size:11.5px;padding-left:12px;padding-right:12px}}
/* ヘッダーを追随（2026-09-25 わたるさん）：スクロール中はロゴとメニューだけに細くする */
header.wrap{position:sticky;top:0;z-index:50;background:#fff;box-shadow:0 0 0 100vmax #fff;clip-path:inset(0 -100vmax -1px)}
body.stuck header.wrap{border-bottom:1px solid var(--line)}
body.stuck header .wm small{display:none}
@media (max-width:700px){body.stuck header .r{display:none}}
/* WALL と同じく、下に行くとヘッダー全体を少し小さく（body.hdr-min 相当） */
header .wm img,header .nav,header .nav ul{transition:height .15s,padding .15s,font-size .15s}
body.stuck header .wm img{height:24px}
body.stuck header .nav{padding-block:10px}
@media (max-width:700px){body.stuck header .wm img{height:20px}body.stuck header .nav{padding-block:8px 0}body.stuck header .nav ul{padding:8px 0;font-size:13px}}
/* 一覧カードを WALL 寄りに（2026-09-25 わたるさん）：写真が主役。社名が主・ひとことは小さな添え書き（「」なし）。NEW の帯 */
.sec-h h2{font-family:"Shippori Mincho B1","Hiragino Mincho ProN",serif;font-weight:600;font-size:26px;letter-spacing:.02em}
.card .co{font-family:var(--sans);font-size:15px;font-weight:700;letter-spacing:.06em;margin:10px 0 3px;line-height:1.4;text-wrap:initial}
.card .co .kn{font-size:11px;font-weight:500;color:var(--mute);letter-spacing:.04em;margin-left:4px;white-space:nowrap}
.card .cp{font-family:"Shippori Mincho B1","Hiragino Mincho ProN",serif;font-size:13px;font-weight:500;line-height:1.6;color:var(--ink-2);padding-bottom:8px;border-bottom:1px solid var(--line);margin:0 0 8px}
.card .cr{font-size:10.5px;letter-spacing:.08em;margin-top:0}
.newb{display:block;top:0;right:0;width:64px;height:64px;padding:0;border-radius:0;box-shadow:none;background:linear-gradient(135deg,#163a8a,#2F6A98);clip-path:polygon(0 0,100% 0,100% 100%);font-size:0}
.newb::after{content:"NEW";position:absolute;left:66.67%;top:33.33%;transform:translate(-50%,-50%) rotate(45deg);color:#fff;font:800 10.5px/1 var(--sans);letter-spacing:.14em;white-space:nowrap}
.cards{gap:26px 20px}
/* 人気のコワーキング：写真の左上に順位（2026-09-26） */
.card .phw{position:relative}
.rk{position:absolute;left:0;top:0;z-index:2;min-width:34px;height:34px;padding:0 8px;background:#111;color:#fff;font:700 15px/34px var(--sans);font-style:normal;text-align:center;letter-spacing:.02em}
.cards.bynew .rk{display:none}
.sortbar{display:flex;justify-content:space-between;align-items:center;margin:0 0 18px;padding-bottom:10px;border-bottom:1px solid var(--line);font-size:13px}
.sortbar .cnt{color:var(--mute)}
.sortbar .tg{display:flex;border:1px solid #111}
.sortbar button{appearance:none;border:0;background:#fff;color:#111;cursor:pointer;padding:6px 14px;font:700 12.5px/1 var(--sans);letter-spacing:.06em}
.sortbar button.on{background:#111;color:#fff}
.toc{top:calc(var(--hh,60px) + 16px)}
.fbar{margin:0 0 18px;padding-bottom:14px;border-bottom:1px solid var(--line)}.fbar .srch{display:block;position:relative;max-width:620px;margin:0 0 14px}.fbar .srch input{width:100%;box-sizing:border-box;border:1px solid var(--line);background:#fff;padding:12px 14px 12px 38px;font:14px/1.4 var(--sans);color:#111;border-radius:2px}.fbar .srch input:focus{outline:none;border-color:#111}.fbar .srch:before{content:"";position:absolute;left:14px;top:50%;width:12px;height:12px;margin-top:-8px;border:2px solid var(--accent);border-radius:50%;box-sizing:border-box}.fbar .srch:after{content:"";position:absolute;left:24px;top:50%;width:6px;height:2px;margin-top:2px;background:var(--accent);transform:rotate(45deg)}.fbar .chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}.fbar .chips button{appearance:none;cursor:pointer;border:1px solid var(--accent);background:#fff;color:var(--accent);padding:7px 14px;border-radius:999px;font:500 13px/1 var(--sans);white-space:nowrap}.fbar .chips button small{font-size:10.5px;margin-left:5px;opacity:.75;font-weight:400}.fbar .chips button.on{background:var(--accent);color:#fff}.fbar .chips button:hover{background:var(--ground)}.fbar .chips button.on:hover{background:var(--accent)}.fbar .fsel{display:flex;flex-wrap:wrap;align-items:center;gap:10px;font-size:13px}.fbar select{appearance:none;-webkit-appearance:none;border:1px solid var(--line);background:#fff url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2710%27 height=%276%27%3E%3Cpath d=%27M1 1l4 4 4-4%27 fill=%27none%27 stroke=%27%23111%27 stroke-width=%271.5%27/%3E%3C/svg%3E") no-repeat right 10px center;padding:8px 28px 8px 12px;font:13px/1.2 var(--sans);color:#111;border-radius:2px;cursor:pointer}.fbar .cnt{margin-left:auto;color:var(--mute)}.fbar .cnt b{color:#111;font-size:15px;margin-right:2px}.fnone{padding:40px 0;color:var(--mute);text-align:center}@media(max-width:700px){.fbar .chips{flex-wrap:nowrap;overflow-x:auto;padding-bottom:6px;margin-right:-16px;padding-right:16px;scrollbar-width:none}.fbar .chips::-webkit-scrollbar{display:none}.fbar .cnt{width:100%;margin-left:0}}
@media (max-width:700px){.rk{min-width:28px;height:28px;font-size:13px;line-height:28px;padding:0 6px}}
@media (max-width:700px){.card .co{font-size:13.5px;letter-spacing:.04em;margin:8px 0 2px}.card .cp{font-size:12px;line-height:1.55}.newb{width:48px;height:48px}.newb::after{font-size:9px}.cards{gap:22px 14px}}
'''
css += '\n/* 2026-09-27 施設情報（施設ページ最下部） */\n.shopinfo{margin:8px 0 40px;padding:22px 24px;background:var(--accent-tint,#f6f6f6);border-radius:4px}.shopinfo h2{font-size:18px;margin:0 0 12px}.shopinfo dl{margin:0;display:grid;gap:10px}.shopinfo dl div{display:grid;grid-template-columns:7em 1fr;gap:12px;font-size:14px;line-height:1.7}.shopinfo dt{color:var(--mute);font-size:12px;padding-top:2px}.shopinfo dd{margin:0}.shopinfo a{border-bottom:1px solid var(--accent)}@media(max-width:600px){.shopinfo dl div{grid-template-columns:1fr;gap:2px}}\n'
open(OUT + 'assets/style.css', 'w', encoding='utf-8').write(css)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho+B1:wght@500;600&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">'
E = lambda s: html.escape(str(s), quote=True)
# 見出しの区切り「｜」が行頭に来ないように：直前の1文字と「｜」をくっつけ、「｜」の直後で折り返せるようにする（2026-09-25）
T = lambda s: re.sub(r'(.)｜', r'<span class="nb">\1｜</span><wbr>', E(s))
CUR = ' aria-current="page"'; NEWB = '<i class="newb">NEW</i>'; LAZY = ' loading="lazy"'; ON = ' class="on"'
def toc_items(slugs):
    return ''.join(f'<li><a href="#s{i+1}">{E(A_by[s]["company"])}</a></li>' for i, s in enumerate(slugs))
# OFFICEMILL バナー（日本語版）。_src/banner/ の実物を assets/banner/ に置く（2026-09-25。それまでは WALL の英語版を直リンクしていた）
OMB160 = '/assets/banner/officemill_160x600.webp'
OMB728 = '/assets/banner/officemill_728x90.webp'
os.makedirs(OUT + 'assets/banner', exist_ok=True)
for _b in ('officemill_160x600.webp', 'officemill_728x90.webp'):
    shutil.copy(f'/tmp/cwrepo/_src/banner/{_b}', OUT + 'assets/banner/' + _b)

SITE = 'https://cowkml.com'
# 公開用（2026-09-25 わたるさん判断：写真は公式プレス素材＋出典明記のまま公開。noindex を外す）
# ---- メタタイトルの決まり（2026-09-27 わたるさん「アルファベットとカタカナをマストで」） ----
# ①トップ：英字名（カタカナ）＋一言  ②下層：ページ名 | 英字名（カタカナ）  ③About：英字名（カタカナ）について
_BRAND_EN = 'COWORKMILL'; _BRAND_KANA = 'コワークミル'
def _brand_title(t):
    full = _BRAND_EN + '（' + _BRAND_KANA + '）'
    if full in t: return t
    if t.startswith(_BRAND_EN): return full + t[len(_BRAND_EN):].lstrip()
    t = re.sub(r'\s*[|｜]\s*' + re.escape(_BRAND_EN) + r'\s*$', '', t)
    return t + ' | ' + full
def head(title, desc, p, path='', og=None, otype='website'):
    title = _brand_title(title)
    u = SITE + '/' + ('' if path == 'index.html' else path)
    _ogdef = og is None; og = og or (SITE + '/assets/og.png'); _ogwh = '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if _ogdef else ''
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="index,follow,max-image-preview:large"><title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            f'<link rel="canonical" href="{E(u)}"><meta property="og:url" content="{E(u)}"><meta property="og:site_name" content="COWORKMILL"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">'
            f'<meta property="og:type" content="{otype}"><meta property="og:image" content="{E(og)}"><meta property="og:locale" content="ja_JP"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{E(og)}">'
            f'<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#3B7DAE"><meta name="author" content="COWORKMILL 編集部"><meta property="og:image:alt" content="{E(title)}">{_ogwh}'
            f''
            '<meta name="google-adsense-account" content="ca-pub-1379037925480740">'
            f'{FONTS}<link rel="stylesheet" href="{p}assets/style.css">{GA}</head><body>')
# 2026-09-25 Search Console（URL プレフィックス https://cowkml.com/）の HTML タグ認証と GA4（プロパティ COWORKMILL 555994414、ストリーム 15843068805）
GSC_TOKEN = 'Ixm7-L8tqlN2EwSv7kkjfVxdeBSa6Hwyk-9DueLBYVY'
GA_ID = "G-P6CZCM6K18"
GA = '' if not GA_ID else (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}",{{anonymize_ip:true}});</script>')
shutil.copy('flip.js', OUT + 'assets/flip.js')  # 一覧カードの写真めくり
for _f in os.listdir('/tmp/cwrepo/_src/icons_cowork'):
    shutil.copy('/tmp/cwrepo/_src/icons_cowork/' + _f, OUT + _f)

BAND = "内装デザインが日本で最も優れたコワーキングを、見に行こう。"  # 2026-09-25 わたるさん選択
def nav(p, cur='', band=None):
    # 青い帯（.draft）は全ページに出す（2026-09-25 わたるさん「サイトのデザインが締まる」）
    items = [('spaces', 'コワーキング'), ('collections', '特集'), ('questions', 'Q&amp;A'), ('about', 'About')]
    li = ''.join(f'<li><a href="{p}{k}/index.html"{CUR if k == cur else ""}>{v}</a></li>' for k, v in items)
    return (f'<header class="wrap"><div class="nav"><a class="wm" href="{p}index.html"><img src="{p}assets/logo.svg" alt="COWORKMILL" width="120" height="30"><small>内装デザインが最も優れたコワーキングを厳選紹介</small></a>\n'
            f'<ul>{li}</ul>\n<div class="r"><span>JP</span><a class="btn" href="{p}contact/index.html?topic=listing">掲載のご相談</a></div></div></header>'
            f'<div class="draft">{band or BAND}</div>')

def foot(p):
    return (f'<footer class="foot"><div class="wrap"><div class="fbrand"><a class="wm" href="{p}index.html"><img src="{p}assets/logo-white.svg" alt="COWORKMILL" width="96" height="22"></a><p class="fbang">内装デザインが最も優れたコワーキングを厳選紹介メディア、COWORKMILL。</p></div>\n'
            f'<ul><li><a href="{p}about/index.html">COWORKMILL について</a></li><li><a href="{p}questions/index.html">Q&amp;A</a></li><li><a href="{p}spaces/index.html">地域から探す</a></li><li><a href="{p}spaces/index.html">業種から探す</a></li></ul>\n'
            f'<ul><li><a href="{p}about/privacy.html">プライバシーポリシー</a></li><li><a href="{p}about/terms.html">利用規約</a></li><li><a href="{p}contact/index.html">お問い合わせ</a></li></ul>\n'
            '<p class="copy">© 2026 COWORKMILL. 日本のコワーキングスペースを取材・紹介するメディアです。</p></div></footer>'
            f'<script src="{p}assets/flip.js" defer></script>'
            '<script>(function(){var b=document.body,h=document.querySelector("header.wrap"),f=function(){b.classList.toggle("stuck",window.scrollY>80);if(h)document.documentElement.style.setProperty("--hh",h.offsetHeight+"px")};window.addEventListener("resize",f);f();window.addEventListener("scroll",f,{passive:true})})();</script>')

J = {}
for _slug, _j in J.items():
    _a = A_by[_slug]
    for k in ('card', 'title', 'lead', 'concept'):
        _a[k] = _j[k]
    _a['word'] = dict(_a['word'], title=_j['word']['title'], body=_j['word']['body'])
    assert len(_j['steps']) == len(_a['steps']), _slug
    _a['steps'] = [(f'{i+1:02d}｜{lab}', h, ps, _a['steps'][i][3]) for i, (lab, h, ps) in enumerate(_j['steps'])]

def fig(a, n, cap, cls=''):
    u = purl(a, n)
    if not u: return ''
    return f'<figure class="fig {cls}"><img class="ph" src="{E(u)}" alt="{E(cap)}" loading="lazy"><figcaption class="cap">{E(cap)}</figcaption></figure>'

def tagline(a): return f'{city_short(a)}｜{a["industry"]}'
def city_short(a): return a['city'].split('（')[0]

# 社名のふりがな（2026-09-25 わたるさん：社名を主役に。「DYSON（ダイソン）」の形で大きく）
KANA = {}
KANA.update(KANA20)
def coname(a): return E(a['company'].upper()) + (f'<span class="kn">（{E(KANA[a["slug"]])}）</span>' if a['slug'] in KANA else '')  # 読みは途中で折り返さない
def card(a, p, new=True, rank=None, attrs=''):
    u = purl(a, a['hero'][0])
    img = f'<img class="ph" src="{E(u)}" alt="" loading="lazy">' if u else ''
    _ex = [purl(a, n) for st in a['steps'] for n, _ in st[3]]; _ex = [x for x in _ex if x and x != u][:3]
    _dp = f' data-ph="{E("|".join(_ex))}"' if _ex else ''
    _rk = f'<i class="rk">{rank}</i>' if rank else ''
    return (f'<a class="card" href="{p}spaces/{a["slug"]}.html"{_dp}{attrs}><span class="phw">{_rk}{img}{NEWB if new else ""}</span>'
            f'<div class="co">{coname(a)}</div><div class="cp">{E(a["card"])}</div><div class="cr">{E(city_short(a))}｜{E(a["industry"])}</div></a>')

# 掲載施設の公式サイト（2026-09-25 わたるさん指摘：「公式サイト」は出典ではなく会社の公式ページ。出典は下の基本情報に残す）
OFFICIAL = {}
OFFICIAL.update(globals().get('OFFICIAL30', {}))
assert all(a['slug'] in OFFICIAL for a in A), [a['slug'] for a in A if a['slug'] not in OFFICIAL]

# メタタイトル（2026-09-25 わたるさん：「社名（英字/カタカナ）＋オフィス」で引っかかるように。「コワーキングスペース」でも1位を狙う）
# 検索は「ダイソン オフィス」「dyson 施設」「〜 オフィス 内装」「〜 オフィス 写真」が中心なので、英字とカタカナの両方＋オフィス・施設・内装・写真を入れる
LOC = {}
LOC.update(globals().get('LOC30', {}))
def meta_title(a):
    if a['slug'] in SEO: return SEO[a['slug']][0] + ' | ' + SITE_NAME
    kn = KANA.get(a['slug']); loc = LOC.get(a['slug'], city_short(a) + '施設')
    return f"{a['company']}{'（' + kn + '）' if kn else ''}のコワーキング｜{loc}の内装・写真 | COWORKMILL"
def meta_desc(a):
    if a['slug'] in SEO: return SEO[a['slug']][1]
    kn = KANA.get(a['slug'])
    return f"{a['company']}{'（' + kn + '）' if kn else ''}の{LOC.get(a['slug'], city_short(a) + '施設')}のコワーキングを、公式の写真と情報で紹介。{a['card']}。{a['lead']}"

# ---- 記事ページ（WALL spaces/mitsui-fudosan.html と同じ並び） ----
import os
_UNCONF = ('確認中', '要確認', '未確認', 'to confirm', 'TBD', 'TODO')
def _unconf(v):
    # 未確認メモは本番に出さない。値そのものがメモなら行ごと消し、「、」区切りの一部なら、その部分だけ消す
    v = str(v)
    if not any(u in v for u in _UNCONF): return v
    parts = [x for x in re.split(r'[、,]', v) if not any(u in x for u in _UNCONF)]
    return '、'.join(p.strip() for p in parts if p.strip())
def article(a):
    p = '../'
    src = next(c[1] for c in a['credits'] if c[0] == '出典URL')
    host = re.sub(r'^https?://(www\.)?', '', src).split('/')[0]
    _off = OFFICIAL.get(a['slug'], src)
    # 2026-09-27 わたるさん「会社名そのものを公式HPへのリンクに。端の『公式サイト ○○ ↗』は置かない」「未確認メモを本番に出さない」
    _NAMEK = ('会社', '施設', '店', '店名', '企業')
    def _lk(v): return f'<a class="offl" href="{E(_off)}" target="_blank" rel="noopener">{E(v)} &#8599;</a>'
    _fx = [(k, _unconf(v)) for k, v in a['facts'] if k != '写真']
    _fx = [(k, v) for k, v in _fx if v]
    facts = ''.join(f'<span>{E(k)} <b>{_lk(v) if k in _NAMEK and _off else E(v)}</b></span>' for k, v in _fx)
    if _off and not any(k in _NAMEK for k, v in _fx):
        facts = f'<span>{"店" if os.environ.get("BRAND") == "cafe" else "会社"} <b>{_lk(a["company"])}</b></span>' + facts
    toc = '<li><a href="#concept">はじめに</a></li>' + ''.join(f'<li><a href="#s{i+1}">{E(s[0].split("｜")[1].strip())}</a></li>' for i, s in enumerate(a['steps'])) + '<li><a href="#context">キーワード</a></li><li><a href="#editor">編集部より</a></li><li><a href="#credits">基本情報</a></li>'
    body = f'<section class="step" id="concept"><p class="no">はじめに</p><h2>{E(a["concept"][0])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in a['concept'][1]) + '</section>'
    # 写真の並べ方（2026-09-25 わたるさん）：写真が少ない記事は1枚ずつ幅いっぱいに大きく。本文の写真が12枚以上ある記事だけ横並び
    _total = sum(1 for st in a['steps'] for n, _ in st[3] if purl(a, n))
    _grid = _total >= 12
    for i, s in enumerate(a['steps']):
        figs = [fig(a, n, c) for n, c in s[3]]; figs = [f for f in figs if f]
        g = ''
        if len(figs) == 1 or not _grid: g = ''.join(figs)
        elif figs: g = f'<div class="grid3">{"".join(figs)}</div>'
        body += f'<section class="step" id="s{i+1}"><p class="no">{E(s[0])}</p><h2>{E(s[1])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in s[2]) + g + '</section>'
    w = a['word']
    # 2026-09-26 わたるさん指摘（CAFEMILL「入場料のある本屋」が右の判子からはみ出す）：全角は2文字ぶんで数える
    import unicodedata as _ud
    _tw = sum(2 if _ud.east_asian_width(ch) in 'WF' else 1 for ch in w['term'])
    long = ' long' if _tw > 6 else ''
    wide = ' wide' if _tw > 10 else ''
    ctx = (f'<aside class="ctx ctx-h{wide}" id="context"><div class="hanko{long}"><b>{E(w["term"])}</b><small>{E(w["yomi"])}</small></div>'
           f'<p class="lab">キーワード</p><h2>{E(w["title"])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in w['body']) + '</aside>')
    def crv(k, v):
        if k == '出典URL': return f'<a class="offl" href="{E(v)}" target="_blank" rel="noopener">{E(host)} &#8599;</a>'
        # 2026-09-26 わたるさん「会社名にもちゃんと企業URLでリンクさせる。出典はそのまま」
        if k in _NAMEK and _off: return _lk(v)
        return E(v)
    cr = ''.join(f'<div><span>{E(k)}</span><b>{crv(k, _unconf(v) if k != "出典URL" else v)}</b></div>' for k, v in a['credits'] if k == '出典URL' or _unconf(v))
    # 2026-09-27 わたるさん「施設詳細ページの一番下に、店舗URLと住所（押すとGoogleマップ）と最寄駅を」。データは seo_<brand>.py の PLACE
    _pl = globals().get('PLACE', {}).get(a['slug'])
    shop = ''
    if _pl:
        from urllib.parse import quote as _qq
        _rows = [('名称', f'<a class="offl" href="{E(_off)}" target="_blank" rel="noopener">{E(a["company"])} &#8599;</a>' if _off else E(a['company']))]
        _adr = _pl.get('streetAddress', '')
        if _adr: _rows.append(('住所', f'<a class="offl" href="https://www.google.com/maps/search/?api=1&amp;query={_qq(_adr + " " + a["company"])}" target="_blank" rel="noopener">{E(_adr)} &#8599;</a>'))
        if _pl.get('station'): _rows.append(('最寄駅', E(_pl['station'])))
        if _pl.get('openingHours'): _rows.append(('営業時間', E(_pl['openingHours'])))
        if _off: _rows.append(('公式サイト', f'<a class="offl" href="{E(_off)}" target="_blank" rel="noopener">{E(re.sub(r"^https?://(www[.])?", "", _off).rstrip("/"))} &#8599;</a>'))
        _lab = '店舗情報' if KIND_WORD == '店' else '施設情報'
        shop = f'<section class="shopinfo" id="shopinfo"><h2>{_lab}</h2><dl>' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in _rows) + '</dl></section>'
    # 2026-09-26 「掲載 2026年9月25日」は出さない（オフィスの完成日と誤解されるため）
    heroimg = fig(a, a['hero'][0], a['hero'][1], 'hero-ph')
    edc = '<aside class="edc" id="editor"><p class="lab">編集部より</p>' + ''.join(f'<p>{E(x)}</p>' for x in ED[a['slug']]) + '<p class="sig">COWORKMILL 編集部</p></aside>'
    return (head(meta_title(a), meta_desc(a), p, f'spaces/{a["slug"]}.html', purl(a, a['hero'][0]), 'article') + nav(p, 'spaces') + '\n<main class="wrap">\n'
            f'<div class="crumb">コワーキング › {E(a["city"])} › {E(a["company"].upper())}</div>\n'
            f'<div class="head"><p class="tag" style="color:var(--mute)">{E(tagline(a))}</p>\n<h1>{T(a["title"])}</h1>\n<p class="std">{E(a["lead"])}</p>\n<div class="facts">{facts}</div></div>\n'
            f'<div class="hero">{heroimg}</div>\n<div class="body">\n<nav class="toc"><p>目次</p><ol>{toc}</ol>'
            f'<a class="omv" href="https://offml.com/?utm_source=coworkmill&amp;utm_medium=banner" rel="noopener"><img src="{OMB160}" width="160" height="600" alt="OFFICEMILL"></a></nav>\n'
            f'<article>\n{body}\n{ctx}\n{edc}\n<div class="credits" id="credits">{cr}</div>\n{shop}\n</article></div>\n'
            f'<a class="omb omb-728x90" href="https://offml.com/?utm_source=coworkmill&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a>\n'
            '</main>' + foot(p) + '</body></html>')

for a in A:
    open(OUT + f'spaces/{a["slug"]}.html', 'w', encoding='utf-8').write(article(a))

# ---- 特集カード（WALL の .cc と同じ） ----
# 特集タイトルの最後に施設数で「〇選」（2026-09-26 わたるさん）。施設数が増えれば自動で変わる
for _c in COLLECTIONS:
    _c['title'] = re.sub(r'\d+選$', '', _c['title']) + f'{len(_c["items"])}選'
def cc(c, p):
    imgs = [purl(A_by[s], A_by[s]['hero'][0]) for s, _ in c['items']]
    imgs = [u for u in imgs if u]
    main_i = f'<img src="{E(imgs[0])}" alt="" loading="lazy">' if imgs else ''
    sub = ''.join(f'<img src="{E(u)}" alt="" loading="lazy">' for u in imgs[1:4])
    return (f'<a class="cc" href="{p}collections/{c["slug"]}.html">{main_i}<div class="ccm">{sub}</div>'
            f'<h3>{E(c["title"])}</h3><p class="ccs">{E(c["lead"])}</p></a>')

# ---- トップ（WALL index.html と同じ並び） ----
p = ''
slides = ''
for k, s in enumerate([a['slug'] for a in A[:6]]):
    a = A_by[s]; u = purl(a, a['hero'][0])
    on = k == 0
    slides += (f'<div class="hs{" on" if on else ""}" aria-hidden="{"false" if on else "true"}"><a class="hsimg" href="spaces/{s}.html" tabindex="-1"><img class="ph" src="{E(u)}" alt="{E(a["company"])} のオフィス"{"" if on else LAZY}></a>'
               f'<div class="cap"><p class="tag">{E(tagline(a))}</p><h1><a href="spaces/{s}.html">{T(a["title"])}</a></h1><p class="std">{E(a["lead"])}</p><a class="ctx-tag" href="spaces/{s}.html">続きを読む →</a></div></div>')
dots = ''.join(f'<button type="button" aria-label="スライド {i+1}"{ON if i == 0 else ""}></button>' for i in range(6))
# 2026-09-26 わたるさん「トップ画像、WALLみたいにランダムで表示するようにして」
# WALL と同じ方式：HTMLには固定の6社を入れておき（JSが動かないとき用）、開くたびに全社から6社をランダムに選んで差し替える
_pool = [dict(s=a['slug'], img=purl(a, a['hero'][0]), alt=a['company'] + ' のオフィス', tag=tagline(a), h=T(a['title']), std=a['lead']) for a in A if purl(a, a['hero'][0])]
HERO_JS = ('<script>var OS_HERO=' + json.dumps(_pool, ensure_ascii=False).replace('</', '<\\/') + ';'
 '(function(){var r=document.querySelector(".hslider");if(!r)return;try{var P=OS_HERO.slice(),S=r.querySelectorAll(".hs");'
 'for(var k=0;k<S.length&&k<P.length;k++){var j=k+Math.floor(Math.random()*(P.length-k));var t=P[k];P[k]=P[j];P[j]=t;var d=P[k],e=S[k],u="spaces/"+d.s+".html";'
 'var im=e.querySelector("img");im.src=d.img;im.alt=d.alt;e.querySelector(".hsimg").href=u;e.querySelector(".tag").textContent=d.tag;'
 'var h=e.querySelector("h1 a");h.href=u;h.innerHTML=d.h;e.querySelector(".std").textContent=d.std;e.querySelector(".ctx-tag").href=u;}}catch(x){}})();</script>')
POPULAR = [a['slug'] for a in A]
_bs = {a['slug']: a for a in A}
POP = [_bs[x] for x in POPULAR if x in _bs] + [a for a in A if a['slug'] not in POPULAR]
POPRANK = {a['slug']: i + 1 for i, a in enumerate(POP)}
SLIDER_JS = open(W + 'index.html', encoding='utf-8').read().split('</footer>')[1].replace('</body></html>', '')
top = (head(INDEX_TITLE, INDEX_DESC, p, 'index.html') + nav(p) + '\n<main class="wrap">\n'
       f'<section class="hero hslider" aria-roledescription="carousel">{slides}<div class="hdots">{dots}</div></section>{HERO_JS}\n\n'
       '<form class="tsearch" action="spaces/index.html" method="get" role="search"><input type="search" name="q" placeholder="施設名・街・キーワードで探す" aria-label="コワーキングスペースを探す"><button type="submit">検索</button></form>\n'
       f'<section class="sec"><div class="sec-h"><h2>新着記事</h2><span class="sub">エントランスから順に、1施設ずつご案内</span><a class="more" href="spaces/index.html">一覧へ →</a></div>\n'
       f'<div class="cards">{"".join(card(a, p) for a in A[:12])}</div><div class="viewall"><a href="spaces/index.html">コワーキングスペース一覧を見る <span>→</span></a></div></section>\n\n'
       f'<section class="sec"><div class="sec-h"><h2>人気のコワーキング</h2><span class="sub">いま多く読まれている12施設</span><a class="more" href="spaces/index.html?sort=pop">一覧へ →</a></div>\n'
       f'<div class="cards">{"".join(card(a, p, False, i + 1) for i, a in enumerate(POP[:12]))}</div><div class="viewall"><a href="spaces/index.html?sort=pop">人気順で一覧を見る <span>→</span></a></div></section>\n\n'
       f'<section class="sec"><div class="sec-h"><h2>特集</h2><span class="sub">テーマ別に、国を越えて見比べる</span><a class="more" href="collections/index.html">一覧へ →</a></div>\n'
       f'<div class="ccg">{"".join(cc(c, p) for c in COLLECTIONS[:6])}</div><div class="viewall"><a href="collections/index.html">特集一覧を見る <span>&rarr;</span></a></div></section>\n\n'
       f'<a class="omb omb-728x90" href="https://offml.com/?utm_source=coworkmill&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a>\n\n'
       # 設計・施工パートナー欄は、掲載できる会社がそろうまで非表示（2026-09-25）
       '</main>' + foot(p) + SLIDER_JS + '</body></html>')
open(OUT + 'index.html', 'w', encoding='utf-8').write(top)

# ---- コワーキングスペース一覧 ----
# 絞り込み用の軸（2026-09-26 わたるさん：「何百施設になるつもりで、各施設での絞り込みを」）。build_mill.py が AREA_OF / F2 を差し替える
def AREA_OF(a):
    return a['city'].split('（')[0]
    m = re.search(r'（(.+?)）', a['city']); k = m.group(1) if m else city_short(a)
    return {'アメリカ':'米国','イギリス':'英国','UK':'英国','USA':'米国','ドイツ連邦':'ドイツ'}.get(k, k)
F2_LABEL = globals().get('F2_LABEL', '業種')
F2_OF = globals().get('F2_OF', lambda a: [a['industry']])
def _qtext(a):
    kn = KANA.get(a['slug'], '')
    return ' '.join([a['company'], kn, a['city'], a['industry'], a['card'], a['word']['term'], a['word']['yomi'], AREA_OF(a)] + F2_OF(a)).lower()
_AZ = {a['slug']: i for i, a in enumerate(sorted(A, key=lambda x: (KANA.get(x['slug']) or x['company']).lower()))}
def lcard(i, a):
    r = POPRANK[a['slug']]
    return card(a, '../', False, r if r <= 12 else None, f' data-new="{i}" data-pop="{r}" data-az="{_AZ[a["slug"]]}" data-a="{E(AREA_OF(a))}" data-f2="{E("|".join(F2_OF(a)))}" data-q="{E(_qtext(a))}"')
def fbar(items, kind_word, ph):
    import collections
    ac = collections.Counter(AREA_OF(a) for a in items)
    chips = f'<button type="button" data-a="" class="on">すべて<small>{len(items)}</small></button>' + ''.join(f'<button type="button" data-a="{E(k)}">{E(k)}<small>{n}</small></button>' for k, n in sorted(ac.items(), key=lambda kv: (-kv[1], kv[0])))
    f2 = sorted({v for a in items for v in F2_OF(a)})
    sel2 = f'<select id="ff2" aria-label="{E(F2_LABEL)}"><option value="">すべての{E(F2_LABEL)}</option>' + ''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in f2) + '</select>'
    return (f'<div class="fbar"><label class="srch"><input type="search" id="fq" placeholder="{E(ph)}" autocomplete="off"></label>'
            f'<div class="chips" id="fchips" role="group" aria-label="地域">{chips}</div>'
            f'<div class="fsel">{sel2}<select id="fsort" aria-label="並び替え"><option value="new">新着順</option><option value="pop">人気順</option><option value="az">名前順</option></select>'
            f'<span class="cnt"><b id="fcnt">{len(items)}</b>{kind_word}</span></div></div><p class="fnone" id="fnone" hidden>条件に合う{kind_word if kind_word != "社" else "会社"}がありません。</p>')
FILTER_JS = """<script>(function(){var l=document.getElementById('olist');if(!l)return;var q=document.getElementById('fq'),ch=document.getElementById('fchips'),f2=document.getElementById('ff2'),so=document.getElementById('fsort'),cn=document.getElementById('fcnt'),no=document.getElementById('fnone');
var st={a:'',f2:'',s:'new',q:''};
function norm(x){return (x||'').toLowerCase().replace(/[\s\u3000]+/g,' ').trim();}
function apply(push){var cs=[].slice.call(l.children),n=0,qs=norm(st.q).split(' ').filter(Boolean);
cs.sort(function(a,b){return a.getAttribute('data-'+st.s)-b.getAttribute('data-'+st.s);});
cs.forEach(function(c){var ok=(!st.a||c.getAttribute('data-a')===st.a)&&(!st.f2||('|'+c.getAttribute('data-f2')+'|').indexOf('|'+st.f2+'|')>=0);
if(ok&&qs.length){var t=c.getAttribute('data-q')||'';ok=qs.every(function(w){return t.indexOf(w)>=0;});}
c.hidden=!ok;if(ok)n++;l.appendChild(c);});
l.classList.toggle('bynew',st.s==='new');cn.textContent=n;no.hidden=n>0;
[].forEach.call(ch.children,function(b){b.classList.toggle('on',b.getAttribute('data-a')===st.a);});
if(push){try{var u=new URLSearchParams();if(st.a)u.set('area',st.a);if(st.f2)u.set('f',st.f2);if(st.s!=='new')u.set('sort',st.s);if(st.q)u.set('q',st.q);var qs2=u.toString();history.replaceState(null,'',qs2?'?'+qs2:location.pathname);}catch(e){}}}
ch.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;st.a=b.getAttribute('data-a');apply(true);});
f2.addEventListener('change',function(){st.f2=f2.value;apply(true);});so.addEventListener('change',function(){st.s=so.value;apply(true);});
q.addEventListener('input',function(){st.q=q.value;apply(true);});
try{var u=new URLSearchParams(location.search);st.a=u.get('area')||'';st.f2=u.get('f')||'';st.s=u.get('sort')||'new';st.q=u.get('q')||'';
if(!/^(new|pop|az)$/.test(st.s))st.s='new';f2.value=st.f2;so.value=st.s;q.value=st.q;}catch(e){}
apply(false);})();</script>"""
SORT_JS = FILTER_JS
p = '../'
lst = (head(LIST_TITLE + ' | ' + SITE_NAME, LIST_DESC, p, 'spaces/index.html') + nav(p, 'spaces') + '\n<main class="wrap"><div class="coll"><h1>コワーキングスペース一覧</h1><p class="lead">内装デザインが最も優れたコワーキングを、エントランスから順に1施設ずつご案内しています。</p></div>\n'
       f'<section class="sec">' + fbar(A, '社', '施設名・街・キーワードで探す') +
       f'<div class="cards bynew" id="olist">{"".join(lcard(i, a) for i, a in enumerate(A))}</div></section>\n' + SORT_JS +
       f'<a class="omb omb-728x90" href="https://offml.com/" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot(p) + '</body></html>')
open(OUT + 'spaces/index.html', 'w', encoding='utf-8').write(lst)

# ---- 特集 ----
col = (head('コワーキングスペース特集｜テーマ別に施設を見比べる | COWORKMILL', '丸の内・虎ノ門・渋谷などの街、駅直結、24時間、広さ、つくった会社。日本のコワーキングスペースをテーマ別に見比べる特集。', p, 'collections/index.html') + nav(p, 'collections') + '\n<main class="wrap"><div class="coll"><h1>特集</h1><p class="lead">街、駅からの近さ、使える時間、広さ。コワーキングスペースを、共通のテーマで見比べる特集です。</p>'
       f'<div class="ccg">{"".join(cc(c, p) for c in COLLECTIONS)}</div></div></main>' + foot(p) + '</body></html>')
open(OUT + 'collections/index.html', 'w', encoding='utf-8').write(col)
for c in COLLECTIONS:
    secs = ''
    for i, (s, q) in enumerate(c['items']):
        a = A_by[s]
        secs += (f'<section class="step" id="s{i+1}"><p class="no">{i+1:02d}｜{E(a["company"])}（{E(city_short(a))}）</p><h2>{E(q)}</h2>' + fig(a, a['hero'][0], a['hero'][1]) +
                 f'<p>{E(a["lead"])}</p><p><a class="ctx-tag" href="../spaces/{s}.html">続きを読む →</a></p></section>')
    pg = (head(f'{c["title"]}｜コワーキングスペース特集 | COWORKMILL', c['lead'] + '（' + '・'.join(A_by[x[0]]['company'] for x in c['items']) + '）', p, f'collections/{c["slug"]}.html', purl(A_by[c['items'][0][0]], A_by[c['items'][0][0]]['hero'][0]), 'article') + nav(p, 'collections', '特集｜テーマ別に見比べる') + '\n<main class="wrap">\n'
          f'<div class="crumb">特集 › {E(c["title"])}</div><div class="head"><p class="tag" style="color:var(--mute)">特集</p><h1>{E(c["title"])}</h1><p class="std">{E(c["lead"])}</p></div>\n'
          f'<div class="body"><nav class="toc"><p>登場する会社</p><ol>{toc_items([x[0] for x in c["items"]])}</ol></nav><article>{secs}</article></div>\n'
          f'<a class="omb omb-728x90" href="https://offml.com/" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot(p) + '</body></html>')
    open(OUT + f'collections/{c["slug"]}.html', 'w', encoding='utf-8').write(pg)

# ---- Q&A（2026-09-26 わたるさん「WALL みたいに Q&A のトップを考えろ」→ WALL と同じ型に）
#   questions/index.html = 質問の一覧。questions/<slug>.html = 1問1ページ
#   （短い答え → 根拠になる施設の写真と本文 → キーワード → 登場する施設のカード → ほかの質問）
#   データは questions.py（COWORKMILL）／questions_<brand>.py（MILL）の QUESTIONS。無ければ従来の QA 1問で作る
if 'QUESTIONS' not in globals():
    if os.path.exists('questions.py'):
        exec(open('questions.py', encoding='utf-8').read())
    else:
        QUESTIONS = [dict(slug=QA['slug'], q=QA['q'], a=QA['a'], desc=QA['a'],
                          secs=[(s_, h_, [t_], [(s_, A_by[s_]['hero'][0])]) for s_, h_, t_ in QA['secs']],
                          ctx=None, items=[x[0] for x in QA['secs']])]
_QSEC = SEC_NAME if 'SEC_NAME' in globals() else 'spaces'
def _qcap(slug, n):
    a = A_by[slug]
    if str(a['hero'][0]) == str(n): return a['hero'][1]
    for st in a['steps']:
        for m, c in st[3]:
            if str(m) == str(n): return c
    return a['company']
def question_page(q, others):
    p = '../'
    hs, hn = q['secs'][0][3][0]
    heroimg = fig(A_by[hs], hn, _qcap(hs, hn), 'hero-ph')
    toc = ''.join(f'<li><a href="#s{i+1}">{E(h)}</a></li>' for i, (_, h, _, _) in enumerate(q['secs'])) + ('<li><a href="#context">キーワード</a></li>' if q.get('ctx') else '')
    body = ''
    for i, (sl, h, paras, phs) in enumerate(q['secs']):
        figs = [fig(A_by[a_], n_, _qcap(a_, n_)) for a_, n_ in phs]
        figs = [f for f in figs if f]
        ph = ''.join(figs)
        if len(figs) == 2: ph = f'<div class="two">{ph}</div>'
        elif len(figs) > 2: ph = f'<div class="grid3">{ph}</div>'
        body += (f'<section class="step" id="s{i+1}"><p class="no">{i+1:02d}｜{E(A_by[sl]["company"])}（{E(city_short(A_by[sl]))}）</p><h2>{E(h)}</h2>'
                 + ''.join(f'<p>{E(x)}</p>' for x in paras) + ph + f'<p><a class="ctx-tag" href="../{_QSEC}/{sl}.html">続きを読む →</a></p></section>')
    ctx = ''
    if q.get('ctx'):
        w = q['ctx']
        import unicodedata as _ud
        _tw = sum(2 if _ud.east_asian_width(ch) in 'WF' else 1 for ch in w['term'])
        ctx = (f'<aside class="ctx ctx-h{" wide" if _tw > 10 else ""}" id="context"><div class="hanko{" long" if _tw > 6 else ""}"><b>{E(w["term"])}</b><small>{E(w["yomi"])}</small></div>'
               f'<p class="lab">キーワード</p><h2>{E(w["title"])}</h2>' + ''.join(f'<p>{E(x)}</p>' for x in w['body']) + '</aside>')
    cards = '<section class="step"><p class="no">この答えに出てくる' + KIND_WORD + '</p><h2>1つずつ見る</h2></section><div class="cards">' + ''.join(card(A_by[x], p, False) for x in q['items'] if x in A_by) + '</div>'
    more = ('<section class="step"><p class="no">ほかの質問</p><h2>よく読まれている質問</h2><ul class="qmore">' + ''.join(f'<li><a href="{o["slug"]}.html">{E(o["q"])}</a></li>' for o in others) + '</ul></section>') if others else ''
    return (head(q['q'] + ' | ' + SITE_NAME, q.get('desc') or q['a'], p, f'questions/{q["slug"]}.html', purl(A_by[hs], hn), 'article') + nav(p, 'questions') +
            f'\n<main class="wrap"><div class="crumb"><a href="index.html">Q&amp;A</a> › {E(q["q"])}</div>'
            f'<div class="head"><p class="tag" style="color:var(--mute)">Q&amp;A</p><h1>{E(q["q"])}</h1><p class="std"><b>{E(q["a"])}</b></p></div>'
            f'<div class="hero">{heroimg}</div>'
            f'<div class="body"><nav class="toc"><p>目次</p><ol>{toc}</ol>'
            f'<a class="omv" href="https://offml.com/?utm_source={UTM}&amp;utm_medium=banner" rel="noopener"><img src="{OMB160}" width="160" height="600" alt="OFFICEMILL" loading="lazy"></a></nav>'
            f'<article>{body}{ctx}{cards}{more}</article></div>'
            f'<a class="omb omb-728x90" href="https://offml.com/?utm_source={UTM}&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot(p) + '</body></html>')
KIND_WORD = globals().get('KIND_WORD', '会社')
SITE_NAME = globals().get('SITE_NAME', 'COWORKMILL')
UTM = globals().get('UTM', 'offisnap')
for _i, _q in enumerate(QUESTIONS):
    _others = [o for o in QUESTIONS if o['slug'] != _q['slug']][:4]
    open(OUT + f'questions/{_q["slug"]}.html', 'w', encoding='utf-8').write(question_page(_q, _others))
def _qphotos(q):
    seen, out = set(), []
    for sl, _, _, phs in q['secs']:
        for a_, n_ in phs:
            u = purl(A_by[a_], n_) if a_ in A_by else None
            if u and u not in seen:
                seen.add(u); out.append((u, A_by[a_]['company']))
            if len(out) == 3: return out
    return out
def _qcard(q):
    ph = _qphotos(q)
    while len(ph) < 3 and ph: ph.append(ph[0])
    imgs = ''.join(f'<img src="{u}" alt="{E(c)}" loading="lazy">' for u, c in ph)
    return f'<li><a href="{q["slug"]}.html">{imgs}<span class="qq">Q</span><span class="qc"><b>{E(q["q"])}</b><span>{E(q["a"])[:70]}…</span></span></a></li>'
_qlist = ''.join(_qcard(q) for q in QUESTIONS)
QA_TITLE = globals().get('QA_TITLE', 'コワーキングスペースの Q&A')
QA_LEAD = globals().get('QA_LEAD', '内装デザインが最も優れたコワーキングについて、よく聞かれる質問に短く答えます。答えはすべて、掲載している会社の公式情報から書いています。')
qa = (head(QA_TITLE + ' | ' + SITE_NAME, QA_LEAD, '../', 'questions/index.html') + nav('../', 'questions') +
      f'\n<main class="wrap"><div class="page"><div class="head"><p class="tag" style="color:var(--mute)">Q&amp;A</p><h1>{E(QA_TITLE)}</h1><p class="std">{E(QA_LEAD)}</p></div>'
      f'</div><ul class="qidx">{_qlist}</ul>'
      f'<a class="omb omb-728x90" href="https://offml.com/?utm_source={UTM}&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot('../') + '</body></html>')
open(OUT + 'questions/index.html', 'w', encoding='utf-8').write(qa)
QA = dict(q=QA_TITLE, a=QA_LEAD)

ab = (head('COWORKMILL について', '内装デザインが最も優れたコワーキングを紹介するメディア、COWORKMILL について。', p, 'about/index.html') + nav(p, 'about') + '\n<main class="wrap"><div class="head"><p class="tag" style="color:var(--mute)">About</p><h1>COWORKMILL について</h1>'
      '<p class="std">内装デザインが最も優れたコワーキングを紹介するメディアです。1施設ごとに、受付から執務エリア、会議室、ラウンジへと、初めて訪れた人が歩く順番で紹介します。</p></div>'
      '<div class="body"><nav class="toc"><p>目次</p><ol><li><a href="#s1">編集方針</a></li></ol></nav><article>'
      '<section class="step" id="s1"><p class="no">01｜編集方針</p><h2>受付から順に、歩くように</h2><p>内装デザインが最も優れたコワーキングを、初めて訪れた人が歩く順番でご案内します。写真と事実は各施設の公式発表にもとづき、編集部の見立ては「編集部より」に分けて書いています。</p></section>'
      '</article></div></main>' + foot(p) + '</body></html>')
open(OUT + 'about/index.html', 'w', encoding='utf-8').write(ab)
print('ok', sorted(os.listdir(OUT + 'spaces')))
# ---- プライバシーポリシー・利用規約・お問い合わせ（WALL の about/privacy・terms・contact と同じ型。2026-09-25） ----
os.makedirs(OUT + 'contact', exist_ok=True)
UPD = '2026年9月25日'
privacy = (head('プライバシーポリシー | COWORKMILL', 'COWORKMILL のプライバシーポリシー。', p, 'about/privacy.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page legal"><h1>プライバシーポリシー</h1><p class="upd">最終更新：{UPD}</p>
<p>COWORKMILL（以下「当サイト」）が、cowkml.com の利用にあたって個人情報をどう扱うかを説明します。</p>
<h2>1. 集める情報</h2>
<p><b>お問い合わせでいただく情報。</b>お問い合わせフォームからは、用件、お名前、メールアドレス、会社名（任意）、本文を受け取ります。</p>
<p><b>技術的な情報。</b>ほかの多くのサイトと同じく、サイトを安全に運営するため、ホスティング事業者が IP アドレス、ブラウザの種類、閲覧したページ、アクセス時刻などを自動で記録します。</p>
<p><b>アクセス解析と Cookie。</b>当サイトは、閲覧状況を知るために Google アナリティクス（Google LLC）を使っています。Google アナリティクスは Cookie を使い、閲覧したページや滞在時間などを個人を特定しない形で集めます。IP アドレスは匿名化して送ります。集め方と使い方は <a href="https://policies.google.com/technologies/partner-sites?hl=ja" target="_blank" rel="noopener">Google のポリシー</a>をご覧ください。ブラウザの設定や <a href="https://tools.google.com/dlpage/gaoptout?hl=ja" target="_blank" rel="noopener">オプトアウト アドオン</a>で止められます。広告のための Cookie は使っていません。</p>
<h2>2. 使いみち</h2>
<ul><li>お問い合わせへの返信</li><li>サイトの運営、安全の確保、改善</li><li>法令で求められる対応</li></ul>
<p>個人情報を売ることはありません。上の目的以外に使うときは、事前に同意をいただきます。</p>
<h2>3. 利用しているサービス</h2>
<p>サイトの運営のため、次の事業者を利用しています。情報が日本の外で処理されることがあります。</p>
<ul><li><b>Vercel</b> — サイトの配信</li><li><b>Google Fonts</b> — 書体（ブラウザが Google に接続します）</li><li><b>Google アナリティクス</b> — アクセス解析</li></ul>
<h2>4. 保存する期間</h2>
<p>お問い合わせの内容は、対応と記録に必要な期間だけ保存し、その後削除します。</p>
<h2>5. 開示・訂正・削除</h2>
<p>お送りいただいた個人情報の開示、訂正、削除、利用の停止は、<a href="../contact/index.html">お問い合わせ</a>からご連絡ください。個人情報保護法に沿って、合理的な期間内に対応します。</p>
<h2>6. 安全管理</h2>
<p>受け取った情報を守るため、合理的な対策をとります。ただし、インターネット上の通信が完全に安全であることは保証できません。</p>
<h2>7. 変更</h2>
<p>このポリシーは変更することがあります。最新版は日付とともにこのページに掲載します。</p>
<h2>8. お問い合わせ</h2>
<p>このポリシーについてのご質問は、<a href="../contact/index.html">お問い合わせ</a>からお願いします。</p>
</div></main>''' + foot(p) + '</body></html>')
open(OUT + 'about/privacy.html', 'w', encoding='utf-8').write(privacy)
terms = (head('利用規約 | COWORKMILL', 'COWORKMILL の利用規約。', p, 'about/terms.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page legal"><h1>利用規約</h1><p class="upd">最終更新：{UPD}</p>
<p>この規約は、COWORKMILL（以下「当サイト」）が運営する cowkml.com の利用に適用されます。当サイトを利用した時点で、この規約に同意したものとします。</p>
<h2>1. 記事の内容</h2>
<p>記事は、掲載施設が公開している公式サイト・公式ニュースの情報をもとに、COWORKMILL 編集部が書いています。正確さに努めますが、オフィスや会社、設計者に関する情報は掲載後に変わることがあり、現状のまま提供します。</p>
<h2>2. 知的財産</h2>
<p>文章、レイアウト、ロゴは COWORKMILL に帰属します。写真は、クレジットに記した各施設・設計者・写真家に帰属し、各社が公開している素材を出典を明記して使っています。権利者の許可なく、複製、転載、商用利用はできません。出典と元記事へのリンクを明記した短い引用は歓迎します。</p>
<h2>3. 掲載施設からのご要望</h2>
<p>掲載施設、写真の権利者から、写真や記事の修正・取り下げのご要望があった場合は、すみやかに対応します。<a href="../contact/index.html">お問い合わせ</a>からご連絡ください。</p>
<h2>4. 禁止事項</h2>
<ul><li>法令または他者の権利に反する行為</li><li>自動化された大量アクセスや不正アクセスなど、サイトの運営を妨げる行為</li><li>お問い合わせを通じた虚偽の情報、迷惑行為、有害な内容の送信</li><li>COWORKMILL や掲載施設との関係を偽ること</li></ul>
<h2>5. リンク</h2>
<p>当サイトには、バナーを含め、外部サイトへのリンクがあります。リンク先の内容については責任を負いません。</p>
<h2>6. 免責</h2>
<p>法令で認められる範囲で、当サイトの利用や記事の内容によって生じた損害について責任を負いません。当サイトの内容は、オフィスの計画・賃貸・工事についての専門的な助言ではありません。</p>
<h2>7. 変更・停止</h2>
<p>当サイトやこの規約は、いつでも変更・停止・終了することがあります。変更は、このページに掲載した時点で効力を持ちます。</p>
<h2>8. 準拠法・裁判所</h2>
<p>この規約は日本法に準拠します。当サイトに関する紛争は、東京地方裁判所を第一審の専属的合意管轄裁判所とします。</p>
<h2>9. お問い合わせ</h2>
<p>この規約についてのご質問は、<a href="../contact/index.html">お問い合わせ</a>からお願いします。</p>
</div></main>''' + foot(p) + '</body></html>')
open(OUT + 'about/terms.html', 'w', encoding='utf-8').write(terms)
FORMSPREE_ID = ''  # （使っていない。2026-09-26 から福利厚生JPと同じ FormSubmit の送信先を使う）
FORMSUBMIT = 'https://formsubmit.co/d649df9aee3824d19c00adf93c140681'  # 福利厚生JP contact.astro と同じ送信先（わたるさんのメール宛）
_act = FORMSUBMIT; FORMSPREE_ID = 'formsubmit'
_dis = '' if FORMSPREE_ID else ' disabled'
contact = (head('お問い合わせ | COWORKMILL', 'COWORKMILL 編集部へのお問い合わせ。掲載についてのご要望、取材・提携のご相談。', p, 'contact/index.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page"><h1>お問い合わせ</h1>
<p class="lead">掲載についてのご要望、取材や提携のご相談、記事の誤りのご指摘など、お気軽にお知らせください。1週間以内に返信します。</p>
<form class="cform" action="{_act}" method="POST">
<label>用件<select name="topic" id="topic" required><option value="listing">掲載のご相談（コワーキングを紹介してほしい）</option><option value="content">掲載内容・写真についてのご要望</option><option value="partner">提携・広告のご相談</option><option value="media">取材・メディア</option><option value="other">その他</option></select></label>
<div class="row2"><label>お名前<input name="name" autocomplete="name" required></label><label>メールアドレス<input type="email" name="email" autocomplete="email" required></label></div>
<label><b class="lt">会社名 <span>（任意）</span></b><input name="company" autocomplete="organization"></label>
<div class="lst" id="listing-note" hidden><p><b>掲載のご相談は、次の3つをお書きください。</b></p><ol><li>運営会社名と、紹介してほしいコワーキングの場所</li><li>コワーキングの写真（Googleドライブなどの共有URL、または写真が載っている公式ページのURL）</li><li>コワーキングのことが分かる資料やページのURL（プレスリリース、設計事務所のページなど）</li></ol><p>写真と情報は公式のものだけを使い、出典を明記して紹介します。内容を確認のうえ、掲載の可否を返信します。</p></div>
<label>本文<textarea name="message" rows="7" required placeholder="掲載のご相談の場合は、運営会社名・コワーキングの場所・写真のURL・資料のURLをお書きください"></textarea></label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="_next" value="{SITE}/contact/thanks.html">
<input type="hidden" name="_subject" value="COWORKMILL お問い合わせ"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table">
<p class="note">送信により、<a href="../about/privacy.html" style="border-bottom:1px solid var(--accent)">プライバシーポリシー</a>に同意したものとします。{'' if FORMSPREE_ID else 'フォームは準備中です。'}</p>
<button type="submit"{_dis}>送信する →</button>
</form>
<script>(function(){{var sel=document.getElementById('topic'),nt=document.getElementById('listing-note');function u(){{nt.hidden=sel.value!=='listing';}}try{{var t=new URLSearchParams(location.search).get('topic');if(t)sel.value=t;}}catch(e){{}}sel.addEventListener('change',u);u();}})();</script>
</div></main>''' + foot(p) + '</body></html>')
open(OUT + 'contact/index.html', 'w', encoding='utf-8').write(contact)
thanks = (head('送信しました | ' + globals().get('SITE_NAME', 'COWORKMILL'), 'お問い合わせを受け付けました。', p, 'contact/thanks.html') + nav(p, 'about') +
          '\n<main class="wrap"><div class="page"><h1>送信しました</h1><p class="lead">お問い合わせを受け付けました。内容を確認のうえ、1週間以内に返信します。</p>'
          f'<p><a class="ctx-tag" href="{p}index.html">トップへ戻る →</a></p></div></main>' + foot(p) + '</body></html>')
open(OUT + 'contact/thanks.html', 'w', encoding='utf-8').write(thanks)

# ---- sitemap / robots / vercel（公開用） ----
import datetime
_today = datetime.date.today().isoformat()
_paths = ['', 'spaces/index.html', 'collections/index.html', 'questions/index.html', 'about/index.html', 'about/privacy.html', 'about/terms.html', 'contact/index.html'] + [f'spaces/{a["slug"]}.html' for a in A] + [f'collections/{c["slug"]}.html' for c in COLLECTIONS] + [f'questions/{q["slug"]}.html' for q in QUESTIONS]
open(OUT + 'sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}/{x}</loc><lastmod>{_today}</lastmod></url>\n' for x in _paths) + '</urlset>\n')
open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
# 2026-09-27 わたるさん「URLの末尾に index.html がつくのが嫌」→ 古い …/index.html は …/ へ転送する
open(OUT + 'vercel.json', 'w').write(json.dumps({"redirects": [{"source": "/index.html", "destination": "/", "permanent": True}, {"source": "/:path*/index.html", "destination": "/:path*/", "permanent": True}]}, indent=1) + '\n')

# ---- SEO / AIO（構造化データ・llms.txt・webmanifest）2026-09-25 ----
COUNTRY = dict(COUNTRY20)
ORG = {"@type":"Organization","@id":SITE+"/#org","name":"COWORKMILL","alternateName":"コワークミル","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/favicon-512x512.png","width":512,"height":512},"description":"内装デザインが最も優れたコワーキングを、写真と一緒に日本語で1施設ずつ紹介するメディア。","inLanguage":"ja"}
PUB = '2026-09-25'
def ld_for(path):
    ld = []
    u = SITE + '/' + ('' if path == 'index.html' else path)
    if path == 'index.html':
        ld.append({"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#website","name":"COWORKMILL","alternateName":"コワークミル — 内装デザインが最も優れたコワーキングを厳選紹介","url":SITE+"/","inLanguage":"ja","publisher":{"@id":SITE+"/#org"},"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":SITE+"/spaces/index.html?q={search_term_string}"},"query-input":"required name=search_term_string"}})
        ld.append({"@context":"https://schema.org",**ORG})
        ld.append({"@context":"https://schema.org","@type":"ItemList","name":"新着記事","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/spaces/{a['slug']}.html","name":a['title']} for i, a in enumerate(A)]})
    m = re.match(r'spaces/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        a = A_by[m.group(1)]
        src = next(c[1] for c in a['credits'] if c[0] == '出典URL')
        ld.append({"@context":"https://schema.org","@type":"Article","@id":u+"#article","mainEntityOfPage":u,"headline":a['title'],"description":a['lead'],"image":[purl(a, a['hero'][0])],
                   "datePublished":PUB,"dateModified":PUB,"inLanguage":"ja","author":{"@type":"Organization","name":"COWORKMILL 編集部","url":SITE+"/about/index.html"},"publisher":{"@id":SITE+"/#org"},
                   "about":{"@type":"Place","name":f"{a['company']} のオフィス","address":{"@type":"PostalAddress","addressLocality":city_short(a),"addressCountry":COUNTRY.get(a['slug'],'')}},
                   "mentions":[{"@type":"Organization","name":a['company']}],"citation":src,"keywords":", ".join([a['company'], city_short(a), a['industry'], '施設', a['word']['term']]),
                   "articleSection":"コワーキングスペース","isBasedOn":src})
        _pl = PLACE.get(a["slug"])
        if _pl:
            _d = {"@context":"https://schema.org","@type":"LocalBusiness","@id":u+"#place","name":a["company"],"url":OFFICIAL.get(a["slug"], src),"sameAs":OFFICIAL.get(a["slug"], src),"image":purl(a, a["hero"][0]),"description":a["card"]}
            if KANA.get(a["slug"]): _d["alternateName"] = KANA[a["slug"]]
            _d["address"] = {"@type":"PostalAddress","streetAddress":_pl["streetAddress"],"addressLocality":_pl["addressLocality"],"addressRegion":_pl["addressRegion"],"addressCountry":"JP"}
            if _pl.get("openingHours"): _d["openingHours"] = _pl["openingHours"]
            _d["subjectOf"] = {"@id":u+"#article"}
            ld.append(_d)
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"COWORKMILL","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"コワーキング","item":SITE+"/spaces/index.html"},{"@type":"ListItem","position":3,"name":a['company'],"item":u}]})
    if path == 'spaces/index.html':
        ld.append({"@context":"https://schema.org","@type":"CollectionPage","name":"コワーキングスペース一覧","url":u,"inLanguage":"ja","isPartOf":{"@id":SITE+"/#website"},"hasPart":[{"@type":"Article","url":f"{SITE}/spaces/{a['slug']}.html","headline":a['title']} for a in A]})
    m = re.match(r'collections/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        c = next(x for x in COLLECTIONS if x['slug'] == m.group(1))
        ld.append({"@context":"https://schema.org","@type":"Article","mainEntityOfPage":u,"headline":c['title'],"description":c['lead'],"image":[purl(A_by[c['items'][0][0]], A_by[c['items'][0][0]]['hero'][0])],"datePublished":PUB,"dateModified":PUB,"inLanguage":"ja","author":{"@type":"Organization","name":"COWORKMILL 編集部"},"publisher":{"@id":SITE+"/#org"},"articleSection":"特集","hasPart":[{"@type":"WebPage","url":f"{SITE}/spaces/{sl}.html","name":A_by[sl]['company']} for sl, _ in c['items']]})
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"COWORKMILL","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"特集","item":SITE+"/collections/index.html"},{"@type":"ListItem","position":3,"name":c['title'],"item":u}]})
    if path == 'questions/index.html':
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q_['q'],"acceptedAnswer":{"@type":"Answer","text":q_['a']}} for q_ in QUESTIONS]})
    m = re.match(r'questions/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        q_ = next(x for x in QUESTIONS if x['slug'] == m.group(1))
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q_['q'],"acceptedAnswer":{"@type":"Answer","text":q_['a'] + ' ' + ' '.join(x for _, _, ps, _ in q_['secs'] for x in ps)}}]})
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":SITE_NAME,"item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Q&A","item":SITE+"/questions/index.html"},{"@type":"ListItem","position":3,"name":q_['q'],"item":u}]})
    if path == 'about/index.html':
        ld.append({"@context":"https://schema.org","@type":"AboutPage","name":"COWORKMILL について","url":u,"inLanguage":"ja","about":{"@id":SITE+"/#org"}})
    if path == 'contact/index.html':
        ld.append({"@context":"https://schema.org","@type":"ContactPage","name":"お問い合わせ","url":u,"inLanguage":"ja","about":{"@id":SITE+"/#org"}})
    return ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
for _root, _dirs, _files in os.walk(OUT):
    for _f in _files:
        if not _f.endswith('.html'): continue
        _path = os.path.relpath(os.path.join(_root, _f), OUT).replace(os.sep, '/')
        _h = open(os.path.join(_root, _f), encoding='utf-8').read()
        _h = _h.replace('</head>', ld_for(_path) + '</head>', 1)
        open(os.path.join(_root, _f), 'w', encoding='utf-8').write(_h)
for _old, _new in REDIRECTS.items():
    open(OUT + f'{SEC_NAME}/{_old}.html', 'w', encoding='utf-8').write(f'<!doctype html><meta charset="utf-8"><title>Redirecting</title><meta http-equiv="refresh" content="0;url=/{SEC_NAME}/{_new}.html"><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{SEC_NAME}/{_new}.html">')
open(OUT + 'site.webmanifest', 'w', encoding='utf-8').write(json.dumps({"name":"COWORKMILL — 内装デザインが最も優れたコワーキングを厳選紹介","short_name":"COWORKMILL","description":"内装デザインが最も優れたコワーキングを日本語で紹介","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#3B7DAE","lang":"ja","icons":[{"src":"/favicon-192x192.png","sizes":"192x192","type":"image/png"},{"src":"/favicon-512x512.png","sizes":"512x512","type":"image/png"}]}, ensure_ascii=False))
# llms.txt（AI 向けのサイト案内。WALL と同じ考え方）
_lines = ['# COWORKMILL', '', '> 内装デザインが最も優れたコワーキングを、公式素材をもとに日本語で1施設ずつ紹介するメディア。受付から執務フロア、会議室、食堂へと、初めて訪れた人が歩く順番で案内する。運営: COWORKMILL 編集部（日本）。', '',
          '## 記事（コワーキング）', ''] + [f'- [{a["title"]}]({SITE}/spaces/{a["slug"]}.html): {a["lead"]}' for a in A] + ['', '## 特集', ''] + [f'- [{c["title"]}]({SITE}/collections/{c["slug"]}.html): {c["lead"]}' for c in COLLECTIONS] + \
         ['', '## その他', '', f'- [Q&A]({SITE}/questions/index.html): {QA["q"]}'] + [f'- [{q_["q"]}]({SITE}/questions/{q_["slug"]}.html): {q_["a"]}' for q_ in QUESTIONS] + [ f'- [COWORKMILL について]({SITE}/about/index.html)', f'- [お問い合わせ]({SITE}/contact/index.html)', '', '## 引用について', '', '記事の事実は各施設の公式サイト・公式ニュースが出典。引用の際は記事URLを添えてください。写真の権利は各社・撮影者に帰属します。']
open(OUT + 'llms.txt', 'w', encoding='utf-8').write('\n'.join(_lines) + '\n')

# ---- 2026-09-27 わたるさん「サイトを開くと末尾に index.html がつくのが嫌」----
# 出力したHTML・sitemap・llms.txt のリンクから index.html を外す（…/index.html → …/、index.html → ./）
import re as _re, os as _os
for _root, _ds, _fs in _os.walk(OUT):
    for _f in _fs:
        if not _f.endswith(('.html', '.xml', '.txt', '.json', '.js')) or _f == 'vercel.json': continue
        _p = _os.path.join(_root, _f)
        try: _t = open(_p, encoding='utf-8').read()
        except Exception: continue
        _n = _re.sub(r'(?<=/)index\.html(?=[?#"\'\s)<\]])', '', _t)
        _n = _re.sub(r'(?<=["\'])index\.html(?=[?#"\'])', './', _n)
        if _n != _t: open(_p, 'w', encoding='utf-8').write(_n)
