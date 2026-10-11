# -*- coding: utf-8 -*-
# 2026-10-11 COWORKMILL 地図ページ（わたるさん「インバウンド向けのコワーキングサイトNo1」の項目5）
# 位置は各施設の公式住所を国土地理院の住所検索（msearch.gsi.go.jp）で座標にしたもの（en/geo.json：slug → [緯度, 経度, 検索で当たった住所]）
# 地図は Leaflet（cdnjs）＋ OpenStreetMap のタイル。build_en.py から exec される
GEO = json.load(open(os.path.join(HERE, 'en', 'geo.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'en', 'geo.json')) else {}
def map_page():
    pts = []
    for s in ORDER:
        g_ = GEO.get(s)
        if not g_ or not g_[0]: continue
        e = EN[s]; img = photo(s, JA[s]['hero'][0])
        pts.append({'s': s, 'n': e['name'], 'a': e['area'], 'p': pref(e), 'la': round(g_[0], 6), 'lo': round(g_[1], 6), 'i': img or '', 't': TRAIT[s][:3]})
    n = len(pts)
    prefs = [p for p, _ in collections.Counter(x['p'] for x in pts).most_common()]
    chips = '<button type="button" class="on" data-p="">All</button>' + ''.join(f'<button type="button" data-p="{E(p)}">{E(p)}</button>' for p in prefs)
    data = json.dumps(pts, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": "Map of coworking spaces in Japan", "url": SITE + '/spaces/map.html'}]
    css = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
           '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.min.css">'
           '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.Default.min.css">'
           '<style>#map{height:72vh;min-height:420px;border:1px solid var(--line);border-radius:12px;margin-top:14px}.mchips{display:flex;flex-wrap:wrap;gap:6px}'
           '.mchips button{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}.mchips button.on{background:var(--ink);color:#fff;border-color:var(--ink)}'
           '.mpop{width:220px}.mpop img{width:100%;height:120px;object-fit:cover;border-radius:6px;display:block;margin-bottom:6px}.mpop b{display:block;font-size:14px}.mpop small{color:#666}.mpop .chips{margin-top:4px;font-size:11px;color:#2F6A98}</style>')
    h = head(f'Map of {n} coworking spaces in Japan | {NAME}', f'All {n} coworking spaces on one map — Tokyo, Yokohama, Osaka, Kyoto, Fukuoka, Sapporo and Naha. Tap a pin for photos, prices and how to get there.', 'spaces/map.html', None, 'website', ld)
    h = h.replace('</head>', css + '</head>', 1)
    js = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>'
          '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.min.js"></script>'
          f'<script>(function(){{var P={data};var m=L.map("map",{{scrollWheelZoom:false}});'
          'L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"&copy; <a href=\\"https://www.openstreetmap.org/copyright\\">OpenStreetMap</a> contributors · positions from official addresses via GSI"}).addTo(m);'
          'var g=L.markerClusterGroup({showCoverageOnHover:false,maxClusterRadius:40});'
          'function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}'
          f'function draw(p){{g.clearLayers();var b=[];P.forEach(function(x){{if(p&&x.p!==p)return;var mk=L.marker([x.la,x.lo]);'
          f'mk.bindPopup(\'<a class="mpop" hr\'+\'ef="{U("spaces/")}\'+x.s+\'.html">\'+(x.i?\'<img src="\'+esc(x.i)+\'" alt="" loading="lazy">\':"")+\'<b>\'+esc(x.n)+\'</b><small>\'+esc(x.a)+\'</small>\'+(x.t.length?\'<div class="chips">\'+x.t.map(esc).join(" · ")+\'</div>\':"")+\'</a>\');'
          'g.addLayer(mk);b.push([x.la,x.lo])});m.addLayer(g);if(b.length)m.fitBounds(b,{padding:[30,30],maxZoom:15})}'
          'var q=new URLSearchParams(location.search).get("pref")||"";draw(q);'
          'document.querySelectorAll(".mchips button").forEach(function(bt){if(bt.dataset.p===q){document.querySelectorAll(".mchips button").forEach(function(o){o.classList.remove("on")});bt.classList.add("on")}'
          'bt.addEventListener("click",function(){document.querySelectorAll(".mchips button").forEach(function(o){o.classList.remove("on")});bt.classList.add("on");draw(bt.dataset.p)})});'
          'm.on("click",function(){m.scrollWheelZoom.enable()})})();</script>')
    return (h + nav('spaces/') +
            f'<main class="wrap"><div class="crumb"><a href="{U("spaces/")}">Spaces</a> › Map</div><div class="head"><p class="tag">{n} spaces</p><h1>Coworking spaces in Japan on a map</h1>'
            f'<p class="lead">Every space we list, placed from its official address. Tap a pin for the photos, prices, hours and directions.</p></div>'
            f'<div class="mchips">{chips}</div><div id="map" role="region" aria-label="Map of coworking spaces"></div>'
            f'<p class="note">Pins are placed from each space\'s official address using the Geospatial Information Authority of Japan\'s address search, so a pin can sit a little off the entrance. Use the Directions link on each page for the exact route.</p>'
            f'<p class="more"><a href="{U("spaces/")}">See the list of all {len(ORDER)} spaces →</a></p></main>' + foot()).replace('</body>', js + '</body>', 1)
