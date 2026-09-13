# Where Relational Databases Struggle — and the Four Kinds of NoSQL

**Context:** Having learned enough SQL to design a schema, I wanted to know the shape of the thing I'd chosen: what relational databases are *bad* at, and what the alternatives actually are. "NoSQL" turned out not to be one thing at all — it's four quite different designs that share only what they gave up, and each one is legible once you know which relational limitation it was built to escape.

---

## 1. Three places the relational model strains

**Scale.** A single server has a ceiling. Spreading across a hundred machines is hard specifically because **joins across tables on different servers are expensive** — the operation that makes the relational model powerful is the one that resists being distributed.

**Varying structure.** Every row in a table has the same columns. But suppose one counterparty needs a regional messaging ID, another a tax registration number, a third a VAT identifier. In a strict schema you either add a column that's null for almost everyone, or you build a side table, or you stuff a blob in a text field.

**Deeply nested data.** Some data is naturally tree-shaped — category inside category, comment replying to a reply. Tables model that awkwardly, usually with a self-referencing key and a recursive query.

Worth noticing: **all three are consequences of the same choice.** The fixed schema and the join are what buy you integrity and expressive queries, and they're what cost you flexibility and easy distribution. It's one trade seen from three angles.

---

## 2. What "NoSQL" actually means

Originally "No SQL," now usually read as **"Not Only SQL."** In the mid-2000s the companies that hit relational limits at genuinely large scale built new systems, each trading away some relational feature — strict schemas, joins, or strong consistency — for something they needed more.

Which reframes the category. **NoSQL is not "a newer kind of database." It's a set of systems defined by which guarantee they abandoned.** So the useful question about any of them is never "is it better?" — it's *what did this one give up, and do I need that thing?*

---

## 3. The four types

### Document databases

Store everything about one entity as a single JSON document:

```json
{
  "id": "abc123",
  "company": "Example Components Ltd",
  "region_messaging_id": "...",
  "listings": [
    { "part": "STM32F103C8T6", "quantity": 10000, "price": 2.40 },
    { "part": "LM7805CT",      "quantity": 5000,  "price": 0.35 }
  ]
}
```

Every document can have different fields, so the varying-structure problem disappears. Reading one entity is a single fast lookup, and documents shard cleanly across machines because each is self-contained.

**Given up:** joins, and with them a lot of integrity. The nested listings are duplicated data — update a part name and you touch every document containing it, with nothing enforcing that you did.

### Key-value stores

The simplest possible database: a key maps to a value.

```
"session:user:abc123"    →  "{logged_in: true, role: ...}"
"cache:part:STM32F103"   →  "{price_avg: 2.35, suppliers: 47}"
```

Usually in memory, millions of operations per second. Caching, sessions, rate limiting.

**Given up:** essentially all querying. You cannot ask "which sessions are admins" — you can only fetch a key you already know. Which is why this is a **supplement to a main database rather than a replacement**, and why the one I looked at closely is best understood as a data-structure server rather than a cache.

### Column-family stores

Group data by column rather than by row. Computing an average across a billion readings touches only the temperature column and skips everything else.

That's the whole idea, and it explains the use cases immediately: event streams, sensor data, financial ticks — **write once, aggregate over one dimension, at enormous volume.**

**Given up:** typically strong consistency, in exchange for staying available while partitioned.

### Graph databases

Data as **nodes** and **edges**:

```
(Buyer)──[PLACED]──→(Request)──[FOR_PART]──→(STM32F103)
                                    ↑
                              [SUPPLIES]
                                    │
                             (Supplier)
```

Relationships are first-class objects rather than foreign keys resolved at query time. Excels at questions that are painful in SQL: shortest path, friends-of-friends, "who else carries similar parts."

**Given up:** the tabular model, and much of the tooling ecosystem that assumes it.

---

## 4. Side by side

| | relational | document | key-value | column-family | graph |
|---|---|---|---|---|---|
| structure | strict tables | flexible documents | key → value | column families | nodes and edges |
| best at | transactions, relationships | varied, nested data | speed, caching | analytics, time series | relationship queries |
| schema | fixed, enforced | flexible | none | semi-structured | flexible |
| transactions | full | partial | none, by design | eventually consistent | yes |

The row that matters most is the last one. **Every alternative to relational weakened transactional guarantees somewhere**, and that's the thing to check first, because it's the one you cannot add back in application code without effectively rebuilding a database.

---

## 5. The distinction I'd been missing: language versus engine

A smaller confusion this cleared up, which was blocking me for a while.

**SQL is a language. PostgreSQL is an engine that speaks it.** SQLite is another. MySQL is another. They implement overlapping dialects of the same standard, which is why a query moves between them with small edits and why "learning SQL" transfers across all of them.

Once that was straight, "NoSQL" stopped sounding like a rejection of a language and started meaning what it does: **these systems don't organize data as relations, so the relational query language mostly doesn't apply** — though several have since added SQL-like layers, which is why "Not Only SQL" became the preferred reading.

---

## 6. What I took away

**Every alternative is defined by what it abandoned.** Documents gave up joins. Key-value gave up querying. Column-family gave up strong consistency. Graph gave up tables. Learn the sacrifice and the use case is obvious; learn the feature list and nothing is.

**The relational trade-off is one choice, not three weaknesses.** Fixed schemas and joins buy integrity and expressive queries, and cost flexibility and distribution. Complaining about the cost while wanting the benefit is wanting a different database.

**And the default is still relational for most things.** All three limitations bite at a scale most projects never reach, while the guarantee they trade away — that the database enforces what must be true — is valuable from the first row. Which is the same conclusion I reached from the other direction when I asked why databases exist at all instead of a spreadsheet: **the enforcement is the product.**
