# セキュリティ対策 進捗

## ✅ Phase 1 完了(2026-04-29): voices テーブル保護

レビュー(利用者の声)の承認・拒否・削除を JWT 認証付き Edge Function 経由に。

## ✅ Phase 2 完了(2026-04-29): spaces / space_images 保護

施設情報・施設写真の write 操作を全て JWT 認証付き Edge Function 経由に。

### Edge Function `cwm-admin` の網羅範囲

| target | actions |
|--------|---------|
| `voice` | approve, reject, delete |
| `space` | insert, update, delete |
| `space_image` | insert, update, delete |

### 各 action の処理

1. **JWT verify** (HMAC-SHA256, CWM_JWT_SECRET)
2. **アカウント有効性チェック** (status='active')
3. **Ownership check**:
   - voice: 対象 voice の space → space.account_id == requester
   - space (update/delete): space.account_id == requester
   - space (insert): data の account_id をリクエスタ強制セット(改ざん防止)
   - space_image (update/delete): image.space_id → space.account_id == requester
   - space_image (insert): data.space_id → space.account_id == requester
4. **Service_role で実行**
5. **id / account_id の改ざん防止**: incoming data から自動削除

### admin-view.html 側の実装

`sbFetch(path, options)` ヘルパーが path をパースして自動的に Edge Function に振り分け:

| パス | メソッド | ルーティング先 |
|------|----------|----------------|
| `/rest/v1/spaces?id=eq.<uuid>` | PATCH/DELETE | space.update / space.delete |
| `/rest/v1/spaces` | POST | space.insert |
| `/rest/v1/space_images?id=eq.<uuid>` | PATCH/DELETE | space_image.update / space_image.delete |
| `/rest/v1/space_images` | POST | space_image.insert |

既存の admin-view.html の write 呼び出し(全 24 箇所)は変更不要 — sbFetch 経由なので自動的に保護対象に。

### voices RLS 状態
- RLS: 有効
- anon ポリシー: SELECT, INSERT のみ(投稿フォームと公開表示用)
- UPDATE/DELETE: anon 不可 → Edge Function (service_role) のみ可能

### 攻撃耐性(検証済み)

| 攻撃シナリオ | 結果 |
|-------------|------|
| publishable key で voice を直接削除 | ✅ RLS で拒否(0行更新) |
| publishable key で他人の space を改ざん | ✅ RLS / ポリシーで拒否 |
| 他人の cwm_token を入手して操作 | ✅ JWT verify は通るが ownership check で 403 |
| 他人の施設の voice を、自分のアカウントから操作 | ✅ ownership check で 403 |
| 期限切れ JWT で操作 | ✅ 401(自動的にリロード+再ログイン誘導) |
| 改ざん JWT で操作 | ✅ HMAC-SHA256 検証で 401 |
| insert で account_id を他人に偽装 | ✅ Edge Function が requester のIDで強制上書き |
| update で id/account_id を改ざん | ✅ Edge Function が data から自動削除 |

## 残タスク

### Phase 3: architects テーブル保護(後日)
建築家情報の write も Edge Function 経由化。少数の操作なので軽量。

### Phase 4: admin-ops.html(運営者画面)保護(後日)
運営者(白木さん)が使う画面。**別権限レベル(super admin)が必要**:
- accounts テーブルの管理(他人のアカウント操作)
- 全 spaces の管理(全テナント)
- ~10箇所の write 操作

実装方針: cwm-admin に `is_super_admin: boolean` フィールド or 別 Edge Function `cwm-ops` を作る。

### Phase 5: 監査ログ・レート制限
- cwm-admin 内で操作ログを別テーブルに記録
- 連続呼び出しを制限(brute force 対策)
- 異常パターン検知

## 補足

- CWM_JWT_SECRET, SUPABASE_SERVICE_ROLE_KEY は Edge Function の環境変数として管理(漏洩リスク低)
- service_role key は Edge Function 内のみで使用、ブラウザに出ない
- cwm_token は localStorage 保存、有効期限あり(cwm-auth で発行時に exp 設定)
