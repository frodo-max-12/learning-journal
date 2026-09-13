# What a Database Actually Looks Like on Disk

**Context:** I'd been shown schema diagrams — neat boxes with column names, arrows between tables — and something about them bothered me. Those are drawings. So I asked what felt like a slightly stupid question: *is it possible to see what a database actually looks like from the inside, or is that the wrong question to ask?* It's the right question, and answering it produced a five-layer walk from raw bytes up to the diagram, plus the reason the word "schema" means what it does.

---

## Level 1 — the physical reality

At the bottom, **a database is just files on a disk.** Nothing magical.

Create a database and the engine makes a directory that looks roughly like this:

```
/var/lib/postgresql/data/
└── base/
    └── 16384/          ← your database — just a numbered folder
        ├── 24576       ← one table — just a file
        ├── 24577       ← another table
        └── ...
```

**Each table is literally a file.** Not a metaphor. And the contents are binary — open one in a text editor and you get `\x00\x03\x8f\xa2...`.

Why binary rather than something readable like CSV? Speed. There's no parsing step, and fixed-width binary fields can be located by arithmetic rather than by scanning for delimiters.

Inside each file, data is organized into **pages** — fixed-size blocks, typically 8 KB:

```
File: 24576 (one table)
┌──────────── Page 0 (8 KB) ────────────┐
│ Row 1: {...}                          │
│ Row 2: {...}                          │
│ ... more rows until the page is full  │
├──────────── Page 1 (8 KB) ────────────┤
│ Row 47: {...}                         │
└───────────────────────────────────────┘
```

So `SELECT * FROM t WHERE role = 'x'` means: read through these pages, check every row, return the matches. **That's a full table scan** — a worker walking a warehouse opening every box.

The 8 KB figure isn't arbitrary, which is the part I like. It's there because **the disk and the operating system move data in blocks**, so the database matches its unit to the unit underneath it. Reading one row costs the same as reading the page containing it, and every layer above inherits that fact.

---

## Level 2 — indexes, the speed trick

Full scans are fine until the table is large. An index is the fix, and the analogy is exact: **the index at the back of a textbook.** Rather than reading every page looking for a word, you flip to the index and it tells you which pages to turn to.

An index on a column is stored as a **B-tree** — a sorted structure you can descend in a few steps rather than scanning linearly.

```
Without an index: scan every page.
With an index:    jump straight to the right location.
```

Which finally made concrete why indexes are a *trade* rather than free speed. The index is **another structure on disk** — more files, more pages. It has to be updated on every insert and every update. You're buying read speed with write cost and storage, and that's why nobody indexes every column.

---

## Level 3 — the engine

Between the files and your query sits the **database engine** — the software doing the actual work. Six jobs:

1. receive the query
2. **plan the route** — use an index or not? which one? in what order to join?
3. fetch from disk or memory
4. **enforce the rules** — foreign keys, types, uniqueness
5. **handle concurrency** — many writers at once without corruption
6. return results as a neat table

PostgreSQL, MySQL, SQLite are all engines. And a hosted platform you talk to over an API is usually an engine with layers on top — your code hits the service, the service runs SQL against the engine, the engine manages binary files.

Point 2 is the one worth dwelling on: **the engine decides how to answer, you only say what you want.** That's the deal SQL makes. You write a declaration of the result you want; something else picks the strategy. It's why the same query can be fast today and slow next month if the data distribution shifts — the plan changed, not your code.

---

## Level 4 — the abstractions, and which is "real"

Here's where it connects back to the diagrams that started the question. There are several ways to look at the same data, and they are **not** the same kind of thing:

**a) The schema diagram** — boxes with column names, arrows between tables. This is the **architect's blueprint.** It shows design intent: what tables exist, what columns they hold, how they relate. Drawn by humans, for humans, usually before any data exists.

> **No database actually looks like this. It's a communication tool.**

That sentence answered my original question. I'd been half-suspecting the diagram was a picture of a real internal structure. It's a picture of an *intention*.

**b) The result table** — flat rows and columns, like a spreadsheet, when you actually query. This is the human-readable *rendering* of those binary pages.

**c) The GUI** — a web or desktop app showing the same data as an editable grid. Underneath it's running SQL against the engine against the files, which is exactly what the query log in such a tool shows you if you look.

---

## The etymology, and the idea underneath it

**"Schema" comes from Greek σχῆμα (*skhēma*) — "shape, form, figure, plan."**

It entered database terminology in the 1970s through **Edgar Codd**, who invented the relational model, and his key insight was this:

> **Separate the logical structure (the schema) from the physical storage. SQL is the bridge between them.**

That's the thesis the whole five-layer stack exists to serve, and it reframes everything above it. Levels 1 and 2 are *physical*. Level 4 is *logical*. The engine at Level 3 is the machinery that keeps the two independent — so you can add an index, change the page layout, or move to different hardware without a single query changing.

It also retroactively explains things I'd learned separately and filed as unrelated facts:

- **A table has no inherent row order.** Order is a physical property of pages at Level 1 and simply doesn't exist at Level 4, which is why you must impose it with `ORDER BY` every time you read.
- **Why the declarative style works at all.** You can describe a result rather than a procedure precisely because Codd's separation means the *how* is not your concern.
- **Why "SQL" and "PostgreSQL" are different kinds of noun** — a language versus an engine that speaks it, which is the same logical/physical split showing up in the vocabulary.

---

## What I took away

**A table is a file. That's the fact I was missing**, and everything else became easier once I had it. Pages, indexes, scans, and query plans all follow from "this is bytes on a disk, organized into blocks."

**The diagram was never a picture of the thing.** I'd been treating a blueprint as a photograph. Knowing which representations are *design intent* and which are *rendered data* stops a whole class of confusion — and it's the same distinction as source code versus a running process.

**The most important idea in the relational model is a separation, not a structure.** Not tables, not keys, not SQL — the decision to make the logical description independent of the physical storage. Tables and SQL are what that decision made possible, and fifty years of storage changing underneath while the queries stayed the same is the evidence it was the right call.
