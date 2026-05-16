-- ============================================
-- COWORKMILL: 編集部キュレーション施設 投入SQL
-- 12施設 を status='draft' + needs_owner_claim=true で投入
-- 作成日: 2026-05-16
-- 情報源: 公開情報（JFO検索結果含む）
-- ============================================
-- 実行方法:
-- 1. https://supabase.com/dashboard/project/jakwntemjkwqwaqujffh/sql/new で開く
-- 2. 全文をコピペして「Run」ボタン
-- 3. 投入後、admin で1施設ずつ確認 → status='live' に変更
-- ============================================
-- 注意: 写真・ロゴ・設計者情報は含めません（権利配慮）
-- ============================================

INSERT INTO spaces (
  name, slug, prefecture, area, nearest_station, address, official_url, description,
  plan, status, needs_owner_claim, is_verified, created_at, updated_at
) VALUES
  ('WeWork オーシャンゲートみなとみらい', 'wework-oceangate-minatomirai', '神奈川県', '横浜駅・みなとみらい', 'みなとみらい駅(徒歩2分)、桜木町駅(徒歩12分)', '神奈川県横浜市西区みなとみらい3-7-1 オーシャンゲートみなとみらい', 'https://www.wework.com/ja-JP/buildings/oceangate--minatomirai--yokohama', 'みなとみらいエリア、ベイエリアの海を望む開放感あるWeWork拠点。グローバルなコワーキングコミュニティを体感できる。', 'free', 'draft', true, false, NOW(), NOW()),
  ('ミッドポイント六本木', 'midpoint-roppongi', '東京都', '赤坂・六本木', '六本木駅(徒歩1分)、六本木一丁目駅(徒歩9分)、乃木坂駅(徒歩10分)', '東京都港区六本木7-15-7', 'https://www.midpoint.jp/roppongi', '六本木駅徒歩1分、ミニマルで上質なレンタルオフィス＆コワーキング。', 'free', 'draft', true, false, NOW(), NOW()),
  ('ミッドポイント市ヶ谷', 'midpoint-ichigaya', '東京都', '市ヶ谷・四ツ谷', '市ケ谷駅(徒歩3分)、半蔵門駅(徒歩6分)、麹町駅(徒歩9分)', '東京都新宿区市谷田町', 'https://www.midpoint.jp/ichigaya', '市ヶ谷駅近、シンプルな設計と機能性を兼ね備えたコワーキング。', 'free', 'draft', true, false, NOW(), NOW()),
  ('ミッドポイント豊洲', 'midpoint-toyosu', '東京都', '豊洲・有明', '豊洲駅(徒歩3分)', '東京都江東区豊洲', 'https://www.midpoint.jp/toyosu', '豊洲駅近、ベイエリアの開放感を感じられるコワーキング。', 'free', 'draft', true, false, NOW(), NOW()),
  ('CIC Tokyo', 'cic-tokyo', '東京都', '虎ノ門・赤坂', '虎ノ門ヒルズ駅(直結)、虎ノ門駅(徒歩4分)', '東京都港区虎ノ門1-17-1 虎ノ門ヒルズビジネスタワー15F', 'https://cic.com/tokyo', '虎ノ門ヒルズビジネスタワーに位置するスタートアップ・イノベーション拠点。建築美と機能性を両立。', 'free', 'draft', true, false, NOW(), NOW()),
  ('CIC 福岡', 'cic-fukuoka', '福岡県', '天神・博多', '天神駅(直結)、西鉄福岡（天神）駅(徒歩3分)、天神南駅(徒歩5分)', '福岡県福岡市中央区天神', 'https://cic.com/fukuoka', '九州初の本格イノベーション拠点。スタートアップ・大企業・研究機関が集まる空間。', 'free', 'draft', true, false, NOW(), NOW()),
  ('BLOCKS 目黒', 'blocks-meguro', '東京都', '目黒・白金台', '目黒駅(徒歩1分)、白金台駅(徒歩14分)', '東京都品川区上大崎', 'https://blocks-rental.jp/meguro', '目黒駅直結、スタイリッシュなフレキシブルオフィス。', 'free', 'draft', true, false, NOW(), NOW()),
  ('BuD square 市ヶ谷', 'bud-square-ichigaya', '東京都', '市ヶ谷・四ツ谷', '市ケ谷駅(徒歩5分)', '東京都新宿区市谷', 'https://bud-square.jp', '市ヶ谷エリア、デザイン性の高いレンタルオフィス。', 'free', 'draft', true, false, NOW(), NOW()),
  ('Vlag yokohama', 'vlag-yokohama', '神奈川県', '横浜駅・みなとみらい', '横浜駅(直結)', '神奈川県横浜市西区', 'https://www.vlag-yokohama.com', '横浜駅直結。利便性とモダンなデザインを両立した拠点。', 'free', 'draft', true, false, NOW(), NOW()),
  ('THE HUB 横浜元町', 'the-hub-yokohama-motomachi', '神奈川県', '横浜元町・関内', '石川町駅(徒歩2分)、元町・中華街駅(徒歩11分)', '神奈川県横浜市中区元町', 'https://thehub.jp/yokohama-motomachi', '横浜元町エリアのモダンなフレキシブルオフィス。', 'free', 'draft', true, false, NOW(), NOW()),
  ('THE HUB 有楽町イースト', 'the-hub-yurakucho-east', '東京都', '銀座・有楽町・新橋', '京橋駅(徒歩2分)、銀座一丁目駅(徒歩3分)、宝町駅(徒歩5分)、東京駅(徒歩7分)', '東京都中央区京橋', 'https://thehub.jp/yurakucho-east', '有楽町・京橋エリアの洗練されたフレキシブルオフィス。', 'free', 'draft', true, false, NOW(), NOW()),
  ('コンパスオフィス恵比寿グリーングラス', 'compass-ebisu-greenglass', '東京都', '渋谷・恵比寿・代官山', '恵比寿駅(徒歩5分)', '東京都渋谷区恵比寿南3-1-1 いちご恵比寿グリーングラス6F-9F', 'https://www.compass-offices.com/jp/locations/ebisu', '恵比寿の落ち着いた立地、上質なサービスオフィス。', 'free', 'draft', true, false, NOW(), NOW());

-- 投入結果を確認
SELECT slug, name, area, prefecture, status, needs_owner_claim 
FROM spaces 
WHERE status = 'draft' AND needs_owner_claim = true
ORDER BY created_at DESC;
