# 2026-09-28 About に「運営者情報」「広告について」「訂正について」を足す（Google AdSense の審査対策。福利厚生JP の /about と同じ型）
# build_mill.py / build_site.py の最後に exec で読み込む。OUT と（MILL なら）B が入っている前提
_B = globals().get('B') or dict(name='OFFISNAP', kana='オフィスナップ', domain='offisnap.com')
_abp = OUT + 'about/index.html'
_h = open(_abp, encoding='utf-8').read()
if 'id="ops"' not in _h:
    _lead = __import__('re').search(r'<p class="std">(.*?)</p>', _h)
    _lead = _lead.group(1) if _lead else ''
    _th = 'style="text-align:left;vertical-align:top;white-space:nowrap;padding:12px 16px 12px 0;border-bottom:1px solid var(--line,#ddd);font-weight:600"'
    _td = 'style="padding:12px 0;border-bottom:1px solid var(--line,#ddd)"'
    _rows = [('サイト名', f'{_B["name"]}（{_B["kana"]} / {_B["domain"]}）'),
             ('運営', f'{_B["name"]}運営'),
             ('連絡先', '<a href="../contact/">お問い合わせフォーム</a>よりご連絡ください'),
             ('サイト概要', _lead)]
    _tbl = '<table style="border-collapse:collapse;width:100%;margin:8px 0 0">' + ''.join(f'<tr><th {_th}>{k}</th><td {_td}>{v}</td></tr>' for k, v in _rows) + '</table>'
    _sec = (f'<section class="step" id="ops"><p class="no">02｜運営者情報</p><h2>運営者情報</h2>{_tbl}</section>'
            '<section class="step" id="ads"><p class="no">03｜広告について</p><h2>広告について</h2>'
            '<p>当サイトは、Google AdSense などの広告を掲載する場合があります。広告の有無や広告主が、掲載する内容や並び順に影響することはありません。</p></section>'
            '<section class="step" id="fix"><p class="no">04｜訂正について</p><h2>訂正について</h2>'
            '<p>掲載内容に誤りを見つけた場合は、<a href="../contact/">お問い合わせ</a>よりご連絡ください。確認のうえ、すみやかに修正します。掲載先のご担当者さまからの情報更新のご連絡も歓迎しています。</p></section>')
    _h = _h.replace('</article></div></main>', _sec + '</article></div></main>', 1)
    _h = _h.replace('<li><a href="#s1">編集方針</a></li></ol>', '<li><a href="#s1">編集方針</a></li><li><a href="#ops">運営者情報</a></li><li><a href="#ads">広告について</a></li><li><a href="#fix">訂正について</a></li></ol>', 1)
    _h = _h.replace(f'<title>{_B["name"]} について', f'<title>{_B["name"]} について・運営者情報', 1)
    open(_abp, 'w', encoding='utf-8').write(_h)
    print('about_ops ok')
