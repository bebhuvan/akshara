---
title: "About"
type: "page"
layout: "about"
---

# Project Akshara

Hi, my name is Bhuvan, and this is my passion project.

I love reading. In one form or another, I've read for as long as I can remember. If I can confidently claim to know a thing or two—or even anything at all—it is because pretty much everything that has happened to me revolves around words and pages. I owe a deep gratitude to these magical squiggly lines that have given me so much.

Somewhere along my reading journey, I came across the concept of the public domain. At the time, I was too dumb to immediately realise its importance. It took me a few years before it slowly started to sink in: just how extraordinary the idea really is. The fact that something like 99% of the written wisdom of our world is available for free, out of copyright, on the internet is not an easy thing to wrap one's head around. For me, it was like a slow-release drug. But once it finally clicked, it fundamentally changed how I think about knowledge, books, writing—and what it means to read and write.

Around the same time, I came across [Project Gutenberg](https://www.gutenberg.org/). I think it was when I discovered Blaise Pascal's *Pensées*—available for free, in a clean and readable format. That was when it hit me just how bloody awesome that website is.

And then one question began to bother me deeply: **why isn't there a Project Gutenberg for India?**

There is no shortage of jingoistic rhetoric about the richness of Indian civilisation—how it spans thousands of years, how we have supposedly given the world everything. Here I can't resist making the plastic surgery and flying planes joke. We constantly beat our chests about being a great nation, the oldest civilisation. And yet, we have done a fucking piss-poor job of preserving our written heritage.

Given the sheer amount of wisdom accumulated over centuries, much of it is still not easily accessible to anyone genuinely interested in learning about India.

I felt a strong urge to do something about it. The problem was that I'm not a technical person. I'm a coder with a K, not a C. I didn't even know where to begin.

Then large language models entered our lives. At first, I thought of it like a bad smell wafting in through an open window. Okay, I'm joking. But suddenly, even idiots like me had access to coding tools—Claude Code, Cursor, and so on. I started using them to build small websites.

I couldn't figure out how to build even a terrible, small-scale version of Project Gutenberg. But then an idea popped into my head: if I couldn't build a site where all these texts were readable, I could at least build a simple directory—a collection of links to Indian literary and historical works on Project Gutenberg, Archive.org, and other places where noble souls had already done the hard work of digitising these old texts.

That project became [Dhwani](https://dhwani.ink)—*dhwani* as in the Kannada word for sound.

But while browsing Archive.org, I kept coming across so many extraordinary works—across multiple languages, rich with historical and cultural detail. The urge to do something more kept growing.

A couple of colleagues introduced me to OCR—optical character recognition. I started experimenting with Tesseract, but the output was poor. Then, by accident, I came across a tweet announcing a new OCR model from Baidu. And luckily—because the Chinese are generous—they had a free API tier that allowed OCR for up to 3,000 pages a day.

Baidu's Paddle OCR turned out to be ridiculously good at extracting text from old, horrible, unreadable PDFs. All of a sudden, 70–80% accurate text extraction was feasible.

And so, like any self-respecting Indian, I created three accounts to scam Baidu and started running OCR on my laptop through the night.

But the error rates were still high. Large chunks of text couldn't be extracted. Tables were a mess. Then [Kailash](https://nadh.in) suggested using LLM APIs directly—things like Gemini. Suddenly, accuracy shot up to 90–95%. The downside was hallucinations, poor formatting, and other issues.

For the first four or five books, I extracted text using Paddle OCR, then manually copy-pasted and reassembled chunks in Gemini's AI Studio. I did this for a couple of thousand pages. Very quickly, my eyes started hurting. That's when I discovered you could use LLM APIs directly to extract clean text.

After K showed me how to use LLM APIs to extract text, he jokingly said: "That's one small step for man, one giant leap for a**hole." It was funny—but also painfully true.

That's essentially the backstory of this project.

Right now, I'm doing this alone. I'd love to turn this into a volunteer effort someday.

The cheaper API models are reasonably okay, but the costs still add up. Ideally, I'd love to use the costlier models—Sonnet, Gemini 2.5 Pro, Gemini 2.5 Think, Gemini 3—but the API costs are prohibitively expensive. Hopefully, they become cheaper over time, so I'll be able to publish more books here.

I don't know where this will go, but I'm genuinely excited. There are so many amazing books—trapped inside horribly scanned PDFs—just waiting to be read.

You might ask: why do this? Initially, I told myself it would help scholars and researchers. But if I'm honest, that's not the real reason. The simple reason is this: **do I think this should exist? Yes.** And that's it.

Whether anyone visits the site, whether people find it useful—I honestly don't know. Any other justification feels like a way to masturbate my own ego.

At a very high level, this site is a love letter to the public domain. There is an insane amount of wealth and wisdom freely available there. And we Indians have done a horrible job of protecting our public knowledge commons. I just want to contribute, in a very small way, to making that better.

I don't harbour grand illusions that I'll change everything. I'd simply rather do something than nothing.

Another reason comes from a podcast by Venkatesh Rao. He said that we all draw from the same pool of words—and that the goal should be to add more back than we take out. That framing stuck with me. It's pretty much how I think about reading and writing: you add back a little, in whatever shape or form, to the common pool of wisdom.

We live in a moment where books are being banned, authors are being kicked out, atomistic tendencies are on the rise, and hope often feels thin. There are attempts—across the world—to rewrite history itself.

In his book *Knife*, Salman Rushdie [writes](https://www.goodreads.com/quotes/12220571-we-are-engaged-in-a-world-war-of-stories-a-war):

> We are engaged in a world war of stories—a war between incompatible versions of reality—and we need to learn how to fight it. A tyrant has arisen in Russia and brutality engulfs Ukraine, whose people, led by a satirist turned hero, offer heroic resistance, and are already creating a legend of freedom. The tyrant creates false narratives to justify his assault—the Ukrainians are Nazis, and Russia is menaced by Western conspiracies. He seeks to brainwash his own citizens with such lying stories. Meanwhile, America is sliding back towards the Middle Ages, as white supremacy exerts itself not only over Black bodies, but over women's bodies too. False narratives rooted in antiquated religiosity and bigoted ideas from hundreds of years ago are used to justify this, and find willing audiences and believers. In India, religious sectarianism and political authoritarianism go hand in hand, and violence grows as democracy dies. Once again, false narratives of Indian history are in play, narratives that privilege the majority and oppress minorities; and these narratives, let it be said, are popular, just as the Russian tyrant's lies are believed. This, now, is the ugly dailiness of the world. How should we respond?

That line hit me like a ton of bricks.

One grandiose hope—if you, the discerning and judgmental reader, will allow me—is that this site acts as a small antidote: a bulwark against people's fetish for rewriting history to suit their own idiotic purposes. I hope that making our history and culture readable, and preserving it in some form, contributes towards that larger cause.

The final reason—one that will fully expose my spectacular lack of IQ—is simply this: I think words are truly amazing.

Just think about what words actually are. Random sequences of squiggly lines on a piece of paper or a screen. And yet they can unleash profound visions, wild reveries, throw you into deep spirals of contemplation, and hold up a mirror—showing you who you truly are, and who we truly are.

That is magical.

None of this would have been possible without my friend Joice and the great [Kailash](https://nadh.in), who showed me how to use these LLM APIs.

As I've watched these models progress, I genuinely believe they'll unlock new use cases around text—especially text extracted through this project. I can imagine AI-assisted books, strange magazines, experiments grounded in historical source material. Those are things I hope to do someday.

But for now, this is a humble start.

## Why Akshara?

*Akshara* was the first word that popped into my head. It's a Kannada word for "letter." But when I looked it up on [alar.ink](https://alar.ink/dictionary/kannada/english/%E0%B2%85%E0%B2%95%E0%B3%8D%E0%B2%B7%E0%B2%B0), I discovered it also means: undecaying, imperishable, not degenerating, eternal.

**ಅಕ್ಷರ** (*akṣara*)  
*adjective:* undecaying; imperishable; not degenerating; eternal.

*noun:* a letter of the alphabet; a syllable; a sign representing a sound of speech; that which is written; hand-writing; a written message.

I can't think of a better name than that.

Words are truly eternal.

## Get in Touch

If you'd like to reach out, you can find me at:

[bebhuvan.com](https://bebhuvan.com) · [LinkedIn](https://www.linkedin.com/in/bebhuvan/) · [Substack](https://bhuvan.substack.com/) · [Twitter](https://twitter.com/bebhuvan) · [Email](mailto:bhuvan@bebhuvan.com)

