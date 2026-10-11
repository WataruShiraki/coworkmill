# MILL インバウンド化パッケージ（COWORKMILL で作り込んだ型・2026-10-11）

わたるさんの方針：「MILL（WALL・OFFISNAP・DESKMILL 以外）を、訪日客・外国企業向けに全部英語へ」。
COWORKMILL（cowkml.com）で「できるところをやり尽くした」型を、ほかの MILL（CAFEMILL・OFFICEMILL など）にそのまま持っていくための手順書です。

---

## 1. 守ること（全MILL共通）

- **事実は公式サイトだけ**から。推測で埋めない。分からない項目は欄ごと出さない（「—」＋注記「公式情報に記載なし」）。
- **英語の住所と日本語の住所**を並べる（タクシー用。日本語はコピーボタンと Google Maps リンクつき）。番地のローマ字は推測になるので書かない。
- **企業名・施設名そのものを公式HPへのリンクに**する（「Website ↗」を別に置かない）。
- **自作アイコン禁止**。文字と写真だけ。
- **テキストだらけにしない**（2026-10-11 指摘）。一覧系（特集・Q&A）は改修前と同じ**写真カード**：
  - 特集：大きい写真1枚＋小さい写真3枚＋件数＋タイトル＋短い説明（`col_card`）
  - Q&A：写真3枚の帯の上に質問を重ねる（`q_card`）
- 同じページで同じ内容を繰り返さない（例：Plan your visit に出した項目は、本文上の事実欄から外す）。
- 報告・作業メモは日本語。サイトは英語。

## 2. ページの部品（COWORKMILL の `build_en.py` にある関数）

| 部品 | 中身 | 関数・データ |
|---|---|---|
| 施設ページの「Plan your visit」 | Who / Price / Hours / Closed / Train / **Has（設備）** / **How（予約・入り方）** / **Pay（支払い）** / **English** ＋「Checked on the official website, 年月」 | `space_page` / `en/visit_extra.json` |
| タクシー欄 | 日本語住所＋英語住所（建物名・階・街・県）＋コピー＋Google Maps | `en_address` |
| 設備（Has） | 本文（公式由来の英訳）に書かれた設備だけを拾う。否定文・「1F Kitchen」のような階名は除外 | `AMEN` / `amenities` |
| 特徴タグ（絞り込み） | Day pass / Open weekends / Open late / 24-hour access / Station-linked / Phone booths / English website / Members only | `traits` |
| 検索の入口ページ `/find/` | 用途（day pass・24時間・週末・夜・電話ブース・英語サイト）と地域（都道府県）ごとの固定URL。訪日客は「coworking + 地名/用途」で検索する | `FINDS` / `PREF_FINDS` / `find_page` |
| 特集の「Planning a visit」 | 数字のまとめ／最寄り駅／Drop in for a day（料金・入り方・支払い）／比較表（Day pass・Price・Hours・Payment・English）／よくある質問（FAQ構造化データつき） | `visitor_block` |
| 旅行者向け Q&A | 支払い方法・英語対応・初めて行くときに必要なもの | `en/questions.json` |
| 英語の掲載案内・特商法表記 | `about/list-your-space.html`・`about/legal-notice.html`（日本語原本は残す） | `LIST` / `LEGAL` |
| OFFICEMILL バナー（英語版） | 全ページ下部 728x90 | `om_banner` |

### `en/visit_extra.json` の形（施設ごと）
```json
"slug": {
  "Who": "誰向けか（会員限定・法人限定など）",
  "Price": "料金（税込/税抜を明記）",
  "Hours": "営業時間（本文に無いときの補完）",
  "Booking": "予約・入り方（例: Drop-in: sign up at reception, no booking needed.）",
  "Payment": "支払い方法（現金不可・交通系IC・PayPay など）",
  "English": "英語サイト・英語スタッフ（『日本語のみ』と公式が書いていればそれも）",
  "day": true,
  "src": "確認した公式ページのURL"
}
```
- チェーン（同じ運営会社）は、運営会社の公式ルールを一度確かめて全拠点に当てはめる（例：WeWork・H¹T・ワークスタイリング）。拠点ごとに違う値（時間・料金）は拠点ページで上書き。

## 3. SEO・SNS（全MILL共通の基準）

- タイトル 60字以内（`fit()` で候補を順に試す）。「施設名, 街 — photos & how to visit | ブランド」。街名が施設名に入っていれば重ねない。
- 説明文 158字以内。「特徴. 施設名: photos, prices, hours, how to get in and the Japanese address for your taxi.」
- 特集のタイトルには必ず「coworking + 地名/用途」を入れる（`COL_SEO`）。CAFEMILL なら「cafe + 地名」。
- OGP：og:title / description / url / type / image / locale(en_US) / twitter:card(summary_large_image)。トップはブランド画像、施設・特集・Q&Aは写真。
- 構造化データ：施設＝Article＋LocalBusiness（住所）、特集＝ItemList＋FAQPage、Q&A＝FAQPage、入口ページ＝ItemList、トップ＝WebSite＋SearchAction。
- **旧日本語ページは英語版へ 301 転送**（`vercel.json` の redirects）。作業用ページは `X-Robots-Tag: noindex`（`vercel.json` の headers）。
- 公開後に Search Console でサイトマップを再送信（Chrome で実施）。

## 4. 点検（公開のたびに）

```
cd <サイトのリポジトリ>
python3 _src/audit_en.py . _src/en/visit_extra.json
```
- タイトル60字超・説明文160字超・OGP/canonical 抜け・サイト内リンク切れ・検索に載る日本語ページ・同じタイトル/説明文を一覧で出す。
- 写真の表示とスマホ幅（390px）は、本番を Chrome で開いて確かめる（写真は外部サイトなので、コンテナからは読めない）。
- 写真が読めなかったときは `en.js` が `img.broken` を付けて地の色で受ける（壊れた画像アイコンを出さない）。

## 5. ほかの MILL に展開する順番

1. 英訳データ（施設本文・特集・Q&A）を作る（COWORKMILL の `en/b*.json` の形）
2. `build_en.py` を複製し、ブランド名・色・`VISIT_KEYS`・`AMEN`（設備）・`TFILTERS`（絞り込み）をその業種に合わせる
   - CAFEMILL の例：Has＝Wi-Fi / Power outlets / English menu / Non-smoking / Takeout / Kids welcome、絞り込み＝Open early / Open late / Wi-Fi / English menu / Card OK
3. `visit_extra.json` を公式サイトで埋める（チェーン → 個店の順）
4. `/find/` の用途・地域を業種に合わせる
5. 特集に `visitor_block`、一覧は写真カード（`col_card` / `q_card`）
6. 旧日本語ページを 301、作業用ページを noindex
7. `audit_en.py` → Chrome で本番確認 → Search Console にサイトマップ再送信

## 6. 失敗の記録（同じことをしない）

- JSON を `indent=1` で書き戻して全行差分になった → **元の書式（questions.json は `indent=0`、b*.json は元の並び）を保つ**。差し替えは該当行だけ。
- `__pycache__` をコミットに入れてしまった（2回）→ コミット前に `git status --short | grep -v '^ M'` で確認。
- 「Most are in Yokohama (3)…」のように、件数がばらけているのに「ほとんど」と書いた → **「Areas include …」**。
- 「English website」は運営会社サイトの英語版。施設スタッフが英語を話せるという意味ではない（ページにもそう書く）。
- テキストだけの特集一覧・Q&A一覧は「見る気にならない」と言われた → 写真カードに戻した。
- SNSカードを文字だけの自作画像にする案は、見た目で劣るので見送り（写真のまま。壊れたときは JS で受ける）。

## 7. 2026-10-11 に足した部品（ほかの MILL にもそのまま移せる）

- **地方の入口**：`PREF_FINDS` に地域を足すと `/find/<地域>.html` ができる（京都・福岡・札幌・沖縄を追加）。地方の施設は「旅行者が予約なし・1日から使えるか」を優先して選ぶ（ホテル併設・駅直結が強い）
- **旅行者向けQ&A**：`en/questions.json` に `outside-tokyo`（東京以外で1日使える場所）・`id-registration`（身分証と登録）・`weekly-pass`（週単位の利用）。質問が60字を超えるときは `title` に短い題を入れる
- **鮮度**：`en/checked.json`（施設ごとの「公式サイトで確かめた日」）を施設ページに表示し、サイトマップの lastmod にも使う。`python3 freshness.py` で90日を過ぎた施設を人気順に10件出し、確かめ直したら `--mark`、閉店なら `--gone`
- **地図**：`map_en.py`。座標は公式住所を国土地理院の住所検索（msearch.gsi.go.jp）で変換し `en/geo.json` に保存。コンテナからは届かないので、Chrome で maps.gsi.go.jp を開き、そのページから fetch する（JSON のページ自体からは fetch できない）。Leaflet＋OSM タイル、地域ボタン付き、`?pref=Fukuoka` で絞り込み
- **中国語・韓国語の入口**：`lang_hubs.py`。施設ページは英語のまま、入口だけ母語（使い方3点・地域・1日使える施設・人気・Q&A）。hreflang を英語トップと相互に張る。翻訳の文言は固定、施設データから自動で並べる
- **運営者からのリンク**：掲載依頼ページに「自分の英語ページへのリンクの貼り方」と「変更の連絡先」を置いた（被リンクの入口）
- **やっていないこと**：IndexNow の鍵ファイル設置（自動判定で止められたため未実施。わたるさんの判断待ち）、Search Console でのサイトマップ再送信（わたるさんのアカウント操作のため）

## 8. 残っている穴（COWORKMILL・2026-10-11 夕方時点）

- 料金が無い施設 44件（法人向けで公式に料金を出していないところが中心：JustCo、PORTAL POINT など）
- 営業時間が無い施設 20件（本文にある公式の時間を visit_extra.json に移して29件→20件）
- 予約・支払い・英語の情報が無い施設 16件（公式サイトの中身が読めない／記載が無い）
- 車いす対応：調べた公式サイトのどこにも記載が無かった（記載が出てきたら `visit_extra.json` に `Access` 項目を足す）
- 地方：札幌・那覇・京都はまだ1〜2件。見送り候補と理由は cowork_facilities.py の 2026-10-11 の見出しに記録

## 9. CAFEMILL へ移した記録（2026-10-11）

- 同じ部品（build_en.py・map_en.py・lang_hubs.py・freshness.py・audit_en.py）を cafemill/_src に移植。297店・特集50・Q&A18・探し方ページ（朝早い・夜遅い・建築家・テラス・Wi-Fi・駅）と地域9つ
- 掲載プランや特商法が無いサイトなので、「掲載依頼」の代わりに `about/suggest-a-cafe.html`（お問い合わせフォームへ）を置いた
- 店の特徴は営業時間（8時までに開く／21時以降まで）・設計者の記載・設備から自動で付ける。正規表現は誤判定（「テラスを見下ろす」「ホットドッグ」など）が出るので `_XAM`・`_NOAM` で除外
- 旧URL（日本語版の店・特集・about など）は vercel.json の redirects で新ページへ。**既にある同じ source の規則が先に効く**ので、追加ではなく既存の行の行き先を書き換えること
- 地図：住所が県・市までしか無い店33件と、地理院の結果があいまいな3件は地図に載せていない（261/297）
- 残り：`visit_extra.json`（支払い・予約・英語メニュー）は未調査で空
- 2026-10-11 追記：人気上位50店＋スタバ22店・ブルーボトル21店の支払い・英語メニュー・予約・Wi-Fi を公式ページから `visit_extra.json` に入れた（54店）。**チェーンは同じドメインの店舗ページを、そのドメインを開いたタブの中から fetch＋DOMParser で読むと1回で全店取れる**（スタバは `.payment-method__item img` の alt、ブルーボトルは「メニュー|Menu」の言語リンク）。独立店の多くは公式サイトに支払い方法を書いていない。WebFetch はこの日、会話に出ていないURLを開けなかった
- 英語メニューの判定は「English に menu の語がある」ときだけ（サイトの英語版があるだけではメニューとみなさない）。`find/english-menu.html` を追加
