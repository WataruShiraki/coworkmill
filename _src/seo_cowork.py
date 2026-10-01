# cowork のページごとの SEO（2026-09-26 に本番へ入れたもの）。メタタイトルは末尾に " | COWORKMILL" が自動で付く
# SEO[slug] = (メタタイトル, description)。PLACE[slug] = 住所（構造化データ LocalBusiness の address と openingHours。名前・URL・写真・ひとことは施設データから自動）。REDIRECTS = 旧スラッグ → 新スラッグ
INDEX_TITLE = "COWORKMILL（コワークミル）｜内装デザインが最も優れたコワーキングを厳選紹介"
import os as _os, sys as _sys
_sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__)))
from cowork_facilities import A30 as _A30
_N = len(_A30)  # 2026-09-27 施設数は手書きせず自動で数える（10のまま残っていた）
INDEX_DESC = f"内装・内観・雰囲気で選ぶ、東京のコワーキングスペース・シェアオフィス{_N}施設。渋谷・虎ノ門・大手町・丸の内・麻布台・永田町・中目黒・恵比寿・有楽町・青山の空間を、公式の写真と情報で、初めて訪れる人が歩く順番で紹介します。"
LIST_TITLE = f"東京の内装がかっこいいコワーキング{_N}施設｜内観・雰囲気の写真"
LIST_DESC = f"渋谷・虎ノ門・大手町・丸の内・麻布台・永田町・中目黒・恵比寿・有楽町・青山。内装・内観・雰囲気の写真で選ぶコワーキングスペース{_N}施設を、公式情報をもとに1施設ずつ紹介します。"
REDIRECTS = {}  # 2026-09-27 CIC Tokyo は写真8枚が揃ったので掲載に戻した（9/26は写真不足で co-lab 渋谷キャストへ転送していた）
SEO = {
  "100banch": ("100BANCH 渋谷｜内装・内観・雰囲気の写真｜組み替え自由の実験区、3階建ての空間",
    "100BANCH（渋谷）の内装・内観・外観・雰囲気を写真で。1階のテストキッチン、10〜20組のプロジェクトが同居する2階のガレージ、200インチのスクリーンがある3階のロフトを、歩く順番で紹介します。"),
  "business-airport-aoyama": ("Business Airport 青山｜内装・内観・雰囲気の写真｜自由な発想を誘う青山のシェアオフィス",
    "Business Airport 青山（スプライン青山東急ビル4・6階）の内装・内観・雰囲気を写真で。「青山らしく、自由な発想を喚起するスタイリッシュなワークスペース」と公式が説明するラウンジ、ROOM と BOOTH、60名のイベントスペースを紹介します。"),
  "co-ba-ebisu": ("co-ba ebisu 恵比寿｜内装・内観・雰囲気の写真｜「働き方解放区」、約1,600㎡の2フロア",
    "co-ba ebisu（JP noie 恵比寿西1・2階）の内装・内観・雰囲気を写真で。デザインテーマは「WORK ASSEMBLE」。70人の PARK と40人の CAFE、フリーアドレスから固定席、8〜20人の個室まで、約1,600㎡の空間を紹介します。"),
  "co-lab-shibuya-cast": ("co-lab 渋谷キャスト｜内装・内観・雰囲気の写真｜つくる人が集まる1・2階のシェアオフィス",
    "co-lab 渋谷キャストの内装・内観・雰囲気を写真で。1〜2人のブースから22人のルームまで、窓際の共用スペースとキッチン、4つの会議室と手を動かす場所。24時間365日使える、クリエイターのための空間を紹介します。"),
  "lifork-otemachi": ("LIFORK 大手町｜内装・内観・雰囲気の写真｜駅直結、落ち着いた木の質感のシェアオフィス",
    "LIFORK 大手町（大手町ファーストスクエア1・2階）の内装・内観・雰囲気を写真で。「上質かつ落ち着いた内装で開放的な空間」と公式が説明する13タイプの部屋、199.1㎡のラウンジ、30分単位で借りる10室を紹介します。"),
  "midori-so-nakameguro": ("MIDORI.so 中目黒｜内装・内観・雰囲気の写真｜蔦に覆われた廃屋を直した2棟のシェアオフィス",
    "MIDORI.so Nakameguro の内装・内観・外観・雰囲気を写真で。蔦に覆われていた廃屋を改装した本館と母屋の2棟。ワークスペースとラウンジ、個室オフィスの棟、展示と撮影に貸すギャラリーを紹介します。"),
  "saai-yurakucho": ("有楽町 SAAI｜内装・内観・雰囲気の写真｜畳と六角形のシート、新東京ビルの会員制コミュニティ",
    "有楽町 SAAI Wonder Working Community の内装・内観・雰囲気を写真で。新東京ビルの地下1階・1階・4階。畳の御座敷、六角形のシート、ステージ、会員専用のバー。三菱地所が「多様な人が出逢う場所」として作った空間を紹介します。"),
  "shibuya-qws": ("SHIBUYA QWS｜内装・内観・雰囲気の写真｜スクランブル交差点を見下ろす15階の会員制施設",
    "SHIBUYA QWS（渋谷スクランブルスクエア15階）の内装・内観・雰囲気を写真で。可動式テーブルの PROJECT BASE、人が行き交う CROSS PARK、交差点を見下ろす200名規模の SCRAMBLE HALL、陸上トラックの床材のカフェを紹介します。"),
  "toranomon-hills-arch": ("ARCH 虎ノ門ヒルズ｜内装・内観・雰囲気の写真｜Wonderwall 設計、中庭に開く3,800㎡",
    "ARCH（虎ノ門ヒルズ インキュベーションセンター）の内装・内観・雰囲気を写真で。Wonderwall が内装を手がけた3,800㎡。場面で選べるワークスペース、ガラス張りのイベントの部屋と隣の中庭、開放感のあるカフェ＆ラウンジを紹介します。"),
  "wework-shibuya-scramble-square": ("WeWork 渋谷スクランブルスクエア｜内装・内観・雰囲気の写真｜地上47階、窓際ラウンジから渋谷を見下ろす",
    "WeWork 渋谷スクランブルスクエア（37〜42階・45階）の内装・内観・雰囲気を写真で。窓際に長く続く共用ラウンジ、キッチンを囲む場所、イベント仕様のラウンジ、天井高3,000mm超のフロアを紹介します。"),
}
PLACE = {
  "100banch": {"streetAddress": "東京都渋谷区渋谷3-27-1", "addressLocality": "渋谷", "addressRegion": "東京都"},
  "business-airport-aoyama": {"streetAddress": "東京都港区南青山3-1-3 スプライン青山東急ビル4F・6F", "addressLocality": "青山", "addressRegion": "東京都"},
  "co-ba-ebisu": {"streetAddress": "東京都渋谷区恵比寿西1-33-6 JP noie 恵比寿西 1F・2F", "addressLocality": "恵比寿", "addressRegion": "東京都"},
  "co-lab-shibuya-cast": {"streetAddress": "東京都渋谷区渋谷1-23-21 渋谷キャスト 1-2F", "addressLocality": "渋谷", "addressRegion": "東京都", "openingHours": "24時間365日"},
  "lifork-otemachi": {"streetAddress": "東京都千代田区大手町1-5-1 大手町ファーストスクエア ウエストタワー1・2階", "addressLocality": "大手町", "addressRegion": "東京都"},
  "midori-so-nakameguro": {"streetAddress": "東京都目黒区青葉台3-3-11", "addressLocality": "目黒", "addressRegion": "東京都"},
  "saai-yurakucho": {"streetAddress": "東京都千代田区丸の内三丁目3番1号 新東京ビル", "addressLocality": "有楽町", "addressRegion": "東京都"},
  "shibuya-qws": {"streetAddress": "東京都渋谷区渋谷二丁目24番12号 渋谷スクランブルスクエア（東棟）15階", "addressLocality": "渋谷", "addressRegion": "東京都", "openingHours": "9:00〜22:00（最終入館21:30）"},
  "toranomon-hills-arch": {"streetAddress": "東京都港区虎ノ門1丁目17番1号 虎ノ門ヒルズビジネスタワー4階", "addressLocality": "虎ノ門", "addressRegion": "東京都"},
  "wework-shibuya-scramble-square": {"streetAddress": "渋谷スクランブルスクエア（渋谷駅直結）", "addressLocality": "渋谷", "addressRegion": "東京都"},
}

# ---- 2026-09-27 追加5施設 ----
SEO_ADD = {
  'tokyo-venture-capital-hub': ('Tokyo Venture Capital Hub 麻布台｜内装・内観・雰囲気の写真',
    'Tokyo Venture Capital Hub（麻布台ヒルズ）の内装・内観・雰囲気を写真で。森ビルが運営する日本初のVC集積拠点。レセプション、サロン、ラウンジ、オープンスペース、テラスを歩く順番で紹介します。'),
  'cic-tokyo': ('CIC Tokyo 虎ノ門｜内装・内観・雰囲気の写真｜約6,000㎡',
    'CIC Tokyo（虎ノ門ヒルズ ビジネスタワー）の内装・内観・外観・雰囲気を写真で。325社以上が入居する日本最大級の拠点。コワーキング、Venture Café、会議室、ウェルネスエリアを歩く順番で紹介します。'),
  'point-0-marunouchi': ('point 0 marunouchi 丸の内｜内装・内観・雰囲気の写真',
    'point 0 marunouchi（丸の内2丁目ビル4階）の内装・内観・雰囲気を写真で。Klein Dytham architecture が内装を手がけた緑あふれるコワーキング。席、カフェ、休息の部屋を歩く順番で紹介します。'),
  'midori-so-nagatacho': ('MIDORI.so NAGATACHO 永田町｜内装・内観・雰囲気の写真',
    'MIDORI.so NAGATACHO（平河町）の内装・内観・外観・雰囲気を写真で。地下1階から6階まで1棟丸ごと使う旗艦拠点。5階のラウンジとライブラリ、2階のエンゲージメントスペースを歩く順番で紹介します。'),
  'tokyo-innovation-base': ('Tokyo Innovation Base 有楽町｜内装・内観・雰囲気の写真',
    'Tokyo Innovation Base（TIB、丸の内3-8-3）の内装・内観・雰囲気を写真で。東京都が運営する有楽町駅前の拠点。1階の SQUARE、2階の STAGE、3階の SALON を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'tokyo-venture-capital-hub': {'streetAddress': '東京都港区虎ノ門五丁目9番1 麻布台ヒルズ ガーデンプラザB 4階/5階', 'addressLocality': '麻布台', 'addressRegion': '東京都'},
  'cic-tokyo': {'streetAddress': '東京都港区虎ノ門1-17-1 虎ノ門ヒルズ ビジネスタワー 15階', 'addressLocality': '虎ノ門', 'addressRegion': '東京都'},
  'point-0-marunouchi': {'streetAddress': '東京都千代田区丸の内2-5-1 丸の内2丁目ビル 4F', 'addressLocality': '丸の内', 'addressRegion': '東京都'},
  'midori-so-nagatacho': {'streetAddress': '東京都千代田区平河町2-5-3', 'addressLocality': '永田町', 'addressRegion': '東京都'},
  'tokyo-innovation-base': {'streetAddress': '東京都千代田区丸の内3-8-3', 'addressLocality': '有楽町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-21:00, Sa-Su 10:00-17:00'},
}
SEO.update(SEO_ADD)
PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 _b ----
# ===== SEO と住所（seo_<brand>.py に足す分） =====
SEO_ADD = {
  'share-m-10': ('SHARE M-10 麻布十番｜内装・内観・雰囲気の写真｜隈研吾設計、木の輪の森',
    'SHARE M-10（麻布十番 MAXPLAN AZABU10）の内装・内観・雰囲気を写真で。隈研吾さんが設計した、木の輪のプランターに囲まれた16席のコワーキング。席、窓際、会議室を歩く順番で紹介します。'),
  'birth-work-azabujuban': ('BIRTH WORK 麻布十番｜内装・内観・雰囲気の写真｜集中と憩いの3フロア',
    'BIRTH WORK 麻布十番（麻布十番髙木ビル）の内装・内観・雰囲気を写真で。5階は集中、8・9階は憩いのフロア。1階の BIRTH LAB のウッドシェルフまで、歩く順番で紹介します。'),
  'base-point-shinjuku': ('BASE POINT 西新宿｜内装・内観・雰囲気の写真｜1階はワーキングカフェ',
    'BASE POINT（西新宿7丁目）の内装・内観・雰囲気を写真で。1階は22席の時間制ワーキングカフェ、2階は会議室、3階はシェアオフィス。朝7時から開く3層のワークスペースを歩く順番で紹介します。'),
  '3x3lab-future': ('3×3Lab Future 大手町｜内装・内観・雰囲気の写真｜竹と杉と板倉構法の11ゾーン',
    '3×3Lab Future（大手門タワー・ENEOSビル1階）の内装・内観・雰囲気を写真で。竹集成材の机、足場板の杉の床、板倉構法の部屋。素材で語る11のゾーンを歩く順番で紹介します。'),
  'global-business-hub-tokyo': ('Global Business Hub Tokyo 大手町｜内装・内観・雰囲気の写真｜家具付き50区画',
    'Global Business Hub Tokyo（大手町フィナンシャルシティ グランキューブ3階）の内装・内観・雰囲気を写真で。家具付きオフィス50区画、会議室14室、200名のイベントスペースを歩く順番で紹介します。'),
  'egg-japan-marunouchi': ('EGG 丸の内｜内装・内観・雰囲気の写真｜新丸ビル10階のインキュベーション',
    'EGG（新丸の内ビルディング10階・9階）の内装・内観・雰囲気を写真で。三菱地所が運営する丸の内のインキュベーションオフィス。Sundial Lounge、個室、ダイニングを歩く順番で紹介します。'),
  'x-nihonbashi-tower': ('X-NIHONBASHI TOWER 日本橋｜内装・内観・雰囲気の写真｜宇宙ビジネスの拠点',
    'X-NIHONBASHI TOWER（日本橋三井タワー7階）の内装・内観・雰囲気を写真で。三井不動産が運営する宇宙ビジネスの共創拠点。307㎡のコワーキングとカンファレンスを歩く順番で紹介します。'),
  'potluck-yaesu': ('POTLUCK YAESU 八重洲｜内装・内観・雰囲気の写真｜地域の夢が集まるラウンジ',
    'POTLUCK YAESU（東京ミッドタウン八重洲5階）の内装・内観・雰囲気を写真で。三井不動産と NewsPicks Re:gion の拠点。ラウンジ、カフェ、140人のスタジオ、展示を歩く順番で紹介します。'),
  'hills-house-azabudai': ('Hills House 麻布台｜内装・内観・雰囲気の写真｜森JPタワー33・34階',
    'Hills House 麻布台（麻布台ヒルズ森JPタワー33・34階）の内装・内観・雰囲気を写真で。森ビルが運営する会員制エリア。3つのラウンジ、Dining 33、カフェ＆バーを歩く順番で紹介します。'),
  'midori-so-bakuroyokoyama': ('MIDORI.so 馬喰横山｜内装・内観・雰囲気の写真｜昭和のビルと屋上の畑',
    'MIDORI.so Bakuroyokoyama（日本橋横山町）の内装・内観・外観・雰囲気を写真で。昭和のビル7階分に、ラウンジ、工房、ギャラリー、屋上の庭。働く・作る・見せる場所を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'share-m-10': {'streetAddress': '東京都港区麻布十番4-1-1 MAXPLAN AZABU10 2F・3F', 'addressLocality': '麻布十番', 'addressRegion': '東京都'},
  'birth-work-azabujuban': {'streetAddress': '東京都港区麻布十番2-20-7 麻布十番髙木ビル5F/8F/9F', 'addressLocality': '麻布十番', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'base-point-shinjuku': {'streetAddress': '東京都新宿区西新宿7丁目22-3', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-23:00'},
  '3x3lab-future': {'streetAddress': '東京都千代田区大手町1-1-2 大手門タワー・ENEOSビル1F', 'addressLocality': '大手町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:00'},
  'global-business-hub-tokyo': {'streetAddress': '東京都千代田区大手町1丁目9-2 大手町フィナンシャルシティ グランキューブ3F', 'addressLocality': '大手町', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'egg-japan-marunouchi': {'streetAddress': '東京都千代田区丸の内1-5-1 新丸の内ビルディング 10F', 'addressLocality': '丸の内', 'addressRegion': '東京都'},
  'x-nihonbashi-tower': {'streetAddress': '東京都中央区日本橋室町2-1-1 日本橋三井タワー7階', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-19:00'},
  'potluck-yaesu': {'streetAddress': '東京都中央区八重洲2丁目2-1 東京ミッドタウン八重洲 5F', 'addressLocality': '八重洲', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 11:00-22:00, Sa-Su 11:00-19:00'},
  'hills-house-azabudai': {'streetAddress': '東京都港区麻布台一丁目3番1号 麻布台ヒルズ森JPタワー33F・34F', 'addressLocality': '麻布台', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-23:00'},
  'midori-so-bakuroyokoyama': {'streetAddress': '東京都中央区日本橋横山町5-13', 'addressLocality': '馬喰横山', 'addressRegion': '東京都'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 _c ----
# ===== SEO と住所（seo_<brand>.py に足す分） =====
SEO_ADD = {
  'midori-so-shibuya': ('MIDORI.so 渋谷｜内装・内観・雰囲気の写真｜桜丘町の4フロアとライブラリ',
    'MIDORI.so Shibuya（渋谷区桜丘町）の内装・内観・外観・雰囲気を写真で。3階から6階の4フロアに、ラウンジ、キッチン、ライブラリ、会議室。渋谷駅4分の拠点を歩く順番で紹介します。'),
  'midori-so-aoyama': ('MIDORI.so 青山｜内装・内観・雰囲気の写真｜固定席のない「会う」場所',
    'MIDORI.so Aoyama（南青山1丁目）の内装・内観・外観・雰囲気を写真で。固定の机を置かないワークスペース、音にこだわったリスニングラウンジ、夜のバー、屋上の庭を歩く順番で紹介します。'),
  'midori-so-ikejiri': ('MIDORI.so 池尻｜内装・内観・雰囲気の写真｜3つのゾーンのワンフロア',
    'MIDORI.so Ikejiri（世田谷区池尻）の内装・内観・雰囲気を写真で。WEST・CENTRAL・EAST の3つのゾーンに、ラウンジ、キッチン、集中席、ギャラリー。池尻の拠点を歩く順番で紹介します。'),
  'midori-so-kichijoji': ('MIDORI.so 吉祥寺｜内装・内観・雰囲気の写真｜吉祥寺PARCO 8階',
    'MIDORI.so Kichijoji（吉祥寺PARCO 8階）の内装・内観・雰囲気を写真で。MIDORI.so で23区の外の最初の拠点。ワークスペース、キッチン、会議室を歩く順番で紹介します。'),
  'midori-so-nihonbashi': ('MIDORI.so 日本橋｜内装・内観・雰囲気の写真｜働いて泊まれる東日本橋',
    'MIDORI.so Nihonbashi（東日本橋3丁目）の内装・内観・外観・雰囲気を写真で。1階のカフェ＆バー、2階のラウンジ、3・4階の仕事と眠りの部屋。働くと泊まるが同居する拠点を歩く順番で紹介します。'),
  'business-airport-kudanshita': ('Business Airport 九段下｜内装・内観・雰囲気の写真｜お濠に面した九段会館テラス',
    'Business Airport 九段下（九段会館テラス1階）の内装・内観・雰囲気を写真で。お濠の緑と水景を望む、歴史を受け継ぐワークプレイス。コワーキング、個室、会議室を歩く順番で紹介します。'),
  'business-airport-daikanyama': ('Business Airport 代官山｜内装・内観・雰囲気の写真｜緑に囲まれた3階',
    'Business Airport 代官山（Forestgate Daikanyama MAIN棟3階）の内装・内観・雰囲気を写真で。にぎわいと落ち着きが共存する緑の中のワークプレイスを、歩く順番で紹介します。'),
  'business-airport-shibuya-sakurastage': ('Business Airport 渋谷サクラステージ｜内装・内観・雰囲気の写真｜SHIBUYAタワー7階',
    'Business Airport 渋谷サクラステージ（SHIBUYAタワー7階）の内装・内観・雰囲気を写真で。土日祝も開くワーカーズラウンジ、個室、会議室、イベントスペースを歩く順番で紹介します。'),
  'business-airport-takeshiba': ('Business Airport 竹芝｜内装・内観・雰囲気の写真｜東京湾の水上空港',
    'Business Airport 竹芝（東京ポートシティ竹芝オフィスタワー8階）の内装・内観・雰囲気を写真で。スマートシティの中の「水上空港」。コワーキングと個室を歩く順番で紹介します。'),
  'business-airport-nihonbashi': ('Business Airport 日本橋｜内装・内観・雰囲気の写真｜五街道の起点を思わせる1階',
    'Business Airport 日本橋（日本橋フロント1階）の内装・内観・雰囲気を写真で。五街道の起点を思わせる内装のシェアワークプレイス、ソロワークエリア、会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'midori-so-shibuya': {'streetAddress': '東京都渋谷区桜丘町16-13 3F〜6F', 'addressLocality': '渋谷', 'addressRegion': '東京都'},
  'midori-so-aoyama': {'streetAddress': '東京都港区南青山1-7-12 2F/3F', 'addressLocality': '青山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
  'midori-so-ikejiri': {'streetAddress': '東京都世田谷区池尻2-4-5 2F', 'addressLocality': '池尻', 'addressRegion': '東京都'},
  'midori-so-kichijoji': {'streetAddress': '東京都武蔵野市吉祥寺本町1-5-1 吉祥寺 PARCO 8F', 'addressLocality': '吉祥寺', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-23:00'},
  'midori-so-nihonbashi': {'streetAddress': '東京都中央区東日本橋3丁目9-1', 'addressLocality': '東日本橋', 'addressRegion': '東京都'},
  'business-airport-kudanshita': {'streetAddress': '東京都千代田区九段南1-6-5 九段会館テラス1F', 'addressLocality': '九段下', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00'},
  'business-airport-daikanyama': {'streetAddress': '東京都渋谷区代官山町20-23 Forestgate Daikanyama MAIN棟3F', 'addressLocality': '代官山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
  'business-airport-shibuya-sakurastage': {'streetAddress': '東京都渋谷区桜丘町1-4 渋谷サクラステージSHIBUYAサイド SHIBUYAタワー7F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa-Su 10:00-18:00'},
  'business-airport-takeshiba': {'streetAddress': '東京都港区海岸1-7-1 東京ポートシティ竹芝オフィスタワー8F', 'addressLocality': '竹芝', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
  'business-airport-nihonbashi': {'streetAddress': '東京都中央区日本橋3-6-2 日本橋フロント1F', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 _d ----
# ===== SEO と住所（seo_<brand>.py に足す分） =====
SEO_ADD = {
  'andwork-shibuya': ('.andwork 渋谷｜内装・内観・雰囲気の写真｜ホテルのラウンジで働く',
    '.andwork 渋谷（The Millennials 渋谷）の内装・内観・雰囲気を写真で。世界中の宿泊客と地元で働く人が交わるホテルハイブリッド型のコワーキング。ラウンジ、キッチン、ブースを歩く順番で紹介します。'),
  'andwork-azabujuban': ('.andwork 麻布十番｜内装・内観・雰囲気の写真｜大人の隠れ家的オフィス',
    '.andwork 麻布十番（THE LIVELY 東京麻布十番）の内装・内観・雰囲気を写真で。2階のラウンジで働き、最上階のバーで過ごす。仕事と遊びを両立する大人の隠れ家を、歩く順番で紹介します。'),
  'andwork-shibuya-higashi': ('.andwork 渋谷東｜内装・内観・雰囲気の写真｜ホテル1階のカフェで働く',
    '.andwork 渋谷東（HOTEL GRAPHY 渋谷1階）の内装・内観・雰囲気を写真で。コーヒーからアイデアを育てるカフェ兼コワーキング。週4日、昼だけ開く隠れ家を歩く順番で紹介します。'),
  'co-ba-akasaka': ('co-ba 赤坂｜内装・内観・雰囲気の写真｜溜池山王1分、集中の基地',
    'co-ba 赤坂（赤坂2丁目 吉川ビル2階）の内装・内観・雰囲気を写真で。落ち着いて集中できる赤坂のスタートアップ基地。ゆったりした机と椅子、個室、会議室を歩く順番で紹介します。'),
  'business-airport-tokyo': ('Business Airport 東京｜内装・内観・雰囲気の写真｜丸の内ガーデンタワー3階',
    'Business Airport 東京（日本生命丸の内ガーデンタワー3階）の内装・内観・雰囲気を写真で。東京駅のそば、日祝も開くコワーキング、個室、会議室を歩く順番で紹介します。'),
  'business-airport-marunouchi': ('Business Airport 丸の内｜内装・内観・雰囲気の写真｜岸本ビルヂングの上質な空間',
    'Business Airport 丸の内（岸本ビルヂング6階）の内装・内観・雰囲気を写真で。安心感、ステイタス、落ち着き、信頼を備えた上質なワークプレイスを、歩く順番で紹介します。'),
  'business-airport-hibiya': ('Business Airport 日比谷｜内装・内観・雰囲気の写真｜劇場モチーフと緑',
    'Business Airport 日比谷（東宝日比谷ビル9階）の内装・内観・雰囲気を写真で。劇場をモチーフに緑が調和するワークプレイス。コワーキング、個室、会議室を歩く順番で紹介します。'),
  'business-airport-kyobashi': ('Business Airport 京橋｜内装・内観・雰囲気の写真｜職人の街を和テイストで',
    'Business Airport 京橋（FPG links KYOBASHI）の内装・内観・雰囲気を写真で。ものづくりの街・京橋の魅力を優しい和テイストで表したワークプレイスを、歩く順番で紹介します。'),
  'business-airport-shibuya-fukuras': ('Business Airport 渋谷フクラス｜内装・内観・雰囲気の写真｜駅前の17階',
    'Business Airport 渋谷フクラス（渋谷フクラス17階）の内装・内観・雰囲気を写真で。渋谷駅前の高層階のコワーキング、個室、会議室、20名のイベントスペースを歩く順番で紹介します。'),
  'business-airport-shibuya-nanpeidai': ('Business Airport 渋谷南平台｜内装・内観・雰囲気の写真｜SHIBUYA SOLASTA 3階',
    'Business Airport 渋谷南平台（SHIBUYA SOLASTA 3階）の内装・内観・雰囲気を写真で。エンターテインメントシティ渋谷から世界へ。シェアワークスペース、個室、会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'andwork-shibuya': {'streetAddress': '東京都渋谷区神南1-20-13', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-24:00'},
  'andwork-azabujuban': {'streetAddress': '東京都港区麻布十番1-5-23', 'addressLocality': '麻布十番', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-22:00'},
  'andwork-shibuya-higashi': {'streetAddress': '東京都渋谷区東1-29-3 HOTEL GRAPHY 渋谷 1階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo,Tu,Th,Fr 11:00-18:00'},
  'co-ba-akasaka': {'streetAddress': '東京都港区赤坂2-10-2 吉川ビル2階', 'addressLocality': '赤坂', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'business-airport-tokyo': {'streetAddress': '東京都千代田区丸の内1-1-3 日本生命丸の内ガーデンタワー3F', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Su 10:00-18:00'},
  'business-airport-marunouchi': {'streetAddress': '東京都千代田区丸の内2-2-1 岸本ビルヂング6F', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00'},
  'business-airport-hibiya': {'streetAddress': '東京都千代田区有楽町1-2-2 東宝日比谷ビル9F', 'addressLocality': '日比谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa-Su 10:00-18:00'},
  'business-airport-kyobashi': {'streetAddress': '東京都中央区京橋2-7-8 FPG links KYOBASHI 2F・4F〜8F', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00'},
  'business-airport-shibuya-fukuras': {'streetAddress': '東京都渋谷区道玄坂1-2-3 渋谷フクラス17F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Su 10:00-18:00'},
  'business-airport-shibuya-nanpeidai': {'streetAddress': '東京都渋谷区道玄坂1-21-1 SHIBUYA SOLASTA 3F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 _e ----
# ===== SEO と住所（seo_<brand>.py に足す分） =====
SEO_ADD = {
  'workstyling-tokyo-midtown-hibiya': ('ワークスタイリング 東京ミッドタウン日比谷｜内装・内観・雰囲気の写真｜ZEN MODERN',
    'ワークスタイリング 東京ミッドタウン日比谷（日比谷三井タワー12階）の内装・内観・雰囲気を写真で。日本の伝統文様をあしらった「ZEN MODERN」のオープンスペース、会議室、個室を歩く順番で紹介します。'),
  'diagonal-run-tokyo': ('DIAGONAL RUN TOKYO 京橋｜内装・内観・雰囲気の写真｜東京と全国が交わる',
    'DIAGONAL RUN TOKYO（京橋MIDビル4階）の内装・内観・雰囲気を写真で。東京と全国各地、人と企業とアイデアが交わるコワーキング。フリーデスク、ブース、会議室を歩く順番で紹介します。'),
  'birth-work-kanda': ('BIRTH WORK 神田｜内装・内観・雰囲気の写真｜成長型フリーワーキングオフィス',
    'BIRTH WORK 神田（神田髙木ビル）の内装・内観・雰囲気を写真で。6階の眺めの良いワークスペース、窓に面した4階と7階の個室。会社の成長に合わせて移れる拠点を、歩く順番で紹介します。'),
  'birth-work-toranomon': ('BIRTH WORK 虎の門｜内装・内観・雰囲気の写真｜書斎のようなセカンドオフィス',
    'BIRTH WORK 虎の門（西新橋1丁目）の内装・内観・雰囲気を写真で。木を基調に小分けにした2階の集中ゾーン、3階の打ち合わせとリラックスのゾーンを歩く順番で紹介します。'),
  'business-airport-kanda': ('Business Airport 神田｜内装・内観・雰囲気の写真｜レトロと新しさの共存',
    'Business Airport 神田（oak神田鍛冶町7階）の内装・内観・雰囲気を写真で。レトロな様式に新しいトレンドを散りばめた、不思議な落ち着きのワークプレイスを歩く順番で紹介します。'),
  'business-airport-shimbashi': ('Business Airport 新橋｜内装・内観・雰囲気の写真｜鉄道発祥の地のモチーフ',
    'Business Airport 新橋（新橋プレイス6〜8階）の内装・内観・雰囲気を写真で。鉄道発祥の地・新橋を思わせるモチーフが満載のワークプレイス。コワーキング、個室、4つの会議室を歩く順番で紹介します。'),
  'business-airport-tamachi': ('Business Airport 田町｜内装・内観・雰囲気の写真｜格式あるオフィスを継ぐ',
    'Business Airport 田町（田町スクエア2階）の内装・内観・雰囲気を写真で。格式あるオフィスの姿を継承し、落ち着きと機能性が共存するワークプレイスを、歩く順番で紹介します。'),
  'business-airport-shinagawa': ('Business Airport 品川｜内装・内観・雰囲気の写真｜太陽生命品川ビル28階',
    'Business Airport 品川（太陽生命品川ビル28階）の内装・内観・雰囲気を写真で。ビジネスの成功は品川から。高層階のコワーキング、個室、会議室を歩く順番で紹介します。'),
  'business-airport-ebisu': ('Business Airport 恵比寿｜内装・内観・雰囲気の写真｜柔らかな曲線の基地',
    'Business Airport 恵比寿（恵比寿ビジネスタワー2・10階）の内装・内観・雰囲気を写真で。恵比寿の街を柔らかな曲線で表した、基地のようなワークプレイスを歩く順番で紹介します。'),
  'business-airport-shinjuku3chome': ('Business Airport 新宿三丁目｜内装・内観・雰囲気の写真｜街の多様性を表す',
    'Business Airport 新宿三丁目（キュープラザ新宿三丁目4〜6階）の内装・内観・雰囲気を写真で。街を行く人々の多様性を表したワークプレイス。シェアワークスペース、個室、会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'workstyling-tokyo-midtown-hibiya': {'streetAddress': '東京都千代田区有楽町1-1-2 日比谷三井タワー12階', 'addressLocality': '日比谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'diagonal-run-tokyo': {'streetAddress': '東京都中央区京橋2丁目13-10 京橋MIDビル 4階', 'addressLocality': '京橋', 'addressRegion': '東京都'},
  'birth-work-kanda': {'streetAddress': '東京都千代田区神田錦町1-17-1 神田髙木ビル', 'addressLocality': '神田', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'birth-work-toranomon': {'streetAddress': '東京都港区西新橋1-7-5', 'addressLocality': '虎ノ門', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'business-airport-kanda': {'streetAddress': '東京都千代田区神田鍛冶町3-4 oak神田鍛冶町7F', 'addressLocality': '神田', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00, Sa 10:00-18:00'},
  'business-airport-shimbashi': {'streetAddress': '東京都港区新橋1-12-9 新橋プレイス6F・7F・8F', 'addressLocality': '新橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
  'business-airport-tamachi': {'streetAddress': '東京都港区芝5-26-24 田町スクエア2F', 'addressLocality': '田町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00'},
  'business-airport-shinagawa': {'streetAddress': '東京都港区港南2-16-2 太陽生命品川ビル28F', 'addressLocality': '品川', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'business-airport-ebisu': {'streetAddress': '東京都渋谷区恵比寿1-19-19 恵比寿ビジネスタワー2F・10F', 'addressLocality': '恵比寿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
  'business-airport-shinjuku3chome': {'streetAddress': '東京都新宿区新宿3-5-6 キュープラザ新宿三丁目 4F・5F・6F', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:00, Sa 10:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 _f ----
# ===== SEO と住所（seo_<brand>.py に足す分） =====
SEO_ADD = {
  'senq-kyobashi': ('SENQ 京橋｜内装・内観・雰囲気の写真｜京橋エドグランの FOOD INNOVATION',
    'SENQ 京橋（京橋エドグラン3・4階）の内装・内観・雰囲気を写真で。京橋駅直結、テーマは FOOD INNOVATION。約60席のラウンジ、ルーム、ブース、会議室を歩く順番で紹介します。'),
  'senq-kasumigaseki': ('SENQ 霞が関｜内装・内観・雰囲気の写真｜LEAD JAPAN と掘りごたつ',
    'SENQ 霞が関（日土地ビル2階）の内装・内観・雰囲気を写真で。テーマは LEAD JAPAN。80名のラウンジ、サロン、ダイニング、掘りごたつ、ブースを歩く順番で紹介します。'),
  'senq-roppongi': ('SENQ 六本木｜内装・内観・雰囲気の写真｜9階のスカイテラス',
    'SENQ 六本木（新六本木ビル4〜9階）の内装・内観・雰囲気を写真で。テーマは CHANGE THE THEORY。約70席のコワーキング、昼と夜のスカイテラス、個室を歩く順番で紹介します。'),
  'senq-aoyama': ('SENQ 青山｜内装・内観・雰囲気の写真｜22室の CREATOR\'S VILLAGE',
    'SENQ 青山（ラティス青山スクエア2階）の内装・内観・雰囲気を写真で。テーマは CREATOR\'S VILLAGE。22室のルームと共有のラウンジ、会議室を歩く順番で紹介します。'),
  'senq-meguro': ('SENQ 目黒｜内装・内観・雰囲気の写真｜暮らしながら働く8階',
    'SENQ 目黒（目黒センタービル8階）の内装・内観・雰囲気を写真で。「暮らしながら働く」がコンセプト。ラウンジ、カフェエリア、26室のソロブース、会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'senq-kyobashi': {'streetAddress': '東京都中央区京橋二丁目2番1号 京橋エドグラン3・4F', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
  'senq-kasumigaseki': {'streetAddress': '東京都千代田区霞が関一丁目4-1 日土地ビル2F', 'addressLocality': '霞が関', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
  'senq-roppongi': {'streetAddress': '東京都港区六本木七丁目15-7 新六本木ビル4〜9F', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
  'senq-aoyama': {'streetAddress': '東京都港区南青山一丁目2-6 ラティス青山スクエア2F', 'addressLocality': '青山', 'addressRegion': '東京都'},
  'senq-meguro': {'streetAddress': '東京都品川区上大崎三丁目2-1 目黒センタービル8F', 'addressLocality': '目黒', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 cowork_add_2026-09-27_g.py ----
SEO_ADD = {
  'workstyling-tokyo-midtown-yaesu': ('ワークスタイリング 東京ミッドタウン八重洲｜内装・内観・雰囲気の写真｜東京駅直結',
    'ワークスタイリング 東京ミッドタウン八重洲（八重洲セントラルタワー7階）の内装・内観・雰囲気を写真で。東京駅と地下で直結し土日も開くシェアオフィス。会議室、個室を歩く順番で紹介します。'),
  'workstyling-otemachi': ('ワークスタイリング 大手町｜内装・内観・雰囲気の写真｜芸術作品モチーフの会議室',
    'ワークスタイリング 大手町（Otemachi Oneタワー6階）の内装・内観・雰囲気を写真で。白基調のモダンな空間と、世界の芸術作品をモチーフにした会議室を歩く順番で紹介します。'),
  'workstyling-yaesu-kitaguchi': ('ワークスタイリング 八重洲北口｜内装・内観・雰囲気の写真｜東京駅直結の17階',
    'ワークスタイリング 八重洲北口（グラントウキョウノースタワー17階）の内装・内観・雰囲気を写真で。東京駅直結の高層階のオープンスペース、会議室、個室を歩く順番で紹介します。'),
  'workstyling-yaesu-minamiguchi': ('ワークスタイリング 八重洲南口｜内装・内観・雰囲気の写真｜土日も22時まで',
    'ワークスタイリング 八重洲南口（パシフィックセンチュリープレイス丸の内2階）の内装・内観・雰囲気を写真で。土日も22時まで開くオープンスペース、会議室、個室を歩く順番で紹介します。'),
  'workstyling-nihonbashi-mitsui-tower': ('ワークスタイリング 日本橋三井タワー｜内装・内観・雰囲気の写真｜WORKSTYLING LAB',
    'ワークスタイリング 日本橋三井タワー（6階）の内装・内観・雰囲気を写真で。コンセプトは「WORKSTYLING LAB」。テーマの異なる9つの会議室とオープンスペースを歩く順番で紹介します。'),
  'workstyling-nihonbashi-takashimaya-mitsui': ('ワークスタイリング 日本橋髙島屋三井ビル｜内装・内観・雰囲気の写真｜日本橋駅直結',
    'ワークスタイリング 日本橋髙島屋三井ビル（9階）の内装・内観・雰囲気を写真で。日本橋駅直結で登記もできるシェアオフィス。オープンスペース、会議室、個室を歩く順番で紹介します。'),
  'workstyling-nihonbashi-ichome': ('ワークスタイリング 日本橋一丁目｜内装・内観・雰囲気の写真｜レンタルオフィスも',
    'ワークスタイリング 日本橋一丁目（日本橋一丁目三井ビルディング5階）の内装・内観・雰囲気を写真で。日本橋駅直結、オープンスペースからレンタルオフィスまでを歩く順番で紹介します。'),
  'workstyling-ginza': ('ワークスタイリング 銀座｜内装・内観・雰囲気の写真｜銀座駅1分、土日も営業',
    'ワークスタイリング 銀座（ギンザ・グラッセ9階）の内装・内観・雰囲気を写真で。銀座駅から徒歩1分、土日祝も22時まで開くシェアオフィス。会議室と個室を歩く順番で紹介します。'),
  'workstyling-shiodome-city-center': ('ワークスタイリング 汐留シティーセンター｜内装・内観・雰囲気の写真｜INDUSTRY+FOREST',
    'ワークスタイリング 汐留シティーセンター（5階）の内装・内観・雰囲気を写真で。駅舎のようなエントランスと緑豊かな「INDUSTRY+FOREST」の空間を、歩く順番で紹介します。'),
  'workstyling-shinbashi': ('ワークスタイリング 新橋｜内装・内観・雰囲気の写真｜新橋駅徒歩1分',
    'ワークスタイリング 新橋（新橋M-SQUARE 2階）の内装・内観・雰囲気を写真で。新橋駅から徒歩1分、予約なしで使えるオープンスペースと会議室、個室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'workstyling-tokyo-midtown-yaesu': {'streetAddress': '東京都中央区八重洲2-2-1 東京ミッドタウン八重洲 八重洲セントラルタワー7階', 'addressLocality': '八重洲', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00, Sa-Su 10:00-18:00'},
  'workstyling-otemachi': {'streetAddress': '東京都千代田区大手町1-2-1 Otemachi Oneタワー6階', 'addressLocality': '大手町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-yaesu-kitaguchi': {'streetAddress': '東京都千代田区丸の内1-9-1 グラントウキョウノースタワー17階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-yaesu-minamiguchi': {'streetAddress': '東京都千代田区丸の内1-11-1 パシフィックセンチュリープレイス丸の内2階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-22:00'},
  'workstyling-nihonbashi-mitsui-tower': {'streetAddress': '東京都中央区日本橋室町二丁目1番1号 日本橋三井タワー6階', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-nihonbashi-takashimaya-mitsui': {'streetAddress': '東京都中央区日本橋二丁目5番1号 日本橋髙島屋三井ビルディング9階', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-nihonbashi-ichome': {'streetAddress': '東京都中央区日本橋1丁目4-1 日本橋一丁目三井ビルディング5階', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-ginza': {'streetAddress': '東京都中央区銀座3-2-15 ギンザ・グラッセ9階', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-22:00'},
  'workstyling-shiodome-city-center': {'streetAddress': '東京都港区東新橋1-5-2 汐留シティセンター5階', 'addressLocality': '汐留', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-shinbashi': {'streetAddress': '東京都港区新橋1-10-6 新橋M-SQUARE 2階', 'addressLocality': '新橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 cowork_add_2026-09-27_h.py ----
SEO_ADD = {
  'workstyling-hamamatsucho': ('ワークスタイリング 浜松町｜内装・内観・雰囲気の写真｜浜松町・大門から徒歩2分',
    'ワークスタイリング 浜松町（オリックス浜松町ビル3階）の内装・内観・雰囲気を写真で。浜松町駅と大門駅から歩いて2分。予約なしで座れるオープンスペース、会議室、個室を歩く順番で紹介します。'),
  'workstyling-omotesando': ('ワークスタイリング 表参道｜内装・内観・雰囲気の写真｜平日夜と土日も営業',
    'ワークスタイリング 表参道（ミヤヒロビル4階・8階）の内装・内観・雰囲気を写真で。平日は22時30分まで、土日祝日も開く青山通り沿いの拠点。オープンスペース、会議室、個室を紹介します。'),
  'workstyling-shibuya': ('ワークスタイリング 渋谷｜内装・内観・雰囲気の写真｜渋谷駅東口から徒歩4分',
    'ワークスタイリング 渋谷（渋谷パークビル3階）の内装・内観・雰囲気を写真で。渋谷駅の東口から歩いて4分。予約なしで座れるオープンスペース、12名までの会議室、個室を歩く順番で紹介します。'),
  'workstyling-shibuya-sakurastage': ('ワークスタイリング 渋谷サクラステージ｜内装・内観・雰囲気の写真｜最大108名のオープンスペース',
    'ワークスタイリング 渋谷サクラステージ（SAKURAサイド2階）の内装・内観・雰囲気を写真で。三井不動産が運営する、最大108名のオープンスペースと土日営業の拠点。会議室、個室、レンタルオフィスも紹介。'),
  'workstyling-meguro': ('ワークスタイリング 目黒｜内装・内観・雰囲気の写真｜目黒駅から徒歩1分',
    'ワークスタイリング 目黒（目黒ヒルトップウォーク5階）の内装・内観・雰囲気を写真で。目黒駅から歩いて1分。エントランス、オープンスペース、12名までの会議室、個室を歩く順番で紹介します。'),
  'workstyling-nakameguro': ('ワークスタイリング 中目黒｜内装・内観・雰囲気の写真｜中目黒駅から徒歩2分',
    'ワークスタイリング 中目黒（中目黒GS第一ビル8階）の内装・内観・雰囲気を写真で。中目黒駅の東口から歩いて2分。予約なしで座れるオープンスペース、会議室、個室を歩く順番で紹介します。'),
  'workstyling-ebisu': ('ワークスタイリング 恵比寿｜内装・内観・雰囲気の写真｜150名のカンファレンスルーム',
    'ワークスタイリング 恵比寿（フジワラビルディング8階）の内装・内観・雰囲気を写真で。恵比寿駅から徒歩1分。オープンスペース、会議室、150名まで入るカンファレンスルーム、個室を紹介します。'),
  'workstyling-shinagawa': ('ワークスタイリング 品川｜内装・内観・雰囲気の写真｜働くための巣',
    'ワークスタイリング 品川（NBF品川タワー5・6階）の内装・内観・雰囲気を写真で。「極上のソロワークができる、働くための巣」がコンセプト。多種多様な席、会議室、個室、レンタルオフィスを紹介します。'),
  'workstyling-tamachi-mitaguchi': ('ワークスタイリング 田町三田口｜内装・内観・雰囲気の写真｜田町・三田から徒歩1分',
    'ワークスタイリング 田町三田口（田町センタービル13階）の内装・内観・雰囲気を写真で。田町駅と三田駅から歩いて1分。オープンスペース、12名までの会議室、個室を歩く順番で紹介します。'),
  'workstyling-shinjuku-mitsui-building': ('ワークスタイリング 新宿三井ビルディング｜内装・内観・雰囲気の写真｜RETRO FUTURE',
    'ワークスタイリング 新宿三井ビルディング（11階）の内装・内観・雰囲気を写真で。過去と未来を横断する「RETRO FUTURE」の空間。オープンスペース、会議室、個室、レンタルオフィスを紹介します。'),
}
PLACE_ADD = {
  'workstyling-hamamatsucho': {'streetAddress': '東京都港区浜松町1-24-8 オリックス浜松町ビル3階', 'addressLocality': '浜松町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-omotesando': {'streetAddress': '東京都港区北青山3-5-15 ミヤヒロビル4階・8階', 'addressLocality': '表参道', 'addressRegion': '東京都', 'openingHours': 'Mo-Tu 08:00-22:30, We 08:00-21:00, Th-Fr 08:00-22:30, Sa-Su 10:00-18:00'},
  'workstyling-shibuya': {'streetAddress': '東京都渋谷区渋谷3-6-6 渋谷パークビル3階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-shibuya-sakurastage': {'streetAddress': '東京都渋谷区桜丘町3-4 渋谷サクラステージ SAKURAサイド2階201区画', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00, Sa-Su 10:00-18:00'},
  'workstyling-meguro': {'streetAddress': '東京都品川区上大崎4-1-5 目黒ヒルトップウォーク5階', 'addressLocality': '目黒', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-nakameguro': {'streetAddress': '東京都目黒区上目黒2-9-1 中目黒GS第一ビル8階', 'addressLocality': '中目黒', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-ebisu': {'streetAddress': '東京都渋谷区恵比寿西1-10-11 フジワラビルディング8階', 'addressLocality': '恵比寿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-shinagawa': {'streetAddress': '東京都港区港南2-16-5 NBF品川タワー5階・6階', 'addressLocality': '品川', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-tamachi-mitaguchi': {'streetAddress': '東京都港区芝5-34-7 田町センタービル13階', 'addressLocality': '田町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-shinjuku-mitsui-building': {'streetAddress': '東京都新宿区西新宿2-1-1 新宿三井ビルディング11階', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 cowork_add_2026-09-27_i.py ----
SEO_ADD = {
  'workstyling-shinjuku-higashiguchi': ('ワークスタイリング 新宿東口｜内装・内観・雰囲気の写真｜駅直結で土日祝も営業',
    'ワークスタイリング 新宿東口（NEWNO･GS新宿8階）の内装・内観・雰囲気を写真で。丸ノ内線新宿駅B12出口直結、土日祝も開くシェアオフィスのオープンスペース、会議室、個室を紹介します。'),
  'workstyling-iidabashi-grand-bloom': ('ワークスタイリング 飯田橋グラン・ブルーム｜内装・内観・雰囲気の写真｜2階と9階',
    'ワークスタイリング 飯田橋グラン・ブルーム（2階・9階）の内装・内観・雰囲気を写真で。JR飯田橋駅西口から徒歩1分、二つのフロアのオープンスペース、会議室、個室、レンタルオフィスを紹介します。'),
  'workstyling-kasumigaseki-building': ('ワークスタイリング 霞が関ビルディング｜内装・内観・雰囲気の写真｜36階の高層階',
    'ワークスタイリング 霞が関ビルディング（36階）の内装・内観・雰囲気を写真で。虎ノ門駅から徒歩2分、80名まで入る会議室を持つ高層階のシェアオフィスのオープンスペース、個室を紹介します。'),
  'workstyling-tokyo-midtown-roppongi': ('ワークスタイリング 東京ミッドタウン（六本木）｜内装・内観・雰囲気の写真｜アートを加えた空間',
    'ワークスタイリング 東京ミッドタウン（東京ミッドタウン・タワー18階）の内装・内観・雰囲気を写真で。「デザイン思考」の場に「アート」を加えた空間のオープンスペース、会議室、個室を紹介します。'),
  'workstyling-futako-tamagawa': ('ワークスタイリング 二子玉川｜内装・内観・雰囲気の写真｜ショッピングセンターの中',
    'ワークスタイリング 二子玉川（玉川髙島屋SC ケヤキコート1階）の内装・内観・雰囲気を写真で。商業施設の中にある、土日祝も開くシェアオフィスのオープンスペース、会議室、個室を紹介します。'),
  'h1t-roppongi': ('H¹T六本木｜内装・内観・雰囲気の写真｜駅から徒歩1分、席の種類が多い',
    'H¹T六本木（誠志堂ビル7階）の内装・内観・雰囲気を写真で。六本木駅4a出口から徒歩1分、オープンスペース、ブース、ボックス、個室10室と会議室2室がそろう法人向けシェアオフィスを紹介します。'),
  'h1t-ikebukuro-higashiguchi-the-garden': ('H¹T池袋東口 THE GARDEN｜内装・内観・雰囲気の写真｜個室18室、土日祝も営業',
    'H¹T池袋東口 THE GARDEN（池袋伊藤ビル10階）の内装・内観・雰囲気を写真で。JR池袋駅北改札から徒歩3分、一人用の個室18室と会議室2室、土日祝も7時から開く法人向けシェアオフィスです。'),
  'h1t-ochanomizu-the-garden': ('H¹T御茶ノ水 THE GARDEN｜内装・内観・雰囲気の写真｜駅から徒歩1分の個室',
    'H¹T御茶ノ水 THE GARDEN（御茶ノ水穂高ビル2階）の内装・内観・雰囲気を写真で。JR御茶ノ水駅聖橋口から徒歩1分、一人用の個室11室だけで構成された法人向けシェアオフィスを紹介します。'),
  'h1t-shinjuku-nishiguchi': ('H¹T新宿西口｜内装・内観・雰囲気の写真｜会議室7室の法人向けシェアオフィス',
    'H¹T新宿西口（西新宿昭和ビル9階）の内装・内観・雰囲気を写真で。新宿駅西口から徒歩2分、オープンスペース、ボックス、個室18室、会議室7室がそろう法人向けシェアオフィスを紹介します。'),
  'h1t-omotesando': ('H¹T表参道｜内装・内観・雰囲気の写真｜個室15室と10名の会議室',
    'H¹T表参道（プレファス表参道4階）の内装・内観・雰囲気を写真で。表参道駅A2出口から徒歩2分、一人用の個室15室と2〜10名の会議室を持つ、土日祝も開く法人向けシェアオフィスを紹介します。'),
}
PLACE_ADD = {
  'workstyling-shinjuku-higashiguchi': {'streetAddress': '東京都新宿区新宿3-24-1 NEWNO･GS新宿8階', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00, Sa-Su 10:00-18:00'},
  'workstyling-iidabashi-grand-bloom': {'streetAddress': '東京都千代田区富士見2-10-2 飯田橋グラン・ブルーム 2階・9階', 'addressLocality': '飯田橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-kasumigaseki-building': {'streetAddress': '東京都千代田区霞が関3-2-5 霞が関ビルディング 36階', 'addressLocality': '霞が関', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-tokyo-midtown-roppongi': {'streetAddress': '東京都港区赤坂9-7-1 東京ミッドタウン・タワー18階', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'workstyling-futako-tamagawa': {'streetAddress': '東京都世田谷区玉川2-27-8 玉川髙島屋ショッピングセンター ケヤキコート1階', 'addressLocality': '二子玉川', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00, Sa-Su 10:00-18:00'},
  'h1t-roppongi': {'streetAddress': '東京都港区六本木7-14-10 誠志堂ビル7階', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:30-22:00'},
  'h1t-ikebukuro-higashiguchi-the-garden': {'streetAddress': '東京都豊島区東池袋1-3-5 池袋伊藤ビル10階', 'addressLocality': '池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-22:30'},
  'h1t-ochanomizu-the-garden': {'streetAddress': '東京都千代田区神田駿河台4-5-3 御茶ノ水穂高ビル2階', 'addressLocality': '御茶ノ水', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'h1t-shinjuku-nishiguchi': {'streetAddress': '東京都新宿区西新宿1-13-12 西新宿昭和ビル9階', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-22:00'},
  'h1t-omotesando': {'streetAddress': '東京都渋谷区神宮前4-11-6 プレファス表参道4階', 'addressLocality': '表参道', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:30-21:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 cowork_add_2026-09-27_j.py ----
SEO_ADD = {
  'fabbit-shibuya-ekimae': ('fabbit 渋谷駅前｜内装・内観・雰囲気の写真｜渋谷駅2分と TKP の会議室',
    'fabbit 渋谷駅前（渋谷東口ビル5階）の内装・内観・雰囲気を写真で。渋谷駅から徒歩2分、6名用から18名規模の完全個室と、同じフロアの TKP の会議室を歩く順番で紹介します。'),
  'crosscoop-shibuya-nextsite': ('クロスコープ 渋谷ネクストサイト｜内装・内観・雰囲気の写真｜植栽のラウンジ',
    'クロスコープ 渋谷ネクストサイト（ネクストサイト渋谷ビル5・6階）の内装・内観・雰囲気を写真で。＋PERFORMANCE を掲げ、植栽のラウンジ、7室の会議室、19室のテレブースを紹介します。'),
  'crosscoop-shinjuku-avenue': ('クロスコープ 新宿AVENUE｜内装・内観・雰囲気の写真｜7階の24時間ラウンジ',
    'クロスコープ 新宿AVENUE（4〜7階）の内装・内観・雰囲気を写真で。新宿三丁目駅と新宿御苑前駅の間、7階の24時間ラウンジ、8室の会議室、大きな窓の個室を歩く順番で紹介します。'),
  'fabbit-ginza': ('fabbit 銀座｜内装・内観・雰囲気の写真｜銀座一丁目のコワーキングラウンジ',
    'fabbit 銀座（ヒューリック銀座一丁目昭和通りビル7階）の内装・内観・雰囲気を写真で。銀座一丁目駅3分、コワーキングラウンジと2〜6名の完全個室を歩く順番で紹介します。'),
  'fabbit-kyobashi': ('fabbit 京橋｜内装・内観・雰囲気の写真｜東京駅4分のセントラルビル',
    'fabbit 京橋（セントラルビル2階）の内装・内観・雰囲気を写真で。東京駅の八重洲地下街24番出口すぐ、コワーキングラウンジと2〜6名用の完全個室を歩く順番で紹介します。'),
  'crosscoop-roppongi-next': ('クロスコープ 六本木NEXT｜内装・内観・雰囲気の写真｜60席のラウンジ',
    'クロスコープ 六本木NEXT（ラウンドクロス六本木4・5階）の内装・内観・雰囲気を写真で。2フロア約490坪、約60席のコワーキングラウンジ、テレブース、窓付きの個室を紹介します。'),
  'fabbit-aoyama-itchome': ('fabbit 青山一丁目｜内装・内観・雰囲気の写真｜青山タワープレイス8階',
    'fabbit 青山一丁目（青山タワープレイス8階）の内装・内観・雰囲気を写真で。青山一丁目駅2分、コワーキングラウンジと2名用から20名規模の完全個室を歩く順番で紹介します。'),
  'crosscoop-nihonbashi': ('クロスコープ 日本橋｜内装・内観・雰囲気の写真｜約43席のラウンジ',
    'クロスコープ 日本橋（日本橋三丁目スクエア2・3階）の内装・内観・雰囲気を写真で。約43席のラウンジ、コワーキングエリア、リフレッシュラウンジ、会議室、テレブースを紹介します。'),
  'crosscoop-aoyama': ('クロスコープ 青山｜内装・内観・雰囲気の写真｜外苑前駅2分の3フロア',
    'クロスコープ 青山（Landwork青山ビル2・4・5階）の内装・内観・雰囲気を写真で。外苑前駅2分、受付と待合、5室の会議室、1名用から20名用の個室を歩く順番で紹介します。'),
  'crosscoop-shibuya': ('クロスコープ 渋谷｜内装・内観・雰囲気の写真｜宮益坂の30席のラウンジ',
    'クロスコープ 渋谷（ヒューリック渋谷一丁目ビル5〜7階）の内装・内観・雰囲気を写真で。宮益坂の途中、30席のコワーキングラウンジ、リフレッシュラウンジ、会議室、個室を紹介します。'),
}
PLACE_ADD = {
  'fabbit-shibuya-ekimae': {'streetAddress': '東京都渋谷区渋谷2-22-3 渋谷東口ビル5階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-shibuya-nextsite': {'streetAddress': '東京都渋谷区渋谷2-12-4 ネクストサイト渋谷ビル5・6F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-shinjuku-avenue': {'streetAddress': '東京都新宿区新宿2丁目5-12 4〜7F', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'fabbit-ginza': {'streetAddress': '東京都中央区銀座1丁目15-4 ヒューリック銀座一丁目昭和通りビル7階', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'fabbit-kyobashi': {'streetAddress': '東京都中央区京橋1-1-5 セントラルビル2階', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-roppongi-next': {'streetAddress': '東京都港区六本木7丁目14-23 ラウンドクロス六本木4・5F', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'fabbit-aoyama-itchome': {'streetAddress': '東京都港区赤坂8丁目4-14 青山タワープレイス8階', 'addressLocality': '赤坂', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-nihonbashi': {'streetAddress': '東京都中央区日本橋3丁目9-1 日本橋三丁目スクエア2・3F', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-aoyama': {'streetAddress': '東京都港区北青山2-7-26 Landwork青山ビル 2・4・5F', 'addressLocality': '北青山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-shibuya': {'streetAddress': '東京都渋谷区渋谷1丁目3-9 ヒューリック渋谷一丁目ビル5〜7F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


# ---- 2026-09-27 追加 cowork_add_2026-09-27_k.py ----
SEO_ADD = {
  'the-hub-nihonbashi-odenmacho': ('THE HUB 日本橋大伝馬町｜内装・内観・雰囲気の写真｜有人フロントと81室',
    'THE HUB 日本橋大伝馬町（日本橋大富ビル2・3階）の内装・内観・雰囲気を写真で。小伝馬町駅3分、有人フロント付き。全81室の個室、会議室、ブース席を歩く順番で紹介します。'),
  'the-hub-kayabacho': ('THE HUB 茅場町｜内装・内観・雰囲気の写真｜新川の2〜5名用個室',
    'THE HUB 茅場町（AIビル茅場町2〜5階）の内装・内観・雰囲気を写真で。茅場町駅4分、2〜5名用の個室オフィスに、ウェイティングスペース、会議室、ブース席を歩く順番で紹介します。'),
  'the-hub-nihonbashi-kayabacho': ('THE HUB 日本橋茅場町｜内装・内観・雰囲気の写真｜士業に人気のコンパクトオフィス',
    'THE HUB 日本橋茅場町（BIZMARKS 日本橋茅場町）の内装・内観・雰囲気を写真で。東証の近く、1階に受付と会議室。ラウンジと全室個室のオフィスを歩く順番で紹介します。'),
  'the-hub-nihonbashi-kabutocho': ('THE HUB 日本橋兜町｜内装・内観・雰囲気の写真｜全室完全個室と屋上テラス',
    'THE HUB 日本橋兜町（兜町平和ダイヤビル）の内装・内観・雰囲気を写真で。SOHO物件を大胆にリニューアル。全室完全個室、会議室、ラウンジ、屋上テラスを歩く順番で紹介します。'),
  'the-hub-higashi-nihonbashi': ('THE HUB 東日本橋｜内装・内観・雰囲気の写真｜1〜4名用の個室',
    'THE HUB 東日本橋（三幸日本橋プラザビル5〜7階）の内装・内観・雰囲気を写真で。4駅が使える立地に、1〜4名用の個室オフィスとMTGスペースを歩く順番で紹介します。'),
  'the-hub-ginza-6chome': ('THE HUB 銀座6丁目｜内装・内観・雰囲気の写真｜高品質フロントの銀座オフィス',
    'THE HUB 銀座6丁目（銀座石井ビル4〜7階）の内装・内観・雰囲気を写真で。東銀座駅2分、高品質フロント付き。2〜4名用の個室、会議室、ブース席を歩く順番で紹介します。'),
  'the-hub-ginza-oct': ('THE HUB 銀座OCT｜内装・内観・雰囲気の写真｜一棟まるごとのシェアオフィス',
    'THE HUB 銀座OCT（銀座8丁目、地上10階の一棟）の内装・内観・雰囲気を写真で。ラウンジ、フロント、7室の会議室・応接室、4〜35名用の個室、屋上テラスを歩く順番で紹介します。'),
  'senq-aoyama-namikidori': ('SENQ 青山並木通り｜内装・内観・雰囲気の写真｜BUILD NEXT CULTURES',
    'SENQ 青山並木通り（第一法規本社ビル3階）の内装・内観・雰囲気を写真で。テーマは BUILD NEXT CULTURES。ラウンジ、カフェコーナー、18室のルーム、ソロブースを歩く順番で紹介します。'),
  'crosscoop-shinjuku': ('CROSSCOOP 新宿SOUTH｜内装・内観・雰囲気の写真｜会議室15室のレンタルオフィス',
    'クロスコープ 新宿SOUTH（ヒューリック新宿四丁目ビル3・5・6階）の内装・内観・雰囲気を写真で。新宿三丁目駅1分。ラウンジ、15室の会議室、個室を歩く順番で紹介します。'),
  'crosscoop-shimbashi': ('CROSSCOOP 新橋｜内装・内観・雰囲気の写真｜約96席のラウンジと個室',
    'クロスコープ新橋（アーバンネット内幸町ビル3〜5階）の内装・内観・雰囲気を写真で。内幸町駅2分。約96席のラウンジ、会議室、セミナールーム、100名用までの個室を紹介します。'),
}
PLACE_ADD = {
  'the-hub-nihonbashi-odenmacho': {'streetAddress': '東京都中央区日本橋大伝馬町13-7 日本橋大富ビル2-3F', 'addressLocality': '日本橋大伝馬町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-kayabacho': {'streetAddress': '東京都中央区新川1-6-12 AIビル茅場町2-5F', 'addressLocality': '茅場町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-nihonbashi-kayabacho': {'streetAddress': '東京都中央区日本橋小網町8-2 BIZMARKS 日本橋茅場町', 'addressLocality': '日本橋小網町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-nihonbashi-kabutocho': {'streetAddress': '東京都中央区日本橋兜町9-5 兜町平和ダイヤビル', 'addressLocality': '日本橋兜町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-higashi-nihonbashi': {'streetAddress': '東京都中央区東日本橋1-1-20 三幸日本橋プラザビル5-7F', 'addressLocality': '東日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-ginza-6chome': {'streetAddress': '東京都中央区銀座6-14-8 銀座石井ビル4-7F', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'the-hub-ginza-oct': {'streetAddress': '東京都中央区銀座8-17-5 THE HUB 銀座 OCT', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 10:00-18:30'},
  'senq-aoyama-namikidori': {'streetAddress': '東京都港区南青山二丁目11-17 第一法規本社ビル3F', 'addressLocality': '南青山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-22:00'},
  'crosscoop-shinjuku': {'streetAddress': '東京都新宿区新宿4-3-17 ヒューリック新宿四丁目ビル3・5・6F', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'crosscoop-shimbashi': {'streetAddress': '東京都港区新橋1-1-13 アーバンネット内幸町ビル3F', 'addressLocality': '新橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# 2026-09-28 cowork_add_2026-09-28_a.py
SEO_ADD = {
  'wework-marunouchi-kitaguchi': ('WeWork 丸の内北口｜内装・内観・雰囲気の写真｜フロアごとに違うラウンジ',
    'WeWork 丸の内北口（丸の内北口ビルディング7〜11階）の内装・内観・雰囲気を写真で。東京駅直結、リラックスがコンセプト。フロアごとのラウンジ、35室の会議室を歩く順番で紹介します。'),
  'wework-kamiyacho-trust-tower': ('WeWork 神谷町トラストタワー｜内装・内観・雰囲気の写真｜虎ノ門の過去と現代',
    'WeWork 神谷町トラストタワー（21〜24階）の内装・内観・雰囲気を写真で。神谷町駅直結の国内最大規模の拠点。和の要素の共用エリア、56室の会議室、アートを歩く順番で紹介します。'),
  'wework-hibiya-fort-tower': ('WeWork 日比谷FORT TOWER｜内装・内観・雰囲気の写真｜メタボリズムの8フロア',
    'WeWork 日比谷FORT TOWER（4〜11階）の内装・内観・雰囲気を写真で。内装のテーマはメタボリズム。10階のホットデスクとコミュニティバー、11階の SOHO 区画を歩く順番で紹介します。'),
  'wework-ginza-six': ('WeWork ギンザシックス｜内装・内観・雰囲気の写真｜最上階と屋上庭園',
    'WeWork ギンザシックス（GINZA SIX 13階）の内装・内観・雰囲気を写真で。銀座駅直結、街に合わせたラグジュアリーな内装。共用エリア、9室の会議室、屋上庭園を歩く順番で紹介します。'),
  'wework-kanda-square': ('WeWork KANDA SQUARE｜内装・内観・雰囲気の写真｜電気街と昔のゲーム',
    'WeWork KANDA SQUARE（神田錦町）の内装・内観・雰囲気を写真で。秋葉原の電気街と昔のゲームがテーマのアート。共用エリア、45室の会議室、専用オフィスを歩く順番で紹介します。'),
  'wework-tokyo-square-garden': ('WeWork 東京スクエアガーデン｜内装・内観・雰囲気の写真｜ワンフロアに凝縮',
    'WeWork 東京スクエアガーデン（14階）の内装・内観・雰囲気を写真で。京橋駅直結、WeWork の要素をワンフロアに凝縮。共用エリア、15室の会議室、ビル内の施設を歩く順番で紹介します。'),
  'wework-d-tower-nishishinjuku': ('WeWork Dタワー西新宿｜内装・内観・雰囲気の写真｜モダニズムと木の濃淡',
    'WeWork Dタワー西新宿（16階）の内装・内観・雰囲気を写真で。モダニズムがコンセプトの木の濃淡の空間。共用エリア、高層階の眺め、20室の会議室を歩く順番で紹介します。'),
  'wework-tk-ikedayama': ('WeWork TK 池田山｜内装・内観・雰囲気の写真｜昭和のノスタルジア',
    'WeWork TK 池田山（TK池田山ビル2階）の内装・内観・雰囲気を写真で。五反田駅から徒歩3分、昭和のノスタルジアがコンセプト。共用エリア、会議室、個室を歩く順番で紹介します。'),
  'wework-hareza-ikebukuro': ('WeWork Hareza 池袋｜内装・内観・雰囲気の写真｜アート・日本絵画・映画',
    'WeWork Hareza 池袋（Hareza Tower 高層階）の内装・内観・雰囲気を写真で。池袋のアートや日本絵画、映画に着想した内装。共用エリア、22室の会議室を歩く順番で紹介します。'),
  'wework-ark-hills-south': ('WeWork アークヒルズサウス｜内装・内観・雰囲気の写真｜アメリカンと華やかさ',
    'WeWork アークヒルズサウス（アークヒルズサウスタワー16階）の内装・内観・雰囲気を写真で。六本木一丁目駅直結、アメリカンな雰囲気の空間。共用エリアと会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'wework-marunouchi-kitaguchi': {'streetAddress': '東京都千代田区丸の内1-6-5 丸の内北口ビルディング 9F', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-20:00'},
  'wework-kamiyacho-trust-tower': {'streetAddress': '東京都港区虎ノ門4-1-1 神谷町トラストタワー 23F', 'addressLocality': '神谷町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-20:00'},
  'wework-hibiya-fort-tower': {'streetAddress': '東京都港区西新橋1-1-1 日比谷フォートタワー 10F', 'addressLocality': '西新橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-ginza-six': {'streetAddress': '東京都中央区銀座6-10-1 GINZA SIX 13F', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-kanda-square': {'streetAddress': '東京都千代田区神田錦町2-2-1 KANDA SQUARE 11F', 'addressLocality': '神田', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-tokyo-square-garden': {'streetAddress': '東京都中央区京橋3-1-1 東京スクエアガーデン 14F', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-d-tower-nishishinjuku': {'streetAddress': '東京都新宿区西新宿6-11-3 Dタワー西新宿 16F', 'addressLocality': '西新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-tk-ikedayama': {'streetAddress': '東京都品川区東五反田5-22-33 TK池田山ビル 2F', 'addressLocality': '五反田', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-hareza-ikebukuro': {'streetAddress': '東京都豊島区東池袋1-18-1 Hareza Tower 20F', 'addressLocality': '池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-20:00'},
  'wework-ark-hills-south': {'streetAddress': '東京都港区六本木1-4-5 アークヒルズサウスタワー 16F', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# 2026-09-28 cowork_add_2026-09-28_b.py
SEO_ADD = {
  'the-executive-centre-jp-tower': ('The Executive Centre JPタワー｜内装・内観・雰囲気の写真｜東京駅を見下ろすバリスタバー',
    'The Executive Centre JPタワー（11・14階）の内装・内観・雰囲気を写真で。旧東京中央郵便局を再生した東京駅直結のビル。ラウンジ、バリスタバー、個室、会議室を歩く順番で紹介します。'),
  'the-executive-centre-shin-marunouchi-center': ('The Executive Centre 新丸の内センタービル｜内装・内観・雰囲気の写真｜木と大理石の2フロア',
    'The Executive Centre 新丸の内センタービル（20・21階）の内装・内観・雰囲気を写真で。東京駅と地下直結。大理石とオークの受付、リフレッシュエリア、個室、6室の会議室を紹介します。'),
  'the-executive-centre-roppongi-hills': ('The Executive Centre 六本木ヒルズ ノースタワー｜内装・内観・雰囲気の写真｜オークと障子風の会議室',
    'The Executive Centre 六本木ヒルズ ノースタワー（16・17階）の内装・内観・雰囲気を写真で。明るいオークの仕上げと障子風の会議室。受付、リフレッシュエリア、個室を歩く順番で紹介します。'),
  'the-executive-centre-sanno-park-tower': ('The Executive Centre 山王パークタワー｜内装・内観・雰囲気の写真｜静けさのある3階',
    'The Executive Centre 山王パークタワー（3階）の内装・内観・雰囲気を写真で。溜池山王・国会議事堂前駅直結。ラウンジ、コワーキング、個室、会議室、ファンクションルームを紹介します。'),
  'the-executive-centre-cerulean-tower': ('The Executive Centre セルリアンタワー｜内装・内観・雰囲気の写真｜茶室に着想を得た受付',
    'The Executive Centre セルリアンタワー（15階）の内装・内観・雰囲気を写真で。茶室に着想を得た受付、ブース席のラウンジ、コワーキング、パントリー、個室、渋谷の眺めを紹介します。'),
  'the-executive-centre-jingumae-tower': ('The Executive Centre 神宮前タワービルディング｜内装・内観・雰囲気の写真｜英国と日本の混じる内装',
    'The Executive Centre 神宮前タワービルディング（12〜14階）の内装・内観・雰囲気を写真で。オークの床と紺の壁紙、ヴィンテージ家具。ラウンジ、個室、9室の会議室を紹介します。'),
  'the-executive-centre-meguro-arco-tower': ('The Executive Centre 目黒アルコタワー｜内装・内観・雰囲気の写真｜目黒川を見下ろす7階',
    'The Executive Centre 目黒アルコタワー（7階）の内装・内観・雰囲気を写真で。目黒川の桜並木を見下ろす木の仕上げのセンター。ラウンジ、コワーキング、個室、ボードルームを紹介します。'),
  'justco-shibuya-hikarie': ('JustCo 渋谷ヒカリエ｜内装・内観・雰囲気の写真｜渋谷駅直結の33階',
    'ジャストコ 渋谷ヒカリエ（33階）の内装・内観・雰囲気を写真で。渋谷駅直結、晴れた日は富士山まで見渡せる高さ。メインラウンジ、ホットデスク、プライベートオフィス、会議室を紹介します。'),
  'justco-shinjuku-miraina-tower': ('JustCo 新宿ミライナタワー｜内装・内観・雰囲気の写真｜新宿駅直結の18階',
    'ジャストコ 新宿ミライナタワー（18階）の内装・内観・雰囲気を写真で。新宿駅ミライナタワー改札直結。メインラウンジ、パントリー、ホットデスク、プライベートオフィス、会議室を紹介します。'),
  'justco-grantokyo-south-tower': ('JustCo グラントウキョウサウスタワー｜内装・内観・雰囲気の写真｜東京駅直結の11階',
    'ジャストコ グラントウキョウサウスタワー（11階）の内装・内観・雰囲気を写真で。東京駅直結、八重洲南口から約150m。メインラウンジ、プライベートオフィス、会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'the-executive-centre-jp-tower': {'streetAddress': '東京都千代田区丸の内2-7-2 JPタワー11・14階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-shin-marunouchi-center': {'streetAddress': '東京都千代田区丸の内1-6-2 新丸の内センタービル20・21階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-roppongi-hills': {'streetAddress': '東京都港区六本木6-2-31 六本木ヒルズノースタワー16・17階', 'addressLocality': '六本木', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-sanno-park-tower': {'streetAddress': '東京都千代田区永田町2-11-1 山王パークタワー3階', 'addressLocality': '永田町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-cerulean-tower': {'streetAddress': '東京都渋谷区桜丘町26-1 セルリアンタワー15階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'the-executive-centre-jingumae-tower': {'streetAddress': '東京都渋谷区神宮前1-5-8 神宮前タワービルディング12〜14階', 'addressLocality': '原宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-meguro-arco-tower': {'streetAddress': '東京都目黒区下目黒1-8-1 アルコタワー7階', 'addressLocality': '目黒', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'justco-shibuya-hikarie': {'streetAddress': '東京都渋谷区渋谷2-21-1 渋谷ヒカリエ33階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'justco-shinjuku-miraina-tower': {'streetAddress': '東京都新宿区新宿4-1-6 JR新宿ミライナタワー18階', 'addressLocality': '新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'justco-grantokyo-south-tower': {'streetAddress': '東京都千代田区丸の内1-9-2 グラントウキョウサウスタワー11階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# 2026-09-28 cowork_add_2026-09-28_c.py
SEO_ADD = {
  'the-hub-hanzomon': ('THE HUB 半蔵門｜内装・内観・雰囲気の写真｜麹町の4フロアと1名用ブース',
    'THE HUB 半蔵門（BIZMARKS 麹町2・3・5・6階）の内装・内観・雰囲気を写真で。半蔵門駅と麹町駅から3分。ウェイティングスペース、1〜6名用の個室、会議室、ブース席を歩く順番で紹介します。'),
  'the-hub-shimbashi': ('THE HUB 新橋｜内装・内観・雰囲気の写真｜4路線が使える第一日比谷ビル',
    'THE HUB 新橋（第一日比谷ビル4〜7階）の内装・内観・雰囲気を写真で。内幸町駅1分、新橋・虎ノ門・日比谷も徒歩圏。ラウンジ、受付、1〜9名用の個室、会議室を歩く順番で紹介します。'),
  'the-hub-akasaka': ('THE HUB 赤坂｜内装・内観・雰囲気の写真｜1階に待合と契約者ラウンジ',
    'THE HUB 赤坂（BIZMARKS 赤坂）の内装・内観・雰囲気を写真で。2020年にリノベーションした4階建て。1階の契約者専用ラウンジと待合、6名用の会議室、全室個室のオフィスを歩く順番で紹介します。'),
  'the-hub-takadanobaba': ('THE HUB 高田馬場｜内装・内観・雰囲気の写真｜新築ビルの会話・通話OKラウンジ',
    'THE HUB 高田馬場（東京三協信用金庫本店ビル6〜8階）の内装・内観・雰囲気を写真で。2023年新築、駅1分。会話・通話OKのラウンジ、完全個室のブース、1〜11名用の個室を歩く順番で紹介します。'),
  'the-hub-meguro': ('THE HUB 目黒｜内装・内観・雰囲気の写真｜少人数企業向けの駅3分オフィス',
    'THE HUB 目黒（千里馬ビル）の内装・内観・雰囲気を写真で。目黒駅西口から3分、少人数企業向けのオフィス。ラウンジ、ウェイティングスペース、会議室、1・2・5名用の個室を歩く順番で紹介します。'),
  'the-hub-toranomon': ('THE HUB 虎ノ門｜内装・内観・雰囲気の写真｜駅直結、士業・コンサル向け',
    'THE HUB 虎ノ門（新虎ノ門実業会館5階）の内装・内観・雰囲気を写真で。虎ノ門駅10番出口直結。4名用の会議室3室、MTGコーナー、ブース席、1〜5名用の個室を歩く順番で紹介します。'),
  'co-ba-chofu': ('co-ba CHOFU｜内装・内観・雰囲気の写真｜調布駅1分の仕事軸のコミュニティ',
    'co-ba CHOFU（調布・寿ビル2階）の内装・内観・雰囲気を写真で。2014年開設、「仕事軸のコミュニティ」を掲げる調布駅1分の場所。対話しやすいワークテーブル、会議室、フォンブースを紹介します。'),
  'co-ba-re-sohko-tamachi': ('co-ba Re-SOHKO 田町｜内装・内観・雰囲気の写真｜芝浦のスケルトン空間',
    'co-ba Re-SOHKO 田町（芝浦・第3東運ビル8階）の内装・内観・雰囲気を写真で。ベイエリアのスケルトン空間を生かしたコワーキングと個室、大小の会議室、屋上会議スペースを歩く順番で紹介します。'),
  'co-ba-kamikitazawa': ('co-coono KAMIKITAZAWA WORK LOUNGE｜内装・内観・雰囲気の写真｜住まいに併設したラウンジ',
    'co-coono KAMIKITAZAWA WORK LOUNGE（上北沢）の内装・内観・雰囲気を写真で。リノベーション賃貸住宅に併設し、朝6時から開くワークラウンジ。会議室やイベントスペースも紹介します。'),
  'co-ba-re-sohko-shinagawa': ('co-ba Re-SOHKO shinagawa｜内装・内観・雰囲気の写真｜港南の「ニュー倉庫街」',
    'co-ba Re-SOHKO shinagawa（港南の倉庫ビル4階）の内装・内観・雰囲気を写真で。倉庫でありショールームでもある「ニュー倉庫街」。ラウンジ、ミーティングルーム、倉庫空間を紹介します。'),
}
PLACE_ADD = {
  'the-hub-hanzomon': {'streetAddress': '東京都千代田区平河町1-3-6 BIZMARKS 麹町2-3F・5-6F', 'addressLocality': '半蔵門', 'addressRegion': '東京都'},
  'the-hub-shimbashi': {'streetAddress': '東京都港区新橋1-18-21 第一日比谷ビル4-7F', 'addressLocality': '新橋', 'addressRegion': '東京都'},
  'the-hub-akasaka': {'streetAddress': '東京都港区赤坂2-16-6 BIZMARKS 赤坂', 'addressLocality': '赤坂', 'addressRegion': '東京都'},
  'the-hub-takadanobaba': {'streetAddress': '東京都新宿区高田馬場2-17-3 東京三協信用金庫本店ビル6-8F', 'addressLocality': '高田馬場', 'addressRegion': '東京都'},
  'the-hub-meguro': {'streetAddress': '東京都品川区上大崎2-17-6 千里馬ビル', 'addressLocality': '目黒', 'addressRegion': '東京都'},
  'the-hub-toranomon': {'streetAddress': '東京都港区虎ノ門1-1-21 新虎ノ門実業会館5F', 'addressLocality': '虎ノ門', 'addressRegion': '東京都'},
  'co-ba-chofu': {'streetAddress': '東京都調布市小島町2丁目51番地2号 寿ビル2階', 'addressLocality': '調布', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-23:59'},
  'co-ba-re-sohko-tamachi': {'streetAddress': '東京都港区芝浦1-13-10 第3東運ビル8階', 'addressLocality': '田町', 'addressRegion': '東京都', 'openingHours': 'Mo-Sa 09:00-22:00'},
  'co-ba-kamikitazawa': {'streetAddress': '東京都杉並区上高井戸3-1-3', 'addressLocality': '上北沢', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 06:00-24:00'},
  'co-ba-re-sohko-shinagawa': {'streetAddress': '東京都港区港南3丁目4-27 第2東運ビル（WARE HOUSE Konan）4F', 'addressLocality': '品川', 'addressRegion': '東京都'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# ==== 2026-09-28 cowork_add_2026-09-28_d.py の SEO／場所 ====
SEO_ADD = {
  'wework-the-argyle-aoyama': ('WeWork ジ アーガイル アオヤマ｜内装・内観・雰囲気の写真｜白木とオークの共用エリア',
    'WeWork ジ アーガイル アオヤマ（the ARGYLE aoyama 6階）の内装・内観・雰囲気を写真で。青山ベルコモンズ跡地の複合ビル。白木とオークの共用エリア、9室の会議室を歩く順番で紹介します。'),
  'wework-nogizaka': ('WeWork 乃木坂｜内装・内観・雰囲気の写真｜全オフィスエリアに自然光',
    'WeWork 乃木坂（南青山1丁目）の内装・内観・雰囲気を写真で。乃木坂駅から徒歩1分、文化と自然が交わる街の拠点。ホットデスクの共用エリア、自然光の執務スペース、会議室を歩く順番で紹介します。'),
  'wework-akasaka-green-cross': ('WeWork 赤坂グリーンクロス｜内装・内観・雰囲気の写真｜ウェルビーイングと赤坂のアート',
    'WeWork 赤坂グリーンクロス（5・6階）の内装・内観・雰囲気を写真で。2025年2月開業、溜池山王駅直結。6階ラウンジとアート、5・6階のキッチン、会議室を歩く順番で紹介します。'),
  'wework-shiroyama-trust-tower': ('WeWork 城山トラストタワー｜内装・内観・雰囲気の写真｜グローバルな雰囲気と眺め',
    'WeWork 城山トラストタワー（21階）の内装・内観・雰囲気を写真で。神谷町駅から徒歩3分、外資系企業の集まる街。コミュニティバー、カフェスペース、19室の会議室を歩く順番で紹介します。'),
  'wework-kabuto-one': ('WeWork KABUTO ONE｜内装・内観・雰囲気の写真｜国際金融街・兜町の再開発ビル',
    'WeWork KABUTO ONE（9・10階）の内装・内観・雰囲気を写真で。茅場町駅直結、兜町の再開発の中心。9階の入口とコミュニティバー、窓際のラウンジ、パントリーを歩く順番で紹介します。'),
  'wework-hibiya-park-front': ('WeWork 日比谷パークフロント｜内装・内観・雰囲気の写真｜日比谷公園を望む4フロア',
    'WeWork 日比谷パークフロント（17〜20階）の内装・内観・雰囲気を写真で。霞ヶ関駅直結、日比谷公園の目の前。グリーンの多い共用エリア、公園側の区画、36室の会議室を歩く順番で紹介します。'),
  'wework-jimbocho': ('WeWork 神保町｜内装・内観・雰囲気の写真｜本の街の手描きアート',
    'WeWork 神保町（神田神保町2丁目）の内装・内観・雰囲気を写真で。神保町駅から徒歩2分、本の街から着想した手描きアートのある小さな拠点。共用エリア、個室、会議室を歩く順番で紹介します。'),
  'wework-daiwa-harumi': ('WeWork Daiwa 晴海｜内装・内観・雰囲気の写真｜晴れた日の海のような内装',
    'WeWork Daiwa 晴海（Daiwa晴海ビル2階）の内装・内観・雰囲気を写真で。晴れた日の海から着想した明るい色づかいの空間。共用エリア、7室の会議室、周辺の環境を歩く順番で紹介します。'),
  'wework-link-square-shinjuku': ('WeWork リンクスクエア新宿｜内装・内観・雰囲気の写真｜新宿御苑を望む和のラウンジ',
    'WeWork リンクスクエア新宿（リンクスクエア新宿）の内装・内観・雰囲気を写真で。新宿駅新南口から徒歩5分、4フロアの大型拠点。新宿御苑を望むラウンジ、31室の会議室を歩く順番で紹介します。'),
  'wework-nippon-tv-yotsuya': ('WeWork 日テレ四谷ビル｜内装・内観・雰囲気の写真｜日本庭園を意識した空間',
    'WeWork 日テレ四谷ビル（麹町5丁目）の内装・内観・雰囲気を写真で。ビル一棟を WeWork が借りた拠点。日本庭園を意識した共用エリア、テラス、14室の会議室を歩く順番で紹介します。'),
}
PLACE_ADD = {
  'wework-the-argyle-aoyama': {'streetAddress': '東京都港区北青山2-14-4 the ARGYLE aoyama 6F', 'addressLocality': '北青山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-nogizaka': {'streetAddress': '東京都港区南青山1-24-3 1F', 'addressLocality': '南青山', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-akasaka-green-cross': {'streetAddress': '東京都港区赤坂2-4-6 赤坂グリーンクロス 6F', 'addressLocality': '赤坂', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-shiroyama-trust-tower': {'streetAddress': '東京都港区虎ノ門4-3-1 城山トラストタワー 21F', 'addressLocality': '虎ノ門', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-kabuto-one': {'streetAddress': '東京都中央区日本橋兜町7-1 KABUTO ONE', 'addressLocality': '日本橋兜町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-hibiya-park-front': {'streetAddress': '東京都千代田区内幸町2-1-6 日比谷パークフロント 19F', 'addressLocality': '内幸町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-jimbocho': {'streetAddress': '東京都千代田区神田神保町2-11-15 2F', 'addressLocality': '神田神保町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-daiwa-harumi': {'streetAddress': '東京都中央区晴海3-10-1 Daiwa晴海ビル 2F', 'addressLocality': '晴海', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-link-square-shinjuku': {'streetAddress': '東京都渋谷区千駄ヶ谷5-27-5 リンクスクエア新宿 16F', 'addressLocality': '千駄ヶ谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-nippon-tv-yotsuya': {'streetAddress': '東京都千代田区麹町5-3-23 日テレ四谷ビル 1F', 'addressLocality': '麹町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# ==== 2026-09-28 cowork_add_2026-09-28_e.py の SEO／場所 ====
SEO_ADD = {
  'the-hub-shiodome': ('THE HUB 汐留｜内装・内観・雰囲気の写真｜イタリア街の1棟オフィス',
    'THE HUB 汐留（東新橋・昭和アステック1号館）の内装・内観・雰囲気を写真で。汐留「イタリア街」の7階建てを1棟で使う拠点。ラウンジ、会議室、応接室、ブース席を歩く順番で紹介します。'),
  'the-hub-shimbashi-west': ('THE HUB 新橋WEST｜内装・内観・雰囲気の写真｜内幸町3分の機能的なオフィス',
    'THE HUB 新橋WEST（プロス西新橋ビル6・7階）の内装・内観・雰囲気を写真で。内幸町駅3分、虎ノ門・新橋も徒歩圏。ラウンジ、共有スペース、会議室、個室、ブース席を歩く順番で紹介します。'),
  'the-hub-tamachi': ('THE HUB 田町｜内装・内観・雰囲気の写真｜テラスと応接室のある共用部',
    'THE HUB 田町（シャーメゾンステージ田町3〜7階）の内装・内観・雰囲気を写真で。三田駅1分、田町駅3分。ラウンジ、テラス、5名用の会議室、応接室、2〜13名用の個室を歩く順番で紹介します。'),
  'the-hub-tamachi-mita': ('THE HUB 田町三田｜内装・内観・雰囲気の写真｜1〜14名用の個室がそろうRIPL9',
    'THE HUB 田町三田（三田・RIPL9の1〜7階）の内装・内観・雰囲気を写真で。「都心の機動力と落ち着きが同居するビジネス拠点」。共有スペース、ラウンジ、会議室、ブース席、個室を紹介します。'),
  'the-hub-takanawa': ('THE HUB 高輪｜内装・内観・雰囲気の写真｜泉岳寺4分、進化と落ち着きの拠点',
    'THE HUB 高輪（グレイス高輪ビル8・9階）の内装・内観・雰囲気を写真で。泉岳寺駅4分、高輪ゲートウェイ駅6分。ウェイティングスペース、会議室、個室型と半個室型のブース席、個室を紹介します。'),
  'the-base-hamamatsucho': ('THE BASE 浜松町｜内装・内観・雰囲気の写真｜20〜25名用のセットアップオフィス',
    'THE BASE 浜松町（港ビル4階）の内装・内観・雰囲気を写真で。浜松町駅3分、内装完備で敷金・礼金ゼロのワンフロア。オフィススペース、会議室、ブース、ウェイティングスペースを紹介します。'),
  'the-executive-centre-kyobashi-edogrand': ('The Executive Centre 京橋エドグラン｜内装・内観・雰囲気の写真｜京橋駅直結の26階',
    'The Executive Centre 京橋エドグラン（26階）の内装・内観・雰囲気を写真で。京橋駅と地下直結、東京駅を見下ろす眺め。石のカウンターのバリスタバー、ラウンジ、個室、4室の会議室を紹介します。'),
  'the-executive-centre-grantokyo-south-tower': ('The Executive Centre グラントウキョウサウスタワー｜内装・内観・雰囲気の写真｜東京駅1分の7階',
    'The Executive Centre グラントウキョウサウスタワー（7階）の内装・内観・雰囲気を写真で。東京駅八重洲南口の上、駅から1分。受付、メンバーズラウンジ、パントリー、個室、会議室を紹介します。'),
  'the-executive-centre-tofrom-yaesu-tower': ('The Executive Centre TOFROM YAESU TOWER｜内装・内観・雰囲気の写真｜和の意匠の220席',
    'The Executive Centre TOFROM YAESU TOWER（11階）の内装・内観・雰囲気を写真で。東京駅と地下直結。和紙の照明、松の木、瓦に着想を得たバリスタバー、ラウンジ、個室、会議室を紹介します。'),
  'the-executive-centre-world-trade-center-south-tower': ('The Executive Centre 世界貿易センタービルディング南館｜内装・内観・雰囲気の写真｜東京湾を望む17階',
    'The Executive Centre 世界貿易センタービルディング南館（17階）の内装・内観・雰囲気を写真で。浜松町駅直結、東京湾を望む窓。黒い大理石のバリスタバー、コワーキング、個室、会議室を紹介します。'),
}
PLACE_ADD = {
  'the-hub-shiodome': {'streetAddress': '東京都港区東新橋2-7-3 昭和アステック1号館', 'addressLocality': '汐留', 'addressRegion': '東京都'},
  'the-hub-shimbashi-west': {'streetAddress': '東京都港区西新橋2-4-3 プロス西新橋ビル6-7F', 'addressLocality': '新橋', 'addressRegion': '東京都'},
  'the-hub-tamachi': {'streetAddress': '東京都港区芝5-32-12 シャーメゾンステージ田町3-7F', 'addressLocality': '田町', 'addressRegion': '東京都'},
  'the-hub-tamachi-mita': {'streetAddress': '東京都港区三田3-4-3 RIPL9（リップルナイン）1-7F', 'addressLocality': '三田', 'addressRegion': '東京都'},
  'the-hub-takanawa': {'streetAddress': '東京都港区高輪2-14-17 グレイス高輪ビル8-9F', 'addressLocality': '高輪', 'addressRegion': '東京都'},
  'the-base-hamamatsucho': {'streetAddress': '東京都港区浜松町1-21-4 港ビル4F', 'addressLocality': '浜松町', 'addressRegion': '東京都'},
  'the-executive-centre-kyobashi-edogrand': {'streetAddress': '東京都中央区京橋2-2-1 京橋エドグラン26階', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-grantokyo-south-tower': {'streetAddress': '東京都千代田区丸の内1-9-2 グラントウキョウサウスタワー7階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-tofrom-yaesu-tower': {'streetAddress': '東京都中央区八重洲1-6-1 TOFROM YAESU TOWER 11階', 'addressLocality': '八重洲', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'the-executive-centre-world-trade-center-south-tower': {'streetAddress': '東京都港区浜松町2-4-1 世界貿易センタービルディング南館17階', 'addressLocality': '浜松町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# ==== 2026-09-28 cowork_add_2026-09-28_f.py の SEO／場所 ====
SEO_ADD = {
  'the-collective-grantokyo-south-tower': ('ザ・コレクティブ グラントウキョウサウスタワー｜内装・内観・雰囲気の写真｜東京駅直結のラグジュアリーコワーキング',
    'ザ・コレクティブ グラントウキョウサウスタワー（9階）の内装・内観・雰囲気を写真で。JustCo 最上位ブランド。アーロンチェアの共用デスク、パントリー、会議室、個室を歩く順番で紹介します。'),
  'newwork-shibuya-goto-ikueikai-building': ('NewWork 渋谷五島育英会ビル The Flagship｜内装・内観・雰囲気の写真｜93席の旗艦店',
    'NewWork 渋谷五島育英会ビル The Flagship（7階）の内装・内観・雰囲気を写真で。東急の法人会員制サテライトオフィス。93席、プレミアム会議室、個室ブース、マッサージチェアを紹介します。'),
  'newwork-ginza': ('NewWork 銀座｜内装・内観・雰囲気の写真｜銀座と新橋のあいだの2階',
    'NewWork 銀座（K-18ビル2階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。新橋駅5分、40席と6名用の会議室、個室ブースを歩く順番で紹介します。'),
  'newwork-ebisu': ('NewWork 恵比寿｜内装・内観・雰囲気の写真｜西口3分の39席',
    'NewWork 恵比寿（恵比寿STビル3階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。39席と6名・4名用の会議室、個室ブースを歩く順番で紹介します。'),
  'newwork-akihabara': ('NewWork 秋葉原｜内装・内観・雰囲気の写真｜駅1分・土日祝も開く10階',
    'NewWork 秋葉原（新秋葉原ビル10階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。土日祝日も営業、31席と会議室、9室の個室ブースを紹介します。'),
  'newwork-ikebukuro-higashiguchi': ('NewWork 池袋東口｜内装・内観・雰囲気の写真｜個室ブース15室の9階',
    'NewWork 池袋東口（菊邑91ビル9階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。土日祝日も営業、40席、15室の個室ブース、会議室を紹介します。'),
  'newwork-daimon-hamamatsucho': ('NewWork 大門・浜松町｜内装・内観・雰囲気の写真｜大門駅1分の4階',
    'NewWork 大門・浜松町（RBM浜松町ビル4階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。大門駅1分、36席と会議室、個室ブースを歩く順番で紹介します。'),
  'newwork-ueno': ('NewWork 上野｜内装・内観・雰囲気の写真｜上野駅3分の37席',
    'NewWork 上野（VORT上野2階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。上野駅3分、37席と6名・4名用の会議室、個室ブースを歩く順番で紹介します。'),
  'newwork-oimachi': ('NewWork 大井町｜内装・内観・雰囲気の写真｜個室ブース11室の5階',
    'NewWork 大井町（K-3ビル5階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。土日祝日も営業、27席、11室の個室ブース、8名用の会議室を紹介します。'),
  'newwork-kinshicho-2nd': ('NewWork 錦糸町2nd｜内装・内観・雰囲気の写真｜南口2分・土日祝も開く2階',
    'NewWork 錦糸町2nd（錦糸町スクエアビル2階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。土日祝日も営業、27席と会議室、個室ブースを紹介します。'),
}
PLACE_ADD = {
  'the-collective-grantokyo-south-tower': {'streetAddress': '東京都千代田区丸の内1-9-2 グラントウキョウサウスタワー9階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'newwork-shibuya-goto-ikueikai-building': {'streetAddress': '東京都渋谷区道玄坂1-10-7 五島育英会ビル7F', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-ginza': {'streetAddress': '東京都中央区銀座8-9-13 K-18ビル2F', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-ebisu': {'streetAddress': '東京都渋谷区東3-24-2 恵比寿STビル3F', 'addressLocality': '恵比寿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-akihabara': {'streetAddress': '東京都千代田区外神田1-18-19 新秋葉原ビル10F', 'addressLocality': '秋葉原', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-21:00'},
  'newwork-ikebukuro-higashiguchi': {'streetAddress': '東京都豊島区東池袋1-41-6 菊邑91ビル9F', 'addressLocality': '池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-21:00'},
  'newwork-daimon-hamamatsucho': {'streetAddress': '東京都港区浜松町1-27-12 RBM浜松町ビル4F', 'addressLocality': '浜松町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'newwork-ueno': {'streetAddress': '東京都台東区上野7-4-7 VORT上野2F', 'addressLocality': '上野', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'newwork-oimachi': {'streetAddress': '東京都品川区大井1-14-3 K-3ビル5F', 'addressLocality': '大井町', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-21:00'},
  'newwork-kinshicho-2nd': {'streetAddress': '東京都墨田区江東橋3-10-8 錦糸町スクエアビル2F', 'addressLocality': '錦糸町', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 08:00-20:00'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)


SEO_ADD = {
  'h1t-machida': ('H¹T町田（町田）｜内装・内観・雰囲気の写真｜町田モディの6階、ブースと個室で一人の仕事に集中できる拠点',
    'H¹T町田（町田）の内装・内観・雰囲気を写真で。町田モディ6階、一人用のブースと個室がそろうシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-ichigaya': ('H¹T市ヶ谷（市ヶ谷）｜内装・内観・雰囲気の写真｜4路線の市ヶ谷駅から徒歩1分、会議室が3室ある拠点',
    'H¹T市ヶ谷（市ヶ谷）の内装・内観・雰囲気を写真で。4路線が乗り入れる市ヶ谷駅から徒歩1分、会議室3室のシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-tachikawa': ('H¹T立川（立川）｜内装・内観・雰囲気の写真｜立川駅南口から徒歩2分、席の種類が多い多摩の拠点',
    'H¹T立川（立川）の内装・内観・雰囲気を写真で。立川駅南口から徒歩2分、席の種類がそろう多摩エリアのシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-iidabashi': ('H¹T飯田橋（飯田橋）｜内装・内観・雰囲気の写真｜ビルの16階、緑の大きなテーブルがある飯田橋の拠点',
    'H¹T飯田橋（飯田橋）の内装・内観・雰囲気を写真で。ステージビルディング16階、緑を置いた大テーブルのシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-kojimachi': ('H¹T麹町（麹町）｜内装・内観・雰囲気の写真｜麹町駅から徒歩1分、6名の会議室が3室ある拠点',
    'H¹T麹町（麹町）の内装・内観・雰囲気を写真で。麹町駅から徒歩1分、会議室が4室あるシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-kunitachi': ('H¹T国立（国立）｜内装・内観・雰囲気の写真｜国立駅南口から徒歩2分、一人用の個室が17室ある拠点',
    'H¹T国立（国立）の内装・内観・雰囲気を写真で。国立駅南口から徒歩2分、一人用の個室17室のシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-kyodo': ('H¹T経堂（経堂）｜内装・内観・雰囲気の写真｜経堂駅北口から徒歩2分、個室だけの静かな拠点',
    'H¹T経堂（経堂）の内装・内観・雰囲気を写真で。経堂駅北口から徒歩2分、一人用の個室だけのシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-musashikoganei': ('H¹T武蔵小金井（武蔵小金井）｜内装・内観・雰囲気の写真｜武蔵小金井駅から徒歩3分、個室18室の大きな拠点',
    'H¹T武蔵小金井（武蔵小金井）の内装・内観・雰囲気を写真で。武蔵小金井駅から徒歩3分、一人用の個室18室のシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-chitosefunabashi': ('H¹T千歳船橋（千歳船橋）｜内装・内観・雰囲気の写真｜千歳船橋駅から徒歩3分、朝7時から夜22時まで開く拠点',
    'H¹T千歳船橋（千歳船橋）の内装・内観・雰囲気を写真で。千歳船橋駅南口から徒歩3分、朝7時から夜22時まで使えるシェアオフィスを、席の種類から順番に紹介します。'),
  'h1t-tsukiji': ('H¹T築地（築地）｜内装・内観・雰囲気の写真｜築地駅4番出口から徒歩30秒、個室だけの拠点',
    'H¹T築地（築地）の内装・内観・雰囲気を写真で。築地駅から徒歩30秒、一人用の個室10室のシェアオフィスを、席の種類から順番に紹介します。'),
}
PLACE_ADD = {
  'h1t-machida': {'streetAddress': '東京都町田市原町田6-2-6 町田モディ6階', 'addressLocality': '町田', 'addressRegion': '東京都'},
  'h1t-ichigaya': {'streetAddress': '東京都千代田区五番町1-9 MG市ヶ谷ビルディング3階', 'addressLocality': '市ヶ谷', 'addressRegion': '東京都'},
  'h1t-tachikawa': {'streetAddress': '東京都立川市柴崎町3-6-29 アレアレア2 6階', 'addressLocality': '立川', 'addressRegion': '東京都'},
  'h1t-iidabashi': {'streetAddress': '東京都千代田区富士見2-7-2 ステージビルディング16階', 'addressLocality': '飯田橋', 'addressRegion': '東京都'},
  'h1t-kojimachi': {'streetAddress': '東京都千代田区麹町4-2-1 MK麹町ビル3階', 'addressLocality': '麹町', 'addressRegion': '東京都'},
  'h1t-kunitachi': {'streetAddress': '東京都国立市東1-4-8 国立セントラルビル2階', 'addressLocality': '国立', 'addressRegion': '東京都'},
  'h1t-kyodo': {'streetAddress': '東京都世田谷区宮坂3-10-9 経堂フコク生命ビル4階', 'addressLocality': '経堂', 'addressRegion': '東京都'},
  'h1t-musashikoganei': {'streetAddress': '東京都小金井市本町6-2-30 ソコラ武蔵小金井クロス2階', 'addressLocality': '小金井', 'addressRegion': '東京都'},
  'h1t-chitosefunabashi': {'streetAddress': '東京都世田谷区桜丘2-27-16 TOMビル2階', 'addressLocality': '千歳船橋', 'addressRegion': '東京都'},
  'h1t-tsukiji': {'streetAddress': '東京都中央区築地2-10-4 エミタ銀座イーストビル', 'addressLocality': '築地', 'addressRegion': '東京都'},
}
SEO.update(SEO_ADD); PLACE.update(PLACE_ADD)

# ---- 2026-10-01 追加（9/28の8施設と10/1の10施設） ----
SEO_ADD_1001 = {
  'ws-ueno': ('WORKSTYLING（ワークスタイリング）上野｜内装・内観・雰囲気の写真｜JR上野駅から徒歩1分、予約なしで座れるオープンスペース',
    'ワークスタイリング 上野（東京都台東区上野7-7-6 TT上野駅前ビル2階）の内装・内観・雰囲気を写真で。JR上野駅から1分、予約なしで座れる。入口から順に、歩く順番で紹介します。'),
  'ws-ikebukuro-nishiguchi': ('WORKSTYLING（ワークスタイリング）池袋西口｜内装・内観・雰囲気の写真｜池袋駅から徒歩1分、東武アネックスビル5階のシェアオフィス',
    'ワークスタイリング 池袋西口（東京都豊島区西池袋1-10-10 東武アネックスビル5階）の内装・内観・雰囲気を写真で。池袋駅から1分、5階のシェアオフィス。入口から順に、歩く順番で紹介します。'),
  'ws-yotsuya': ('WORKSTYLING（ワークスタイリング）四谷｜内装・内観・雰囲気の写真｜麹町駅と四ツ谷駅の両方から4分、第7秋山ビルディング6階',
    'ワークスタイリング 四谷（東京都千代田区麹町5-3-6 第7秋山ビルディング6階）の内装・内観・雰囲気を写真で。麹町と四ツ谷、二つの駅から4分。入口から順に、歩く順番で紹介します。'),
  'ws-gotanda': ('WORKSTYLING（ワークスタイリング）五反田｜内装・内観・雰囲気の写真｜五反田駅から徒歩1分、A-PLACE五反田駅前ビル5階',
    'ワークスタイリング 五反田（東京都品川区西五反田1-5-1 A-PLACE五反田駅前ビル5階）の内装・内観・雰囲気を写真で。五反田駅から1分、駅前ビルの5階。入口から順に、歩く順番で紹介します。'),
  'h1t-toranomon': ('H¹T（エイチワンティー）虎ノ門｜内装・内観・雰囲気の写真｜虎ノ門駅10番出口に直結、1名用ルーム27室とボックス5席',
    'H¹T虎ノ門（東京都港区虎ノ門1-1-20 虎ノ門実業会館本館9階）の内装・内観・雰囲気を写真で。虎ノ門駅10番出口直結、ルーム27室。入口から順に、歩く順番で紹介します。'),
  'h1t-ginza': ('H¹T（エイチワンティー）銀座｜内装・内観・雰囲気の写真｜銀座駅A7出口から徒歩1分、土日祝も朝7時から夜10時まで',
    'H¹T銀座（東京都中央区銀座4-6-11 銀座センタービル4階）の内装・内観・雰囲気を写真で。銀座駅A7出口から1分、朝7時から。入口から順に、歩く順番で紹介します。'),
  'h1t-otemachi': ('H¹T（エイチワンティー）大手町｜内装・内観・雰囲気の写真｜大手町駅から徒歩1分、20階と21階にルーム45室とオープンスペース',
    'H¹T大手町（東京都千代田区大手町2-1-1 大成大手町ビル 20階・21階）の内装・内観・雰囲気を写真で。大手町駅から1分、20階と21階の2フロア。入口から順に、歩く順番で紹介します。'),
  'h1t-ueno': ('H¹T（エイチワンティー）上野｜内装・内観・雰囲気の写真｜上野マルイ3階、ビーズソファに座って靴を脱いで使う席がある',
    'H¹T上野（東京都台東区上野6-15-1 上野マルイ3階）の内装・内観・雰囲気を写真で。上野マルイ3階、靴を脱ぐ席がある。入口から順に、歩く順番で紹介します。'),
  'ws-kanda': ('WORKSTYLING（ワークスタイリング）神田｜内装・内観・雰囲気の写真｜神田駅から徒歩1分、13名から80名までの会議室もそろう',
    'ワークスタイリング 神田（東京都千代田区鍛冶町2-6-2 上野ビルディング6階）の内装・内観・雰囲気を写真で。神田駅から1分、13名以上の会議室まで。入口から順に、歩く順番で紹介します。'),
  'ws-akihabara': ('WORKSTYLING（ワークスタイリング）秋葉原中央｜内装・内観・雰囲気の写真｜秋葉原駅中央改札口から徒歩1分、大人数の会議室もある拠点',
    'ワークスタイリング 秋葉原中央（東京都千代田区神田相生町1 秋葉原フコク生命ビル3階）の内装・内観・雰囲気を写真で。秋葉原駅の中央改札から1分。入口から順に、歩く順番で紹介します。'),
  'ws-jimbocho': ('WORKSTYLING（ワークスタイリング）神保町｜内装・内観・雰囲気の写真｜神保町駅から徒歩1分、登記もできる神保町三井ビルディング3階',
    'ワークスタイリング 神保町（東京都千代田区神田神保町1-105 神保町三井ビルディング3階）の内装・内観・雰囲気を写真で。本の街の駅から1分、登記もできる。入口から順に、歩く順番で紹介します。'),
  'ws-toyosu': ('WORKSTYLING（ワークスタイリング）豊洲｜内装・内観・雰囲気の写真｜豊洲駅から徒歩2分、登記もできる豊洲センタービル3階',
    'ワークスタイリング 豊洲（東京都江東区豊洲3-3-3 豊洲センタービル3階）の内装・内観・雰囲気を写真で。豊洲駅から2分、湾岸の登記できる拠点。入口から順に、歩く順番で紹介します。'),
  'ws-kichijoji': ('WORKSTYLING（ワークスタイリング）吉祥寺｜内装・内観・雰囲気の写真｜吉祥寺駅から徒歩1分、住む街の駅前にあるシェアオフィス',
    'ワークスタイリング 吉祥寺（東京都武蔵野市吉祥寺南町1-6-1 吉祥寺スバルビル4階）の内装・内観・雰囲気を写真で。住む街の駅前で、通勤せずに働く。入口から順に、歩く順番で紹介します。'),
  'ws-machida': ('WORKSTYLING（ワークスタイリング）町田｜内装・内観・雰囲気の写真｜町田駅から徒歩3分、JRと小田急の両方から歩ける町映ビル7階',
    'ワークスタイリング 町田（東京都町田市原町田6-3-3 町映ビル7階）の内装・内観・雰囲気を写真で。JRと小田急の町田駅から3分。入口から順に、歩く順番で紹介します。'),
  'ws-musashikosugi': ('WORKSTYLING（ワークスタイリング）ららテラス武蔵小杉店｜内装・内観・雰囲気の写真｜武蔵小杉駅から徒歩1分、商業施設の4階にある登記できる拠点',
    'ワークスタイリング ららテラス武蔵小杉店（神奈川県川崎市中原区新丸子東3-1302 ららテラス武蔵小杉4階）の内装・内観・雰囲気を写真で。駅前の商業施設の中、登記もできる。入口から順に、歩く順番で紹介します。'),
  'ws-shinyokohama': ('WORKSTYLING（ワークスタイリング）新横浜｜内装・内観・雰囲気の写真｜新横浜駅から徒歩3分、新幹線の駅の近くにあるSD18ビル8階',
    'ワークスタイリング 新横浜（神奈川県横浜市港北区新横浜3-7-18 SD18ビル8階）の内装・内観・雰囲気を写真で。新幹線の駅から3分、出張の合間に。入口から順に、歩く順番で紹介します。'),
  'ws-umeda': ('WORKSTYLING（ワークスタイリング）梅田｜内装・内観・雰囲気の写真｜阪急梅田駅から徒歩1分、阪急ターミナルビル10階のシェアオフィス',
    'ワークスタイリング 梅田（大阪府大阪市北区芝田1-1-4 阪急ターミナルビル10階）の内装・内観・雰囲気を写真で。阪急梅田駅の改札から1分、ビルの10階。入口から順に、歩く順番で紹介します。'),
  'ws-kyoto-ekimae': ('WORKSTYLING（ワークスタイリング）京都駅前｜内装・内観・雰囲気の写真｜京都駅から徒歩2分、日本生命京都ヤサカビル5階のシェアオフィス',
    'ワークスタイリング 京都駅前（京都府京都市下京区塩小路通西洞院東入東塩小路町843-2 日本生命京都ヤサカビル5階）の内装・内観・雰囲気を写真で。京都駅から2分、新幹線の前後に。入口から順に、歩く順番で紹介します。'),
}
PLACE_ADD_1001 = {
  'ws-ueno': {'streetAddress': '東京都台東区上野7-7-6 TT上野駅前ビル2階', 'addressLocality': '上野', 'addressRegion': '東京都'},
  'ws-ikebukuro-nishiguchi': {'streetAddress': '東京都豊島区西池袋1-10-10 東武アネックスビル5階', 'addressLocality': '池袋', 'addressRegion': '東京都'},
  'ws-yotsuya': {'streetAddress': '東京都千代田区麹町5-3-6 第7秋山ビルディング6階', 'addressLocality': '四谷', 'addressRegion': '東京都'},
  'ws-gotanda': {'streetAddress': '東京都品川区西五反田1-5-1 A-PLACE五反田駅前ビル5階', 'addressLocality': '五反田', 'addressRegion': '東京都'},
  'h1t-toranomon': {'streetAddress': '東京都港区虎ノ門1-1-20 虎ノ門実業会館本館9階', 'addressLocality': '虎ノ門', 'addressRegion': '東京都'},
  'h1t-ginza': {'streetAddress': '東京都中央区銀座4-6-11 銀座センタービル4階', 'addressLocality': '銀座', 'addressRegion': '東京都'},
  'h1t-otemachi': {'streetAddress': '東京都千代田区大手町2-1-1 大成大手町ビル 20階・21階', 'addressLocality': '大手町', 'addressRegion': '東京都'},
  'h1t-ueno': {'streetAddress': '東京都台東区上野6-15-1 上野マルイ3階', 'addressLocality': '上野', 'addressRegion': '東京都'},
  'ws-kanda': {'streetAddress': '東京都千代田区鍛冶町2-6-2 上野ビルディング6階', 'addressLocality': '神田', 'addressRegion': '東京都'},
  'ws-akihabara': {'streetAddress': '東京都千代田区神田相生町1 秋葉原フコク生命ビル3階', 'addressLocality': '秋葉原', 'addressRegion': '東京都'},
  'ws-jimbocho': {'streetAddress': '東京都千代田区神田神保町1-105 神保町三井ビルディング3階', 'addressLocality': '神保町', 'addressRegion': '東京都'},
  'ws-toyosu': {'streetAddress': '東京都江東区豊洲3-3-3 豊洲センタービル3階', 'addressLocality': '豊洲', 'addressRegion': '東京都'},
  'ws-kichijoji': {'streetAddress': '東京都武蔵野市吉祥寺南町1-6-1 吉祥寺スバルビル4階', 'addressLocality': '吉祥寺', 'addressRegion': '東京都'},
  'ws-machida': {'streetAddress': '東京都町田市原町田6-3-3 町映ビル7階', 'addressLocality': '町田', 'addressRegion': '東京都'},
  'ws-musashikosugi': {'streetAddress': '神奈川県川崎市中原区新丸子東3-1302 ららテラス武蔵小杉4階', 'addressLocality': '武蔵小杉', 'addressRegion': '神奈川県'},
  'ws-shinyokohama': {'streetAddress': '神奈川県横浜市港北区新横浜3-7-18 SD18ビル8階', 'addressLocality': '新横浜', 'addressRegion': '神奈川県'},
  'ws-umeda': {'streetAddress': '大阪府大阪市北区芝田1-1-4 阪急ターミナルビル10階', 'addressLocality': '梅田', 'addressRegion': '大阪府'},
  'ws-kyoto-ekimae': {'streetAddress': '京都府京都市下京区塩小路通西洞院東入東塩小路町843-2 日本生命京都ヤサカビル5階', 'addressLocality': '京都', 'addressRegion': '京都府'},
}
SEO.update(SEO_ADD_1001); PLACE.update(PLACE_ADD_1001)


# ---- 2026-10-01 統合 cowork_add_2026-09-30_a〜f.py の SEO と住所 ----

SEO_ADD_0930A = {
  'wework-hanzomon-prex-north': ('WeWork 半蔵門 PREX North（ウィーワーク ハンゾウモン プレックスノース）｜内装・内観・雰囲気の写真｜「門」から着想したメタルと木',
    'WeWork 半蔵門 PREX North（麹町2丁目）の内装・内観・雰囲気を写真で。半蔵門駅から徒歩1分、メタルと木を組み合わせた空間と屋上庭園。共用エリア、会議室、1フロア専有区画を紹介します。'),
  'wework-kojimachi': ('WeWork 麹町（ウィーワーク コウジマチ）｜内装・内観・雰囲気の写真｜7フロアの明るい色づかい',
    'WeWork 麹町（番町麹町ビルディング）の内装・内観・雰囲気を写真で。2駅5路線が使える街の中心、ビルの3〜9階の7フロアを占める拠点。明るい色の共用エリアと会議室を紹介します。'),
  'wework-shinagawa': ('WeWork 品川（ウィーワーク シナガワ）｜内装・内観・雰囲気の写真｜品川駅徒歩1分の東京の玄関口',
    'WeWork 品川（京急第1ビル13階）の内装・内観・雰囲気を写真で。品川駅から徒歩1分、新幹線や羽田空港に近い拠点。広く開放的なラウンジ、11室の会議室、電話ブースを紹介します。'),
  'wework-tokyo-portcity-takeshiba': ('WeWork 東京ポートシティ竹芝（ウィーワーク トウキョウポートシティタケシバ）｜内装・内観・雰囲気の写真｜「NY×和風」の空間',
    'WeWork 東京ポートシティ竹芝（10階）の内装・内観・雰囲気を写真で。浜松町駅から歩行者デッキ直結、竹芝スマートシティの中心。「NY×和風」の共用エリアと14室の会議室を紹介します。'),
  'wework-kdx-toranomon-1chome': ('WeWork KDX 虎ノ門１丁目（ウィーワーク ケーディーエックス トラノモンイッチョウメ）｜内装・内観・雰囲気の写真｜屋外テラスとつながるラウンジ',
    'WeWork KDX 虎ノ門１丁目（11階）の内装・内観・雰囲気を写真で。虎ノ門駅から徒歩3分、ラウンジと屋外テラスがひと続きの拠点。24室の会議室、1フロア専有区画を紹介します。'),
  'wework-nippon-life-nihonbashi': ('WeWork 日本生命日本橋ビル（ウィーワーク ニホンセイメイニホンバシビル）｜内装・内観・雰囲気の写真｜「日本橋」を映したデザイン',
    'WeWork 日本生命日本橋ビル（4階）の内装・内観・雰囲気を写真で。日本橋駅から徒歩5分、「日本橋」をデザインに取り入れた空間。共用エリア、プライベートオフィス、免震構造のビルを紹介します。'),
  'wework-metropolitan-plaza-building': ('WeWork メトロポリタンプラザビル（ウィーワーク メトロポリタンプラザビル）｜内装・内観・雰囲気の写真｜池袋駅直結の小さな拠点',
    'WeWork メトロポリタンプラザビル（14階）の内装・内観・雰囲気を写真で。池袋駅直結、8路線が使えるビルの中の小規模拠点。広々とした共用エリアと8室の会議室、ビルの外観を紹介します。'),
}
PLACE_ADD_0930A = {
  'wework-hanzomon-prex-north': {'streetAddress': '東京都千代田区麹町2-3-2 半蔵門PREX North 2F', 'addressLocality': '麹町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-kojimachi': {'streetAddress': '東京都千代田区麹町6-6-2 番町麹町ビルディング 5F', 'addressLocality': '麹町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-shinagawa': {'streetAddress': '東京都港区高輪4-10-18 京急第1ビル 13F', 'addressLocality': '高輪', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-tokyo-portcity-takeshiba': {'streetAddress': '東京都港区海岸1-7-1 東京ポートシティ竹芝 10F', 'addressLocality': '海岸', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-kdx-toranomon-1chome': {'streetAddress': '東京都港区虎ノ門1-10-5 KDX虎ノ門一丁目ビル 11F', 'addressLocality': '虎ノ門', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
  'wework-nippon-life-nihonbashi': {'streetAddress': '東京都中央区日本橋2-13-12 日本生命日本橋ビル 4F', 'addressLocality': '日本橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-18:00'},
  'wework-metropolitan-plaza-building': {'streetAddress': '東京都豊島区西池袋1-11-1 メトロポリタンプラザビル 14F', 'addressLocality': '西池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:30-18:00'},
}

SEO.update(SEO_ADD_0930A); PLACE.update(PLACE_ADD_0930A)

SEO_ADD_0930B = {
  'the-base-shimbashi': ('THE BASE 新橋（ザ ベース シンバシ）｜内装・内観・雰囲気の写真｜新橋3分の内装完備オフィス',
    'THE BASE 新橋（新橋フォディアビル3階・8階）の内装・内観・雰囲気を写真で。新橋駅烏森口3分、敷礼ゼロのセットアップオフィス。3階と8階の区画、ウェイティングスペースを紹介します。'),
  'the-base-tamachi': ('THE BASE 田町（ザ ベース タマチ）｜内装・内観・雰囲気の写真｜芝浦運河沿いの6階',
    'THE BASE 田町（内村芝浦ビル6階）の内装・内観・雰囲気を写真で。田町駅芝浦口4分、2023年リノベーションのビルにある内装完備のオフィス。6Cと6Dの区画、会議室、ブース席を紹介します。'),
  'the-base-tamachi-mita': ('THE BASE 田町三田（ザ ベース タマチミタ）｜内装・内観・雰囲気の写真｜RIPL9の8階の自社オフィス',
    'THE BASE 田町三田（RIPL9の8階）の内装・内観・雰囲気を写真で。三田駅5分、少人数の会社の自社オフィスやセカンドオフィスに向く内装完備の部屋と、8階からの眺めを紹介します。'),
  'newwork-ikebukuro-7f': ('NewWork 池袋7F（ニューワーク イケブクロ ナナエフ）｜内装・内観・雰囲気の写真｜東口4分の31席',
    'NewWork 池袋7F（オーク池袋ビルディング7階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。31席と4名用の会議室、個室ブースを歩く順番で紹介します。'),
  'newwork-ikebukuro-4f': ('NewWork 池袋4F（ニューワーク イケブクロ ヨンエフ）｜内装・内観・雰囲気の写真｜会議室2室と個室ブース7室',
    'NewWork 池袋4F（オーク池袋ビルディング4階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。24のブース席、8名・6名用の会議室、個室ブースを紹介します。'),
  'newwork-omori': ('NewWork 大森（ニューワーク オオモリ）｜内装・内観・雰囲気の写真｜駅3分・個室ブース11室',
    'NewWork 大森（いちご大森ビル6階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。大森駅3分、30のブース席と11室の個室ブース、8名用の会議室を紹介します。'),
  'newwork-aoto': ('NewWork 青砥（ニューワーク アオト）｜内装・内観・雰囲気の写真｜13席の小さな拠点',
    'NewWork 青砥（朝日生命葛飾ビル4階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。青砥駅5分、13席と6名用の会議室、3室の個室ブースを紹介します。'),
  'h1t-shibuya-miyamasuzaka': ('H¹T渋谷宮益坂（エイチワンティー シブヤミヤマスザカ）｜内装・内観・雰囲気の写真｜個室14室と会議室5室',
    'H¹T渋谷宮益坂（ワコー宮益坂8階）の内装・内観・雰囲気を写真で。渋谷駅3分、土曜・祝日も開く野村不動産の法人向けシェアオフィス。オープンスペース、個室14室、会議室5室を紹介します。'),
  'h1t-akasaka-mitsuke': ('H¹T赤坂見附（エイチワンティー アカサカミツケ）｜内装・内観・雰囲気の写真｜駅1分、日曜・祝日も営業',
    'H¹T赤坂見附（No.R赤坂見附7階）の内装・内観・雰囲気を写真で。赤坂見附駅10番出口1分、日曜・祝日も開く法人向けシェアオフィス。オープンスペース、ボックス、個室、会議室を紹介します。'),
  'h1t-toranomon': ('H¹T虎ノ門（エイチワンティー トラノモン）｜内装・内観・雰囲気の写真｜駅直結・個室27室',
    'H¹T虎ノ門（虎ノ門実業会館本館9階）の内装・内観・雰囲気を写真で。虎ノ門駅10番出口直結、平日は22時半まで開く法人向けシェアオフィス。ボックス、個室27室、会議室4室を紹介します。'),
}
PLACE_ADD_0930B = {
  'the-base-shimbashi': {'streetAddress': '東京都港区新橋3-7-3 新橋フォディアビル', 'addressLocality': '新橋', 'addressRegion': '東京都'},
  'the-base-tamachi': {'streetAddress': '東京都港区芝浦3-19-18 内村芝浦ビル6F', 'addressLocality': '田町', 'addressRegion': '東京都'},
  'the-base-tamachi-mita': {'streetAddress': '東京都港区三田3-4-3 RIPL9（リップルナイン）8F', 'addressLocality': '三田', 'addressRegion': '東京都'},
  'newwork-ikebukuro-7f': {'streetAddress': '東京都豊島区東池袋1-21-11 オーク池袋ビルディング7F', 'addressLocality': '池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-ikebukuro-4f': {'streetAddress': '東京都豊島区東池袋1-21-11 オーク池袋ビルディング4F', 'addressLocality': '池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-omori': {'streetAddress': '東京都品川区南大井6-25-3 いちご大森ビル6F', 'addressLocality': '大森', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'newwork-aoto': {'streetAddress': '東京都葛飾区青戸6-1-1 朝日生命葛飾ビル4F', 'addressLocality': '青砥', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-20:00'},
  'h1t-shibuya-miyamasuzaka': {'streetAddress': '東京都渋谷区渋谷2-19-19 ワコー宮益坂8階', 'addressLocality': '渋谷', 'addressRegion': '東京都', 'openingHours': 'Mo-Sa 07:30-20:00'},
  'h1t-akasaka-mitsuke': {'streetAddress': '東京都港区赤坂3-9-2 No.R赤坂見附7階', 'addressLocality': '赤坂', 'addressRegion': '東京都', 'openingHours': 'Mo-Sa 07:30-20:30, Su 07:30-17:30'},
  'h1t-toranomon': {'streetAddress': '東京都港区虎ノ門1-1-20 虎ノ門実業会館本館9階', 'addressLocality': '虎ノ門', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:00-22:30, Sa 07:00-17:30'},
}

SEO.update(SEO_ADD_0930B); PLACE.update(PLACE_ADD_0930B)

SEO_ADD_0930C = {
  'basispoint-jimbocho': ('BasisPoint 神保町店（ベーシスポイント ジンボウチョウ）｜内装・内観・雰囲気の写真｜神保町駅1分のホテルラウンジ',
    'BasisPoint 神保町店（クロサワビル6階）の内装・内観・雰囲気を写真で。神保町駅A5出口から1分。ソファ席のあるオープンスペース、BOX席、2つの会議室を歩く順番で紹介します。'),
  'basispoint-shimbashi-ginzaguchi': ('BasisPoint 新橋銀座口店（ベーシスポイント シンバシギンザグチ）｜内装・内観・雰囲気の写真｜56名の大会議室まで',
    'BasisPoint 新橋銀座口店（カシケイビル2階）の内装・内観・雰囲気を写真で。新橋駅銀座口から1分。オープンスペース、BOX席、会議室、56名の大会議室を歩く順番で紹介します。'),
  'basispoint-nishishinjuku': ('BasisPoint 西新宿店（ベーシスポイント ニシシンジュク）｜内装・内観・雰囲気の写真｜都庁を望む10階と鍵付き個室',
    'BasisPoint 西新宿店（惠徳ビル4〜10階）の内装・内観・雰囲気を写真で。都庁と新宿中央公園を望む10階のコワーキング、1〜6名の鍵付き個室、会議室を歩く順番で紹介します。'),
  'basispoint-ikebukuro': ('BasisPoint 池袋店（ベーシスポイント イケブクロ）｜内装・内観・雰囲気の写真｜池袋駅東口1分の全席会話OK',
    'BasisPoint 池袋店（深野ビル4階）の内装・内観・雰囲気を写真で。池袋駅東口から1分、全席で会話とWeb会議ができます。オープンスペース、BOX席、個室ブース、会議室を紹介します。'),
  'hapon-shinjuku': ('HAPON 新宿（ハポン シンジュク）｜内装・内観・雰囲気の写真｜日本列島型テーブルと畳の富士の間',
    'HAPON 新宿（西新宿・武蔵ビル5階）の内装・内観・雰囲気を写真で。テーマは「日本」。日本列島型の共有テーブル、畳の「富士の間」、カフェ、本棚、会議室を歩く順番で紹介します。'),
  'co-lab-daikanyama': ('co-lab 代官山（コラボ ダイカンヤマ）｜内装・内観・雰囲気の写真｜SodaCCo のテラスと屋上',
    'co-lab 代官山（SodaCCo 4〜6階）の内装・内観・雰囲気を写真で。クリエイター向けのシェアオフィス。受付、デスク、ブース、テラス付きのルーム、屋上を歩く順番で紹介します。'),
  'co-lab-gotanda': ('co-lab 五反田 with JPRE（コラボ ゴタンダ ウィズ ジェイピーアールイー）｜内装・内観・雰囲気の写真｜サウナのあるクリエイター拠点',
    'co-lab 五反田 with JPRE（五反田JPビルディング2階）の内装・内観・雰囲気を写真で。「つくる人が集えば街がかわる」。共用部、会議室、スタジオ、サウナを歩く順番で紹介します。'),
  'nagaya-aoyama': ('NAGAYA 青山（ナガヤ アオヤマ）｜内装・内観・雰囲気の写真｜約70㎡のウッドテラスと静かな個室',
    'NAGAYA 青山（グランカーサ南青山2階）の内装・内観・雰囲気を写真で。都心でも実現できる静寂なワーク環境。オープンスペース、29室の個室、ウッドテラス、会議室を紹介します。'),
  'soil-work-nihonbashi': ('Soil work Nihonbashi 1st（ソイル ワーク ニホンバシ ファースト）｜内装・内観・雰囲気の写真｜公園に面した窓',
    'Soil work Nihonbashi 1st（日本橋小舟町・6階）の内装・内観・雰囲気を写真で。公園に面した窓から季節を感じるコワーキング。1階はカフェベーカリー PARKLET。構成と使い方を紹介します。'),
  'faro-aoyama': ('FARO青山（ファーロ アオヤマ）｜内装・内観・雰囲気の写真｜国産の木と緑のシェアオフィス',
    'FARO青山（南青山二丁目）の内装・内観・雰囲気を写真で。100％国産の木材を使った、緑につつまれたシェアオフィス。メンバーズラウンジ、スモールオフィス、屋上を歩く順番で紹介します。'),
}
PLACE_ADD_0930C = {
  'basispoint-jimbocho': {'streetAddress': '東京都千代田区神田神保町1-4-6 クロサワビル6F', 'addressLocality': '神保町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-22:00, Sa-Su 10:00-22:00'},
  'basispoint-shimbashi-ginzaguchi': {'streetAddress': '東京都港区新橋2-19-3 カシケイビル2F', 'addressLocality': '新橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-22:00, Sa-Su 10:00-22:00'},
  'basispoint-nishishinjuku': {'streetAddress': '東京都新宿区西新宿5-8-2 惠徳ビル4F-10F', 'addressLocality': '西新宿', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:00-19:00, Sa-Su 10:00-19:00'},
  'basispoint-ikebukuro': {'streetAddress': '東京都豊島区南池袋1-24-6 深野ビル4F', 'addressLocality': '南池袋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-22:00, Sa-Su 10:00-22:00'},
  'hapon-shinjuku': {'streetAddress': '東京都新宿区西新宿7-4-4 武蔵ビル5F', 'addressLocality': '西新宿', 'addressRegion': '東京都'},
  'co-lab-daikanyama': {'streetAddress': '東京都渋谷区代官山町9-10 SodaCCo 4-6F', 'addressLocality': '代官山', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'co-lab-gotanda': {'streetAddress': '東京都品川区西五反田8-4-13 五反田JPビルディング2F', 'addressLocality': '西五反田', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'nagaya-aoyama': {'streetAddress': '東京都港区南青山4-17-33 グランカーサ南青山2F', 'addressLocality': '南青山', 'addressRegion': '東京都'},
  'soil-work-nihonbashi': {'streetAddress': '東京都中央区日本橋小舟町14-7 6F', 'addressLocality': '日本橋小舟町', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'faro-aoyama': {'streetAddress': '東京都港区南青山二丁目', 'addressLocality': '南青山', 'addressRegion': '東京都'},
}

SEO.update(SEO_ADD_0930C); PLACE.update(PLACE_ADD_0930C)

SEO_ADD_0930D = {
  'startup-hub-tokyo-marunouchi': ('Startup Hub Tokyo 丸の内（スタートアップハブトウキョウ マルノウチ）｜内装・内観・雰囲気の写真｜無料の創業支援施設',
    'Startup Hub Tokyo 丸の内（明治安田生命ビル1階）の内装・内観・雰囲気を写真で。起業を考え始めた人のための無料の創業支援施設。ラウンジ、起業相談、イベント、キッズルームを紹介します。'),
  'startup-hub-tokyo-tama': ('Startup Hub Tokyo TAMA（スタートアップハブトウキョウ タマ）｜内装・内観・雰囲気の写真｜立川の創業支援施設',
    'Startup Hub Tokyo TAMA（立川 GREEN SPRINGS E2 3階）の内装・内観・雰囲気を写真で。無料の多摩の創業支援施設。ラウンジ、1,500冊以上の書籍、起業相談、キッズルームを紹介します。'),
  'nexs-tokyo-community-space': ('NEXs Tokyo コミュニティスペース（ネクスト トウキョウ コミュニティスペース）｜内装・内観・雰囲気の写真｜丸の内の会員制拠点',
    'NEXs Tokyo コミュニティスペース（新東京ビル4階）の内装・内観・雰囲気を写真で。全国と東京のスタートアップがつながる無料の会員制拠点。LIVE PARK、WORK STUDIO などを紹介します。'),
  'koca-umeyashiki': ('KOCA（コーカ）｜内装・内観・雰囲気の写真｜梅屋敷の高架下、工房のあるコワーキング',
    'KOCA（京急線 梅屋敷駅 徒歩1分）の内装・内観・雰囲気を写真で。高架下の分棟にコワーキング、デジタルファブリケーションの工房、シェアキッチンを備えた、ものづくりの拠点を紹介します。'),
  'chiyoda-platform-square': ('ちよだプラットフォームスクウェア｜内装・内観・雰囲気の写真｜2004年からのシェアオフィス',
    'ちよだプラットフォームスクウェア（竹橋駅2分）の内装・内観・雰囲気を写真で。千代田区の公共施設を生かした2004年開設のシェアオフィス。オープンネスト、会議室、屋上庭園を紹介します。'),
  'startupside-tokyo': ('StartupSide Tokyo（スタートアップサイド トウキョウ）｜内装・内観・雰囲気の写真｜水道橋の起業家支援施設',
    'StartupSide Tokyo（VORT水道橋III 8・9階）の内装・内観・雰囲気を写真で。24時間使える起業家のためのインキュベーション施設。9階のコワーキング50席と8階の個室8室を紹介します。'),
  'city-lab-tokyo': ('シティラボ東京｜内装・内観・雰囲気の写真｜京橋のまちづくりの拠点',
    'シティラボ東京（東京スクエアガーデン6階）の内装・内観・雰囲気を写真で。持続可能なまちづくりのためのオープンイノベーション拠点。天然素材の約300㎡のサロン、会議室を紹介します。'),
  'case-shinjuku': ('CASE Shinjuku（ケース シンジュク）｜内装・内観・雰囲気の写真｜高田馬場駅1分のシェアオフィス',
    'CASE Shinjuku（三慶ビル4階）の内装・内観・雰囲気を写真で。クリエイター・エンジニア・起業家がつながる高田馬場駅1分の拠点。コワーキング、シェアオフィス、個室を紹介します。'),
  'ship-osaki': ('品川産業支援交流施設 SHIP（シナガワサンギョウシエンコウリュウシセツ シップ）｜内装・内観・雰囲気の写真｜大崎のラウンジと工房',
    '品川産業支援交流施設 SHIP（大崎ブライトコア3・4階）の内装・内観・雰囲気を写真で。月額会員制のオープンラウンジ、カフェエリア、3Dプリンターのある工房を歩く順番で紹介します。'),
  'merise-tachikawa': ('me:rise 立川（ミライズ タチカワ）｜内装・内観・雰囲気の写真｜信用金庫の旧本店を生かした共創拠点',
    'me:rise 立川（立川駅北口 徒歩約4分）の内装・内観・雰囲気を写真で。多摩信用金庫の旧本店をリノベーションした共創センター。フリースペース、ブース席、個室、会議室を紹介します。'),
}
PLACE_ADD_0930D = {
  'startup-hub-tokyo-marunouchi': {'streetAddress': '東京都千代田区丸の内2-1-1 明治安田生命ビル1階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': ['Mo-Fr 10:00-22:00', 'Sa-Su 10:00-18:00']},
  'startup-hub-tokyo-tama': {'streetAddress': '東京都立川市緑町3-1 GREEN SPRINGS E2 3階', 'addressLocality': '立川', 'addressRegion': '東京都', 'openingHours': ['Mo-Fr 10:00-22:00', 'Sa-Su 10:00-18:00']},
  'nexs-tokyo-community-space': {'streetAddress': '東京都千代田区丸の内3-3-1 新東京ビル4階', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': ['Mo-Fr 10:00-22:00', 'Sa-Su 10:00-18:00']},
  'koca-umeyashiki': {'streetAddress': '東京都大田区大森西6-17-17', 'addressLocality': '梅屋敷', 'addressRegion': '東京都', 'openingHours': ['Mo-Fr 09:00-22:00', 'Sa-Su 10:00-22:00']},
  'chiyoda-platform-square': {'streetAddress': '東京都千代田区神田錦町3-21', 'addressLocality': '竹橋', 'addressRegion': '東京都'},
  'startupside-tokyo': {'streetAddress': '東京都千代田区神田猿楽町2-8-11 VORT水道橋III 8・9階', 'addressLocality': '水道橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'city-lab-tokyo': {'streetAddress': '東京都中央区京橋3-1-1 東京スクエアガーデン6階', 'addressLocality': '京橋', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 09:30-18:00'},
  'case-shinjuku': {'streetAddress': '東京都新宿区高田馬場1-28-10 三慶ビル4階', 'addressLocality': '高田馬場', 'addressRegion': '東京都', 'openingHours': 'Mo-Sa 10:00-18:00'},
  'ship-osaki': {'streetAddress': '東京都品川区北品川5-5-15 大崎ブライトコア3・4階', 'addressLocality': '大崎', 'addressRegion': '東京都', 'openingHours': ['Mo-Fr 08:00-22:00', 'Sa-Su 09:00-18:00']},
  'merise-tachikawa': {'streetAddress': '東京都立川市曙町2-8-28 TAMA MIRAI SQUARE', 'addressLocality': '立川', 'addressRegion': '東京都'},
}

SEO.update(SEO_ADD_0930D); PLACE.update(PLACE_ADD_0930D)

SEO_ADD_0930E = {
  'tefu-lounge-shimokitazawa': ('tefu lounge 下北沢（テフ ラウンジ シモキタザワ）｜内装・内観・雰囲気の写真｜駅0分のラウンジ複合施設',
    'tefu lounge 下北沢の内装・内観・雰囲気を写真で。下北沢駅の南西改札口から0分。カフェ併設のラウンジ、3階のブースと会議室、4階のルームとテラスを紹介します。'),
  'tefu-jiyugaoka': ('tefu jiyugaoka（テフ ジユウガオカ）｜内装・内観・雰囲気の写真｜ビンテージ家具のラウンジ',
    'tefu jiyugaoka の内装・内観・雰囲気を写真で。自由が丘駅南口から2分。ビンテージ家具が点在するカフェ併設のラウンジ、会議室、24時間使えるオフィスを紹介します。'),
  'mov-kuramae': ('MOV KURAMAE（モヴ クラマエ）｜内装・内観・雰囲気の写真｜コクヨのシェア型オフィス',
    'MOV KURAMAE の内装・内観・雰囲気を写真で。コクヨが蔵前で運営する8階建てのシェア型オフィス。2階のラウンジ、1階のカフェ、ブース、畳の会議室を紹介します。'),
  'ryozan-park-sugamo-grand': ('RYOZAN PARK 巣鴨 GRAND（リョウザン パーク スガモ グランド）｜内装・内観・雰囲気の写真｜シェアキッチン付き',
    'RYOZAN PARK 巣鴨 GRAND の内装・内観・雰囲気を写真で。自然素材とアートの1階コワーキング、TEL ブース、会議室、個室、許可付きのシェアキッチンを紹介します。'),
  'ryozan-park-sugamo-annex': ('RYOZAN PARK 巣鴨 ANNEX（リョウザン パーク スガモ アネックス）｜内装・内観・雰囲気の写真｜モノトーンの集中空間',
    'RYOZAN PARK 巣鴨 ANNEX の内装・内観・雰囲気を写真で。自然光の入るモノトーンのコワーキング、アーロンチェア、集中ブース、会議室を紹介します。学割プランもあります。'),
  'ryozan-park-otsuka': ('RYOZAN PARK 大塚 OTSUKA（リョウザン パーク オオツカ）｜内装・内観・雰囲気の写真｜いちばん広いコワーキング',
    'RYOZAN PARK 大塚 OTSUKA の内装・内観・雰囲気を写真で。6階の広く開放的なコワーキング、共有スペース、会議室、集中ブース、5階の個室と固定席を紹介します。'),
  'ryozan-park-otsuka-green': ('RYOZAN PARK 大塚 GREEN（リョウザン パーク オオツカ グリーン）｜内装・内観・雰囲気の写真｜平田晃久設計',
    'RYOZAN PARK 大塚 GREEN の内装・内観・雰囲気を写真で。建築家・平田晃久氏が手がけた緑あふれるオフィス。共有スペース、固定席、個室、実験室のような会議室を紹介します。'),
  'mid-point-komagome': ('MID POINT 駒込（ミッドポイント コマゴメ）｜内装・内観・雰囲気の写真｜六義園を望むラウンジ',
    'MID POINT 駒込の内装・内観・雰囲気を写真で。駒込駅から3分の8・9階。六義園を望む窓と苔をイメージした緑のタイルのラウンジ、ワークスペース、個室を紹介します。'),
}
PLACE_ADD_0930E = {
  'tefu-lounge-shimokitazawa': {'streetAddress': '東京都世田谷区北沢2-21-22', 'addressLocality': '下北沢', 'addressRegion': '東京都'},
  'tefu-jiyugaoka': {'streetAddress': '東京都世田谷区奥沢5-42-3', 'addressLocality': '自由が丘', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 09:00-21:00'},
  'mov-kuramae': {'streetAddress': '東京都台東区蔵前1丁目4-1', 'addressLocality': '蔵前', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'ryozan-park-sugamo-grand': {'streetAddress': '東京都豊島区巣鴨1-9-1 グランド東邦ビル', 'addressLocality': '巣鴨', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 06:00-24:00'},
  'ryozan-park-sugamo-annex': {'streetAddress': '東京都豊島区巣鴨1-7-6 東邦アネックス2F', 'addressLocality': '巣鴨', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 06:00-24:00'},
  'ryozan-park-otsuka': {'streetAddress': '東京都豊島区南大塚3-36-7 南大塚T&Tビル', 'addressLocality': '大塚', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 06:00-24:00'},
  'ryozan-park-otsuka-green': {'streetAddress': '東京都豊島区南大塚2丁目35-11 Urban Green', 'addressLocality': '大塚', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 00:00-24:00'},
  'mid-point-komagome': {'streetAddress': '東京都文京区本駒込6丁目25番5号 HONKOMAGOME NISHIGAI BUILDING 8〜9F', 'addressLocality': '駒込', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-23:00'},
}

SEO.update(SEO_ADD_0930E); PLACE.update(PLACE_ADD_0930E)

SEO_ADD_0930F = {
  'h1t-otemachi': ('H¹T大手町（エイチワンティー オオテマチ）｜内装・内観・雰囲気の写真｜20階・21階に個室45室',
    'H¹T大手町（大成大手町ビル20階・21階）の内装・内観・雰囲気を写真で。大手町駅B2a出口1分、野村不動産の法人向けシェアオフィス。オープンスペース、ボックス、個室45室、会議室を紹介します。'),
  'h1t-jimbocho': ('H¹T神保町（エイチワンティー ジンボウチョウ）｜内装・内観・雰囲気の写真｜神保町駅1分、会議室4室',
    'H¹T神保町（いちご神保町ビル5階）の内装・内観・雰囲気を写真で。神保町駅A7出口1分、平日に開く野村不動産の法人向けシェアオフィス。14席のオープンスペース、個室、会議室4室を紹介します。'),
  'h1t-ginza': ('H¹T銀座（エイチワンティー ギンザ）｜内装・内観・雰囲気の写真｜銀座駅1分、土日祝も7時から',
    'H¹T銀座（銀座センタービル4階）の内装・内観・雰囲気を写真で。銀座駅A7出口1分、毎日7時から22時まで開く法人向けシェアオフィス。18席のオープンスペース、個室11室、会議室4室を紹介します。'),
  'basispoint-gotanda': ('BasisPoint 五反田店（ベーシスポイント ゴタンダ）｜内装・内観・雰囲気の写真｜受付なしで入れるラウンジ',
    'BasisPoint 五反田店（五反田さくらビル3階）の内装・内観・雰囲気を写真で。五反田駅東口3分、スマートロックで入れるコワーキング。オープンスペース、個室ブース、BOX席、会議室を紹介します。'),
  'newwork-tokyo-the-flagship': ('NewWork 東京 The Flagship（ニューワーク トウキョウ ザ フラッグシップ）｜内装・内観・雰囲気の写真｜東京駅1分の95席',
    'NewWork 東京 The Flagship（丸の内トラストタワーN館11階）の内装・内観・雰囲気を写真で。東急が運営する法人会員制のサテライトオフィス。95席、会議室4室、個室ブース22室を紹介します。'),
}
PLACE_ADD_0930F = {
  'h1t-otemachi': {'streetAddress': '東京都千代田区大手町2-1-1 大成大手町ビル20階・21階', 'addressLocality': '大手町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 07:30-22:00, Sa 08:00-18:00'},
  'h1t-jimbocho': {'streetAddress': '東京都千代田区神田神保町1-11-1 いちご神保町ビル5階', 'addressLocality': '神保町', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
  'h1t-ginza': {'streetAddress': '東京都中央区銀座4-6-11 銀座センタービル4階', 'addressLocality': '銀座', 'addressRegion': '東京都', 'openingHours': 'Mo-Su 07:00-22:00'},
  'basispoint-gotanda': {'streetAddress': '東京都品川区東五反田1-22-6 五反田さくらビル3F', 'addressLocality': '五反田', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-22:00, Sa-Su 10:00-22:00'},
  'newwork-tokyo-the-flagship': {'streetAddress': '東京都千代田区丸の内1-8-1 丸の内トラストタワーN館 11F', 'addressLocality': '丸の内', 'addressRegion': '東京都', 'openingHours': 'Mo-Fr 08:00-21:00'},
}

SEO.update(SEO_ADD_0930F); PLACE.update(PLACE_ADD_0930F)
