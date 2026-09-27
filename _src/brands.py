# COWORKMILL / CAFEMILL の設定（OFFISNAP の build_site.py を流用するための差分）
BRANDS = {
 'cowork': dict(
    name='COWORKMILL', kana='コワークミル', domain='cowkml.com', sec='spaces',
    subj='コワーキングスペース', subj_s='コワーキング', kind='施設', owner='運営会社',
    tag='日本で最も優れたコワーキングを厳選紹介', band='日本のかっこいいコワーキングスペースを、見に行こう。',
    c1='#7FC39A', c2='#3B7DAE', dark='#2F6A98', light='#EEF6F1', light2='#F3F8F4', light3='#F6FAF7', line='#CFE3D8', mid='#4F9DB0',
    logo=os.path.join(HERE, 'logo_cowork.svg'), ga='G-P6CZCM6K18',
    facilities='cowork_facilities.py',
    desc='日本のかっこいいコワーキングスペースを、公式の写真と情報で1施設ずつ紹介するメディア。',
    coll_lead='街、駅からの近さ、使える時間、広さ。コワーキングスペースを、共通のテーマで見比べる特集です。',
    coll_desc='丸の内・虎ノ門・渋谷などの街、駅直結、24時間、広さ、つくった会社。日本のコワーキングスペースをテーマ別に見比べる特集。',
    about_lead='日本のかっこいいコワーキングスペースを、公式の写真と情報で1施設ずつ紹介するメディアです。受付から執務エリア、会議室、ラウンジへと、初めて訪れた人が歩く順番でご案内します。',
    utm='coworkmill'),
 'cafe': dict(
    name='CAFEMILL', kana='カフェミル', domain='cfmill.com', sec='cafes',
    subj='カフェ', subj_s='カフェ', kind='店', owner='運営会社',
    tag='日本で最も優れたカフェを厳選紹介', band='日本のかっこいいカフェを、見に行こう。',
    c1='#F2B21F', c2='#E0431F', dark='#C8380F', light='#FDF4E6', light2='#FDF6EC', light3='#FEF9F2', line='#F3DCB8', mid='#E07828',
    logo=os.path.join(HERE, 'logo_cafe.svg'), ga='G-4T5SDW3MHR',
    facilities='cafe_facilities.py',
    desc='日本のかっこいいカフェを、公式の写真と情報で1店ずつ紹介するメディア。',
    about_lead='日本のかっこいいカフェを、公式の写真と情報で1店ずつ紹介するメディアです。入口からカウンター、客席、焙煎所や工房へと、初めて訪れた人が歩く順番でご案内します。',
    utm='cafemill'),
}
