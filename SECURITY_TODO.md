# セキュリティ対策 進捗

## 完了済み(2026-04-29)

### Phase 1: voices テーブル(利用者の声)完全保護 ✅

**Edge Function `cwm-admin` をデプロイ**して、admin の write 操作(承認/削除)を JWT 認証付きバックエンド経由に切り替え。

実装内容:
- 新規 Edge Function `cwm-admin` 作成・デプロイ
  - URL: `https://jakwntemjkwqwaqujffh.supabase.co/functions/v1/cwm-admin`
  - cwm_token (HMAC-SHA256 署名 JWT) を verify
  - account.status 有効性チェック
  - target='voice' の場合: 対象 voice の space_id がリクエスタの所有か確認
  - 一致したら service_role で update/delete 実行
- admin-view.html の `approveVoice` / `deleteVoice` を Edge Function 経由に書き換え
- voices テーブルの RLS を**再有効化**
- 既存ポリシー: `voices_anon_insert`(投稿フォーム用)、`voices_public_select`(公開表示用)
- UPDATE/DELETE は anon ポリシー無し → 完全拒否

**動作検証(2026-04-29)**:
- ✅ publishable key で直接 PATCH → HTTP 200 だが body=`[]`(0行更新)、データは保護される
- ✅ admin 画面の「承認して公開」「削除」ボタン → Edge Function 経由で動く
- ✅ JWT 検証エラー時はユーザーに「再ログインしてください」アラート + リロード
- ✅ 他人の施設の voice を操作しようとした場合は 403 拒否

## 残タスク

### Phase 2: spaces テーブル(施設情報)保護
spaces の UPDATE/DELETE 操作も同様に cwm-admin 経由化する。
- admin-view.html の施設情報更新処理を Edge Function 経由に
- cwm-admin に target='space' のロジック追加
  - space.account_id がリクエスタと一致するか確認
- spaces RLS は既に anon UPDATE policy 無し(現状維持で OK)

### Phase 3: architects, space_images
同パターンで保護。

### Phase 4: 監査ログ・レート制限
- cwm-admin 内で操作ログを別テーブルに記録
- 連続呼び出しを制限(brute force 対策)

## 補足: 攻撃シナリオへの耐性

| 攻撃 | 結果 |
|------|------|
| publishable key で voices を勝手に削除 | RLS で拒否(検証済み) |
| publishable key で他人の voice を承認 | RLS で拒否(検証済み) |
| 他人の cwm_token を入手して操作 | JWT verify で別人と判明、ownership check で 403 |
| 他人の施設の voice を、自分のアカウントから操作 | ownership check で 403 |
| 期限切れ JWT で操作 | JWT verify で 401(自動的にリロード+再ログイン) |
| 改ざん JWT で操作 | HMAC-SHA256 検証で 401 |

## メモ

- CWM_JWT_SECRET は Supabase Edge Function の環境変数として管理(漏洩リスクなし)
- service_role key は Edge Function 内のみで使用、ブラウザに出ない
- cwm_token は localStorage 保存、有効期限あり(cwm-auth で発行時に exp 設定)
