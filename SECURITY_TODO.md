# セキュリティ対策 TODO

## 現状(2026-04-29 時点)

開発を高速化するため、複数の Supabase テーブルで RLS(Row Level Security)が
無効化されている、または UPDATE/DELETE が `anon` キーに対して開放された状態。

### RLS無効化済みテーブル
- `voices`(2026-04-29 無効化、admin の承認/削除を動かすため)

### RLS有効だが UPDATE/DELETE が anon に開いてないテーブル
- `spaces`(SELECT/INSERT のみ anon 許可、UPDATE は service_role 経由?)
- `architects`
- `accounts`
- `registrations`
- `space_images`
- `reviews`(投稿用)
- `click_logs`

## 起こりうる攻撃シナリオ(本番化後)

1. **誰かが開発者ツールを開く** → サイトのHTMLに埋め込まれた `sb_publishable_*` キーを取得
2. そのキーで Supabase REST API を直接叩く
3. RLS無効テーブル(voices)に対して、誰でも以下が可能になる:
   - 全件SELECT(問題なし、元から公開情報)
   - 任意レコードのUPDATE(reviewの本文書き換え、なりすまし、sql injectionは無理だが意味的破壊が可能)
   - 任意レコードのDELETE(嫌がらせ的全消し)

## 推奨対策

### 短期(MVP公開直後〜利用者100人ごろまで)
- voices テーブルにRLSを再有効化
- ポリシー追加:
  - `voices_anon_insert` (公開フォーム用、既にある)
  - `voices_public_select` (公開表示用、既にある)
  - **新規**: 認証済みユーザーが**自分の施設の**voicesのみUPDATE/DELETEできるポリシー
    ```sql
    CREATE POLICY voices_owner_update ON voices
      FOR UPDATE TO authenticated
      USING (space_id IN (SELECT id FROM spaces WHERE owner_id = auth.uid()));
    CREATE POLICY voices_owner_delete ON voices
      FOR DELETE TO authenticated
      USING (space_id IN (SELECT id FROM spaces WHERE owner_id = auth.uid()));
    ```

### 中期(認証導入時に必須)
- admin-view.html に Supabase Auth (email/password または magic link) を導入
- ログイン後、`auth.uid()` を使ったRLSポリシーで施設オーナー単位でアクセス制御
- spaces, architects, voices, space_images すべてに owner ベースのRLS
- 公開キー(sb_publishable_*)はSELECTのみで write には使えない構成にする

### 長期
- service_role キーが必要な処理はサーバーレス関数(Supabase Edge Functions)経由に移行
- 公開キーはブラウザに置いてもOK、書き込み系は全てログイン+RLSで保護

## 補足

現在のサイトは利用者が極めて少ないため、上記対策は急ぎではない。
ただし、コワーキング業界でちょっと話題になった瞬間、悪意ある操作を受ける可能性は十分ある。
**「お問い合わせ」「掲載申し込み」が日に5件以上来るようになったら本気で対策する**を目安に。
