-- architects テーブルの RLS を anon write 不可に固定
-- Phase 3 (2026-04-30): architects も Edge Function 経由のみ書き込み可能に

-- 既存テーブルがあるはず(scaffold で作成済み)
ALTER TABLE public.architects ENABLE ROW LEVEL SECURITY;

-- anon SELECT は許可(公開情報なので一覧取得OK)
DROP POLICY IF EXISTS "architects_anon_read" ON public.architects;
CREATE POLICY "architects_anon_read"
  ON public.architects FOR SELECT
  USING (true);

-- INSERT/UPDATE/DELETE: anon 不可(Edge Function 経由のみ)
-- ※ 既存に anon write policy があれば DROP すること
DROP POLICY IF EXISTS "architects_anon_insert" ON public.architects;
DROP POLICY IF EXISTS "architects_anon_update" ON public.architects;
DROP POLICY IF EXISTS "architects_anon_delete" ON public.architects;
