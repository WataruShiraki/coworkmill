# ★最初に読む：人の顔が分かる写真は使わない（2026-09-28 わたるさんのルール）

わたるさん「MILLシリーズだけど基本的に人の顔が認識できる画像は絶対使わないで。いろいろと問題が起こるから。ちゃんと守るように。これから。」

- 人の顔が分かる写真は、TOP画像にも本文にも使わない。後ろ姿や、遠くて顔の分からない人はよい。
- 2026-09-28 に全部の写真を目で確認し、顔の分かる写真を外した。外した一覧は cowork_facilities.py の末尾の `_DROP_FACE`（写真の番号）と `_HOLD_FACE`（写真が残らなくなって保留にした施設）にある。
- 保留にした施設の URL は gone.txt に書き、about_ops.py が vercel.json で一覧ページへ転送している（gone.txt がないサイトは保留なし）。
- ★施設を足すとき、ビルドする前に必ず GitHub の最新の _src を取り直すこと。手元の古い写しでビルドすると、外した写真が本番に戻ってしまう。
- ★新しく足す施設も、写真を1枚ずつ見て、顔の分かる写真は IMG に入れない。外した結果、店内の写真が1枚以下になる施設は載せない。

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
