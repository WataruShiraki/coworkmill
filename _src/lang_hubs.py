# -*- coding: utf-8 -*-
# 2026-10-11 COWORKMILL 中国語（簡体字）・韓国語の入口ページ（わたるさん「インバウンド向けのコワーキングサイトNo1」の項目4）
# 施設ページは英語のまま。入口ページで「使い方」「地域」「日帰りで使える施設」を母語で案内し、英語の施設ページへつなぐ
# build_en.py から exec される（EN・JA・TRAIT・ORDER・POPULAR・card・head・nav・foot・U・E・photo・pref・town を使う）
# 中身は施設データ（公式サイト由来）から自動で作る。数字や事実を新しく書き足さない
LANGS = {
 'zh': dict(lang='zh-Hans', loc='zh_CN', name='简体中文',
  title='日本联合办公空间指南：日票、营业时间、交通 | COWORKMILL',
  desc='COWORKMILL 收录日本{n}家注重设计的联合办公空间。价格、营业时间、交通方式均来自各空间官网，详情页为英文并附日文地址。',
  h1='在日本找联合办公空间',
  lead='COWORKMILL 收录日本{n}家注重室内设计的联合办公空间（coworking space）。价格、营业时间、交通方式等信息全部来自各空间的官方网站，照片也是官方照片。各空间的详情页为英文，并附有日文地址，可以直接给出租车司机或前台看。',
  how_h='第一次使用前要知道的三件事',
  how=[('日票与按小时付费','很多空间不需要成为会员，可以按小时或按天使用（英文页面上标有 “Day pass”）。也有只对会员或法人开放的空间（标有 “Members only”）。'),
       ('首次登记与证件','有的空间第一次使用时需要在前台登记，并出示带照片的身份证件；有的需要先在网上注册。请在详情页的 “How” 一栏确认。'),
       ('付款方式','有的空间只接受信用卡、交通IC卡等无现金支付，不收现金。请在详情页的 “Pay” 一栏确认。')],
  city_h='按地区查找', pick_h='东京以外，不用预约、按天就能用的空间', pop_h='人气空间',
  q_h='常见问题（英文）', all_l='查看全部{n}家空间（英文）', note='详情页为英文。地址附日文，可复制或放大显示。',
  tr={'Day pass':'可按天使用','English website':'有英文网站','24-hour access':'24小时','Open weekends':'周末营业','Phone booths':'电话间','Open late':'营业到很晚','Members only':'仅限会员','Station-linked':'车站直通'},
  pref={'Tokyo':'东京','Kanagawa':'横滨・神奈川','Osaka':'大阪','Kyoto':'京都','Fukuoka':'福冈','Hokkaido':'札幌・北海道','Okinawa':'冲绳','Chiba':'千叶','Saitama':'埼玉'},
  qs={'outside-tokyo':'在东京以外，哪里可以按天使用？','drop-in':'可以不预约直接去吗？','id-registration':'按天使用需要证件或登记吗？','payment':'可以用什么方式付款？','english':'有英文服务的空间吗？','weekly-pass':'有适合旅行者的周票吗？','24h':'有24小时开放的空间吗？'}),
 'ko': dict(lang='ko', loc='ko_KR', name='한국어',
  title='일본 코워킹 스페이스 가이드: 일일권·영업시간·가는 길 | COWORKMILL',
  desc='COWORKMILL은 디자인이 좋은 일본의 코워킹 스페이스 {n}곳을 소개합니다. 가격·영업시간·가는 길은 모두 각 공식 사이트 기준이며, 상세 페이지는 영어와 일본어 주소로 안내합니다.',
  h1='일본에서 코워킹 스페이스 찾기',
  lead='COWORKMILL은 인테리어가 좋은 일본의 코워킹 스페이스 {n}곳을 소개합니다. 가격, 영업시간, 가는 길 등은 모두 각 스페이스의 공식 사이트에서 가져왔고, 사진도 공식 사진입니다. 상세 페이지는 영어이며, 일본어 주소가 있어 택시 기사나 접수처에 그대로 보여줄 수 있습니다.',
  how_h='처음 이용하기 전에 알아둘 세 가지',
  how=[('일일권과 시간제','회원이 아니어도 시간 단위나 하루 단위로 쓸 수 있는 곳이 많습니다(영어 페이지에 “Day pass” 표시). 회원이나 법인만 쓸 수 있는 곳도 있습니다(“Members only” 표시).'),
       ('첫 방문 등록과 신분증','처음 이용할 때 접수처에서 등록하고 사진이 있는 신분증을 보여 달라는 곳도 있고, 미리 온라인으로 가입해야 하는 곳도 있습니다. 상세 페이지의 “How” 항목에서 확인하세요.'),
       ('결제 방법','신용카드나 교통 IC 카드 같은 캐시리스 결제만 받고 현금은 받지 않는 곳도 있습니다. 상세 페이지의 “Pay” 항목에서 확인하세요.')],
  city_h='지역별로 찾기', pick_h='도쿄 밖에서 예약 없이 하루 단위로 쓸 수 있는 곳', pop_h='인기 스페이스',
  q_h='자주 묻는 질문(영어)', all_l='전체 {n}곳 보기(영어)', note='상세 페이지는 영어입니다. 일본어 주소를 복사하거나 크게 띄울 수 있습니다.',
  tr={'Day pass':'일일 이용 가능','English website':'영어 웹사이트','24-hour access':'24시간','Open weekends':'주말 영업','Phone booths':'전화 부스','Open late':'늦게까지 영업','Members only':'회원 전용','Station-linked':'역 직결'},
  pref={'Tokyo':'도쿄','Kanagawa':'요코하마・가나가와','Osaka':'오사카','Kyoto':'교토','Fukuoka':'후쿠오카','Hokkaido':'삿포로・홋카이도','Okinawa':'오키나와','Chiba':'지바','Saitama':'사이타마'},
  qs={'outside-tokyo':'도쿄 밖에서 하루 단위로 쓸 수 있는 곳은?','drop-in':'예약 없이 바로 가도 되나요?','id-registration':'일일 이용에 신분증이나 등록이 필요한가요?','payment':'결제는 어떻게 하나요?','english':'영어가 통하는 곳이 있나요?','weekly-pass':'여행자용 주간 이용권이 있나요?','24h':'24시간 여는 곳이 있나요?'}),
}
_PREF_PAGE = {'Tokyo': 'tokyo', 'Kanagawa': 'kanagawa', 'Osaka': 'osaka', 'Kyoto': 'kyoto', 'Fukuoka': 'fukuoka', 'Hokkaido': 'hokkaido', 'Okinawa': 'okinawa', 'Chiba': 'chiba', 'Saitama': 'saitama'}
def _lcard(slug, L):
    e = EN[slug]; img = photo(slug, JA[slug]['hero'][0])
    tr = ''.join(f'<span>{E(L["tr"].get(t, t))}</span>' for t in TRAIT[slug][:3])
    return (f'<a class="card" href="{U("spaces/" + slug + ".html")}" hreflang="en"><div class="ph">{f"""<img src="{E(img)}" alt="{E(e["name"])}" loading="lazy">""" if img else ""}</div>'
            f'<div class="k">{E(L["pref"].get(pref(e), pref(e)))} · {E(town(e))}</div><b>{E(e["name"])}</b>' + (f'<div class="chips">{tr}</div>' if tr else '') + '</a>')
def _alts():
    return ('<link rel="alternate" hreflang="en" href="https://cowkml.com/"><link rel="alternate" hreflang="x-default" href="https://cowkml.com/">'
            + ''.join(f'<link rel="alternate" hreflang="{v["lang"]}" href="https://cowkml.com/{k}/">' for k, v in LANGS.items()))
def lang_page(k):
    L = LANGS[k]; n = len(ORDER); path = f'{k}/index.html'
    cnt = collections.Counter(pref(EN[s]) for s in ORDER)
    cities = ''.join(f'<a href="{U("find/" + _PREF_PAGE[p] + ".html")}" hreflang="en">{E(L["pref"][p])}<span>{cnt[p]}</span></a>' for p in _PREF_PAGE if cnt.get(p))
    picks = [s for s in ORDER if pref(EN[s]) != 'Tokyo' and 'Day pass' in TRAIT[s] and 'Members only' not in TRAIT[s]][:8]
    pops = [s for s in POPULAR if s in EN and 'Members only' not in TRAIT[s]][:8]
    how = ''.join(f'<li><b>{E(t)}</b><p>{E(b)}</p></li>' for t, b in L['how'])
    qs = ''.join(f'<li><a href="{U("questions/" + qk + ".html")}" hreflang="en">{E(qt)}</a></li>' for qk, qt in L['qs'].items() if any(q['slug'] == qk for q in QS))
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": L['h1'], "inLanguage": L['lang'], "url": f'https://cowkml.com/{k}/'}]
    h = head(L['title'], L['desc'].format(n=n), path, None, 'website', ld)
    h = h.replace('<html lang="en">', f'<html lang="{L["lang"]}">', 1).replace('content="en_US"', f'content="{L["loc"]}"', 1).replace('</head>', _alts() + '</head>', 1)
    return (h + nav('') +
            f'<main class="wrap"><div class="head"><p class="tag">{E(L["name"])}</p><h1>{E(L["h1"])}</h1><p class="lead">{E(L["lead"].format(n=n))}</p></div>'
            f'<section class="lh"><h2>{E(L["how_h"])}</h2><ol class="lhow">{how}</ol></section>'
            f'<section class="lh"><h2>{E(L["city_h"])}</h2><div class="areas">{cities}</div></section>'
            f'<section class="lh"><h2>{E(L["pick_h"])}</h2><div class="cards">' + ''.join(_lcard(s, L) for s in picks) + '</div></section>'
            f'<section class="lh"><h2>{E(L["pop_h"])}</h2><div class="cards">' + ''.join(_lcard(s, L) for s in pops) + '</div></section>'
            f'<section class="lh"><h2>{E(L["q_h"])}</h2><ul class="lq">{qs}</ul></section>'
            f'<p class="note">{E(L["note"])}</p><p class="more"><a href="{U("spaces/")}" hreflang="en">{E(L["all_l"].format(n=n))} →</a></p></main>' + foot())
LANG_PAGES = [(f'{k}/index.html', lang_page(k)) for k in LANGS]
LANG_LINKS = ''.join(f'<a href="{U(k + "/")}" hreflang="{v["lang"]}" lang="{v["lang"]}">{v["name"]}</a>' for k, v in LANGS.items())
