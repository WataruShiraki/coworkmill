-- COWORKMILL journal: ライターが自分の記事を直接 CRUD できるよう RLS 拡張
-- (Phase 2-2)
--
-- 設計方針:
--   ライターは Supabase Auth で認証 → JWT 取得 → Supabase REST 直アクセス
--   RLS で「自分が author の記事だけ書ける」を保証
--   公開ステータス変更も自分の記事内なら自由(編集部承認なし方針 — 後で変えるなら追加policy)
--
-- 既存の Edge Function (article.* / media.*) は運営用に維持。

-- ============== articles: 認証済みユーザー(ライター)用 INSERT ==============
DROP POLICY IF EXISTS "articles_writer_insert" ON public.articles;
CREATE POLICY "articles_writer_insert"
  ON public.articles
  FOR INSERT
  TO authenticated
  WITH CHECK (
    author_user_id = auth.uid()
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

-- UPDATE: 自分が author で、かつアクティブなライター
DROP POLICY IF EXISTS "articles_writer_update" ON public.articles;
CREATE POLICY "articles_writer_update"
  ON public.articles
  FOR UPDATE
  TO authenticated
  USING (
    author_user_id = auth.uid()
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  )
  WITH CHECK (
    author_user_id = auth.uid()  -- author を別人に変更されないよう保護
  );

-- DELETE: 自分が author の記事だけ削除可能(soft delete 推奨だが、ハード削除も認める)
DROP POLICY IF EXISTS "articles_writer_delete" ON public.articles;
CREATE POLICY "articles_writer_delete"
  ON public.articles
  FOR DELETE
  TO authenticated
  USING (
    author_user_id = auth.uid()
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

-- ============== media_assets: ライター用 INSERT/DELETE ==============
-- ライターは自分の記事に紐づく画像のみ挿入可能(article_id 先存在チェック)
DROP POLICY IF EXISTS "media_writer_insert" ON public.media_assets;
CREATE POLICY "media_writer_insert"
  ON public.media_assets
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.articles a
      JOIN public.journal_writers w ON w.user_id = auth.uid()
      WHERE a.id = media_assets.article_id
        AND a.author_user_id = auth.uid()
        AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "media_writer_select" ON public.media_assets;
CREATE POLICY "media_writer_select"
  ON public.media_assets
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.articles a
      WHERE a.id = media_assets.article_id
        AND a.author_user_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "media_writer_delete" ON public.media_assets;
CREATE POLICY "media_writer_delete"
  ON public.media_assets
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.articles a
      WHERE a.id = media_assets.article_id
        AND a.author_user_id = auth.uid()
        AND EXISTS (SELECT 1 FROM public.journal_writers w WHERE w.user_id = auth.uid() AND w.status = 'active')
    )
  );
