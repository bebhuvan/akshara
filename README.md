# Akshara - Indian Literary Archive

A warm, sophisticated design system for Indian literary archives built with Hugo. Features an exceptional reading experience with focus mode, keyboard shortcuts, and multiple themes.

## 🎯 Features

### Reading Experience
- **Focus Mode** (F key) - Complete UI removal for distraction-free reading
- **Keyboard Shortcuts** - T (TOC), S (Settings), F (Focus), Arrow keys (Navigation)
- **Reading Time** - Estimates on every chapter
- **Progress Tracking** - Percentage and chapter count
- **Position Memory** - LocalStorage remembers scroll position
- **Three Themes** - Light, Dark, Sepia
- **Smart Controls** - Auto-hide during reading

### Design
- **Libre Baskerville** - Warm, editorial serif for reading
- **Inter** - Clean sans-serif for UI
- **Terracotta Accent** - #c85a3a
- **Paper Background** - #fffef9 (warm, not stark white)
- **No Borders** - Depth through space and backgrounds
- **Dramatic Typography** - 11px to 96px scale

### Technical
- **Hugo** - Static site generator (v0.139.3)
- **Cloudflare Workers** - Deployment and CDN
- **Pagefind** - Client-side search (optional)
- **Minimal JavaScript** - ~15KB for all interactions
- **Mobile First** - Optimized for mobile reading
- **Performance** - <50KB initial load

## 📁 Project Structure

```
akshara/
├── assets/
│   └── css/
│       ├── base.css           # Variables, resets, typography
│       ├── components.css     # Reusable components
│       └── pages.css          # Page-specific styles
├── content/
│   ├── books/                 # Book content
│   ├── authors/               # Author pages
│   ├── collections/           # Collections
│   └── pages/                 # Static pages
├── layouts/
│   ├── _default/              # Default templates
│   ├── books/                 # Book templates
│   ├── chapters/              # Reading templates
│   ├── authors/               # Author templates
│   ├── collections/           # Collection templates
│   └── partials/              # Reusable components
├── static/
│   ├── js/                    # JavaScript files
│   ├── fonts/                 # Self-hosted fonts
│   ├── covers/                # Book covers
│   └── downloads/             # Downloadable files
├── src/
│   └── index.js               # Cloudflare Worker
├── scripts/
│   ├── build.sh               # Build script
│   └── deploy.sh              # Deployment script
├── hugo.toml                  # Hugo configuration
└── wrangler.toml              # Cloudflare Workers config
```

## 🚀 Quick Start

### Prerequisites
- Hugo Extended v0.139.3 or later
- Node.js (for Pagefind, optional)
- Wrangler CLI (for deployment)

### Installation

1. **Clone the repository:**
   ```bash
   cd Akshara
   ```

2. **Build the site:**
   ```bash
   hugo --gc --minify
   ```

3. **Start development server:**
   ```bash
   hugo server -D
   ```

4. **View the site:**
   Open http://localhost:1313

## 📚 Adding Content

### Adding a Book

1. Create book directory:
   ```bash
   hugo new books/your-book-name/_index.md
   ```

2. Edit the book metadata in `_index.md`:
   ```yaml
   ---
   title: "Book Title"
   author: "Author Name"
   year: 1927
   language: "English"
   pages: 454
   chapters: 164
   reading_time: "~8 hours"
   description: "Book description..."
   ---
   ```

3. Create chapters:
   ```bash
   mkdir -p content/books/your-book-name/chapters
   hugo new books/your-book-name/chapters/01-chapter-name.md
   ```

4. Edit chapter metadata:
   ```yaml
   ---
   title: "Chapter Title"
   chapter_number: 1
   reading_time: 8
   weight: 1
   next: "/books/your-book-name/chapters/02-next-chapter"
   ---
   ```

### Adding an Author

```bash
hugo new authors/author-name.md
```

Edit the author metadata:
```yaml
---
title: "Author Name"
birth_year: 1869
death_year: 1948
short_bio: "Brief biography..."
---
```

### Adding a Collection

```bash
hugo new collections/collection-name.md
```

Edit the collection metadata:
```yaml
---
title: "Collection Name"
description: "Brief description"
book_count: 42
---
```

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

## 🔧 Configuration

### Hugo Configuration (hugo.toml)

Key settings:
- `baseURL` - Your site URL
- `title` - Site title
- `params.featured_book` - Featured book on homepage
- Taxonomies for authors, collections, themes, periods, languages

### Cloudflare Workers (wrangler.toml)

Configure your deployment:
```toml
name = "akshara"
route = "akshara.dhwani.ink/*"
```

## 📦 Deployment

### Deploy to Cloudflare Workers

1. **Install Wrangler:**
   ```bash
   npm install -g wrangler
   ```

2. **Login to Cloudflare:**
   ```bash
   wrangler login
   ```

3. **Deploy:**
   ```bash
   ./scripts/deploy.sh
   ```

### Build Only

```bash
./scripts/build.sh
```

## ⌨️ Keyboard Shortcuts

On reading pages:
- **T** - Toggle table of contents
- **S** - Toggle settings/controls
- **F** - Toggle focus mode
- **←** - Previous chapter
- **→** - Next chapter
- **Esc** - Close all panels / exit focus mode

## 📖 Design Principles

1. **Warmth Over Coldness** - Paper tones, not stark white
2. **Character Through Typography** - Libre Baskerville + Inter
3. **No Borders** - Depth through backgrounds and white space
4. **Dramatic Scale** - 88px headlines to 11px labels
5. **Reading First** - Every decision serves the text
6. **Restrained Color** - Grayscale + single terracotta accent

## 🔍 Search (Optional)

To add search functionality:

1. **Install Pagefind:**
   ```bash
   npm install -D pagefind
   ```

2. **Build with search:**
   ```bash
   ./scripts/build.sh
   ```

## 📱 Mobile Optimization

The site is mobile-first with:
- Touch-optimized UI (44px tap targets)
- Responsive typography (19px on mobile)
- Progressive enhancement
- Minimal JavaScript
- Fast page loads

## 📊 Performance Targets

- **Initial Load:** <50KB HTML + CSS
- **JavaScript:** ~15KB total
- **Fonts:** WOFF2 with swap
- **Images:** Lazy loading
- **Lighthouse:** 95+ on all metrics

## 🤝 Contributing

To add new books or improve the design:

1. Fork the repository
2. Create a feature branch
3. Add content or make changes
4. Test locally with `hugo server`
5. Submit a pull request

## 📝 License

All texts are in the public domain. Digitization methodology documented per work.

## 🔗 Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
- [Build Guide](BUILD-GUIDE.md)
- [Libre Baskerville Font](https://fonts.google.com/specimen/Libre+Baskerville)
- [Inter Font](https://fonts.google.com/specimen/Inter)

## ✨ Vision

An archive that readers *want* to use. Not functional—exceptional. Every book deserves this level of care.

Built for Indian literary heritage.

---

**Ready to build?** Run `hugo server` and open http://localhost:1313
