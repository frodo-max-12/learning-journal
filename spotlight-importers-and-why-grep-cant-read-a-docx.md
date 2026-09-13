# Spotlight, Importers, and Why `grep` Can't Read a .docx

*This started as housekeeping, not curiosity. I wanted to find every résumé I'd ever written — PDFs and Word files — scattered across a laptop holding 4,768 files in one folder alone. I typed `"resume"` into a Finder window, got a wall of results, and realised I didn't actually understand what I was looking at. What is Finder doing when I type in that box? Is it reading my files right then, or something else? By the end I'd learned that Finder never touches your files when you search, that a `.docx` is a zip archive somebody already unpacked hours ago, and that the last honest answer to "when did I edit this?" is sealed inside the file rather than shown in the Date Modified column.*

---

## The question that started it

I had a specific target: **the newest résumé I had personally edited in Microsoft Word** — not the ones generated for me by a tool. Two clauses, and both turned out to be traps. "Newest" is a lie in a backup folder, and "personally edited" isn't something a filename can tell you.

But before any of that, the basic question: how does search on this machine work at all?

## Two machines, not three tools

I'd been thinking of Finder search, `ls`, and `grep` as three tools on a spectrum of power. They're not. There are **two completely different machines**, and everything else is a front-end.

**Machine A — the pre-built index.** macOS runs a background service, Spotlight, that watches for file changes. When a file changes, Spotlight cracks it open, extracts its text and metadata, and writes an index card: filename, kind, dates, author, and the full text inside — *including* text inside PDFs and Word documents. When you search, **nothing reads your files.** It reads the card catalogue. That's why it's instant across thousands of files.

Both of these are the same machine wearing different faces:

| Front-end | What it's for |
|---|---|
| **⌘Space** (Spotlight) | One best answer. Blends apps, files, Mail, Safari, calculator. Ranked and **truncated**. |
| **⌘F** (Finder Find) | Every matching file. Files only. Exhaustive, sortable, filterable, saveable. |
| **`mdfind`** (terminal) | The raw pipe to the same index. No ranking, no truncation, scriptable. |

Same catalogue, different hands. ⌘Space is a launcher that happens to search files; ⌘F is a query builder.

**Machine B — walking the actual shelves.** `ls`, `find`, and `grep` ignore the catalogue entirely and touch the real filesystem, right now.

| Tool | What it physically does | Reads inside a PDF/Word file? | Speed across a disk |
|---|---|---|---|
| `ls` | Lists names in one directory | No — names only | Instant per folder |
| `find` | Walks the tree, matches name/date/size | No — names and metadata only | Slow (minutes) |
| `grep` | Opens each file, scans **raw bytes** | **No** — see below | Very slow |
| Spotlight | Reads the pre-built index | **Yes** | Instant |

The `grep` row is the one that taught me something. `grep resume myfile.docx` finds nothing — not because grep is weak, but because a `.docx` is a **zip archive**. The text is compressed. Grep is looking at the right file and seeing genuine gibberish.

Spotlight wins not because it's cleverer at search time, but because **the expensive work already happened**, once, in the background, the moment I hit save.

## How the index gets built

The path a file takes, end to end:

```
file changes
   ↓  FSEvents  (the kernel notifies — no polling)
  mds           (the metadata server)
   ↓
mdworker        (sandboxed worker process)
   ↓  looks up the file's UTI, finds the matching plugin
Office.mdimporter / PDF.mdimporter / ...
   ↓  extracts text + metadata
inverted index in .Spotlight-V100
```

Three details worth keeping:

**`mdworker` is sandboxed** — it parses untrusted files all day, so a booby-trapped document shouldn't be able to own the machine through the indexer.

**Dispatch happens by UTI, not file extension.** A Uniform Type Identifier is the system's real answer to "what kind of thing is this" — my `.docx` resolves to `org.openxmlformats.wordprocessingml.document`.

**The final structure is an inverted index** — a map from *word* → *list of files containing it*. Same data structure that makes web search work, running on my laptop against my own files.

## The part I actually wanted to understand: importers

If a `.docx` is a zip, *something* has to know how to unzip it and find the text. Where does that knowledge live?

It's a **plugin**. Each `.mdimporter` bundle teaches Spotlight one family of formats:

```bash
mdimport -L        # list every registered importer
```

```
/System/Library/Spotlight/PDF.mdimporter
/System/Library/Spotlight/Office.mdimporter
/System/Library/Spotlight/RichText.mdimporter
/System/Library/Spotlight/iWork.mdimporter
/Applications/LibreOffice.app/Contents/Library/Spotlight/OOoSpotlightImporter.mdimporter
```

Twenty of them on my machine. The last line is the giveaway: **installing LibreOffice added its own importer.** Format knowledge isn't baked into the OS — it ships inside the app that understands the format. New format, new plugin, dropped in by the app. `mdworker` loads whichever plugin claims the file's UTI and calls a single entry point, handing it the path and an empty dictionary to fill.

So the answer to "does macOS contain the logic for walking a .docx?" is: **not in the OS core — in a plugin, and any app can add one.**

## Cracking one open by hand

The satisfying part was doing the importer's job manually. Taking one of my own résumés:

```bash
xxd 'Alice Smith Resume v15.1 062025.docx' | head -1
# 00000000: 504b 0304 ...
```

`504b` is `PK` in ASCII — the ZIP file signature, initials of Phil Katz who wrote the format. It is literally a zip. So list it like one:

```bash
unzip -l 'resume.docx'
```

```
   150284  word/document.xml       ← the body text
   207414  word/settings.xml
    61691  word/numbering.xml
    38107  word/styles.xml
      813  docProps/core.xml       ← author, dates, revision count
      992  docProps/app.xml        ← which application wrote this
```

The text lives in `<w:t>` ("word text") elements:

```bash
unzip -p resume.docx word/document.xml | grep -oE '<w:t[^>]*>[^<]+</w:t>' | head
```

```xml
<w:t>Alice</w:t>
<w:t xml:space="preserve"> Jain</w:t>
```

That's the whole trick. **The importer unzips the package, walks `word/document.xml` concatenating every `<w:t>` run into a plain-text stream, reads `docProps/core.xml` for the metadata, and hands both to Spotlight.** I'd guessed this was roughly what happened; watching the raw XML come out is different from guessing.

And a PDF needs a *completely different* importer, because a PDF has no `<w:t>` tags — it has content streams full of glyph-drawing operators. `PDF.mdimporter` has to map glyph codes back to Unicode through each font's encoding table. Which explains something I'd noticed before without understanding: **a scanned PDF indexes zero text.** There are no glyph operators, just a photograph of a page. Search goes blind on it unless OCR adds a text layer.

This connects to what I'd already worked out in [Everything Is Text Underneath](everything-is-text-underneath-file-formats-demystified.md) and [Three Categories of Document Formats](three-categories-of-document-formats.md) — but those answered *what a .docx is*. This answers *who unpacks it, and when*.

## When does the index fail?

Every mechanism deserves this question, and here I got a live demonstration by accident.

I created test files in a temp folder to check something, and `mdfind` returned **zero results** — while `mdls` happily read each file's type. The files existed. Their metadata was readable. But they weren't in the *store*, so search couldn't see them.

That's the whole failure mode in one shot: **the index is not the filesystem.** It's a model of the filesystem, and models go stale. Spotlight is blind to:

- Folders excluded in **Settings → Spotlight → Search Privacy**
- **External or network drives** that were never indexed
- **iCloud "optimize storage"** placeholders — metadata present, contents not on disk
- Anything changed in the last few seconds, before indexing catches up
- Files where the importer exists but extracts nothing (scanned PDFs)

`find` and `grep` are the fallback for exactly these cases, plus one more: **regex**. Spotlight's query language can't express "version numbers matching `v[0-9]+\.[0-9]+`". `grep -E` can.

So the rule I'd want to remember: **index by default, shelf when the index is blind or when you need a pattern it can't express.**

## The operators, tested rather than assumed

Finder's `Name` row has a dropdown — contains, matches, begins with, ends with, is — and I couldn't have told you the difference between the first two. Rather than reason about it, I made seven files with deliberately awkward names and ran each operator.

Files: `resume`, `resume.pdf`, `resumes.pdf`, `myresume.pdf`, `presumed.pdf`, `my resume final.pdf`, `annual resume.pdf`. Searching for `resume`:

| filename | contains | **matches** | begins with | ends with | is |
|---|:-:|:-:|:-:|:-:|:-:|
| `resume` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `resume.pdf` | ✓ | ✓ | ✓ | — | — |
| `resumes.pdf` | ✓ | **—** | ✓ | — | — |
| `myresume.pdf` | ✓ | **—** | — | — | — |
| `presumed.pdf` | ✓ | **—** | — | — | — |
| `my resume final.pdf` | ✓ | ✓ | — | — | — |
| `annual resume.pdf` | ✓ | ✓ | — | — | — |

Two things fell out that I would have got wrong:

**contains is substring; matches is whole-word.** `contains` finds `resume` buried inside `presumed` — it's doing pure substring matching with no notion of where words begin. `matches` respects word boundaries, so `presumed` and `myresume` drop out. That's the difference, and it's the one worth internalising: **`contains` over-collects, `matches` understands that names are made of words.** Note `resumes.pdf` also drops from `matches` — plural is a different word.

**"ends with" almost never does what you expect.** Only the extensionless `resume` matched. Not `annual resume.pdf` — because the real filename ends in `.pdf`, not `resume`. The operator works on the true filename, not the name Finder displays with extensions hidden. Useful for `ends with .docx`; near-useless for words.

I also got the underlying query wrong on my first attempt — I assumed `matches` mapped to a wildcard query, ran it, and got results identical to `contains`. The test files are what caught it. Guessing the mechanism and checking the mechanism are different activities, and only one of them is reliable.

## "Document" does not include PDF

The `Kind` dropdown offers *Any, Application, Archive, Document, Executable, Folder, Image, Movie, Music, PDF, Presentation, Text, Other* — single-select, radio buttons. Wanting both PDFs and Word files, the obvious move is to pick "Document" and assume it covers both.

Measured against my own résumé files:

| Kind filter | matches |
|---|--:|
| `kind:pdf` | 450 |
| `kind:word` (catches `.doc` *and* `.docx`) | 296 |
| `kind:document` | **351** |
| PDF **or** Word combined | **746** |

If "Document" contained PDFs it would be at least 450. It's 351 — it catches Word, Pages, RTF and **none of the 450 PDFs.** Picking the intuitive option would have silently dropped every PDF I owned, with no error and no warning. A filter that quietly under-collects is worse than one that fails loudly.

The fix is to stop using the dropdown and type the query, where `OR` exists:

```
resume kind:pdf OR resume kind:word
```

Space means AND, capital `OR` means or. The typed `kind:` token *is* the same filter as the dropdown, minus the ceiling on expressiveness. (In the UI, ⌥-clicking the `+` button turns it into `···` and inserts a nested **Any/All/None** group — that's how you build an OR visually.)

## Metadata as evidence

Back to the original question: **the newest résumé I edited in Word myself.**

Sorting by Date Modified is wrong here, and it's worth being precise about why. Most of my résumés live inside a folder copied off an old laptop. Copying rewrites modification timestamps. The Finder column would have been reporting *when the backup was made*, not when I wrote anything — sorting by it would have produced a confident, wrong answer.

But `docProps/core.xml` is written **by Word, inside the file, at save time**, and copying a file doesn't touch its contents:

```bash
unzip -p resume.docx docProps/core.xml
```

```xml
<dc:creator>Alice Smith</dc:creator>
<cp:revision>9</cp:revision>
<dcterms:modified>2025-06-17T08:28:00Z</dcterms:modified>
```

So I extracted that from all 272 candidate `.docx` files and sorted on the *internal* date. Then, to be sure nothing newer existed under a different name, I swept **every** `.docx` on the machine with an internal save-date after that timestamp — 131 files, none of them résumés.

The second clause — *edited by me, not generated by a tool* — was answered by `docProps/app.xml`:

| | Word-saved file | Library-generated file |
|---|---|---|
| `Application` | `Microsoft Office Word` | *(empty)* |
| `dc:creator` | `Alice Smith` | `Un-named` |
| `cp:revision` | `9` | absent |

Word always stamps its own name into `<Application>`. A file built by a software library leaves it blank. Some tool-generated documents on my disk even carried a real `dc:creator` name — the author field was set correctly — but the empty `<Application>` gave them away. **One field was forgeable-looking; the other was the real fingerprint.**

That's the generalisable idea, and it's the thing I'd most want to keep: **a file carries several independent records of its own history, and they fail differently.** Filesystem timestamps are maintained by the OS and get destroyed by copying. Internal metadata is maintained by the authoring application and survives copying. When two sources disagree, the question isn't "which do I trust" but "what is each one actually a record of?"

## What I'd want to remember

- **Finder search never reads your files.** It reads a card catalogue built in the background. ⌘Space, ⌘F, and `mdfind` are three faces of one index.
- **The catalogue can read a .docx because a plugin taught it how** — an `.mdimporter` bundle, dispatched by UTI, shipped inside the app that owns the format. `grep` fails on the same file because nobody taught grep anything; it sees compressed bytes.
- **The index is a model of the filesystem, not the filesystem.** It goes blind on unindexed drives, excluded folders, cloud placeholders and scanned PDFs. That's when you walk the shelves with `find`.
- **`contains` is substring, `matches` is whole-word.** I only learned the difference by building files designed to separate them.
- **Measure the filter before trusting it.** "Document" excluding PDF is the kind of thing that produces a wrong answer silently.
- **Ask what each timestamp is a record of.** The one Finder shows you and the one Word wrote inside the file answer different questions, and in a folder of copied files only one of them is answering yours.

The four questions I try to ask of anything new — *what does it bottom out in, why is it fast or slow, when does it fail, where else does it reach* — landed unusually cleanly here. It bottoms out in an inverted index and a set of format plugins. It's fast because the parsing happened once, at save time, not at search time. It fails when the index is stale or the importer has nothing to extract. And it reaches everywhere: this is the same architecture as [how web search engines work](how-search-engines-work-from-crawling-to-ranking.md) — crawl, extract, invert, query — with FSEvents playing the role of the crawler and my own disk as the corpus.
