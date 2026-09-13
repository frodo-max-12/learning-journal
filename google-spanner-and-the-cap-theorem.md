# Google Spanner and the CAP theorem

---

## What Spanner is, in one line

**Spanner** is a database Google built that gives you SQL with full ACID transactions, runs across data centres on multiple continents, with strong consistency and high availability. Until Spanner existed, the conventional wisdom said this combination was impossible. The way Spanner pulled it off involves GPS receivers, atomic clocks, and one of the more elegant pieces of distributed-systems engineering I've come across.

Worth understanding because (a) it underlies a huge amount of Google's infrastructure, including the database behind Google Docs, (b) it inspired a generation of open-source databases (CockroachDB, YugabyteDB, TiDB) that anyone can use today, and (c) the story illustrates a principle that generalises far beyond databases.

## The problem Spanner was built to solve

By 2008, Google had two kinds of database systems internally, and neither was good enough.

1. **Traditional relational databases** (MySQL-style): great for transactions, joins, SQL. But they ran on a single machine. To scale, you had to *shard* — split data across machines — and once you did, you lost cross-shard transactions, lost cross-shard joins.

2. **Bigtable** (Google's own NoSQL system, inspiration for HBase, Cassandra, DynamoDB): scaled to thousands of machines. But sacrificed consistency for "eventual consistency," and had no real transactions, no SQL, no joins.

The AdWords team — billions of dollars of business — needed both. Transactional correctness (can't double-charge an advertiser) AND global scale (data on multiple continents for latency and disaster recovery). The conventional wisdom, captured in something called the **CAP theorem**, said this was impossible.

## The CAP theorem in 30 seconds

CAP says any distributed data system can guarantee at most two of three properties:

- **C**onsistency — every read returns the most recent write.
- **A**vailability — every request gets a response, even during failures.
- **P**artition tolerance — the system keeps working when the network drops messages between nodes.

In practice, network partitions *will* happen (cables get cut, routers fail), so you really have to pick between C and A. NoSQL databases like Cassandra and DynamoDB famously chose A — "we'll always respond, but the data might be slightly stale." Traditional databases chose C — "we'll be correct, but if we can't reach the other shards, we just won't respond."

Google needed both. The textbook answer: tough luck.

## Spanner's insight: the real obstacle is clocks

Here's the deep observation. The reason transactional consistency across a globally distributed database is so hard is that **you can't agree on what "now" means** across machines 100ms apart.

If a transaction commits in Tokyo at "10:00:00.000" and another in Frankfurt at "10:00:00.001," which happened first? You can't trust wall-clock time on either machine — computer clocks drift, sometimes by seconds. So databases historically used logical clocks (counters that increment with each operation), which work within a single shard but break across shards.

The Spanner team asked: **what if we made the clocks reliable enough to just use wall-clock time?**

To do this, they put physical hardware in every Google data centre:

- **GPS receivers** on the roof, pulling time from GPS satellites (which carry atomic clocks).
- **Atomic clocks** as backup, in case GPS reception fails.
- Multiple of each, cross-checking.

Then they built an API called **TrueTime** that exposes time as an interval, not a single value:

```python
now = TrueTime.now()
# Returns: {earliest: "10:00:00.000", latest: "10:00:00.007"}
# Meaning: "the real time is somewhere in this 7ms window"
```

TrueTime doesn't claim to know the exact time — it gives you a bounded **uncertainty window** of about 7ms across Google's fleet. Spanner uses this for its key trick: when committing a transaction, it **deliberately waits out the uncertainty window** before declaring the transaction complete. This guarantees that if transaction A finished before transaction B started (in real time), then A's timestamp will be earlier than B's — globally, across every data centre.

That property is called **external consistency**, and it's stronger than textbook ACID consistency. The database behaves as if every transaction happened in some specific order in real time, even though it's running on multiple continents.

## What Spanner gives you

With TrueTime as the foundation, Spanner offers what no other database had:

1. SQL with full ACID transactions — feels like PostgreSQL.
2. Across data centres on multiple continents — automatic geographic replication.
3. With strong consistency — every read sees the latest write, anywhere.
4. And high availability — survives data-centre failures invisibly.

You write code that looks like ordinary SQL:

```sql
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 'alice';
  UPDATE accounts SET balance = balance + 100 WHERE id = 'sagar';
COMMIT;
```

Same as PostgreSQL. Except those two accounts might physically live on different continents, and Spanner still guarantees the transaction is atomic with strict global ordering against every other transaction in the system.

## The cost

This isn't free:

- **Custom hardware in every data centre** (GPS + atomic clocks). Only an entity with hundreds of data centres could pull this off. That's why it took Google.
- **Higher latency than single-region databases.** The "wait out the uncertainty window" trick adds ~7ms to every commit. Globally distributed transactions also pay the round-trip network time between continents.
- **Operational complexity.** Enormous system, many moving parts.

**Most companies don't need Spanner.** If your user base is in one region, PostgreSQL on a beefy machine handles it. PostgreSQL with read replicas, or sharded PostgreSQL with something like Vitess, scales most of the way. Spanner is for cases with genuinely *global*, *transactional*, *high-availability* requirements all at once — rare outside FAANG-scale companies and global financial systems.

## Spanner today and its legacy

Internally at Google, Spanner runs AdWords/AdSense, Google Play, parts of Gmail and Photos, the Drive metadata layer (the database that knows about your Google Docs), Search and YouTube metadata. By 2017 it was handling tens of millions of queries per second.

In 2017, Google opened it up as **Cloud Spanner** on GCP — rentable, expensive (hundreds of dollars/month minimum), used by global fintechs like Wise.

The 2012 Spanner paper inspired a generation of **NewSQL** databases — systems aiming for SQL + ACID + global scale without requiring Google's hardware:

- **CockroachDB** (2015, ex-Googlers) — the most direct Spanner clone. Open source, commodity hardware, approximates TrueTime with logical clocks plus a clever protocol. Used by Netflix, DoorDash, many fintechs.
- **YugabyteDB** — similar, PostgreSQL-compatible.
- **TiDB** — Chinese-origin, MySQL-compatible.

AWS and Azure took different paths: **AWS Aurora** scales relational databases by separating compute from storage, but within a single region. **Azure Cosmos DB** is global but lets you pick from several consistency levels rather than guaranteeing the strongest.

The "global, strongly consistent, SQL database" niche remains genuinely Spanner-shaped.

## The transferable principle

The pattern I want to remember: **when something is "impossible," check what's being assumed.**

CAP wasn't wrong as a mathematical theorem. It correctly modelled the trade-offs *given the assumption that clock uncertainty is unbounded*. Spanner didn't violate the theorem — it made the assumption false in practice by installing GPS receivers everywhere. Once clock uncertainty has a tight, knowable bound, the original impossibility result no longer applies because the proof depended on the unbounded case.

This generalises. Many "fundamental limits" in engineering are limits *given a set of assumptions*. If you can re-engineer the underlying conditions, the limit dissolves. "It's impossible to do high-frequency trading from Mumbai because latency to NYC is too high" was true until people co-located servers in the same building as the exchange. Same shape of move.

If you want to read the original, the 2012 OSDI paper "Spanner: Google's Globally-Distributed Database" is unusually readable for an academic systems paper — about 25 pages, written like an engineering report. One of the canonical reads in distributed systems.

---

*This entry pairs with [A Google Doc is a database row, not a file](a-google-doc-is-a-database-row-not-a-file.md) — Spanner is the specific database technology that makes "your Google Doc lives as rows in our database" work across continents at scale.*
