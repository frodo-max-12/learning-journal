# SQLite vs PostgreSQL — One Architectural Fact Explains Everything Else

**Context:** I was choosing a database for a project and wanted the real comparison, not a feature checklist. What I got was better than a list: **almost every difference between the two is downstream of a single architectural choice.** Once I had that, the rest of the comparison stopped needing to be memorized — and the follow-up question, "how painful is migrating later?", turned out to have an answer that isn't about the databases at all.

---

## 1. The one fact

> **SQLite is an embedded library that runs inside your process. PostgreSQL is a separate server you talk to over a socket.**

That's it. Concurrency, type strictness, security, replication, extensions, operational burden — nearly all of it follows.

SQLite links into your binary as a C library. A query is a *function call* in the same address space: no network hop, no inter-process communication, no port, no connection string, no process to start. This is why it's the most widely deployed database engine on earth — every phone, every browser, most desktop applications, billions of live copies.

PostgreSQL runs a daemon that forks a **dedicated backend process per connection** (roughly 5–10 MB each), and clients connect over TCP or a Unix socket using a documented wire protocol. That protocol is standard enough that several other databases emulate it. The cost of the model: past a few hundred connections you need a connection pooler, because thousands of forked backends will exhaust memory.

---

## 2. What follows from it

| dimension | SQLite | PostgreSQL |
|---|---|---|
| storage | one `.db` file (plus `-wal`, `-shm`) | a data directory of many files |
| concurrency | many readers, **exactly one writer** | MVCC + row-level locking; many concurrent writers |
| type system | dynamic "type affinity" — the declared type is a *hint* | static and strict; a mismatch raises an error |
| access control | none — filesystem permissions only | roles, GRANT/REVOKE, row-level security, SSL |
| replication | none in core | streaming and logical replication, point-in-time recovery |
| server-side code | none | stored procedures, triggers, multiple procedural languages |
| extensions | a few, mostly built in | a large ecosystem — geospatial, vector, time-series |
| administration | zero config, no DBA | config tuning, vacuum, backups, monitoring |

**Concurrency is the real gap.** In WAL mode SQLite lets readers and the writer proceed without blocking each other — but there is still only **one writer at a time**, enforced by a database-level lock. A second writer gets told the database is busy and must retry. That still supports thousands of small transactions per second on an SSD, which is more than most projects ever need. But it's a hard ceiling with a shape: not "slow under load" but "serialized, by design."

Postgres uses MVCC with row-level locking, so two writers only contend if they touch *the same row*. That's the reason to reach for it the moment you have genuine concurrent write traffic from multiple processes.

**The type system difference surprised me most.** SQLite has five storage classes, and you can store a string in a column declared `INTEGER` — the declared type is advisory. Modern SQLite offers strict tables if you opt in, but the default is permissive. Postgres is strictly typed with a rich catalog — arbitrary-precision numerics, timestamps with time zones, intervals, arrays, ranges, network address types, JSON with indexing.

Coming from spreadsheets, SQLite's leniency initially felt friendly. It isn't. It means a data-quality bug can sit in the database for months without a single error, and you find it when a comparison silently does the wrong thing.

---

## 3. The histories, which explain the personalities

**PostgreSQL is 50 years of academic lineage.** Codd's relational model paper at IBM in 1970. Ingres at Berkeley in the early 70s. Then POSTGRES — "Post-Ingres" — started at Berkeley in 1986, whose explicit research goal was to go *beyond* flat relational tables with user-defined types, user-defined functions and operators, and rules. Berkeley shipped through 1994; two grad students then ripped out its original query language and bolted on SQL, producing Postgres95, renamed PostgreSQL in 1996 and community-run ever since under a permissive license.

The throughline that still matters: **every feature that makes Postgres powerful today — custom types, geospatial, vector search, custom index methods — exists because extensibility was the original 1986 research goal.** The modern superpowers are 40-year-old design intent finally paying off.

**SQLite has no academic pedigree at all.** It was written in 2000 by one engineer building software for a US Navy destroyer. His program talked to a database server, which on a warship is a liability: if the server goes down or needs an administrator to restart it, the application stops. He wanted a database with no server, no installation, no configuration, and no administrator — embedded in the program, everything in one ordinary file. So he wrote one.

That origin explains every design choice: self-contained, serverless, zero-config, single-file, and released into the **public domain** with no license at all. The public-domain status is also why the project doesn't accept outside contributions into core — they keep copyright provenance perfectly clean.

I like this pairing a lot as a case study. Two excellent pieces of software, both relational, both SQL, with almost opposite design centres — because one was asking *how do many users safely share one giant pool of data*, and the other was asking *how does one program store its data with nothing else installed*.

---

## 4. "How hard is it to migrate later?"

I asked this expecting a number. The answer reframed the question:

> **The difficulty is set almost entirely by decisions you make in the first week, not by any inherent gap between the two.**

Prepare, and migration is roughly a one-day job — a migration tool, a connection-string change, and testing. Don't, and it's a multi-week archaeology project. Same two databases, same data, an order of magnitude of difference in effort — determined by choices that cost nothing at the time.

The preparation that does the work is mostly about **not leaning on SQLite's leniency**:

- Use explicit, honest column types instead of relying on type affinity, so the strict database doesn't reject your data later.
- Don't depend on SQLite-specific behaviours in queries.
- Keep database access behind a thin layer rather than scattering raw queries through the codebase.
- Write real constraints — foreign keys, NOT NULL, uniqueness — from the start. Constraints you never declared are data problems you'll discover at migration time, at the worst possible moment.

The general principle, which I think generalizes well past databases: **"start simple, upgrade later" is only cheap if you spend the small amount now that keeps the door open.** Otherwise "we can always migrate later" is a sentence that quietly becomes false while you're not looking, and nothing warns you when it does.

---

## 5. What I took away

**Find the one architectural fact.** I'd been trying to hold a dozen differences in my head as independent facts. They're one fact and its consequences. In-process versus over-a-socket predicts the concurrency model, the security model, the deployment story, and the operational burden. That's a much better thing to remember, and it generalizes — most comparison tables have a root somewhere.

**"SQLite is the lightweight one" is the wrong frame.** It's not a smaller Postgres. It's a different *shape*: it wins on deployment and read-heavy single-writer workloads, and it doesn't compete at all on concurrent writes or multi-tenant access control, because those were never in its design goals. Choosing between them is choosing which problem you actually have.

**Origin stories are useful engineering documentation.** A research project whose stated goal was extensibility, and a field-deployment tool whose stated goal was needing no administrator. Both are still visibly true of the software today, decades later, and knowing why explains more than any feature list did.
