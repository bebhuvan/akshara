# Review 0003: pre-launch, the Plate redesign (`0f41df2..3c96224`, and `origin/main...design/plate` as a whole)

Reviewed up to: 3c96224
Reviewer model: Claude Opus 5.5 (claude-opus-5-5), fresh subagent, not the author
Gates: `./verify` passed with Hugo 0.170.0 (scratchpad build, first on PATH): every cover's picture checked;
build; Pagefind indexed 1178 pages / 159,878 words; "Checked 1427 known addresses and 190 redirects. Every
known address works."; "Checked 1250 pages for unsafe or broken markup. No unsafe or broken markup."; 6804
files (limit 20000), 379 redirects (limit 2000); 38 unit tests OK; Python compiles; `npm audit` 0
vulnerabilities. `verify` still has no lint or format check (carried over from reviews 0001 and 0002).

Extra checks run: the built site served locally twice, once plain and once with the exact
`Content-Security-Policy` from `static/_headers` added to every response, and checked in a browser for CSP
errors (home, a book page, a chapter, library search, a "one page" download); horizontal-scroll audit at 320px
on twelve page types (no page scrolls sideways; only the intended shelf and plate strips run past the edge);
screenshots of the home page, a book page's "How this text was read" and a chapter at 320px; a contrast audit
of the new reading section in light and dark mode; tap-target sizes for the new links at 320px; Pagefind
queried directly ("Banerji", "Toru Dutt", "Foster"); every book's record compared with what its page says
about how it was read; the 47 non-Stage-One books compared with the proofreading desk's catalogue in
`../akshara_proofing/public/data/catalog.json` (all 47 present, every page seeded, so "every page of this book
is on the proofreading desk" holds, provided the deployed desk matches that catalogue, which I could not check).

## In plain words

The site is in good shape to go public: every old address still works, nothing scrolls sideways on a small
phone, search results are built safely as text, and no page breaks the security policy. Three things should
be fixed before launch. **The "one page" edition of all 47 books is unstyled when opened on akshara.ink**,
because the security policy tightened for review 0002 now blocks the style sheet inside those files.
**The new "How this text was read" section says more than the records support**: it tells every reader that
the text was "checked against the scans" and that "what errors remain are few and small", on pages whose own
record says no page was re-read against the scan and the checks scored 75 or 80. And **search now matches the
author's name and the book's title in every chapter**, so searching "Foster" returns 411 pages, almost all of
them his own volumes, drowning the places where he is actually mentioned. Below those are smaller wording,
documentation and test issues.

## Findings

### 1. [high] The "one page" HTML edition of every book renders without its styles on the live site
- Where: `static/_headers:13` (`style-src-elem 'self'`, added in 0f41df2 to answer review 0002 finding on
  inline styles); the files are `public/downloads/<book>/<book>.html` (47 of them), linked from every book page
  as "one page" (`layouts/books/book.html:64`, `:167`).
- Failure: each of those files carries its styles in a `<style>` element. With the policy as written, the browser
  refuses it ("Applying inline style violates ... 'style-src-elem 'self''" in the console, confirmed locally with
  the real header). A reader who clicks "One page — the whole book as one web page" gets browser-default Times,
  full-width headings and images wider than a phone screen. This was not visible in `./verify` because nothing
  serves the build with its headers.
- Rule: D4/D25 (the policy must not break the site's own pages); global standard, "it does what was asked".
- Fix: all 47 files share one identical style block (sha256 `BhZHOuPKomo/9dw1d2sZ3beCkwmqPd+WWX7nNgWi4ls=`).
  Either add `'sha256-BhZHOuPKomo/9dw1d2sZ3beCkwmqPd+WWX7nNgWi4ls='` to `style-src-elem` and add a check to
  `scripts/check_content.py` that every `<style>` in `public/` hashes to an allowed value (so a pipeline change
  fails `verify` instead of silently unstyling the downloads), or have the pipeline write that CSS to a file
  next to the HTML. Do not try to loosen it with a second `/downloads/*` rule: Cloudflare joins repeated headers,
  and two CSPs are both enforced. (If a separate policy is wanted there, the rule must first detach the header with
  `! Content-Security-Policy`.)
- Resolution: Fixed. The pipeline's one style block is allowed by its fingerprint in `static/_headers`; new `scripts/check_styles.py` (run by `verify`) fails if any built page has a `<style>` the policy would refuse; tests in `tests/test_checks.py` (`InlineStyles`).

### 2. [high] "How this text was read" claims scan-checking and few, small errors for every book, against the books' own records
- Where: `layouts/_partials/book/reading.html:12` (the non-Stage-One `rd-lede`), shown on all 47 machine-checked
  and community books.
- Failure: every such page says the text was "then checked against the scans by Akshara's own tools", "far
  cleaner than ordinary OCR", and "What errors remain are few and small, and they do not spoil the reading."
  The records say otherwise for several books, and the page prints both side by side:
  - `palas-of-bengal`: score 80.2; provenance "Automated reading (38 open review items); 0 of 105 pages had
    flagged passages re-read against the scan".
  - `indian-famines-causes-prevention-dutt-1901`, `economics-in-india-inaugural-lecture-jevons-1915`,
    `guide-to-india-office-records-1919`: also "0 of N pages ... re-read against the scan".
  - `journey-from-madras-vol-ii`: score 75; 26 columns that do not add up, 10 unclear passages, 39 open review
    items; 22 of 584 pages had flagged passages re-read.
  Across all 47, the most any record says is that flagged passages on some pages were re-read; none says the
  text as a whole was checked against the scans. "Far cleaner than ordinary OCR" is not measured anywhere in the
  records. A careful reader (or a scholar quoting the edition) who reads the lede, then the provenance line
  beneath it, sees the library contradict itself on the page meant to be its most honest.
- Rule: D28 ("the score is shown with its limit stated beside it ... because a bare number would claim more than
  the checks measure"); the brief's own focus on true public wording; review 0002's footer finding was the same
  kind of overclaim.
- Fix: make the lede say only what is true of every book, and let the record say the rest. For example: "read
  from photographs of its pages by a vision-language model ... then run through Akshara's automatic checks, which
  flag passages to be re-read against the scan." Drop "few and small" and "do not spoil the reading", or show it
  only above a score threshold the owner chooses. Drop or source "far cleaner than ordinary OCR". Add a test that
  the lede does not say "checked against the scans" when `reread_pages` is 0.
- Resolution: Fixed. The lede now says the text was run through the automatic checks, which flag passages to be re-read, never that it was checked against the scans. "Few and small" is said only at a score of 95 or more; below 90 the page says the checks flagged more than usual (D30). "Far cleaner than ordinary OCR" is kept as the owner's statement about the method, not a claim about each book. Test: `HowTheTextWasRead.test_the_account_claims_no_more_than_the_record`.

### 3. [medium] Search matches every chapter on its book's title and author, burying real mentions
- Where: `layouts/_partials/book/search-meta.html:5-6`, included inside `data-pagefind-body` on every book page
  (`layouts/books/book.html:48`) and every chapter (`layouts/chapters/page.html:120`).
- Failure: the hidden `<span data-pagefind-meta="book">` and the new `<span data-pagefind-meta="author">` are
  inside the indexed body, so Pagefind indexes their text as words of every chapter. Searching "Foster" returns
  411 pages, nearly all from his thirteen volumes; a reader looking for where Moreland or Smith cite Foster cannot
  find it. Searching "Banerji" returns all 24 pages of *The Pālas of Bengal*, and every excerpt begins with the
  title and author ("The Pālas of Bengal R. D. Banerji [p. 9] ..."), not the passage. The same happens with title
  words: every chapter of *The Truth About Indian Opium* matches "opium".
- Rule: D7 (search reads the whole text; results should point to where the words occur).
- Fix: add `data-pagefind-ignore` to both spans (Pagefind's default ignore mode, "index", still reads metadata
  inside an ignored element), rebuild, and confirm in a test that a chapter's excerpt does not begin with its
  book's title and that `Foster` returns far fewer than 400 pages.
- Resolution: Fixed. Both spans carry `data-pagefind-ignore`. Test: `SearchAndPages.test_title_and_author_are_not_indexed_as_words_of_every_chapter`.

### 4. [medium] Stage One books are told the quirks of a vision-language model, though some were made with plain OCR
- Where: `layouts/_partials/book/reading.html:13` (`rd-key`) and `:15-23` (the quirks list), shown to the 16
  `v1_archive` books as well; `layouts/chapters/page.html:116` ("It may hold small errors").
- Failure: the records of `comprehensive-history-india-v1` and `-v2` say their text was "extracted ... using
  PaddleOCR, then used Google AI Studio to clean it up", and others say "AI-assisted extraction" without saying
  how. Their pages say "its mistakes are not the ones older OCR made. OCR leaves garbled letters ... A language
  model reads for sense", and every chapter says "It may hold small errors". For an OCR-first text the opposite
  is the likely failure: garbled letters. The PaddleOCR record itself puts accuracy at "well north of 95%",
  which on a 300-page book is thousands of wrong words, not "small errors". Separately,
  `imperial-gazetteer-india-v1`'s record says "The appendix, glossary, and index have been omitted from this
  digital edition", and no page says so (no template reads `digitization_notes`), so a reader looking for the
  index will think it is lost from the source.
- Rule: D28 ("Stage One books ... get the account without [the score]" assumes the account is true of them);
  global standard on provenance on every record.
- Fix: for `isV1`, replace `rd-key` and the quirks list with a short, true account (read from the scans by an
  earlier method, OCR and AI clean-up, not checked page by page), and on Stage One chapters drop "small". Show a
  record's omissions (from `digitization_notes`, or a new field) in "This edition".
- Resolution: Fixed. Stage One books get their own account (OCR or an earlier AI reading, cleaned up with AI, not read page by page; errors of either kind) without the model's quirks; their chapters say "It may hold errors". Omissions are shown from `data/edition_notes.toml` (the record that says so is `modern-religious-movements-india`, not the Gazetteer). Test updated.

### 5. [medium] The score stands among the facts as "N of 100, checked", without the limit D28 requires beside it
- Where: `layouts/books/book.html:76` (`<a class="fact-score">…<span>of 100, checked</span>`).
- Failure: 26 books show "100 of 100, checked" at the top of the page, next to "584 pages". A stranger reads
  "100% checked". The caveat ("A book can score 100 and still hold misreadings") is several screens down.
  D28 itself rejects a bare number because it "would claim more than the checks measure".
- Rule: D28.
- Fix: label it so it cannot be read as proofread, e.g. "of 100 in the automatic checks", or drop "checked".
- Resolution: Fixed. The label reads "of 100 in automatic checks". Test: `test_a_score_among_the_facts_cannot_be_read_as_proofread`.

### 6. [low] The "Lately added" sentence will be wrong when fewer than six books arrive on a day
- Where: `layouts/blog/section.html:49`.
- Failure: the text is fixed: "{N} editions on that day; six of them, from across the shelves, are here." The next
  time three books are added on one day the journal says "Three editions on that day; six of them ... are here",
  and when one is added, "One editions". Today it reads correctly only because 47 were added at once.
- Fix: say "six of them" only when `len $added` is over six; otherwise "all of them"; use the singular for one.
- Resolution: Fixed: one, six or fewer, and more than six each read correctly.

### 7. [low] The authors page counts an office and "Various Authors" as writers
- Where: `layouts/authors/section.html:15`.
- Failure: "Forty writers, filed by surname" counts "Great Britain. India Office" (filed under O, as "Office") and
  "Various Authors". Small, but it is the first sentence of the page.
- Fix: count only personal authors, or say "Forty names"; file corporate authors under their first word.
- Resolution: Fixed by counting honestly: "Forty names, filed by surname".

### 8. [low] Third-ink text on the score panel falls just below AA contrast
- Where: `layouts/_partials/book/reading.html:33` (`.pl-n i`, the "/25" after each part's score).
- Failure: measured 4.26:1 on the panel's tint in light mode and 4.47:1 in dark mode, at 16px; WCAG AA needs 4.5:1.
  D24 darkened `--ink-3` to 4.8:1 against white, not against tinted panels.
- Fix: use `--ink-2` for it, or audit `--ink-3` on every tinted surface.
- Resolution: Fixed: `.pl-n i` uses `--ink-2`.

### 9. [low] The header test is skipped when the file is run on its own
- Where: `tests/test_checks.py:81` (`if __name__ == "__main__": unittest.main()`) comes before `class Headers` at
  `:85`.
- Failure: `python3 tests/test_checks.py` runs `unittest.main()` before `Headers` is defined, so the pagefind cache
  test silently does not run. `verify` uses `discover`, so it does run there.
- Fix: move the `__main__` block to the end of the file.
- Resolution: Fixed: the `__main__` block is at the end of the file.

### 10. [low] The visual grammar disagrees with the code and with D29 in two places
- Where: `docs/VISUAL_GRAMMAR.md:126` says the headline's last phrase is "italic in the house ink"; D29 and
  `assets/css/plate.css:208` make it upright. `docs/VISUAL_GRAMMAR.md:224` says a plate's name is italic "if it is
  a scientific or foreign name"; D29 allows only scientific names. Relatedly, the footer sets the foreign word
  `akṣara` in italic (`layouts/_partials/page/foot.html:7`), which D29 does not allow for.
- Failure: the next person (or model) to build a component from the grammar will reintroduce italic that D29
  removed. The global standard counts a doc that disagrees with the code as a bug.
- Fix: correct both lines; decide whether foreign words are a fourth D29 exception and record it.
- Resolution: Fixed both lines; foreign words cited as words are a fourth D29 case, recorded in D29.

### 11. [low] `verify` still has no format or lint check, and does not exercise the headers
- Where: `verify`.
- Failure: finding 1 shipped through a green `verify` because nothing serves the build with `_headers` applied.
  The format/lint gap is carried over from reviews 0001 and 0002.
- Fix: add the hash check from finding 1 (cheap and catches this class of failure) and the long-deferred lint step.
- Resolution: Partly fixed: the hash check now catches the class of failure behind finding 1. A format/lint step is still not added; carried over.
