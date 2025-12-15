# Akshara Complete Design System

A sophisticated design system for Indian literary archives with 12 complete page templates.

---

## 🎨 Design Principles

1. **Warmth Over Coldness** - Paper tones (#fffef9), not stark white
2. **Character Through Typography** - Libre Baskerville + Inter
3. **No Borders** - Depth through backgrounds and white space
4. **Dramatic Scale** - 88px headlines to 11px labels
5. **Reading First** - Every decision serves the text
6. **Restrained Color** - Grayscale + single terracotta accent

---

## 📄 Complete Page List (12 Pages)

### Core Pages (3)
1. **elevated-landing.html** - Archive homepage
2. **elevated-book-hub.html** - Book introduction page
3. **elevated-reading.html** - Full reading experience

### Discovery & Browse (6)
4. **browse-books.html** - All books with filters
5. **collections.html** - Collections directory
6. **collection-page.html** - Individual collection
7. **authors-directory.html** - All authors alphabetically
8. **author-page.html** - Individual author page
9. **by-period.html** - Browse by time period

### Utility (3)
10. **search-results.html** - Search results page
11. **about.html** - About/mission page
12. **404.html** - Error page

Plus:
- **complete-site-map.html** - Overview of all pages
- **elevated-index.html** - Design system showcase

---

## 🎯 Key Features

### Reading Experience
- **Focus Mode** (F key) - Hides all UI
- **Keyboard Shortcuts** - T (TOC), S (Settings), F (Focus), Arrows (Navigation)
- **Reading Time** - Estimates on every chapter
- **Progress Tracking** - "3 of 164 chapters · 18% complete"
- **Position Memory** - LocalStorage remembers scroll position
- **Smart Controls** - Appear on mouse move, hide during reading
- **Themes** - Light, Dark, Sepia with warm palettes
- **Print Styles** - Beautiful when printed

### Typography
- **Libre Baskerville** - All reading content (400, 700 weights)
- **Inter** - All UI elements (300, 400, 500, 600 weights)
- **Scale** - 11px labels to 96px headlines
- **Drop Caps** - 5.2em terracotta on first paragraph
- **Line Height** - 1.8 for comfortable reading
- **Custom Selection** - Terracotta tint background

### Color Palette
```css
--ink: #1a1412;           /* Text */
--paper: #fffef9;         /* Background */
--smoke: #6b6560;         /* Secondary text */
--ash: #9c948e;           /* Tertiary text */
--sand: #e8e3dd;          /* Borders */
--cream: #f5f2ec;         /* Backgrounds */
--terracotta: #c85a3a;    /* Accent */
```

### Layout
- **Max Width** - 1600px containers
- **Padding** - 80px desktop, 48px tablet, 32px mobile
- **Section Spacing** - 120px+ between sections
- **Reading Width** - 720px max for text
- **Grid Systems** - 2-col, 3-col, auto-fill patterns

---

## 🛠 Hugo Implementation

### Content Structure
```
content/
  books/
    gandhi-my-experiments/
      _index.md                 # Book metadata
      chapters/
        01-birth.md
        02-childhood.md
        03-child-marriage.md
        [...]
  authors/
    _index.md
    gandhi.md
  collections/
    _index.md
    freedom-struggle.md
```

### Front Matter Example
```yaml
---
title: "My Experiments with Truth"
author: "Mahatma Gandhi"
author_slug: "gandhi"
year: 1927
language: "English"
translator: "Mahadev Desai"
pages: 454
chapters: 164
reading_time: "~8 hours"
themes: ["autobiography", "philosophy", "resistance"]
collection: "freedom-struggle"
period: "1901-1930"
archive_url: "https://archive.org/details/..."
wikipedia_url: "https://en.wikipedia.org/wiki/..."
download_epub: "/downloads/gandhi-experiments.epub"
download_markdown: "/downloads/gandhi-experiments.md"
download_text: "/downloads/gandhi-experiments.txt"
---
```

### Hugo Templates Needed
- `layouts/index.html` → Landing
- `layouts/books/single.html` → Book hub
- `layouts/books/chapter.html` → Reading experience
- `layouts/authors/single.html` → Author page
- `layouts/authors/list.html` → Authors directory
- `layouts/collections/single.html` → Collection page
- `layouts/collections/list.html` → Collections directory
- `layouts/_default/search.html` → Search results
- `layouts/404.html` → Error page

---

## 🚀 Tech Stack

### Static Generation
- **Hugo** - Fast builds, simple deployment
- **Markdown** - Content format
- **Git** - Version control and content management

### Hosting & CDN
- **Cloudflare Pages** - Auto-deploy from Git
- **Cloudflare R2** - EPUB and large file storage
- **Global CDN** - Edge caching worldwide

### Search
- **Pagefind** - Client-side search
- No server needed
- Works offline
- Build-time indexing

### Fonts
- **Google Fonts** - Libre Baskerville, Inter
- Variable weights for both
- Self-hosted option available

### JavaScript
- Minimal vanilla JS for:
  - Reading controls
  - TOC drawer
  - Theme switching
  - Keyboard shortcuts
  - Position memory
  - Progress tracking
  - Focus mode

---

## 📱 Responsive Breakpoints

```css
/* Desktop */
@media (min-width: 1024px) {
  padding: 80px;
  grid-template-columns: repeat(3, 1fr);
}

/* Tablet */
@media (max-width: 1024px) {
  padding: 48px;
  grid-template-columns: repeat(2, 1fr);
}

/* Mobile */
@media (max-width: 640px) {
  padding: 32px;
  grid-template-columns: 1fr;
}
```

---

## 🎨 Component Patterns

### Buttons
```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: var(--ink);
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.03em;
  transition: all 0.3s ease;
}

.btn-primary::after {
  content: '→';
  transition: transform 0.3s ease;
}

.btn-primary:hover {
  color: var(--terracotta);
}

.btn-primary:hover::after {
  transform: translateX(4px);
}
```

### Cards
```css
.book-card {
  text-decoration: none;
  color: var(--ink);
  transition: all 0.3s ease;
}

.book-card:hover {
  transform: translateY(-8px);
}

.book-card:hover .book-cover {
  box-shadow: 0 16px 48px rgba(26, 20, 18, 0.15);
}
```

### Filters
```css
.filter-btn {
  background: transparent;
  border: none;
  padding: 10px 20px;
  font-size: 13px;
  color: var(--smoke);
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 6px;
}

.filter-btn.active {
  background: var(--cream);
  color: var(--ink);
  font-weight: 500;
}
```

---

## 🔑 Keyboard Shortcuts

### Reading Page
- **T** - Toggle table of contents
- **S** - Toggle settings/controls
- **F** - Toggle focus mode
- **←** - Previous chapter
- **→** - Next chapter
- **Esc** - Close all panels / exit focus mode

### Implementation
```javascript
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  
  switch(e.key.toLowerCase()) {
    case 't': toggleTOC(); break;
    case 's': toggleControls(); break;
    case 'f': toggleFocusMode(); break;
    case 'escape': closeAll(); break;
  }
});
```

---

## 📊 Performance Targets

- **Initial Load** - <50KB HTML + CSS
- **JavaScript** - ~15KB total
- **Fonts** - WOFF2 with swap
- **Images** - Lazy loading
- **Build Time** - <5s for 250 books
- **Lighthouse** - 95+ on all metrics

---

## 🎭 Interactive States

### Hover Patterns
1. **Cards** - `translateY(-8px)` lift
2. **Links** - Color change to terracotta
3. **Arrows** - `translateX(4px)` shift
4. **Covers** - Enhanced shadow

### Transitions
- **Duration** - 0.3s for most
- **Easing** - `cubic-bezier(0.4, 0, 0.2, 1)`
- **Properties** - color, transform, opacity, shadow

---

## 📝 Content Guidelines

### Reading Time Calculation
```
Words per minute: 250 (average)
Reading time = (word_count / 250) rounded to nearest 15min
Display as "~2 hours" or "~12 minutes"
```

### Image Placeholders
All `.book-cover` divs are placeholders:
```css
.book-cover {
  aspect-ratio: 2/3;
  background: var(--cream);
}
```

Replace with actual cover images:
```html
<img src="/covers/gandhi-experiments.jpg" alt="Book cover" class="book-cover">
```

### Chapter Count
Include in book metadata and display in:
- Book hub ("164 chapters")
- TOC progress ("3 of 164")
- Search results metadata

---

## 🔍 SEO & Metadata

### Per Page
```html
<title>My Experiments with Truth - Akshara</title>
<meta name="description" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="/covers/...">
```

### Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "My Experiments with Truth",
  "author": "Mahatma Gandhi",
  "datePublished": "1927",
  "inLanguage": "en"
}
```

---

## 🎯 Next Steps

1. **Set up Hugo** - Initialize project, configure
2. **Add content** - Start with 5-10 books
3. **Implement templates** - Begin with landing, book hub, reading
4. **Add Pagefind** - Install and configure search
5. **Deploy to Cloudflare** - Connect Git, auto-deploy
6. **Test reading** - Focus mode, keyboard shortcuts, position memory
7. **Add analytics** - Privacy-respecting analytics
8. **Iterate** - Based on user feedback

---

## 📚 Resources

- **Hugo Docs** - https://gohugo.io/documentation/
- **Pagefind** - https://pagefind.app/
- **Cloudflare Pages** - https://pages.cloudflare.com/
- **Google Fonts** - Libre Baskerville, Inter
- **Archive.org API** - For source PDFs

---

## ✨ The Vision

Every book deserves an exceptional reading experience. Not functional—exceptional. This system treats literature with the care it deserves: warm colors, sophisticated typography, thoughtful interactions, and features that genuinely improve reading.

This is an archive that readers will *want* to use, not just *have* to use.

---

Built with care for Indian literary heritage.
