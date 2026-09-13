# Why PDFs are binary, not text

---

## The thing that surprised me

I had always assumed PDFs were some kind of text format with formatting layered on top — like styled Markdown, or a "frozen" Word document. Open one in a text editor, I figured, and you'd see something readable underneath.

That assumption is wrong. A PDF is a **binary file** defined by an ISO standard (ISO 32000). Open one in a text editor and what you see is mostly garbage — compressed streams of drawing commands, embedded fonts, cross-reference tables. There is no "the text of the document" sitting anywhere in the file as a plain string. Instead there are thousands of instructions that say "draw glyph M at position (72, 720)" and "draw glyph u at position (80.5, 720)."

Once I saw this, every weird thing about working with PDFs made sense. The hard part of extracting text isn't the PDF being "messy" — the hard part is that PDFs were deliberately designed to *not* store text as text. That choice has a reason, and the reason is interesting.

## The original design goal: a digital piece of paper

PDF was created by John Warnock at Adobe in 1991. The pitch was one sentence: capture documents so they can be **viewed, printed, and exchanged anywhere, looking exactly the same, on any device, forever**.

That's the entire goal. Visual fidelity. Everything weird about the format is downstream of it.

In 1991, this was hard. Microsoft Word 1.0 had just released, and opening a `.doc` on a different version of Word, or on a Mac instead of Windows, rendered differently — page breaks moved, tables shifted, fonts substituted. HTML didn't exist publicly yet, and when it did, it was explicitly designed to *reflow* content based on the viewer's screen — opposite goal. The only digital format that rendered identically everywhere was paper, after you printed it. Adobe's pitch: make a digital format that behaves like paper.

So PDF's design question became: what's the smallest set of instructions that lets two different machines, with different OSes and different installed fonts, render the same pixel-perfect output?

The answer: don't ship the *text*, ship the *drawing commands*.

## What's actually inside a PDF

A decompressed chunk of a PDF looks like this:

```
BT                       % Begin Text object
/F1 12 Tf                % Use font F1 at 12pt
72 720 Td                % Move cursor to position (72, 720)
(Mukesh Ambani &) Tj     % Draw this text at current position
0 -14 Td                 % Move down 14 units
(family) Tj              % Draw this text
ET                       % End Text object
```

This is a page description language. It's not HTML, not Markdown, not Word — closer to PostScript or SVG. The PDF doesn't say "here is the paragraph 'Mukesh Ambani & family'." It says "draw these glyphs at these positions."

Three things follow:

1. **Each character has its absolute position pre-computed at authoring time.** The renderer doesn't decide where things go — the author did, and burned the result into the file. That's how the layout stays identical everywhere.
2. **The font is embedded in the file** (or the subset of glyphs used). Your machine doesn't need Helvetica installed — the PDF brings it.
3. **There are no "paragraphs," "lines," or "words."** Those are reading-level abstractions. The format only knows about glyphs at coordinates.

That last point is the source of every PDF text-extraction headache. There's no `<paragraph>` tag to look for. Any structural interpretation has to be *inferred* by extraction tools looking at the coordinate patterns.

## The trade-off

You're trading **semantic information** for **visual determinism**. Compare:

| Format | What it stores | Trade-off |
|---|---|---|
| HTML | `<p>Mukesh Ambani & family</p>` | Easy to extract. Layout varies by renderer. |
| Word `.docx` | XML with the text + style | Mostly easy to extract. Mostly consistent across viewers, not pixel-perfect. |
| PDF | "Draw M at x,y, draw u at x,y, ..." | Pixel-perfect everywhere. Extraction must reverse-engineer structure from coordinates. |

HTML and Word store *what the content is*. PDF stores *what to draw on the page*. Fundamentally different problems.

## The PostScript heritage

PDF is essentially "PostScript without the programming." PostScript (Adobe, 1982) was a full programming language for driving laser printers. For interactive document viewing, that was overkill and a security risk, so Adobe stripped it down to a fixed, deterministic subset — no loops, no variables — and called it PDF. The drawing commands above (`Td`, `Tj`, `Tf`, `BT`, `ET`) are direct descendants of PostScript operators.

This heritage is why PDF feels engineering-ish in a way HTML and Word don't. It was designed by graphics people for the print pipeline, not by document people for content authoring.

## The modern compromise: tagged PDFs

PDF actually supports a feature called **tagged PDF**, defined in the standard as PDF/UA (Universal Accessibility). A tagged PDF includes a parallel tree of semantic structure: "this is a heading, this is a paragraph, this is a table with these rows and columns." Screen readers use these tags. Extraction tools could too.

The catch: almost no PDFs in the wild are tagged. Authoring tools don't add tags by default. It's extra work for the author with no visual benefit. Compliance regulations (US Section 508, EU EN 301 549) are starting to push for it in government, healthcare, and finance — but adoption is slow.

When you do encounter a tagged PDF, extraction becomes trivial. When you don't (90%+ of PDFs), libraries fall back to layout analysis on the raw coordinate data.

## The mental model that makes everything click

PDF feels weirdly complex when you approach it expecting "a document format." It's actually **a page-rendering instruction set, frozen for portability.** Once that landed for me, every quirk made sense:

- Why text extraction is hard → the format doesn't know what text *is*, only what to draw.
- Why columns confuse extractors → there are no columns in the file, just characters at x-coordinates that cluster into columns when rendered.
- Why copy-pasting often produces garbled text → the draw order can differ from the reading order.
- Why scanned PDFs need OCR → they contain *images* of text, with no character objects at all.
- Why PDFs are ubiquitous in contracts and scientific publishing → both communities care more about visual fidelity than text extractability.

## The transferable principle

This taught me a general framing: **whenever a format seems badly designed for what I'm trying to do, ask what it was actually designed for.** Most "weird" formats are weird because they're optimised for a use case adjacent to but not the same as mine.

- PDF optimises for visual fidelity. Extraction is collateral damage.
- JSON optimises for machine-to-machine exchange.
- CSV optimises for spreadsheet compatibility.
- Protocol Buffers optimise for compact binary efficiency at Google scale.

Once I know the original goal, the design decisions stop feeling arbitrary. They start feeling like deliberate trade-offs.

---

*What I studied next: [Three categories of document formats](three-categories-of-document-formats.md) — extending the same "optimised for one axis" framing across the whole document landscape.*
