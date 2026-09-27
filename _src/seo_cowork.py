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
