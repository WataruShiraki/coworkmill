-- COWORKMILL journal: articles & media_assets schema
-- 2026-05-01 (Phase 1A)
-- 
-- Tables:
--   articles      : 記事本体(タイトル/本文/カテゴリ/状態/著者など)
--   media_assets  : 画像の出所管理(著作権・クレジット必須)
-- 
-- RLS方針:
--   anon: status='live' のみ SELECT 可、write 一切不可
--   service_role(Edge Function 経由): 全権限
--   write は cwm-admin Edge Function の article.* アクション経由のみ

-- ============== articles テーブル ==============
CREATE TABLE IF NOT EXISTS public.articles (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug            TEXT UNIQUE NOT NULL,
  title           TEXT NOT NULL,
  subtitle        TEXT,
  category        TEXT NOT NULL,
  hero_image      TEXT,
  excerpt         TEXT,
  body_md         TEXT,
  body_html       TEXT,
  related_space_ids UUID[],
  tags            TEXT[],
  author_name     TEXT NOT NULL DEFAULT 'COWORKMILL journal 編集部',
  author_bio      TEXT,
  author_avatar   TEXT,
  status          TEXT NOT NULL DEFAULT 'draft',
  scheduled_at    TIMESTAMPTZ,
  published_at    TIMESTAMPTZ,
  updated_at      TIMESTAMPTZ DEFAULT now(),
  view_count      INTEGER DEFAULT 0,
  is_pr           BOOLEAN DEFAULT false,
  pr_disclosure   TEXT,
  meta_title      TEXT,
  meta_description TEXT,
  og_image        TEXT,
  reading_minutes INTEGER,
  created_at      TIMESTAMPTZ DEFAULT now(),
  CONSTRAINT articles_status_check CHECK (status IN ('draft','scheduled','live','archived')),
  CONSTRAINT articles_category_check CHECK (category IN ('area-guide','interview','workstyle','data','design','other'))
);

CREATE INDEX IF NOT EXISTS idx_articles_status_published ON public.articles(status, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_category ON public.articles(category, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_slug ON public.articles(slug);
CREATE INDEX IF NOT EXISTS idx_articles_tags ON public.articles USING GIN(tags);

-- updated_at を自動更新
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS articles_set_updated_at ON public.articles;
CREATE TRIGGER articles_set_updated_at
  BEFORE UPDATE ON public.articles
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============== media_assets テーブル ==============
CREATE TABLE IF NOT EXISTS public.media_assets (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  article_id      UUID REFERENCES public.articles(id) ON DELETE CASCADE,
  storage_path    TEXT,
  url             TEXT NOT NULL,
  alt_text        TEXT NOT NULL,
  -- 出所管理(必須)
  source_type     TEXT NOT NULL,
  photographer    TEXT,
  source_name     TEXT,
  source_url      TEXT,
  license         TEXT,
  permission_note TEXT,
  -- メタデータ
  width           INTEGER,
  height          INTEGER,
  file_size       INTEGER,
  position_in_body INTEGER,
  caption         TEXT,
  uploaded_at     TIMESTAMPTZ DEFAULT now(),
  CONSTRAINT media_source_type_check CHECK (source_type IN ('own','facility','stock','ai','cc'))
);

CREATE INDEX IF NOT EXISTS idx_media_article ON public.media_assets(article_id);

-- ============== RLS: articles ==============
ALTER TABLE public.articles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "articles_anon_read_live" ON public.articles;
CREATE POLICY "articles_anon_read_live"
  ON public.articles
  FOR SELECT
  USING (status = 'live');

DROP POLICY IF EXISTS "articles_anon_no_write" ON public.articles;
CREATE POLICY "articles_anon_no_write"
  ON public.articles
  FOR INSERT
  WITH CHECK (false);

DROP POLICY IF EXISTS "articles_anon_no_update" ON public.articles;
CREATE POLICY "articles_anon_no_update"
  ON public.articles
  FOR UPDATE
  USING (false);

DROP POLICY IF EXISTS "articles_anon_no_delete" ON public.articles;
CREATE POLICY "articles_anon_no_delete"
  ON public.articles
  FOR DELETE
  USING (false);

-- ============== RLS: media_assets ==============
ALTER TABLE public.media_assets ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "media_anon_read_via_live_article" ON public.media_assets;
CREATE POLICY "media_anon_read_via_live_article"
  ON public.media_assets
  FOR SELECT
  USING (
    article_id IS NULL
    OR EXISTS (
      SELECT 1 FROM public.articles a
      WHERE a.id = media_assets.article_id AND a.status = 'live'
    )
  );

DROP POLICY IF EXISTS "media_anon_no_write" ON public.media_assets;
CREATE POLICY "media_anon_no_write"
  ON public.media_assets
  FOR INSERT WITH CHECK (false);

DROP POLICY IF EXISTS "media_anon_no_update" ON public.media_assets;
CREATE POLICY "media_anon_no_update"
  ON public.media_assets
  FOR UPDATE USING (false);

DROP POLICY IF EXISTS "media_anon_no_delete" ON public.media_assets;
CREATE POLICY "media_anon_no_delete"
  ON public.media_assets
  FOR DELETE USING (false);

-- ============== サンプルデータ(動作確認用、後で消してOK) ==============
INSERT INTO public.articles (
  slug, title, subtitle, category, excerpt, body_md, body_html,
  status, published_at, author_name, tags, reading_minutes
) VALUES (
  'hello-coworkmill-journal',
  'COWORKMILL journal、はじめます。',
  'デザインコワーキングの「いま」と「これから」を伝える編集部からの最初のお知らせ',
  'other',
  'COWORKMILL journal は、デザイン性に優れたコワーキングスペースの取材・選び方・トレンドを伝える編集メディアです。',
  E'## はじめまして、COWORKMILL journal です。\n\nコワーキングを「探す」だけのプラットフォームから、「知る・選ぶ・行きたくなる」までを支えるメディアへ。\n\nこれから、エリアごとのおすすめ施設、運営者・建築家の取材、ワークスタイル別の選び方など、月10本ペースで記事をお届けしていきます。\n\nどうぞよろしくお願いします。',
  E'<h2>はじめまして、COWORKMILL journal です。</h2><p>コワーキングを「探す」だけのプラットフォームから、「知る・選ぶ・行きたくなる」までを支えるメディアへ。</p><p>これから、エリアごとのおすすめ施設、運営者・建築家の取材、ワークスタイル別の選び方など、月10本ペースで記事をお届けしていきます。</p><p>どうぞよろしくお願いします。</p>',
  'live',
  now(),
  'COWORKMILL journal 編集部',
  ARRAY['お知らせ','編集部'],
  2
)
ON CONFLICT (slug) DO NOTHING;
