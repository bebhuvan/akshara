---
title: "Stage Two of Akshara: 47 New Books, an Archival Compiler, and an Open Call for Proofreaders"
date: 2026-11-19
description: "How a solo, out-of-pocket passion project went from copy-pasting pages in AI Studio to digitizing 47 foundational Indian volumes (15,681 pages and 1,004 statistical tables) in days—and why we are opening the archive for community proofreading."
category: "Dispatches"
tags: ["stage two", "public domain", "archival compiler", "vlm", "indian economic history", "proofreading"]
---

Last December, when I wrote [the first post introducing Akshara](/blog/introducing-akshara/), the project was held together with duct tape, stubbornness, and sheer bloody-mindedness.

If you want to know how hacky Stage One was, here is the truth: for the first book I put up—*Life and Letters of Raja Rammohun Roy*—I literally uploaded PDF chunks into Google AI Studio by hand, waited for it to spit out Markdown, copied the text into a local file, and glued chapters together myself. Then I discovered Baidu's Paddle OCR free tier and, like any self-respecting Indian trying to stretch zero budget, created three accounts to run OCR on my laptop overnight. Even after [Kailash](https://nadh.in) finally sat me down and showed me how to call LLM APIs directly, every 300-page book still took hours of brittle regex scripts, manual chapter slicing, and eyeball debugging. It took three to four agonizing months just to limp to twenty-something books.

And yet the underlying itch never went away. We boast endlessly about being a multi-millennial civilization. Yet if you go looking for clean, open, readable, well-typeset public-domain editions of foundational Indian books—the economic histories, famine commission tracts, district surveys, East India Company letter-books, and parliamentary testimonies that actually explain how this subcontinent functioned—what exists? Almost nothing. The scans sit trapped in crooked, blot-compressed PDFs on the Internet Archive, often photographed by Western university libraries a century after the books were printed. We still don't have a Project Gutenberg or Standard Ebooks for India.

Over the past few weeks, two things happened at once.

First, there was a genuine step-change in frontier vision-language models—especially Google's latest Gemini models (`Gemini 3.8 Flash`, `Gemini 4 Hydrogen`, and `Gemini 4 Argon`), alongside Anthropic's Claude models, which helped architect, stress-test, and harden the software around them. Second, through hundreds of expensive, trial-and-error runs, I stopped treating book digitization as a prompt-engineering trick and built what it actually needed to be: **an archival compiler**.

The result is Stage Two of Akshara. Over the last few days alone, the new compiler digitized **47 complete historical volumes**—**15,681 pages** and **1,004 structured statistical tables**—at roughly **\$0.50 to \$3.00 per volume** in API spend.

---

## Why 19th-Century Indian Books Break Normal OCR (and Naive LLM Prompts)

If you have never tried to extract text from an 1807 London imprint or an 1893 Calcutta parliamentary return, it is easy to assume "OCR is a solved problem." It isn't. Historical Indian print is an obstacle course specifically engineered to humiliate generic pipelines:

1. **The Archive.org Compression Trap**: The default PDFs on the Internet Archive are processed with aggressive JBIG2/MRC foreground compression. On a dense statistical page, that compression literally swaps digits—turning a `3` into an `8`—or smears faded lead type into unreadable ink blots. Our compiler refuses to read compressed derivative PDFs whenever raw camera scans exist: it pulls the original `_jp2.zip` camera images and rebuilds a clean `.originals.pdf` at `1:1` native camera pixel resolution before a model ever sees a single page.
2. **Autoregressive Table Lying**: Give an LLM a dense 19th-century trade ledger denominated in pre-decimal *Rupees, Annas, and Pies* (`1:16:12`) or *Pounds, Shillings, and Pence* (`1:20:12`), and watch what happens when it misreads one digit in column three: rather than admit uncertainty, the model quietly *alters the printed Total row at the bottom* so the column adds up! Our pipeline defeats this with a two-part guard: deterministic colonial arithmetic validators, plus a **blind 450-DPI totals-strip pass** that crops only the bottom total row out of context so the model cannot cheat from the rows above.
3. **Diplomatic Orthography and Diacritics**: A nineteenth-century history written by Romesh Chunder Dutt, Francis Buchanan, or W. H. Moreland is full of period English spellings (*shew*, *connexion*, *ryotwar*), Geneva IAST (`Rājputāna`, `ṣūbahdār`), pre-IAST Hunterian acutes (`Rájputána`, `Kâshmîr`), and occasional Greek or Devanagari passages. Standard LLM prompts try to be "helpful" by silently modernizing spellings and stripping accents. Akshara treats **100% diplomatic fidelity** as non-negotiable: we preserve what the printer printed, including original compositor discrepancies.
4. **Split Footnotes, Shoulder Marginalia, and Broadsides**: In old histories, 6-point footnotes keyed by `*`, `†`, `‡` spill across two or three physical pages; shoulder notes sit tucked into outer margins; and massive fold-out statistical tables are bound sideways.

---

## How the Sixth-Generation Compiler Works

Instead of asking a language model to emit a finished Markdown book in one giant, hallucination-prone dump, the sixth-generation compiler (`akshara_new`) separates **visual observation** from **deterministic assembly**:

| Stage | What Happens | Why It Matters |
| :--- | :--- | :--- |
| **1. Camera JP2 Ingest** | Reconstructs `.originals.pdf` from raw Archive.org camera JP2s & detects sideways broadsides | Eliminates JBIG2 digit-swap corruption before extraction |
| **2. Lean Visual Wire** | `Gemini 3.8 Flash` or `Gemini 4 Hydrogen` (via Batch API + Context Cache) observes blocks, bboxes, and inline formatting (`<i>`, `<sc>`, `<sup>`) | Cuts output tokens ~50%, prevents `MAX_TOKENS` drops on dense indexes |
| **3. Deterministic IR & Rescue** | Validates `Rs. a. p.` / `£ s. d.` / lakh arithmetic, checks diacritic drift, runs 450-DPI crop re-reads & continuation arbiters | Catches silent errors and repairs cross-page split paragraphs and footnotes |
| **4. Unified `BookAST`** | Compiles all output formats from one canonical structural tree and scores a 100-point quantitative rubric | Guarantees Web, EPUB 3, HTML, Markdown, TEI XML, and CSVs never diverge |

Across our benchmarks and real-book audits, this architecture puts raw extraction accuracy well north of traditional OCR—typically **98.5% to 99.8%+** on historical prose and apparatus before a human eye even touches the text—while cutting the cost of digitizing a 450-page volume to the price of a cup of coffee.

---

## What Is Launching Today: 47 Volumes & 1,004 CSV Tables

Our first major Stage Two wave focuses heavily on **Indian Economic History (1600–1925)** alongside foundational general histories—the primary evidence base for understanding how India's agrarian, commercial, monetary, and industrial life evolved over three centuries:

- **The Drain Debate & National Political Economy**: Dadabhai Naoroji's *Poverty and Un-British Rule in India* (1901) alongside his *Essays, Speeches, Addresses and Writings* (1887) and *Speeches and Writings* (1918); Romesh Chunder Dutt's two-volume *The Economic History of India* (*Under Early British Rule* and *In the Victorian Age*); Lala Lajpat Rai's *England's Debt to India* (1917); and Raja Rammohun Roy's 1832 Parliamentary testimony, *Exposition of the Practical Operation of the Judicial and Revenue Systems of India*.
- **Famines, Land Settlements & Rural Surveys**: Francis Buchanan's monumental three-volume *A Journey from Madras through the Countries of Mysore, Canara, and Malabar* (1807)—1,670 pages packed with 177 statistical tables and 80 engraved plates and maps; Dutt's *Famines and Land Assessments in India*; Alexander Loveday's *History & Economics of Indian Famines*; A. T. Etheridge's *Report on Past Famines in the Bombay Presidency* (1868); J. C. Jack's classic household survey *The Economic Life of a Bengal District: Faridpur* (1916); and S. S. Thorburn's *Musalmans and Money-Lenders in the Punjab* (1886).
- **East India Company & Early Modern Commerce**: William Foster's *The English Factories in India* multi-volume series (all twelve volumes, Vols. I–XII), *The First Letter-Book of the East India Company (1600–1619)*, *Early Travels in India (1583–1619)*, Shafaat Ahmad Khan's *The East India Trade in the XVIIth Century*, and Wilfred Schoff's annotated *Periplus of the Erythræan Sea* (1912).
- **Mughal & Classical Foundations**: W. H. Moreland's *India at the Death of Akbar* (1920) and *From Akbar to Aurangzeb* (1923), Jadunath Sarkar's *Mughal Administration* (1920), Mahadev Govind Ranade's *Introduction to the Peishwa's Diaries* (1900), Vincent Smith's *Early History of India* (1924), and R. D. Banerji's *The Pālas of Bengal* (1915).

### Seven Open Formats Per Book

Google Drive folders were a clumsy stopgap. Every Stage Two volume is now packaged cleanly for readers, scholars, and programmers:

1. **Chapter-by-Chapter Web Reader** right here on `akshara.ink`, with outer-margin printed `[p. N]` folio markers—click any `[p. N]` button to slide open the original Internet Archive scan leaf beside the text.
2. **Single-Page Gutenberg HTML**: The entire book in one self-contained HTML file for instant `Ctrl+F` searching or offline saving.
3. **Typeset EPUB 3**: With pop-up footnotes, semantic navigation, progressive JPEG illustrations, and contextual covers.
4. **Scholarly Markdown & TEI P5 XML**: Clean plain text plus archival XML masters ready for scholarly tooling or one-command `.docx` export.
5. **Archival Print PDF & Original Scan Backups**: Published cleanly on our open GitHub library repository (`akshara-library`), including the de-blotted camera-original PDF so a vanishing Archive.org link never erases our source witness.
6. **Diplomatic & Tidy CSV Datasets**: All **1,004 extracted statistical tables**—75,365 tidy data observations—searchable in our [Statistical Atlas](/datasets/) and downloadable as ready-to-analyze CSVs.

---

## Honest Provenance & An Open Call for Proofreaders

One rule governs everything we publish: **never pretend machine output is human-certified.**

Holding back 47 foundational books indefinitely until an army of volunteers proofreads all 15,681 pages would defeat the point of public access. Conversely, hiding model uncertainty behind fake certainty betrays scholarly trust. So every edition on Akshara carries one of three explicit provenance badges:

- **Community Edition**: All structural, compilation, and page-completeness checks pass, and every folio maps cleanly to its source scan—but open numeric or glyph hotspots remain flagged for human eyes.
- **Machine-Checked Edition**: A **100.0 / 100** rubric score with zero open validator hotspots after surgical close-up crop verification—while stating plainly how many pages had flagged passages re-read and that zero pages have yet been signed off by a person.
- **Source-Certified Edition** *(our ultimate goal)*: Every single page checked independently against the original scan by a human proofreader, with an optional second independent pass.

That final tier is where I need your help.

**[Akshara Proofing](https://akshara-proofing.r-bhuvanesh2007.workers.dev)** is our live, lightweight, zero-ceremony distributed proofreader inspired by Distributed Proofreaders and Wikisource. You open a book, pick a single page (a five-minute task), see the deep-zoom scan right beside the plain text, fix whatever the machine misread, and save. Verified corrections export cleanly into our open Git repository and rebuild the web and EPUB editions.

If you care about preserving India's written commons—whether you are a historian, an economist tired of manually retyping 19th-century tables, a programmer, or simply someone who loves reading old books—explore the [Library](/books/), dig into the [Statistical Atlas](/datasets/), inspect the raw artifacts on [GitHub](/github/), and [get in touch](/contact/) if you want to be among the first wave of proofreaders.

Words endure when someone bothers to keep the lamp lit. Let's keep building.
