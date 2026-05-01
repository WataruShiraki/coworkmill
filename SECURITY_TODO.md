# COWORKMILL セキュリティ状況

最終更新: 2026-05-01(段階B 完了)

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

## ✅ 入力バリデーション完了(2026-05-01)

### 共通バリデーター shared/cwm-security.js に追加(commit 95a2fea)
- cwm.validate.string(s, {min, max, label, allowEmpty}) — 長さ制限つき汎用 text
- cwm.validate.email(s, {label}) — RFC-5322 lite + 254 文字キャップ
- cwm.validate.url(s, {label, allowEmpty}) — http/https のみ、URL constructor 経由、最大2000文字
- cwm.validate.phone(s, {label}) — 数字/ハイフン/括弧/+ のみ、最低7桁
- cwm.validate.multiline(s, {min, max}) — textarea 用、制御文字除去
- cwm.validate.oneOf(s, allowed) — ホワイトリスト
- cwm.validate.safeText(s) — XSS payload 拒否(<script>, javascript:, on*=)
- cwm.validate.all(checks) — 複数バリデーターを一括処理

### 各フォームに適用
- **register form** (commit 51ddb46) — 5 input すべて maxLength + safeText 適用、URL に javascript: 拒否、動作確認済み
- **contact form** (commit 32a5394) — 3 input + 1 textarea、submit ロジックも新規実装、registrations queue 経由
- **architect-form** (commit 3bb8af7) — 6 input + 2 textarea、anon 直接 PATCH をやめて registrations queue 経由に切り替え
- **login forms** (commit 9da0ed3) — 全 input に maxlength、password に minlength 8、email + safeText チェック追加

## ✅ HTTP セキュリティヘッダ(vercel.json — commit 4f5854e)
- Content-Security-Policy(active): script-src から `'unsafe-eval'` 削除済み(`'unsafe-inline'` は当面残す)
- Content-Security-Policy-Report-Only: 厳しい strict CSP で違反検知のみ
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy: camera=()/microphone=()/geolocation=(self)/interest-cohort=()
- Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
- Cross-Origin-Opener-Policy: same-origin (window.opener制御 — reverse-tabnabbing対策)
- Cross-Origin-Resource-Policy: same-origin (cross-origin読み込み制限)

その他の CSP ハードニング(既存):
- object-src 'none'
- base-uri 'self'
- form-action 'self'
- frame-ancestors 'none'
- upgrade-insecure-requests

## 🟡 Phase 4(後日): admin-ops 保護(super admin)
運営者(白木さん本人)が使う画面。別権限レベルが必要:
- accounts テーブルの管理(他人のアカウント操作)
- 全 spaces の管理(全テナント横断)
- ~10 箇所の write 操作

実装方針: cwm-admin に `is_super_admin: boolean` フィールド or 別 Edge Function `cwm-ops` を作る。
現状: 運営者 1 人だけなのでローンチ後に対応する。

## 🟡 残タスク(優先度順)

### 中優先(ローンチ後すぐ)
1. **CSP `unsafe-inline` の完全削除**
   - 現状: 18ファイル合計 78個のインライン `<script>`、35個のインライン `<style>`、737個のインライン event handler
   - 戦略: hash-based CSP で既知のインラインscriptを許可 + 段階的に外部化
   - Report-Only ヘッダで現実の違反を観測してから本番 CSP に昇格
2. **audit_logs を admin-view から見られるように**
   - 現在 service_role のみ閲覧可
   - JWT 経由で自分のアカウント分だけ表示する Edge Function を追加(`cwm-admin` に audit.list を追加)
3. **レート制限の永続化**
   - 現状 in-memory(Edge Function instance ごと)
   - 強化版: Supabase の rate_limit テーブル + Postgres function に移行
   - もしくは Cloudflare Workers KV 等の外部ストレージ
4. **registrations queue の運営承認 UI**
   - architect-form / contact form の送信が queue に入る
   - admin-ops に承認画面を追加して、承認時に architects / 通知メール送信に反映
5. **Cross-Origin-Embedder-Policy: require-corp**
   - Supabase / fonts / YouTube が CORS で require-corp を返すようになったら追加

### 低優先(将来)
6. **Phase 4: admin-ops 保護**(super admin 権限導入)
7. **画像アップロード時のウイルススキャン**(Storage hook)
8. **異常検知アラート**(audit_logs を定期 SELECT して slack 通知)

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
