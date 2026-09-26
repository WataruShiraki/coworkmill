# COWORKMILL 東京コワーキング10施設 調査メモ（2026-09-26）

出力: cowork_facilities.py（A30 = 10件）。写真URLはすべて WebFetch が返したものだけ（curl 不使用）。写真の中身は目視できていないため、キャプションはページ上の掲載位置（セクション名・ファイル名）から付けた。公開前に画像を実際に見てキャプションを合わせる必要あり。

## 入れ替え（2件）
| 依頼 | 結果 | 理由 |
|---|---|---|
| SHIBAURA HOUSE | → **WeWork 渋谷スクランブルスクエア**（予備1） | shibaurahouse.jp は Studio 製でJS描画。WebFetch で取れた写真が1枚（1F Living）のみ、Access ページは404。事実（2011年・妹島和世設計・7層・1F 100㎡等）は取れたが写真4枚に届かず |
| Impact HUB Tokyo | → **co-ba ebisu**（予備2の代替） | hubtokyo.com もJS描画でメタ情報のみ、写真0枚。予備の co-ba shibuya（co-ba.net/shibuya/）は写真0枚で、運営も別会社（グランサーズコワーキング）だったため、co-ba 直営の恵比寿拠点（co-ba.net/ebisu/、写真20枚）に変更 |

## 3回目の修正（コーディネーターの画像目視の結果）
- shibuya-qws: #1 img.jpg はフロア図 → 削除。hero を #3 project_img02 に変更（写真7枚）
- 100banch: #2 floor-4（ポスター）#3 floor-5（照明の寄り）→ 削除（写真6枚。hero #1 のまま）
- cic-tokyo → **co-lab 渋谷キャスト（slug: co-lab-shibuya-cast）** に差し替え（上記3番）
- midori-so-nakameguro: #6（本の寄り）#7（看板の寄り）→ 削除（写真6枚）
- co-ba-ebisu: #8（ロゴのイラスト）→ 削除（写真7枚）
- wework: hero を #2（人のいるラウンジ）に変更、#1 は step 01 に残した
- lifork-otemachi: hero は #3 photo-lounge.jpg（会員ラウンジ）
- 候補として当たって使えなかったもの: Kant.（証明書エラー）、Blink（名前解決不可）、BASE Q（名前解決不可）、TIB（写真がog画像のみ・ニュース記事404）、point 0（写真2枚）、THE CAMPUS（フロアガイドに画像なし）、Startup Hub Tokyo（相対パスのみ）

## 2回目の修正（コーディネーター指摘）
- **Nagatacho GRiD → LIFORK 大手町（slug: lifork-otemachi）**: grid.tokyo.jp がVPNサイト化（施設閉鎖の可能性）、ガイアックスの写真8枚中6枚が360px幅のサムネのため削除・差し替え。
- **SAAI の写真**: /space/ の png（630×330）をやめ、トップページのヒーロースライダー 1.jpg〜6.jpg と SPACE セクションの fw_img.jpg の7枚に差し替え。★サイズは未計測（curl も wsrv.nl も遮断）。ヒーロースライダーなので通常は横幅1000px超だが、ブラウザで要確認。中身も未確認のためキャプションは「館内の風景」など中立にしてある。目視後に具体化すること。yurakucho-saai.com にはギャラリー／ニュースのサブページは無し（note.com のみ）。

## 施設ごと

### 1. 100BANCH（slug: 100banch）写真6
- 出典: https://100banch.com/about/ ／ https://100banch.com/about/floor/ ／ https://100banch.com/about/access-contact/
- 事実: 2017年7月7日開設、渋谷3-27-1、1F KITCHEN(カフェ・カンパニー)/2F GARAGE(常時10〜20組、U35)/3F LOFT(100人規模、200インチ、木のステージ)、平日10-19時、見学ツアー17時2,200円、GARAGE Program 毎月審査・無料
- 写真: about ページの img-switch-1〜3、floor ページの img-slide-floor-1〜6。★スライド1〜3が3F、4〜6が2F と推定（ページの掲載順）。要目視
- 不確か: 設計者、面積

### 2. SHIBUYA QWS（shibuya-qws）写真7
- 出典: https://shibuya-qws.com/ ／ /about/ ／ /about/space/ ／ /about/outline/
- 事実: 渋谷2-24-12 スクランブルスクエア東棟15階、約2,600㎡、9-22時、会員4区分、SCRAMBLE HALL 200名、連携大学7校
- 写真: /about/space/ の img.jpg, project_img01/02, cross_img01/02, scramble_img01, salon_img01, playground_img01
- 不確か: 運営会社名（トップに Loftwork 採用リンクがあるだけ）、開業日、設計者 → ask に入れた

### 3. co-lab 渋谷キャスト（co-lab-shibuya-cast）写真8【CIC Tokyo の差し替え・3回目の修正】
- 出典: https://www.co-lab.jp/base/shibuya-cast/ ／ https://co-lab.jp/
- 事実: 渋谷1-23-21 渋谷キャスト1-2F、春蒔プロジェクト株式会社（co-lab は2003年〜）、ルーム4(12〜22人 380,000円〜)／アトリエ8(4〜12人 160,000円〜)／スタジオ7(3〜5人 126,000円〜)／ブース16(1〜2人 60,000円〜)／デスク5(42,000円〜)／フレックス(15,000円〜)税別、24時間365日、会議室4・co-factory・イベントスペース・キッチン・駐輪場、渋谷キャストは17階建て「Echoes of Uniqueness／不揃いの調和」
- 写真: DSC_1616(2F窓際共用), DSC_1537(2Fブース), DSC_1568(2Fスタジオ), DSC_1474(2Fキッチン), DSC_1640(1F MR), DSC_1409(会議室4), DSC_1339(1F共用部入口), DSC_1316(渋谷キャスト外観)。すべて幅1024px版
- 不確か: 開設日（記載なし）、設計者
- CIC Tokyo は /en/cic-tokyo/ /news/ /innovation-program/ 各ニュース記事まで当たったが、実写真は外観1＋内観1のみ（png3枚はイラスト）で4枚に届かず削除

### 4. 虎ノ門ヒルズ ARCH（toranomon-hills-arch）写真8
- 出典: https://arch-incubationcenter.com/ ／ /service/index.html ／ /facility/index.html（toranomonhills.com/arch/ と arch.mori.co.jp は404/名前解決不可）
- 事実: ビジネスタワー4階、3,800㎡、森ビル企画運営、内装 Wonderwall®、空間名（CO-WORK 等）、4本柱
- 写真: facility_001/002/008/010/004/003/007/011（FACILITY ページのキャプション付き）
- 不確か: 開業日、入居社数、料金

### 5. LIFORK 大手町（lifork-otemachi）写真8【Nagatacho GRiD の差し替え・2回目の修正】
- 出典: https://lifork.jp/ ／ /otemachi/ ／ /otemachi/workroom.html ／ /otemachi/lounge.html ／ /otemachi/styleroom.html ／ /otemachi/access.html
- 事実: 大手町1-5-1 大手町ファーストスクエア ウエストタワー1・2階、NTT都市開発、シェアオフィス13タイプ(4〜30名)、24時間365日、入会金1か月・保証金1.1か月・追加会員22,000円、レンタルラウンジ199.1㎡ 着席50/立食60 60分44,000円 9-21時、スタイルルーム B〜L 10室 30分1,650〜4,400円
- 写真: workroom-intro02/01, service/photo-lounge, photo-locker, photo-selfdrink_wr, lounge1, lounge5（セミナー例）, styleroom/roomG-fg07（各ページのキャプション付き）
- 不確か: 開業日、設計者。Kant.（kant.co.jp）は証明書エラー、Blink（blink.co.jp）は名前解決不可で取得できず

### 6. WeWork 渋谷スクランブルスクエア（wework-shibuya-scramble-square）写真8【SHIBAURA HOUSE の代替】
- 出典: https://wework.co.jp/location/tokyo/shibuya-aoyama-area/shibuya-scramble-square（wework.com/ja-JP からのリダイレクト先）
- 事実: 渋谷駅直結、37〜42階・45階、会議室70、天井3,000〜3,200mm、平日8:30〜20:00、ビル 地上47階地下7階 東棟2019年11月開業、駐車116台、プラン4種
- 写真: SSS-42F_* 6枚＋WeWork-Shibuya-Scramble-Square-3.webp＋外観
- 不確か: WeWork の入居開始日、面積

### 7. MIDORI.so Nakameguro（midori-so-nakameguro）写真6
- 出典: https://midori.so/locations/nakameguro ／ https://midori.so/about ／ https://midori.so/
- 事実: 青葉台3-3-11、本館2F/3F・母屋1F/2F、蔦に覆われた廃屋を改装、24時間365日、フリーデスク42,350円/固定60,500円/入会金11,000円、ポップイン3,300円・11日33,000円、ギャラリー料金、運営ミライ・インスティテュート2011-01-05設立
- 写真: sanity CDN の URL（クエリ付き）を _wq で包んだ。8枚中、縦長写真が多い
- 不確か: 中目黒拠点の開設年、設計者

### 8. co-ba ebisu（co-ba-ebisu）写真7【Impact HUB Tokyo の代替】
- 出典: https://co-ba.net/ebisu/ ／ https://co-ba.net/
- 事実: 恵比寿西1-33-6 JP noie 恵比寿西 1F/2F、2019年11月開設、1,573.42㎡、バ・アンド・コー運営、料金表一式、PARK 70人・CAFE 40人、ドロップイン2,000円
- 写真: co-ba_ebisu_1f.jpg, 1-31-1.jpg, co-ba-ebisu_5_16-9.jpg, imgi_33_park.jpg, imgi_34_cafe.jpg, DSC04949.jpg（シングルルーム）, ebisu_2f_220_01.jpg（スイート）, imgi_2_ebisu_web_main_@2.jpg（メイン）。日本語ファイル名の1枚は避けた
- 不確か: 設計者、席数

### 9. SAAI（saai-yurakucho）写真7
- 出典: https://yurakucho-saai.com/ ／ https://yurakucho-saai.com/space/（saai.tokyo は名前解決不可 → 検索で公式 yurakucho-saai.com を特定）
- 事実: 新東京ビル（丸の内3-3-1）、2020年2月、B1F/1F/4F、各空間の説明文、料金（コミュニティ16,500／フリーデスク33,000／固定ブース77,000／個室ASK）、運営 三菱地所
- 写真: トップのヒーロースライダー 1.jpg〜6.jpg ＋ fw_img.jpg?ver=2（2回目の修正で差し替え。サイズ・中身は未確認）
- 不確か: 設計者、面積

### 10. Business Airport 青山（business-airport-aoyama）写真6
- 出典: https://business-airport.net/shop/aoyama/ ／ /concept/ ／ /
- 事実: 南青山3-1-3 スプライン青山東急ビル4F・6F、2013年3月、外苑前1a出口3分、コワーキング平日7-22時・日祝10-18時、受付平日9-18時、会議室5＋オンライン、イベント60名、東急不動産、20拠点、ブランド共通料金
- 写真: 2025/09 の6枚（260315_175-HDR-Edit, 260315_178-HDR-1, 260315_140-Edit, aoyama-workspace__img01, aoyama-merit__img03, aoyama-info__img）
- 不確か: 設計者、面積・席数。土曜の営業時間は出典に記載なし（そのまま書いていない）

## 未使用の候補
- Tokyo Innovation Base（tib.metro.tokyo.lg.jp）: 写真が og 画像程度で不可
- co-ba shibuya: 写真0、運営別会社
