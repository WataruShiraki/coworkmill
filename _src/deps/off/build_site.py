# OFFISNAP プレビュー：WALL の build.py が出す HTML と style.css をそのまま使い、色・ロゴ・言語だけ変える
import os, re, html, json, shutil
import omfont as o
exec(open('site.py', encoding='utf-8').read())
exec(open('editorial.py', encoding='utf-8').read())

W = os.environ.get('WALL_DIR', '/mnt/user-data/uploads/Downloads/offisnap-preview/_wall/wall-main/')
OUT = os.environ.get('OUT_DIR', '/mnt/user-data/outputs/offisnap-preview/')
shutil.rmtree(OUT, ignore_errors=True)
for d in ['', 'assets', 'offices', 'collections', 'questions', 'about']:
    os.makedirs(OUT + d, exist_ok=True)

def load(name):
    m = {}
    for line in open(f'img/{name}.txt'):
        k, u = line.split(' ', 1); m[k] = u.strip()
    return m

# ---- 写真URL（各社の公式ページのURLをそのまま参照。WALL の preview_data と同じ方式） ----
sp = load('spotify'); am = load('amazon'); dy = load('dyson'); ad = load('adidas'); bl = load('bloomberg')
lg = load('lego'); go = load('google'); bk = load('booking')
SPK = {1:'Arcade',2:'Cafe',3:'Craft',4:'Karaoke',5:'Neon',6:'Ping',7:'R1',8:'R2',9:'R3',10:'Roof',11:'S1',12:'S2',13:'S3',14:'Theater'}
BLK = {1:'mithraeum',2:'pantry',3:'millennium',4:'nook',5:'fish',6:'terminal',7:'tv',8:'meeting',9:'huddle',10:'pods'}
GOK = {1:'aerial',2:'floor2',3:'stair',4:'courtyard',5:'pond',6:'dragon',7:'bay'}
def url(slug, n):
    if slug == 'spotify': return sp[SPK[n]]
    if slug == 'amazon': return am[str(n - 1 if n <= 23 else 25)]
    if slug == 'dyson': return dy[str(n - 1)]
    if slug == 'adidas': return ad[str(n - 1)]
    if slug == 'bloomberg': return bl[BLK[n]]
    if slug == 'google-bay-view': return go[GOK[n]]
    if slug == 'lego': return {6: lg['entrance'], 7: lg['atrium2']}.get(n)
    if slug in IMG20: return IMG20[slug].get(str(n))
    return None

# 2026-09-25 追加の20社（articles20.py）。新しい記事を先頭にして「新着」の順にする
exec(open('articles20.py', encoding='utf-8').read())
A[:0] = A20
# 別チャットで作る30社（articles30.py があれば先頭に足す）
if os.path.exists('articles30.py'):
    exec(open('articles30.py', encoding='utf-8').read())
    A[:0] = A30; IMG20.update(IMG30); KANA20.update(KANA30); COUNTRY20.update(COUNTRY30); ED20.update(ED30)
exec(open('tokushu.py', encoding='utf-8').read())  # 特集14本（2026-09-25）
A_by = {a['slug']: a for a in A}
ED.update(ED20)
# 写真の差し替え・追加（取得できた写真に合わせる）
A_by['lego']['hero'] = (6, '正面入口')
A_by['lego']['steps'][0] = ('01 · 入口', '正面入口と外観', ['公式のメディア素材には、正面入口、外観、上空からの写真がそろっています。'], [])
A_by['lego']['steps'][1] = A_by['lego']['steps'][1][:3] + ([(7, '2階のアトリウム')],)
A_by['dyson']['steps'][4] = A_by['dyson']['steps'][4][:3] + ([(7, 'らせん階段'), (8, 'らせん階段')],)
A_by['dyson']['steps'][2] = A_by['dyson']['steps'][2][:3] + ([(4, 'ワークスペース'), (5, 'アトリウム'), (6, '館内')],)
# トップ画像のルール（2026-09-25 わたるさん）：①ロゴ入りの開放的なエントランス ②自社ビルを引きで ③カラフルできれいなフリースペース
A_by['adidas']['hero'] = (10, '本社の建物と運動場')
A_by['bloomberg']['hero'] = (2, 'グラブ・アンド・ゴーのパントリー')
A_by['bloomberg']['steps'][3] = A_by['bloomberg']['steps'][3][:3] + ([(5, '大きな水槽')],)
A_by['google-bay-view']['hero'] = (5, '池越しに見た Bay View')
A_by['spotify']['hero'] = (7, 'ロゴのある受付')
A_by['nike']['hero'] = (1, 'Nike 本社キャンパス（Skylab Architecture 提供）')
# 2026-09-25 わたるさん：メインは内装を優先（ロゴ入りの受付＞内装＞外観）。日本企業に再現性があるのは内装だから
# 2026-09-25 わたるさん（2回目）：Amazon はスフィアの外観（②建物）、adidas は ARENA のエントランス（①ロゴ入り）。どちらも公式の追加写真
AM_HERO = 'https://assets.aboutamazon.com/f2/e4/6f67188e480392ce0b19a6671b59/spheres-rolling-blog-hero-1.jpg'  # About Amazon「How to tour Seattle offices」
AD_HERO = 'https://res.cloudinary.com/confirmed-web/image/upload/v1706442258/adidas-group/media/pictures-videos/arena_2_k1rzan.jpg'  # adidas Group 報道用画像「The entrance area…136 steps」
# 2026-09-25 わたるさん（3回目）：優先順位は ①ロゴ入りの入口 ②建物 ③カラフルなフリースペース。内装の一場面は使わない
LG_HERO = 'https://www.lego.com/cdn/cs/aboutus/assets/blt46d84e22b9f45e8c/lego-campus-main-entrance.jpg'  # LEGO 報道用画像（main entrance・大きい版）
A_by['amazon']['hero'] = ('h', 'ガラスの球体「スフィア」')
A_by['dyson']['hero'] = (1, 'セント・ジェームス・パワーステーション。煙突に dyson のロゴ')
A_by['adidas']['hero'] = ('h', 'ARENA のエントランス。床に adidas のロゴ、136段の階段')
A_by['lego']['hero'] = ('h', '正面入口。巨大なミニフィグが出迎える')
A_by['google-bay-view']['hero'] = (5, '池越しに見た Bay View')
A_by['booking']['hero'] = (1, 'Booking.com キャンパス（©UNStudio）')
NIKE_HERO = 'https://images.prismic.io/skylab/2373031a-7213-4637-9101-b06f2cafe936_14075_N924.jpg'
BK = {'hero': 'https://content.presspage.com/uploads/685/86c4b08c-0d1d-49f4-87df-c4697f42eb6c/1920_booking.comcampus1-copyhuftoncrow-courtesyofunstudio.jpg'}
bsteps = A_by['booking']['steps']
bsteps[2] = bsteps[2][:3] + ([('g2', '館内のテーブル席'), ('g3', '打ち合わせの様子')],)
bsteps[3] = bsteps[3][:3] + ([('g1', '植物に囲まれた通路'), ('g4', '吹き抜けと植物')],)
# メインに使った写真は本文の章から外す（同じページで同じ写真を繰り返さない）
for _a in A:
    _h = _a['hero'][0]
    _a['steps'] = [st[:3] + ([(n, c) for n, c in st[3] if n != _h],) for st in _a['steps']]
def purl(a, n):
    if n == 'h' and a['slug'] == 'amazon': return AM_HERO
    if n == 'h' and a['slug'] == 'adidas': return AD_HERO
    if n == 'h' and a['slug'] == 'lego': return LG_HERO
    if a['slug'] == 'booking':
        return BK['hero'] if n == 1 else bk.get(n)
    if a['slug'] == 'nike':
        return NIKE_HERO if n == 1 else None
    return url(a['slug'], n)

# ---- ロゴ ----
def logo_svg(fill=None):
    w = o.text_width('OFFISNAP', 10); H = 10 * (5 + 4 * o.GAP)
    f = fill or 'url(#g)'
    sh, _ = o.text_svg('OFFISNAP', 0, 0, 10, f)
    d = '' if fill else (f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w:.2f}" y2="0">'
                         '<stop offset="0" stop-color="#1E2A78"/><stop offset="1" stop-color="#12A5C4"/></linearGradient></defs>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {H:.2f}" role="img" aria-label="OFFISNAP">{d}{sh}</svg>'
open(OUT + 'assets/logo.svg', 'w').write(logo_svg())
open(OUT + 'assets/logo-white.svg', 'w').write(logo_svg('#FFFFFF'))

# ---- CSS：WALL の style.css をそのまま。色だけ置換し、日本語用の書体を足す ----
css = open(W + 'assets/style.css', encoding='utf-8').read()
for a, b in [('#e2551b', '#1F6FB2'), ('#E2551B', '#1F6FB2'), ('#f2a93b', '#12A5C4'), ('#fdf0e7', '#EAF2FA'), ('#fbf3ee', '#F0F5FA'),
             ('#fdf6f2', '#F4F8FC'), ('#f3d9c7', '#CADCEE'), ('#c2440f', '#1E2A78'), ('#E86A1F', '#2B84C6'), ('#C8400F', '#1E2A78')]:
    css = css.replace(a, b)
css += '''
.lst{background:var(--ground);border-left:3px solid var(--accent);padding:14px 18px;margin:0 0 16px;font-size:14px;line-height:1.8}.lst ol{margin:6px 0 8px 20px;padding:0}.lst p{margin:0 0 6px}
.qidx{list-style:none;padding:0;margin:8px 0 48px;display:grid;gap:18px}.qidx li{margin:0}.qidx a{position:relative;display:grid;grid-template-columns:2fr 1fr 1fr;gap:3px;height:260px;text-decoration:none;overflow:hidden;background:#111;color:#fff}.qidx a img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s}.qidx a:hover img{transform:scale(1.03)}.qidx a .qc{position:absolute;left:0;right:0;bottom:0;padding:56px 18px 16px;background:linear-gradient(transparent,rgba(0,0,0,.72))}.qidx a .qc b{display:block;font-size:22px;font-weight:700;line-height:1.35;font-family:var(--sans);color:#fff}.qidx a .qc span{display:block;margin-top:4px;font-size:13px;color:rgba(255,255,255,.85);line-height:1.6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.qidx a .qq{position:absolute;left:0;top:0;background:var(--accent);color:#fff;font:700 11px/1 var(--sans);padding:6px 8px}@media(max-width:720px){.qidx a{grid-template-columns:1fr 1fr;grid-template-rows:150px 90px;height:auto}.qidx a img:first-of-type{grid-column:1/3}.qidx a .qc b{font-size:18px}}
.qmore{list-style:none;padding:0;margin:0}.qmore li{border-top:1px solid var(--line)}.qmore li:last-child{border-bottom:1px solid var(--line)}.qmore a{display:block;padding:14px 0;font-weight:600;text-decoration:none}.qmore a:hover{color:var(--accent)}
/* 2026-09-26 わたるさん「ページを狭くするとガタガタ」→ 長い社名で列の幅が変わらないように、列を等幅に固定 */
.cards{grid-template-columns:repeat(4,minmax(0,1fr))}.card{min-width:0}.card .co .kn{white-space:normal}
@media (max-width:900px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
/* OFFISNAP: 日本語の書体（欧文は WALL と同じ Cormorant / Inter Tight、和文は明朝とゴシック） */
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
/* OFFISNAP 2026-09-25 デザイン改善：WALLの寸法に合わせ、和文を読みやすく */
/* 1. ロゴ：WALL（109×44）と同じ見た目の量に。OFFISNAPは8文字なので高さを30pxに */
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
/* 2026-09-30 わたるさん「特集のタイトル、フォントサイズ大きすぎない？バランス考えて」→ 22px から 18px（スマホ16px）に。句ごとの改行をやめて自然に折り返す */
.cc h3{font-size:18px!important;line-height:1.5;word-break:normal!important;margin:10px 0 6px}@media(max-width:720px){.cc h3{font-size:16px!important}}
.sec-h h2{font-size:24px;letter-spacing:.04em}
.sec-h .sub{letter-spacing:.04em}
/* 6. 上部の帯・パンくず・目次 */
.draft{letter-spacing:.14em;font-size:11px}
.crumb{letter-spacing:.06em}
.toc{font-size:12px;line-height:1.7}.toc p{letter-spacing:.16em}
.foot p.fbang{font-size:15px;letter-spacing:.03em;line-height:1.6}
.foot{letter-spacing:.03em}
.nb{white-space:nowrap}
/* OFFISNAP 2026-09-25 その2：写真の並び・トップのスライド・パートナー欄・フッターと検索欄 */
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
.newb{display:block;top:0;right:0;width:64px;height:64px;padding:0;border-radius:0;box-shadow:none;background:linear-gradient(135deg,#163a8a,#1F6FB2);clip-path:polygon(0 0,100% 0,100% 100%);font-size:0}
.newb::after{content:"NEW";position:absolute;left:66.67%;top:33.33%;transform:translate(-50%,-50%) rotate(45deg);color:#fff;font:800 10.5px/1 var(--sans);letter-spacing:.14em;white-space:nowrap}
.cards{gap:26px 20px}
/* 人気のオフィス：写真の左上に順位（2026-09-26） */
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
    shutil.copy(f'banner/{_b}', OUT + 'assets/banner/' + _b)

SITE = 'https://offisnap.com'
# 公開用（2026-09-25 わたるさん判断：写真は公式プレス素材＋出典明記のまま公開。noindex を外す）
# ---- メタタイトルの決まり（2026-09-27 わたるさん「アルファベットとカタカナをマストで」） ----
# ①トップ：英字名（カタカナ）＋一言  ②下層：ページ名 | 英字名（カタカナ）  ③About：英字名（カタカナ）について
_BRAND_EN = 'OFFISNAP'; _BRAND_KANA = 'オフィスナップ'
def _brand_title(t):
    full = _BRAND_EN + '（' + _BRAND_KANA + '）'
    if full in t: return t
    if t.startswith(_BRAND_EN): return full + t[len(_BRAND_EN):].lstrip()
    t = re.sub(r'\s*[|｜]\s*' + re.escape(_BRAND_EN) + r'\s*$', '', t)
    return t + ' | ' + full
def head(title, desc, p, path='', og=None, otype='website'):
    title = _brand_title(title)
    u = SITE + '/' + ('' if path == 'index.html' else path)
    og = og or purl(A_by['spotify'], 7)
    return (f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="robots" content="index,follow,max-image-preview:large"><title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            f'<link rel="canonical" href="{E(u)}"><meta property="og:url" content="{E(u)}"><meta property="og:site_name" content="OFFISNAP"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">'
            f'<meta property="og:type" content="{otype}"><meta property="og:image" content="{E(og)}"><meta property="og:locale" content="ja_JP"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{E(og)}">'
            f'<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"><link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><meta name="theme-color" content="#1E2A78"><meta name="author" content="OFFISNAP 編集部"><meta property="og:image:alt" content="{E(title)}">'
            f'<meta name="google-site-verification" content="{GSC_TOKEN}">'
            '<meta name="google-adsense-account" content="ca-pub-1379037925480740">'
            f'{FONTS}<link rel="stylesheet" href="{p}assets/style.css">{GA}</head><body>')
# 2026-09-25 Search Console（URL プレフィックス https://offisnap.com/）の HTML タグ認証と GA4（プロパティ OFFISNAP 555994414、ストリーム 15843068805）
GSC_TOKEN = 'Ixm7-L8tqlN2EwSv7kkjfVxdeBSa6Hwyk-9DueLBYVY'
GA_ID = 'G-69FCWMYT6Y'
GA = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}",{{anonymize_ip:true}});</script>')
shutil.copy('flip.js', OUT + 'assets/flip.js')  # 一覧カードの写真めくり
for _f in os.listdir('icons'):
    shutil.copy('icons/' + _f, OUT + _f)

BAND = '世界の有名企業のオフィスを、見に行こう。'  # 2026-09-25 わたるさん選択
def nav(p, cur='', band=None):
    # 青い帯（.draft）は全ページに出す（2026-09-25 わたるさん「サイトのデザインが締まる」）
    items = [('offices', 'オフィス'), ('collections', '特集'), ('questions', 'Q&amp;A'), ('about', 'About')]
    li = ''.join(f'<li><a href="{p}{k}/index.html"{CUR if k == cur else ""}>{v}</a></li>' for k, v in items)
    return (f'<header class="wrap"><div class="nav"><a class="wm" href="{p}index.html"><img src="{p}assets/logo.svg" alt="OFFISNAP" width="120" height="30"><small>海外の最新オフィス紹介</small></a>\n'
            f'<ul>{li}</ul>\n<div class="r"><span>JP</span><a class="btn" href="{p}contact/index.html?topic=listing">掲載のご相談</a></div></div></header>'
            f'<div class="draft">{band or BAND}</div>')

def foot(p):
    return (f'<footer class="foot"><div class="wrap"><div class="fbrand"><a class="wm" href="{p}index.html"><img src="{p}assets/logo-white.svg" alt="OFFISNAP" width="96" height="22"></a><p class="fbang">海外の最新オフィス紹介メディア、OFFISNAP。</p></div>\n'
            f'<ul><li><a href="{p}about/index.html">OFFISNAP について</a></li><li><a href="{p}questions/index.html">Q&amp;A</a></li><li><a href="{p}offices/index.html">地域から探す</a></li><li><a href="{p}offices/index.html">業種から探す</a></li></ul>\n'
            f'<ul><li><a href="{p}about/privacy.html">プライバシーポリシー</a></li><li><a href="{p}about/terms.html">利用規約</a></li><li><a href="{p}contact/index.html">お問い合わせ</a></li></ul>\n'
            '<p class="copy">© 2026 OFFISNAP. 海外のオフィスを取材・紹介するメディアです。</p></div></footer>'
            f'<script src="{p}assets/flip.js" defer></script>'
            '<script>(function(){var b=document.body,h=document.querySelector("header.wrap"),f=function(){b.classList.toggle("stuck",window.scrollY>80);if(h)document.documentElement.style.setProperty("--hh",h.offsetHeight+"px")};window.addEventListener("resize",f);f();window.addEventListener("scroll",f,{passive:true})})();</script>')

exec(open('articles_ja.py', encoding='utf-8').read())
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
KANA = {'spotify':'スポティファイ','amazon':'アマゾン','dyson':'ダイソン','adidas':'アディダス','bloomberg':'ブルームバーグ','lego':'レゴ','google-bay-view':'グーグル','nike':'ナイキ','booking':'ブッキングドットコム'}
KANA.update(KANA20)
def coname(a): return E(a['company'].upper()) + (f'<span class="kn">（{E(KANA[a["slug"]])}）</span>' if a['slug'] in KANA else '')  # 読みは途中で折り返さない
def card(a, p, new=True, rank=None, attrs=''):
    u = purl(a, a['hero'][0])
    img = f'<img class="ph" src="{E(u)}" alt="" loading="lazy">' if u else ''
    _ex = [purl(a, n) for st in a['steps'] for n, _ in st[3]]; _ex = [x for x in _ex if x and x != u][:3]
    _dp = f' data-ph="{E("|".join(_ex))}"' if _ex else ''
    _rk = f'<i class="rk">{rank}</i>' if rank else ''
    return (f'<a class="card" href="{p}offices/{a["slug"]}.html"{_dp}{attrs}><span class="phw">{_rk}{img}{NEWB if new else ""}</span>'
            f'<div class="co">{coname(a)}</div><div class="cp">{E(a["card"])}</div><div class="cr">{E(city_short(a))}｜{E(a["industry"])}</div></a>')

# 掲載企業の公式サイト（2026-09-25 わたるさん指摘：「公式サイト」は出典ではなく会社の公式ページ。出典は下の基本情報に残す）
OFFICIAL = {'spotify':'https://www.spotify.com/','amazon':'https://www.aboutamazon.com/','dyson':'https://www.dyson.com/','adidas':'https://www.adidas-group.com/','bloomberg':'https://www.bloomberg.com/company/','lego':'https://www.lego.com/','google-bay-view':'https://about.google/','nike':'https://about.nike.com/','booking':'https://www.booking.com/',
 'apple':'https://www.apple.com/','nvidia':'https://www.nvidia.com/','salesforce':'https://www.salesforce.com/','siemens':'https://www.siemens.com/','puma':'https://about.puma.com/','alibaba':'https://www.alibabagroup.com/','tencent':'https://www.tencent.com/','deloitte':'https://www.deloitte.com/nl/en.html','zalando':'https://corporate.zalando.com/','airbnb':'https://www.airbnb.com/','uber':'https://www.uber.com/','ikea':'https://www.ikea.com/','etsy':'https://www.etsy.com/','swatch':'https://www.swatch.com/','samsung':'https://www.samsung.com/','carlsberg':'https://www.carlsberggroup.com/','adobe':'https://www.adobe.com/','continental':'https://www.continental.com/','merck':'https://www.merckgroup.com/'}
OFFICIAL.update(globals().get('OFFICIAL30', {}))
assert all(a['slug'] in OFFICIAL for a in A), [a['slug'] for a in A if a['slug'] not in OFFICIAL]

# メタタイトル（2026-09-25 わたるさん：「社名（英字/カタカナ）＋オフィス」で引っかかるように。「海外オフィス」でも1位を狙う）
# 検索は「ダイソン オフィス」「dyson 本社」「〜 オフィス 内装」「〜 オフィス 写真」が中心なので、英字とカタカナの両方＋オフィス・本社・内装・写真を入れる
LOC = {'apple':'クパティーノ本社 Apple Park','nvidia':'サンタクララ本社 Voyager','salesforce':'サンフランシスコ本社','siemens':'ミュンヘン本社','puma':'ドイツ本社','alibaba':'杭州本社','tencent':'深圳本社','deloitte':'アムステルダム The Edge','zalando':'ベルリン本社','airbnb':'サンフランシスコ本社','uber':'サンフランシスコ本社','ikea':'マルメ Hubhult','etsy':'ニューヨーク本社','swatch':'スイス本社','samsung':'シリコンバレー本社','carlsberg':'コペンハーゲン本社','adobe':'サンノゼ本社','continental':'ハノーファー本社','merck':'ドイツの研究拠点','spotify':'ストックホルム本社','amazon':'シアトル本社','dyson':'シンガポール本社','adidas':'ドイツ本社','bloomberg':'ロンドン欧州本社','lego':'デンマーク本社','google-bay-view':'本社 Bay View','nike':'米国本社','booking':'アムステルダム本社'}
LOC.update(globals().get('LOC30', {}))
def meta_title(a):
    kn = KANA.get(a['slug']); loc = LOC.get(a['slug'], city_short(a) + '本社')
    return f"{a['company']}{'（' + kn + '）' if kn else ''}のオフィス｜{loc}の内装・写真 | OFFISNAP"
def meta_desc(a):
    kn = KANA.get(a['slug'])
    return f"{a['company']}{'（' + kn + '）' if kn else ''}の{LOC.get(a['slug'], city_short(a) + '本社')}のオフィスを、公式の写真と情報で紹介。{a['card']}。{a['lead']}"

# ---- 記事ページ（WALL offices/mitsui-fudosan.html と同じ並び） ----
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
    edc = '<aside class="edc" id="editor"><p class="lab">編集部より</p>' + ''.join(f'<p>{E(x)}</p>' for x in ED[a['slug']]) + '<p class="sig">OFFISNAP 編集部</p></aside>'
    return (head(meta_title(a), meta_desc(a), p, f'offices/{a["slug"]}.html', purl(a, a['hero'][0]), 'article') + nav(p, 'offices') + '\n<main class="wrap">\n'
            f'<div class="crumb">オフィス › {E(a["city"])} › {E(a["company"].upper())}</div>\n'
            f'<div class="head"><p class="tag" style="color:var(--mute)">{E(tagline(a))}</p>\n<h1>{T(a["title"])}</h1>\n<p class="std">{E(a["lead"])}</p>\n<div class="facts">{facts}</div></div>\n'
            f'<div class="hero">{heroimg}</div>\n<div class="body">\n<nav class="toc"><p>目次</p><ol>{toc}</ol>'
            f'<a class="omv" href="https://offml.com/?utm_source=offisnap&amp;utm_medium=banner" rel="noopener"><img src="{OMB160}" width="160" height="600" alt="OFFICEMILL"></a></nav>\n'
            f'<article>\n{body}\n{ctx}\n{edc}\n<div class="credits" id="credits">{cr}</div>\n{shop}\n</article></div>\n<!--REL:{a["slug"]}-->\n'
            f'<a class="omb omb-728x90" href="https://offml.com/?utm_source=offisnap&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a>\n'
            '</main>' + foot(p) + '</body></html>')

for a in A:
    open(OUT + f'offices/{a["slug"]}.html', 'w', encoding='utf-8').write(article(a))

# ---- 特集カード（WALL の .cc と同じ） ----
# 特集タイトルの最後に社数で「〇選」（2026-09-26 わたるさん）。社数が増えれば自動で変わる
for _c in COLLECTIONS:
    _c['title'] = re.sub(r'\d+選$', '', _c['title']) + f'{len(_c["items"])}選'
def cc(c, p):
    imgs = [purl(A_by[s], A_by[s]['hero'][0]) for s, _ in c['items']]
    imgs = [u for u in imgs if u]
    main_i = f'<img src="{E(imgs[0])}" alt="" loading="lazy">' if imgs else ''
    sub = ''.join(f'<img src="{E(u)}" alt="" loading="lazy">' for u in imgs[1:4])
    return (f'<a class="cc" href="{p}collections/{c["slug"]}.html">{main_i}<div class="ccm">{sub}</div>'
            f'<h3>{E(c["title"])}</h3><p class="ccs">{E(c["lead"])}</p></a>')

# 2026-09-29 わたるさん「WALLみたいに一覧ボタンに数を入れろ」→ トップの一覧ボタン3つ全部に数（WALL: VIEW ALL 128 OFFICES）
_KW = globals().get('KIND_WORD', '社') if globals().get('KIND_WORD') not in (None, '', 'オフィス') else '社'
# ---- トップ（WALL index.html と同じ並び） ----
p = ''
slides = ''
for k, s in enumerate(['apple', 'swatch', 'nvidia', 'dyson', 'siemens', 'google-bay-view']):
    a = A_by[s]; u = purl(a, a['hero'][0])
    on = k == 0
    slides += (f'<div class="hs{" on" if on else ""}" aria-hidden="{"false" if on else "true"}"><a class="hsimg" href="offices/{s}.html" tabindex="-1"><img class="ph" src="{E(u)}" alt="{E(a["company"])} のオフィス"{"" if on else LAZY}></a>'
               f'<div class="cap"><p class="tag">{E(tagline(a))}</p><h1><a href="offices/{s}.html">{T(a["title"])}</a></h1><p class="std">{E(a["lead"])}</p><a class="ctx-tag" href="offices/{s}.html">続きを読む →</a></div></div>')
dots = ''.join(f'<button type="button" aria-label="スライド {i+1}"{ON if i == 0 else ""}></button>' for i in range(6))
# 2026-09-26 わたるさん「トップ画像、WALLみたいにランダムで表示するようにして」
# WALL と同じ方式：HTMLには固定の6社を入れておき（JSが動かないとき用）、開くたびに全社から6社をランダムに選んで差し替える
_pool = [dict(s=a['slug'], img=purl(a, a['hero'][0]), alt=a['company'] + ' のオフィス', tag=tagline(a), h=T(a['title']), std=a['lead']) for a in A if purl(a, a['hero'][0])]
HERO_JS = ('<script>var OS_HERO=' + json.dumps(_pool, ensure_ascii=False).replace('</', '<\\/') + ';'
 '(function(){var r=document.querySelector(".hslider");if(!r)return;try{var P=OS_HERO.slice(),S=r.querySelectorAll(".hs");'
 'for(var k=0;k<S.length&&k<P.length;k++){var j=k+Math.floor(Math.random()*(P.length-k));var t=P[k];P[k]=P[j];P[j]=t;var d=P[k],e=S[k],u="offices/"+d.s+".html";'
 'var im=e.querySelector("img");im.src=d.img;im.alt=d.alt;e.querySelector(".hsimg").href=u;e.querySelector(".tag").textContent=d.tag;'
 'var h=e.querySelector("h1 a");h.href=u;h.innerHTML=d.h;e.querySelector(".std").textContent=d.std;e.querySelector(".ctx-tag").href=u;}}catch(x){}})();</script>')
exec(open('popular.py', encoding='utf-8').read())
_bs = {a['slug']: a for a in A}
POP = [_bs[x] for x in POPULAR if x in _bs] + [a for a in A if a['slug'] not in POPULAR]
POPRANK = {a['slug']: i + 1 for i, a in enumerate(POP)}
SLIDER_JS = open(W + 'index.html', encoding='utf-8').read().split('</footer>')[1].replace('</body></html>', '')
top = (head('OFFISNAP（オフィスナップ）海外オフィス｜有名企業・本社の内装を写真で紹介', f'海外の有名企業のオフィスを、公式の写真と情報で1社ずつ紹介。Apple・Google・Amazon・Spotify・Dyson など{len(A)}社の本社の内装、デザイン、働き方を日本語で。', p, 'index.html') + nav(p) + '\n<main class="wrap">\n'
       f'<section class="hero hslider" aria-roledescription="carousel">{slides}<div class="hdots">{dots}</div></section>{HERO_JS}\n\n'
       '<form class="tsearch" action="offices/index.html" method="get" role="search"><input type="search" name="q" placeholder="会社名・都市・キーワードで探す" aria-label="オフィスを探す"><button type="submit">検索</button></form>\n'
       f'<section class="sec"><div class="sec-h"><h2>新着記事</h2><span class="sub">エントランスから順に、1社ずつご案内</span><a class="more" href="offices/index.html">一覧へ →</a></div>\n'
       f'<div class="cards">{"".join(card(a, p) for a in A[:12])}</div><div class="viewall"><a href="offices/index.html">オフィス一覧を見る（{len(A)}{_KW}） <span>→</span></a></div></section>\n\n'
       f'<section class="sec"><div class="sec-h"><h2>人気のオフィス</h2><span class="sub">いま多く読まれている12社</span><a class="more" href="offices/index.html?sort=pop">一覧へ →</a></div>\n'
       f'<div class="cards">{"".join(card(a, p, False, i + 1) for i, a in enumerate(POP[:12]))}</div><div class="viewall"><a href="offices/index.html?sort=pop">人気順で一覧を見る（{len(A)}{_KW}） <span>→</span></a></div></section>\n\n'
       f'<section class="sec"><div class="sec-h"><h2>特集</h2><span class="sub">テーマ別に、国を越えて見比べる</span><a class="more" href="collections/index.html">一覧へ →</a></div>\n'
       f'<div class="ccg">{"".join(cc(c, p) for c in COLLECTIONS[:6])}</div><div class="viewall"><a href="collections/index.html">特集一覧を見る（{len(COLLECTIONS)}本） <span>&rarr;</span></a></div></section>\n\n'
       f'<a class="omb omb-728x90" href="https://offml.com/?utm_source=offisnap&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a>\n\n'
       # 設計・施工パートナー欄は、掲載できる会社がそろうまで非表示（2026-09-25）
       '</main>' + foot(p) + SLIDER_JS + '</body></html>')
open(OUT + 'index.html', 'w', encoding='utf-8').write(top)

# ---- オフィス一覧 ----
# 絞り込み用の軸（2026-09-26 わたるさん：「何百施設になるつもりで、各施設での絞り込みを」）。build_mill.py が AREA_OF / F2 を差し替える
def AREA_OF(a):
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
lst = (head(f'海外オフィス一覧｜有名企業{len(A)}社の本社・内装写真 | OFFISNAP', f'海外の有名企業{len(A)}社のオフィス一覧。本社の内装とデザインを、公式の写真と情報で1社ずつ紹介します。', p, 'offices/index.html') + nav(p, 'offices') + '\n<main class="wrap"><div class="coll"><h1>海外オフィス一覧</h1><p class="lead">海外の有名企業のオフィスを、エントランスから順に1社ずつご案内しています。</p></div>\n'
       f'<section class="sec">' + fbar(A, '社', '会社名・都市・キーワードで探す') +
       f'<div class="cards bynew" id="olist">{"".join(lcard(i, a) for i, a in enumerate(A))}</div></section>\n' + SORT_JS +
       f'<a class="omb omb-728x90" href="https://offml.com/" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot(p) + '</body></html>')
open(OUT + 'offices/index.html', 'w', encoding='utf-8').write(lst)

# ---- 特集 ----
col = (head('海外オフィス特集｜テーマ別に有名企業の本社を見比べる | OFFISNAP', '植物、階段、木造、運動できる本社など、海外の有名企業のオフィスをテーマ別に見比べる特集。', p, 'collections/index.html') + nav(p, 'collections') + '\n<main class="wrap"><div class="coll"><h1>特集</h1><p class="lead">国も業種も違うオフィスを、共通のテーマで見比べる特集です。</p>'
       f'<div class="ccg">{"".join(cc(c, p) for c in COLLECTIONS)}</div></div></main>' + foot(p) + '</body></html>')
open(OUT + 'collections/index.html', 'w', encoding='utf-8').write(col)
for c in COLLECTIONS:
    secs = ''
    for i, (s, q) in enumerate(c['items']):
        a = A_by[s]
        secs += (f'<section class="step" id="s{i+1}"><p class="no">{i+1:02d}｜{E(a["company"])}（{E(city_short(a))}）</p><h2>{E(q)}</h2>' + fig(a, a['hero'][0], a['hero'][1]) +
                 f'<p>{E(a["lead"])}</p><p><a class="ctx-tag" href="../offices/{s}.html">続きを読む →</a></p></section>')
    pg = (head(f'{c["title"]}｜海外オフィス特集 | OFFISNAP', c['lead'] + '（' + '・'.join(A_by[x[0]]['company'] for x in c['items']) + '）', p, f'collections/{c["slug"]}.html', purl(A_by[c['items'][0][0]], A_by[c['items'][0][0]]['hero'][0]), 'article') + nav(p, 'collections', '特集｜テーマ別に見比べる') + '\n<main class="wrap">\n'
          f'<div class="crumb">特集 › {E(c["title"])}</div><div class="head"><p class="tag" style="color:var(--mute)">特集</p><h1>{E(c["title"])}</h1><p class="std">{E(c["lead"])}</p></div>\n'
          f'<div class="body"><nav class="toc"><p>登場する会社</p><ol>{toc_items([x[0] for x in c["items"]])}</ol></nav><article>{secs}</article></div>\n'
          f'<a class="omb omb-728x90" href="https://offml.com/" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot(p) + '</body></html>')
    open(OUT + f'collections/{c["slug"]}.html', 'w', encoding='utf-8').write(pg)

# ---- Q&A（2026-09-26 わたるさん「WALL みたいに Q&A のトップを考えろ」→ WALL と同じ型に）
#   questions/index.html = 質問の一覧。questions/<slug>.html = 1問1ページ
#   （短い答え → 根拠になる施設の写真と本文 → キーワード → 登場する施設のカード → ほかの質問）
#   データは questions.py（OFFISNAP）／questions_<brand>.py（MILL）の QUESTIONS。無ければ従来の QA 1問で作る
if 'QUESTIONS' not in globals():
    if os.path.exists('questions.py'):
        exec(open('questions.py', encoding='utf-8').read())
    else:
        QUESTIONS = [dict(slug=QA['slug'], q=QA['q'], a=QA['a'], desc=QA['a'],
                          secs=[(s_, h_, [t_], [(s_, A_by[s_]['hero'][0])]) for s_, h_, t_ in QA['secs']],
                          ctx=None, items=[x[0] for x in QA['secs']])]
_QSEC = SEC_NAME if 'SEC_NAME' in globals() else 'offices'
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
SITE_NAME = globals().get('SITE_NAME', 'OFFISNAP')
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
QA_TITLE = globals().get('QA_TITLE', '海外オフィスの Q&A')
QA_LEAD = globals().get('QA_LEAD', '海外の有名企業のオフィスについて、よく聞かれる質問に短く答えます。答えはすべて、掲載している会社の公式情報から書いています。')
qa = (head(QA_TITLE + ' | ' + SITE_NAME, QA_LEAD, '../', 'questions/index.html') + nav('../', 'questions') +
      f'\n<main class="wrap"><div class="page"><div class="head"><p class="tag" style="color:var(--mute)">Q&amp;A</p><h1>{E(QA_TITLE)}</h1><p class="std">{E(QA_LEAD)}</p></div>'
      f'</div><ul class="qidx">{_qlist}</ul>'
      f'<a class="omb omb-728x90" href="https://offml.com/?utm_source={UTM}&amp;utm_medium=banner" rel="noopener"><img src="{OMB728}" width="728" height="90" alt="OFFICEMILL"></a></main>' + foot('../') + '</body></html>')
open(OUT + 'questions/index.html', 'w', encoding='utf-8').write(qa)
QA = dict(q=QA_TITLE, a=QA_LEAD)

ab = (head('OFFISNAP について', '海外の有名企業の最新オフィスを紹介するメディア、OFFISNAP について。', p, 'about/index.html') + nav(p, 'about') + '\n<main class="wrap"><div class="head"><p class="tag" style="color:var(--mute)">About</p><h1>OFFISNAP について</h1>'
      '<p class="std">海外の有名企業の最新オフィスを紹介するメディアです。1社ごとに、受付から執務フロア、会議室、食堂、福利厚生の場所へと、初めて訪れた人が歩く順番で紹介します。</p></div>'
      '<div class="body"><nav class="toc"><p>目次</p><ol><li><a href="#s1">編集方針</a></li></ol></nav><article>'
      '<section class="step" id="s1"><p class="no">01｜編集方針</p><h2>受付から順に、歩くように</h2><p>海外の有名企業のオフィスを、初めて訪れた人が歩く順番でご案内します。写真と事実は各社の公式発表にもとづき、編集部の見立ては「編集部より」に分けて書いています。</p></section>'
      '</article></div></main>' + foot(p) + '</body></html>')
open(OUT + 'about/index.html', 'w', encoding='utf-8').write(ab)
print('ok', sorted(os.listdir(OUT + 'offices')))
# ---- プライバシーポリシー・利用規約・お問い合わせ（WALL の about/privacy・terms・contact と同じ型。2026-09-25） ----
os.makedirs(OUT + 'contact', exist_ok=True)
UPD = '2026年9月25日'
privacy = (head('プライバシーポリシー | OFFISNAP', 'OFFISNAP のプライバシーポリシー。', p, 'about/privacy.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page legal"><h1>プライバシーポリシー</h1><p class="upd">最終更新：{UPD}</p>
<p>OFFISNAP（以下「当サイト」）が、offisnap.com の利用にあたって個人情報をどう扱うかを説明します。</p>
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
terms = (head('利用規約 | OFFISNAP', 'OFFISNAP の利用規約。', p, 'about/terms.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page legal"><h1>利用規約</h1><p class="upd">最終更新：{UPD}</p>
<p>この規約は、OFFISNAP（以下「当サイト」）が運営する offisnap.com の利用に適用されます。当サイトを利用した時点で、この規約に同意したものとします。</p>
<h2>1. 記事の内容</h2>
<p>記事は、掲載企業が公開している公式サイト・公式ニュースの情報をもとに、OFFISNAP 編集部が書いています。正確さに努めますが、オフィスや会社、設計者に関する情報は掲載後に変わることがあり、現状のまま提供します。</p>
<h2>2. 知的財産</h2>
<p>文章、レイアウト、ロゴは OFFISNAP に帰属します。写真は、クレジットに記した各企業・設計者・写真家に帰属し、各社が公開している素材を出典を明記して使っています。権利者の許可なく、複製、転載、商用利用はできません。出典と元記事へのリンクを明記した短い引用は歓迎します。</p>
<h2>3. 掲載企業からのご要望</h2>
<p>掲載企業、写真の権利者から、写真や記事の修正・取り下げのご要望があった場合は、すみやかに対応します。<a href="../contact/index.html">お問い合わせ</a>からご連絡ください。</p>
<h2>4. 禁止事項</h2>
<ul><li>法令または他者の権利に反する行為</li><li>自動化された大量アクセスや不正アクセスなど、サイトの運営を妨げる行為</li><li>お問い合わせを通じた虚偽の情報、迷惑行為、有害な内容の送信</li><li>OFFISNAP や掲載企業との関係を偽ること</li></ul>
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
contact = (head('お問い合わせ | OFFISNAP', 'OFFISNAP 編集部へのお問い合わせ。掲載についてのご要望、取材・提携のご相談。', p, 'contact/index.html') + nav(p, 'about') + f'''
<main class="wrap"><div class="page"><h1>お問い合わせ</h1>
<p class="lead">掲載についてのご要望、取材や提携のご相談、記事の誤りのご指摘など、お気軽にお知らせください。1週間以内に返信します。</p>
<form class="cform" action="{_act}" method="POST">
<label>用件<select name="topic" id="topic" required><option value="listing">掲載のご相談（オフィスを紹介してほしい）</option><option value="content">掲載内容・写真についてのご要望</option><option value="partner">提携・広告のご相談</option><option value="media">取材・メディア</option><option value="other">その他</option></select></label>
<div class="row2"><label>お名前<input name="name" autocomplete="name" required></label><label>メールアドレス<input type="email" name="email" autocomplete="email" required></label></div>
<label><b class="lt">会社名 <span>（任意）</span></b><input name="company" autocomplete="organization"></label>
<div class="lst" id="listing-note" hidden><p><b>掲載のご相談は、次の3つをお書きください。</b></p><ol><li>会社名と、紹介してほしいオフィスの場所</li><li>オフィスの写真（Googleドライブなどの共有URL、または写真が載っている公式ページのURL）</li><li>オフィスのことが分かる資料やページのURL（プレスリリース、設計事務所のページなど）</li></ol><p>写真と情報は公式のものだけを使い、出典を明記して紹介します。内容を確認のうえ、掲載の可否を返信します。</p></div>
<label>本文<textarea name="message" rows="7" required placeholder="掲載のご相談の場合は、会社名・オフィスの場所・写真のURL・資料のURLをお書きください"></textarea></label>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="hidden" name="_next" value="{SITE}/contact/thanks.html">
<input type="hidden" name="_subject" value="OFFISNAP お問い合わせ"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_template" value="table">
<p class="note">送信により、<a href="../about/privacy.html" style="border-bottom:1px solid var(--accent)">プライバシーポリシー</a>に同意したものとします。{'' if FORMSPREE_ID else 'フォームは準備中です。'}</p>
<button type="submit"{_dis}>送信する →</button>
</form>
<script>(function(){{var sel=document.getElementById('topic'),nt=document.getElementById('listing-note');function u(){{nt.hidden=sel.value!=='listing';}}try{{var t=new URLSearchParams(location.search).get('topic');if(t)sel.value=t;}}catch(e){{}}sel.addEventListener('change',u);u();}})();</script>
</div></main>''' + foot(p) + '</body></html>')
open(OUT + 'contact/index.html', 'w', encoding='utf-8').write(contact)
thanks = (head('送信しました | ' + globals().get('SITE_NAME', 'OFFISNAP'), 'お問い合わせを受け付けました。', p, 'contact/thanks.html') + nav(p, 'about') +
          '\n<main class="wrap"><div class="page"><h1>送信しました</h1><p class="lead">お問い合わせを受け付けました。内容を確認のうえ、1週間以内に返信します。</p>'
          f'<p><a class="ctx-tag" href="{p}index.html">トップへ戻る →</a></p></div></main>' + foot(p) + '</body></html>')
open(OUT + 'contact/thanks.html', 'w', encoding='utf-8').write(thanks)

# ---- sitemap / robots / vercel（公開用） ----
import datetime
_today = datetime.date.today().isoformat()
_paths = ['', 'offices/index.html', 'collections/index.html', 'questions/index.html', 'about/index.html', 'about/privacy.html', 'about/terms.html', 'contact/index.html'] + [f'offices/{a["slug"]}.html' for a in A] + [f'collections/{c["slug"]}.html' for c in COLLECTIONS] + [f'questions/{q["slug"]}.html' for q in QUESTIONS]
open(OUT + 'sitemap.xml', 'w', encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}/{x}</loc><lastmod>{_today}</lastmod></url>\n' for x in _paths) + '</urlset>\n')
open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
# 2026-09-27 わたるさん「URLの末尾に index.html がつくのが嫌」→ 古い …/index.html は …/ へ転送する
open(OUT + 'vercel.json', 'w').write(json.dumps({"redirects": [{"source": "/index.html", "destination": "/", "permanent": True}, {"source": "/:path*/index.html", "destination": "/:path*/", "permanent": True}]}, indent=1) + '\n')

# ---- SEO / AIO（構造化データ・llms.txt・webmanifest）2026-09-25 ----
COUNTRY = {**COUNTRY20, 'spotify':'SE','amazon':'US','dyson':'SG','adidas':'DE','bloomberg':'GB','lego':'DK','google-bay-view':'US','nike':'US','booking':'NL'}
ORG = {"@type":"Organization","@id":SITE+"/#org","name":"OFFISNAP","alternateName":"オフィスナップ","url":SITE+"/","logo":{"@type":"ImageObject","url":SITE+"/favicon-512x512.png","width":512,"height":512},"description":"海外の有名企業の最新オフィスを、写真と一緒に日本語で1社ずつ紹介するメディア。","inLanguage":"ja"}
PUB = '2026-09-25'
def ld_for(path):
    ld = []
    u = SITE + '/' + ('' if path == 'index.html' else path)
    if path == 'index.html':
        ld.append({"@context":"https://schema.org","@type":"WebSite","@id":SITE+"/#website","name":"OFFISNAP","alternateName":"オフィスナップ — 海外の最新オフィス紹介","url":SITE+"/","inLanguage":"ja","publisher":{"@id":SITE+"/#org"},"potentialAction":{"@type":"SearchAction","target":{"@type":"EntryPoint","urlTemplate":SITE+"/offices/index.html?q={search_term_string}"},"query-input":"required name=search_term_string"}})
        ld.append({"@context":"https://schema.org",**ORG})
        ld.append({"@context":"https://schema.org","@type":"ItemList","name":"新着記事","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/offices/{a['slug']}.html","name":a['title']} for i, a in enumerate(A)]})
    m = re.match(r'offices/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        a = A_by[m.group(1)]
        src = next(c[1] for c in a['credits'] if c[0] == '出典URL')
        ld.append({"@context":"https://schema.org","@type":"Article","@id":u+"#article","mainEntityOfPage":u,"headline":a['title'],"description":a['lead'],"image":[purl(a, a['hero'][0])],
                   "datePublished":PUB,"dateModified":PUB,"inLanguage":"ja","author":{"@type":"Organization","name":"OFFISNAP 編集部","url":SITE+"/about/index.html"},"publisher":{"@id":SITE+"/#org"},
                   "about":{"@type":"Place","name":f"{a['company']} のオフィス","address":{"@type":"PostalAddress","addressLocality":city_short(a),"addressCountry":COUNTRY.get(a['slug'],'')}},
                   "mentions":[{"@type":"Organization","name":a['company']}],"citation":src,"keywords":", ".join([a['company'], city_short(a), a['industry'], 'オフィス', '本社', a['word']['term']]),
                   "articleSection":"海外オフィス","isBasedOn":src})
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"OFFISNAP","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"オフィス","item":SITE+"/offices/index.html"},{"@type":"ListItem","position":3,"name":a['company'],"item":u}]})
    if path == 'offices/index.html':
        ld.append({"@context":"https://schema.org","@type":"CollectionPage","name":"オフィス一覧","url":u,"inLanguage":"ja","isPartOf":{"@id":SITE+"/#website"},"hasPart":[{"@type":"Article","url":f"{SITE}/offices/{a['slug']}.html","headline":a['title']} for a in A]})
    m = re.match(r'collections/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        c = next(x for x in COLLECTIONS if x['slug'] == m.group(1))
        ld.append({"@context":"https://schema.org","@type":"Article","mainEntityOfPage":u,"headline":c['title'],"description":c['lead'],"image":[purl(A_by[c['items'][0][0]], A_by[c['items'][0][0]]['hero'][0])],"datePublished":PUB,"dateModified":PUB,"inLanguage":"ja","author":{"@type":"Organization","name":"OFFISNAP 編集部"},"publisher":{"@id":SITE+"/#org"},"articleSection":"特集","hasPart":[{"@type":"WebPage","url":f"{SITE}/offices/{sl}.html","name":A_by[sl]['company']} for sl, _ in c['items']]})
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"OFFISNAP","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"特集","item":SITE+"/collections/index.html"},{"@type":"ListItem","position":3,"name":c['title'],"item":u}]})
    if path == 'questions/index.html':
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q_['q'],"acceptedAnswer":{"@type":"Answer","text":q_['a']}} for q_ in QUESTIONS]})
    m = re.match(r'questions/([^/]+)\.html$', path)
    if m and m.group(1) != 'index':
        q_ = next(x for x in QUESTIONS if x['slug'] == m.group(1))
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q_['q'],"acceptedAnswer":{"@type":"Answer","text":q_['a'] + ' ' + ' '.join(x for _, _, ps, _ in q_['secs'] for x in ps)}}]})
        ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":SITE_NAME,"item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Q&A","item":SITE+"/questions/index.html"},{"@type":"ListItem","position":3,"name":q_['q'],"item":u}]})
    if path == 'about/index.html':
        ld.append({"@context":"https://schema.org","@type":"AboutPage","name":"OFFISNAP について","url":u,"inLanguage":"ja","about":{"@id":SITE+"/#org"}})
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
open(OUT + 'site.webmanifest', 'w', encoding='utf-8').write(json.dumps({"name":"OFFISNAP — 海外の最新オフィス紹介","short_name":"OFFISNAP","description":"海外の有名企業の最新オフィスを日本語で紹介","start_url":"/","display":"standalone","background_color":"#ffffff","theme_color":"#1E2A78","lang":"ja","icons":[{"src":"/favicon-192x192.png","sizes":"192x192","type":"image/png"},{"src":"/favicon-512x512.png","sizes":"512x512","type":"image/png"}]}, ensure_ascii=False))
# llms.txt（AI 向けのサイト案内。WALL と同じ考え方）
_lines = ['# OFFISNAP', '', '> 海外の有名企業の最新オフィスを、公式素材をもとに日本語で1社ずつ紹介するメディア。受付から執務フロア、会議室、食堂へと、初めて訪れた人が歩く順番で案内する。運営: OFFISNAP 編集部（日本）。', '',
          '## 記事（オフィス）', ''] + [f'- [{a["title"]}]({SITE}/offices/{a["slug"]}.html): {a["lead"]}' for a in A] + ['', '## 特集', ''] + [f'- [{c["title"]}]({SITE}/collections/{c["slug"]}.html): {c["lead"]}' for c in COLLECTIONS] + \
         ['', '## その他', '', f'- [Q&A]({SITE}/questions/index.html): {QA["q"]}'] + [f'- [{q_["q"]}]({SITE}/questions/{q_["slug"]}.html): {q_["a"]}' for q_ in QUESTIONS] + [ f'- [OFFISNAP について]({SITE}/about/index.html)', f'- [お問い合わせ]({SITE}/contact/index.html)', '', '## 引用について', '', '記事の事実は各社の公式サイト・公式ニュースが出典。引用の際は記事URLを添えてください。写真の権利は各社・撮影者に帰属します。']
open(OUT + 'llms.txt', 'w', encoding='utf-8').write('\n'.join(_lines) + '\n')

# ---------- 詳細ページ下のおすすめ（2026-09-29 WALLと同じ仕組み。指示書_記事下おすすめ_内部リンク_2026-09-29） ----------
# ①この施設が載っている特集（最大3本）＋質問ページの1行 ②次に見る施設3件（理由つき）。人気順ではなく「候補リストの中で自分の次」を選ぶ
REL_NOUN  = globals().get('REL_NOUN', 'オフィス')
REL_ORDER = globals().get('REL_ORDER', ['kind', 'town', 'coll', 'country', 'coll2'])
_REL_CN = {'UK': 'イギリス', 'US': 'アメリカ', 'GB': 'イギリス', 'DE': 'ドイツ', 'FR': 'フランス', 'NL': 'オランダ', 'SE': 'スウェーデン', 'DK': 'デンマーク', 'SG': 'シンガポール', 'CN': '中国', 'KR': '韓国', 'CH': 'スイス', 'IT': 'イタリア', 'ES': 'スペイン', 'AU': 'オーストラリア', 'CA': 'カナダ', 'JP': '日本', 'IE': 'アイルランド', 'FI': 'フィンランド', 'NO': 'ノルウェー', 'BE': 'ベルギー', 'AT': 'オーストリア', 'HK': '香港', 'TW': '台湾', 'IN': 'インド', 'BR': 'ブラジル', 'MX': 'メキシコ', 'IL': 'イスラエル', 'AE': 'アラブ首長国連邦', 'TH': 'タイ', 'PL': 'ポーランド', 'PT': 'ポルトガル', 'CZ': 'チェコ', 'NZ': 'ニュージーランド', 'ZA': '南アフリカ', 'RU': 'ロシア', 'TR': 'トルコ', 'VN': 'ベトナム', 'MY': 'マレーシア', 'ID': 'インドネシア', 'PH': 'フィリピン', 'AR': 'アルゼンチン', 'CL': 'チリ', 'LU': 'ルクセンブルク', 'HU': 'ハンガリー'}
NEAR      = globals().get('NEAR', {})
REL_KIND_LABEL = globals().get('REL_KIND_LABEL', '同じ{kind}業界')
def _rel_next(lst, slug, taken):
    ss = [x['slug'] for x in lst]
    if slug in ss: st = ss.index(slug) + 1
    else:  # 自分が候補に入っていない（近いエリアなど）ときは、データの並びで自分の次の位置から選ぶ（先頭ばかりに集まらないように）
        _ix = {x['slug']: i for i, x in enumerate(A)}
        st = sum(1 for x in lst if _ix.get(x['slug'], 0) < _ix.get(slug, 0))
    for x in lst[st:] + lst[:st]:
        if x['slug'] != slug and x['slug'] not in taken:
            return x
    return None
def related_html(a):
    s = a['slug']
    colls = [c for c in COLLECTIONS if s in [it[0] for it in c['items']]]
    qs = [q for q in QUESTIONS if any(a_ == s for sec in q['secs'] for a_, _ in sec[3])]
    picks, taken = [], set()
    def add(lst, label):
        x = _rel_next(lst, s, taken) if lst else None
        if x:
            picks.append((x, label)); taken.add(x['slug'])
    town = city_short(a)
    near = NEAR.get(town)
    kind = a.get('industry')
    c0 = colls[0] if colls else None
    cands = {
        'town_kind': ([x for x in A if city_short(x) == town and x.get('industry') == kind], f'{town}の{kind}'),
        'kind':      ([x for x in A if x.get('industry') == kind], REL_KIND_LABEL.format(kind=kind)),
        'town':      ([x for x in A if city_short(x) == town], f'同じ{town}エリア'),
        'near':      ([x for x in A if near and NEAR.get(city_short(x)) == near and city_short(x) != town], f'近くの{near}エリア'),
        'coll':      ([A_by[it[0]] for it in c0['items'] if it[0] in A_by] if c0 else [], f'特集「{c0["title"]}」から' if c0 else ''),
    }
    _cty = globals().get('COUNTRY', {}).get(s)
    cands['country'] = ([x for x in A if _cty and globals().get('COUNTRY', {}).get(x['slug']) == _cty], f'同じ{_REL_CN.get(_cty, _cty)}' if _cty else '')
    c1 = colls[1] if len(colls) > 1 else None
    cands['coll2'] = ([A_by[it[0]] for it in c1['items'] if it[0] in A_by] if c1 else [], f'特集「{c1["title"]}」から' if c1 else '')
    for key in REL_ORDER:
        lst, label = cands[key]
        if len(picks) < 3: add(lst, label)
    while len(picks) < 3:
        x = _rel_next(A, s, taken)
        if not x: break
        picks.append((x, f'ほかの{REL_NOUN}')); taken.add(x['slug'])
    out = '<section class="rel">'
    qline = (f'<p class="qchip">この質問でも紹介しています：<a href="../questions/{qs[0]["slug"]}.html">{E(qs[0]["q"])} &rarr;</a></p>' if qs else '')
    if colls:
        out += (f'<div class="rel-block"><p class="rel-h">{E(a["company"])}が載っている特集（{len(colls)}本）</p>'
                f'<div class="ccg rel-cc">' + ''.join(cc(c, '../') for c in colls[:3]) + '</div>' + qline + '</div>')
    elif qline:
        out += '<div class="rel-block">' + qline + '</div>'
    if picks:
        out += (f'<div class="rel-block"><p class="rel-h">次に見る{REL_NOUN}</p><div class="rel-grid">'
                + ''.join(f'<div class="rel-item"><p class="why">{E(lb)}</p>{card(x, "../", False)}</div>' for x, lb in picks)
                + '</div></div>')
    return out + '</section>\n'
REL_LOG = []
for _root, _ds, _fs in os.walk(OUT):
    for _f in _fs:
        if not _f.endswith('.html'): continue
        _p = os.path.join(_root, _f)
        _t = open(_p, encoding='utf-8').read()
        _m = re.search(r'<!--REL:([^>]+?)-->', _t)
        if not _m or _m.group(1) not in A_by: continue
        _h = related_html(A_by[_m.group(1)])
        REL_LOG.append(_m.group(1))
        open(_p, 'w', encoding='utf-8').write(_t.replace(_m.group(0), _h))
_css_p = OUT + 'assets/style.css'
if os.path.exists(_css_p) and '.rel-grid' not in open(_css_p, encoding='utf-8').read():
    open(_css_p, 'a', encoding='utf-8').write('\n/* 詳細ページ下のおすすめ 2026-09-29 */\n.rel{margin:10px 0 40px;display:grid;gap:44px}\n.rel-h{font-weight:600;font-size:13px;letter-spacing:.08em;color:var(--accent);margin:0 0 14px}\n.ccg.rel-cc{grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}\n.qchip{margin:16px 0 0;font-size:13px;color:var(--mute)}\n.qchip a{color:var(--ink);border-bottom:1px solid var(--accent);text-decoration:none}\n.rel-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}\n.why{margin:0 0 8px;font-size:12px;font-weight:600;color:var(--ink)}\n@media (max-width:700px){.ccg.rel-cc,.rel-grid{grid-template-columns:1fr}}\n')

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
