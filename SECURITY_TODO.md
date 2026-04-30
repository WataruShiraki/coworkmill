# COWORKMILL セキュリティ状況

最終更新: 2026-04-30(段階A 完了)

## ✅ Phase 1 完了(2026-04-29): voices テーブル保護
- voices に対する write は cwm-admin Edge Function 経由のみ
- anon キー直接 INSERT/UPDATE/DELETE 不可
- approve / reject / delete アクションで ownership チェック(空間オーナー以外は 403)

## ✅ Phase 2 完了(2026-04-29): spaces / space_images 保護
- spaces.insert/update/delete を Edge Function 経由化
- space_images.insert/update/delete を Edge Function 経由化
- account_id/id の改ざん防止(server 側で必ず置換 or 削除)
- 新規 space は requestor の plan を継承(client 側からの plan 注入を防止)

## ✅ Phase 3 完了(2026-04-30): architects テーブル保護
- architect.insert/update/delete を Edge Function 経由化
- 入力バリデーション: 名前 1〜100 文字、URL 500 文字以内、contact_status はホワイトリスト(pending/contacted/approved/declined)
- architects テーブル RLS 強化(anon SELECT のみ、write は service_role 経由のみ)
- 動作検証済み: anon 直接 INSERT は 401 + RLS policy violation で拒否される

## ✅ Phase 5 完了(2026-04-30): 監査ログ・レート制限
- audit_logs テーブルを新設(account_id / target / action / record_id / status / detail / ip / created_at)
- すべての write 試行(ok / denied / error)が記録される
- RLS は USING(false) で anon/auth はアクセス不可、service_role(Edge Function)経由のみ
- 3 つのインデックスで「アカウント別最新」「target+action 別」「非ok のみ」のクエリを高速化
- レート制限: account_id × target × action あたり 60 秒で 30 リクエスト(in-memory sliding window)
- 超過時は 429 を返却
- 動作検証済み: architect.insert を試した結果が audit_logs に正しく記録され、IP も含まれた

## ✅ XSS 対策(2026-04-30)
すべての公開ページの innerHTML を cwm.esc / cwm.escAttr / cwm.safeUrl / cwm.escMultiline で wrap 済み。

| ファイル | 対応箇所数 | 主なコミット |
|---|---|---|
| coworkmill-detail.html | 23 | 8cb7378, d985434, b7dba19, d9ad7a0, a783af1 |
| coworkmill.html (TOP) | 9 | 701b5da, e86afdd |
| coworkmill-spaces.html | 7 | b87a329 |
| coworkmill-architects.html | 11 | 528b0cd |
| coworkmill-photos.html | 6 | eb5f0e0 |
| coworkmill-favorites.html | 6 | 6b3208b |

shared/cwm-security.js が以下を提供:
- cwm.esc(s): &/</>/"/' を HTML エンティティに変換
- cwm.escAttr(s): cwm.esc と同等(属性値用エイリアス)
- cwm.safeUrl(s): javascript:/data:/vbscript:/file: スキームを拒否してから esc
- cwm.escMultiline(s): cwm.esc + 改行を <br> に変換

## ✅ HTTP セキュリティヘッダ(vercel.json)
- Content-Security-Policy(unsafe-inline は当面残す。将来削除予定)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: camera=()/microphone=()/geolocation=(self)/interest-cohort=()
- X-XSS-Protection
- HSTS は DNS 設定後に追加予定(現時点で cowkml.com は未接続)

## 🟡 Phase 4(後日): admin-ops 保護(super admin)
運営者(白木さん本人)が使う画面。別権限レベルが必要:
- accounts テーブルの管理(他人のアカウント操作)
- 全 spaces の管理(全テナント横断)
- ~10 箇所の write 操作

実装方針: cwm-admin に `is_super_admin: boolean` フィールド or 別 Edge Function `cwm-ops` を作る。
現状: 運営者 1 人だけなのでローンチ後に対応する。

## 🟡 残タスク(優先度順)

### 高優先(ローンチ直前)
1. **入力バリデーション強化(フロント側)**
   - 登録フォーム / お問い合わせフォームの URL 正規表現 / 文字数上限
   - workstyle 投稿の長さ制限(現状 server 側で nullable のため)

2. **CSP の unsafe-inline 削除**
   - 残存するインライン script / style を外部化
   - nonce ベース CSP に切り替え

### 中優先(ローンチ後すぐ)
3. **audit_logs を admin-view から見られるように**
   - 現在 service_role のみ閲覧可
   - JWT 経由で自分のアカウント分だけ表示する Edge Function を追加(`cwm-admin` に audit.list を追加)

4. **レート制限の永続化**
   - 現状 in-memory(Edge Function instance ごと)
   - 強化版: Supabase の rate_limit テーブル + Postgres function に移行
   - もしくは Cloudflare Workers KV 等の外部ストレージ

### 低優先(将来)
5. **Phase 4: admin-ops 保護**(super admin 権限導入)
6. **画像アップロード時のウイルススキャン**(Storage hook)
7. **異常検知アラート**(audit_logs を定期 SELECT して slack 通知)

## 補足

### Edge Function 設定
- 関数名: cwm-admin
- URL: https://jakwntemjkwqwaqujffh.supabase.co/functions/v1/cwm-admin
- 環境変数: SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY / CWM_JWT_SECRET
- ソース: supabase/functions/cwm-admin/index.ts(repo と本番一致)

### ローンチ前必須(セキュリティ外の項目)
- DNS: お名前.com で nameserver を 01-04.dnsv.jp に変更 → cowkml.com を Vercel に向ける
- Stripe: Standard / Pro 用 Payment Link + Webhook で account.plan 更新
- Resend: 新規施設登録通知 / voice 投稿通知 / お問い合わせ転送
