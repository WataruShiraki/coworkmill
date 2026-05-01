-- COWORKMILL journal: 運営アカウント1つで全記事を編集できるよう RLS を緩和
-- (外部ライター機能を一旦無効化し、Edge Function 不要で運用するための調整)

-- ============== articles RLS ==============
DROP POLICY IF EXISTS "articles_writer_insert" ON public.articles;
CREATE POLICY "articles_writer_insert"
  ON public.articles
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "articles_writer_update" ON public.articles;
CREATE POLICY "articles_writer_update"
  ON public.articles
  FOR UPDATE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "articles_writer_delete" ON public.articles;
CREATE POLICY "articles_writer_delete"
  ON public.articles
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "articles_author_self_select" ON public.articles;
DROP POLICY IF EXISTS "articles_writer_select_all" ON public.articles;
CREATE POLICY "articles_writer_select_all"
  ON public.articles
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

-- ============== media_assets RLS ==============
DROP POLICY IF EXISTS "media_writer_insert" ON public.media_assets;
CREATE POLICY "media_writer_insert"
  ON public.media_assets
  FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "media_writer_select" ON public.media_assets;
CREATE POLICY "media_writer_select"
  ON public.media_assets
  FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "media_writer_delete" ON public.media_assets;
CREATE POLICY "media_writer_delete"
  ON public.media_assets
  FOR DELETE
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

-- ============== Storage bucket RLS ==============
DROP POLICY IF EXISTS "journal_images_writer_insert" ON storage.objects;
CREATE POLICY "journal_images_writer_insert"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (
    bucket_id = 'journal-images'
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "journal_images_writer_update" ON storage.objects;
CREATE POLICY "journal_images_writer_update"
  ON storage.objects FOR UPDATE
  TO authenticated
  USING (
    bucket_id = 'journal-images'
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );

DROP POLICY IF EXISTS "journal_images_writer_delete" ON storage.objects;
CREATE POLICY "journal_images_writer_delete"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (
    bucket_id = 'journal-images'
    AND EXISTS (
      SELECT 1 FROM public.journal_writers w
      WHERE w.user_id = auth.uid() AND w.status = 'active'
    )
  );
