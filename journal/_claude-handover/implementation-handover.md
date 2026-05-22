# COWORKMILL 実装引き継ぎ書 — 詳細ページ・管理画面の本実装

作成: 2026-05-22 ／ 対象: Claude Code（ターミナルからの実装作業）

## 0. この文書の位置づけ

施設詳細ページと施設管理画面を、FIX 済みの新デザインへ本実装するための指示書。
設計・DB はすべて確定済み。この文書だけで実装に着手できることを目指す。

## 1. 設計の正解（プロトタイプ）

新デザインの確定版は次の3つのプロトタイプ HTML。チャットで納品済み・リポジトリ未配置のため、
実装前に作業者へ渡すこと（またはリポジトリに配置する）。

- coworkmill-detail-prototype.html       — 施設詳細ページ
- coworkmill-admin-edit-prototype.html   — 管理画面「施設情報の編集」
- coworkmill-admin-photos-prototype.html — 管理画面「写真管理」

見た目・構成・CSS・セクション順がすべて FIX。実装はこの通りに行う。
プロトタイプはダミーデータ（架空施設「KUROGANE 蔵前」）で作成。実装ではダミーを外し
Supabase 実データへ接続する。入力欄はすべて例示プレースホルダーで作ってある。

## 2. Supabase（本番DB）

project ref: jakwntemjkwqwaqujffh
主要テーブル: spaces / space_images / space_tags / tags / voices / architects / articles / reviews

### 今回追加済みの列（適用済み）
- spaces.plans (jsonb)          — 提供プラン・料金セクション一式
- space_tags.description (text) — 特徴ごとのひとこと説明
- space_images.caption (text)   — 写真ごとのキャプション

### spaces の主な既存列（実装で使用）
name, slug, status, area, region_area, prefecture, address, nearest_station,
nearest_line, walk_minutes, open_hours, description, image_main, images(array),
price_dropin_hour, price_dropin_day, price_monthly_amount, price_monthly_max,
price_note, has_meeting_room, meeting_capacity, architect_id, architect_name,
architect_firm, designer_name, designer_url, design_year, architect_comment,
photographer_name, photographer_url, latitude, longitude, official_url,
contact_url, instagram, youtube_url, youtube_video_id, award, is_pick,
is_verified, coworkmill_note, plan, logo_url, smoking,
features(array), facilities(array), workstyle_tags(array)

### space_images
id, space_id, url, display_order, caption, created_at
→ 写真。display_order 昇順、先頭がメイン写真。

### space_tags
id, space_id, tag_id, photo_url, description, created_at
→ 施設×特徴タグの紐付け。photo_url=特徴ごとの写真、description=特徴ごとの説明。

### tags
id, key, name, type, tag_group, requires_photo, show_on_shelf, shelf_title, shelf_min_count, sort_order
→ 特徴タグの定義。

### spaces.plans (jsonb) の構造
管理画面が書き込み、詳細ページが読み取る。トップレベルのキー:
- dropin    : on（提供有無）, hour（時間料金）, day（1日料金）
- freedesk  : on, monthly（月額）, note（補足）
- dedicated : on, monthly, note
- private   : on, monthly, note
- initial_fee      : 入会金・初期費用
- meeting_room_fee : 会議室利用料（時間あたり）
- note             : その他・料金の補足
on が true のプランのみ詳細ページに表示する。

## 3. detail.html の実装

### 現状
本番 detail.html は約415KB・実装済み。データ層あり:
loadSpace / sbFetch（Supabase REST ラッパ）/ renderPlanCards / renderBlock /
lVoices / showMap / loadSameStationSpaces ほか計42関数。?id / ?slug で施設特定。

### 方針
プロトタイプ coworkmill-detail-prototype.html の見た目・構成・CSS を新 detail.html の
土台とし、現行 detail.html のデータ取得ロジック（sbFetch の Supabase 接続方法・取得項目）を
移植する。現行の動作（声の投稿・地図・お気に入り・関連施設）は維持する。

### セクション対応表（プロトタイプ全14ブロック → データ）
1  パンくず        : area / prefecture
2  ギャラリー      : space_images（display_order順・先頭メイン）。caption は alt 等に
3  施設見出し      : name / area / nearest_station / 特徴タグ(space_tags+tags)
4  この施設について : description
5  この施設の特徴   : space_tags(photo_url, description) + tags.name。写真+特徴名+説明。
                    写真や説明が無い特徴は該当部分を省略
6  設計した建築家   : architect_name / architect_firm / designer_url /
                    architect_comment（建築家から一言の引用）。comment 空なら引用は非表示
7  動画〔有料〕     : youtube_url / youtube_video_id。有料プラン かつ 値ありで表示
8  仕事タイプ投票   : 既存 voices 投票ロジックを流用
9  利用者の声      : voices
10 運営より一言    : coworkmill_note。空なら非表示
11 施設情報＋送客   : 住所 / 地図(latitude,longitude) / open_hours / 料金(plans)。
                    official_url・contact_url は〔有料〕
12 特集棚掲載      : show_on_shelf のタグ
13 同じ建築家      : architect_id 一致の他施設
14 次の一軒へ      : 関連施設

### 無料 / 有料の出し分け
spaces.plan で判定。有料項目=動画・公式/問い合わせ送客リンク・写真4枚目以降。
無料でもページは美しく保つ。建築家から一言は全プラン表示。

### 実装段階の詰め
- 空状態: データの無いセクションは非表示（ページが欠けて見えないように）
- 読み込み中表示・404（該当施設なし）
- proto-bar / プレビュー切替バーは本番では除去

## 4. 管理画面の実装

### 現状
cowkml.com/admin は多ページのライトテーマ管理画面（アナリティクス / 施設情報の編集 /
写真管理 / 利用者の声 / 建築家情報 / 企業情報 / 掲載ステータス / プラン管理）。
現行を活かして更新する。

### 施設情報の編集（coworkmill-admin-edit-prototype.html 準拠）
- 基本情報        : name / prefecture / region_area(市区町村) / address / nearest_station / open_hours / latitude / longitude
- 提供プラン・料金 : plans(jsonb)。4プラン種別の on+料金+補足、入会金、会議室利用料、補足
- 施設紹介文      : description
- 写真           : space_images（編集は写真管理ページ）
- 設計者・建築家   : designer_name / designer_url / architect_comment（建築家から一言・入力ガイド付き）
- 受賞歴         : award（施設側の自由入力。COWORKMILL の事前チェック無し）
- 特徴タグ       : space_tags / tags（自由入力＝新規タグ追加も可）
- 設備・サービス   : facilities
- 公式リンク・SNS〔有料〕 : instagram / official_url / contact_url
- 紹介動画〔有料〕 : youtube_url
- COWORKMILL設定〔読取専用〕: is_verified / is_pick / coworkmill_note
- 掲載状態       : status

### 写真管理（coworkmill-admin-photos-prototype.html 準拠）
- 写真グリッド: space_images。アップロード、ドラッグで display_order 変更、
  先頭=メイン、削除、caption 入力。無料3枚/有料無制限（plan で判定）
- 特徴ごとの写真と説明: space_tags。施設の各特徴タグごとに photo_url
  （アップロード済み写真から選択）と description（ひとこと説明）を設定。
  TOP の特集棚・詳細ページの「この施設の特徴」で共通利用

## 5. このセッションで確定した重要判断

- 「設計の読みどころ（光・素材・空間）」は廃止。運営者には抽象的すぎるため。
  代わりに「建築家から一言」(architect_comment)。運営者が建築家本人に直接たずねて
  言葉をもらい貼り付ける。連絡先（個人情報）は扱わない。建築家サイト URL(designer_url)
  経由で COWORKMILL がつながる。掲載前の COWORKMILL 確認は無し。
- 受賞歴は施設側の自由入力。事実ベース前提・COWORKMILL の事前チェック無し。
  問題があれば公開後に運営がコメントする。
- 提供プランは選択式（ドロップイン / フリーデスク / 専用デスク / 個室）。各々に説明文。
  施設が提供するものを選び、料金を入力する。
- 特徴ごとに写真＋ひとこと説明。TOP 特集棚・詳細ページの特徴セクションで共通利用。
- 特徴タグに自由入力（その他）あり。
- 入力欄はすべて例示プレースホルダー。実在名は入れない。

## 6. 推奨作業順序

1. detail.html: プロトタイプを土台に Supabase 接続を移植 → ?id/?slug で実データ表示 → 空状態・読み込み中・404
2. 管理画面「施設情報の編集」: 新セクション反映、plans(jsonb) の読み書き
3. 管理画面「写真管理」: 特徴ごとの写真と説明、space_images の caption / display_order
4. TOP・一覧ページ（確定済み TOP 構成 coworkmill-top-prototype.html）
5. ダミー施設投入 → サンプルサイト化 → 段階公開

各段階でローカル確認 → cowkml.com（Vercel・main へ push で自動デプロイ）へ反映。
本番反映前に必ず動作確認すること。
