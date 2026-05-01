-- COWORKMILL journal: 画像アップロード用 Supabase Storage バケット
-- (Phase 2-6)
--
-- バケット名: journal-images
-- パス命名: {writer_user_id}/{article_id}/{timestamp}-{filename}
-- 認証: ライターは自分の writer_user_id 配下にのみ書き込み可
-- 公開: 誰でも読める(public bucket)— journal は記事内画像なので問題なし

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'journal-images',
  'journal-images',
  true,
  10485760, -- 10 MB
  ARRAY['image/jpeg','image/png','image/webp','image/gif','image/svg+xml']
)
ON CONFLICT (id) DO UPDATE SET
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

-- RLS: バケット内オブジェクトのアクセス制御
-- アクティブなライターは自分の user_id プレフィックス配下にのみ書き込み可

DROP POLICY IF EXISTS "journal_images_anon_read" ON storage.objects;
CREATE POLICY "journal_images_anon_read"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'journal-images');

DROP POLICY IF EXISTS "journal_images_writer_insert" ON storage.objects;
CREATE POLICY "journal_images_writer_insert"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (
    bucket_id = 'journal-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
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
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

DROP POLICY IF EXISTS "journal_images_writer_delete" ON storage.objects;
CREATE POLICY "journal_images_writer_delete"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (
    bucket_id = 'journal-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );
