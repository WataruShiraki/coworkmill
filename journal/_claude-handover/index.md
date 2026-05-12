# COWORKMILL Journal — Claude引き継ぎパック

> **最終更新**: 2026-05-12  
> **目的**: 新規チャットの Claude が瞬時に状況把握し、 航さんの「3ステップワークフロー」を実行できるようにする  
> **置き場所**: https://cowkml.com/journal/_claude-handover/index.md

---

## 0. 新規チャットの Claude へ（最重要）

**航さんは Lily Partners LLC を一人で運営しており、 COWORKMILL は本人の主力サービスです。 引き継ぎが面倒なため、 このパックを作りました。 まずこれを最後まで読んでから動いてください。**

### 航さんの理想ワークフロー（3ステップ・厳守）

| ステップ | 航さんがやること | Claude がやること |
|---|---|---|
| ① **テーマ提案** | YES / NO で答える | 既存記事と被らない次のテーマを **3案** 提示（タイトル・著者・想定施設数） |
| ② **施設候補** | Instagram URL を Claude に送る | 施設候補リストを提示（名前・エリア・想定の特徴） |
| ③ **記事化＆公開** | 完成記事を確認 | 完成 HTML を書く → GitHub push → cowkml.com に反映 |

### やってはいけないこと（過去の反省）

1. **30項目フォーム** のような中途半端なジェネレータを提案しない（本人が埋める手間が消えていない）
2. **Claude API in Artifacts** で従量課金を発生させる提案をしない（航さん拒否）
3. **既存シリーズ記事との不統一** な記事を書かない（CSS テーマ、 Instagram 組み込み形式、 必須セクション全部統一）
4. **要件確認なしの実装** をしない（必ず1〜2文で「機能の使い方」を言語化して認識合わせ）

### 対応スタイル（毎チャット必須）

- **敬語徹底**: 〜です、 〜ます、 〜でしょうか（「だ・である」「〜だね」NG）
- **謝罪表現**: 「申し訳ございません」（「すみません」NG）
- **了承表現**: 「承知いたしました」（「承知。」NG）
- **例え話**: 技術的説明には必ず中学生レベルの例えを添える
- **1ステップずつ**: ユーザー作業依頼は番号付き、 完全URL・クリック場所・ボタン見た目を明記
- **ファイル添付**: メッセージ末尾に毎回 `present_files` で最新版を再添付（「上を見て」NG）
- **要件確認**: 機能依頼を受けたら最初に「この機能をどう使うか」を1〜2文で言語化

---

## 1. 既存記事一覧（2026-05-12 時点）

| 公開日 | スラッグ | タイトル | 軸 | 著者 | 件数 |
|---|---|---|---|---|---|
| 2026-05-10 | `gotanda-design-coworking-2026` | 五反田駅から徒歩圏 デザインで選ぶコワーキング 4選 | デザイン | coffee-bucho | 4 |
| 2026-05-12 | `shimbashi-toranomon-coworking-2026` | 新橋エリア ビジネス街で選ぶコワーキング 6選 | ビジネス街・商談 | yoshiki-bucho | 6 |

**確認URL**:
- 五反田: https://cowkml.com/journal/gotanda-design-coworking-2026/
- 新橋: https://cowkml.com/journal/shimbashi-toranomon-coworking-2026/

---

## 2. 記者11人プロフィール

> **使い方**: 新記事の著者を選ぶときは、 テーマと記者の専門が一致するものを選ぶ。 既出記者（coffee-bucho, yoshiki-bucho）以外を優先するとシリーズに厚みが出る。

### 2-1. coffee-bucho — コーヒー部長 ✅ 既出

| 項目 | 値 |
|---|---|
| 名前 | コーヒー部長（Coffee Bucho） |
| 年齢 / 性別 | 32歳 / 男性 |
| 拠点 | 自由が丘 |
| 職業 | Webディレクター |
| 担当 | 東京（山手線・湾岸） |
| 専門 | 機能を体験で語る、 コーヒーと回線、 自転車派 |
| avatar | 珈 / color: `#C2785A` |
| 声の特徴 | 「まず一杯目を頼んでから席に着く」「机の高さ、 椅子の沈み、 Wi-Fiの安定、 レジ前の動線――体験の細部から街の輪郭を描く」 |
| 既出記事 | 五反田デザイン4選 |

### 2-2. yoshiki-bucho — ヨシキ部長 ✅ 既出

| 項目 | 値 |
|---|---|
| 名前 | ヨシキ部長（Yoshiki Bucho） |
| 年齢 / 性別 | 42歳 / 男性 |
| 拠点 | 港区 |
| 職業 | 元営業マネージャー / 現コンサルタント |
| 担当 | 商談・電話ブース・アクセス（全国） |
| 専門 | Zoom中の声漏れ、 商談前の身だしなみ |
| avatar | ヨ / color: `#5A6F8A` |
| 声の特徴 | 「Zoomの声漏れ、 鏡の有無、 ネクタイを直すスペース、 トイレの清潔感。 商談を本業にしてきた人間にしか書けない切り口で、 コワーキングを採点する」 |
| 既出記事 | 新橋ビジネス街6選 |

### 2-3. machiya-nanami — マチヤナナミ 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | マチヤナナミ（Machiya Nanami） |
| 年齢 / 性別 | 29歳 / 女性 |
| 拠点 | 京都 |
| 職業 | エディター（出版社で街と建築の特集を担当） |
| 担当 | 関西（京都・大阪・神戸・奈良） |
| 専門 | 街の歴史と文化、 町家リノベに敏感 |
| avatar | マ / color: `#B58B6E` |
| 声の特徴 | 「働く場所には、 その街の記憶が宿る」「町家を活かしたコワーキングや、 町並みに溶け込む新築の佇まいに目を細める」 |

### 2-4. haruking — ハルキング 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | ハルキング（Haruking） |
| 年齢 / 性別 | 38歳 / 男性 |
| 拠点 | 札幌 |
| 職業 | スタートアップPR |
| 担当 | 北海道・東北 |
| 専門 | 寒さ・日照・冬の通勤、 実用主義 |
| avatar | ハ / color: `#7BA8D9` |
| 声の特徴 | 「マイナス10度の通勤で鍛えられた実用主義者」「窓の大きさ、 暖房の効き、 雪解け後のラウンジの清潔感――北国でしか拾えない観点」 |

### 2-5. hakata-aniki — ハカタの兄貴 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | ハカタの兄貴（Hakata no Aniki） |
| 年齢 / 性別 | 35歳 / 男性 |
| 拠点 | 福岡 |
| 職業 | 映像クリエイター |
| 担当 | 九州・沖縄 |
| 専門 | 街のエネルギー、 食、 アジア距離感 |
| avatar | ハ / color: `#E47B4F` |
| 声の特徴 | 「コワーキング選びの基準は『飯と人と速度感』。 屋台帰りでも仕事できる空気感のある場所を、 迷わず推す」 |

### 2-6. aya-nee — 二拠点アヤ姉 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | 二拠点アヤ姉（Aya-nee） |
| 年齢 / 性別 | 31歳 / 女性 |
| 拠点 | 名古屋⇄東京 |
| 職業 | 広報 |
| 担当 | 中部・東海・北陸 |
| 専門 | 車通勤前提、 地方の働き方の変化 |
| avatar | 二 / color: `#9FB8A6` |
| 声の特徴 | 「駐車場の出入り、 車から机までの距離、 雨の日の動線――車社会のリアルな視点から地方コワーキングを語る」 |

### 2-7. wifi-mio — Wi-Fi番長ミオ 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | Wi-Fi番長ミオ（Wi-Fi Bancho Mio） |
| 年齢 / 性別 | 27歳 / 女性 |
| 拠点 | 恵比寿 |
| 職業 | 元エンジニア / 現PdM |
| 担当 | エンジニア向け・回線・モニタ（全国） |
| 専門 | 技術スペックを実測で語る、 絵文字なし硬め |
| avatar | W / color: `#6B7DA5` |
| 声の特徴 | 「必ずSpeedtestと、 モニタの色域、 コンセントの位置を測る。 文章には絵文字を使わない。 スペックで判断し、 感情は数字の後ろに置く」 |

### 2-8. touma-sensei — トウマ先生 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | トウマ先生（Touma Sensei） |
| 年齢 / 性別 | 45歳 / 男性 |
| 拠点 | 銀座 |
| 職業 | 税理士（開業20年） |
| 担当 | 士業・静音・長時間滞在（全国） |
| 専門 | お茶の質、 椅子の品、 空気の落ち着き |
| avatar | ト / color: `#8B7355` |
| 声の特徴 | 「お茶の品書き、 椅子の張地、 午後3時の空気の重さ――静かに長く滞在する人間にしか見えないものを、 丁寧に書く」 |

### 2-9. tokyo-sam — 東京サム Sam 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | 東京サム Sam（Tokyo Sam） |
| 年齢 / 性別 | 34歳 / 男性 |
| 拠点 | 東京（オーストラリア・メルボルン出身、 東京12年） |
| 職業 | バイリンガルライター |
| 担当 | 外国語対応・国際カンファレンス（全国） |
| 専門 | 英語スタッフの有無、 国際送金、 ビザ事情、 ハラル／ベジ対応 |
| avatar | 東 / color: `#6A9A8B` |
| 声の特徴 | 「受付の英語対応、 ベジ／ハラル対応、 ビザ書類の引き取り可否――海外から来る人が本当に困るポイントを、 当事者として書く」 |

### 2-10. shibui — シブイ渋井 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | シブイ渋井（Shibui） |
| 年齢 / 性別 | 66歳 / 男性 |
| 拠点 | 東京 |
| 職業 | 元雑誌編集長（文芸誌・建築誌 30年） / 現フリー |
| 担当 | 品ある運営・読書・落ち着き（全国） |
| 専門 | 椅子と照明、 本棚の有無、 運営者の振る舞い |
| avatar | シ / color: `#5C5C5C` |
| 声の特徴 | 「本棚の選書、 照明の温度、 運営者が客にかける一言――急がない人間にしか拾えない品格を、 淡々と記録する」 |

### 2-11. kinako — きなこ 🆕 未起用

| 項目 | 値 |
|---|---|
| 名前 | きなこ（Kinako） |
| 年齢 / 性別 | 21歳 / 女性 |
| 拠点 | 東京（都内私大3年） |
| 職業 | Z世代インターン |
| 担当 | 学生・SNS映え・カジュアル（全国） |
| 専門 | TikTokっぽさ、 ドリンクバー、 友達と作業、 「これから」目線 |
| avatar | き / color: `#E8A0BF` |
| 声の特徴 | 「ドリンクバーの種類、 撮りやすい壁、 友達と並んで作業できる席――『学生でも入れる場所』『これから働く人の場所』の視点で書く」 |

---

## 3. 次の記事候補リスト（提案待ち）

> **使い方**: 新規チャットで Claude が記事を提案するときは、 このリストから3案ピックアップする。 航さんが YES と言ったテーマを進める。 既に記事化したら、 このリストから削除して引き継ぎパックを更新する。

| # | 想定タイトル | 著者 | エリア / テーマ | 想定件数 |
|---|---|---|---|---|
| 1 | 京都・町家リノベで選ぶコワーキング 5選 | machiya-nanami | 京都・街の記憶 | 5 |
| 2 | 札幌 雪国の通勤に頼れるコワーキング 5選 | haruking | 札幌・冬の実用 | 5 |
| 3 | 福岡 屋台帰りでも仕事できるコワーキング 5選 | hakata-aniki | 福岡・熱量と速度感 | 5 |
| 4 | 名古屋 駐車場で選ぶ二拠点ワーカー向け 5選 | aya-nee | 名古屋・車社会 | 5 |
| 5 | エンジニアが Speedtest で選ぶコワーキング 6選 | wifi-mio | 全国・回線スペック | 6 |
| 6 | 士業が長時間こもれる静音コワーキング 5選 | touma-sensei | 銀座・霞が関・士業街 | 5 |
| 7 | 国際カンファレンス参加者のためのコワーキング 5選 | tokyo-sam | 東京・英語対応 | 5 |
| 8 | 読書と仕事のあいだに本棚があるコワーキング 5選 | shibui | 全国・品ある運営 | 5 |
| 9 | Z世代の学生インターンが選ぶカジュアルコワーキング 5選 | kinako | 全国・SNS映え | 5 |
| 10 | 大阪・梅田 通勤30分圏のコワーキング 5選 | machiya-nanami | 大阪・梅田周辺 | 5 |
| 11 | 横浜・みなとみらいで選ぶ景色のいいコワーキング 5選 | coffee-bucho | 横浜・湾岸 | 5 |
| 12 | 渋谷 デジタル系企業の常連が使うコワーキング 6選 | coffee-bucho | 渋谷・IT | 6 |

---

## 4. スタイル要件（既存シリーズ記事との完全統一が必須）

> **重要**: 新記事を書く前に、 必ず五反田記事と新橋記事の HTML を web_fetch で読んで、 構造・CSS・JSON-LD を完全に踏襲してください。 統一感欠如は航さんが最も嫌う失敗です。

### 4-1. ダークモード必須（CSS変数）

```css
:root{
  --bg:#121212; --bg-2:#1a1a1a; --bg-3:#222; --bg-4:#2a2a2a;
  --fg:#f0f0f0; --fg-2:#ccc; --fg-3:#999; --fg-4:#666;
  --line:#2a2a2a; --line-2:#333;
  --teal:#79F1A4; --teal-2:#2BB5C8; --rust:#A0533C;
  --fb:'Cormorant Garamond',serif;
  --fd:'Noto Sans JP',-apple-system,BlinkMacSystemFont,sans-serif;
}
```

### 4-2. フォント（Google Fonts 必須）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Noto+Sans+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 4-3. 必須セクション（記事HTMLの構造、 順序厳守）

1. `<header class="j-nav">` — ヘッダーナビ
2. `<article class="j-article">`
   1. `.j-article-eyebrow`（カテゴリ・公開日・読了時間）
   2. `.j-article-title`（h1）
   3. `.j-article-meta`（著者リンク・担当・タグ）
   4. `.j-hero-img`（**インラインSVG** ※直リンク画像 NG）
   5. `.j-article-body`
      - `.j-lead`（リード文・1段落）
      - 導入の追加段落 1〜2 個
      - `.j-pullquote`（オープニングキャッチ）
      - **施設ブロック × N**（h2 + 本文3段落 + IG embed + j-info-box）
      - `.j-mid-cta`（任意・中盤誘導）
      - Conclusion h2 + 本文
      - `.j-pullquote`（クロージングキャッチ）
   6. `.j-writer-card`（著者プロフィール・記者ページへのリンク）
   7. `.j-end-cta`（**COWORKMILL誘導CTA・必須**）
   8. `.j-related`（関連記事リンク）
3. `<footer class="j-foot">`（フッター）
4. `<script async src="//www.instagram.com/embed.js">`（最後に必須）

### 4-4. Instagram 組み込み（**公式 oEmbed のみ、 直リンク画像は禁止**）

```html
<div class="j-ig-embed-wrap">
  <blockquote class="instagram-media"
    data-instgrm-permalink="https://www.instagram.com/p/POSTID/?img_index=1"
    data-instgrm-version="14"
    style="background:#FFF; border:0; border-radius:6px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5); margin:0; max-width:540px; min-width:326px; width:100%; padding:0;"></blockquote>
</div>
<div class="j-ig-caption">via @handle on Instagram</div>
```

### 4-5. Hero SVG 構造

インライン SVG（jpg/png/webp 直リンク禁止）。 ダーク背景にラジアルグラデ、 巨大ローマ字、 漢字サブ、 英語タグライン、 著者クレジット、 No. の構成。 五反田・新橋記事のSVGをそのままコピーして文字だけ差し替えるのが最速。

### 4-6. JSON-LD（SEO 必須）

`Article` schema を `<script type="application/ld+json">` で記事末尾に埋める。 五反田・新橋記事をコピーして slug・title・date・author だけ差し替え。

### 4-7. OGP / Twitter Card / canonical（必須）

`og:title`, `og:description`, `og:image`, `og:url`, `twitter:card=summary_large_image`, `<link rel="canonical">` を全て記事ヘッダに含める。

---

## 5. 技術情報

### 5-1. インフラ

| 項目 | 値 |
|---|---|
| 本番URL | https://cowkml.com |
| Vercel URL | https://coworkmill.vercel.app |
| GitHub Repo | https://github.com/WataruShiraki/coworkmill |
| Supabase Project | https://supabase.com/dashboard/project/jakwntemjkwqwaqujffh/ |
| Supabase URL | https://jakwntemjkwqwaqujffh.supabase.co |
| Supabase publishable key | `sb_publishable_bQ84WCmRiFUbpPemMcO9xQ_Dj9Mh1mQ` |
| GA4 ID | `G-P6CZCM6K18` |

### 5-2. GitHub PAT 発行手順（30日有効、 都度発行）

新記事を push するときは、 航さんに PAT 発行をお願いします。 記憶しないルール（航さん指示）のため、 都度貼り付けてもらいます。

1. https://github.com/settings/personal-access-tokens/new にアクセス
2. Token name: `COWORKMILL deploy`
3. Expiration: `30 days`
4. Repository access: `Only select repositories` → `WataruShiraki/coworkmill`
5. Repository permissions → Contents: `Read and write`
6. 緑色「Generate token」ボタン押下
7. `github_pat_...` を Claude に貼り付け

### 5-3. push の実装（bash）

```bash
export GH_PAT="github_pat_..."
cd /home/claude/coworkmill
# ファイルコピー
cp /mnt/user-data/outputs/journal/[slug]/index.html journal/[slug]/index.html
cp /mnt/user-data/outputs/articles.json journal/articles.json
cp /mnt/user-data/outputs/writers.json journal/writers.json
# commit + push
git add -A
git commit -m "[コミットメッセージ]"
git push "https://x-access-token:${GH_PAT}@github.com/WataruShiraki/coworkmill.git" main
```

### 5-4. 既存ファイル構成

```
/journal/
  ├ index.html                       # journal トップ
  ├ articles.json                    # 記事メタデータ
  ├ writers.json                     # 記者プロフィール
  ├ sitemap.xml
  ├ _claude-handover/
  │   └ index.md                     # ← このファイル
  ├ gotanda-design-coworking-2026/
  │   ├ index.html
  │   └ og-image.svg
  ├ shimbashi-toranomon-coworking-2026/
  │   ├ index.html
  │   └ og-image.svg
  └ writers/
      ├ index.html
      ├ coffee-bucho/index.html
      └ ... (各記者ページ ※ヨシキ部長は未作成・要対応)
```

### 5-5. 未対応の残課題（次のチャットで対応推奨）

- [ ] ヨシキ部長プロフィールページ `/journal/writers/yoshiki-bucho/index.html` 未作成（既存 coffee-bucho ページをベースに10分で作れる）
- [ ] 五反田記事のタイトルが articles.json 上「4選」になっているが、 writer.json では「5選」と表記揺れ。 統一が必要
- [ ] Stripe 決済の正式導入（試し導入の状態を再確認 → Edge Function / Webhook / Price ID / テスト⇄本番）
- [ ] SNS準備（Buffer 無料プラン 3チャンネル、 Instagram / X / Pinterest）
- [ ] 営業メール送信、 営業リスト管理

---

## 6. 新規チャット用・標準プロンプト

新しいチャットを開いたとき、 航さんは以下のどれかを貼り付ければ Claude が瞬時に動きます。

### 6-1. 「次の記事を提案して」モード

```
COWORKMILL journal の引き継ぎパック
https://cowkml.com/journal/_claude-handover/index.md
を最初に読んでください。 読み終わったら、 「次の記事候補リスト」から3案を選んで、 私に提示してください。 私がYES/NOで答えます。
```

### 6-2. 「今すぐ記事を書きたい」モード

```
COWORKMILL journal の引き継ぎパック
https://cowkml.com/journal/_claude-handover/index.md
を最初に読んでください。 そのあと、 [テーマ名] の記事を [著者slug] で書いてください。 まず施設候補を5〜6個リストアップしてください。 私がインスタURLを送ります。
```

### 6-3. 「ヨシキ部長プロフィールページ作成」など個別タスク

```
COWORKMILL journal の引き継ぎパック
https://cowkml.com/journal/_claude-handover/index.md
を読んでから、 ヨシキ部長プロフィールページ /journal/writers/yoshiki-bucho/index.html を作成してください。 既存の coffee-bucho ページをベースにしてください。
```

---

## 7. このパックの更新ルール

新しい記事を公開したら、 必ずこのパックを更新してください：

1. **「1. 既存記事一覧」** にエントリ追加
2. **「3. 次の記事候補リスト」** から該当エントリを削除
3. 記者の `articles` フィールド（writers.json）も更新
4. 更新日（ファイル冒頭）を変更
5. このパック自体を GitHub に push

---

*— 編集: Claude (Anthropic)、 監修: 航 (Lily Partners, Inc.)*
