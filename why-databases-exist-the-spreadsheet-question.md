# Why Databases Exist — Asking What a Spreadsheet Can't Do

**Context:** I had a matching problem — a list of things wanted on one side, a list of things available on the other, pair them up where they're compatible and rank by value. I was about to build it in a database, and stopped to ask a question I actually wanted answered: **why couldn't I just do this in Google Sheets?** Not rhetorically. I wanted to find the exact point where the spreadsheet breaks, because that point is the reason databases were invented.

---

## 1. Doing it in a spreadsheet

You'd make three tabs mirroring three tables — one row per request, one row per available offer, and a third where the pairings are supposed to land. The match is: *for each request, find offers for the same item where the price works and the quantity covers it.*

Reaching for the obvious tools:

- **`VLOOKUP` / `XLOOKUP`** returns only the **first** match. If an item has five offers, you see one and silently miss four. Not an error — just a wrong answer that looks like a right answer.
- **`FILTER`** gets all offers for one request. Better. But now each request spills a different number of rows, and you have to hand-arrange a grid whose shape changes every time the data changes.
- Then you bolt on columns for margin, sorting, deduplication — each a formula dragged down thousands of rows, recalculating on every keystroke.

And here's the honest part: **for 20 requests and 30 offers, this works fine.** You eyeball it and move on. The spreadsheet is not a bad tool; it's a tool with a scale.

---

## 2. The same thing as one query

```sql
SELECT d.id AS demand_id, s.id AS supply_id, d.item_key,
       s.price  AS buy,
       d.target AS sell,
       (d.target - s.price) * min(d.qty, s.qty) AS margin
FROM   demand d
JOIN   supply s ON d.item_key = s.item_key
WHERE  s.price < d.target
  AND  d.status = 'open'
ORDER  BY margin DESC;
```

That `JOIN ... ON` **is** the matching engine. It pairs every open request with every viable offer for the same item, computes the value, and ranks — across the whole table, every time you run it.

The contrast is the whole answer to my question. Five specific things break in the spreadsheet the moment this stops being a toy.

---

## 3. The five things

**1. The join is native, not faked.** "Pair every row on the left with every compatible row on the right" is the single most common database operation, and it has a name and an implementation. A spreadsheet's native unit is *a cell in a grid* — the join is something you rebuild by hand out of lookups, and the built-in lookup hands you one row when you need all of them.

The realization that stuck: my "matches" tab, with its two columns pointing back at the source tabs, is literally a **stored join**. I'd been hand-computing something the other tool does as a primitive.

**2. Integrity is enforced.** The database refuses to let a match point at a request that doesn't exist, refuses a null key, refuses a duplicate id. A spreadsheet won't stop you typing `STM32F407` in one tab and `stm32f407` in another — now they don't match, silently — or deleting a row that three other rows still reference.

At thousands of rows that rot is *guaranteed*, not likely. And it's the actual reason you normalize a key column at all: the database makes that column do real work, and tells you when the work fails.

**3. Speed at scale.** Spreadsheets crawl in the tens of thousands of rows and hard-cap not far above that. A database keeps an **index** on the join key, so the match is found in milliseconds across millions of rows instead of scanning every one. The index is *why* the query stays fast, and it's the thing with no spreadsheet equivalent.

**4. Many writers at once.** If an ingestion job, a matcher, and a report generator all touch the same data, some on a schedule, a database serializes concurrent writes with transactions. Two processes editing the same spreadsheet clobber each other.

**5. All-or-nothing operations.** "Insert the match *and* flip the request's status *and* create the follow-up record" must either all happen or none happen. That's a transaction. In a spreadsheet, a crash between step two and step three leaves you in a state your logic thinks is impossible — and nothing tells you.

---

## 4. Keys, and what a foreign key actually is

Chasing this made me ask what a foreign key really is — a special kind of column, or just an ordinary column with a note attached? The answer is a clean two-layer distinction.

**Layer 1 — the column is completely ordinary.** It's an integer or a text column like any other. Nothing special about its storage.

**Layer 2 — the constraint is a rule the engine enforces.** Declaring it a foreign key registers a rule in the schema: *every non-null value in this column must exist in that column of that table.* The engine checks it on every insert and update, and refuses the write if it fails.

So my instinct was almost right, and the correction is precise: it's **not a note, it's a rule.** A comment describes intent and permits violations. A constraint makes violations impossible. That's the whole difference between documentation and integrity, and it's why "we'll just be careful" never works — carefulness is a comment.

The same two-layer pattern explains a **primary key** (a uniqueness-and-not-null constraint, plus an automatic index) and explains why deleting a referenced row either fails or cascades: the engine is enforcing a promise you made when you declared the schema.

Which is also the answer to "what *is* a schema?" It's not a description of the data. It's **the set of promises the engine will enforce about the data** — the difference between a shape your data happens to have and a shape it cannot escape.

---

## 5. The history, and a coincidence I liked

Then I got curious about which came first, the spreadsheet or the relational database. The answer is more lopsided than I expected:

| year | what |
|---|---|
| ~1963 | the first database management system — navigational, you wrote code to walk pointers between records |
| 1966–68 | hierarchical databases, built for the Apollo program |
| **1970** | **Codd's relational model** — the paper |
| 1973–74 | SQL invented at IBM; Ingres at Berkeley |
| **1979** | **VisiCalc** — the first spreadsheet — *and* the first commercial relational database |
| 1983–87 | Lotus 1-2-3, then Excel |

**Idea to idea, the database is about nine years older.** Databases in general go back further still, to the mid-1960s.

But the coincidence is 1979: the spreadsheet shipped the *same year* as the first commercial relational database. The theory had a decade's head start; the shrink-wrapped products ordinary people could buy arrived simultaneously.

And the deeper thing hiding in the dates is that these came from **opposite worlds**. Codd's database was corporate mainframe research asking *how do many users safely share one giant pool of data*. VisiCalc was one person on a personal computer who wanted *his own numbers to recalculate without a pencil*.

Shared-and-structured versus personal-and-ad-hoc. That split was baked in at birth, and it is exactly the tension I was feeling when I asked "why not just a spreadsheet?" I wasn't inventing a question — I was standing on a fault line that's been there since 1979.

---

## 6. What I took away

**The right question was "where does it break," not "which is better."** Every one of the five failures has a threshold. Below it the spreadsheet is genuinely the better tool — faster to build, visible, no setup. Above it the spreadsheet doesn't get slow, it gets *quietly wrong*, which is worse. Knowing the thresholds is more useful than a preference.

**Silent wrongness is the real argument.** Four of the five failures — first-match-only lookups, inconsistent keys, clobbered concurrent edits, half-completed multi-step updates — produce *plausible output*. No error, no warning. That's what a database buys: not speed exactly, but the conversion of silent wrongness into loud failure.

**Constraints are the feature, not the ceremony.** I'd read schema design as bureaucracy you do before the interesting part. It's the opposite — it's where you write down what must be true, so that the machine, and not your attention, is responsible for keeping it true.
