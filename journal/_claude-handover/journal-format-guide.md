# COWORKMILL journal — 記事フォーマットガイド

> **絶対に守るルール**：新しい記事を書く前に必ず**新橋記事**（`/journal/shimbashi-toranomon-coworking-2026/index.html`）を GitHub で開かてフルスクャンすること。新橋記事が唯一のフォーマット基準。このドクュメントだけを見て書き始めることは禁止。

---

## 1. body 直下の要素（順番）

```html
<body>

<header class="j-nav">...</header>

<!-- 読書進捗バー（固定） -->
<div class="j-progress" id="progress"></div>

<!-- SNSシェア縦バー（左固定：X / LINE / Facebook / コピー） -->
<aside class="j-share-vbar">
  <a href="https://twitter.com/intent/tweet?url=..." target="_blank" rel="noopener" title="Xでシェア">𝕏</a>
  <a href="https://social-plugins.line.me/lineit/share?url=..." target="_blank" rel="noopener" title="LINEで送る">L</a>
  <a href="https://www.facebook.com/sharer/sharer.php?u=..." target="_blank" rel="noopener" title="Facebookでシェア">f</a>
  <a href="javascript:void(0)" onclick="navigator.clipboard.writeText(location.href)" title="リンクをコピー">⎘</a>
</aside>

<!-- メインコンテンツ：2カラムグリッド -->
<main class="j-page-grid">
  <article class="j-article">
    ... 記事本文 ...
  </article>
  <aside class="j-sidebar">
    ... 右サイドバー ...
  </aside>
</main>

<footer class="j-foot">...</footer>

<script async src="//www.instagram.com/embed.js"></script>
<script>/* 読書進捗バー + TOCアクティブ追跡 JS */</script>

</body>
```

---

## 2. head の必須要素

```html
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>記事タイトル — COWORKMILL journal</title>
<meta name="description" content="...">
<meta name="author" content="ライター名">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="article">
<meta property="og:url" content="https://cowkml.com/journal/スラッグ/">
<meta property="og:image" content="https://cowkml.com/journal/スラッグ/og-image.svg">
<meta property="og:site_name" content="COWORKMILL journal">
<meta property="og:locale" content="ja_JP">
<meta property="article:published_time" content="2026-05-XX T10:00:00+09:00">
<!-- CSS は <style> タグでインライン（外部ファイルは参照しない） -->
<style>
  /* 新橋記事の <style> タグ全体をそのままコピーしてベースにする */
</style>
</head>
```

---

## 3. CSS 変数（ダークモード固定）

```css
:root {
  --bg: #121212; --bg-2: #1c1c1c; --bg-3: #242424;
  --fg: #f0f0f0; --fg-2: #d8d8d8; --fg-3: #a8a8a8; --fg-4: #686868;
  --teal: #79f1a4; --teal-2: #4dd68a;
  --line: rgba(255,255,255,.08); --line-2: rgba(255,255,255,.13);
  --fd: 'Noto Sans JP', -apple-system, 'system-ui', sans-serif;
  --fb: 'Georgia', 'Times New Roman', serif;
}
```

---

## 4. article 内の構造（順番）

```html
<article class="j-article">

  <!-- eyebrow：カテゴリ / 日付 / 読了時間 -->
  <div class="j-article-eyebrow">
    <span class="j-article-cat">エリアガイド</span>
    <span>—</span>
    <time datetime="2026-05-XX">2026.05.XX</time>
    <span>—</span>
    <span>X min read</span>
  </div>

  <!-- タイトル -->
  <h1 class="j-article-title">...</h1>

  <!-- メタ：ライター / 担当 / ハッシュタグ -->
  <div class="j-article-meta">
    <a href="/journal/writers/ライタースラッグ/" class="j-writer-link">
      <span class="j-writer-dot" style="background:#色">文字</span>
      <span>ライター名</span>
    </a>
    <span class="j-meta-sep">·</span>
    <span>担当エリア</span>
    <span class="j-meta-sep">·</span>
    <span>#タグ #タグ</span>
  </div>

  <!-- ヒーロー SVG -->
  <div class="j-hero-img">
    <svg viewBox="0 0 1200 675" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
      <!-- ダークグラデーション背景 + テキスト -->
    </svg>
  </div>

  <!-- 本文 -->
  <div class="j-article-body">

    <p class="j-lead">導入文（17px・太め）</p>

    <p>本文...</p>

    <p class="j-pullquote">「引用フレーズ」</p>

    <!-- 施設セクション（各施設ごとに繰り返す） -->
    <h2 id="sec-01">
      <span class="j-num">No.01</span>施設名
      <span class="j-en">英語サブタイトル</span>
    </h2>

    <p>施設説明文...</p>

    <!-- Instagram embed（直リンク画像禁止・blockquote または iframe のみ） -->
    <div class="j-ig-embed-wrap">
      <!-- Instagram公式 blockquote embed コードをそのまま貼る -->
      <blockquote class="instagram-media" data-instgrm-captioned
        data-instgrm-permalink="https://www.instagram.com/アカウント名/"
        data-instgrm-version="14"
        style="background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin:1px; max-width:540px; min-width:326px; padding:0; width:99.375%;">
        <div style="padding:16px;">
          <a href="https://www.instagram.com/アカウント名/" style="background:#FFFFFF; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank">施設名 (@アカウント名) on Instagram</a>
        </div>
      </blockquote>
      <script async src="//www.instagram.com/embed.js"></script>
    </div>
    <div class="j-ig-caption">via @アカウント名 on Instagram</div>

    <!-- 施設情報（dt/dd タグ必須、span は使わない） -->
    <div class="j-info-box">
      <div class="j-info-row"><dt>住所</dt><dd>...</dd></div>
      <div class="j-info-row"><dt>アクセス</dt><dd>...</dd></div>
      <div class="j-info-row"><dt>料金</dt><dd>...</dd></div>
      <div class="j-info-row"><dt>営業時間</dt><dd>...</dd></div>
      <div class="j-info-row"><dt>特徴</dt><dd>...</dd></div>
      <div class="j-info-row"><dt>公式</dt><dd><a href="..." target="_blank" rel="noopener">URL</a></dd></div>
      <div class="j-info-row j-sns-line"><dt>SNS</dt><dd>
        <a href="https://www.instagram.com/..." target="_blank" rel="noopener noreferrer" class="j-sns-pill">Instagram</a>
        <!-- X / note なども同様 -->
      </dd></div>
    </div>

    <!-- 中間 CTA（記事中盤に1回） -->
    <div class="j-mid-cta">
      <p>ここまで読んで「他のエリアも気になる」「建築家から探したい」と思った方は、<a href="/spaces">COWORKMILL の施設一覧</a>からエリア・建築家・写真別に検索できます。</p>
    </div>

    <!-- Conclusion h2 -->
    <h2 id="sec-conclusion">
      <span class="j-num">Conclusion</span>まとめタイトル
      <span class="j-en">英語サブタイトル</span>
    </h2>

    <p>まとめ文...</p>

    <!-- ライターカード -->
    <div class="j-writer-card">
      <span class="j-avatar">文字</span>
      <span class="j-w-body">
        <span class="j-w-eyebrow">Written by</span>
        <div class="j-w-name">ライター名</div>
        <div class="j-w-bio">プロフィール文...</div>
        <span class="j-w-link">記者プロフィールを見る →</span>
      </span>
    </div>

    <!-- Related -->
    <div class="j-related">
      <div class="j-related-h">More from COWORKMILL journal</div>
      <p class="j-related-msg">他の街・テーマの記事も準備中です。最新の更新は <a href="/journal/">journalトップ</a> から。</p>
    </div>

    <!-- End CTA -->
    <section class="j-end-cta">
      <div class="j-end-cta-bg-img"></div>
      <div class="j-end-cta-bg-overlay"></div>
      <div class="j-end-cta-logo"><img src="/shared/coworkmill-logo.svg" alt="COWORKMILL"></div>
      <div class="j-end-cta-eyebrow">— Find more —</div>
      <h3>エリアだけじゃない。<br>全国の「デザインで選ぶ」コワーキング。</h3>
      <p>COWORKMILL は、デザイン性に優れたコワーキング・シェアオフィスを、<br>エリア・建築家・写真から探せる日本初の編集型データベースです。</p>
      <div class="j-end-cta-btns">
        <a href="/spaces" class="j-end-cta-btn j-end-cta-primary">→ コワーキングを探す</a>
        <a href="/architects" class="j-end-cta-btn">→ 建築家から探す</a>
        <a href="/photos" class="j-end-cta-btn">→ 写真から探す</a>
      </div>
    </section>

  </div><!-- /.j-article-body -->

</article>
```

---

## 5. 右サイドバー（aside.j-sidebar）の構造

```html
<aside class="j-sidebar">
  <div class="j-sidebar-sticky">

    <!-- ① COWORKMILLバナー -->
    <div class="j-side-block">
      <div class="j-side-banner">
        <strong>デザインコワーキングポータル<br>COWORKMILL</strong>
        デザイン性に優れたコワーキングを、エリア・建築家・写真から探せる編集型データベース。
        <a href="/spaces">COWORKMILL を使う →</a>
      </div>
    </div>

    <!-- ② 目次（Contents）-->
    <div class="j-side-block">
      <div class="j-side-h">Contents</div>
      <ul class="j-toc-list" id="toc-list">
        <li><a href="#sec-01">No.01 施設名</a></li>
        <!-- ... -->
        <li><a href="#sec-conclusion">Conclusion</a></li>
      </ul>
    </div>

    <!-- ③ 最新記事（Latest）-->
    <div class="j-side-block">
      <div class="j-side-h">Latest</div>
      <ul class="j-side-list">
        <li><a href="/journal/スラッグ/">
          <span class="j-side-thumb"><img src="/journal/スラッグ/og-image.svg" alt=""></span>
          <span class="j-side-body">
            <span class="j-side-title">記事タイトル</span>
            <span class="j-side-meta">2026.05.XX</span>
          </span>
        </a></li>
      </ul>
    </div>

    <!-- ④ 人気記事（Popular）ランキングバッジ付き -->
    <div class="j-side-block">
      <div class="j-side-h">Popular</div>
      <ul class="j-side-list">
        <li><a href="/journal/スラッグ/">
          <span class="j-side-thumb">
            <span class="j-side-rank">01</span>  <!-- バッジ -->
            <img src="/journal/スラッグ/og-image.svg" alt="">
          </span>
          <span class="j-side-body">
            <span class="j-side-title">記事タイトル</span>
            <span class="j-side-meta">2026.05.XX</span>
          </span>
        </a></li>
      </ul>
    </div>

    <!-- ⑤ Writers（現在コメントアウト中） -->

    <!-- ⑥ タグクラウド（Topics）-->
    <div class="j-side-block">
      <div class="j-side-h">Topics</div>
      <div class="j-side-tags">
        <a href="/journal/?tag=タグ名" class="j-side-tag j-side-tag-lg">#タグ名</a>  <!-- 大 -->
        <a href="/journal/?tag=タグ名" class="j-side-tag">#タグ名</a>  <!-- 小 -->
      </div>
    </div>

    <!-- ⑦ Find a Space -->
    <div class="j-side-block">
      <div class="j-side-h">Find a Space</div>
      <div class="j-side-find">
        <a href="/spaces">コワーキングを探す</a>
        <a href="/architects">建築家から探す</a>
        <a href="/photos">写真から探す</a>
      </div>
    </div>

    <!-- ⑧ OFFICEMILLバナー -->
    <div class="j-side-block">
      <div class="j-side-banner">
        <strong>オフィス環境ポータル</strong>
        快適なオフィス環境はOFFICEMILLへ
        <a href="https://offml.com/" target="_blank" rel="noopener">OFFICEMILL →</a>
      </div>
    </div>

  </div>
</aside>
```

---

## 6. h2 の構造（施設番号 + 英語サブタイトル）

```html
<!-- id は必須（TOCリンクターゲット）-->
<h2 id="sec-01">
  <span class="j-num">No.01</span>施設名
  <span class="j-en">英語サブタイトル（イタリック小文字）</span>
</h2>

<h2 id="sec-conclusion">
  <span class="j-num">Conclusion</span>まとめタイトル
  <span class="j-en">英語サブタイトル</span>
</h2>
```

---

## 7. info-box のルール

```html
<!-- ❌ 禁止：span.j-info-label は使わない -->
<div class="j-info-row"><span class="j-info-label">住所</span><span>...</span></div>

<!-- ✅ 正解：dt / dd タグを使う -->
<div class="j-info-row"><dt>住所</dt><dd>...</dd></div>
```

---

## 8. Instagram embed のルール

```
❌ 禁止：<img src="https://www.instagram.com/p/.../media/..."> （直リンク画像）
✅ 正解：Instagram 公式 blockquote embed コードをそのまま使う
```

Instagram のプロフィールページ URL を `data-instgrm-permalink` に指定する場合：
```html
data-instgrm-permalink="https://www.instagram.com/アカウント名/"
```

---

## 9. articles.json への登録

新記事を追加する際は `journal/articles.json` の先頭に追記：

```json
{
  "status": "draft",        // 公開前は必ず draft
  "slug": "スラッグ名",
  "title": "記事タイトル",
  "cat": "エリアガイド",    // または 用途・テーマ
  "date": "2026-05-XX",
  "min": X,
  "writer": "ライター名",
  "tags": ["タグ1", "タグ2"],
  "og": "/journal/スラッグ名/og-image.svg"
}
```

---

## 10. 新記事作成時のチェックリスト

記事を書く前：
- [ ] 新橋記事の HTML を GitHub で開いてフルスキャン（article + sidebar + CSS + JS すべて）
- [ ] 施設名・エリア・Instagram URL を航さんに共有して確認を取る
- [ ] articles.json に status: "draft" で登録

記事作成中：
- [ ] CSS は新橋記事の `<style>` タグをベースにする（外部 CSS ファイルは参照しない）
- [ ] `<main class="j-page-grid">` でラップ（`<main class="j-main">` は旧フォーマット、使用禁止）
- [ ] h2 に `id="sec-XX"` を付与（TOC リンク用）
- [ ] info-row は `<dt>/<dd>` タグ（`<span>` は禁止）
- [ ] Instagram は公式 blockquote embed のみ（直リンク禁止）
- [ ] `j-mid-cta`（中間 CTA）を記事の中盤に1回挿入
- [ ] `j-writer-card` を Conclusion の後に挿入
- [ ] サイドバーの Latest / Popular を最新の記事リストに更新

公開前：
- [ ] 航さんに施設名・内容を共有して最終確認を取る
- [ ] プレビューページを作成して確認してもらう
- [ ] Instagram URL が揃っていることを確認
- [ ] articles.json の status を "live" に変更して commit

---

## 11. 現在の記事一覧と担当ライター

| スラッグ | タイトル | ライター | 公開日 | status |
|---|---|---|---|---|
| `shimbashi-toranomon-coworking-2026` | 新橋エリア 6選 | ヨシキ部長 | 2026-05-12 | live |
| `gotanda-design-coworking-2026` | 五反田 4選 | コーヒー部長 | 2026-05-10 | live |
| `shibuya-creators-coworking-2026` | 渋谷 5選 | ハルカ部長 | - | draft |

---

## 12. ディレクトリ構造

```
journal/
├── articles.json               ← 全記事一覧（Topページが参照）
├── _claude-handover/
│   ├── business-roadmap.md     ← 事業ロードマップ
│   └── journal-format-guide.md ← このファイル（記事フォーマット）
├── shimbashi-toranomon-coworking-2026/
│   ├── index.html              ← 記事本体（フォーマット基準）
│   └── og-image.svg            ← OGP画像
├── gotanda-design-coworking-2026/
│   ├── index.html
│   └── og-image.svg
└── shibuya-creators-coworking-2026/
    ├── index.html              ← Instagram URL 待ち・draft
    └── og-image.svg
```

---

## 13. 要注意：旧フォーマット（五反田記事の元の状態）との違い

五反田記事は 2026-05-15 に新橋記事フォーマットに合わせて修正済み。 以前の構造は**廃止**。

| 項目 | 旧（廃止） | 新（正解） |
|---|---|---|
| メインラッパー | `<main class="j-main">` | `<main class="j-page-grid">` |
| サイドバー | なし | `<aside class="j-sidebar">` あり |
| SNS縦バー | なし | `<aside class="j-share-vbar">` あり |
| 進捗バー | なし | `<div class="j-progress">` あり |
| info-row | `<span class="j-info-label">` | `<dt>/<dd>` タグ |

---

_最終更新：2026-05-15 / 記事フォーマット確立（新橋記事を基準に統一）_
