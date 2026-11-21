# Akshara: the visual grammar

The rulebook for how Akshara looks and behaves: for this site, for future sessions working on it, and for
the sister projects (living books, a review) that will share its look. It is the source of truth for
design (DECISIONS.md, D16). Where it and the site disagree, one of them is a bug: fix whichever is wrong in
the same change.

**Values live in the stylesheet, not here.** Every colour, size and space is a CSS custom property in
`assets/css/plate.css` (the `:root` block and the eight shelf classes). This document names those tokens
and says when to use them; it does not repeat their values, so the two cannot drift apart. To change a
value, change the token.

The design is "The Plate", approved by Bhuvanesh on 2026-11-21 after seventeen rounds of refinement. The
approved mock is `../design_directions/2026-11-redesign/plate.html`; the brief it answered is `BRIEF.md`
beside it.

> Status: first draft, written with milestone 1 (tokens, header, footer, home). Sections marked
> *(to be confirmed)* describe approved decisions that are not yet built; they are checked against the
> built pages before the redesign is merged.

---

## 1. Principles

Akshara is a library of rare books about India, read on phones first. It should feel **refined, quiet and
alive**: a fine-press series, not a blog; a museum's calm, not a startup's energy.

1. **The books' own material carries the design.** The engravings, maps, seals and frontispieces printed in
   these books are the most beautiful things the project has, and nobody else has them. Show them large.
2. **One rule applied without exception.** A series is recognisable from across a room because every cover
   obeys the same system. Strict enough to hold five hundred books.
3. **Every device is something a real book, press or library does.** Plate numbers, marginal notes, folios,
   colophons, printer's devices, shelf marks. Decoration that means nothing is not allowed.
4. **The reading page is the product.** Care where a reader never consciously notices: measure, spacing,
   real quotation marks, the opening of a chapter.
5. **Show the material, do not describe it.** Short, exact prose. Captions written like a gallery label.

### Banned (from the brief)
The look AI tools produce by default, and the clichés of the "tasteful" web. Never:
- warm cream paper with a serif and a terracotta accent; near-black with one acid accent;
- purple-blue gradients; glassy cards; rounded cards with shadows in a grid;
- emoji or icon markers;
- everything centred;
- numbered "01 / 02 / 03" sections that are not a real sequence;
- tiny tracked capital eyebrows over every heading;
- pill buttons;
- scroll-triggered fade-ins;
- placeholder copy or stock images: every word and picture comes from the real books.

Bhuvanesh has also rejected: saturated colour bands, many small spaced capitals, and timidity that reads
like a personal blog.

---

## 2. Colour

### Paper and ink
| Token | Use |
|---|---|
| `--paper` | The page. Pure white (D11). Never tinted site-wide. |
| `--ink` | Text and anything that must read first. |
| `--ink-2` | Secondary text: descriptions, captions, inactive navigation. |
| `--ink-3` | Tertiary: dates in captions, notes on notes, placeholders. |
| `--hair` | Every hairline rule. One weight: 1px. |
| `--well`, `--well-edge` | The search field's tinted well, the only filled form control. |
| `--on-k` | Text set on a block of shelf ink (the Begin reading button). |
| `--shadow` | The RGB of the shadow under covers, used inside `rgba()`. |

### The eight shelves
Each shelf has a cloth colour (`cloth` in `data/shelves.toml`), from which come two tokens, set by the
shelf's class (`code` in `data/shelves.toml`):

| Class | Shelf |
|---|---|
| `.le` | Literature and Letters |
| `.vi` | Village and Society |
| `.co` | Travel and Chronicles |
| `.cl` | Classical and Philology |
| `.ma` | Maritime and Company Records |
| `.ec` | Political Economy |
| `.su` | Surveys and Gazetteers |
| `.cu` | Currency and Finance |

- `--g`, **the ground**: the cloth washed very pale. Covers, plate tiles, the turning plate's stage, the
  book page's head band.
- `--k`, **the ink**: the cloth deepened until it reads as text on white and on its own ground. Plates
  (printed through their mask), shelf names, the Begin reading button, a book's series line, rules in a
  shelf's section.

Put the shelf class on the element that owns the colour (a cover, a section, a tile); everything inside
inherits `--g` and `--k`. Never write a shelf's colour as a raw value.

### Where colour may appear
- **May:** covers; plate tiles and plates; the turning plate; the featured edition's band (its `--g`
  mixed half-way to paper); the book page's head; a shelf's name and its rule; the one solid button;
  link underlines (the ink at 40%, so a link is a word with a coloured hairline, never coloured text).
- **May not:** the header, the footer (the device prints in a neutral grey), body text, large flat bands
  of saturated colour, gradients, or more than one shelf's colour behind any one block.

### Dark mode *(to be confirmed in milestone 4)*
The site follows the reader's device. The plan: `--paper` becomes a deep neutral, the inks lighten, each
shelf's `--g` darkens to a ground a step above the paper and its `--k` lifts toward the light ink so plates
still read. Defined by redefining the same tokens under `prefers-color-scheme: dark` and under the reading
room's Night paper; no component writes its own dark colours.

---

## 3. Type

### Faces
- **Newsreader** for every word (D12), self-hosted, variable weight 200–800 and optical size 6–72.
  `font-optical-sizing: auto` lets one family serve 84px headlines and 19px reading text.
- **Noto Serif Kannada**, weight 500, only for the mark ಅಕ್ಷರ (`--kn`, class `.kn`).
- No sans-serif anywhere. No third-party font hosts.

### The scale
Use the role tokens; do not invent sizes.

| Token | Role |
|---|---|
| `--fs-display` | The opening headline. Weight 300, tight leading, negative tracking. |
| `--fs-title` | A page's title (Library, an author, a book's short title). Weight 300. |
| `--fs-feature` | A featured title inside a section. Weight 300. |
| `--fs-quote` | A book's own words set large: weight 300, italic, in the shelf's ink. |
| `--fs-h1` | A heading inside prose. |
| `--fs-h2` | Section headings (`.sec-h`). Weight 400. |
| `--fs-h3` | Shelf names, sub-headings. |
| `--fs-h4` | Small headings: steps, the way on at a chapter's end. |
| `--fs-read`, `--fs-read-wide` | Reading text: phone, then wider screens. |
| `--fs-body` | The site's body text. |
| `--fs-lede` | The sentence under a page or section title, in `--ink-2`. |
| `--fs-ui` | Navigation, captions under covers. |
| `--fs-aside` | Asides beside headings, the line under a button. |
| `--fs-note` | Marginal notes, counts, small italic labels. |
| `--fs-caption`, `--fs-tiny` | Plate captions; captions under small tiles. |
| `--fs-mark`, `--fs-mark-kn` | The mark (two scripts sized to read as one name). |

Covers size their type from the cover's own width (container units, `cqi`), so a cover reads the same at
any size.

### Rules
- **Measure:** `--measure` for any running text (about 65 characters). Never wider.
- **Weights:** 300 for display sizes, 400 for everything else. No bold in the interface; emphasis is italic.
- **Italic** is the house's second voice: asides, labels, captions, the second line of a title, a book's
  own words. Titles of books are always italic in running text.
- **Small capitals** only at a chapter's opening line. Newsreader has none, so the browser draws them from
  capitals (D12). Never small or spaced capitals as labels or eyebrows.
- **Figures:** the reading text asks for old-style figures (`oldstyle-nums`); Newsreader draws lining ones,
  and that is accepted (D12). Tables and page numbers use tabular figures.
- **Punctuation:** real quotation marks and apostrophes (’ “ ”), en dashes for ranges (1642–1645), a
  middle dot with spaces to join facts (Francis Buchanan · London, 1807).
- **Headlines** use `text-wrap: balance`; paragraphs `text-wrap: pretty`.

---

## 4. Space and layout

- **Gutters:** `--gut` and `--gut-r`, wider from 760px, never less than the phone's safe area.
- **Column:** `.wrap` holds content to 1240px with the gutters. Reading text holds to `--measure`.
- **Section rhythm:** `--sec` between sections (grows on wide screens); `--sec-end` before the footer.
  Inside components, spacing is set on the component and is not a token: keep it to the steps already
  used (4, 6, 8, 10, 12, 14, 18, 22, 26, 34, 40px) rather than adding new ones.
- **Breakpoint:** one, at 760px (written in the media query; CSS cannot put it in a token). Below it the
  phone composition, above it the wide one. Design phone first; the wide layout is an expansion.
- **Grids:** covers two to a row on a phone, four (or six in shelf rows) on a wide screen; plate tiles two,
  then four.

### Phone rules (every page)
1. The first screen says what the page is and offers the next step (on a book's page, Begin reading is
   on the first screen).
2. Every tap target is at least 44px tall: navigation, footer links, buttons, list rows.
3. Nothing scrolls sideways except the deliberate shelf rows and plate strips, which snap.
4. Images are sized for the screen they are on.

---

## 5. The plate

A plate is a picture from a book's own pages, cleaned so it prints in one ink.

### Processing (the mask recipe)
1. Crop tight to the picture: no caption, page number or printed frame (unless the frame belongs to a
   device).
2. Grayscale, auto-level, then level so the paper goes to pure white and the line to black.
3. Negate, and use the result as the alpha channel of solid black: black on transparent, WebP.
4. Photographs and halftone frontispieces first get an ordered-dither (Bayer) halftone, so they read as a
   fine screen of dots, as a printed halftone does.
5. Long side about 1000–1600px for line, 700–900px for halftones.

`uv run scripts/make_plates.py` does this from `data/plate_sources.toml`, which records each plate's
book, source page and crop (and, where needed, levels, a colour channel that drops a library stamp, boxes
painted out as paper, or a rotation). Plates made earlier are recorded in `data/plates.toml`. Every plate's
book must be recorded in one of the two: the cover check refuses a plate it cannot trace.

### Printing
A plate is never shown as an image. It is an element with class `.plate` and `--src:url(...)`: the file is
the mask and `--k` shows through it, so one file prints in any shelf's ink and in dark mode. Plates sit on
their shelf's `--g`.

### Cropping and placing
- In a tile, a plate is inset so it never touches the tile's edge.
- On a cover, an engraving may run off the edge (it is printed large); a map never does.
- On the turning plate, the engraving bleeds off the right edge of its stage.

### Captions
Like a label in a gallery: the plate's name (italic if it is a scientific or foreign name), then where it
was printed: *Plate xx, fig. 51 · Buchanan, A Journey from Madras, 1807*. See §9.

---

## 6. Covers

Every book has a cover drawn from its data (`layouts/_partials/book/cover.html`): its shelf's ground and
ink, a label at the top (the short title, and an italic second line for a volume or the years covered),
a foot line (Akshara No. and the year), and in the middle whatever the book itself offers.

### The five kinds
| Kind | Class | What it shows | Placement |
|---|---|---|---|
| Engraving | `k-plate` | the book's own engravings, woodcuts or drawings | printed large, may run off the edge |
| Map | `k-map` | a map bound into the book | kept whole inside a fine rule |
| Device | `k-device` | arms, a seal or a printer's device from the title page | small and centred, as the printer placed it |
| Photograph | `k-portrait` / `k-photo` | a frontispiece portrait or photograph, as halftone | an oval for a portrait, a ruled frame otherwise |
| Type only | `k-type` | nothing: the title alone | title set larger and lower, under one rule, author above |

### The rule that is never broken
**A cover's picture comes from that same book.** Never another book, another volume or another edition. If
the book has no usable picture, it is type only, and the reason is written in `data/covers.toml` (`why`).
Type only is a full member of the series, not a placeholder.

### Choosing a book's kind
Look through the book's own scan in this order: engraved plates or woodcuts → maps → the title-page device
→ a frontispiece portrait or photograph. Take the first that will read at 200px wide. Prefer a picture
that says what the book is about over one that is merely decorative.

### Crop
Each kind has a default placement. When a picture's shape does not suit it, set `inset` (CSS inset: top,
right, bottom, left) for that book in `data/covers.toml`. Keep the label and the foot line clear.

### Adding a new book's cover
1. Find its picture in its own scan (above), or decide it is type only.
2. Add the source and crop to `data/plate_sources.toml` and run `uv run scripts/make_plates.py`.
3. Add the book to `data/covers.toml`: `kind`, `plate`, and `inset` or `line` if needed; or
   `kind = "type"` with `why`.
4. Run `./verify`. `scripts/check_covers.py` stops it if a book has no cover, a kind is unknown, a plate file
   is missing, a plate is recorded for another book, or a type-only cover does not say why.

### Title lines
The label's first line is the short title (`cover_title` in `data/bookdetails.toml`, or the title). A
trailing ", Vol. II" becomes an italic second line "Volume II"; trailing years ("1642–1645") and a short
subtitle after a colon do the same. A title is never broken inside a word: one with a word of eleven
letters or more steps its type down (`.lw`), and one over forty characters steps down again (`.long`);
on a pictured cover a long title moves the picture down to keep clear of it. Hyphenated names do not break
at the hyphen. Straight apostrophes from the records are set as ’.

---

## 7. Components

Each is a class in `plate.css`; the comment above it says what it is for.

- **Header (`.hd`).** A masthead with one hairline beneath, slightly translucent paper, sticky. Wide:
  Library, Plates, Authors · the mark · Journal, About, Search. Phone: the mark left; Library and Search
  right. The mark always prints its Kannada in the Surveys shelf's ink. No colour band. (D13)
- **Footer (`.ft`).** A colophon, centred: the printer's device in neutral grey, ಅಕ್ಷರ Akshara, its gloss,
  one sentence, the ways back in on one line, a last line with Bhuvan elsewhere. (D14)
- **Buttons and links.** One solid button style (`.cta`, `.cta-solo`): a block of the shelf's ink, square
  corners, an arrow that moves 3px on hover. One outlined (`.readon`) for a second way in. Everything else
  is a link: a word with a hairline in the shelf's ink beneath (`.ln`, `.quiet a`). No pills, no icons
  except the search glass.
- **Section heading (`.sec-h`).** The name at `--fs-h2`, a quiet italic aside on the right (often a link),
  one hairline beneath. Inside a shelf-coloured band, `.voice-h` does the same in the shelf's ink.
- **Featured edition (`.feature`).** A band of the shelf's ground mixed half-way to paper: the cover, the
  full title, the author line, the book's own first sentence set large, a description, two ways in, then
  three of its plates on one rule.
- **Plate tiles (`.smalls`, `.feat-plates`).** A plate inset on its shelf's ground; the caption beneath,
  name first. The ground deepens a little under the pointer.
- **The eight shelves (`.sh`).** The shelf's name in its ink, its count and years, its epigraph in italic
  with the source beneath, and one cover from the shelf beside it.
- **Search field (`.findbox`).** The one filled form control: a tinted well (`--well`), a glass, at least
  58px tall, an italic placeholder that says what can be searched. It turns to paper with an ink edge when
  in use. Under it, one italic line saying what it searches. It is a real form, so it works with no script.
- **Arrangement switch (`.views`).** Plain words on one hairline, the chosen one in ink with a 2px rule
  under it, like a running head; a count in italic at the right. Never tabs, pills or a dropdown.
- **Shelf row (`.row`, `.row-h`).** The group's name in the shelf's ink over a 1px rule in that ink, its
  count in italic at the right; then its covers, face out. On a phone a row to swipe, each cover snapping
  to the gutter, the next one showing at the edge to say there is more; on a wide screen a grid of six.
  Rows that are not one shelf's (decades, letters) use the neutral ink.
- **Cover with caption (`.book`, `.cap`).** The cover, then the short title in ink and the author and year
  in `--ink-2`. The whole is one link.
- **Search results (`.hit-list`).** Rows on hairlines: the chapter's name, the book in italic, an excerpt
  with the found words underlined in the shelf's ink (`mark`). Built as text, never as HTML.
- **Shelf band (`.band`).** A page that belongs to one shelf opens on the shelf's ground: the way up in
  italic, the name in the shelf's ink, its epigraph, its count.
- **Lists of pages (`.rows`, `.au`).** One row per entry on hairlines; titles of books in italic with a
  hairline beneath in the shelf's ink.
- **The book head, the chapter opener, marginal notes, folios, chapter end.** *(to be written with
  milestone 3)*

---

## 8. Motion

- **The turning plate:** a crossfade between engravings every 6.5 seconds over 1.4 seconds; the stage's
  ground and caption colour change with it. It pauses while the tab is hidden.
- **Hover lift:** a cover rises 3px and its shadow deepens; a tile's ground deepens; a button's arrow moves.
- **Reduced motion:** if the reader's device asks for less motion, nothing moves on its own and nothing
  lifts. The page must make sense with no motion at all.
- Never: scroll-triggered reveals, parallax, animated entrances.

---

## 9. Writing

- **Voice:** plain, exact, warm. Sentences, not slogans. The house writes "Begin reading", "The library",
  "Small things from the books".
- **Sentence case** for every heading and label. No capitals for emphasis.
- **Numbers in running text** are words (sixty-three books); in data, labels and captions, figures.
- **Asides** are italic and short: "The library", "All 24 plates", "Akshara No. 19".
- **Crediting a plate:** name first, then detail, then the book: *Name* · Plate or fig. · Author's surname,
  *Short title*, year, volume, page. The plate always links to the book it came from.
- Every word on a page comes from the books, their records, or the editor; nothing is placeholder.

---

## 10. Do and don't

| Do | Don't |
|---|---|
| Print a plate through its mask in the shelf's ink | Show the scan as a photo with its yellow paper |
| A type-only cover when the book has no picture | Borrow a picture from another book or volume |
| One hairline under a heading | A box, a card shadow, or a coloured band |
| Italic for an aside | Small spaced capitals as an eyebrow |
| "Begin reading →" in the shelf's ink, square | A rounded pill button |
| A link as a word with a coloured hairline | Blue underlined links, or coloured link text |
| Sizes from the `--fs-` tokens | A new pixel size for one heading |
| A count in words in a sentence | "63 BOOKS" in tracked capitals |

---

## 11. Adding to the grammar

- **A new component** reuses the tokens, the hairline, italic for its quiet voice, and a shelf's `--g`/`--k`
  if it belongs to one book or shelf. Add it to §7 with what it is for and why it looks so, in the same
  change that ships it.
- **A new token** only when a role is genuinely new, named for its role (`--fs-…`), added to `:root` with a
  comment, and listed here.
- **A new shelf** gets a class with `--g` and `--k` derived from its cloth like the others (ground washed
  very pale; ink deep enough to read on white and on its ground), and a `code` in `data/shelves.toml`.
- **A sister project** (living books, a review) takes `plate.css`'s tokens and type as they are and adds
  its own components on top. It may choose its own cloth colours as new shelf classes; it keeps white
  paper, Newsreader, the plate, the hairline and the banned list. If it needs to break a rule here, change
  the rule here first, with a DECISIONS entry, so the family stays one family.
