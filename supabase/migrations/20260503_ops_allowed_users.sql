-- ============================================================
-- Migration: ops_allowed_users
-- Date: 2026-05-03
-- Purpose: 運営管理画面 (admin-ops) のアクセス許可リスト
-- ============================================================
-- 設計:
-- - Google ログイン後、このテーブルにメールアドレスが存在すれば admin-ops に入れる
-- - role: 'owner' は他ユーザーの招待・削除が可能、'staff' はログインのみ
-- - 全ての書き込みは Edge Function (cwm-admin, target=ops) 経由のみ
-- - RLS により公開鍵 (sb_publishable_*) からの直接アクセスは完全禁止

CREATE TABLE IF NOT EXISTS ops_allowed_users (
  email          text PRIMARY KEY,
  role           text NOT NULL DEFAULT 'staff' CHECK (role IN ('owner','staff')),
  invited_by     text,
  invited_at     timestamptz NOT NULL DEFAULT now(),
  last_login_at  timestamptz,
  notes          text,
  CONSTRAINT ops_allowed_users_email_lower CHECK (email = lower(email))
);

CREATE INDEX IF NOT EXISTS idx_ops_allowed_users_role ON ops_allowed_users(role);

-- RLS: 完全に閉じる。Edge Function は service_role で接続するので RLS をバイパスする
ALTER TABLE ops_allowed_users ENABLE ROW LEVEL SECURITY;

-- 既存のポリシーがある場合は削除してから作り直し
DROP POLICY IF EXISTS "deny_all_anon" ON ops_allowed_users;
DROP POLICY IF EXISTS "deny_all_authenticated" ON ops_allowed_users;

-- 公開鍵からの SELECT/INSERT/UPDATE/DELETE を完全拒否
CREATE POLICY "deny_all_anon" ON ops_allowed_users
  FOR ALL TO anon
  USING (false)
  WITH CHECK (false);

CREATE POLICY "deny_all_authenticated" ON ops_allowed_users
  FOR ALL TO authenticated
  USING (false)
  WITH CHECK (false);

-- ============================================================
-- 初期 owner: 白木さんのメールアドレスを以下に挿入してください
-- ============================================================
-- ※このマイグレーション適用後、Supabase ダッシュボードの SQL Editor で
--   下記コメントアウトを外して実行してください（メアドは実際のものに置換）
-- ============================================================

-- INSERT INTO ops_allowed_users (email, role, invited_by, notes)
-- VALUES ('YOUR_EMAIL_HERE@example.com', 'owner', 'system', '初期 owner (system bootstrap)')
-- ON CONFLICT (email) DO UPDATE SET role = 'owner';
