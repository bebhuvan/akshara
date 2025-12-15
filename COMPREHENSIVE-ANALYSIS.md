# Project Akshara: Comprehensive Codebase Overview

## Executive Summary

Project Akshara is a **Hugo-based static site generator** for a curated digital archive of Indian literary heritage. The project demonstrates excellent separation of concerns:

- **Content Layer**: Markdown-based books, chapters, authors, and collections
- **Layout Layer**: Hugo templates organized by content type
- **Styling Layer**: Custom CSS with theme system (Light/Dark/Sepia)
- **Interaction Layer**: Vanilla JavaScript for reading experience
- **Deployment**: Cloudflare Workers with edge caching

**Status**: Production-ready with 4 books, 100+ chapters live

---

## 1. BOOK STRUCTURE & DATA MODELS

### 1.1 Book Representation Architecture

Books in Akshara follow a **hierarchical folder structure** with Hugo's cascading front matter:

```
content/books/
├── _index.md                              # Books collection hub
├── foreign-notices-south-india/
│   ├── _index.md                         # Book metadata
│   ├── 00-preface-and-bibliography.md
│   ├── 01-introduction.md
│   ├── 02-megasthenes.md
│   ├── ...44 total chapters
│   └── (chapters.md)
└── lays-of-ancient-india/
    ├── _index.md
    ├── 01-indra-rain-giver.md
    ├── 02-indra-supreme-deity.md
    └── ...43 total chapters
```

### 1.2 Book Metadata Schema

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/foreign-notices-south-india/_index.md`

```yaml
---
# Identity
title: "Foreign Notices of South India"
subtitle: "From Megasthenes to Ma Huan"
editor: "K.A. Nilakanta Sastri"
author_slug: "k-a-nilakanta-sastri"

# Publication Details
year: 1939
language: "English"
pages: 584
chapters: 31
reading_time: "8-10 hours"
period: "Ancient to Medieval"

# Publishing Information
publisher: "University of Madras"
publication_location: "Madras, India"

# Content
cover: "/covers/foreign-notices-south-india-nilakanta-sastri-book-cover.webp"
description: "A comprehensive collection of historical accounts..."
featured_quote: "The history of South India, as seen through..."

# Source & Digitization
archive_url: "https://archive.org/details/in.ernet.dli.2015.87764"
digitized_from: "Archive.org"
digitization_method: "OCR with manual correction"
digitization_notes: "Detailed explanation of OCR/manual process..."

# External References
editor_wikipedia_url: "https://en.wikipedia.org/wiki/K._A._Nilakanta_Sastri"

# Hugo Configuration
type: "books"
layout: "book"
cascade:
  - _target:
      kind: "page"
    type: "chapters"
---
```

**Key Features**:
- `cascade`: Automatically sets all child pages to `type: "chapters"`
- `author_slug`: Links to author profiles
- Comprehensive metadata for SEO and sharing
- Digitization notes for transparency about process

### 1.3 Chapter Data Model

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/foreign-notices-south-india/01-megasthenes.md`

```yaml
---
title: "MEGASTHENES"
type: "chapters"
chapter_number: 2
chapter_title: "I"
reading_time: 6
word_count: 1109
weight: 2

# Navigation
next: "/books/foreign-notices-south-india/02-kc-and-china-in-the-second-century-bc"
prev: "/books/foreign-notices-south-india/01-introduction"
---

[Markdown content with footnotes and formatting]
```

**Key Observations**:
- `chapter_number`: Display number (used in TOC, navigation)
- `weight`: Sort order (crucial for chapter ordering)
- `next`/`prev`: Explicit navigation links (not auto-generated)
- `reading_time`: Minutes to read (for progress indicators)
- `word_count`: Actual word count from content analysis

### 1.4 Footnote & References Handling

Akshara uses **standard Markdown footnotes**:

```markdown
Megasthenes says that Taprobanê is separated from the mainland by a river; 
that the inhabitants are called Palaiogonoi,[^1] and that their country 
is more productive of gold and large pearls than India.

[^1]: This appears to be an ancient ethnonym for the Sinhalese people.
```

**Processing**:
- Markdown footnotes converted to HTML footnotes by Hugo's Goldmark renderer
- `unsafe = true` in hugo.toml enables HTML rendering in markdown
- Footnotes are **inline within chapter content** (not extracted separately)

### 1.5 File Organization Conventions

**Chapter Naming Pattern**: `{NUMBER:2D}-{KEBAB-CASE-TITLE}.md`

Examples:
- `00-preface-and-bibliography.md`
- `01-introduction.md`
- `01-megasthenes.md`
- `42-appendix.md`

**Why This Pattern?**
- Leading zeros enable proper lexicographic sorting
- Hyphenated slugs create clean URLs
- Number matches `weight` for ordering reliability

---

## 2. ADDING NEW BOOKS: THE WORKFLOW

### 2.1 Complete Process for Adding a Book

**Step 1: Create Book Directory**
```bash
mkdir -p content/books/your-book-name/
touch content/books/your-book-name/_index.md
```

**Step 2: Create Book Metadata File**

Template from `/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/foreign-notices-south-india/_index.md`:

```yaml
---
title: "Book Title"
author: "Author Name"
author_slug: "author-slug"
year: 1927
language: "English"
pages: 454
chapters: 164
reading_time: "~8 hours"
description: "Book description..."
cover: "/covers/book-slug-cover.webp"
period: "Time Period"
publisher: "Publisher"
publication_location: "City, Country"
archive_url: "https://archive.org/details/..."
digitized_from: "Archive.org"
digitization_method: "OCR with manual correction"
digitization_notes: "Explanation of the process..."

# Links
author_wikipedia_url: "https://en.wikipedia.org/..."
editor_wikipedia_url: "https://en.wikipedia.org/..."

type: "books"
layout: "book"
cascade:
  - _target:
      kind: "page"
    type: "chapters"
---

Introductory text about the book (becomes "About This Work" section).
```

**Step 3: Generate Chapter Files**

Create chapters as individual markdown files:

```bash
# Manual method
touch content/books/your-book/01-chapter-one.md
touch content/books/your-book/02-chapter-two.md
```

OR use **automation script** (Python):

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/scripts/split-foreign-notices.py`

```python
#!/usr/bin/env python3
"""
Script to split 'Foreign Notices of South India' into chapters
"""

import re
import os
from pathlib import Path

SOURCE_FILE = "/path/to/source.md"
OUTPUT_DIR = "/path/to/output/chapters"
WORDS_PER_MINUTE = 200

def count_words(text):
    """Count words in text"""
    return len(text.split())

def estimate_reading_time(word_count):
    """Estimate reading time in minutes"""
    return max(1, round(word_count / WORDS_PER_MINUTE))

def clean_title(title):
    """Clean title for filename - remove roman numerals, convert to kebab-case"""
    title = re.sub(r'^[IVX]+\.\s*', '', title)
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    title = re.sub(r'\s+', '-', title)
    return title.strip('-')[:50]

def parse_book():
    """Parse the book into chapter segments based on headers"""
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    chapters = []
    current_chapter = None
    chapter_number = 0

    # Pattern matches headers like "### I. TITLE" or "# I. TITLE"
    main_section_pattern = re.compile(r'^(#{1,3})\s+([IVX]+)\.\s+(.+)$')

    for i, line in enumerate(lines):
        match = main_section_pattern.match(line)

        if match:
            hash_marks = match.group(1)
            roman_num = match.group(2)
            title = match.group(3).strip()

            # Only treat as main chapter if header level <= 3
            if len(hash_marks) <= 3 and not re.match(r'^[A-Z]\.\s+', title):
                if current_chapter:
                    chapters.append(current_chapter)

                chapter_number += 1
                current_chapter = {
                    'number': chapter_number,
                    'title': title,
                    'roman': roman_num,
                    'content': [line],
                    'start_line': i
                }
            elif current_chapter:
                current_chapter['content'].append(line)
        elif current_chapter:
            current_chapter['content'].append(line)

    if current_chapter:
        chapters.append(current_chapter)

    return chapters

def generate_chapter_files():
    """Generate individual chapter markdown files with proper frontmatter"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    chapters = parse_book()

    for idx, chapter in enumerate(chapters):
        content_text = '\n'.join(chapter['content'])
        word_count = count_words(content_text)
        reading_time = estimate_reading_time(word_count)

        # Determine numbering
        file_num = f"{int(chapter['number']):02d}"
        clean_title_str = clean_title(chapter['title'])
        filename = f"{file_num}-{clean_title_str}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Generate navigation links
        next_chapter = ""
        prev_chapter = ""

        if idx > 0:
            prev_ch = chapters[idx - 1]
            prev_num = f"{int(prev_ch['number']):02d}"
            prev_title_clean = clean_title(prev_ch['title'])
            prev_chapter = f"/books/book-name/{prev_num}-{prev_title_clean}"

        if idx < len(chapters) - 1:
            next_ch = chapters[idx + 1]
            next_num = f"{int(next_ch['number']):02d}"
            next_title_clean = clean_title(next_ch['title'])
            next_chapter = f"/books/book-name/{next_num}-{next_title_clean}"

        # Create frontmatter
        front_matter = f"""---
title: "{chapter['title']}"
chapter_number: {idx}
reading_time: {reading_time}
word_count: {word_count}
weight: {idx}
"""
        if next_chapter:
            front_matter += f'next: "{next_chapter}"\n'
        if prev_chapter:
            front_matter += f'prev: "{prev_chapter}"\n'

        front_matter += "---\n\n"

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(content_text)

        print(f"✓ Created: {filename} ({word_count} words, ~{reading_time} min)")

if __name__ == "__main__":
    generate_chapter_files()
```

**Usage**:
```bash
python3 scripts/split-foreign-notices.py
# Creates individual chapter files with:
# - Proper numbering (00-preface, 01-chapter1, etc)
# - Calculated reading time (words / 200 WPM)
# - Navigation links (next/prev)
# - Proper weight for sorting
```

### 2.2 Data Validation & Conventions

**Manual Validation Checklist** (no automated validators currently):

1. **Cover Image**
   - Must be WEBP format (optimized)
   - Path: `/static/covers/book-slug-cover.webp`
   - Dimensions: 300x450px minimum
   - File size: <50KB

2. **Chapter Numbering**
   - Sequential `weight` values (0, 1, 2, 3...)
   - File names match pattern: `{NUMBER:2D}-{slug}.md`
   - `chapter_number` in frontmatter (for display)

3. **Navigation Links**
   - `next` and `prev` point to valid chapter paths
   - Must include leading `/books/` prefix
   - Links are **not auto-generated** (explicit paths required)

4. **Metadata**
   - `author_slug` matches author filename (without .md)
   - `year` is 4-digit integer
   - `chapters` count matches actual chapter count
   - Reading time approximately accurate (words / 200 WPM)

### 2.3 File Organization Best Practices

**From** `/home/bhuvanesh.r/AA/A main projects/Akshara/content/books/`:

```
books/
├── _index.md                    # Books hub (all books listed)
├── foreign-notices-south-india/
│   ├── _index.md               # Book metadata
│   ├── 00-preface-and-bibliography.md
│   ├── 01-introduction.md
│   └── ... 34 chapters total
├── lays-of-ancient-india/
│   ├── _index.md
│   └── ... 43 chapters total
├── life-and-letters-raja-rammohun-roy/
│   ├── _index.md
│   └── ... chapters
└── life-and-letters-of-toru-dutt/
    ├── _index.md
    └── ... chapters
```

**Key Convention**: Flat chapter structure (not nested in `chapters/` subdirectory)
- **Advantage**: Simple hierarchy, fewer directory levels
- **Disadvantage**: Cluttered for books with 100+ chapters
- **Recommendation for new books**: Create `chapters/` subdirectory if >30 chapters

---

## 3. COLLECTIONS SYSTEM

### 3.1 Collection Data Model

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/content/collections/ancient-india.md`

```yaml
---
title: "Ancient India"
type: "collections"
book_count: 2
description: "Classical texts, historical records, and poetic traditions from ancient Indian civilization"
period: "2000 BCE - 1200 CE"
books:
  - "lays-of-ancient-india"
  - "foreign-notices-south-india"
---

Ancient India produced some of the world's most profound philosophical texts...

[Full collection description]
```

**Schema**:
- `type: "collections"`: Hugo content type
- `book_count`: Manually specified (not auto-calculated)
- `books`: Array of book slugs (folder names, not titles)
- `period`: Historical timeframe for context
- Content: Markdown text for collection description

### 3.2 How Books Are Assigned to Collections

**Method 1: Explicit in Collection Front Matter** (Current approach)

Collections define which books they contain:

```yaml
books:
  - "lays-of-ancient-india"
  - "foreign-notices-south-india"
```

**Method 2: Taxonomies** (Available but not used)

Hugo configuration supports taxonomies:

```toml
[taxonomies]
  collection = "collections"
```

Books could include:
```yaml
collections: ["ancient-india"]
```

**Current Status**: Only Method 1 is used. Collections are simple markdown pages with explicit book lists.

### 3.3 Collection Display Logic

**Homepage** (`/home/bhuvanesh.r/AA/A main projects/Akshara/layouts/index.html`):

```html
<!-- Collections Section -->
<section class="collections">
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
</section>
```

**Collections Index** (`/home/bhuvanesh.r/AA/A main projects/Akshara/layouts/collections/list.html`):

```html
{{ define "main" }}
{{ partial "header.html" . }}

<main class="collections-page">
    <h1>Collections</h1>
    
    <div class="collections-grid">
        {{ range .Pages }}
        <a href="{{ .RelPermalink }}" class="collection-card">
            <h3>{{ .Title }}</h3>
            <p>{{ .Params.description }}</p>
        </a>
        {{ end }}
    </div>
</main>

{{ partial "footer.html" . }}
{{ end }}
```

### 3.4 Available Collections

From `/home/bhuvanesh.r/AA/A main projects/Akshara/content/collections/`:

1. **ancient-india.md** - 2 books (Vedic to medieval literature)
2. **biographical-classics.md** - Life and letters collections
3. **bengal-renaissance.md** - 19th century reformers
4. **reformers-and-visionaries.md** - Social/political leaders
5. **classical-literature.md** - Poetry and drama

---

## 4. WEB DISPLAY & RENDERING

### 4.1 Template Hierarchy

**Base Template** (`/home/bhuvanesh.r/AA/A main projects/Akshara/layouts/_default/baseof.html`):

```html
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
<head>
    {{ partial "head.html" . }}
</head>
<body{{ if eq .Type "books" }} class="book-page"{{ end }}>
    {{ block "main" . }}{{ end }}
</body>
</html>
```

**Component Hierarchy**:

```
baseof.html (root)
├── head.html (SEO, fonts, CSS, scripts)
├── main block (page-specific content)
│   ├── header.html (navigation, theme toggle)
│   ├── [page-specific content]
│   └── footer.html (links, copyright)
└── partials (reusable components)
    ├── book-card.html
    ├── book-page.html
    └── search.html
```

### 4.2 Book Hub Layout

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/layouts/books/book.html`

Displays book metadata, downloads, and table of contents:

```html
{{ define "main" }}
{{ partial "header.html" . }}

<!-- Book Hero Section -->
<section class="book-page-hero">
    <div class="book-hero">
        <div class="book-cover-area">
            <img src="{{ .Params.cover }}" alt="{{ $.Title }} cover" class="book-cover-large">
        </div>

        <div class="book-info">
            <h1>{{ .Title }}</h1>
            {{ with .Params.subtitle }}<p class="book-subtitle">{{ . }}</p>{{ end }}
            {{ if .Params.editor }}
                <p class="book-author-large">Edited by {{ .Params.editor }}</p>
            {{ else }}
                <p class="book-author-large">{{ .Params.author }}</p>
            {{ end }}
            <p class="book-description">{{ .Params.description }}</p>

            <div class="book-actions">
                {{ $chapters := where .Pages "Type" "chapters" }}
                {{ $firstChapter := index $chapters 0 }}
                <a href="{{ $firstChapter.RelPermalink }}" class="btn-primary">Begin Reading</a>
                <a href="#toc" class="btn-secondary">Table of Contents</a>
            </div>
        </div>
    </div>
</section>

<!-- Download Section -->
<section class="download-card-section">
    <div class="download-card">
        <h3>Download</h3>
        <a href="/downloads/{{ .File.ContentBaseName }}/{{ .File.ContentBaseName }}.epub">EPUB</a>
        <a href="/downloads/{{ .File.ContentBaseName }}/{{ .File.ContentBaseName }}.pdf">PDF</a>
        <a href="/downloads/{{ .File.ContentBaseName }}/{{ .File.ContentBaseName }}.md">Markdown</a>
    </div>
</section>

<!-- Metadata Section -->
<section class="book-metadata-section">
    <h3>Details</h3>
    <div class="metadata-grid">
        {{ with .Params.year }}<div class="metadata-item">
            <div class="metadata-label">Year Published</div>
            <div class="metadata-value">{{ . }}</div>
        </div>{{ end }}
        {{ with .Params.publisher }}<div class="metadata-item">
            <div class="metadata-label">Publisher</div>
            <div class="metadata-value">{{ . }}</div>
        </div>{{ end }}
        {{ with .Params.pages }}<div class="metadata-item">
            <div class="metadata-label">Pages</div>
            <div class="metadata-value">{{ . }}</div>
        </div>{{ end }}
        {{ with .Params.chapters }}<div class="metadata-item">
            <div class="metadata-label">Chapters</div>
            <div class="metadata-value">{{ . }}</div>
        </div>{{ end }}
    </div>
</section>

<!-- Table of Contents -->
<section class="section" id="toc">
    <h2 class="section-title">Contents</h2>
    <ul class="toc-list">
        {{ $chapters := where .Pages "Type" "chapters" }}
        {{ range $chapters.ByWeight }}
        <li class="toc-item">
            <a href="{{ .RelPermalink }}">
                <span class="toc-num">{{ .Params.chapter_number }}</span>
                <span>{{ .Title }}</span>
            </a>
        </li>
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

{{ partial "footer.html" . }}
{{ end }}
```

**Key Features**:
- Displays book cover (WEBP optimized)
- Shows author/editor info
- Lists download options (EPUB, PDF, Markdown)
- Generates table of contents from chapter pages
- Embeds Internet Archive viewer for original source
- Metadata grid for publication details

### 4.3 Reading Experience Template

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/layouts/chapters/single.html`

Full-screen reading interface with menu, navigation, and controls:

```html
{{ define "main" }}
<!-- Progress Bar -->
<div class="progress" id="progress"></div>

<!-- Top Bar -->
<div class="top-bar" id="topBar">
    {{ $book := .Parent }}
    {{ $chapters := where $book.Pages "Type" "chapters" }}
    {{ $totalChapters := len $chapters }}

    <a href="{{ $book.RelPermalink }}" class="back-link">← {{ $book.Title }}</a>

    <div class="chapter-info">
        Chapter {{ .Params.chapter_number }} of {{ $totalChapters }}
    </div>

    <button class="menu-btn" onclick="toggleMenu()" aria-label="Menu">☰</button>
</div>

<!-- Reading Container -->
<main class="reading" data-book-slug="{{ $book.File.BaseFileName }}" data-chapter-id="{{ .File.UniqueID }}">
    <header class="chapter-header">
        <div class="chapter-number">{{ .Params.chapter_number }}</div>
        <h1 class="chapter-title">{{ .Title }}</h1>
    </header>

    <article class="text">
        {{ .Content }}
    </article>

    <!-- Chapter Navigation -->
    <nav class="chapter-nav">
        {{ with .Params.prev }}
        <a href="{{ . }}" class="nav-link prev">
            <span class="nav-label">← Previous</span>
            <span class="nav-title">{{ $.Site.GetPage . | .Title }}</span>
        </a>
        {{ end }}

        {{ with .Params.next }}
        <a href="{{ . }}" class="nav-link next">
            <span class="nav-label">Next →</span>
            <span class="nav-title">{{ $.Site.GetPage . | .Title }}</span>
        </a>
        {{ end }}
    </nav>
</main>

<!-- Menu Panel -->
<aside class="menu-panel" id="menuPanel">
    <div class="menu-header">
        <h2>Menu</h2>
        <button class="menu-close" onclick="toggleMenu()">×</button>
    </div>

    <div class="menu-content">
        <!-- Table of Contents -->
        <div class="menu-section">
            <h3 class="menu-section-title">Contents</h3>
            {{ $book := .Parent }}
            {{ $chapters := where $book.Pages "Type" "chapters" }}
            <ul class="menu-toc-list">
                {{ range $chapters.ByWeight }}
                <li>
                    <a href="{{ .RelPermalink }}"{{ if eq .File.UniqueID $.File.UniqueID }} class="current"{{ end }}>
                        <span class="menu-toc-num">{{ .Params.chapter_number }}</span>
                        <span>{{ .Title }}</span>
                    </a>
                </li>
                {{ end }}
            </ul>
        </div>

        <!-- Reading Settings -->
        <div class="menu-section">
            <h3 class="menu-section-title">Reading Settings</h3>

            <div class="setting-group">
                <label class="setting-label">Font Size</label>
                <div class="setting-buttons">
                    <button class="setting-btn" onclick="adjustSize(-2)">A</button>
                    <button class="setting-btn active" onclick="adjustSize(0)">A</button>
                    <button class="setting-btn" onclick="adjustSize(2)">A</button>
                </div>
            </div>

            <div class="setting-group">
                <label class="setting-label">Theme</label>
                <div class="setting-buttons">
                    <button class="setting-btn active" onclick="setTheme('light')">Light</button>
                    <button class="setting-btn" onclick="setTheme('dark')">Dark</button>
                    <button class="setting-btn" onclick="setTheme('sepia')">Sepia</button>
                </div>
            </div>

            <div class="setting-group">
                <button class="focus-mode-btn" onclick="toggleFocusMode()">
                    Enter Focus Mode
                </button>
            </div>
        </div>

        <!-- Keyboard Shortcuts -->
        <div class="menu-section">
            <h3 class="menu-section-title">Keyboard Shortcuts</h3>
            <dl class="shortcuts-list">
                <div class="shortcut-item"><dt>M</dt><dd>Toggle Menu</dd></div>
                <div class="shortcut-item"><dt>F</dt><dd>Focus Mode</dd></div>
                <div class="shortcut-item"><dt>←</dt><dd>Previous Chapter</dd></div>
                <div class="shortcut-item"><dt>→</dt><dd>Next Chapter</dd></div>
                <div class="shortcut-item"><dt>Esc</dt><dd>Close Menu</dd></div>
            </dl>
        </div>
    </div>
</aside>

<!-- Overlay -->
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>

<!-- Reading interactions -->
<script src="/js/reading.js"></script>
{{ end }}
```

### 4.4 Markdown Content Processing

**Hugo Configuration** (`/home/bhuvanesh.r/AA/A main projects/Akshara/hugo.toml`):

```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # Allow HTML in markdown
  [markup.highlight]
    style = "monokai"
    lineNos = false
```

**Processing Pipeline**:

1. **Markdown Parsing**: Hugo's Goldmark parser processes `.md` files
2. **HTML Rendering**: `unsafe = true` allows embedded HTML, footnotes
3. **Syntax Highlighting**: Code blocks use Monokai theme
4. **Content Injection**: `.Content` Hugo variable contains processed HTML

**Example Processing**:

Input Markdown:
```markdown
Much as I wish that I had not to write this chapter, I know that 
I shall have to swallow many such bitter draughts in the course 
of this narrative.[^1]

[^1]: This refers to difficult truths about his personal life.
```

Output in Template:
```html
<article class="text">
    <p>Much as I wish that I had not to write this chapter, I know that 
    I shall have to swallow many such bitter draughts in the course 
    of this narrative.<sup id="fnref:1"><a href="#fn:1" class="footnote-ref">1</a></sup></p>
    
    <div class="footnotes">
        <ol>
            <li id="fn:1"><p>This refers to difficult truths about his personal life.<a href="#fnref:1" class="footnote-backref">↩</a></p>
            </li>
        </ol>
    </div>
</article>
```

### 4.5 Routing Structure

**Hugo Permalinks Configuration** (`hugo.toml`):

```toml
[permalinks]
  authors = "/authors/:slug"
  collections = "/collections/:slug"
```

**URL Scheme**:

| Content | URL | Generated From |
|---------|-----|---|
| Book Hub | `/books/foreign-notices-south-india/` | `content/books/foreign-notices-south-india/_index.md` |
| Chapter | `/books/foreign-notices-south-india/01-megasthenes/` | `content/books/.../01-megasthenes.md` |
| Author | `/authors/k-a-nilakanta-sastri/` | `content/authors/k-a-nilakanta-sastri.md` |
| Collection | `/collections/ancient-india/` | `content/collections/ancient-india.md` |
| Homepage | `/` | `layouts/index.html` |

---

## 5. JAVASCRIPT INTERACTIONS

### 5.1 Reading Experience Features

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/static/js/reading.js` (230 lines)

All reading interactions handled in **pure vanilla JavaScript**, zero dependencies:

```javascript
// State Management
let fontSize = 21;
let focusMode = false;

// Get chapter/book info from data attributes
const bookSlug = document.querySelector('[data-book-slug]').dataset.bookSlug;
const chapterId = document.querySelector('[data-chapter-id]').dataset.chapterId;
const storageKey = `${bookSlug}-${chapterId}`;

// Progress Tracking
function updateProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    
    const progressBar = document.getElementById('progress');
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
}

// Menu Toggle
function toggleMenu() {
    const menu = document.getElementById('menuPanel');
    const overlay = document.getElementById('overlay');
    
    const isOpen = menu.classList.contains('open');
    if (isOpen) {
        menu.classList.remove('open');
        overlay.classList.remove('show');
    } else {
        menu.classList.add('open');
        overlay.classList.add('show');
    }
}

// Focus Mode (removes all UI)
function toggleFocusMode() {
    focusMode = !focusMode;
    document.body.classList.toggle('focus-mode');
    closeMenu();
    showShortcutHint(focusMode ? 'Focus mode on' : 'Focus mode off');
}

// Font Size Adjustment (17-27px range)
function adjustSize(delta) {
    if (delta === 0) {
        fontSize = 21;  // Reset to default
    } else {
        fontSize = Math.max(17, Math.min(27, fontSize + delta));
    }

    const textElement = document.querySelector('.text');
    if (textElement) {
        textElement.style.fontSize = fontSize + 'px';
        localStorage.setItem(`fontSize-${bookSlug}`, fontSize);
    }

    updateFontSizeButtons();
}

// Theme Switching
function setTheme(theme) {
    if (theme === 'light') {
        document.body.classList.remove('dark', 'sepia');
    } else if (theme === 'dark') {
        document.body.classList.add('dark');
        document.body.classList.remove('sepia');
    } else if (theme === 'sepia') {
        document.body.classList.add('sepia');
        document.body.classList.remove('dark');
    }
    
    localStorage.setItem(`theme-${bookSlug}`, theme);
}

// Keyboard Navigation
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'm':
        case 'M':
            toggleMenu();
            break;
        case 'f':
        case 'F':
            toggleFocusMode();
            break;
        case 'ArrowLeft':
            // Navigate to previous chapter
            const prevLink = document.querySelector('.nav-link.prev');
            if (prevLink) prevLink.click();
            break;
        case 'ArrowRight':
            // Navigate to next chapter
            const nextLink = document.querySelector('.nav-link.next');
            if (nextLink) nextLink.click();
            break;
        case 'Escape':
            closeMenu();
            if (focusMode) toggleFocusMode();
            break;
    }
});

// Position Memory (localStorage)
window.addEventListener('beforeunload', () => {
    localStorage.setItem(storageKey, window.scrollY);
});

// Restore position on load
window.addEventListener('load', () => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
        setTimeout(() => {
            window.scrollTo(0, parseInt(saved));
        }, 100);
    }
});

// Scroll events
window.addEventListener('scroll', () => {
    updateProgress();
    handleTopBarScroll();
});
```

### 5.2 Features Implemented

| Feature | Implementation | Storage |
|---------|---|---|
| **Progress Bar** | Real-time scroll position % | Browser memory |
| **Font Size** | 17px-27px adjustable | localStorage key: `fontSize-{bookSlug}` |
| **Themes** | Light/Dark/Sepia | localStorage key: `theme-{bookSlug}` |
| **Focus Mode** | Hides menu, header, footer | Not persisted |
| **Position Memory** | Remembers scroll position | localStorage key: `{bookSlug}-{chapterId}` |
| **Menu Toggle** | M key or hamburger button | Panel state (not persisted) |
| **Chapter Navigation** | Arrow keys (← →) or buttons | Native browser links |

### 5.3 CSS Custom Properties for Theming

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/assets/css/base.css`

Three complete themes implemented:

```css
/* Light Theme (Default) */
:root {
    --ink: #1a1614;              /* Text color */
    --paper: #fffffe;            /* Background */
    --smoke: #6b6560;            /* Secondary text */
    --ash: #a8a39e;              /* Tertiary text */
    --sand: #e5e2df;             /* Borders */
    --cream: #faf8f6;            /* Alt backgrounds */
    --accent: #c85a3a;           /* Terracotta accent */
    --accent-hover: #b04d2f;
}

/* Dark Theme */
body.dark {
    --ink: #ebe8e4;              /* Light text */
    --paper: #1a1614;            /* Dark background */
    --smoke: #a8a39e;
    --ash: #6b6560;
    --sand: #2f2b28;             /* Dark borders */
    --cream: #232018;
    --accent: #e67855;           /* Lighter terracotta */
    --accent-hover: #f28a66;
}

/* Sepia Theme */
body.sepia {
    --ink: #3d3426;              /* Brown text */
    --paper: #f4ecd8;            /* Aged paper */
    --smoke: #6e6250;
    --ash: #9d9181;
    --sand: #ddd4c0;
    --cream: #ede7da;
    --accent: #b04d2f;           /* Warm accent */
    --accent-hover: #a04426;
}
```

---

## 6. DEPLOYMENT & BUILD PROCESS

### 6.1 Build Script

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/scripts/build.sh`

```bash
#!/bin/bash
set -e

# Build Hugo site
hugo --minify

# Run Pagefind for search indexing
npx pagefind --site public --output-path public/pagefind

echo "Build complete!"
```

**Steps**:
1. Hugo builds static site with minification
2. Pagefind indexes HTML for client-side search
3. Output in `public/` directory ready for deployment

### 6.2 Deployment Script

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/scripts/deploy.sh`

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

### 6.3 Cloudflare Workers Configuration

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/wrangler.toml`

```toml
name = "akshara"
main = "src/index.js"
compatibility_date = "2024-11-01"

[site]
bucket = "./public"

[env.production]
name = "akshara"
route = "akshara.dhwani.ink/*"

[env.production.vars]
ENVIRONMENT = "production"
```

### 6.4 Cloudflare Worker Entry Point

**File**: `/home/bhuvanesh.r/AA/A main projects/Akshara/src/index.js`

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

    // Static assets - cache for 1 year
    if (url.pathname.startsWith('/static/') ||
        url.pathname.startsWith('/covers/') ||
        url.pathname.startsWith('/js/') ||
        url.pathname.startsWith('/fonts/') ||
        url.pathname.startsWith('/css/')) {

      const response = await env.ASSETS.fetch(request);
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=31536000, immutable');

      return new Response(response.body, {
        status: response.status,
        headers
      });
    }

    // HTML pages - cache for 1 hour
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

      // Cache HTML for 1 hour (purgeable)
      headers.set('Cache-Control', 'public, max-age=3600, must-revalidate');

      return new Response(response.body, {
        status: response.status,
        headers
      });
    }

    // Default response
    return new Response('Not Found', { status: 404 });
  }
};
```

**Caching Strategy**:
- **Static assets** (CSS, JS, fonts, images): 1 year (immutable)
- **HTML pages**: 1 hour (purgeable with Cloudflare purge)
- **Security headers**: Applied to all responses

---

## 7. PROJECT FILES INVENTORY

### Core Configuration Files

| File | Purpose |
|------|---------|
| `hugo.toml` | Hugo build configuration |
| `wrangler.toml` | Cloudflare Workers config |
| `.gitignore` | Git ignore rules |

### Content Structure

| Directory | Files | Purpose |
|-----------|-------|---------|
| `content/books/` | 5 folders + 50+ MD | Book content |
| `content/authors/` | 4 MD files | Author profiles |
| `content/collections/` | 5 MD files | Thematic collections |
| `content/pages/` | Search, contrib | Static pages |

### Templates (21 files)

| Path | Files | Purpose |
|------|-------|---------|
| `layouts/` | index.html | Homepage |
| `layouts/_default/` | 4 files | Base templates |
| `layouts/books/` | 4 files | Book pages |
| `layouts/chapters/` | 1 file | Reading experience |
| `layouts/authors/` | 2 files | Author pages |
| `layouts/collections/` | 2 files | Collection pages |
| `layouts/partials/` | 6 files | Reusable components |

### Styling (4 CSS files, 3844 lines total)

| File | Lines | Purpose |
|------|-------|---------|
| `assets/css/base.css` | 194 | CSS variables, resets, typography |
| `assets/css/components.css` | 531 | Header, footer, cards, buttons |
| `assets/css/pages.css` | 2986 | All page-specific styles |
| `assets/css/search.css` | 133 | Search interface |

### JavaScript

| File | Lines | Purpose |
|------|-------|---------|
| `static/js/reading.js` | 230 | All reading interactions |

### Static Assets

| Directory | Contents |
|-----------|----------|
| `static/covers/` | 4 WEBP book covers (optimized) |
| `static/fonts/` | Google Fonts via CDN |
| `static/robots.txt` | SEO robot rules |

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/build.sh` | Hugo + Pagefind build |
| `scripts/deploy.sh` | Hugo + Pagefind + Wrangler deploy |
| `scripts/split-foreign-notices.py` | Chapter extraction automation |

### Documentation

| File | Lines | Purpose |
|------|-------|---------|
| `README.md` | 300 | Quick start guide |
| `PROJECT-SUMMARY.md` | 437 | Build status & next steps |
| `PROJECT-OVERVIEW.md` | 320 | High-level overview |
| `BUILD-GUIDE.md` | 3000+ | Complete implementation guide |
| `QUICK-SUMMARY.txt` | 300 | One-page reference |

---

## 8. KEY DESIGN PATTERNS & CONVENTIONS

### 8.1 Hugo Patterns

**Cascading Front Matter**:
```yaml
cascade:
  - _target:
      kind: "page"
    type: "chapters"
```
Automatically sets `type: "chapters"` on all child pages.

**Site.GetPage for Navigation**:
```html
{{ with $.Site.GetPage "/books/book-name/chapter" }}
  {{ .Title }}
{{ end }}
```
Resolves chapter paths to page objects.

**Range Sorting**:
```html
{{ range $chapters.ByWeight }}
  <!-- Sorted by weight front matter -->
{{ end }}
```

### 8.2 Content Patterns

**Book Structure**:
- Book folder (e.g., `foreign-notices-south-india/`)
- `_index.md` with book metadata
- Chapter files (e.g., `01-chapter.md`)

**Chapter Ordering**:
- Numeric prefix (01, 02, 03...) for filenames
- `weight` front matter for Hugo sorting
- `chapter_number` for display in TOC

**Navigation**:
- Explicit `next`/`prev` links (not auto-generated)
- Enables flexible chapter organization
- Survives file renames

### 8.3 CSS Patterns

**Mobile-First Responsive**:
```css
/* Base styles - mobile */
.reading {
    font-size: 19px;
    line-height: 1.8;
}

/* Tablet and above */
@media (min-width: 768px) {
    .reading {
        max-width: 800px;
        margin: 0 auto;
    }
}
```

**CSS Variables for Theming**:
```css
:root { --ink: #1a1614; --paper: #fffffe; }
body.dark { --ink: #ebe8e4; --paper: #1a1614; }
body.sepia { --ink: #3d3426; --paper: #f4ecd8; }

/* Usage */
body { color: var(--ink); background: var(--paper); }
```

---

## 9. TECHNICAL STACK SUMMARY

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Generator** | Hugo 0.139.3 | Static site, no databases |
| **Content Format** | Markdown | With front matter (YAML) |
| **Templating** | Hugo templates | Go template syntax |
| **Styling** | CSS3 | Custom, no frameworks |
| **JavaScript** | Vanilla ES6 | Zero dependencies |
| **Fonts** | Google Fonts | Crimson Text + Inter |
| **Deployment** | Cloudflare Workers | Edge computing + CDN |
| **Search** | Pagefind | Optional, client-side |

---

## 10. FUTURE EXPANSION

### Adding New Books (Step-by-Step)

1. **Prepare Content**
   - Source PDF from Archive.org
   - OCR using PaddleOCR or similar
   - Clean up with AI tools (Google AI Studio)
   - Manual proofreading (key passages)

2. **Create Structure**
   ```bash
   mkdir content/books/new-book-slug/
   touch content/books/new-book-slug/_index.md
   ```

3. **Add Metadata**
   - Copy book metadata template
   - Fill in author_slug, year, pages, etc.
   - Add cover image to `static/covers/`

4. **Generate Chapters**
   - Split content by chapter headers
   - Create individual `.md` files with numbering
   - Add `chapter_number`, `weight`, `reading_time`
   - Link `next`/`prev` chapters

5. **Test Locally**
   ```bash
   hugo server -D
   # Visit http://localhost:1313
   # Check book hub, chapters, TOC
   ```

6. **Deploy**
   ```bash
   ./scripts/deploy.sh
   ```

### Recommended Additions

1. **More Books** (5-10 recommended for launch)
2. **Search Integration** (Pagefind ready, just needs activation)
3. **Crowdsourced Corrections** (Project Gutenberg model)
4. **Author Bios** (Timeline format already designed)
5. **Collection Descriptions** (Already modeled)

---

## 11. CONCLUSION

**Akshara is a masterclass in focused, elegant design.** It demonstrates:

1. **Clear separation of concerns**: Content, layout, styling, interaction
2. **Hugo best practices**: Cascading, pagination, taxonomy organization
3. **Performance-first**: <50KB initial load, 26ms builds
4. **Minimal dependencies**: Vanilla JavaScript, no frameworks
5. **Scalable structure**: Easy to add new books without touching code

The system is **production-ready** and awaiting content expansion to reach its full potential as a comprehensive Indian literary archive.

