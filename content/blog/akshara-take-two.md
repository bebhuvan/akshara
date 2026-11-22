---
title: "Akshara, Take Two"
date: 2026-11-22
description: "The messy backstory of Project Akshara—from copy-pasting PDFs in AI Studio to 66 books, a distributed proofing site, and crazier experiments ahead."
category: "Dispatches"
tags: ["akshara", "public domain", "proofreading", "paper lanterns"]
---

![Fine-line architectural etching of a sunlit 19th-century Indian library archway with partly open louvered shutters and a single book resting on a wooden table](/img/akshara-take-two.webp)

Hello, random stranger, possible book lover, or person who accidentally clicked a link and landed here. And hello, LLM bot scraping this page too. I'm [Bhuvan](https://bebhuvan.com), and welcome to an all-new, revamped Project Akshara.

I started Akshara around this time last year, and for a while it took a backseat. I hadn't uploaded new books in months, though I never really stopped working on it. Even though you didn't ask for it, let me tell you the backstory—what Akshara is, how it came to be, why I'm doing this, how I do it, and why I'm so excited, ebullient, and overjoyed about it right now.

I discovered the virtues of the public domain relatively late in life. That some of the greatest books, letters, pamphlets, ideas, music, poetry, and philosophy ever created were freely available for anybody to read, watch, listen to, reuse, and build upon just shattered my already flimsy brain.

Somewhere along that reading journey, I came across Project Gutenberg. I loved the sheer audacity of the idea, let alone that somebody actually made it real—more than 70,000 books, free to download, remix, and share. It's an absurd notion. The fact that volunteers pulled it off before the modern web even existed is spectacular.

And a question got stuck in my head: why isn't there a Project Gutenberg for India?

We talk endlessly about our history—how old it is, how we gave the world this and that, all our jingoistic boasts. And yet when it comes to preserving the written memory of our civilization, we've done a piss-poor job. Yes, a piss-poor job. Sure, there are lakhs of scans of public-domain Indian books scattered across the Internet Archive, Heidelberg, Chicago's DSAL, and elsewhere. Every year the government spends god knows how many hundreds or thousands of crores on digitizing this and preserving that, and I've lost track of the portals built to make archives accessible. Where did all that money go? Where are the actual books?

It depressed me a little that nobody bothered to fix this, even though I knew of noble souls who spent their entire lives scanning and archiving these books—people like Omshivaprakash (behind [Sanchaya](https://sanchaya.org) and Servants of Knowledge) and [Shiju Alex](https://shijualex.in) (behind [Granthappura](https://gpura.org) and the [Indic Digital Archive Foundation](https://indicarchive.org/)). But scanning is only one part of it. If a book isn't easy to read and share, its reach shrinks. Even for me, there's only so much patience I have for squinting at shoddy scans.

This kept bothering me, but I couldn't do anything about it because I wasn't a coder—I don't know JavaScript from idli-vada. Just a reader and a bit of a writer. Then, after 2023, coding tools like Windsurf, Claude Code, and Codex showed up, and I saw a glimmer of hope. I still had no intuition for turning old scans into clean, readable books, so the first thing I built was a small directory called [Dhwani](https://dhwani.ink/). I haven't worked on it since Akshara started, but at the time I figured if these books were unreadable, they should at least be discoverable.

Then I started messing around with OCR models and had an *oh shit* moment—I could actually do a little bit of this myself. I had no clue what I was doing. I was uploading entire 700-page PDFs straight into chat boxes and asking LLMs to transcribe them. I created five different accounts on Baidu's PaddleOCR to get around their 50,000-page monthly cap and ran books overnight. Even then, the output wasn't great.

In hindsight, what I was doing back then was very, very stupid. For the first couple of books—Harihar Das's *Life and Letters of Toru Dutt* and Sophia Dobson Collet's *The Life and Letters of Raja Rammohun Roy*—I tried Gemini, found it unreliable, then moved to Google AI Studio for its longer context window. I'd ask for Markdown, copy-paste the output, and stitch the files together by hand. I kept hitting recitation blocks and content filters, so I'd open a fresh session, chop the PDFs smaller, and do it all over again. A giant waste of time. But I don't come from a technical background, and I knew nothing about archiving or text extraction, so my stupidity has to be excused.

Everything changed when I happened to tell [Kailash](https://nadh.in) what I was doing. He gave me what can only be described as a quick workshop and told me to use Gemini models. I'd already been playing with vision models, I just didn't have a structure. Suddenly, extracting clean text and turning these books into downloadable EPUBs, PDFs, and Markdown files became doable. The vision models still had plenty of weird quirks, the coding tools weren't nearly as good as they are today, and I was doing it alone. Still, around November or December 2025, [Akshara](https://akshara.ink) went live with about 25 books.

After that, the site mostly sat still for a year. I kept processing books, and I also wasted a whole lot of money testing every model with vision capabilities—Gemini, Anthropic, Kimi, Qwen, GLM, DeepSeek. Parallelly, I started a sister project called [Paper Lanterns](https://paperlanterns.ink). Thanks to Shaun Usher's [*Letters of Note*](https://lettersofnote.com/), I fell in love with historical correspondence, which is insanely good, and started curating letters and transcribing whole collections—Rabindranath Tagore, Jawaharlal Nehru, Dostoevsky, and Gandhi to start with, plus a bunch more I still haven't put up.

The real reason I stopped uploading to Akshara was proofreading. I was checking every book by hand, and reading word for word—Romesh Chunder Dutt's two volumes of *The Economic History of India* alone are 1,128 pages—is impossible with a full-time job and a family. So I did fuzzy checking: first and last word of each paragraph against the source PDF, making sure split paragraphs were joined, diacritics preserved, running headers stripped, tables intact. Even that took a full day per big book. Doing it weekend after weekend put so much stress on my eyes that I still have a slight pain in one eye from last year. It was untenable.

Then, a couple of weeks ago, the newer Gemini models launched. I had an old pipeline full of Python scripts, and on a whim I asked Gemini to look at it and build a better one. What followed was shocking. In the previous year, I had uploaded fewer than 25 books. In the last two weeks alone, Gemini helped me process 51 new books—over 18,000 pages, taking the library to 66 books—at accuracy well north of 90%, better than every OCR tool I've tried. Clean EPUBs and PDFs, and every chapter readable right on the site.

Around the same time, I realized proofreading only works if other people who care about this can pitch in—however many of us there are. I'd wanted to build that from the beginning, I just didn't know how, until Claude pointed me to [Distributed Proofreaders](https://www.pgdp.net/) (the volunteer system behind Project Gutenberg, similar to Wikisource). So I asked Gemini and Claude to build [Akshara Proofing](https://proof.akshara.ink), where anyone can open a book, inspect any page against the original scan, and flag errors right away—and if you'd like to proofread and edit full pages directly, drop me a note for an invite link. That's the new avatar of Akshara.

Now, before leaving for work, I tell Gemini to queue up a bunch of books and let it run through the day. I can easily do more than a couple of books a week now. The only real constraint is cost—roughly three to five dollars a book (and the same for each collection of letters), all out of pocket—so I stick mostly to cheaper models like Gemini Flash, plus Sonnet and Haiku for letters. The frontier models are noticeably better, but the cost shoots up fast, and Gemini's Flash discount ends on January 1st.

Still, these coding tools are so good that even a dummy like me can work on things that are wildly complex for someone with my abilities—and I'm measuring against a normie baseline here. A person without any technical background shouldn't be doing all of this solo, yet here I am. I still can't believe this is real.

And if somebody from the Gemini team is reading this: for all the people who shit on you, I remain a fan. Even when your coding capabilities were bad, your vision capabilities were really, really good, and Gemini has always been my primary vision model. Thank you for these models, for the discounts, and for keeping them cheap.

Now I want to try a few crazier things under Akshara. I work at Zerodha and I'm deeply interested in economic and financial history. I know a whole lot of random things about US financial history, and almost nothing about India's—mostly because there are very few modern works I can just buy and read. Again, we've done a piss-poor job documenting this. So the experiment I'm working on (coming soon) is a "living book" of the economic and financial history of India: extracting text from old economic books, pamphlets, and letters to build a corpus, and then getting an LLM to act as an author and write an economic history grounded directly in that archive. If it works, I want to try it for other topics I care about, like Indian maritime trade. I have no idea if it'll pan out, but LLMs are now letting me "just do things."

The other sub-project—in line with [Paper Lanterns](https://paperlanterns.ink)—is historical Indian correspondence. A lot of it is still in copyright, which is a challenge, but I want to find everything that's out of copyright and put it up, along with philosophy.

And the one thing I really, really want to do is regional literature—Hindi, Kannada, Tamil, Telugu, and so on. The models still aren't great at Indian scripts, and I need help proofreading. If you want to volunteer on languages that are better represented in LLM training sets, like Hindi, Kannada, or Tamil, I'd love to work with you.

So that's what I've been up to. Go to the library—I keep adding books, and the count will keep steadily growing. I'd love to hear your feedback, thoughts, brickbats, and suggestions.

Also, if you're an expert in archival digitization or vision LLMs and know how to do this better, cheaper, and at scale, I'd love to learn from you. I have no shame in admitting I'm just a monkey with Claude Code access. I'm 100% sure this can be done better than what one person hacked together solo—if you have advice or want to collaborate, please reach out.

Say hi anytime—email me at [bhuvan@bebhuvan.com](mailto:bhuvan@bebhuvan.com), or DM me on [Twitter](https://twitter.com/bebhuvan) (`@bebhuvan`), [LinkedIn](https://www.linkedin.com/in/bebhuvan/), or [Substack](https://bhuvan.substack.com/).

Anyway, thank you for landing here.

P.S. If somebody from the Gemini team really is reading: please give me some credits. I promise I'm putting them to good use—all of this is going straight back to the public domain with no commercial interest.
