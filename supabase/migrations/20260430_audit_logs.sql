-- audit_logs: cwm-admin Edge Function の操作履歴
-- Phase 5 (2026-04-30): 監査ログテーブル

CREATE TABLE IF NOT EXISTS public.audit_logs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id  UUID NOT NULL REFERENCES public.accounts(id) ON DELETE CASCADE,
  target      TEXT NOT NULL,         -- voice / space / space_image / architect
  action      TEXT NOT NULL,         -- insert / update / delete / approve / reject
  record_id   UUID NULL,             -- 操作対象 record の ID(insert時はnull)
  status      TEXT NOT NULL,         -- ok / denied / error
  detail      TEXT NULL,             -- エラーメッセージや拒否理由
  ip          TEXT NULL,             -- リクエスト元 IP
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_account ON public.audit_logs(account_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_target ON public.audit_logs(target, action, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_status ON public.audit_logs(status, created_at DESC) WHERE status != 'ok';

-- RLS: anon/auth ともに直接アクセス不可。Edge Function (service_role) 経由のみ。
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- 自分のアカウント分のみ読める policy
CREATE POLICY "audit_logs_self_read"
  ON public.audit_logs
  FOR SELECT
  USING (false);  -- 当面は service_role 以外読めない(将来 admin-view から見たければ JWT 経由で開放)

COMMENT ON TABLE public.audit_logs IS 'cwm-admin Edge Function operation audit trail';
