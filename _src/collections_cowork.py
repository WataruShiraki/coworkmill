# 特集（3施設以上に共通することがあれば特集にする。一言は各記事の本文にある事実だけ）
COLLECTIONS = [
 dict(slug='shibuya', title='渋谷のコワーキングスペース', lead='実験区、問いの場所、駅直結の高層階。渋谷の駅まわりに集まる3施設です。',
      items=[('100banch','35歳未満の100プロジェクトが実験する'),('shibuya-qws','スクランブル交差点の上、約2,600㎡'),('wework-shibuya-scramble-square','渋谷駅直結の高層階、会議室70室')]),
 dict(slug='incubation', title='新しい事業を生む場所', lead='大企業の新規事業、日本最大級のキャンパス、失敗を恐れないコミュニティ。事業づくりのための施設です。',
      items=[('toranomon-hills-arch','大企業の新規事業だけを集めた、世界初のインキュベーションセンター'),('co-lab-shibuya-cast','渋谷キャストの中、24時間使えるクリエイターの拠点'),('saai-yurakucho','畳と会員バーのある事業創造コミュニティ'),('shibuya-qws','「問い」から始める場所')]),
 dict(slug='reuse', title='建物をそのまま生かす', lead='蔦に覆われた廃屋、1棟まるごと、1,573㎡の2フロア。あるものを生かした施設です。',
      items=[('midori-so-nakameguro','蔦に覆われた廃屋を、2棟のシェアオフィスに'),('lifork-otemachi','大手町の駅直結、13タイプのシェアオフィス'),('co-ba-ebisu','「働き方解放区」、1,573㎡の2フロア'),('business-airport-aoyama','外苑前3分、青山の4階と6階')]),
 dict(slug='marunouchi', title='丸の内・有楽町・大手町のコワーキングスペース', lead='東京駅のまわりには、東京都、三菱地所、NTT都市開発、大企業の共同体と、つくり手の違う4施設が集まっています。',
      items=[('point-0-marunouchi','丸ビルの隣、大企業19社が共同で運営する実証実験のオフィス'),('tokyo-innovation-base','有楽町駅から1分、東京都が運営するスタートアップ支援の拠点'),('saai-yurakucho','新東京ビルの3フロア、畳と会員バーのある事業創造コミュニティ'),('lifork-otemachi','大手町駅直結、4〜30名用のシェアオフィス13タイプ')]),
 dict(slug='toranomon-azabudai', title='虎ノ門・麻布台のコワーキングスペース', lead='虎ノ門ヒルズと麻布台ヒルズ。森ビルの2つの街に、新規事業、スタートアップ、ベンチャーキャピタルの拠点が集まっています。',
      items=[('toranomon-hills-arch','虎ノ門ヒルズ ビジネスタワー4階、3,800㎡のインキュベーションセンター'),('cic-tokyo','同じビルの15・16階、約6,000㎡に325社以上が入居'),('tokyo-venture-capital-hub','麻布台ヒルズ、VC約70社が集まる日本初の拠点')]),
 dict(slug='station-direct', title='駅直結のコワーキングスペース', lead='改札から外に出ずに着く施設です。雨の日も、打ち合わせの前後も移動が短くすみます。',
      items=[('lifork-otemachi','大手町駅直結、大手町ファーストスクエアの1・2階'),('wework-shibuya-scramble-square','渋谷駅直結、渋谷スクランブルスクエアの37〜42階と45階'),('cic-tokyo','虎ノ門ヒルズ駅直結、虎ノ門ヒルズ ビジネスタワーの15・16階'),('tokyo-venture-capital-hub','神谷町駅直結、麻布台ヒルズ ガーデンプラザBの4・5階')]),
 dict(slug='24hours', title='24時間使えるコワーキングスペース', lead='締め切り前の夜も、早朝の海外との会議も。公式サイトに「24時間365日」と書かれている施設です。',
      items=[('co-lab-shibuya-cast','渋谷キャストの1・2階、クリエイターのためのシェアオフィス'),('lifork-otemachi','シェアオフィスは24時間365日、大手町駅直結'),('cic-tokyo','365日24時間、プライベートオフィス163室')]),
 dict(slug='large-floor', title='広さで選ぶ、大きなコワーキングスペース', lead='約6,000㎡から1,573㎡まで。フロアが広い施設は、会議室やイベントの場所も一緒にそろっています。',
      items=[('cic-tokyo','約6,000㎡、プライベートオフィス163室と100席のコワーキング'),('toranomon-hills-arch','3,800㎡、ガラス張りのマグネットルームとカフェ＆ラウンジ'),('shibuya-qws','約2,600㎡、200名規模の SCRAMBLE HALL'),('co-ba-ebisu','1,573㎡の2フロア、1階がコワーキングで2階が個室')]),
 dict(slug='corporate-public', title='企業や行政がつくった場所', lead='不動産会社だけでなく、メーカーや東京都もコワーキングスペースをつくっています。つくった側の目的が、場所の性格に表れます。',
      items=[('100banch','パナソニックの創業100周年を機に開いた実験区'),('tokyo-innovation-base','東京都が運営する「世界中のイノベーションの結節点」'),('point-0-marunouchi','ダイキン、オカムラ、パナソニックなど19社が参画'),('toranomon-hills-arch','森ビルが企画運営、大企業の新規事業のための施設')]),
]
QA = dict(slug='q-community', q='コワーキングスペースには、どんな「人をつなぐ仕組み」があるの？',
  a='会員だけの集まり、コミュニティマネージャー、会員バー。席を貸すだけではなく、人と人が出会う仕組みを持つ施設が増えています。',
  secs=[('co-lab-shibuya-cast','クリエイターだけが集まる、24時間の拠点','co-lab 渋谷キャストは、クリエイターのための会員制の拠点です。同じ職種の人が同じ場所にいることが、仕事のつながりになります。'),
        ('business-airport-aoyama','コミュニティマネージャーが人をつなぐ','Business Airport 青山には、会員同士や会員と施設をつなぐコミュニティマネージャーがいます。席を借りるだけでは生まれない出会いを、人が担っています。'),
        ('saai-yurakucho','畳と会員バーで、肩の力を抜いて話す','有楽町 SAAI には畳の場所と会員バーがあります。「失敗なんて無い」という合言葉のもと、事業の相談を肩の力を抜いてできる場所です。'),
        ('100banch','100のプロジェクトが同じ場所で実験する','100BANCH では35歳未満の100のプロジェクトが同じフロアで活動します。隣のプロジェクトが自然に見えることが、いちばんの仕組みです。')])

# ==== 2026-09-27 特集を10本追加（110施設になったため）。一言は各記事の本文・基本情報にある事実だけ ====
_EXT = {
 'shibuya': [('workstyling-shibuya-sakurastage','渋谷駅から1分、最大108名のオープンスペース'),('business-airport-shibuya-fukuras','渋谷フクラス17階'),('business-airport-shibuya-sakurastage','渋谷サクラステージ7階'),('midori-so-shibuya','桜丘の4つの階にワークスペースとライブラリ'),('andwork-shibuya','ホテルのロビーが仕事場に'),('crosscoop-shibuya-nextsite','植栽を配したラウンジ'),('fabbit-shibuya-ekimae','渋谷駅から2分、同じフロアに TKP の会議室')],
 'marunouchi': [('egg-japan-marunouchi','新丸ビル10階、起業家が集まる場所'),('global-business-hub-tokyo','大手町フィナンシャルシティの家具付き50区画'),('3x3lab-future','竹の机、杉の床、板倉構法'),('business-airport-tokyo','日本生命丸の内ガーデンタワー3階'),('workstyling-otemachi','芸術作品をモチーフにした会議室'),('workstyling-yaesu-kitaguchi','東京駅直結の17階')],
 'station-direct': [('workstyling-tokyo-midtown-yaesu','東京駅の地下から直結'),('workstyling-yaesu-kitaguchi','東京駅直結、グラントウキョウノースタワー17階'),('workstyling-nihonbashi-takashimaya-mitsui','日本橋駅直結の9階'),('workstyling-nihonbashi-ichome','日本橋駅直結の5階'),('workstyling-shinjuku-higashiguchi','丸ノ内線 新宿駅B12出口に直結'),('workstyling-tokyo-midtown-roppongi','六本木駅8番出口直結の18階')],
 '24hours': [('co-ba-akasaka','溜池山王駅1分、24時間'),('global-business-hub-tokyo','家具付きオフィス50区画、24時間'),('birth-work-azabujuban','年中無休、24時間入退出')],
 'reuse': [('midori-so-bakuroyokoyama','昭和のビル7階分を、カフェと工房と屋上の畑に'),('the-hub-nihonbashi-kabutocho','SOHO物件を大胆にリニューアル')],
}
for _c in COLLECTIONS:
    _have = {x[0] for x in _c['items']}
    _c['items'] += [x for x in _EXT.get(_c['slug'], []) if x[0] not in _have]

COLLECTIONS += [
 dict(slug='nihonbashi-yaesu', title='日本橋・京橋・八重洲のコワーキングスペース', lead='宇宙ビジネスの拠点、地域と東京をつなぐラウンジ、FOOD INNOVATION。東京駅の東側に集まる施設です。',
      items=[('x-nihonbashi-tower','日本橋三井タワー7階、宇宙ビジネスの共創拠点'),('potluck-yaesu','東京ミッドタウン八重洲5階、地域と東京をつなぐ'),('senq-kyobashi','京橋エドグラン、テーマは FOOD INNOVATION'),('diagonal-run-tokyo','人と企業とアイデアが斜めに交わる'),('business-airport-nihonbashi','五街道の起点を思わせる内装'),('business-airport-kyobashi','職人の街を、優しい和テイストで'),('workstyling-nihonbashi-mitsui-tower','テーマの違う9つの会議室'),('crosscoop-nihonbashi','約43席のラウンジ')]),
 dict(slug='shinjuku', title='新宿のコワーキングスペース', lead='コーヒーの香るワーキングカフェ、RETRO FUTURE の11階、24時間のラウンジ。駅の東西に広がる新宿の施設です。',
      items=[('base-point-shinjuku','1階はコーヒーの香る時間制のワーキングカフェ'),('workstyling-shinjuku-mitsui-building','過去と未来を横断する「RETRO FUTURE」'),('workstyling-shinjuku-higashiguchi','新宿駅B12出口に直結'),('h1t-shinjuku-nishiguchi','個室18室と会議室7室'),('crosscoop-shinjuku-avenue','7階に24時間のラウンジ'),('crosscoop-shinjuku','会議室15室のハイグレード個室'),('business-airport-shinjuku3chome','街を行く人の多様性を表した空間')]),
 dict(slug='aoyama-omotesando', title='青山・表参道のコワーキングスペース', lead='CREATOR\'S VILLAGE、固定の机を置かない会員制、屋上の庭。デザインの街にあるワークスペースです。',
      items=[('senq-aoyama','テーマは CREATOR\'S VILLAGE'),('senq-aoyama-namikidori','テーマは BUILD NEXT CULTURES'),('midori-so-aoyama','固定の机を置かず「会う」ことから考える'),('business-airport-aoyama','外苑前3分、4階と6階'),('workstyling-omotesando','平日は22時30分まで'),('h1t-omotesando','表参道駅から2分、個室15室'),('crosscoop-aoyama','外苑前駅2分のシェアオフィス'),('fabbit-aoyama-itchome','青山タワープレイス8階')]),
 dict(slug='high-floor', title='眺めのいい高層階のコワーキングスペース', lead='45階、東京タワーを望む34階、霞が関ビルの36階。窓の外まで仕事場にした施設です。',
      items=[('wework-shibuya-scramble-square','渋谷スクランブルスクエアの37〜42階と45階'),('hills-house-azabudai','森JPタワー33・34階、東京タワーを望む'),('workstyling-kasumigaseki-building','霞が関ビルディング36階'),('business-airport-shinagawa','太陽生命品川ビル28階'),('workstyling-tokyo-midtown-roppongi','東京ミッドタウン・タワー18階'),('business-airport-shibuya-fukuras','渋谷フクラス17階'),('workstyling-yaesu-kitaguchi','グラントウキョウノースタワー17階'),('cic-tokyo','虎ノ門ヒルズの15・16階')]),
 dict(slug='weekend', title='土日も使えるコワーキングスペース', lead='土日も朝8時から夜22時まで、毎日朝7時から、毎日夜23時まで。週末に仕事をする日にも開いている施設です。',
      items=[('workstyling-yaesu-minamiguchi','平日・土日とも8時〜22時'),('workstyling-ginza','平日・土日祝とも8時〜22時'),('h1t-shinjuku-nishiguchi','全日7時〜22時'),('h1t-ikebukuro-higashiguchi-the-garden','土日祝も7時〜22時30分'),('h1t-roppongi','土日祝も7時30分〜22時'),('midori-so-kichijoji','毎日8時〜23時'),('workstyling-shibuya-sakurastage','土日祝は10時〜18時'),('base-point-shinjuku','全日7時〜23時')]),
 dict(slug='solo', title='ひとりで集中できるコワーキングスペース', lead='1名用の個室18室、ソロブース26室、「集中」のフロア。ひとりの仕事のためにつくられた場所です。',
      items=[('h1t-ikebukuro-higashiguchi-the-garden','定員1名のルームが18室'),('h1t-shinjuku-nishiguchi','1名用のルーム18室とボックス'),('h1t-ochanomizu-the-garden','定員1名のルームが11室'),('workstyling-shinagawa','極上のソロワークができる、働くための巣'),('senq-meguro','ソロブース26室'),('birth-work-azabujuban','5階は「集中」のフロア'),('birth-work-toranomon','自宅の書斎のような集中ゾーン')]),
 dict(slug='hotel', title='ホテルの中のコワーキングスペース', lead='ロビー、ラウンジ、最上階のバー、泊まれる部屋。ホテルの中で働ける施設です。',
      items=[('andwork-shibuya','The Millennials 渋谷のロビーが仕事場に'),('andwork-azabujuban','THE LIVELY 東京麻布十番、最上階にバー'),('andwork-shibuya-higashi','HOTEL GRAPHY 渋谷の1階、カフェ兼コワーキング'),('midori-so-nihonbashi','働くことと泊まることが同じ建物に')]),
 dict(slug='design-theme', title='内装にテーマのあるコワーキングスペース', lead='伝統文様の ZEN MODERN、RETRO FUTURE、劇場、鉄道、五街道。街や物語を内装に取り入れた施設です。',
      items=[('workstyling-tokyo-midtown-hibiya','日本の伝統文様をあしらった「ZEN MODERN」'),('workstyling-shinjuku-mitsui-building','過去と未来を横断する「RETRO FUTURE」'),('workstyling-shiodome-city-center','駅舎のようなエントランスと緑の「INDUSTRY+FOREST」'),('workstyling-otemachi','世界の芸術作品をモチーフにした会議室'),('business-airport-hibiya','劇場をモチーフに、緑と芸術に囲まれて'),('business-airport-shimbashi','鉄道発祥の地を思わせるモチーフ'),('business-airport-nihonbashi','五街道の起点を思わせる内装'),('business-airport-kyobashi','職人の街を、優しい和テイストで'),('business-airport-ebisu','恵比寿の街を柔らかな曲線で')]),
 dict(slug='rooftop', title='屋上やテラスのあるコワーキングスペース', lead='9階のスカイテラス、屋上の畑、屋上の庭。外の空気を吸える場所がある施設です。',
      items=[('senq-roppongi','新六本木ビル9階のスカイテラス'),('the-hub-nihonbashi-kabutocho','全室完全個室と屋上テラス'),('the-hub-ginza-oct','一棟まるごとのシェアオフィスと屋上テラス'),('midori-so-bakuroyokoyama','昭和のビルの屋上に畑'),('midori-so-aoyama','3階の会員エリアと屋上の庭')]),
 dict(slug='midori-so', title='MIDORI.so の拠点', lead='蔦の廃屋、1棟まるごとの旗艦拠点、泊まれる建物、商業ビルの8階。同じ運営会社が、建物ごとに違う場所をつくっています。',
      items=[('midori-so-nakameguro','蔦に覆われた廃屋を、2棟のシェアオフィスに'),('midori-so-nagatacho','地下1階から6階まで1棟丸ごと'),('midori-so-bakuroyokoyama','カフェ、印刷の工房、ギャラリー、屋上の畑'),('midori-so-shibuya','桜丘の4つの階'),('midori-so-aoyama','固定の机を置かない'),('midori-so-ikejiri','WEST・CENTRAL・EAST の3つの棟'),('midori-so-kichijoji','吉祥寺PARCOの8階'),('midori-so-nihonbashi','働くことと泊まることが同じ建物に')]),
]

# ==== 2026-09-28 人の顔が分かる写真を外した結果、保留にした施設は特集からも外す ====
_GONE_FACE = {'andwork-shibuya-higashi', 'wework-tokyo-square-garden', 'base-point-shinjuku', 'the-hub-shimbashi', 'the-hub-toranomon', 'midori-so-ikejiri', 'the-hub-takadanobaba', 'tokyo-innovation-base', 'saai-yurakucho', 'hills-house-azabudai', 'the-hub-nihonbashi-kayabacho', 'the-hub-meguro', 'tokyo-venture-capital-hub', 'the-hub-kayabacho', 'the-hub-ginza-6chome', 'wework-ginza-six', 'the-hub-hanzomon', 'the-hub-ginza-oct', 'the-hub-nihonbashi-odenmacho'}
for _c in COLLECTIONS:
    _c['items'] = [x for x in _c['items'] if x[0] not in _GONE_FACE]
QA['secs'] = [s for s in QA['secs'] if s[0] not in _GONE_FACE]


# ==== 2026-09-30 地域×テーマの特集を追加（わたるさん指示「地域＋〇〇の特集をがんがん」）。一言は各記事のタイトルにある事実だけ ====
_EXT30 = {"shibuya": [["co-lab-shibuya-cast", "つくる人が集まる1・2階のシェアオフィス"],
 ["justco-shibuya-hikarie", "渋谷駅直結の33階"],
 ["newwork-shibuya-goto-ikueikai-building", "93席の旗艦店"],
 ["the-executive-centre-cerulean-tower", "茶室に着想を得た受付"],
 ["workstyling-shibuya", "渋谷駅東口から徒歩4分"],
 ["business-airport-shibuya-nanpeidai", "SHIBUYA SOLASTA 3階"],
 ["crosscoop-shibuya", "宮益坂の30席のラウンジ"]],
 "shinjuku": [["justco-shinjuku-miraina-tower", "新宿駅直結の18階"],
 ["wework-d-tower-nishishinjuku", "モダニズムと木の濃淡"]]}
for _c in COLLECTIONS:
    _have = {x[0] for x in _c['items']}
    _c['items'] += [tuple(x) for x in _EXT30.get(_c['slug'], []) if x[0] not in _have]
COLLECTIONS += [ { "slug": "shibuya-high-floor", "title": "渋谷の高層階のコワーキングスペース", "lead": "地上47階、ヒカリエ33階、駅前の17階、スクランブル交差点を見下ろす15階。渋谷の街を見下ろせる施設です。", "items": [[ "wework-shibuya-scramble-square", "地上47階、窓際ラウンジから渋谷を見下ろす" ], [ "justco-shibuya-hikarie", "渋谷駅直結の33階" ], [ "business-airport-shibuya-fukuras", "駅前の17階" ], [ "shibuya-qws", "スクランブル交差点を見下ろす15階の会員制施設" ] ] }, { "slug": "ebisu-meguro", "title": "恵比寿・目黒・中目黒のコワーキングスペース", "lead": "約1,600㎡の「働き方解放区」、150名のカンファレンスルーム、目黒川を見下ろす7階、蔦の廃屋を直した2棟。恵比寿から目黒までの施設です。", "items": [[ "co-ba-ebisu", "「働き方解放区」、約1,600㎡の2フロア" ], [ "business-airport-ebisu", "柔らかな曲線の基地" ], [ "workstyling-ebisu", "150名のカンファレンスルーム" ], [ "newwork-ebisu", "西口3分の39席" ], [ "the-executive-centre-meguro-arco-tower", "目黒川を見下ろす7階" ], [ "midori-so-nakameguro", "蔦に覆われた廃屋を直した2棟のシェアオフィス" ], [ "workstyling-meguro", "目黒駅から徒歩1分" ], [ "senq-meguro", "暮らしながら働く8階" ], [ "workstyling-nakameguro", "中目黒駅から徒歩2分" ], [ "business-airport-daikanyama", "緑に囲まれた3階" ] ] }, { "slug": "roppongi-azabu", "title": "六本木・麻布十番のコワーキングスペース", "lead": "9階のスカイテラス、オークと障子風の会議室、隈研吾設計の木の輪の森、大人の隠れ家。六本木から麻布十番までの施設です。", "items": [[ "senq-roppongi", "9階のスカイテラス" ], [ "the-executive-centre-roppongi-hills", "オークと障子風の会議室" ], [ "workstyling-tokyo-midtown-roppongi", "アートを加えた空間" ], [ "wework-ark-hills-south", "アメリカンと華やかさ" ], [ "crosscoop-roppongi-next", "60席のラウンジ" ], [ "h1t-roppongi", "駅から徒歩1分、席の種類が多い" ], [ "share-m-10", "隈研吾設計、木の輪の森" ], [ "andwork-azabujuban", "大人の隠れ家的オフィス" ], [ "birth-work-azabujuban", "集中と憩いの3フロア" ] ] }, { "slug": "ginza-shimbashi", "title": "銀座・新橋・汐留のコワーキングスペース", "lead": "GINZA SIX の最上階と屋上庭園、一棟まるごとのシェアオフィス、鉄道発祥の地のモチーフ、イタリア街。銀座から汐留までの施設です。", "items": [[ "workstyling-ginza", "銀座駅1分、土日も営業" ], [ "fabbit-ginza", "銀座一丁目のコワーキングラウンジ" ], [ "newwork-ginza", "銀座と新橋のあいだの2階" ], [ "business-airport-shimbashi", "鉄道発祥の地のモチーフ" ], [ "crosscoop-shimbashi", "約96席のラウンジと個室" ], [ "workstyling-shinbashi", "新橋駅徒歩1分" ], [ "the-hub-shiodome", "イタリア街の1棟オフィス" ], [ "workstyling-shiodome-city-center", "INDUSTRY+FOREST" ] ] }, { "slug": "kanda-akihabara", "title": "神田・秋葉原・御茶ノ水・神保町のコワーキングスペース", "lead": "電気街と昔のゲーム、本の街の手描きアート、レトロと新しさ、駅から徒歩1分の個室。神田のまわりの施設です。", "items": [[ "wework-kanda-square", "電気街と昔のゲーム" ], [ "wework-jimbocho", "本の街の手描きアート" ], [ "business-airport-kanda", "レトロと新しさの共存" ], [ "birth-work-kanda", "成長型フリーワーキングオフィス" ], [ "newwork-akihabara", "駅1分・土日祝も開く10階" ], [ "h1t-ochanomizu-the-garden", "駅から徒歩1分の個室" ], [ "workstyling-iidabashi-grand-bloom", "2階と9階" ], [ "h1t-iidabashi", "ビルの16階、緑の大きなテーブルがある飯田橋の拠点" ] ] }, { "slug": "shinagawa-hamamatsucho", "title": "品川・田町・浜松町のコワーキングスペース", "lead": "28階の太陽生命品川ビル、芝浦のスケルトン空間、東京湾を望む17階、東京湾の水上空港。品川から浜松町までの施設です。", "items": [[ "business-airport-shinagawa", "太陽生命品川ビル28階" ], [ "workstyling-shinagawa", "働くための巣" ], [ "co-ba-re-sohko-tamachi", "芝浦のスケルトン空間" ], [ "business-airport-tamachi", "格式あるオフィスを継ぐ" ], [ "workstyling-tamachi-mitaguchi", "田町・三田から徒歩1分" ], [ "the-executive-centre-world-trade-center-south-tower", "東京湾を望む17階" ], [ "workstyling-hamamatsucho", "浜松町・大門から徒歩2分" ], [ "newwork-daimon-hamamatsucho", "大門駅1分の4階" ], [ "business-airport-takeshiba", "東京湾の水上空港" ], [ "the-hub-takanawa", "泉岳寺4分、進化と落ち着きの拠点" ] ] }, { "slug": "tama-chuo-line", "title": "中央線・多摩エリアのコワーキングスペース", "lead": "吉祥寺PARCOの8階、調布駅1分、立川駅南口、武蔵小金井、国立。都心に出なくても使える、西側の施設です。", "items": [[ "midori-so-kichijoji", "吉祥寺PARCO 8階" ], [ "co-ba-chofu", "調布駅1分の仕事軸のコミュニティ" ], [ "h1t-tachikawa", "立川駅南口から徒歩2分、席の種類が多い多摩の拠点" ], [ "h1t-musashikoganei", "武蔵小金井駅から徒歩3分、個室18室の大きな拠点" ], [ "h1t-kunitachi", "国立駅南口から徒歩2分、一人用の個室が17室ある拠点" ], [ "h1t-machida", "町田モディの6階、ブースと個室で一人の仕事に集中できる拠点" ] ] }, { "slug": "setagaya", "title": "世田谷のコワーキングスペース", "lead": "住まいに併設したラウンジ、経堂の個室、千歳船橋の朝7時から、二子玉川のショッピングセンター。住宅街の近くの施設です。", "items": [[ "co-ba-kamikitazawa", "住まいに併設したラウンジ" ], [ "h1t-kyodo", "経堂駅北口から徒歩2分、個室だけの静かな拠点" ], [ "h1t-chitosefunabashi", "千歳船橋駅から徒歩3分、朝7時から夜22時まで開く拠点" ], [ "workstyling-futako-tamagawa", "ショッピングセンターの中" ] ] }, { "slug": "h1t", "title": "H¹T の拠点", "lead": "駅前の一人用の個室、ブース、ボックス、会議室。野村不動産の法人向けシェアオフィスを、拠点ごとに紹介します。", "items": [[ "h1t-roppongi", "駅から徒歩1分、席の種類が多い" ], [ "h1t-shinjuku-nishiguchi", "会議室7室の法人向けシェアオフィス" ], [ "h1t-omotesando", "個室15室と10名の会議室" ], [ "h1t-ochanomizu-the-garden", "駅から徒歩1分の個室" ], [ "h1t-ikebukuro-higashiguchi-the-garden", "個室18室、土日祝も営業" ], [ "h1t-ichigaya", "4路線の市ヶ谷駅から徒歩1分、会議室が3室ある拠点" ], [ "h1t-iidabashi", "ビルの16階、緑の大きなテーブルがある飯田橋の拠点" ], [ "h1t-kojimachi", "麹町駅から徒歩1分、6名の会議室が3室ある拠点" ], [ "h1t-tsukiji", "築地駅4番出口から徒歩30秒、個室だけの拠点" ], [ "h1t-tachikawa", "立川駅南口から徒歩2分、席の種類が多い多摩の拠点" ], [ "h1t-machida", "町田モディの6階、ブースと個室で一人の仕事に集中できる拠点" ], [ "h1t-kunitachi", "国立駅南口から徒歩2分、一人用の個室が17室ある拠点" ], [ "h1t-kyodo", "経堂駅北口から徒歩2分、個室だけの静かな拠点" ], [ "h1t-musashikoganei", "武蔵小金井駅から徒歩3分、個室18室の大きな拠点" ], [ "h1t-chitosefunabashi", "千歳船橋駅から徒歩3分、朝7時から夜22時まで開く拠点" ] ] } ]
for _c in COLLECTIONS:
    _c['items'] = [tuple(x) for x in _c['items']]


# ==== 2026-09-30 地域×テーマの特集を追加（わたるさん指示「地域＋〇〇の特集をがんがん」）。一言は各記事のタイトルにある事実だけ ====
_EXT30 = {}
for _c in COLLECTIONS:
    _have = {x[0] for x in _c['items']}
    _c['items'] += [tuple(x) for x in _EXT30.get(_c['slug'], []) if x[0] not in _have]
COLLECTIONS += [ { "slug": "brand-wework", "title": "東京のWeWork（ウィーワーク）の拠点", "lead": "昭和のノスタルジア、電気街と昔のゲーム、本の街の手描きアート。拠点ごとに内装のテーマが違う WeWork を紹介します。", "items": [[ "wework-ark-hills-south", "アメリカンと華やかさ" ], [ "wework-d-tower-nishishinjuku", "モダニズムと木の濃淡" ], [ "wework-hareza-ikebukuro", "アート・日本絵画・映画" ], [ "wework-hibiya-fort-tower", "メタボリズムの8フロア" ], [ "wework-jimbocho", "本の街の手描きアート" ], [ "wework-kabuto-one", "国際金融街・兜町の再開発ビル" ], [ "wework-kamiyacho-trust-tower", "虎ノ門の過去と現代" ], [ "wework-kanda-square", "電気街と昔のゲーム" ], [ "wework-marunouchi-kitaguchi", "フロアごとに違うラウンジ" ], [ "wework-shibuya-scramble-square", "地上47階、窓際ラウンジから渋谷を見下ろす" ], [ "wework-the-argyle-aoyama", "白木とオークの共用エリア" ], [ "wework-tk-ikedayama", "昭和のノスタルジア" ] ] }, { "slug": "brand-business-airport", "title": "ビジネスエアポートの拠点", "lead": "鉄道発祥の地、職人の街、劇場、東京湾の水上空港。街の歴史を内装にした、東急不動産のシェアオフィスです。", "items": [[ "business-airport-aoyama", "自由な発想を誘う青山のシェアオフィス" ], [ "business-airport-daikanyama", "緑に囲まれた3階" ], [ "business-airport-ebisu", "柔らかな曲線の基地" ], [ "business-airport-hibiya", "劇場モチーフと緑" ], [ "business-airport-kanda", "レトロと新しさの共存" ], [ "business-airport-kudanshita", "お濠に面した九段会館テラス" ], [ "business-airport-kyobashi", "職人の街を和テイストで" ], [ "business-airport-marunouchi", "岸本ビルヂングの上質な空間" ], [ "business-airport-nihonbashi", "五街道の起点を思わせる1階" ], [ "business-airport-shibuya-fukuras", "駅前の17階" ], [ "business-airport-shibuya-nanpeidai", "SHIBUYA SOLASTA 3階" ], [ "business-airport-shibuya-sakurastage", "SHIBUYAタワー7階" ], [ "business-airport-shimbashi", "鉄道発祥の地のモチーフ" ], [ "business-airport-shinagawa", "太陽生命品川ビル28階" ], [ "business-airport-shinjuku3chome", "街の多様性を表す" ], [ "business-airport-takeshiba", "東京湾の水上空港" ], [ "business-airport-tamachi", "格式あるオフィスを継ぐ" ], [ "business-airport-tokyo", "丸の内ガーデンタワー3階" ] ] }, { "slug": "brand-the-executive-centre", "title": "The Executive Centre 東京の拠点", "lead": "茶室に着想した受付、英国と日本の内装、東京湾を望む17階。高層ビルに入るレンタルオフィスです。", "items": [[ "the-executive-centre-cerulean-tower", "茶室に着想を得た受付" ], [ "the-executive-centre-grantokyo-south-tower", "東京駅1分の7階" ], [ "the-executive-centre-jingumae-tower", "英国と日本の混じる内装" ], [ "the-executive-centre-jp-tower", "東京駅を見下ろすバリスタバー" ], [ "the-executive-centre-kyobashi-edogrand", "京橋駅直結の26階" ], [ "the-executive-centre-meguro-arco-tower", "目黒川を見下ろす7階" ], [ "the-executive-centre-roppongi-hills", "オークと障子風の会議室" ], [ "the-executive-centre-sanno-park-tower", "静けさのある3階" ], [ "the-executive-centre-shin-marunouchi-center", "木と大理石の2フロア" ], [ "the-executive-centre-tofrom-yaesu-tower", "和の意匠の220席" ], [ "the-executive-centre-world-trade-center-south-tower", "東京湾を望む17階" ] ] }, { "slug": "brand-workstyling", "title": "WORKSTYLING（ワークスタイリング）の拠点", "lead": "ZEN MODERN、RETRO FUTURE、INDUSTRY+FOREST。三井不動産のシェアオフィスを、拠点ごとに紹介します。", "items": [[ "workstyling-ebisu", "150名のカンファレンスルーム" ], [ "workstyling-futako-tamagawa", "ショッピングセンターの中" ], [ "workstyling-ginza", "銀座駅1分、土日も営業" ], [ "workstyling-hamamatsucho", "浜松町・大門から徒歩2分" ], [ "workstyling-iidabashi-grand-bloom", "2階と9階" ], [ "workstyling-kasumigaseki-building", "36階の高層階" ], [ "workstyling-meguro", "目黒駅から徒歩1分" ], [ "workstyling-nakameguro", "中目黒駅から徒歩2分" ], [ "workstyling-nihonbashi-ichome", "レンタルオフィスも" ], [ "workstyling-nihonbashi-mitsui-tower", "WORKSTYLING LAB" ], [ "workstyling-nihonbashi-takashimaya-mitsui", "日本橋駅直結" ], [ "workstyling-omotesando", "平日夜と土日も営業" ], [ "workstyling-otemachi", "芸術作品モチーフの会議室" ], [ "workstyling-shibuya", "渋谷駅東口から徒歩4分" ], [ "workstyling-shibuya-sakurastage", "最大108名のオープンスペース" ], [ "workstyling-shinagawa", "働くための巣" ], [ "workstyling-shinbashi", "新橋駅徒歩1分" ], [ "workstyling-shinjuku-higashiguchi", "駅直結で土日祝も営業" ], [ "workstyling-shinjuku-mitsui-building", "RETRO FUTURE" ], [ "workstyling-shiodome-city-center", "INDUSTRY+FOREST" ], [ "workstyling-tamachi-mitaguchi", "田町・三田から徒歩1分" ], [ "workstyling-tokyo-midtown-hibiya", "ZEN MODERN" ], [ "workstyling-tokyo-midtown-roppongi", "アートを加えた空間" ], [ "workstyling-tokyo-midtown-yaesu", "東京駅直結" ], [ "workstyling-yaesu-kitaguchi", "東京駅直結の17階" ], [ "workstyling-yaesu-minamiguchi", "土日も22時まで" ] ] }, { "slug": "brand-crosscoop", "title": "CROSSCOOP（クロスコープ）の拠点", "lead": "植栽のラウンジ、24時間のラウンジ、会議室15室。駅の近くのレンタルオフィスとコワーキングです。", "items": [[ "crosscoop-aoyama", "外苑前駅2分の3フロア" ], [ "crosscoop-nihonbashi", "約43席のラウンジ" ], [ "crosscoop-roppongi-next", "60席のラウンジ" ], [ "crosscoop-shibuya", "宮益坂の30席のラウンジ" ], [ "crosscoop-shibuya-nextsite", "植栽のラウンジ" ], [ "crosscoop-shimbashi", "約96席のラウンジと個室" ], [ "crosscoop-shinjuku", "会議室15室のレンタルオフィス" ], [ "crosscoop-shinjuku-avenue", "7階の24時間ラウンジ" ] ] }, { "slug": "brand-newwork", "title": "NEWWORK（ニューワーク）の拠点", "lead": "個室ブースの多いフロア、土日祝も開く店舗、93席の旗艦店。駅から近い、東急のシェアオフィスです。", "items": [[ "newwork-akihabara", "駅1分・土日祝も開く10階" ], [ "newwork-daimon-hamamatsucho", "大門駅1分の4階" ], [ "newwork-ebisu", "西口3分の39席" ], [ "newwork-ginza", "銀座と新橋のあいだの2階" ], [ "newwork-ikebukuro-higashiguchi", "個室ブース15室の9階" ], [ "newwork-kinshicho-2nd", "南口2分・土日祝も開く2階" ], [ "newwork-oimachi", "個室ブース11室の5階" ], [ "newwork-shibuya-goto-ikueikai-building", "93席の旗艦店" ], [ "newwork-ueno", "上野駅3分の37席" ] ] }, { "slug": "brand-senq", "title": "SENQ（センク）の拠点", "lead": "CREATOR'S VILLAGE、9階のスカイテラス、掘りごたつ。拠点ごとにテーマを掲げるシェアオフィスです。", "items": [[ "senq-aoyama", "22室の CREATOR'S VILLAGE" ], [ "senq-aoyama-namikidori", "BUILD NEXT CULTURES" ], [ "senq-kasumigaseki", "LEAD JAPAN と掘りごたつ" ], [ "senq-kyobashi", "京橋エドグランの FOOD INNOVATION" ], [ "senq-meguro", "暮らしながら働く8階" ], [ "senq-roppongi", "9階のスカイテラス" ] ] }, { "slug": "brand-co-ba", "title": "co-ba（コーバ）の拠点", "lead": "「働き方解放区」、芝浦のスケルトン空間、住まいに併設したラウンジ。地域ごとに運営されるコワーキングです。", "items": [[ "co-ba-akasaka", "溜池山王1分、集中の基地" ], [ "co-ba-chofu", "調布駅1分の仕事軸のコミュニティ" ], [ "co-ba-ebisu", "「働き方解放区」、約1,600㎡の2フロア" ], [ "co-ba-kamikitazawa", "住まいに併設したラウンジ" ], [ "co-ba-re-sohko-tamachi", "芝浦のスケルトン空間" ] ] } ]
for _c in COLLECTIONS:
    _c['items'] = [tuple(x) for x in _c['items']]

# ==== 2026-09-30 特集名を検索されやすい言葉に（わたるさん「SEOを考えて」）。URL（slug）は変えない ====
_RENAME30 = {
 'shibuya': '渋谷のおしゃれなコワーキングスペース',
 'incubation': '東京の起業家向けインキュベーション施設・コワーキングスペース',
 'reuse': '東京の古いビルをリノベーションしたおしゃれなコワーキングスペース',
 'marunouchi': '丸の内・有楽町・大手町のおしゃれなコワーキングスペース',
 'toranomon-azabudai': '虎ノ門・麻布台のおしゃれなコワーキングスペース',
 'station-direct': '東京の駅直結のコワーキングスペース',
 'large-floor': '東京の広くて大きいコワーキングスペース',
 'corporate-public': '東京の企業・行政がつくったコワーキングスペース',
 'nihonbashi-yaesu': '日本橋・京橋・八重洲のおしゃれなコワーキングスペース',
 'shinjuku': '新宿のおしゃれなコワーキングスペース',
 'aoyama-omotesando': '青山・表参道のおしゃれなコワーキングスペース',
 'high-floor': '東京の眺めのいい高層階のコワーキングスペース',
 '24hours': '東京の24時間使えるコワーキングスペース',
 'weekend': '東京の土日も使えるコワーキングスペース',
 'solo': '東京のひとりで集中できる個室のあるコワーキングスペース',
 'hotel': '東京のホテルの中のおしゃれなコワーキングスペース',
 'design-theme': '東京の内装がかっこいいコワーキングスペース',
 'rooftop': '東京の屋上・テラスのある気持ちいいコワーキングスペース',
 'midori-so': 'MIDORI.so（ミドリソー）の拠点',
 'shibuya-high-floor': '渋谷の眺めのいい高層階のコワーキングスペース',
 'ebisu-meguro': '恵比寿・目黒・中目黒のおしゃれなコワーキングスペース',
 'roppongi-azabu': '六本木・麻布十番のおしゃれなコワーキングスペース',
 'ginza-shimbashi': '銀座・新橋・汐留のおしゃれなコワーキングスペース',
 'kanda-akihabara': '神田・秋葉原・御茶ノ水・神保町のおしゃれなコワーキングスペース',
 'shinagawa-hamamatsucho': '品川・田町・浜松町のおしゃれなコワーキングスペース',
 'tama-chuo-line': '吉祥寺・立川・国立など中央線沿いのコワーキングスペース',
 'setagaya': '世田谷のおしゃれなコワーキングスペース',
 'h1t': 'H¹T（エイチワンティー）の拠点',
}
for _c in COLLECTIONS:
    _c['title'] = _RENAME30.get(_c['slug'], _c['title'])

# ==== 2026-09-30 わたるさん「MILLSの強みは内装がかっこいいところ。入れようよ」→ 特集名に「内装がかっこいい」を入れる ====
import re as _re30
def _naisou30(t):
    if '内装' in t: return t
    t = t.replace('おしゃれなコワーキングスペース', '内装がかっこいいコワーキングスペース').replace('気持ちいいコワーキングスペース', '内装がかっこいいコワーキングスペース')
    if '内装' not in t:
        t = _re30.sub(r'のコワーキングスペース$', 'の内装がかっこいいコワーキングスペース', t)
        t = _re30.sub(r'の拠点$', 'の内装がかっこいい拠点', t)
        t = _re30.sub(r'施設・コワーキングスペース$', '施設・内装がかっこいいコワーキングスペース', t)
    return t
for _c in COLLECTIONS:
    _c['title'] = _naisou30(_c['title'])
_FIX30 = {
 '24hours': '東京の24時間使える内装がかっこいいコワーキングスペース',
 'corporate-public': '東京の企業・行政がつくった内装がかっこいいコワーキングスペース',
 'large-floor': '東京の広くて内装がかっこいいコワーキングスペース',
 'solo': '東京のひとりで集中できる個室のある内装がかっこいいコワーキングスペース',
 'weekend': '東京の土日も使える内装がかっこいいコワーキングスペース',
 'incubation': '東京の起業家向け内装がかっこいいインキュベーション施設',
 'high-floor': '東京の眺めがよく内装がかっこいい高層階コワーキングスペース',
 'shibuya-high-floor': '渋谷の眺めがよく内装がかっこいい高層階コワーキングスペース',
}
for _c in COLLECTIONS:
    _c['title'] = _FIX30.get(_c['slug'], _c['title'])
# 2026-09-30 施設を足したので、紹介文の中の古い件数を消す
for _c in COLLECTIONS:
    if _c['slug'] == 'shibuya': _c['lead'] = _c['lead'].replace('集まる3施設です。', '集まる施設です。')
    if _c['slug'] == 'marunouchi': _c['lead'] = _c['lead'].replace('つくり手の違う4施設が', 'つくり手の違う施設が')
# 2026-10-01 9/28と10/1に足した施設を、特集に入れる
_ADD_1001 = {
 'brand-workstyling': [('ws-ueno','JR上野駅から1分、予約なしで座れる'),('ws-ikebukuro-nishiguchi','池袋駅から1分の5階'),('ws-yotsuya','麹町と四ツ谷の両方から4分'),('ws-gotanda','五反田駅から1分'),('ws-kanda','神田駅から1分、80名までの会議室'),('ws-akihabara','秋葉原駅の中央改札から1分'),('ws-jimbocho','神保町駅から1分、登記もできる'),('ws-toyosu','豊洲駅から2分、登記もできる'),('ws-kichijoji','吉祥寺駅から1分'),('ws-machida','JRと小田急の町田駅から3分'),('ws-musashikosugi','ららテラス武蔵小杉の4階'),('ws-shinyokohama','新横浜駅から3分'),('ws-umeda','阪急ターミナルビルの10階'),('ws-kyoto-ekimae','京都駅から2分')],
 'kanda-akihabara': [('ws-kanda','神田駅から徒歩1分'),('ws-akihabara','秋葉原駅中央改札から徒歩1分'),('ws-jimbocho','神保町駅から徒歩1分、登記もできる')],
 'tama-chuo-line': [('ws-kichijoji','吉祥寺駅から徒歩1分'),('ws-machida','町田駅から徒歩3分')],
 'h1t': [('h1t-toranomon','虎ノ門駅10番出口に直結'),('h1t-ginza','銀座駅A7出口から徒歩1分'),('h1t-otemachi','大手町駅から徒歩1分、20階と21階'),('h1t-ueno','上野マルイの3階')],
 'marunouchi': [('h1t-otemachi','大成大手町ビルの20階と21階')],
 'ginza-shimbashi': [('h1t-ginza','銀座駅A7出口から徒歩1分')],
 'toranomon-azabudai': [('h1t-toranomon','虎ノ門駅10番出口に直結')],
 'station-direct': [('h1t-toranomon','虎ノ門駅10番出口に直結')],
 'solo': [('h1t-toranomon','1名用ルーム27室')],
}
for _c in COLLECTIONS:
    _have = {x[0] for x in _c['items']}
    _c['items'] += [tuple(x) for x in _ADD_1001.get(_c['slug'], []) if x[0] not in _have]

# 2026-10-01 別チャットの追加（cowork_add_2026-09-30）を特集に（一言は各記事のカードの文）
_ADD_1001B = {
 'brand-wework': [('wework-hanzomon-prex-north', '半蔵門の「門」をイメージした、メタルと木の組み合わせ'), ('wework-tokyo-portcity-takeshiba', '竹芝スマートシティの中心、「NY×和風」の空間'), ('wework-kdx-toranomon-1chome', '11階のラウンジと屋外テラスがひと続きの空間')],
 'h1t': [('h1t-shibuya-miyamasuzaka', '宮益坂のワコー宮益坂8階、個室14室と会議室5室'), ('h1t-akasaka-mitsuke', '赤坂見附駅10番出口1分、日曜・祝日も開く7階'), ('h1t-jimbocho', '神保町駅A7出口1分、14席と会議室4室の5階')],
 'brand-newwork': [('newwork-ikebukuro-7f', '池袋駅東口4分、オーク池袋ビルディング7階の31席'), ('newwork-ikebukuro-4f', '個室ブース7室と会議室2室、打ち合わせ向きの4階'), ('newwork-omori', '大森駅3分、個室ブース11室のいちご大森ビル6階'), ('newwork-aoto', '青砥駅5分、13席の小さな朝日生命葛飾ビル4階'), ('newwork-tokyo-the-flagship', '東京駅1分、丸の内トラストタワーN館11階の95席')],
 'shinjuku': [('hapon-shinjuku', '日本列島の形のテーブルと、畳の「富士の間」'), ('case-shinjuku', '高田馬場駅1分、クリエイターと起業家がゆるやかにつながる')],
 'incubation': [('startup-hub-tokyo-marunouchi', '起業を考え始めた人のための、無料の創業支援施設'), ('nexs-tokyo-community-space', '全国と東京のスタートアップがつながる、丸の内の会員制スペース'), ('chiyoda-platform-square', '区の公共施設を生まれ変わらせた、2004年からのシェアオフィス'), ('startupside-tokyo', '50席と個室8室、インキュベーションマネージャーが常駐'), ('city-lab-tokyo', '持続可能な都市づくりのための、京橋のオープンイノベーション拠点'), ('ship-osaki', '大崎の会員制ラウンジと3Dプリンターの工房、品川区の拠点')],
 'marunouchi': [('startup-hub-tokyo-marunouchi', '起業を考え始めた人のための、無料の創業支援施設'), ('newwork-tokyo-the-flagship', '東京駅1分、丸の内トラストタワーN館11階の95席')],
 'aoyama-omotesando': [('nagaya-aoyama', '約70㎡のウッドテラスがある、静かな南青山の2階'), ('faro-aoyama', '100％国産の木材、緑につつまれたシェアオフィス')],
 'shibuya': [('h1t-shibuya-miyamasuzaka', '宮益坂のワコー宮益坂8階、個室14室と会議室5室'), ('co-lab-daikanyama', 'SodaCCo の4〜6階、テラスと屋上のあるクリエイターのシェアオフィス')],
 'nihonbashi-yaesu': [('soil-work-nihonbashi', '公園に面した窓、1階にカフェベーカリーのある6階')],
 'kanda-akihabara': [('basispoint-jimbocho', '神保町駅A5出口から1分、ホテルラウンジのような6階'), ('h1t-jimbocho', '神保町駅A7出口1分、14席と会議室4室の5階')],
 'ginza-shimbashi': [('basispoint-shimbashi-ginzaguchi', '新橋駅銀座口から1分、56名の大会議室まで')],
 'toranomon-azabudai': [('wework-kdx-toranomon-1chome', '11階のラウンジと屋外テラスがひと続きの空間')],
 'setagaya': [('tefu-lounge-shimokitazawa', '下北沢駅の南西改札口から0分、ラウンジを中心にした複合施設')],
 'tama-chuo-line': [('merise-tachikawa', '信用金庫の旧本店を生まれ変わらせた、多摩の共創拠点')],
}
for _c in COLLECTIONS:
    _have = {x[0] for x in _c['items']}
    _c['items'] += [tuple(x) for x in _ADD_1001B.get(_c['slug'], []) if x[0] not in _have]
