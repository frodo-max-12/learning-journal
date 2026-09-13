# Redis — a Data-Structure Server, Not a Cache

**Context:** I kept seeing Redis described as "a fast cache," which is true and misses the design idea entirely. Asking what it actually is produced a conceptual distinction I hadn't seen before, and it changed how I think about the boundary between a database and an application.

---

## 1. The core idea, in one comparison

Most databases give you:

```
key → opaque blob
```

You serialize your object, store it, deserialize on read. The database has no idea what's inside.

Redis gives you:

```
key → typed data structure
```

The value isn't a blob. It's a string, a list, a hash, a set, a **sorted set**, a stream, a bitmap, a probabilistic cardinality counter, or a geospatial index — and **the server understands the structure and offers operations on it.**

The consequence is the whole philosophy. Instead of:

```
GET user:123  →  deserialize  →  append to list  →  serialize  →  SET user:123
```

you do:

```
LPUSH user:123:feed "new_item"
```

One operation. Atomic. Constant time. No read-modify-write round trip.

That read-modify-write cycle is where a surprising amount of real-world trouble lives: it's slow (two network round trips plus serialization), and it's a **race condition** — two clients doing it concurrently, one silently overwrites the other. Making the server understand the structure eliminates both problems at once.

The name that captures it: **an in-memory data-structure server**, not a cache. Caching is the most common thing people use it for, and it's an application of the design rather than the design.

---

## 2. Why it's fast — including one choice that looks wrong

- **In-memory primary storage.** RAM rather than disk, so sub-millisecond latency for most operations.
- **Written in C**, very tight. Six figures of operations per second from a single instance is unremarkable; pipelined workloads reach millions.
- **A single-threaded event loop** for command execution.

That last one stopped me. Single-threaded sounds like a limitation you'd apologize for. It's a deliberate trade, and a good one:

**Single-threaded execution eliminates locking entirely, and makes every command atomic by construction.**

No mutexes, no lock contention, no deadlocks, no torn reads — not because they're carefully handled but because the situation that produces them never occurs. Commands execute one at a time, in order.

That's the same shape as several other good designs I've run into: **remove the possibility of a class of bug rather than defending against it.** A single writer is exactly why SQLite's concurrency model is what it is, too — and both are choosing a hard structural guarantee over a soft, faster, more error-prone one.

The cost is real: one core executes commands, so a single instance can't use a whole machine for command processing. The answer is to run more instances, which is a cost you can pay with hardware rather than with correctness.

---

## 3. "In-memory" doesn't mean "lost on restart"

The persistence story is a genuine spectrum you choose from:

- **Periodic binary snapshots** — fork the process and write the dataset to disk at intervals. Fast, and you lose whatever happened since the last snapshot.
- **An append-only log** — every write is recorded and replayed on restart, with a configurable sync policy: sync on every write (safest, slowest), every second (the usual compromise), or leave it to the OS (fastest, loses the most on a crash).

What I like about this is that the durability trade-off is **explicit and tunable** rather than hidden. Most systems make one durability choice and bury it. Here it's a setting, and you're expected to know which one you picked.

The append-only log is also the same idea as the JSONL prompt history I'd looked at elsewhere: an append-only record of operations, crash-safe because appending is atomic in a way that rewriting isn't, replayed to rebuild state.

---

## 4. What people actually use it for

The list is more varied than "cache," and each use exploits a specific data structure:

| use | how |
|---|---|
| cache in front of a database | with expiry times and eviction policy — the most common role by far |
| session storage | short-lived keyed state |
| rate limiting | atomic increment plus expiry, which is the entire implementation |
| leaderboards | sorted sets give ranked queries in logarithmic time |
| job queues | push and blocking-pop, or streams with consumer groups |
| publish/subscribe | fan-out messaging |
| distributed locks | set-if-not-exists with a timeout (with genuine caveats) |
| real-time analytics | probabilistic counters for cardinality, bitmaps for cohorts |

The rate limiter is my favourite because it's the clearest demonstration of the thesis. "Increment a counter and expire it after a window" is *two operations and no application logic*, and it's correct under concurrency because the server executes commands atomically. Implemented against a blob store, the same feature is a read-modify-write race you have to think hard about.

---

## 5. Scaling, and where it gets awkward

- **Replication** — asynchronous copies of the primary, used for read scaling and failover.
- **A monitoring layer** that watches primaries and automates failover.
- **Cluster mode** — keys sharded across nodes via a fixed number of hash slots, giving roughly linear horizontal scale.

And the honest limitation: **cross-shard operations get awkward.** Once your keys live on different nodes, anything spanning them loses the atomicity that made the single-threaded model attractive. The property that makes it elegant at one node is exactly the property that's hard to preserve across many.

That's a recurring shape too. Single-writer simplicity is wonderful and doesn't distribute for free; the guarantees you get from "one thing does it all, in order" are the guarantees that sharding takes away.

---

## 6. The cultural note, which is a design lesson

The original author was famously opinionated about keeping the codebase **small and readable** — the whole thing is on the order of 50,000 lines of C — and routinely declined contributions that added complexity.

That's a real engineering position, not a personality quirk: it stayed fast and stable *while becoming infrastructure a large fraction of the internet depends on*, and the two facts are connected. A small codebase you can hold in your head is one where a performance regression is visible and a subtle concurrency bug has nowhere to hide.

The later licence change was contentious enough that major cloud providers forked it under a permissive licence, and the fork has significant momentum. Worth knowing as an instance of a pattern: infrastructure that becomes load-bearing eventually has a governance problem, and "who controls the licence" turns into a serious question the moment other people's businesses depend on it.

---

## 7. What I took away

**The distinction between a blob store and a structure server is the whole idea**, and it generalizes: when the server understands your data's shape, operations that would be read-modify-write races become single atomic commands. That's a reason to push a *little* logic into the data layer — not business rules, but the structure-manipulating primitives.

**Single-threaded can be a feature.** Removing concurrency removes an entire category of bug for free. Whether that's a good trade depends on whether you can scale by running more instances — and often you can.

**Explicit durability settings are better than good defaults.** Being made to choose between snapshot and log, and between sync policies, means I know what I'd lose in a crash. Most systems make that choice for me and don't tell me what it was.
