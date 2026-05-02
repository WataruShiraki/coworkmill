-- Migration: 20260502_bump_article_view
-- Purpose: Atomically increment article view_count for ranking / Most Read sidebar.
-- Called from journal/article.html on page load via PostgREST RPC.

CREATE OR REPLACE FUNCTION public.bump_article_view(p_slug TEXT)
RETURNS INT
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $func$
DECLARE
  v_count INT;
BEGIN
  UPDATE articles
  SET view_count = COALESCE(view_count, 0) + 1
  WHERE slug = p_slug AND status = 'live'
  RETURNING view_count INTO v_count;
  RETURN COALESCE(v_count, 0);
END;
$func$;

REVOKE ALL ON FUNCTION public.bump_article_view(TEXT) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.bump_article_view(TEXT) TO anon, authenticated;

-- Index to speed up Most Read query
CREATE INDEX IF NOT EXISTS idx_articles_view_count_live
  ON articles (view_count DESC)
  WHERE status = 'live';
