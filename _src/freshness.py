# -*- coding: utf-8 -*-
# 2026-10-11 COWORKMILL 情報の鮮度チェック（わたるさん「インバウンド向けのコワーキングサイトNo1」の項目3）
# 各施設の「公式サイトで最後に確かめた日」を en/checked.json に持ち、施設ページに表示する（build_en.py が読む）
# 使い方（_src で実行）:
#   python3 freshness.py                 … 確認から90日を過ぎた施設を、人気順に10件出す（今日の確認リスト）
#   python3 freshness.py --days 60 --n 20
#   python3 freshness.py --mark slug1 slug2  … 公式サイトで確かめ直した施設の日付を今日にする
#   python3 freshness.py --gone slug         … 閉店・掲載終了：gone.txt に足し、checked.json から外す（データ本体の削除は別に行う）
# 確かめ方（RESEARCH_RULES.md と同じ）: Chrome で公式URLを開き、住所・営業時間・料金・ドロップインの有無を英訳本文・visit_extra.json と見比べる。
#   違っていたら英訳（en/b*.json）・visit_extra.json・日本語データを直してから --mark する。閉店・休止の表示があれば --gone。
import os, sys, json, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, 'en', 'checked.json')
def load(): return json.load(open(P, encoding='utf-8'))
def save(d): json.dump(dict(sorted(d.items())), open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
today = datetime.date.today().isoformat()
a = sys.argv[1:]
if a[:1] == ['--mark']:
    d = load()
    for s in a[1:]:
        if s not in d: print('知らないスラッグ:', s); continue
        d[s] = today
    save(d); print('更新:', len(a) - 1, '件 →', today)
elif a[:1] == ['--gone']:
    d = load()
    with open(os.path.join(HERE, 'gone.txt'), 'a', encoding='utf-8') as f:
        for s in a[1:]: f.write(f'spaces/{s}\n'); d.pop(s, None)
    save(d); print('gone.txt に追加:', a[1:])
else:
    days = int(a[a.index('--days') + 1]) if '--days' in a else 90
    n = int(a[a.index('--n') + 1]) if '--n' in a else 10
    g = {'__file__': os.path.join(HERE, 'x')}
    exec(open(os.path.join(HERE, 'cowork_facilities.py'), encoding='utf-8').read(), g)
    g['A'] = sorted(g['A30'], key=lambda x: x.get('added', ''), reverse=True); g['A_by'] = {x['slug']: x for x in g['A']}
    exec(open(os.path.join(HERE, 'seo_cowork.py'), encoding='utf-8').read(), g)
    exec(open(os.path.join(HERE, 'popular_cowork.py'), encoding='utf-8').read(), g)
    pop = [s for s in g.get('POPULAR', [])]
    d = load(); lim = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    old = [s for s in d if d[s] <= lim]
    old.sort(key=lambda s: (pop.index(s) if s in pop else 10**6, d[s]))
    off = g['OFFICIAL30']
    print(f'確認から{days}日を過ぎた施設: {len(old)} 件（全{len(d)}件）。今日の確認リスト:')
    for s in old[:n]: print(f'  {d[s]}  {s}  {off.get(s, "")}')
