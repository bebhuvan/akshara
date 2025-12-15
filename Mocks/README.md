# Akshara - Complete Design System

A warm, sophisticated design system for Indian literary archives. 12 complete page templates ready for Hugo implementation.

---

## 🎨 [View the Complete System](computer:///mnt/user-data/outputs/complete-site-map.html)

---

## 📄 All Pages

### Core Reading Experience (3 pages)
1. **[Landing Page](computer:///mnt/user-data/outputs/elevated-landing.html)** - Homepage with hero, featured book, collections
2. **[Book Hub](computer:///mnt/user-data/outputs/elevated-book-hub.html)** - Book introduction with metadata, TOC, downloads
3. **[Reading Experience](computer:///mnt/user-data/outputs/elevated-reading.html)** - Full immersion with focus mode, shortcuts

### Browse & Discovery (6 pages)
4. **[All Books](computer:///mnt/user-data/outputs/browse-books.html)** - Complete catalog with filters and search
5. **[Collections Directory](computer:///mnt/user-data/outputs/collections.html)** - All thematic collections
6. **[Individual Collection](computer:///mnt/user-data/outputs/collection-page.html)** - Single collection with books
7. **[Authors Directory](computer:///mnt/user-data/outputs/authors-directory.html)** - Alphabetical author listing
8. **[Author Page](computer:///mnt/user-data/outputs/author-page.html)** - Individual author with timeline
9. **[Browse by Period](computer:///mnt/user-data/outputs/by-period.html)** - Timeline-based browsing

### Utility (3 pages)
10. **[Search Results](computer:///mnt/user-data/outputs/search-results.html)** - Search with filters
11. **[About](computer:///mnt/user-data/outputs/about.html)** - Mission, methodology, contribute
12. **[404 Error](computer:///mnt/user-data/outputs/404.html)** - Warm, helpful error page

---

## 📖 Documentation

- **[Complete Site Map](computer:///mnt/user-data/outputs/complete-site-map.html)** - Visual overview of all pages
- **[Design System Showcase](computer:///mnt/user-data/outputs/elevated-index.html)** - Features and principles
- **[Implementation Guide](computer:///mnt/user-data/outputs/IMPLEMENTATION-GUIDE.md)** - Full technical details

---

## 🎯 Key Features

### Reading Experience
✅ **Focus Mode** (F key) - Complete UI removal  
✅ **Keyboard Shortcuts** - T, S, F, Arrow keys  
✅ **Reading Time** - Estimates on every chapter  
✅ **Progress Tracking** - Percentage and chapter count  
✅ **Position Memory** - LocalStorage scroll position  
✅ **Three Themes** - Light, Dark, Sepia  
✅ **Smart Controls** - Auto-hide during reading  
✅ **Print Styles** - Beautiful printed output  

### Design
✅ **Libre Baskerville** - Warm, editorial serif  
✅ **Inter** - Clean sans-serif for UI  
✅ **Terracotta Accent** - #c85a3a  
✅ **Paper Background** - #fffef9 (not stark white)  
✅ **No Borders** - Depth through space and backgrounds  
✅ **Dramatic Typography** - 11px to 96px scale  

### Technical
✅ **Hugo Ready** - All templates designed for Hugo  
✅ **Pagefind Search** - Client-side, no server needed  
✅ **Cloudflare Pages** - Auto-deploy setup  
✅ **Minimal JS** - ~15KB for all interactions  
✅ **Mobile First** - Optimized for mobile traffic  
✅ **Performance** - <50KB initial load  

---

## 🛠 Tech Stack

- **Hugo** - Static site generator
- **Libre Baskerville + Inter** - Typography (Google Fonts)
- **Cloudflare Pages** - Hosting and CDN
- **Cloudflare R2** - Asset storage
- **Pagefind** - Search
- **Vanilla JS** - No frameworks

---

## 🎨 Color Palette

```css
--ink: #1a1412          /* Primary text */
--paper: #fffef9        /* Background */
--smoke: #6b6560        /* Secondary text */
--ash: #9c948e          /* Tertiary text */
--sand: #e8e3dd         /* Borders */
--cream: #f5f2ec        /* Alt backgrounds */
--terracotta: #c85a3a   /* Accent */
```

---

## 📏 Typography Scale

- **Hero** - 96px Libre Baskerville
- **Page Title** - 72-88px Libre Baskerville
- **Section Title** - 48-56px Libre Baskerville
- **Book Title** - 32-40px Libre Baskerville
- **Reading Text** - 21px Libre Baskerville
- **Body Text** - 15-17px Inter
- **UI Text** - 13-14px Inter
- **Labels** - 11px Inter uppercase

---

## 🚀 Quick Start

### 1. Set Up Hugo
```bash
hugo new site akshara
cd akshara
```

### 2. Add Content Structure
```
content/
  books/
    [book-slug]/
      _index.md
      chapters/
        01-chapter.md
        02-chapter.md
  authors/
    [author-slug].md
  collections/
    [collection-slug].md
```

### 3. Copy Templates
Convert HTML files to Hugo templates in `layouts/`

### 4. Configure Hugo
```toml
baseURL = "https://akshara.dhwani.ink"
languageCode = "en-us"
title = "Akshara"
theme = "akshara"

[params]
  description = "An archive of Indian literature"
```

### 5. Deploy to Cloudflare
- Connect Git repository
- Build command: `hugo`
- Output directory: `public`

---

## 📋 Content Checklist

For each book, you need:
- [ ] Book metadata (title, author, year, language)
- [ ] Chapter-by-chapter Markdown files
- [ ] Cover image (2:3 aspect ratio)
- [ ] Reading time estimate
- [ ] Historical context/about section
- [ ] Table of contents
- [ ] Download files (EPUB, Markdown, Text)
- [ ] Archive.org source link
- [ ] Wikipedia/reference links

---

## 🎯 What Makes This Different

**Not Another Archive Template**

Most digital archives look like databases. This feels like a curated collection. Every detail—from the 5.2em terracotta drop caps to the keyboard shortcuts—serves the reading experience.

**Typography as Design**

No decoration. No borders. No shadows everywhere. Just dramatic typography scales (11px to 96px), generous white space (120px+ section spacing), and a warm color palette that feels like paper, not a screen.

**Features That Matter**

Focus mode isn't a gimmick—it's how people actually read. Position memory isn't fancy—it's respectful of readers' time. Reading time estimates aren't decoration—they set expectations.

**Character Without Clichés**

Warm, not cold. Sophisticated, not generic. Indian, not stereotypically "Indian themed." Editorial quality, not web template.

---

## 📚 File Organization

```
/mnt/user-data/outputs/
├── elevated-landing.html          # Homepage
├── elevated-book-hub.html         # Book intro page
├── elevated-reading.html          # Reading experience
├── browse-books.html              # All books catalog
├── collections.html               # Collections directory
├── collection-page.html           # Single collection
├── authors-directory.html         # All authors
├── author-page.html               # Single author
├── by-period.html                 # Browse by period
├── search-results.html            # Search results
├── about.html                     # About page
├── 404.html                       # Error page
├── complete-site-map.html         # Visual overview
├── elevated-index.html            # Design showcase
├── IMPLEMENTATION-GUIDE.md        # Technical docs
└── README.md                      # This file
```

---

## 💡 Next Steps

1. **Review all pages** - Open complete-site-map.html
2. **Read implementation guide** - IMPLEMENTATION-GUIDE.md
3. **Set up Hugo** - Initialize project structure
4. **Start with core** - Landing, book hub, reading pages
5. **Add 5-10 books** - Test the system with real content
6. **Deploy** - Cloudflare Pages auto-deploy
7. **Iterate** - Based on real usage

---

## ✨ Vision

An archive that readers *want* to use. Not functional—exceptional. Every book deserves this level of care.

Built for Indian literary heritage.

---

**Ready to build?** Start with [complete-site-map.html](computer:///mnt/user-data/outputs/complete-site-map.html)
