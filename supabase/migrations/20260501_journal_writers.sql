-- COWORKMILL journal: writer profiles + author_id link on articles
-- Phase 2-1
--
-- 認証は Supabase Auth(auth.users)を使う。journal_writers はそのプロフィール拡張。
-- 運営(白木さん)が運営管理画面から auth.users に admin API でユーザー作成
-- → journal_writers に row を作る → ライターに ID/PW を手渡し
-- ライターは journal-admin ログイン画面で email + password 入力 → JWT 取得
-- → JWT で article.* / media.* 操作(Edge Function 側で sub と journal_writers
-- の対応を見て、自分の記事だけ操作できるよう絞る)。

-- ============== journal_writers テーブル ==============
CREATE TABLE IF NOT EXISTS public.journal_writers (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  display_name    TEXT NOT NULL,
  bio             TEXT,
  avatar_url      TEXT,
  role            TEXT NOT NULL DEFAULT 'writer',
  status          TEXT NOT NULL DEFAULT 'active',
  invited_by      UUID,
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now(),
  last_login_at   TIMESTAMPTZ,
  CONSTRAINT writer_role_check CHECK (role IN ('writer','editor','admin')),
  CONSTRAINT writer_status_check CHECK (status IN ('active','suspended','deleted'))
);

CREATE INDEX IF NOT EXISTS idx_writers_user_id ON public.journal_writers(user_id);
CREATE INDEX IF NOT EXISTS idx_writers_status ON public.journal_writers(status);

-- updated_at trigger 流用
DROP TRIGGER IF EXISTS journal_writers_set_updated_at ON public.journal_writers;
CREATE TRIGGER journal_writers_set_updated_at
  BEFORE UPDATE ON public.journal_writers
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============== articles テーブルに author_user_id を追加 ==============
-- 既存 author_name は維持(表示用、自由記述)、author_user_id は所有権を表す
ALTER TABLE public.articles
  ADD COLUMN IF NOT EXISTS author_user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_articles_author ON public.articles(author_user_id);

-- ============== RLS: journal_writers ==============
ALTER TABLE public.journal_writers ENABLE ROW LEVEL SECURITY;

-- anon は完全アクセス不可(write の audit_logs と同じ)
DROP POLICY IF EXISTS "writers_anon_no_select" ON public.journal_writers;
CREATE POLICY "writers_anon_no_select" ON public.journal_writers FOR SELECT USING (false);

DROP POLICY IF EXISTS "writers_anon_no_write" ON public.journal_writers;
CREATE POLICY "writers_anon_no_write" ON public.journal_writers FOR INSERT WITH CHECK (false);

DROP POLICY IF EXISTS "writers_anon_no_update" ON public.journal_writers;
CREATE POLICY "writers_anon_no_update" ON public.journal_writers FOR UPDATE USING (false);

DROP POLICY IF EXISTS "writers_anon_no_delete" ON public.journal_writers;
CREATE POLICY "writers_anon_no_delete" ON public.journal_writers FOR DELETE USING (false);

-- 認証済みユーザーは自分の row だけ SELECT 可(プロフィール表示用)
DROP POLICY IF EXISTS "writers_self_select" ON public.journal_writers;
CREATE POLICY "writers_self_select"
  ON public.journal_writers
  FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

-- ============== articles RLS: ライター自身が draft も読めるように ==============
-- 既存の anon SELECT (live のみ) は維持
-- 認証済みユーザーは自分が author の記事を全status で読めるように追加
DROP POLICY IF EXISTS "articles_author_self_select" ON public.articles;
CREATE POLICY "articles_author_self_select"
  ON public.articles
  FOR SELECT
  TO authenticated
  USING (author_user_id = auth.uid());

-- ============== サンプル データ なし(運営管理から実際に追加する) ==============
