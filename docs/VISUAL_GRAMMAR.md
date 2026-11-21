# Akshara: the visual grammar

The rulebook for how Akshara looks and behaves: for this site, for future sessions working on it, and for
the sister projects (living books, a review) that will share its look. It is the source of truth for
design (DECISIONS.md, D16). Where it and the site disagree, one of them is a bug: fix whichever is wrong in
the same change.

**Values live in the stylesheet, not here.** Every colour, size and space is a CSS custom property in
`assets/css/plate.css` (the `:root` block); the shelves' colours are in `data/shelves.toml`, from which the
build writes the eight shelf classes. This document names those tokens
and says when to use them; it does not repeat their values, so the two cannot drift apart. To change a
value, change the token.

The design is "The Plate", approved by Bhuvanesh on 2026-11-21 after seventeen rounds of refinement. The
approved mock is `../design_directions/2026-11-redesign/plate.html`; the brief it answered is `BRIEF.md`
beside it.

> Status: complete for the redesign (milestones 1–4, 2026-11-21). Checked against the built pages before the
> redesign is merged; any later design change updates this document in the same change.

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

### Dark mode
Under `html[data-theme="dark"]` (set by `assets/js/paper.js` from the device's setting or the reader's
chosen paper, D22) the same tokens are redefined: `--paper` becomes a deep neutral, the inks lighten, each
shelf's `--g` darkens to a ground a step above the paper and its `--k` lifts toward the light (every shelf
ink at least 5.5:1 on its ground). A component never writes dark colours of its own; the only dark-specific
rules are: the solid Begin reading block becomes a deep tint of the ink (a slab of light ink shouts on dark
paper), photographs of pages are dimmed a little, the books' own figures in the text are inverted to
print light on dark, and photographs and portraits (cover kinds `portrait` and `photo`, and plates marked
`face = true` in `data/plates.toml`) print as on paper, dark ink on a pale tile, because a face printed
light on dark becomes a negative. Cotton (`html[data-paper="cotton"]`) is a warm light paper for readers who ask for it.

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
- **Small capitals** only at a chapter's opening line, and for the book's own headings that it printed in
  capitals (set in small capitals so they do not shout). Newsreader has none, so the browser draws them from
  capitals (D12). Never small or spaced capitals as labels or eyebrows.
- **Capitals in titles.** A chapter or book title printed in capitals is set in title case; so is a run of
  capitalised words inside a mixed title. The printer's capitals on a chapter's first words are set in lower
  case where they are quoted.
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

### Sizes
Always take a plate's address from `partial "plate/url.html" (dict "key" … "w" …)`, with `w` the widest it
will be drawn at twice its CSS size: covers in grids 440, a book's own cover 800, tiles 600–640, a headpiece
700, the turning plate 960, the footer device 200. The build makes the copy (never larger than the
original, and never heavier: the hand-made file is kept when the copy would weigh more). A plate in a
section below the first screen is fetched only as the reader nears it (`content-visibility: auto`, D23).

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
on a pictured cover a long title moves the picture down to keep clear of it (`.t-long`; and `.t-mid` for a
title over 28 letters on a portrait, map or device, where the portrait's title also steps down a size). Hyphenated names do not break
at the hyphen. Straight apostrophes from the records are set as ’.

---

## 7. Components

Each is a class in `plate.css`; the comment above it says what it is for.

- **Header (`.hd`).** A masthead with one hairline beneath. It scrolls away with the page; only a chapter's
  reading bar stays to hand (it hides going down and returns going up). Wide:
  Library, Plates, Authors · the mark · Journal, About, Search. Phone: the mark left; Library and Search
  right. The mark always prints its Kannada in the Surveys shelf's ink. No colour band. (D13)
- **Footer (`.ft`).** A colophon, centred: the printer's device in neutral grey, ಅಕ್ಷರ Akshara, its gloss,
  one sentence, the ways back in on one line, a last line with Bhuvan elsewhere. (D14)
- **Buttons and links.** One solid button style (`.cta`, `.cta-solo`): a block of the shelf's ink, square
  corners, an arrow that moves 3px on hover. One outlined (`.readon`) for a second way in. Everything else
  is a link: a word with a hairline in the shelf's ink beneath (`.ln`, `.quiet a`). No pills, no icons
  except the search glass.
- **Section heading (`.sec-h`).** The name at `--fs-h2`, a quiet italic aside on the right (often a link),
  one hairline beneath. When the two do not fit on one line the aside goes beneath the name, never leaving a
  word of the heading alone. Inside a shelf-coloured band, `.voice-h` does the same in the shelf's ink.
- **Featured edition (`.feature`).** A band of the shelf's ground mixed half-way to paper: the cover, the
  full title, the author line, the book's own first sentence set large, a description, two ways in, then
  three of its plates on one rule.
- **Plate tiles (`.smalls`, `.feat-plates`).** A plate inset on its shelf's ground; the caption beneath,
  name first. The ground deepens a little under the pointer.
- **The eight shelves (`.sh`).** Each a small bookcase: four of its own books (those with pictures first)
  standing face out against a case a shade deeper than their covers (its paper with a sixth of its ink), on
  a 2px shelf-line in its ink; beneath, its name in its ink with
  the count and years, its epigraph in italic and the source. The books stay still on hover; the shelf's name underlines.
- **How a book is made (`.made`).** A band of the paper of the shelf the example comes from. The
  photographed page and the set table side by side as equals, each on white paper with a fine edge and
  named above itself ("As photographed", "As set"); then the four steps, each under a large light numeral
  in the shelf's ink, because they are a real sequence.
- **Search field (`.findbox`).** A line to write on: white paper, one rule in `--ink-2` beneath that
  becomes 2px of `--ink` while in use, the glass at the left, the placeholder in large light italic saying
  what can be searched, the typed words upright. A "Clear" in italic appears once something is written. It
  is a real form (with a reset button), so it works with no script. Under it, one italic line saying what
  it searches. No filled box, no rounded corners.
- **Arrangement switch (`.views`).** Plain words on one hairline, the chosen one in ink with a 2px rule
  under it, like a running head; a count in italic at the right. Never tabs, pills or a dropdown.
- **Shelf row (`.row`, `.row-h`).** The group's name in the shelf's ink over a 1px rule in that ink, its
  count in italic at the right; then its covers, face out. On a phone a row to swipe, each cover snapping
  to the gutter, the next one showing at the edge to say there is more; on a wide screen a grid of six.
  Rows that are not one shelf's (decades, letters) use the neutral ink.
- **Cover with caption (`.book`, `.cap`).** The cover, then a quiet caption: the short title at `--fs-aside`,
  never more than three lines, then the author in italic at `--fs-caption`. The year and number are already
  on the cover, so the caption does not repeat them. The whole is one link; the title takes the shelf's ink
  on hover.
- **Search results (`.hit`).** Grouped by book, in the order the books first appear: the book's cover small
  at the left (drawn from what the search index records: shelf, kind, plate), its title in italic in its
  shelf's ink with author and year beneath, then each place where the words occur, set in from a fine rule in
  the shelf's ink: the chapter's name, then an excerpt between ellipses, held to a reading width, the found
  words marked with a soft band of the shelf's ink under their lower half (`mark`). Built as text, never as
  HTML.
- **A way further on (`.more`).** A link that stands alone after a list ("Every result, on the search
  page"): the shelf's ink, an arrow that moves 3px on hover, underlined only on hover.
- **Shelf band (`.band`).** A page that belongs to one shelf opens on the shelf's ground: the way up in
  italic, the name in the shelf's ink, its epigraph, its count.
- **Lists of pages (`.rows`).** One row per entry on hairlines; titles of books in italic. A list that follows
  a section heading shares the heading's rule and draws none of its own. The journal's earlier essays set the
  date in its own column on a wide screen, like a register.
- **The authors index (`.index`, `.ix`).** Filed by surname under a large light letter in the margin, as a
  printed index is, with a row of letters at the top to jump to. Each writer: the name, years and
  birthplace in italic, one line on who they were (the record's `short_bio`; the pipeline's placeholder is
  left out), then their own books, each a small cover (its picture and paper only) beside its title.
- **The book head (`.bk-head`).** One full-width band in the shelf's paper: the cover (paler than the band),
  then in reading order the series line in italic in the shelf's ink, the short title at display weight with
  any volume in italic, the rest of the title in light italic, the author (a link) with place and year in
  the shelf's ink, the Begin reading block naming the first chapter, the downloads as one sentence, the
  description, and the book's measure as light figures on one hairline. On a phone the cover is small and
  centred and Begin reading comes before the description, so it is on the first screen.
- **How it begins (`.opening`).** The book's own first sentence (from its first real chapter, forty-five words at
  most) set as an epigraph: light italic in the text's ink, one large quotation mark hung in the margin in the
  shelf's ink, the source beneath after a dash. Printed capitals on the first words are set in lower case.
- **Contents (`.toc`).** As a printed contents page, held to a reading width: the preliminaries as quiet rows
  first, then one row a chapter with its numeral in lower-case roman italic in the shelf's ink, each title led
  by dots to the page it was printed on; the back matter quieter after. Every row at least 44px tall.
- **Tables (`table.ledger`, `.ledger-table`).** Set as a printer's ledger: a 2px rule in the shelf's ink above,
  1px below, faint rules between rows, figures in tabular lining numerals aligned right, headings in italic in
  the shelf's ink. On a book's page the table sits on a panel of the shelf's paper, named by its page; its data
  (as printed, tidy) is offered on one line beneath.
- **This edition (`.edition`).** How far it has been checked, with the way to proofread; then two matching
  columns, "Take it away" (every form) and "The record" (published, pages, scan, shelf, licence), each under a
  small italic head on one hairline; then the editor's note with its full record folded.
- **The reading bar (`.rd-bar`).** Replaces the masthead on a chapter: ಅ and the short title in italic
  (back to the book), then Contents, Aa, Focus. A 2px line in the shelf's ink fills beneath as the chapter
  is read. It slides away going down the page and returns on the first move up.
- **The chapter opener (`.opener`).** Centred over the column: the headpiece (one of the book's own
  engravings in its ink, or the house mark), the chapter's number in italic in the shelf's ink, the title
  in light display type, one line of where it comes from, then a 40px rule.
- **The text (`.text`).** `--fs-read`, `--fs-read-wide` times the reader's size; `--measure`; indented
  paragraphs; small capitals on the first line only; the book's own small capitals (`.sc`) kept.
- **Side-headings (`.sec-h3`).** The book's own headings within a chapter: the text's size, italic in the
  shelf's ink, closer to the paragraph they head than to the one before. Headings the book printed in capitals
  are set in small capitals.
- **Marginal notes (`.sidenote-stack`).** The author's shoulder notes, italic, `--fs-note`, in the shelf's
  ink: right-aligned in the left margin on a wide screen, above their paragraph on a phone.
- **Folios (`.folio-trigger`).** The printed page numbers, small italic figures in `--ink-3` in the right
  margin (at the very edge on a phone), each opening the scan of that page; the shelf's ink on hover.
- **Chapter end (`.chap-end`).** A 40px rule, "End of chapter I" in italic, then the next chapter as one block
  on the shelf's paper ("Turn to chapter II", its name large, an arrow that moves), then the other ways out on
  one quiet centred line: the previous chapter, the book's contents, correcting a misreading.
- **The panel (`.rpanel`) and the scan leaf (`.leaf`).** Slide in from the right. Settings are words, A's
  and small sheets of paper, never boxes; the chosen one is in full ink with a 2px rule in the shelf's ink.

- **No page here (`.lost`).** The Periplus ship on its shelf's paper, the title, a line to search on, two
  ways back. On a phone the words come first.
- **Print.** A printed page keeps the text, its marginal notes and page numbers, in black on white; bars,
  panels, footers and navigation are left off.

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
- **A new shelf** is one entry in `data/shelves.toml`: its `code`, and four colours derived from its cloth
  like the others: `paper` (washed very pale), `ink` (deep enough to read on white and on its paper),
  `paper_dark` and `ink_dark` (at least 5.5:1 on its dark paper). The build writes its class
  (`assets/css/shelves.css`) and the social cards use the same values; nothing else needs touching.
- **A sister project** (living books, a review) takes `plate.css`'s tokens and type as they are and adds
  its own components on top. It may choose its own cloth colours as new shelf classes; it keeps white
  paper, Newsreader, the plate, the hairline and the banned list. If it needs to break a rule here, change
  the rule here first, with a DECISIONS entry, so the family stays one family.
