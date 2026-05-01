-- COWORKMILL journal: カテゴリを4つに簡素化
ALTER TABLE public.articles DROP CONSTRAINT IF EXISTS articles_category_check;
ALTER TABLE public.articles ADD CONSTRAINT articles_category_check
  CHECK (category IN ('interview','trend','news','other'));
