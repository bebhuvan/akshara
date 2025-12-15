# Project Akshara: Visual Architecture Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AKSHARA SYSTEM ARCHITECTURE                  │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                          CONTENT LAYER (Markdown)                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Books/          Authors/          Collections/        Pages/         │
│  ├─ _index.md    ├─ gandhi.md      ├─ ancient.md      ├─about.md     │
│  ├─ book1/       ├─ nehru.md       ├─ bengal-ren.md   └─contribute   │
│  │  ├─ _index    ├─ subhas.md      └─ reformers.md                  │
│  │  ├─ 01-ch.md  └─ 4 more                                           │
│  │  ├─ 02-ch.md                                                       │
│  │  └─ ...43                                                          │
│  └─ book2/                                                            │
│     ├─ _index                                                          │
│     └─ ...34 chapters                                                  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Markdown +
                                  │ Front Matter
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER (Hugo Build)                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Configuration: hugo.toml                                             │
│  - Permalinks: /books/:slug, /authors/:slug                           │
│  - Taxonomies: authors, collections, themes, periods                  │
│  - Markdown: Goldmark with unsafe HTML                                │
│                                                                        │
│  Processing:                                                          │
│  1. Parse markdown with front matter                                  │
│  2. Apply cascade configuration (inherit type)                        │
│  3. Generate HTML from markdown                                       │
│  4. Build TOC from chapter weights                                    │
│  5. Create index pages and archive entries                            │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ .Content HTML
                                  │ .Pages arrays
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    TEMPLATE LAYER (Hugo Templates)                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  baseof.html                                                          │
│  ├─ head.html (meta, fonts, CSS, scripts)                            │
│  ├─ [main block - page specific]                                     │
│  │  ├─ header.html (nav, theme toggle)                               │
│  │  ├─ [Content specific to page type]                               │
│  │  └─ footer.html (links, copyright)                                │
│  └─ partials/                                                         │
│     ├─ book-card.html                                                │
│     ├─ book-page.html                                                │
│     └─ search.html                                                   │
│                                                                        │
│  Specific Templates:                                                 │
│  - index.html (homepage)                                             │
│  - books/book.html (book hub with TOC)                               │
│  - chapters/single.html (reading experience)                         │
│  - authors/single.html (author profiles)                             │
│  - collections/single.html (collection pages)                        │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Generated HTML
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     STYLING LAYER (CSS Variables)                       │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Light Theme (Default)   Dark Theme          Sepia Theme             │
│  --ink: #1a1614          --ink: #ebe8e4      --ink: #3d3426          │
│  --paper: #fffffe        --paper: #1a1614    --paper: #f4ecd8        │
│  --accent: #c85a3a       --accent: #e67855   --accent: #b04d2f       │
│                                                                        │
│  CSS Structure:                                                       │
│  1. base.css (194 lines) - Variables, resets, typography            │
│  2. components.css (531 lines) - Header, footer, cards              │
│  3. pages.css (2986 lines) - Page-specific styles                   │
│  4. search.css (133 lines) - Search interface                       │
│  Total: 3844 lines, no frameworks                                    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ CSS + HTML
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  INTERACTION LAYER (Vanilla JavaScript)                 │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  reading.js (230 lines, zero dependencies)                           │
│  ├─ Progress bar (scroll position %)                                 │
│  ├─ Font size control (17px-27px)                                   │
│  ├─ Theme switching (Light/Dark/Sepia)                              │
│  ├─ Focus mode (hide all UI)                                        │
│  ├─ Keyboard navigation (M, F, arrows, Esc)                         │
│  ├─ Position memory (localStorage)                                  │
│  ├─ Menu toggle                                                      │
│  └─ Keyboard shortcut hints                                          │
│                                                                        │
│  Data Attributes (from template):                                   │
│  - data-book-slug: Used for localStorage keys                       │
│  - data-chapter-id: Unique chapter identifier                       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
                                  │
                                  │ Browser renders
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     BROWSER (Reading Experience)                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ [Sticky Header] [Book Title] [Menu] [Theme]                 │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │ [Progress Bar]                                          ███% │   │
│  ├──────────────────────────────────────────────────────────────┤   │
│  │                                                              │   │
│  │  Chapter 5 of 42                                            │   │
│  │  SECTION TITLE                                              │   │
│  │                                                              │   │
│  │  Content flows here with full typography, footnotes,        │   │
│  │  proper line height, optimal reading width...              │   │
│  │                                                              │   │
│  │  [← Previous] [Reading Controls] [Next →]                   │   │
│  │                                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  [Slide-in Menu]                                                      │
│  ├─ Table of Contents (with progress)                               │
│  ├─ Font Size Adjustment                                            │
│  ├─ Theme Selector                                                  │
│  ├─ Focus Mode Toggle                                               │
│  └─ Keyboard Shortcuts                                              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: Adding a New Book

```
Step 1: Create Structure
────────────────────────
mkdir content/books/new-book-slug/
touch content/books/new-book-slug/_index.md

Step 2: Add Book Metadata
──────────────────────────
_index.md contains:
  - title, author, author_slug
  - year, pages, chapters
  - description, cover image path
  - archive_url, digitization info
  - cascade config (auto-types children as "chapters")

Step 3: Add Chapters
───────────────────
01-chapter-one.md  (title, weight: 1, next/prev links, content)
02-chapter-two.md  (title, weight: 2, next/prev links, content)
...
NN-chapter-n.md

Step 4: Build
─────────────
hugo --minify
  ├─ Parses all markdown
  ├─ Builds TOC from .Pages sorted by weight
  ├─ Renders templates
  ├─ Generates book hub page
  ├─ Generates chapter pages
  └─ Creates HTML in /public/

Step 5: Deploy
──────────────
wrangler deploy
  ├─ Uploads public/ to Cloudflare Workers
  ├─ Sets cache headers (1yr for assets, 1hr for HTML)
  ├─ Applies security headers
  └─ Site live at akshara.dhwani.ink
```

## Content Model Example

```
Book Structure:
===============

content/books/foreign-notices-south-india/
│
├─ _index.md
│  ├─ title: "Foreign Notices of South India"
│  ├─ editor: "K.A. Nilakanta Sastri"
│  ├─ year: 1939
│  ├─ chapters: 31
│  ├─ reading_time: "8-10 hours"
│  ├─ archive_url: "https://archive.org/..."
│  └─ cascade:
│     - _target: {kind: "page"}
│       type: "chapters"
│
├─ 00-preface-and-bibliography.md
│  ├─ title: "Preface and Bibliography"
│  ├─ chapter_number: 1
│  ├─ weight: 1
│  ├─ reading_time: 14
│  ├─ next: "/books/foreign-notices-south-india/01-introduction"
│  └─ [markdown content]
│
├─ 01-introduction.md
│  ├─ title: "Introduction"
│  ├─ chapter_number: 2
│  ├─ weight: 2
│  ├─ prev: "/books/foreign-notices-south-india/00-preface..."
│  ├─ next: "/books/foreign-notices-south-india/01-megasthenes"
│  └─ [markdown content]
│
└─ ... 41 total chapters

Browser sees: /books/foreign-notices-south-india/
              ├─ /books/foreign-notices-south-india/01-introduction/
              ├─ /books/foreign-notices-south-india/02-megasthenes/
              └─ ... 44 chapters total
```

## Template Resolution Flow

```
Chapter Page Request: /books/book-slug/01-chapter/

1. Hugo matches URL pattern
2. Finds content/books/book-slug/01-chapter.md
3. Reads front matter (type: "chapters")
4. Routes to layouts/chapters/single.html
5. Provides context:
   - .Title (from front matter)
   - .Content (rendered markdown HTML)
   - .Parent (parent book page object)
   - .Params (all front matter fields)
6. Template queries:
   - where .Parent.Pages "Type" "chapters"
   - Creates TOC from chapters sorted ByWeight
   - Generates navigation (prev/next from .Params)
7. Includes reading.js for interactions
8. Renders final HTML
```

## URL Schema

```
URL                                          Source File
──────────────────────────────────────────   ────────────────────────────────
/                                            layouts/index.html
/books/                                      layouts/books/list.html
/books/book-slug/                            content/books/book-slug/_index.md
/books/book-slug/chapter-slug/               content/books/book-slug/XX-name.md
/authors/                                    layouts/authors/list.html
/authors/author-slug/                        content/authors/author-slug.md
/collections/                                layouts/collections/list.html
/collections/collection-slug/                content/collections/collection.md
/search/                                     content/search.md (Pagefind)
/404                                         layouts/404.html
```

## Caching Strategy

```
Cloudflare Workers (src/index.js)
│
├─ Static Assets (CSS, JS, fonts, images)
│  Cache: 1 year (immutable)
│  └─ /static/* /covers/* /js/* /fonts/* /css/*
│
├─ HTML Pages
│  Cache: 1 hour (purgeable)
│  └─ Everything else (.html or no extension)
│
└─ Security Headers
   └─ X-Content-Type-Options: nosniff
      X-Frame-Options: DENY
      X-XSS-Protection: 1; mode=block
      Referrer-Policy: strict-origin-when-cross-origin
      Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Collections System

```
Collection = Thematic grouping of books

ancient-india.md (Collection)
├─ title: "Ancient India"
├─ book_count: 2
├─ description: "Classical texts, historical records..."
├─ period: "2000 BCE - 1200 CE"
└─ books: ["lays-of-ancient-india", "foreign-notices-south-india"]

     ↓ Links to

     books/lays-of-ancient-india/
     books/foreign-notices-south-india/

Display on homepage:
├─ Collections grid showing all collections
├─ Click → /collections/ancient-india/
└─ Collection page shows linked books
```

## Storage (localStorage)

```
Key Format                    Value              Used For
──────────────────────────    ─────────────────  ────────────────
theme-{bookSlug}             "light|dark|sepia" Theme persistence
fontSize-{bookSlug}          "17" to "27"       Font size memory
{bookSlug}-{chapterId}       scroll position    Resume reading position
```

## Key Files Manifest

```
Project Akshara (Core)
├── hugo.toml                     Hugo configuration
├── wrangler.toml                 Cloudflare config
├── src/index.js                  Cloudflare Worker entry
│
├── content/                      Content (Markdown)
│   ├── books/
│   │   ├── _index.md            Books hub
│   │   ├── foreign-notices-south-india/
│   │   ├── lays-of-ancient-india/
│   │   ├── life-and-letters-*/
│   │   └── life-and-letters-of-*/
│   ├── authors/                 Author profiles (4 files)
│   ├── collections/             Thematic collections (5 files)
│   └── pages/                   Static pages
│
├── layouts/                      Templates (21 files)
│   ├── index.html               Homepage
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   ├── single.html
│   │   └── search.html
│   ├── books/
│   │   ├── _index.html          Books list
│   │   ├── list.html
│   │   ├── single.html          Book hub
│   │   └── book.html
│   ├── chapters/single.html     Reading page
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
│   │   ├── book-card.html
│   │   ├── book-page.html
│   │   └── search.html
│   └── 404.html
│
├── assets/css/                  Styling (3844 lines)
│   ├── base.css                 Variables, resets
│   ├── components.css           Reusable components
│   ├── pages.css                Page-specific styles
│   └── search.css               Search styling
│
├── static/
│   ├── js/reading.js            All interactions (230 lines)
│   ├── covers/                  Book covers (WEBP)
│   └── robots.txt
│
├── scripts/
│   ├── build.sh                 Hugo + Pagefind
│   ├── deploy.sh                Full deployment
│   └── split-foreign-notices.py Chapter extraction tool
│
└── public/                       Generated HTML (gitignored)
```

---

**This architecture enables:**
- Adding new books without touching code
- Multiple theme support with CSS variables
- Distraction-free reading experience
- Mobile-first responsive design
- Fast static site generation and deployment
- Minimal JavaScript (230 lines, zero dependencies)

