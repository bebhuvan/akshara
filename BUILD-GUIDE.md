# Akshara Build Guide

A thoughtful, opinionated guide for implementing this design system with Hugo and Cloudflare Workers. Written for developers who value clean architecture over defensive coding.

---

## Philosophy

**Write code that serves the reader, not code that serves other code.**

This isn't a SaaS product with feature flags and multi-tenancy. It's a literary archive. Your content structure should reflect this: books have chapters, authors have works, collections have themes. Don't abstract for flexibility you don't need.

**Hugo is a compiler, not a runtime.** Use it that way. Compute at build time, not in the browser. Generate the HTML you need, ship it, done.

**Mobile readers are your primary audience.** In India, most traffic comes from phones. Design for thumbs, optimize for 3G, make text readable on small screens. Desktop is a bonus, not the baseline.

**Speed is a feature.** Every 100ms of delay loses readers. Optimize ruthlessly. Fast builds, fast deploys, fast page loads, fast reading startup.

---

## Project Structure

```
akshara/
├── .git/
├── .gitignore
├── hugo.toml                    # Configuration
├── content/
│   ├── books/
│   │   ├── _index.md
│   │   └── gandhi-my-experiments/
│   │       ├── _index.md        # Book metadata
│   │       └── chapters/
│   │           ├── _index.md
│   │           ├── 01-birth.md
│   │           ├── 02-childhood.md
│   │           └── 03-child-marriage.md
│   ├── authors/
│   │   ├── _index.md
│   │   └── gandhi.md
│   ├── collections/
│   │   ├── _index.md
│   │   └── freedom-struggle.md
│   └── pages/
│       ├── about.md
│       └── contribute.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html          # Base template
│   │   ├── list.html
│   │   └── single.html
│   ├── index.html               # Homepage
│   ├── books/
│   │   ├── list.html            # All books
│   │   └── single.html          # Book hub
│   ├── chapters/
│   │   └── single.html          # Reading experience
│   ├── authors/
│   │   ├── list.html
│   │   └── single.html
│   ├── collections/
│   │   ├── list.html
│   │   └── single.html
│   ├── partials/
│   │   ├── head.html
│   │   ├── header.html
│   │   ├── footer.html
│   │   └── book-card.html
│   └── 404.html
├── static/
│   ├── fonts/                   # Self-hosted fonts (optional)
│   ├── covers/                  # Book cover images
│   └── js/
│       └── reading.js           # Reading page interactions
├── assets/
│   └── css/
│       ├── base.css             # CSS variables, resets
│       ├── components.css       # Reusable components
│       └── pages.css            # Page-specific styles
└── public/                      # Generated (gitignored)
```

---

## Hugo Configuration

**hugo.toml** - Keep it simple. No feature flags, no "maybe later" options.

```toml
baseURL = "https://akshara.dhwani.ink"
languageCode = "en-us"
title = "Akshara"
theme = ""  # No theme, layouts in root

# Performance
buildFuture = false
buildExpired = false
buildDrafts = false

# Taxonomies - only what you need
[taxonomies]
  author = "authors"
  collection = "collections"
  theme = "themes"
  period = "periods"
  language = "languages"

# Permalinks - clean URLs
[permalinks]
  books = "/books/:slug"
  chapters = "/books/:section/:slug"
  authors = "/authors/:slug"
  collections = "/collections/:slug"

# Markdown rendering
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # Allow HTML in markdown
  [markup.highlight]
    style = "monokai"
    lineNos = false

# Output formats
[outputs]
  home = ["HTML"]
  page = ["HTML"]
  section = ["HTML"]
  taxonomy = ["HTML"]
  term = ["HTML"]

# Minification
[minify]
  disableCSS = false
  disableHTML = false
  disableJS = true  # Minify manually, Hugo's JS minifier is basic
  disableJSON = false
  disableSVG = false
  disableXML = false

# Image processing
[imaging]
  quality = 85
  resampleFilter = "Lanczos"
  anchor = "Smart"

# Privacy (no analytics by default)
[privacy]
  [privacy.youtube]
    privacyEnhanced = true
```

---

## Content Modeling

### Book Front Matter

**content/books/gandhi-my-experiments/_index.md**

```yaml
---
title: "My Experiments with Truth"
author: "Mahatma Gandhi"
author_slug: "gandhi"
translator: "Mahadev Desai"
year: 1927
published: 1927-01-01
language: "English"
original_language: "Gujarati"

# Metadata
pages: 454
word_count: 98456
reading_time: 480  # minutes
chapters: 164

# Taxonomies
authors: ["gandhi"]
collections: ["freedom-struggle"]
themes: ["autobiography", "philosophy", "nonviolence"]
periods: ["1901-1930"]
languages: ["English"]

# Downloads & Sources
archive_url: "https://archive.org/details/myexperimentswit00gand"
wikipedia_url: "https://en.wikipedia.org/wiki/The_Story_of_My_Experiments_with_Truth"
wikisource_url: "https://en.wikisource.org/wiki/The_Story_of_My_Experiments_with_Truth"
download_epub: "/downloads/gandhi-experiments.epub"
download_md: "/downloads/gandhi-experiments.md"
download_txt: "/downloads/gandhi-experiments.txt"

# Content
description: "An intimate autobiography chronicling Gandhi's spiritual and political awakening, from his childhood in Gujarat to his development of satyagraha in South Africa."

# Image
cover: "/covers/gandhi-experiments.jpg"

# Digitization info
digitized_from: "1948 edition scanned by Archive.org"
digitization_method: "Tesseract OCR, manually corrected"
---

Gandhi's autobiography, originally serialized in Gujarati between 1925 and 1929, offers an unflinchingly honest account of his moral and spiritual development. He writes candidly about his failures and mistakes, presenting them not as confessions but as lessons learned in his lifelong pursuit of truth.

[More context - this becomes the "About This Work" section]
```

### Chapter Front Matter

**content/books/gandhi-my-experiments/chapters/03-child-marriage.md**

```yaml
---
title: "Child Marriage"
chapter_number: 3
chapter_title: "Chapter Three"
reading_time: 12  # minutes
word_count: 2840
weight: 3  # For ordering

# Navigation
prev: "/books/gandhi-my-experiments/chapters/02-childhood"
next: "/books/gandhi-my-experiments/chapters/04-playing-the-husband"
---

Much as I wish that I had not to write this chapter, I know that I shall have to swallow many such bitter draughts in the course of this narrative...

[Full chapter text in markdown]
```

### Author Front Matter

**content/authors/gandhi.md**

```yaml
---
title: "Mahatma Gandhi"
full_name: "Mohandas Karamchand Gandhi"
birth_year: 1869
death_year: 1948
birth_place: "Porbandar, Gujarat"
languages: ["Gujarati", "English"]

# Bio
short_bio: "Indian lawyer, anti-colonial nationalist, and political ethicist who employed nonviolent resistance to lead the successful campaign for India's independence."

# Works
works_count: 8
first_publication: 1893

# External
wikipedia_url: "https://en.wikipedia.org/wiki/Mahatma_Gandhi"
wikisource_url: "https://en.wikisource.org/wiki/Author:Mohandas_Karamchand_Gandhi"

# Timeline events (for timeline display)
timeline:
  - year: 1893
    title: "Arrival in South Africa"
    description: "Experienced racial discrimination that awakened his consciousness about injustice."
  - year: 1909
    title: "Hind Swaraj Published"
    description: "Wrote his political manifesto during a voyage from London to South Africa."
  - year: 1915
    title: "Return to India"
    description: "Established Sabarmati Ashram in Ahmedabad."
  - year: 1927
    title: "Autobiography Published"
    description: "My Experiments with Truth published in English translation."
  - year: 1930
    title: "Salt March"
    description: "Led the 240-mile Salt March to protest British salt monopoly."
  - year: 1942
    title: "Quit India Movement"
    description: "Launched the movement demanding immediate British withdrawal."
---

Mohandas Karamchand Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist who employed nonviolent resistance to lead the successful campaign for India's independence from British rule. His philosophy of satyagraha and commitment to truth and non-violence profoundly influenced civil rights and freedom movements worldwide.

[Full biography]
```

### Collection Front Matter

**content/collections/freedom-struggle.md**

```yaml
---
title: "Freedom Struggle"
description: "Political treatises and personal accounts from India's independence movement."
long_description: "Political treatises, personal memoirs, and revolutionary writings from India's independence movement. These works capture the intellectual and moral foundations of the struggle against colonial rule."

# Stats
book_count: 42
author_count: 23
earliest_year: 1893
latest_year: 1954

# Context
historical_context: "From the late 19th century through 1954, Indian intellectuals and activists developed sophisticated arguments for self-rule and documented their resistance to British colonialism. These writings laid the philosophical groundwork for independence and influenced anti-colonial movements worldwide."

# Featured books (for homepage)
featured_books:
  - "gandhi-my-experiments"
  - "nehru-discovery-of-india"
  - "gandhi-hind-swaraj"
---
```

---

## Template Architecture

### Base Template

**layouts/_default/baseof.html** - Every page extends this.

```html
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
    {{ partial "head.html" . }}
</head>
<body>
    {{ block "main" . }}{{ end }}
</body>
</html>
```

**That's it.** No header/footer in baseof. Why? Because:
- Homepage doesn't need a header
- Reading page has a different header
- 404 page has minimal header

Each page template includes what it needs. Don't create abstraction for DRY when the repetition is intentional.

### Head Partial

**layouts/partials/head.html**

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ if .Title }}{{ .Title }} - {{ end }}{{ .Site.Title }}</title>
<meta name="description" content="{{ .Params.description | default .Summary | default .Site.Params.description }}">

<!-- Open Graph -->
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ .Params.description | default .Summary }}">
{{ with .Params.cover }}<meta property="og:image" content="{{ . | absURL }}">{{ end }}
<meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<!-- Styles - Single compiled CSS -->
{{ $base := resources.Get "css/base.css" }}
{{ $components := resources.Get "css/components.css" }}
{{ $pages := resources.Get "css/pages.css" }}
{{ $css := slice $base $components $pages | resources.Concat "css/akshara.css" | minify | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}" integrity="{{ $css.Data.Integrity }}">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
```

**No conditional loading.** Ship one CSS file. It's <50KB minified. HTTP/2 makes multiple requests cheap, but cache invalidation makes them expensive. One file, one cache key, done.

### Homepage

**layouts/index.html**

```html
{{ define "main" }}
<!-- Header -->
<header class="header">
    <div class="header-inner">
        <a href="{{ .Site.BaseURL }}" class="logo">AKSHARA</a>
        <nav class="nav">
            <a href="/books">Browse</a>
            <a href="/collections">Collections</a>
            <a href="/authors">Authors</a>
            <a href="/about">About</a>
        </nav>
    </div>
</header>

<!-- Hero -->
<section class="hero">
    <h1>An archive of Indian literature, <em>preserved</em> for generations</h1>
    <p class="hero-subtitle">{{ .Site.Params.description }}</p>
    
    <div class="hero-stats">
        {{ $bookCount := len (where .Site.Pages "Type" "books") }}
        {{ $authorCount := len (where .Site.Pages "Type" "authors") }}
        {{ $languages := .Site.Taxonomies.languages }}
        
        <div class="stat">
            <div class="stat-number">{{ $bookCount }}</div>
            <div class="stat-label">Books</div>
        </div>
        <div class="stat">
            <div class="stat-number">{{ $authorCount }}</div>
            <div class="stat-label">Authors</div>
        </div>
        <div class="stat">
            <div class="stat-number">{{ len $languages }}</div>
            <div class="stat-label">Languages</div>
        </div>
    </div>
</section>

<!-- Featured Book -->
{{ with .Site.Params.featured_book }}
    {{ with $.Site.GetPage (printf "/books/%s" .) }}
    <section class="featured">
        <div class="featured-book">
            <div class="featured-visual">
                {{ with .Params.featured_quote }}
                <blockquote class="featured-quote">{{ . | markdownify }}</blockquote>
                {{ end }}
            </div>
            <div class="featured-content">
                <div class="featured-label">Recently Digitized</div>
                <h2 class="featured-title">{{ .Title }}</h2>
                <p class="featured-author">{{ .Params.author }}, {{ .Params.year }}</p>
                <p class="featured-excerpt">{{ .Params.description }}</p>
                <a href="{{ .RelPermalink }}" class="btn-primary">Begin Reading</a>
            </div>
        </div>
    </section>
    {{ end }}
{{ end }}

<!-- Collections -->
<section class="collections">
    <div class="collections-inner">
        <div class="section-header">
            <h2 class="section-title">Collections</h2>
            <a href="/collections" class="section-link">View all →</a>
        </div>

        <div class="collections-grid">
            {{ range $index, $page := (where .Site.RegularPages "Type" "collections") }}
            <a href="{{ .RelPermalink }}" class="collection-card">
                <div class="collection-number">{{ printf "%02d" (add $index 1) }}</div>
                <h3 class="collection-name">{{ .Title }}</h3>
                <div class="collection-count">{{ .Params.book_count }} Books</div>
                <p class="collection-description">{{ .Params.description }}</p>
            </a>
            {{ end }}
        </div>
    </div>
</section>

<!-- Recent Books -->
<section class="recent">
    <div class="section-header">
        <h2 class="section-title">Recent Additions</h2>
        <a href="/books" class="section-link">View all books →</a>
    </div>

    <div class="books-grid">
        {{ range first 12 (where .Site.RegularPages "Type" "books").ByDate.Reverse }}
            {{ partial "book-card.html" . }}
        {{ end }}
    </div>
</section>

<!-- Footer -->
{{ partial "footer.html" . }}
{{ end }}
```

**Notice:**
- No "if featured book exists" checks - configure it or don't, fail fast
- No null checks on collections - if you don't have collections, the site is broken anyway
- Direct Hugo functions, no custom helpers for simple counts

### Book Hub

**layouts/books/single.html**

```html
{{ define "main" }}
{{ partial "header.html" . }}

<!-- Book Hero -->
<section class="hero">
    <div class="book-cover-area">
        {{ with .Params.cover }}
        <img src="{{ . }}" alt="{{ $.Title }} cover" class="book-cover">
        {{ else }}
        <div class="book-cover"></div>
        {{ end }}
        
        <div class="book-meta-compact">
            <div class="meta-item-compact">
                <div class="meta-label-compact">Published</div>
                <div class="meta-value-compact">{{ .Params.year }}</div>
            </div>
            <div class="meta-item-compact">
                <div class="meta-label-compact">Language</div>
                <div class="meta-value-compact">{{ .Params.language }}</div>
            </div>
            {{ with .Params.translator }}
            <div class="meta-item-compact">
                <div class="meta-label-compact">Translator</div>
                <div class="meta-value-compact">{{ . }}</div>
            </div>
            {{ end }}
            <div class="meta-item-compact">
                <div class="meta-label-compact">Pages</div>
                <div class="meta-value-compact">{{ .Params.pages }}</div>
            </div>
        </div>
    </div>
    
    <div class="book-info">
        <h1>{{ .Title }}</h1>
        <p class="book-author">{{ .Params.author }}</p>
        
        <div class="actions">
            {{ with .GetPage "chapters" }}
                {{ with .Pages }}
                    {{ $firstChapter := index . 0 }}
                    <a href="{{ $firstChapter.RelPermalink }}" class="btn-start">Begin Reading</a>
                {{ end }}
            {{ end }}
            <a href="#toc" class="btn-secondary">Table of Contents</a>
        </div>

        <div class="quick-meta">
            <div class="quick-meta-item">
                <div class="quick-label">Reading Time</div>
                <div class="quick-value">~{{ div .Params.reading_time 60 }} hours</div>
            </div>
            <div class="quick-meta-item">
                <div class="quick-label">Chapters</div>
                <div class="quick-value">{{ .Params.chapters }}</div>
            </div>
            {{ with .Params.period }}
            <div class="quick-meta-item">
                <div class="quick-label">Period</div>
                <div class="quick-value">{{ . }}</div>
            </div>
            {{ end }}
        </div>
    </div>
</section>

<!-- Main Content -->
<div class="main-content">
    <div class="content-primary">
        <!-- About -->
        <section class="section">
            <h2 class="section-title">About This Work</h2>
            <div class="context-text">
                {{ .Content }}
            </div>
        </section>

        <!-- TOC -->
        <section class="section" id="toc">
            <h2 class="section-title">Contents</h2>
            <ul class="toc-list">
                {{ with .GetPage "chapters" }}
                    {{ range .Pages.ByWeight }}
                    <li class="toc-item">
                        <a href="{{ .RelPermalink }}">
                            <span class="toc-num">{{ .Params.chapter_number }}</span>
                            <span>{{ .Title }}</span>
                        </a>
                    </li>
                    {{ end }}
                {{ end }}
            </ul>
        </section>

        <!-- Archive Embed -->
        {{ with .Params.archive_url }}
        <section class="section">
            <h2 class="section-title">Original Source</h2>
            <iframe src="{{ . }}?view=theater" class="archive-embed" frameborder="0"></iframe>
        </section>
        {{ end }}
    </div>

    <!-- Sidebar -->
    <aside class="sidebar">
        <!-- Downloads -->
        <div class="sidebar-section">
            <h3 class="sidebar-title">Download</h3>
            <ul class="download-list">
                {{ with .Params.download_epub }}
                <li class="download-item">
                    <a href="{{ . }}">
                        <span>EPUB</span>
                        <span class="download-size">{{ partial "filesize.html" . }}</span>
                    </a>
                </li>
                {{ end }}
                {{ with .Params.download_md }}
                <li class="download-item">
                    <a href="{{ . }}">
                        <span>Markdown</span>
                        <span class="download-size">{{ partial "filesize.html" . }}</span>
                    </a>
                </li>
                {{ end }}
                {{ with .Params.download_txt }}
                <li class="download-item">
                    <a href="{{ . }}">
                        <span>Plain Text</span>
                        <span class="download-size">{{ partial "filesize.html" . }}</span>
                    </a>
                </li>
                {{ end }}
            </ul>
        </div>

        <!-- References -->
        <div class="sidebar-section">
            <h3 class="sidebar-title">References</h3>
            <ul class="reference-list">
                {{ with .Params.wikipedia_url }}
                <li class="reference-item"><a href="{{ . }}">Wikipedia</a></li>
                {{ end }}
                {{ with .Params.wikisource_url }}
                <li class="reference-item"><a href="{{ . }}">Wikisource</a></li>
                {{ end }}
                {{ with .Params.archive_url }}
                <li class="reference-item"><a href="{{ . }}">Archive.org Source</a></li>
                {{ end }}
            </ul>
        </div>

        <!-- Digitization -->
        {{ with .Params.digitized_from }}
        <div class="sidebar-section">
            <h3 class="sidebar-title">Digitization</h3>
            <p class="digitization-note">
                Digitized from {{ . }}. {{ $.Params.digitization_method }}. Historical spelling and punctuation preserved.
            </p>
        </div>
        {{ end }}
    </aside>
</div>
{{ end }}
```

### Reading Experience

**layouts/chapters/single.html**

This is the most complex template. Critical points:

```html
{{ define "main" }}
<!-- Progress -->
<div class="progress" id="progress"></div>

<!-- Top Bar -->
<div class="top-bar" id="topBar">
    <div class="top-bar-inner">
        <div class="top-left">
            {{ $book := .Parent.Parent }}
            <a href="{{ $book.RelPermalink }}" class="back">← Back</a>
            <span class="book-compact">{{ $book.Title }}</span>
        </div>
        <div class="top-center">
            {{ $chapters := $book.GetPage "chapters" }}
            {{ $totalChapters := len $chapters.Pages }}
            Chapter {{ .Params.chapter_number }} of {{ $totalChapters }} · 
            <span class="reading-time">~{{ .Params.reading_time }} min</span>
        </div>
        <div class="top-right">
            <button class="top-btn" onclick="toggleTOC()">Contents</button>
            <button class="top-btn" onclick="toggleControls()">Settings</button>
            <button class="top-btn" onclick="toggleFocusMode()">Focus</button>
        </div>
    </div>
</div>

<!-- Reading Container -->
<main class="reading">
    <header class="chapter-header">
        <div class="chapter-number">{{ .Params.chapter_title }}</div>
        <h1 class="chapter-title">{{ .Title }}</h1>
        <div class="chapter-meta">~{{ .Params.reading_time }} minute read</div>
    </header>

    <article class="text">
        {{ .Content }}
    </article>

    <!-- Chapter Navigation -->
    <nav class="chapter-nav">
        {{ with .Params.prev }}
        <a href="{{ . }}" class="nav-link prev">
            {{ with $.Site.GetPage . }}
            <span class="nav-label">Previous</span>
            <span class="nav-title">{{ .Title }}</span>
            {{ end }}
        </a>
        {{ end }}

        {{ with .Params.next }}
        <a href="{{ . }}" class="nav-link next">
            {{ with $.Site.GetPage . }}
            <span class="nav-label">Next</span>
            <span class="nav-title">{{ .Title }}</span>
            {{ end }}
        </a>
        {{ end }}
    </nav>
</main>

<!-- TOC Drawer -->
<aside class="toc" id="toc">
    {{ $book := .Parent.Parent }}
    {{ $chapters := $book.GetPage "chapters" }}
    <div class="toc-header">
        <div class="toc-book">{{ $book.Title }}</div>
        <div class="toc-author">{{ $book.Params.author }}</div>
        <div class="toc-progress">
            {{ .Params.chapter_number }} of {{ len $chapters.Pages }} chapters · 
            {{ $progress := div (mul .Params.chapter_number 100) (len $chapters.Pages) }}
            {{ $progress }}% complete
            <div class="toc-progress-bar">
                <div class="toc-progress-fill" style="width: {{ $progress }}%"></div>
            </div>
        </div>
        <button class="toc-close" onclick="toggleTOC()">×</button>
    </div>
    <div class="toc-content">
        <div class="toc-section-title">Chapters</div>
        <ul class="toc-list">
            {{ range $chapters.Pages.ByWeight }}
            <li>
                <a href="{{ .RelPermalink }}"{{ if eq .File.UniqueID $.File.UniqueID }} class="current"{{ end }}>
                    <span class="toc-num">{{ .Params.chapter_number }}</span>
                    <span>{{ .Title }}</span>
                </a>
            </li>
            {{ end }}
        </ul>
    </div>
</aside>

<!-- Reading Controls -->
<div class="controls" id="controls">
    <div class="controls-inner">
        <div class="control-group">
            <button class="control-btn" onclick="adjustSize(-2)">Smaller</button>
            <button class="control-btn active" onclick="adjustSize(0)">Default</button>
            <button class="control-btn" onclick="adjustSize(2)">Larger</button>
        </div>
        <div class="control-separator"></div>
        <div class="control-group">
            <button class="control-btn active" onclick="setTheme('light')">Light</button>
            <button class="control-btn" onclick="setTheme('dark')">Dark</button>
            <button class="control-btn" onclick="setTheme('sepia')">Sepia</button>
        </div>
    </div>
</div>

<!-- Overlay -->
<div class="overlay" id="overlay" onclick="closeAll()"></div>

<!-- Keyboard Shortcut Hint -->
<div class="shortcut-hint" id="shortcutHint"></div>

<!-- Reading interactions -->
<script src="/js/reading.js"></script>

<!-- Store position -->
<script>
    const chapterId = '{{ .File.UniqueID }}';
    const bookSlug = '{{ $book.File.BaseFileName }}';
</script>
{{ end }}
```

**Key decisions:**
- Hugo computes progress percentage at build time
- Chapter navigation uses front matter `prev`/`next` - explicit, not computed
- Current chapter detection via `UniqueID` - reliable across rebuilds
- JavaScript gets minimal data via inline script - book slug, chapter ID

---

## Reusable Partials

**layouts/partials/book-card.html**

```html
<a href="{{ .RelPermalink }}" class="book-card">
    {{ with .Params.cover }}
    <img src="{{ . }}" alt="{{ $.Title }} cover" class="book-cover" loading="lazy">
    {{ else }}
    <div class="book-cover"></div>
    {{ end }}
    <h3 class="book-title">{{ .Title }}</h3>
    <p class="book-author">{{ .Params.author }}</p>
    {{ with .Params.year }}
    <p class="book-year">{{ . }}</p>
    {{ end }}
</a>
```

**When to create a partial:**
- Used in 3+ places: Yes
- Complex logic that obscures the template: Yes
- "Might need to change it later": No

**When NOT to create a partial:**
- Used twice with different contexts
- Premature abstraction
- "Following best practices"

---

## CSS Architecture

**assets/css/base.css** - Variables, resets, typography

```css
/* Variables */
:root {
    --ink: #1a1412;
    --paper: #fffef9;
    --smoke: #6b6560;
    --ash: #9c948e;
    --sand: #e8e3dd;
    --cream: #f5f2ec;
    --terracotta: #c85a3a;
}

/* Dark theme overrides */
body.dark {
    --ink: #f5f2ec;
    --paper: #1a1412;
    --smoke: #9c948e;
    --ash: #6b6560;
    --sand: #3d3530;
    --cream: #2d2520;
    --terracotta: #e8754d;
}

/* Sepia theme overrides */
body.sepia {
    --ink: #2d2520;
    --paper: #f5f1e8;
    --smoke: #6b6560;
    --ash: #9c948e;
    --sand: #d9d3c8;
    --cream: #e8e3dd;
    --terracotta: #b85a3a;
}

/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Base typography */
body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: var(--paper);
    color: var(--ink);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

/* Selection */
::selection {
    background: rgba(200, 90, 58, 0.2);
    color: var(--ink);
}

/* Responsive images */
img {
    max-width: 100%;
    height: auto;
}
```

**assets/css/components.css** - Reusable patterns

```css
/* Header */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background: rgba(255, 254, 249, 0.9);
    backdrop-filter: blur(20px);
}

.header-inner {
    max-width: 1600px;
    margin: 0 auto;
    padding: 28px 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ... more components */
```

**assets/css/pages.css** - Page-specific overrides

```css
/* Homepage hero */
.hero h1 {
    font-family: 'Libre Baskerville', serif;
    font-size: 92px;
    /* ... */
}

/* Reading page specific */
.reading {
    max-width: 720px;
    /* ... */
}
```

**Don't:**
- Create utility classes (`.mt-4`, `.text-center`)
- Abstract too early
- Use CSS frameworks
- Write CSS for hypothetical future pages

**Do:**
- Name things semantically (`.hero`, `.book-card`)
- Repeat yourself if contexts differ
- Write CSS for pages that exist
- Use CSS variables for theming

---

## JavaScript Strategy

**static/js/reading.js** - The ONLY JavaScript file

```javascript
// State
let fontSize = 21;
let scrollTimeout;
let topBarVisible = true;
let focusMode = false;

// Get stored state
const bookSlug = document.currentScript.previousElementSibling.textContent.match(/bookSlug = '(.+)'/)?.[1];
const chapterId = document.currentScript.previousElementSibling.textContent.match(/chapterId = '(.+)'/)?.[1];
const storageKey = `${bookSlug}-${chapterId}`;

// Progress tracking
function updateProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    document.getElementById('progress').style.width = progress + '%';
}

window.addEventListener('scroll', () => {
    updateProgress();
    
    // Auto-hide top bar
    clearTimeout(scrollTimeout);
    if (window.scrollY > 100 && !focusMode) {
        document.getElementById('topBar').classList.add('hidden');
        topBarVisible = false;
    }
    
    scrollTimeout = setTimeout(() => {
        if (!topBarVisible && !focusMode) {
            document.getElementById('topBar').classList.remove('hidden');
            topBarVisible = true;
        }
    }, 1500);
});

// TOC drawer
function toggleTOC() {
    const toc = document.getElementById('toc');
    const overlay = document.getElementById('overlay');
    toc.classList.toggle('open');
    overlay.classList.toggle('show');
}

// Settings panel
function toggleControls() {
    document.getElementById('controls').classList.toggle('visible');
}

// Focus mode
function toggleFocusMode() {
    focusMode = !focusMode;
    document.body.classList.toggle('focus-mode');
    showShortcutHint(focusMode ? 'Focus mode on (Press F to exit)' : 'Focus mode off');
}

// Close all panels
function closeAll() {
    document.getElementById('toc').classList.remove('open');
    document.getElementById('overlay').classList.remove('show');
}

// Font size adjustment
function adjustSize(delta) {
    if (delta === 0) {
        fontSize = 21;
    } else {
        fontSize = Math.max(17, Math.min(27, fontSize + delta));
    }
    document.body.style.fontSize = fontSize + 'px';
    localStorage.setItem(`fontSize-${bookSlug}`, fontSize);
}

// Theme switching
function setTheme(theme) {
    document.body.className = theme === 'light' ? '' : theme;
    if (focusMode) document.body.classList.add('focus-mode');
    localStorage.setItem('theme', theme);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    switch(e.key.toLowerCase()) {
        case 't':
            e.preventDefault();
            toggleTOC();
            showShortcutHint('Table of Contents');
            break;
        case 's':
            e.preventDefault();
            toggleControls();
            showShortcutHint('Settings');
            break;
        case 'f':
            e.preventDefault();
            toggleFocusMode();
            break;
        case 'escape':
            closeAll();
            if (focusMode) toggleFocusMode();
            break;
    }
});

// Position memory
window.addEventListener('beforeunload', () => {
    localStorage.setItem(`scroll-${storageKey}`, window.scrollY);
});

window.addEventListener('load', () => {
    const savedPos = localStorage.getItem(`scroll-${storageKey}`);
    if (savedPos) window.scrollTo(0, parseInt(savedPos));
    
    const savedSize = localStorage.getItem(`fontSize-${bookSlug}`);
    if (savedSize) {
        fontSize = parseInt(savedSize);
        document.body.style.fontSize = fontSize + 'px';
    }
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme && savedTheme !== 'light') setTheme(savedTheme);
    
    updateProgress();
});

// Shortcut hints
function showShortcutHint(text) {
    const hint = document.getElementById('shortcutHint');
    hint.textContent = text;
    hint.classList.add('show');
    setTimeout(() => hint.classList.remove('show'), 2000);
}

// Show controls on mouse movement
let controlsTimeout;
document.addEventListener('mousemove', () => {
    if (focusMode) return;
    
    const controls = document.getElementById('controls');
    controls.classList.add('visible');
    
    clearTimeout(controlsTimeout);
    controlsTimeout = setTimeout(() => {
        controls.classList.remove('visible');
    }, 3000);
});

// Initial show
setTimeout(() => {
    if (!focusMode) document.getElementById('controls').classList.add('visible');
}, 1000);
```

**No build step. No TypeScript. No bundler. No npm.** Ship this file directly.

Why?
- It's 5KB minified
- Works in every browser from 2020+
- No dependencies, no vulnerabilities
- No build complexity
- You can read and modify it in production if needed

---

## Cloudflare Workers Deployment

### Why Workers Over Pages

**Control over caching** - Workers let you set precise cache rules per content type  
**Edge optimization** - Serve WebP to supporting browsers, JPEG to others  
**Smart redirects** - Handle `/books/slug` → `/books/slug/` without rebuild  
**Request modification** - Add security headers, modify responses  
**Future flexibility** - Can add simple APIs (download tracking) without rebuild

**Not using Workers for:**
- Server-side rendering (Hugo already did that)
- Database queries (everything is static)
- User authentication (not needed)
- Complex logic (keep it simple)

### Workers Setup

**wrangler.toml** - Configuration file

```toml
name = "akshara"
main = "src/index.js"
compatibility_date = "2024-01-01"

[site]
bucket = "./public"

[env.production]
name = "akshara"
route = "akshara.dhwani.ink/*"

[env.production.vars]
ENVIRONMENT = "production"
```

**src/index.js** - The Worker

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    // Security headers
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Permissions-Policy': 'camera=(), microphone=(), geolocation=()'
    };
    
    // Handle assets
    if (url.pathname.startsWith('/static/') || 
        url.pathname.startsWith('/covers/') ||
        url.pathname.startsWith('/js/')) {
      
      const response = await env.ASSETS.fetch(request);
      
      // Cache static assets for 1 year
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=31536000, immutable');
      
      return new Response(response.body, {
        status: response.status,
        headers
      });
    }
    
    // Handle HTML pages
    if (url.pathname.endsWith('.html') || !url.pathname.includes('.')) {
      const response = await env.ASSETS.fetch(request);
      
      if (response.status === 404) {
        return env.ASSETS.fetch(new Request(new URL('/404.html', url)));
      }
      
      const headers = new Headers(response.headers);
      
      // Add security headers
      Object.entries(securityHeaders).forEach(([key, value]) => {
        headers.set(key, value);
      });
      
      // Cache HTML for 1 hour (can be purged)
      headers.set('Cache-Control', 'public, max-age=3600, must-revalidate');
      
      return new Response(response.body, {
        status: response.status,
        headers
      });
    }
    
    // Everything else
    return env.ASSETS.fetch(request);
  }
};
```

### Build and Deploy Script

**scripts/deploy.sh**

```bash
#!/bin/bash
set -e

echo "Building Hugo site..."
hugo --gc --minify

echo "Running Pagefind..."
npx pagefind --site public --output-path public/pagefind

echo "Deploying to Cloudflare Workers..."
wrangler deploy

echo "✓ Deployment complete!"
```

### Initial Setup

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create Worker
wrangler init

# Deploy
bash scripts/deploy.sh
```

### Custom Domain

```bash
# Add route in wrangler.toml or via dashboard
wrangler routes add "akshara.dhwani.ink/*" akshara
```

Or in dashboard: Workers → Your Worker → Triggers → Add Custom Domain

### Git Workflow with Workers

```bash
# Make changes
git add .
git commit -m "Update: Add new book"
git push origin main

# Deploy (manual or CI)
bash scripts/deploy.sh
```

### Automated Deployment (GitHub Actions)

**.github/workflows/deploy.yml**

```yaml
name: Deploy to Cloudflare Workers

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.121.0'
          extended: true
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Build
        run: |
          hugo --gc --minify
          npx pagefind --site public
      
      - name: Deploy
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
```

Add `CLOUDFLARE_API_TOKEN` to GitHub repository secrets.

### Asset Storage (R2)

For large files (EPUBs, downloads):

**1. Create R2 bucket:**
```bash
wrangler r2 bucket create akshara-downloads
```

**2. Set up custom domain in Cloudflare Dashboard:**
- R2 → akshara-downloads → Settings → Public Access
- Add custom domain: `downloads.akshara.dhwani.ink`

**3. CORS policy for browser downloads:**

```json
[
  {
    "AllowedOrigins": ["https://akshara.dhwani.ink"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedHeaders": ["*"],
    "MaxAgeSeconds": 3600
  }
]
```

**4. Upload structure:**
```
/books/
  /gandhi-experiments/
    gandhi-experiments.epub      (EPUB download)
    gandhi-experiments.md         (Markdown source)
    gandhi-experiments.txt        (Plain text)
/covers/
  gandhi-experiments.jpg          (If not in Hugo static/)
```

**5. Upload via Wrangler:**

```bash
# Upload a file
wrangler r2 object put akshara-downloads/books/gandhi-experiments/gandhi-experiments.epub --file=./downloads/gandhi-experiments.epub

# Batch upload
cd downloads
for file in *.epub; do
    wrangler r2 object put akshara-downloads/books/${file%.epub}/$file --file=./$file
done
```

**6. Reference in front matter:**
```yaml
download_epub: "https://downloads.akshara.dhwani.ink/books/gandhi-experiments/gandhi-experiments.epub"
download_md: "https://downloads.akshara.dhwani.ink/books/gandhi-experiments/gandhi-experiments.md"
download_txt: "https://downloads.akshara.dhwani.ink/books/gandhi-experiments/gandhi-experiments.txt"
```

**7. Automate with build script:**

```bash
# scripts/upload-downloads.sh
#!/bin/bash

for book in content/books/*/; do
    slug=$(basename $book)
    
    if [ -f "downloads/${slug}.epub" ]; then
        echo "Uploading ${slug}.epub..."
        wrangler r2 object put akshara-downloads/books/${slug}/${slug}.epub \
            --file=downloads/${slug}.epub \
            --content-type="application/epub+zip"
    fi
done
```

**Why R2 over static assets:**
- EPUBs are 1-5MB each, too large for git
- Separate caching strategy (downloads cached longer)
- Bandwidth savings (R2 egress is free to Cloudflare)
- Easy updates without rebuilding entire site

---

## Search Implementation (Pagefind)

### Installation

```bash
npm install -D pagefind
```

### Hugo Configuration

Add to **hugo.toml**:

```toml
[outputs]
  home = ["HTML"]
  section = ["HTML"]
```

### Build Script

**scripts/build.sh**:

```bash
#!/bin/bash
set -e

# Build Hugo site
hugo --minify

# Run Pagefind
npx pagefind --site public --output-path public/pagefind

echo "Build complete!"
```

Make executable:
```bash
chmod +x scripts/build.sh
```

### Update Cloudflare Build Command

```
Build command: bash scripts/build.sh
```

### Search Page Template

**layouts/_default/search.html**:

```html
{{ define "main" }}
{{ partial "header.html" . }}

<div class="search-page">
    <div class="search-header">
        <h1>Search</h1>
        <div id="search"></div>
    </div>
    <div id="results"></div>
</div>

<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<script src="/pagefind/pagefind-ui.js"></script>
<script>
    window.addEventListener('DOMContentLoaded', () => {
        new PagefindUI({
            element: "#search",
            showSubResults: true,
            excerptLength: 30,
            showImages: false
        });
    });
</script>
{{ end }}
```

### Per-Book Search

For book-specific search (optional, advanced):

In **layouts/books/single.html**, add data attribute:

```html
<div class="book-content" data-pagefind-filter="book:{{ .File.BaseFileName }}">
    {{ .Content }}
</div>
```

Then filter in JavaScript:

```javascript
new PagefindUI({
    element: "#book-search",
    filters: {
        book: "{{ .File.BaseFileName }}"
    }
});
```

---

## In-Book Search

Readers need to search **within** a book, not across all books. Essential for research and reference reading.

### Implementation Strategy

**Option 1: Pagefind with Book Filters (Recommended)**

Add to **layouts/books/single.html**:

```html
<!-- Search box in book hub -->
<section class="book-search">
    <h2 class="section-title">Search This Book</h2>
    <div id="book-search"></div>
</section>

<link rel="stylesheet" href="/pagefind/pagefind-ui.css">
<script src="/pagefind/pagefind-ui.js"></script>
<script>
    window.addEventListener('DOMContentLoaded', () => {
        new PagefindUI({
            element: "#book-search",
            showImages: false,
            excerptLength: 50,
            filters: {
                book: "{{ .File.BaseFileName }}"
            },
            translations: {
                placeholder: "Search within this book...",
                zero_results: "No results in this book for [SEARCH_TERM]"
            }
        });
    });
</script>
```

**Mark book content in templates:**

In **layouts/chapters/single.html**, wrap reading content:

```html
<article class="text" data-pagefind-body data-pagefind-filter="book:{{ .Parent.Parent.File.BaseFileName }}">
    {{ .Content }}
</article>
```

In **layouts/books/single.html** (book hub), mark the about section:

```html
<div class="context-text" data-pagefind-body data-pagefind-filter="book:{{ .File.BaseFileName }}">
    {{ .Content }}
</div>
```

**Benefits:**
- Works offline after first load
- Fast (client-side)
- No server required
- Highlight search terms in results

### Search UI in Reading Page

Add search to the reading experience itself:

**layouts/chapters/single.html** - Add to top bar:

```html
<div class="top-right">
    <button class="top-btn" onclick="toggleSearch()">Search</button>
    <button class="top-btn" onclick="toggleTOC()">Contents</button>
    <button class="top-btn" onclick="toggleControls()">Settings</button>
    <button class="top-btn" onclick="toggleFocusMode()">Focus</button>
</div>
```

**Add search drawer (like TOC):**

```html
<!-- Search Drawer -->
<aside class="search-drawer" id="searchDrawer">
    <div class="search-header">
        <h2>Search This Book</h2>
        <button class="search-close" onclick="toggleSearch()">×</button>
    </div>
    <div class="search-content">
        <div id="chapter-search"></div>
    </div>
</aside>
```

**Update reading.js:**

```javascript
// Search drawer
function toggleSearch() {
    const search = document.getElementById('searchDrawer');
    const overlay = document.getElementById('overlay');
    search.classList.toggle('open');
    overlay.classList.toggle('show');
    
    // Initialize Pagefind on first open
    if (!window.pagefindInitialized) {
        const script = document.createElement('script');
        script.src = '/pagefind/pagefind-ui.js';
        script.onload = () => {
            new PagefindUI({
                element: "#chapter-search",
                filters: { book: bookSlug },
                showImages: false
            });
            window.pagefindInitialized = true;
        };
        document.head.appendChild(script);
        
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/pagefind/pagefind-ui.css';
        document.head.appendChild(link);
    }
}

// Keyboard shortcut
// In keydown handler, add:
case '/':
    e.preventDefault();
    toggleSearch();
    showShortcutHint('Search Book');
    break;
```

**CSS for search drawer:**

```css
.search-drawer {
    position: fixed;
    right: -480px;
    top: 0;
    width: 480px;
    height: 100vh;
    background: var(--paper);
    z-index: 150;
    overflow-y: auto;
    transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -4px 0 32px rgba(26, 20, 18, 0.08);
}

.search-drawer.open {
    right: 0;
}

.search-header {
    padding: 56px 56px 32px;
    position: sticky;
    top: 0;
    background: var(--paper);
    z-index: 10;
}

.search-close {
    position: absolute;
    top: 56px;
    right: 56px;
    background: transparent;
    border: none;
    font-size: 28px;
    color: var(--smoke);
    cursor: pointer;
    transition: color 0.3s ease;
}

.search-close:hover {
    color: var(--terracotta);
}

.search-content {
    padding: 0 56px 80px;
}
```

### Search Performance

**Optimize Pagefind index size:**

In **pagefind.toml** (create in project root):

```toml
# Only index actual content
[indexing]
root_selector = "article, .context-text"

# Exclude navigation, headers, footers
exclude_selectors = [".header", ".footer", ".nav", ".toc-list"]

# Keep index small
force_language = "en"
```

**Build with optimization:**

```bash
npx pagefind --site public --glob "**/*.html" --bundle-dir pagefind
```

**Result:** ~30-50KB per book for search index. Lazy-loaded only when needed.

---

## Speed Optimization

Speed isn't a nice-to-have. It's essential. Readers on 3G connections, older phones, limited data plans—they all need fast experiences.

### Build-Time Optimizations

**1. Hugo Build Speed**

```toml
# hugo.toml
[caches]
  [caches.getjson]
    dir = ":cacheDir/:project"
    maxAge = "10m"
  [caches.getcsv]
    dir = ":cacheDir/:project"
    maxAge = "10m"
  [caches.images]
    dir = ":cacheDir/:project"
    maxAge = -1  # Never expire
  [caches.assets]
    dir = ":cacheDir/:project"
    maxAge = -1
  [caches.modules]
    dir = ":cacheDir/:project"
    maxAge = -1
```

**Build only what changed:**
```bash
hugo --gc --minify --cleanDestinationDir
```

**Parallel processing:**
```toml
# hugo.toml
timeout = "30s"
enableGitInfo = false  # Skip git queries if not needed
```

**2. Asset Pipeline**

**Combine CSS (already doing this):**
```html
{{ $base := resources.Get "css/base.css" }}
{{ $components := resources.Get "css/components.css" }}
{{ $pages := resources.Get "css/pages.css" }}
{{ $css := slice $base $components $pages | resources.Concat "css/akshara.css" | minify | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}">
```

**One CSS file = One request = One cache entry**

**JavaScript:**
- reading.js is the ONLY script
- Inline critical JS for above-fold interaction (< 1KB)
- Defer non-critical JS

```html
<script src="/js/reading.js" defer></script>
```

**3. Image Optimization**

**Covers must be optimized:**

```bash
# Install ImageMagick
brew install imagemagick  # or apt-get install imagemagick

# Optimize all covers
cd static/covers
mogrify -strip -interlace Plane -quality 80 -resize 600x900\> *.jpg

# Results: 2-3MB → 150-200KB per cover
```

**Generate WebP:**

```bash
# Install cwebp
brew install webp

# Convert all JPGs to WebP
for img in static/covers/*.jpg; do
    cwebp -q 80 "$img" -o "${img%.jpg}.webp"
done

# Results: Additional 30% size reduction
```

**Serve WebP with fallback:**

```html
<picture>
    <source srcset="{{ .Params.cover | replaceRE "\\.jpg$" ".webp" }}" type="image/webp">
    <img src="{{ .Params.cover }}" alt="{{ .Title }}" loading="lazy" decoding="async">
</picture>
```

**Hugo image processing (for responsive images):**

```html
{{ $cover := resources.Get .Params.cover }}
{{ $small := $cover.Resize "400x" }}
{{ $medium := $cover.Resize "800x" }}
{{ $large := $cover.Resize "1200x" }}

<img 
    srcset="{{ $small.RelPermalink }} 400w,
            {{ $medium.RelPermalink }} 800w,
            {{ $large.RelPermalink }} 1200w"
    sizes="(max-width: 640px) 400px,
           (max-width: 1024px) 800px,
           1200px"
    src="{{ $medium.RelPermalink }}"
    loading="lazy"
    decoding="async"
    alt="{{ .Title }}"
>
```

### Runtime Optimizations

**1. Critical CSS Inlining**

For first paint speed, inline critical CSS:

**layouts/partials/head.html:**

```html
<style>
{{ $critical := resources.Get "css/critical.css" | minify }}
{{ $critical.Content | safeCSS }}
</style>
```

**css/critical.css** - Only above-fold styles:

```css
/* Header */
.header { position: fixed; top: 0; /* ... */ }

/* Hero */
.hero { padding: 200px 80px; /* ... */ }

/* Typography */
h1 { font-family: 'Libre Baskerville', serif; /* ... */ }
```

**Load full CSS async:**

```html
<link rel="preload" href="{{ $css.RelPermalink }}" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{{ $css.RelPermalink }}"></noscript>
```

**2. Font Loading Strategy**

**Preconnect to Google Fonts:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

**Load with font-display: swap:**

```html
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
```

**Or self-host fonts (better for repeated visits):**

```bash
# Download from Google Fonts
# Add to static/fonts/

# Use in CSS
@font-face {
    font-family: 'Libre Baskerville';
    src: url('/fonts/libre-baskerville-regular.woff2') format('woff2');
    font-weight: 400;
    font-display: swap;
}
```

**3. Lazy Loading**

**Images:**

```html
<img src="..." loading="lazy" decoding="async">
```

**Book covers grid:**

```html
<!-- First 6 eager, rest lazy -->
{{ range $index, $book := .Pages }}
    <img src="{{ .Params.cover }}" 
         {{ if gt $index 5 }}loading="lazy"{{ end }}
         decoding="async">
{{ end }}
```

**4. Resource Hints**

**Preload critical resources:**

```html
<!-- Preload fonts -->
<link rel="preload" href="/fonts/libre-baskerville.woff2" as="font" type="font/woff2" crossorigin>

<!-- Preload hero image -->
{{ with .Params.hero_image }}
<link rel="preload" href="{{ . }}" as="image">
{{ end }}
```

**Prefetch next chapter:**

In reading.js:

```javascript
// Prefetch next chapter when reader is 50% through current
window.addEventListener('scroll', () => {
    const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    
    if (scrollPercent > 50 && !window.nextChapterPrefetched) {
        const nextLink = document.querySelector('.nav-link.next');
        if (nextLink) {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = nextLink.href;
            document.head.appendChild(link);
            window.nextChapterPrefetched = true;
        }
    }
});
```

### Cloudflare Workers Optimizations

**1. Smart Caching**

Update **src/index.js**:

```javascript
// Cache static assets aggressively
if (url.pathname.match(/\.(jpg|jpeg|png|webp|woff2|woff)$/)) {
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    headers.set('CDN-Cache-Control', 'public, max-age=31536000');
    
    return new Response(response.body, {
        status: response.status,
        headers
    });
}

// Cache HTML with revalidation
if (url.pathname.endsWith('.html') || !url.pathname.includes('.')) {
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'public, max-age=3600, stale-while-revalidate=86400');
    
    return new Response(response.body, {
        status: response.status,
        headers
    });
}
```

**2. Brotli Compression**

Workers automatically compress. Verify in response:

```javascript
// In Worker
headers.set('Content-Encoding', 'br'); // Cloudflare handles this
```

**3. HTTP/2 Push (use sparingly)**

```javascript
// Push critical CSS with HTML
if (url.pathname.endsWith('.html')) {
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.append('Link', '</css/akshara.css>; rel=preload; as=style');
    
    return new Response(response.body, {
        status: response.status,
        headers
    });
}
```

### Performance Monitoring

**Add performance marks:**

```javascript
// In reading.js
performance.mark('reading-start');

window.addEventListener('load', () => {
    performance.mark('reading-ready');
    performance.measure('reading-init', 'reading-start', 'reading-ready');
    
    const measure = performance.getEntriesByName('reading-init')[0];
    console.log(`Reading ready in ${measure.duration}ms`);
    
    // Send to analytics if needed
});
```

**Target metrics:**
- First Contentful Paint (FCP): < 1.8s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.8s
- Cumulative Layout Shift (CLS): < 0.1
- First Input Delay (FID): < 100ms

**Test on real devices:**

```bash
# Use Lighthouse
npx lighthouse https://akshara.dhwani.ink --view

# Test on slow 3G
npx lighthouse https://akshara.dhwani.ink --throttling.requestLatencyMs=400 --throttling.downloadThroughputKbps=400

# Mobile
npx lighthouse https://akshara.dhwani.ink --preset=mobile
```

### Performance Budget

**Set limits:**

- HTML: < 50KB per page
- CSS: < 30KB total
- JavaScript: < 15KB total
- Fonts: < 100KB total (WOFF2)
- Images: < 200KB per cover
- Total page weight: < 500KB

**Enforce in CI:**

```yaml
# .github/workflows/performance.yml
- name: Check bundle size
  run: |
    MAX_CSS=30000
    CSS_SIZE=$(stat -f%z public/css/akshara.css)
    if [ $CSS_SIZE -gt $MAX_CSS ]; then
      echo "CSS too large: ${CSS_SIZE} bytes"
      exit 1
    fi
```

### Offline Reading (Service Worker)

Critical for mobile users with unreliable connections.

**static/sw.js:**

```javascript
const CACHE_VERSION = 'v1';
const CACHE_NAME = `akshara-${CACHE_VERSION}`;

// Cache these immediately
const STATIC_ASSETS = [
    '/',
    '/css/akshara.css',
    '/js/reading.js',
    '/fonts/libre-baskerville-regular.woff2',
    '/fonts/inter-regular.woff2'
];

// Install - cache static assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
            .then(() => self.skipWaiting())
    );
});

// Activate - clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys()
            .then(keys => Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            ))
            .then(() => self.clients.claim())
    );
});

// Fetch - network first, fallback to cache
self.addEventListener('fetch', event => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') return;
    
    // Network first for HTML (always fresh)
    if (request.headers.get('Accept').includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then(response => {
                    // Cache the page for offline
                    const clone = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put(request, clone));
                    return response;
                })
                .catch(() => caches.match(request))  // Offline fallback
        );
        return;
    }
    
    // Cache first for static assets
    event.respondWith(
        caches.match(request)
            .then(cached => {
                if (cached) return cached;
                
                return fetch(request)
                    .then(response => {
                        const clone = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => cache.put(request, clone));
                        return response;
                    });
            })
    );
});
```

**Register in layouts/partials/head.html:**

```html
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('SW registered'))
            .catch(err => console.log('SW error:', err));
    });
}
</script>
```

**Offline indicator (optional):**

```javascript
// In reading.js
window.addEventListener('online', () => {
    document.body.classList.remove('offline');
    showShortcutHint('Back online');
});

window.addEventListener('offline', () => {
    document.body.classList.add('offline');
    showShortcutHint('Offline - using cached content');
});
```

```css
body.offline::before {
    content: 'Offline';
    position: fixed;
    top: 80px;
    right: 24px;
    background: var(--terracotta);
    color: var(--paper);
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 11px;
    z-index: 200;
}
```

**Benefits:**
- Readers can continue reading offline
- Previously visited chapters load instantly
- Reduces data usage on mobile
- Improves perceived performance

---

## Mobile Reading Experience

**Mobile is not an afterthought. It's the primary experience.**

Most readers will access Akshara on phones. Optimize for:
- Touch interactions
- Small screens
- Variable network speeds
- One-handed reading
- Interrupted sessions

### Touch-Optimized UI

**1. Tap Target Sizes**

Minimum 44x44px for all interactive elements:

```css
/* Buttons */
.top-btn {
    padding: 12px 16px;  /* Ensures > 44px height */
    min-width: 44px;
}

/* TOC links */
.toc-list a {
    padding: 14px 20px;  /* Touch-friendly */
}

/* Chapter navigation */
.nav-link {
    padding: 32px 0;  /* Large touch area */
}
```

**2. Bottom-Aligned Controls**

On mobile, controls at bottom for thumb reach:

```css
@media (max-width: 768px) {
    .controls {
        left: 50%;
        transform: translateX(-50%);
        bottom: 24px;
        right: auto;
    }
    
    .top-bar {
        /* Still at top, but auto-hides */
    }
}
```

**3. Swipe Gestures**

Add swipe for chapter navigation:

```javascript
// In reading.js
let touchStartX = 0;
let touchEndX = 0;

document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    const swipeThreshold = 50;
    const diff = touchStartX - touchEndX;
    
    if (Math.abs(diff) < swipeThreshold) return;
    
    if (diff > 0) {
        // Swipe left = next chapter
        const nextLink = document.querySelector('.nav-link.next');
        if (nextLink) window.location.href = nextLink.href;
    } else {
        // Swipe right = previous chapter
        const prevLink = document.querySelector('.nav-link.prev');
        if (prevLink) window.location.href = prevLink.href;
    }
}
```

### Mobile Typography

**Readable on small screens:**

```css
/* Mobile-specific typography */
@media (max-width: 640px) {
    /* Reading text */
    .reading {
        font-size: 19px;  /* Slightly smaller */
        line-height: 1.75;  /* Tighter for small screens */
        padding: 140px 24px 200px;  /* Less horizontal padding */
    }
    
    /* Chapter titles */
    .chapter-title {
        font-size: 40px;  /* From 68px */
        line-height: 1.1;
    }
    
    /* Drop caps */
    .text p:first-of-type::first-letter {
        font-size: 4em;  /* From 5.2em */
    }
}
```

**Dynamic text sizing (optional):**

```javascript
// Adjust based on screen width
function setOptimalFontSize() {
    const width = window.innerWidth;
    let size = 21;
    
    if (width < 400) size = 18;
    else if (width < 640) size = 19;
    
    document.querySelector('.reading').style.fontSize = size + 'px';
}

window.addEventListener('resize', setOptimalFontSize);
setOptimalFontSize();
```

### Mobile Navigation

**1. Hamburger Menu (if needed)**

For mobile header:

```html
<!-- Mobile menu button -->
<button class="menu-toggle" onclick="toggleMobileMenu()">☰</button>

<!-- Mobile menu drawer -->
<nav class="mobile-menu" id="mobileMenu">
    <button class="menu-close" onclick="toggleMobileMenu()">×</button>
    <a href="/books">Browse</a>
    <a href="/collections">Collections</a>
    <a href="/authors">Authors</a>
    <a href="/about">About</a>
</nav>
```

**2. Bottom Navigation Bar**

Alternative to top header on mobile:

```html
<nav class="bottom-nav">
    <a href="/books">
        <span class="icon">📚</span>
        <span class="label">Browse</span>
    </a>
    <a href="/collections">
        <span class="icon">📑</span>
        <span class="label">Collections</span>
    </a>
    <a href="/authors">
        <span class="icon">✍️</span>
        <span class="label">Authors</span>
    </a>
</nav>
```

```css
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    background: var(--paper);
    border-top: 1px solid var(--sand);
    padding: 8px;
    z-index: 100;
}

.bottom-nav a {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px;
    text-decoration: none;
    color: var(--smoke);
}

.bottom-nav a.active {
    color: var(--terracotta);
}

@media (min-width: 769px) {
    .bottom-nav {
        display: none;  /* Desktop only shows header */
    }
}
```

### Mobile Performance

**1. Reduce Initial Load**

Mobile users on slow connections need fast first paint:

```html
<!-- Inline critical CSS -->
<style>
    /* Minimal above-fold styles */
    .header { /* ... */ }
    .hero { /* ... */ }
</style>

<!-- Load full CSS after -->
<link rel="preload" href="/css/akshara.css" as="style" onload="this.rel='stylesheet'">
```

**2. Image Loading Strategy**

```html
<!-- Use smaller images on mobile -->
<img srcset="cover-400w.webp 400w,
             cover-800w.webp 800w,
             cover-1200w.webp 1200w"
     sizes="(max-width: 640px) 90vw,
            (max-width: 1024px) 45vw,
            400px"
     src="cover-800w.webp"
     loading="lazy"
     alt="Book cover">
```

**3. Reduce JavaScript**

Mobile CPUs are slower. Minimize JS execution:

```javascript
// Debounce scroll handlers
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

const handleScroll = debounce(() => {
    updateProgress();
}, 50);

window.addEventListener('scroll', handleScroll);
```

### Mobile-Specific Features

**1. Reading Progress Indicator**

More important on mobile where overview is harder:

```html
<div class="mobile-progress">
    <div class="progress-text">{{ .Params.chapter_number }} / {{ $totalChapters }}</div>
    <div class="progress-bar">
        <div class="progress-fill" id="mobileFill"></div>
    </div>
</div>
```

```css
@media (max-width: 768px) {
    .mobile-progress {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--paper);
        padding: 12px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        z-index: 90;
        box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
    }
    
    .progress-text {
        font-size: 12px;
        color: var(--ash);
        white-space: nowrap;
    }
    
    .progress-bar {
        flex: 1;
        height: 3px;
        background: var(--sand);
        border-radius: 2px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: var(--terracotta);
        transition: width 0.3s ease;
    }
}
```

**2. One-Handed Reading Mode**

Toggle for bottom-aligned controls:

```javascript
function toggleOneHandedMode() {
    document.body.classList.toggle('one-handed');
    localStorage.setItem('oneHanded', document.body.classList.contains('one-handed'));
}

// Restore on load
if (localStorage.getItem('oneHanded') === 'true') {
    document.body.classList.add('one-handed');
}
```

```css
body.one-handed .controls {
    bottom: 80px;  /* Above progress bar */
}

body.one-handed .top-bar {
    transform: translateY(-100%);  /* Always hidden */
}
```

**3. Auto-Scroll (experimental)**

For hands-free reading:

```javascript
let autoScrollInterval;
let scrollSpeed = 1;  // pixels per 50ms

function startAutoScroll() {
    autoScrollInterval = setInterval(() => {
        window.scrollBy(0, scrollSpeed);
    }, 50);
    
    showShortcutHint('Auto-scroll enabled');
}

function stopAutoScroll() {
    clearInterval(autoScrollInterval);
    showShortcutHint('Auto-scroll disabled');
}

// Toggle with double-tap on text
let lastTap = 0;
document.querySelector('.text').addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTap < 300) {
        if (autoScrollInterval) {
            stopAutoScroll();
        } else {
            startAutoScroll();
        }
    }
    lastTap = now;
});
```

### Mobile Testing

**Test on real devices:**

- iPhone SE (small screen)
- iPhone 12/13 (standard)
- Android mid-range (OnePlus, Samsung)
- Android budget (Redmi, Realme)

**Browser testing:**
- Safari iOS
- Chrome Android
- Firefox Android (less common but important)

**Network testing:**
- 4G
- 3G
- 2G (slow)

**Use Chrome DevTools:**
```
1. Open DevTools
2. Toggle device toolbar (Cmd+Shift+M)
3. Select device profile
4. Network → Slow 3G
5. Test reading flow
```

---

## Common Mistakes to Avoid

### 1. Defensive Front Matter Checks

**DON'T:**
```html
{{ if .Params.author }}
    {{ if ne .Params.author "" }}
        <p>{{ .Params.author }}</p>
    {{ end }}
{{ end }}
```

**DO:**
```html
<p>{{ .Params.author }}</p>
```

If `author` is missing, your content is broken. Fix the content, not the template.

### 2. Complex Navigation Logic

**DON'T:**
```html
{{ $next := "" }}
{{ range .Pages }}
    {{ if gt .Weight $.Weight }}
        {{ $next = . }}
        {{ break }}
    {{ end }}
{{ end }}
```

**DO:**
Set `next` and `prev` in front matter. Explicit is better than computed.

### 3. Premature Abstraction

**DON'T:**
```html
{{ partial "meta.html" (dict "type" "book" "data" .) }}
{{ partial "meta.html" (dict "type" "author" "data" .) }}
```

**DO:**
Write the HTML twice. Different contexts = different code.

### 4. Over-reliance on `.Scratch`

**DON'T:**
```html
{{ .Scratch.Set "count" 0 }}
{{ range .Pages }}
    {{ $.Scratch.Add "count" 1 }}
{{ end }}
{{ .Scratch.Get "count" }}
```

**DO:**
```html
{{ len .Pages }}
```

Hugo has functions. Use them.

### 5. Trying to Be a SPA

**DON'T:**
- Client-side routing
- JSON APIs for navigation
- JavaScript-rendered content

**DO:**
- Server-rendered HTML
- Regular links
- Progressive enhancement

### 6. Theme System Complexity

**DON'T:**
```
themes/
  akshara/
    layouts/
    static/
    config.toml
```

**DO:**
```
layouts/
static/
hugo.toml
```

You're building one site, not distributing a theme.

### 7. Build-Time Personalization

**DON'T:**
Try to make Hugo generate different HTML per user.

**DO:**
- One build = one set of HTML files
- Client-side state (LocalStorage) for preferences
- Accept that static means static

### 8. Markdown Processing Hacks

**DON'T:**
```html
{{ replaceRE "<p>(.+)</p>" "$1" .Content | safeHTML }}
```

**DO:**
Configure Goldmark properly in `hugo.toml`. Trust the renderer.

### 9. Asset Pipeline Over-engineering

**DON'T:**
- PostCSS with 20 plugins
- Babel transpilation
- Webpack integration

**DO:**
- Hugo's built-in minification
- Modern CSS (it works in browsers now)
- Vanilla JS (browsers are good now)

### 10. Ignoring Build Errors

**DON'T:**
```bash
hugo --ignoreErrors
```

**DO:**
```bash
hugo --gc --minify
```

Errors mean something is wrong. Fix it.

---

## Development Workflow

### Local Development

```bash
# Start server
hugo server -D

# Build for production
hugo --gc --minify

# With Pagefind
bash scripts/build.sh
```

### Content Creation Workflow

1. **Create book folder:**
   ```bash
   hugo new books/gandhi-my-experiments/_index.md
   ```

2. **Add metadata** to `_index.md`

3. **Create chapters folder:**
   ```bash
   mkdir -p content/books/gandhi-my-experiments/chapters
   ```

4. **Add chapters:**
   ```bash
   hugo new books/gandhi-my-experiments/chapters/01-birth.md
   ```

5. **Set chapter front matter:**
   - `chapter_number`
   - `reading_time`
   - `weight` (for ordering)
   - `prev` and `next`

6. **Add cover image** to `static/covers/`

7. **Build and test:**
   ```bash
   hugo server -D
   ```

### Git Workflow

```bash
# Feature branch
git checkout -b add-book-gandhi-experiments

# Add content
git add content/books/gandhi-my-experiments/
git add static/covers/gandhi-experiments.jpg

# Commit
git commit -m "Add: My Experiments with Truth"

# Push
git push origin add-book-gandhi-experiments

# Merge to main via PR
# Cloudflare auto-deploys on main merge
```

---

## Performance Checklist

### Before Launch

- [ ] All images optimized (use ImageOptim or similar)
- [ ] Cover images < 200KB each
- [ ] CSS minified (Hugo does this)
- [ ] HTML minified (Hugo does this)
- [ ] JavaScript < 20KB total
- [ ] Fonts: WOFF2 only, subset if possible
- [ ] No external JavaScript dependencies
- [ ] No analytics without consent
- [ ] Lighthouse score 95+ on all metrics

### Images

```bash
# Optimize covers (ImageMagick)
mogrify -strip -interlace Plane -gaussian-blur 0.05 -quality 85% static/covers/*.jpg

# Generate WebP versions (optional)
for img in static/covers/*.jpg; do
    cwebp -q 85 "$img" -o "${img%.jpg}.webp"
done
```

In templates:
```html
<picture>
    <source srcset="{{ .Params.cover | replaceRE "\\.jpg$" ".webp" }}" type="image/webp">
    <img src="{{ .Params.cover }}" alt="{{ .Title }} cover" loading="lazy">
</picture>
```

---

## Content Maintenance

### Archival Best Practices

1. **Keep source PDFs** - Store in R2 or Archive.org
2. **Version control content** - Git tracks all changes
3. **Document methodology** - In front matter `digitization_method`
4. **Preserve original** - Link to Archive.org source
5. **Historical accuracy** - Don't "fix" historical spelling unless OCR error

### Updating Books

```bash
# Edit chapter
vim content/books/gandhi-my-experiments/chapters/03-child-marriage.md

# Commit with descriptive message
git commit -m "Fix: Correct OCR error in Chapter 3, paragraph 5"

# Deploy
git push origin main
```

### Adding Metadata Later

You can always add:
- `featured_quote` for homepage rotation
- `themes` taxonomy for better categorization
- `reading_time` if initially missing
- External URLs as they become available

Hugo rebuilds are fast. Edit, commit, deploy.

---

## Troubleshooting

### Build Fails on Cloudflare

**Check:**
1. Hugo version in environment variables
2. Build command is correct: `hugo --minify`
3. No `.gitignore` excluding necessary files
4. Front matter YAML is valid (no tabs, proper indentation)

### Search Not Working

**Check:**
1. Pagefind ran: `npx pagefind --site public`
2. `/pagefind/` directory exists in `public/`
3. Search page includes script: `<script src="/pagefind/pagefind-ui.js"></script>`
4. No CSP blocking scripts

### Position Memory Not Working

**Check:**
1. LocalStorage enabled in browser
2. `chapterId` and `bookSlug` variables set correctly
3. Script runs after DOM loads: `window.addEventListener('load', ...)`
4. Storage key format: `scroll-${bookSlug}-${chapterId}`

### Images Not Loading

**Check:**
1. Images in `static/` not `assets/`
2. Paths absolute from root: `/covers/book.jpg` not `covers/book.jpg`
3. Image files pushed to Git
4. Correct file extensions in front matter

---

## Security Considerations

### Content Security Policy

Add to **layouts/partials/head.html**:

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline';
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com;
    img-src 'self' data: https:;
    frame-src https://archive.org;
    connect-src 'self';
">
```

Adjust based on what you embed (Archive.org iframes, etc.)

### Subresource Integrity

For external fonts (optional):

```html
<link 
    href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&display=swap" 
    rel="stylesheet"
    integrity="sha384-..."
    crossorigin="anonymous"
>
```

Generate SRI hash:
```bash
curl -s "URL" | openssl dgst -sha384 -binary | openssl base64 -A
```

### Privacy

- No Google Analytics by default
- No external tracking
- LocalStorage only for user preferences
- No cookies unless user-initiated

---

## Launch Checklist

### Content

- [ ] At least 10 books fully digitized
- [ ] All books have cover images
- [ ] All chapters have reading time estimates
- [ ] Author pages created for main authors
- [ ] Collections properly categorized
- [ ] About page written
- [ ] Methodology documented

### Technical

- [ ] Hugo builds without errors
- [ ] All pages render correctly
- [ ] Search works (Pagefind)
- [ ] Responsive on mobile/tablet/desktop
- [ ] Reading features work (focus mode, shortcuts)
- [ ] Position memory persists
- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] Lighthouse score 95+

### Legal

- [ ] All content verified public domain
- [ ] Sources properly attributed
- [ ] Archive.org links working
- [ ] Copyright notice on About page
- [ ] Terms of use (if needed)

### Marketing

- [ ] Share on Twitter/social
- [ ] Submit to relevant directories
- [ ] Announce on dhwani.ink
- [ ] Reach out to libraries/educators

---

## Final Thoughts

**This is not a complex build.** You have:
- 12 HTML templates
- 3 CSS files
- 1 JavaScript file
- Hugo config
- Cloudflare Worker
- Content in Markdown

**What makes it great is:**
- Thoughtful design
- Careful content curation
- Attention to reading experience
- Respect for the texts
- **Speed on mobile devices**
- **In-book search that works**
- **Performance optimization**

**What doesn't make it great:**
- Complex build pipelines
- Cutting-edge frameworks
- Defensive programming
- Premature optimization
- Desktop-first thinking
- Ignoring mobile readers

**Critical priorities:**

1. **Mobile first** - 70%+ of your traffic will be mobile
2. **Speed** - Every 100ms matters on 3G
3. **Reading experience** - Focus mode, search, position memory
4. **Content quality** - Better 50 perfect books than 200 mediocre ones

Build this cleanly. Ship it. Then add more books. The site serves the literature, not the other way around.

**Key metrics to track:**
- Mobile LCP < 2.5s
- Mobile TTI < 3.8s
- Search latency < 100ms
- Chapter navigation < 500ms
- Build time < 30s for 100 books

---

**Now go build it.** 🚀

## Quick Reference

### Essential Commands

```bash
# Development
hugo server -D

# Production build
hugo --gc --minify
npx pagefind --site public

# Deploy to Workers
wrangler deploy

# Optimize images
mogrify -strip -quality 80 -resize 600x900\> static/covers/*.jpg

# Test performance
npx lighthouse https://akshara.dhwani.ink --preset=mobile --view
```

### Performance Checklist

- [ ] All covers < 200KB
- [ ] CSS < 30KB minified
- [ ] JS < 15KB minified
- [ ] First load < 500KB total
- [ ] Mobile LCP < 2.5s
- [ ] Search index < 50KB per book
- [ ] Fonts use font-display: swap
- [ ] Images use loading="lazy"
- [ ] Critical CSS inlined
- [ ] Prefetch next chapter at 50% scroll

### Mobile Checklist

- [ ] Touch targets ≥ 44px
- [ ] Readable at 19px on mobile
- [ ] Swipe navigation works
- [ ] Bottom controls accessible
- [ ] One-handed mode available
- [ ] Auto-scroll option
- [ ] Progress visible at bottom
- [ ] Focus mode hides chrome
- [ ] Tested on real devices
- [ ] Works on 3G

### Build Checklist

- [ ] Hugo config optimized
- [ ] Cloudflare Worker configured
- [ ] In-book search implemented
- [ ] Image optimization automated
- [ ] Performance budget enforced
- [ ] GitHub Actions setup
- [ ] Custom domain configured
- [ ] Analytics (privacy-respecting)
- [ ] Error tracking (if needed)
- [ ] Monitoring enabled
