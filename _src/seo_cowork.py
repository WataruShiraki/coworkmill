# cowork のページごとの SEO（2026-09-26 に本番へ入れたもの）。メタタイトルは末尾に " | COWORKMILL" が自動で付く
# SEO[slug] = (メタタイトル, description)。PLACE[slug] = 住所（構造化データ LocalBusiness の address と openingHours。名前・URL・写真・ひとことは施設データから自動）。REDIRECTS = 旧スラッグ → 新スラッグ
INDEX_TITLE = "COWORKMILL（コワークミル）｜内装デザインが最も優れたコワーキングを厳選紹介"
INDEX_DESC = "内装・内観・雰囲気で選ぶ、東京のコワーキングスペース・シェアオフィス10施設。渋谷・虎ノ門・大手町・中目黒・恵比寿・有楽町・青山の空間を、公式の写真と情報で、初めて訪れる人が歩く順番で紹介します。"
LIST_TITLE = "東京の内装がかっこいいコワーキング10施設｜内観・雰囲気の写真"
LIST_DESC = "渋谷・虎ノ門・大手町・中目黒・恵比寿・有楽町・青山。内装・内観・雰囲気の写真で選ぶコワーキングスペース10施設を、公式情報をもとに1施設ずつ紹介します。"
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
