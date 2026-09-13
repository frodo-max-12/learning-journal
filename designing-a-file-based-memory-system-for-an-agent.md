# Designing a File-Based Memory System for an Agent

**Context:** I'd been using an agent's memory feature for months without knowing how it worked. Then I edited a memory file, was asked whether I wanted a "frontmatter block" added, and had to admit I didn't know what that was. Chasing it turned into something more useful than a definition — it's a small, well-shaped answer to a real design problem: **how do you give a stateless system persistent memory when the thing memory competes for is scarce?**

---

## 1. The problem being solved

A model is stateless. Each conversation starts cold. Without persistence, you re-establish the same context every single time — who you are, what you're working on, what corrections you've already made.

The naive fix is to load everything you know into every conversation. That fails immediately: context is finite, and everything you load competes for attention with the actual task. A large enough memory would crowd out the work it was meant to support — and since attention dilutes well before any hard limit, it degrades quality long before it errors.

So the real problem is: **persistent recall on a fixed, small always-loaded budget.**

---

## 2. The three layers

**Layer 1 — the index.** One file, always loaded into every conversation. It's just a list of one-liners:

```
- [some-memory.md](some-memory.md) — one-line hook describing what's inside
```

It stays deliberately small — around 150 characters per line — so it never blows the context budget.

**Layer 2 — the memory files.** Individual markdown files on disk, each with frontmatter plus a body. **These are not auto-loaded.** They sit on disk until needed.

**Layer 3 — on-demand reads.** When something in the current conversation matches a memory's line in the index, that specific file gets opened and pulled into context.

The flow: every conversation starts with a cheap index of *all* memories → scan for relevance → read only the files that matter. Dozens of memories can exist while only a handful enter any given conversation.

This is the same **progressive disclosure** pattern as extension definitions — index eagerly, content lazily, make the index entry good enough to route on. Seeing one architecture solve two different problems in the same system is what convinced me it's a real pattern rather than an implementation detail.

---

## 3. Frontmatter, and why the description is the load-bearing field

Frontmatter is the metadata block at the top of a markdown file, fenced by `---`:

```
---
name: short-human-label
description: one-line hook used to decide if this is relevant
type: user | feedback | project | reference
---
```

It's YAML key/value metadata, a convention inherited from static-site generators — content below is the body, metadata above is data *about* the document.

Of the three fields, **`description` is the one doing real work.** It's what gets matched against the current conversation to decide whether to open the file.

Which produces the failure mode worth designing against: **a vague description means the memory is silently never used.** Nothing errors. The file exists, is correct, is well-written, and never surfaces. You conclude the feature doesn't work when what actually happened is that the routing key was too weak to route on.

That reframes description-writing entirely. It isn't documentation, it's a **retrieval key** — and it should be written by asking *what would I be saying, in some future conversation, when this file should appear?*

---

## 4. The four types, and why the taxonomy earns its place

Memories are typed, and the categories aren't decorative — they answer different questions:

| type | what it holds | why it's separate |
|---|---|---|
| **user** | who the person is, background, how to pitch explanations | changes rarely; shapes *how* everything else is delivered |
| **feedback** | corrections and confirmed approaches | prevents repeating a mistake already corrected |
| **project** | current work, goals, decisions, constraints | high churn; goes stale fastest |
| **reference** | pointers to external resources and locations | mostly stable; pure lookup |

The useful thing about the split is that the types have **different decay rates and different failure modes.** A stale `project` memory is actively harmful — it asserts something no longer true. A stale `reference` is merely useless. A `feedback` memory that's missing produces a repeated mistake; a `user` memory that's missing produces a mismatched explanation.

Tagging by type gives you a maintenance schedule for free: audit `project` often, `reference` when something breaks, `user` and `feedback` rarely.

---

## 5. The two-tier description problem

Then a genuinely interesting design question came up: should the index line and the file's own description say the same thing?

**Loosely yes — but exact match isn't the goal, because they do different jobs.**

- The **index line** is always loaded, and it competes with every other line for attention. It's the **triage layer**. It has to be punchy and short.
- The **frontmatter description** lives inside the file. It's read once you've already decided to open it, or when something else surfaces it. It can afford to be longer and more precise.

So the index line should be a **compressed teaser** of the frontmatter description — same topic, same key signals, tighter. They must *agree* about what the memory is about, so neither misleads, but the index line is allowed to be shorter and more colloquial.

The thing that makes this more than housekeeping: **the two descriptions are optimized against different constraints.** One is competing for scarce attention against 40 siblings; the other has the reader's full attention already. Writing one text and using it in both places means it's wrong for at least one of them.

That's a general shape I now recognize — the same content needs different compressions at different stages of a retrieval funnel. A search result snippet and the page it points to are the same relationship.

---

## 6. What this buys, stated concretely

- **Continuity across sessions** — long-running context persists without re-explanation.
- **Behavioural consistency** — feedback memories stop the same correction being needed twice.
- **Cheap context** — only the relevant handful of files load, not all of them.

The middle one is the one I'd underrated. It's the difference between a tool that's *informed* and a tool that's *trained by use* — a correction given once becomes permanent rather than evaporating with the session.

---

## 7. What I took away

**"How do I make this persistent?" is really "what's my always-loaded budget, and what goes in it?"** Any system with a scarce always-on tier and a large cold store needs the same three layers: a cheap index, cold content, and a rule for promoting content on demand. Filesystems, databases, and CPU caches all have this shape.

**A retrieval key is a different artifact from a description.** I'd have written these summaries for a human reader. They're written for a matching step, and the question that produces a good one is "what would someone be saying when this should surface?"

**Silent non-retrieval is the failure mode to design against.** Nothing in this system errors when it's badly configured — it just quietly does less than it could. Those are the failures worth building explicit checks for, since nothing else will tell you.
