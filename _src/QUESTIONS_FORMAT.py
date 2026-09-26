# Q&A のデータ形式（WALL の questions.py と同じ考え方。build_site.py が読む）
# 各質問:
#   slug  : 英小文字とハイフン（URL になる）
#   q     : 質問文（「〜の？」で終わる。検索で打たれる言葉を入れる）
#   a     : 短い答え（2〜3文。太字で最初に出る。結論を先に）
#   desc  : メタ説明（1文。a と同じでもよい）
#   secs  : 根拠になる施設のセクション 3〜5個。(施設slug, 見出し, [本文の段落2つ], [(施設slug, 写真番号), ...])
#           写真番号はその施設の IMG のキー（記事データの hero か steps で使っている番号だけ）。1〜3枚
#   ctx   : キーワード（dict term/yomi/title/body）または None
#   items : 「この答えに出てくる施設」のカードに出す施設slug（secs の施設と同じ順）
# 事実は各施設の記事データ（facts・concept・steps の本文）にあることだけ。推測しない。数字は記事のまま。
# 書き方: 敬体。一文短く。ひらがな開きしない。読む人に指図しない。棘のある言葉を使わない。
QUESTIONS = [
 dict(slug='roastery', q='「焙煎所のあるカフェ」は、ふつうのカフェと何が違うの？',
      a='豆を焼く場所と飲む場所が、同じ建物にあります。焙煎の機械と香りが店の風景になり、できたての豆をその場で買えます。',
      desc='焙煎所のあるカフェの見どころを、Blue Bottle 清澄白河・Starbucks Reserve Roastery・Dandelion Chocolate の公式情報から。',
      secs=[
       ('blue-bottle-kiyosumi', '倉庫の中に、焙煎所とカフェを並べる',
        ['Blue Bottle Coffee 清澄白河は、倉庫を焙煎所つきのカフェにした店です。客席から焙煎の機械が見えます。', '焙煎した豆はこの店から都内の店へ運ばれます。作る場所を隠さない造りが、この店の性格です。'],
        [('blue-bottle-kiyosumi', 3), ('blue-bottle-kiyosumi', 4)]),
       ('starbucks-reserve-roastery-tokyo', '17mの豆の塔を、4階から見下ろす',
        ['Starbucks Reserve Roastery Tokyo の中心には、高さ17mの豆の塔があります。焙煎した豆が塔の中を通って運ばれます。', '4階建ての建物のどの階からも塔が見えます。焙煎所そのものを建物の主役にした例です。'],
        [('starbucks-reserve-roastery-tokyo', 2)]),
       ('dandelion-chocolate-kuramae', '1階が工場、2階がカフェ',
        ['Dandelion Chocolate 蔵前は、1階がチョコレートの工場、2階がカフェです。', 'コーヒーではなくカカオ豆ですが、作る場所と食べる場所を重ねる考え方は同じです。'],
        [('dandelion-chocolate-kuramae', 2)]),
      ],
      ctx=dict(term='Roastery', yomi='ロースタリー', title='焙煎所とは', body=['生のコーヒー豆を焼いて、飲める豆にする場所です。', 'カフェに焙煎所があると、豆の鮮度を店で決められます。香りと音が加わるので、店の体験も変わります。']),
      items=['blue-bottle-kiyosumi', 'starbucks-reserve-roastery-tokyo', 'dandelion-chocolate-kuramae']),
]
