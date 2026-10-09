# ★2026-09-29 build_site.py に記事下のおすすめを追加。ビルドの前に必ず最新を取り直すこと

# ★最初に読む：人の顔が分かる写真は使わない（2026-09-28 わたるさんのルール）

わたるさん「MILLシリーズだけど基本的に人の顔が認識できる画像は絶対使わないで。いろいろと問題が起こるから。ちゃんと守るように。これから。」

- 人の顔が分かる写真は、TOP画像にも本文にも使わない。後ろ姿や、遠くて顔の分からない人はよい。
- 2026-09-28 に全部の写真を目で確認し、顔の分かる写真を外した。外した一覧は cowork_facilities.py の末尾の `_DROP_FACE`（写真の番号）と `_HOLD_FACE`（写真が残らなくなって保留にした施設）にある。
- 保留にした施設の URL は gone.txt に書き、about_ops.py が vercel.json で一覧ページへ転送している（gone.txt がないサイトは保留なし）。
- ★施設を足すとき、ビルドする前に必ず GitHub の最新の _src を取り直すこと。手元の古い写しでビルドすると、外した写真が本番に戻ってしまう。
- ★新しく足す施設も、写真を1枚ずつ見て、顔の分かる写真は IMG に入れない。外した結果、店内の写真が1枚以下になる施設は載せない。

## 2026-09-28 別チャットの追加分の統合（Drive「02_設計書・指示書」の「連絡_統合のお願い_2026-09-28.md」どおり）

- 2回目の追加 cowork_add_2026-09-28_d/e/f.py（30施設） は cowork_facilities.py の末尾（SEO と住所は seo_cowork.py の末尾）に統合済み。30施設のうち19施設を掲載、11施設は保留（顔の分かる写真を外すと館内の写真が2枚以下になる10施設と、コワーキングではない THE BASE 浜松町）。
- 写真の確認結果は cowork_facilities.py の最後の `_HOLD_FACE2`・`_DROP_FACE2`・`_HERO_FACE2` にある。
- ★1回目の追加 cowork_facilities_add.py（1回目の追加分・10施設） は、写真の顔チェックがまだのため統合していない。brands.py は cowork_facilities.py を読む形に戻した。載せる場合は、写真を1枚ずつ確認してから cowork_facilities.py の末尾に足すこと。
- ★brands.py を別ファイルに差し替えるやり方はやめて、追加は必ず cowork_facilities.py の末尾に足す（顔写真を外す処理が末尾にあるため、その前に足すこと）。

# COWORKMILL の生成器（2026-09-27 保全版）

公開物（リポジトリ直下の index.html・spaces/・collections/・questions/ など）は、この _src/ だけで作り直せます。
2026-09-27 に、本番の HTML と 1 バイトも違わない出力になることを確認済み（favicon・OGP・バナーまで含む）。

## 作り方

    cd _src
    BRAND=cowork OUT_DIR=/どこか/out/ python3 build_mill.py

出力先の中身をリポジトリ直下にそのまま上げる（1サイト1コミット）。他のリポジトリは要りません。

## ファイル

- build_mill.py … 本体。deps/off/build_site.py（OFFISNAP の生成器の写し）を読み込み、ブランドに関わる部分を文字列置換で差し替えて実行する。§8 が 2026-09-26 後半のぶん（メタタイトル・構造化データ・絞り込み・一言・OGP）
- brands.py … ブランドの設定（名前・ドメイン・色・文言）
- cowork_facilities.py … 施設データ（本文・写真の直リンク・読み・街）。施設を足すときはここに _add(...) を足す
- collections_cowork.py … 特集。一覧の「テーマ」の絞り込みはこの特集の所属から自動で作る
- questions_cowork.py … Q&A（8問）。書き方は QUESTIONS_FORMAT.py
- seo_cowork.py … ページごとのメタタイトル・description（SEO）、構造化データの住所（PLACE）、トップと一覧のタイトル、旧スラッグの転送（REDIRECTS）。施設を足したら SEO と PLACE にも1行ずつ足す
- logo_cowork.svg … ヘッダーのロゴ（公式 SVG）。icons_cowork/ … favicon 一式（公式アイコンから）。banner/ … OFFICEMILL 送客バナー
- deps/ … OFFISNAP の build_site.py と WALL の style.css / index.html の写し（deps/README.md）。OFFISNAP 側を改良したらここにもコピーする
- RESEARCH_RULES.md … 施設調査のルール（写真は公式の直リンクのみ）

## 施設を1軒足す手順
1. cowork_facilities.py に _add(...) を足す（既存の1軒をコピーして書き換える）
2. seo_cowork.py の SEO と PLACE に、その slug の行を足す
3. 特集に入れるなら collections_cowork.py に足す
4. ビルドして、出力先の中身をコミット

## 2026-10-08 追加（cowork_add_1008.py・10施設）
- ワークスタイリングSOLO の10拠点（大宮西口・浦和・所沢・松戸・本八幡・西船橋・津田沼・調布・登戸・溝の口）。_ws7（10/07 分）を使う
- 写真は全部目視し、人の写る写真はなし。住所は各拠点ページの本文から取った
- ★重複の確かめ方：spaces/*.html のファイル名でも照らし合わせること（錦糸町・中野・荻窪はすでに載っていた）
- 残り候補：SOLO 成城学園前・新百合ヶ丘・たまプラーザ・センター北・鶴見・戸塚・大船・藤沢・柏の葉（住所の記載が見つからず保留）ほか

## 2026-10-09 追加（cowork_add_1009.py・10施設）
- ワークスタイリングSOLO の9拠点（ららぽーと柏の葉店・成城学園前・新百合ヶ丘・たまプラーザ・センター北・鶴見・大船・藤沢・名古屋新幹線口）と、提携拠点「福山（コワーキングスペースtovio）」。tovio は運営会社が公式ページに無いので「運営」を書いていない
- 写真は全部目視。新百合ヶ丘の個室写真2枚（privateroom_01-8・02-8）に人が写っていたので外した
- 見送り：SOLO 戸塚（公式の写真が3枚）。Olive LOUNGE 下高井戸・成増はすでに載っていた
- 残り候補：Olive LOUNGE 塚口（写真3枚）・key-site・hiromalab（各4枚）ほか。SOLO はこれでほぼ全部
