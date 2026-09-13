# Trigram Matching, and When Vector Search Isn't Worth It

**Context:** I was choosing a database and reasoning that I should pick the more powerful one so that vector search would be available if I ever wanted "find similar items." The advice I got pushed back in an unexpected direction: the feature I'd actually fall in love with wasn't vector search, it was **trigram matching** — a much older, dumber technique that solves the problem I actually had. Then I pushed back on *that*, and got a correction to the correction, which is the part worth writing down.

---

## 1. The problem: matching strings that should be the same

The real task was matching product part numbers. The same physical part shows up written as `MT40A1G16TB-062E IT:F`, `MT40A1G16TB062E`, `mt40a1g16tb-062e`, and half a dozen other ways — different whitespace, different separators, different case, occasional typos.

"Find the record that means the same thing as this string" *sounds* like a semantic-similarity problem, which is why my mind jumped to embeddings. It isn't. It's a **surface-form** problem: the strings are nearly identical as sequences of characters, and the differences are punctuation and case rather than meaning.

Naming that distinction is most of the answer, and I'd skipped it.

---

## 2. What trigram matching does

Decompose each string into overlapping three-character sequences, then score similarity as **the fraction of trigrams two strings share**.

`MT40A1G16TB` becomes `MT4`, `T40`, `40A`, `0A1`, `A1G`, … Drop a hyphen or change the case and the *overwhelming majority of trigrams survive unchanged*. Similarity stays near 1.

That's the entire idea, and it's why it fits this problem exactly: trigram overlap is a direct measure of *how much the character sequences agree*, which is precisely what varies between the spellings of one part number.

In PostgreSQL it's an extension, and the ergonomics are genuinely nice:

```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX parts_pn_trgm ON parts USING GIN (pn gin_trgm_ops);

-- graded similarity, 0.0 to 1.0
SELECT pn, similarity(pn, 'MT40A1G16TB-062E') AS sim
FROM parts
WHERE pn % 'MT40A1G16TB-062E'          -- '%' means "trigram similar"
ORDER BY sim DESC LIMIT 5;

-- nearest neighbours by distance operator
SELECT pn FROM parts ORDER BY pn <-> 'MT40A1G16TB' LIMIT 5;

-- and it accelerates leading-wildcard LIKE, which normally can't use an index
SELECT pn FROM parts WHERE pn ILIKE '%40A1G16%';
```

That last one is a small marvel on its own. `LIKE '%foo%'` normally can't use a B-tree index at all, because a B-tree is sorted by prefix and a leading wildcard destroys the ordering. A trigram index sidesteps that: it indexes *fragments*, so an interior substring is just another set of trigrams to look up.

---

## 3. Why not vector search?

Embeddings are exciting and, for this job, the wrong tool. The costs are real and recurring:

- **You have to embed first** — every record, and every query at query time.
- **You have to re-embed when the model or taxonomy changes**, which means the index has a maintenance schedule attached to something outside your control.
- **You have to tune approximate-nearest-neighbour parameters** and accept approximate results.
- **You get a similarity you can't fully explain** — "these are 0.87 similar" with no account of *why*.

Against that, trigram similarity is exact, explainable (you can literally count the shared trigrams), needs no model, and has one index to maintain.

The rule I extracted:

> **Vector search earns its cost when the strings differ in *meaning* but not in *characters*. Trigram matching wins when the strings differ in *characters* but not in *meaning*.**

"Laptop" and "notebook computer" share almost no trigrams and need embeddings. `MT40A1G16TB-062E` and `mt40a1g16tb062e` share nearly all their trigrams and need nothing clever at all.

So trigram matching is the workhorse for the large majority of "find similar" lookups on identifier-like data, and vector search becomes the specialist tool for the minority that are genuinely semantic.

---

## 4. The correction — I pushed back and was half right

My follow-up was: does the simpler embedded database have this too? If it does, the argument for the heavier one weakens considerably.

**It does.** SQLite has had trigram-based search since 2020, as a tokenizer inside its full-text-search module. The initial framing had oversimplified by implying this was a Postgres-only capability.

But the two are **different shapes of the same idea**, and the difference is worth being precise about:

| | Postgres extension | SQLite FTS trigram |
|---|---|---|
| setup | one extension + an index on a normal column | a virtual table plus triggers to keep it in sync |
| numeric similarity score | yes — `similarity(a,b) → 0.73` | no native equivalent; a relevance rank instead |
| `ORDER BY` closeness | trivial, via a distance operator | indirect, and the ranking means something different |
| accelerated `LIKE '%…%'` | yes | yes — a genuine tie |
| fuzzy self-joins (dedup a table against itself) | one query with a similarity threshold | multi-step: match, then count shared trigrams in application code |
| composes with other extensions | naturally — accent-stripping, case-insensitive types | you normalize yourself before tokenizing |

**The biggest real gap is the numeric similarity score.** For a workflow like *"auto-merge if similarity > 0.85, otherwise flag for a human"*, one system expresses that directly in SQL and the other requires either computing the score yourself afterwards or accepting a coarser yes/no.

The second gap is structural: an index on a normal column versus a **separate virtual table you must keep synchronized with triggers**. The capability is comparable; the maintenance burden isn't.

So my pushback was right that the feature exists in both, and the honest conclusion is narrower than either of the framings I started with: **the capability is not a differentiator, but the ergonomics around thresholds and self-joins are.**

---

## 5. What I took away

**Classify the difference before choosing the tool.** Surface-form variation and semantic variation look like the same problem — "these should match but don't" — and have completely different solutions. Asking *which kind of difference is this?* would have gotten me to the answer without any of the reasoning about database features.

**A cheap technique that fits beats a powerful one that doesn't.** Trigram matching is decades old, has no model, and needs no tuning. For identifier matching it's not a compromise — it's the *correct* tool, and the sophisticated alternative would be worse along every axis that matters here.

**Push back on advice, including advice that corrected you.** The initial framing was directionally right and imprecise on one point. Asking the obvious follow-up produced a sharper answer than either the original claim or my objection. The final position — same capability, different ergonomics — is one neither of us stated at the start.
