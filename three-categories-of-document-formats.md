# Three categories of document formats

---

## The framing that finally made sense

I had a vague intuition that `.txt`, `.md`, `.html`, `.docx`, and "Google Doc" were all roughly the same category of thing. They're not. They sit in three fundamentally different categories, each optimised for a different stage of a document's life.

| Category | Examples | What's being stored | Where it lives |
|---|---|---|---|
| **Plain text + markup** | `.txt`, `.md`, `.html` | Bytes you can read in any text editor | A file on disk |
| **Document packages** | `.docx`, `.odt`, `.rtf` | A bundle of content + styles + embedded media | A file on disk |
| **Cloud documents** | Google Doc, Notion page, Quip | A database record on someone's server | Not a file at all |

The first two are files. The third one **isn't a file** — which turns out to be the most important difference.

## Category 1: Plain text + markup

Shared rule: **the file is a sequence of characters you can open in any text editor and understand.** They differ in how much markup convention they layer on top.

```
# my_notes.txt — no markup at all
Mukesh Ambani & family
Rank 1
```

```markdown
# my_notes.md — lightweight markup
# Hurun India Rich List
**1. Mukesh Ambani & family**
```

```html
<!-- my_notes.html — heavier markup -->
<h1>Hurun India Rich List</h1>
<p><strong>1. Mukesh Ambani &amp; family</strong></p>
```

Markdown was designed in 2004 (by John Gruber) so that the raw file looks like what you'd write in an email. HTML uses verbose tags meant for browsers. Both are still just text — you can read them in Notepad.

**What this category gives you:** greppable, scriptable, diff-able. `grep "Ambani" *.md` works. Git shows line-by-line changes. Tiny file sizes. No proprietary tooling. Future-proof (UTF-8 will be readable in 50 years).

**What it lacks:** no embedded media (links to images break when you move the file), no layout control, no live edit experience.

This category dominates wherever content matters more than presentation: code, technical docs, blog posts, READMEs.

## Category 2: Document packages

`.docx` looks like a single file in Finder, but it's actually a **ZIP archive of XML files**. Try it on any `.docx` you have:

```bash
cp my_doc.docx my_doc.zip
unzip my_doc.zip
```

You'll find `word/document.xml` (the content), `word/styles.xml` (formatting), `word/media/` (embedded images), and metadata files. Microsoft moved to this design in 2007 (Office Open XML, ISO/IEC 29500). Before that, `.doc` was a closed proprietary binary blob.

OpenDocument (`.odt`, LibreOffice) is structurally identical: zip of XML files. RTF is a single text file with markup, largely obsolete now.

**What this category gives you:** self-contained editable richness (bold, fonts, images, tables, comments, track-changes — all bundled in one emailable file). Reasonable cross-app fidelity. Real WYSIWYG edit experience. Smaller than PDF.

**What it lacks:** not pixel-perfect across apps (this is the exact gap PDF was invented to fill). Not greppable from the outside. Hard to diff in git. De facto tied to proprietary tooling (Word, mostly).

This category dominates wherever you need rich content in a single shareable file: contracts, business reports, drafts in progress.

## Category 3: Cloud documents

This is the most different from the others, and the difference is conceptual, not just technical.

**A Google Doc is not a file.** There is no `my_essay.gdoc` sitting on a server's hard drive somewhere. The "document" exists as a constellation of rows scattered across multiple database tables — a row in `documents` for metadata, many rows in `paragraphs`, many rows in `edit_operations` (one per keystroke), rows in `permissions`, rows in `comments`. The "Google Doc" you see in your browser is **a rendering of that database state**, generated fresh every time you load the page.

When you "download as .docx," Google **generates** a new file on the spot from those database rows. That `.docx` is an export — a derivative — not the canonical document.

(I've written a separate entry on what "Google Doc = database row" really means, with concrete SQL examples. Here I just want to mark the category-level trade-offs.)

**What this category gives you:** real-time collaboration (multiple cursors, instant sync — the whole architecture is built for this). No file management. Permissions as a first-class feature. Server-side rendering consistency. Infinite version history.

**What it lacks:** offline access depends on a sync layer. Vendor lock-in is real — the canonical document only exists in the form the host renders it. No greppability without API access. Privacy/ownership concerns (the doc is on someone else's infrastructure, subject to their policies and uptime).

This category dominates wherever live collaboration is the priority: meeting notes, shared planning, anything multiple people work on simultaneously.

## All four on the same axes

Including PDF (covered in its own entry) for completeness:

| Axis | Plain text/MD/HTML | Word/.docx | Google Doc | PDF |
|---|---|---|---|---|
| **Storage form** | Bytes in a file | ZIP of XML files | Database row on server | Binary draw commands |
| **Primary goal** | Content + markup | Editable rich documents | Real-time collaboration | Frozen visual fidelity |
| **Greppable?** | Yes | Only after unzipping | Only via API | Only after extraction |
| **Diffable in git?** | Yes, line by line | No (binary) | N/A (lives in cloud) | No (binary) |
| **Pixel-perfect across viewers?** | No | Mostly | Yes (same renderer) | Yes (by design) |
| **Self-contained?** | No | Yes | No | Yes |
| **Vendor lock-in risk** | None | Low | High | None |

## The unifying idea

Each format optimises for a different **stage of a document's life**:

1. **Plain text / Markdown / HTML** — "I'm writing content I'll process with scripts or render later."
2. **Word / .docx** — "I'm authoring a rich document I want to email around."
3. **Google Doc** — "I'm collaborating live with others; the document is the conversation."
4. **PDF** — "I'm done editing; lock the visual form for distribution and archive."

A typical workflow uses several in sequence:

```
Draft in Google Doc → Export to .docx → Export to PDF
(collaborate)        (final edits)      (archive)
```

Or for technical content:

```
Write in Markdown → Render to HTML or PDF
(diffable in git)   (publish)
```

## The transferable principle

The right format is the one whose design goal matches your current need. Pushing against the format's goal is when things get painful — trying to collaborate on a PDF, trying to extract structured data from a Word doc, trying to publish a Google Doc as a permanent archive.

You can't have all of: live collaboration, pixel-perfect fidelity, self-contained portability, scriptable text manipulation, and minimal file size. The interesting question is never "is this format good?" — it's **"which axis is this format optimising, and is that the axis I need right now?"**

Once that mental model clicked, the whole document-format zoo (PDF, EPUB, DjVu, OpenDocument, Pages, Notion, Confluence, AsciiDoc, reStructuredText, LaTeX) stopped looking chaotic. It started looking like a map of trade-offs, where each tool occupies a specific niche.

---

*What I studied next: [A Google Doc is a database row, not a file](a-google-doc-is-a-database-row-not-a-file.md) — going deeper on what "cloud document" actually means at the architectural level.*
