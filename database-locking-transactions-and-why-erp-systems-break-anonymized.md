# Database Locking, Transactions, and Why ERP Systems Break

Spent two days debugging a Dynamics NAV "record locked by another user" error on a production ERP system. What started as "why is our accounting system throwing errors" became a deep dive into how relational databases actually work under the hood — transactions, locks, isolation levels, session management, query plans, and the architecture that makes multi-user database systems possible (and fragile). Every concept below was learned by hitting a real problem, not from a textbook.

---

## 1. A database server is an apartment building, not a single room

The first thing I misunderstood: I thought "connecting to the database" meant I was "inside the server." In reality, a Windows server hosting SQL Server runs multiple independent services, each listening on its own TCP port:

| Service | Port | Protocol | What talks to it |
|---|---|---|---|
| SQL Server engine | 1433 | TDS (Tabular Data Stream) | Any SQL client — SSMS, Python, Node.js, NAV |
| SSRS (Reporting) | 80/443 | HTTP | Chrome, any web browser |
| NAV Service Tier | 7046-7049 | SOAP/OData | NAV client apps on employee PCs |
| SMB (File Sharing) | 445 | SMB/CIFS | Windows file explorer, mapped drives |
| RDP (Remote Desktop) | 3389 | RDP | Remote desktop clients |

Each service is a tenant in the apartment building. Having the key to one apartment (SQL login `db_admin`) doesn't get you into the others (SMB requires Windows credentials, RDP requires Windows credentials, etc.). This is why I could query the database from my Mac but couldn't browse the server's file system — different service, different authentication universe.

> **Key insight:** "Connected to the database" means you have ONE TCP socket open to port 1433, speaking the TDS protocol. You're talking to the SQL engine and nothing else. The operating system, file system, other services — all invisible to you unless you explicitly use SQL Server features that bridge the gap (like `xp_cmdshell` or `OPENROWSET`).

---

## 2. What is a SPID?

SPID = Session Process ID. Every TCP connection to SQL Server gets assigned a unique number. It's like a queue token at a bank counter.

```
My Mac (pymssql)  ──TCP──▶  SQL Server port 1433
                              │
                              ├─ SPID 51 (my connection)
                              ├─ SPID 52 (NAV Service connection #1)
                              ├─ SPID 53 (NAV Service connection #2)
                              ├─ SPID 65 (NAV Service connection #3)
                              └─ SPID 77 (someone's SSMS session)
```

SPIDs 1-50 are reserved for SQL Server's own internal processes (checkpoint, lazy writer, lock monitor). SPIDs 51+ are user connections.

The critical thing: **a SPID is a connection, not a user.** NAV's middle tier maintains a pool of SQL connections. One human user's click might be served by SPID 52 one moment and SPID 65 the next. And one SPID might serve different human users at different times.

This matters for debugging: when you see "SPID 65 is holding locks," you can't immediately say "user X is the problem." You have to trace through the application's session mapping to find the human.

---

## 3. Transactions — the most important concept in databases

A transaction is a group of operations that must succeed or fail **as a unit**. There is no "half done."

```sql
BEGIN TRANSACTION
  UPDATE Accounts SET Balance = Balance - 1000 WHERE AccountNo = 'A';
  UPDATE Accounts SET Balance = Balance + 1000 WHERE AccountNo = 'B';
COMMIT TRANSACTION
```

If the server crashes between the two UPDATEs, the database must ensure that NEITHER update persists. Otherwise Account A lost ₹1000 but Account B never got it — money disappeared.

This guarantee is called **ACID**:

| Property | What it means | How SQL Server implements it |
|---|---|---|
| **Atomicity** | All-or-nothing. Transaction either fully commits or fully rolls back. | Transaction log records every change with before/after values. ROLLBACK reads the log backwards and undoes each change. |
| **Consistency** | Database moves from one valid state to another. Constraints are never violated. | CHECK constraints, foreign keys, triggers all enforce rules at commit time. |
| **Isolation** | Concurrent transactions don't interfere with each other. One transaction's uncommitted changes are invisible to others. | **Locking** (the subject of this entire debugging session). |
| **Durability** | Once committed, changes survive crashes, power failures, disk failures. | Write-Ahead Logging (WAL): changes are written to the transaction log on disk BEFORE being applied to data files. |

> **Key insight:** The "I" in ACID — Isolation — is where all the complexity lives. Atomicity, Consistency, and Durability are solved problems (transaction log handles them elegantly). But Isolation requires the database to manage **concurrent access** from multiple sessions, and that's where locks, blocking, deadlocks, and "record locked by another user" errors come from.

---

## 4. The Transaction Log — how KILL can't corrupt data

I was terrified that killing a SQL session (KILL command) would corrupt data. Understanding the transaction log eliminated that fear.

**Write-Ahead Logging (WAL):** Before SQL Server changes any data page in memory, it first writes a log record to the transaction log file on disk. The log record says: "Transaction T changed row R from value A to value B."

This means the log always contains the complete history of what each transaction did. At any point, SQL Server can:
- **Redo** committed transactions (replay the log forward)
- **Undo** uncommitted transactions (replay the log backward)

When you run `KILL 65`:
1. SQL Server marks transaction T as "rolling back"
2. Reads the transaction log backward, finding every write by T
3. For each write: restores the original value (B → A)
4. Marks the transaction as "rolled back"
5. Releases all locks held by T

The database after KILL is **byte-for-byte identical** to what it was before the transaction started. This isn't approximate — it's mathematically exact, because every change was recorded with its inverse.

This same mechanism handles:
- Power failures (redo committed, undo uncommitted on restart)
- Application crashes (connection drops, transaction rolls back)
- Explicit ROLLBACK commands
- KILL commands

> **Key insight:** Transactions are designed to be interrupted. The entire architecture assumes interruption is normal. KILL is not a hack — it's a first-class operation that the log-based recovery system was built to handle.

---

## 5. Locks — the mechanism behind "locked by another user"

When a transaction reads or writes a row, SQL Server places a **lock** on that row. The lock is a small in-memory data structure that says: "Session X is using this resource in mode Y."

### Lock modes (from least to most restrictive)

| Mode | Name | Abbreviation | What it means | Compatible with |
|---|---|---|---|---|
| S | Shared | S | "I'm reading this row" | Other S locks (multiple readers OK) |
| U | Update | U | "I'm reading now but plan to write" | S locks only (prevents deadlock during update) |
| X | Exclusive | X | "I'm writing this row" | Nothing (blocks all other access) |
| IS | Intent Shared | IS | "I plan to take S locks on rows in this page/table" | IS, IX, S |
| IX | Intent Exclusive | IX | "I plan to take X locks on rows in this page/table" | IS, IX |
| Sch-S | Schema Stability | Sch-S | "I'm using this table's schema" | Everything except Sch-M |

### Lock compatibility matrix

This is the core of the entire locking system:

```
Requesting →    S     U     X
Holding ↓
  S            ✓     ✓     ✗
  U            ✓     ✗     ✗
  X            ✗     ✗     ✗
```

Read this as: "If Session A holds a Shared lock, can Session B get an Exclusive lock?" → No (✗). Session B must wait.

**This is why the NAV error happens:** When user A is mid-posting (holding X locks on G/L Entry rows), user B tries to post (needs X locks on the same rows). X is incompatible with X. User B waits 30 seconds, gives up, error message.

### Lock granularity

SQL Server locks at multiple levels simultaneously:

```
DATABASE ──▶ TABLE ──▶ PAGE (8KB) ──▶ ROW (KEY/RID)
```

A single UPDATE takes:
- Intent Exclusive (IX) lock on the TABLE
- Intent Exclusive (IX) lock on the PAGE containing the row
- Exclusive (X) lock on the specific ROW

Intent locks exist to prevent conflicts at higher levels without checking every individual row. If you want to lock an entire table, you only need to check intent locks at the table level — you don't need to scan millions of row-level locks.

---

## 6. Isolation levels — the trade-off between correctness and concurrency

SQL Server supports multiple isolation levels, each making a different trade-off:

| Level | Reads take locks? | Can see uncommitted data? | Phantom reads? | Performance |
|---|---|---|---|---|
| READ UNCOMMITTED | No | Yes ("dirty reads") | Yes | Fastest |
| READ COMMITTED (default) | Yes (S locks, released after read) | No | Yes | Normal |
| READ COMMITTED SNAPSHOT (RCSI) | No (uses row versioning) | No | Yes | Fast reads, slight write overhead |
| REPEATABLE READ | Yes (S locks held until commit) | No | Yes | Slower |
| SERIALIZABLE | Yes (range locks held until commit) | No | No | Slowest |

### `WITH (NOLOCK)` — the quick fix

```sql
SELECT * FROM Customers WITH (NOLOCK)
```

This is equivalent to `READ UNCOMMITTED` for that specific query. It means: "Don't take any locks. I accept that I might see partially-written data from other transactions."

For **reporting queries** (like the external app reading customer outstanding data), dirty reads are usually acceptable — you're generating a dashboard, not making a financial commitment based on the exact values. The 0.01% chance of reading an uncommitted value is irrelevant compared to the certainty of blocking NAV users.

For **transactional writes** (like NAV posting an invoice), you need proper isolation. Dirty reads would be catastrophic — you could double-apply a payment or skip an invoice.

> **Key insight:** The ExtApp was using READ COMMITTED (default) for pure reporting queries. Every SELECT took shared locks. Those shared locks blocked NAV's exclusive locks during posting. Adding `WITH (NOLOCK)` — or setting the connection to READ UNCOMMITTED — eliminates this entirely. The data you read might be 0.001% stale, but you'll never block another user.

### READ COMMITTED SNAPSHOT ISOLATION (RCSI) — the elegant fix

RCSI changes how READ COMMITTED works **without changing any application code.** Instead of taking shared locks, readers use **row versioning**: SQL Server keeps old versions of rows in tempdb, and readers see the version that was committed when their query started.

```
Normal READ COMMITTED:
  Reader takes S lock → Writer wants X lock → BLOCKED (waits)

RCSI:
  Reader reads from version store (no lock) → Writer takes X lock → NO CONFLICT
```

We enabled RCSI on NAV_Production_DB with:
```sql
ALTER DATABASE [YourNavDatabase] SET READ_COMMITTED_SNAPSHOT ON;
```

**What it fixed:** ExtApp queries no longer block NAV posting (reader-writer conflict eliminated).

**What it didn't fix:** Two NAV users both trying to POST (writer-writer conflict). RCSI only helps readers. When two writers need the same row, one still has to wait — that's fundamental, not a configuration issue.

---

## 7. NAV's middle-tier architecture and connection pooling

Dynamics NAV 2016 has a three-tier architecture:

```
Tier 1: NAV Client (Windows app on each employee's PC)
          │
          │  SOAP/OData calls over LAN
          ▼
Tier 2: NAV Service Tier (on the server, C/AL runtime)
          │
          │  TDS protocol, SQL connection pool
          ▼
Tier 3: SQL Server (on the same or different server)
```

The NAV Service Tier maintains a **connection pool** — a set of pre-opened SQL connections (maybe 10-15 SPIDs). When a user clicks "Post" in the NAV client:

1. NAV Service picks a free connection from the pool (say SPID 65)
2. Opens a transaction on that connection
3. Runs C/AL business logic, generating SQL statements
4. Each SQL statement executes through SPID 65
5. On success: COMMIT. On failure: ROLLBACK.
6. Returns the connection to the pool.

**Why this matters for debugging:**
- All connections show `program_name = "Microsoft Dynamics NAV Service"` and `login_name = "DOMAIN\Administrator"` — because they're all from the same service, not from individual users
- You can't directly see which human is behind which SPID
- NAV maps its internal session IDs to SQL SPIDs dynamically
- A "stuck" SPID might be an orphaned connection where the NAV client disconnected but the SQL transaction wasn't rolled back

---

## 8. The blocked process report — SQL Server's recording device

SQL Server can automatically log **every blocking event** that exceeds a threshold:

```sql
sp_configure 'blocked process threshold (s)', 10;
RECONFIGURE;
```

When any session blocks another for >10 seconds, SQL Server writes an XML report to the error log containing:
- The blocker's SPID, login, hostname, application name
- The victim's SPID, login, hostname, application name  
- The **exact SQL** both were running
- The wait type and duration

This is the definitive diagnostic. Instead of catching the problem in real-time (which requires being online at the exact moment), you set the trap and read the report afterward.

---

## 9. Dynamic Management Views (DMVs) — X-raying a running database

DMVs are special system views that expose SQL Server's internal state in real-time. They're read-only and don't affect performance. The key ones I used:

| DMV | What it shows |
|---|---|
| `sys.dm_exec_sessions` | All active connections (SPIDs), their login, host, app, CPU usage, memory |
| `sys.dm_exec_requests` | Currently executing queries, their wait type, blocking status |
| `sys.dm_tran_locks` | Every lock currently held by every session |
| `sys.dm_tran_active_transactions` | Open transactions, their start time, duration |
| `sys.dm_exec_sql_text(handle)` | The SQL text for a given query handle |
| `sys.dm_exec_input_buffer(spid)` | The original client command sent to a session |
| `sys.dm_exec_query_stats` | Cached query plan statistics (execution count, CPU, reads) |

### The two essential diagnostic queries

**Query 1: Who is blocking whom?**
```sql
SELECT
    blocking_session_id AS BlockerSPID,
    session_id AS VictimSPID,
    wait_type, wait_time / 1000.0 AS WaitSec,
    DB_NAME(database_id) AS DBName
FROM sys.dm_exec_requests
WHERE blocking_session_id <> 0;
```

**Query 2: What is the blocker doing?**
```sql
SELECT s.session_id, s.login_name, s.host_name, s.program_name,
       t.text AS SqlText
FROM sys.dm_exec_sessions s
LEFT JOIN sys.dm_exec_connections c ON s.session_id = c.session_id
OUTER APPLY sys.dm_exec_sql_text(c.most_recent_sql_handle) t
WHERE s.session_id = <BlockerSPID>;
```

> **Key insight:** DMVs are like a live X-ray of the database engine. They show you the internal state without affecting it. Learning to read DMVs is the single most valuable SQL Server debugging skill — it turns "something is wrong" into "SPID 65 on machine X running query Y is blocking SPID 52 for 45 seconds on a KEY lock on table Z."

---

## 10. The plan cache — why a server restart can change performance

When SQL Server sees a query for the first time, it:
1. Parses the SQL text
2. Considers multiple execution strategies (index seek vs. scan, join order, etc.)
3. Estimates row counts using **statistics** (histograms of data distribution)
4. Picks the cheapest plan
5. **Caches** the plan for reuse

Subsequent executions of the same query skip steps 1-4 and reuse the cached plan. This makes queries fast.

**When SQL Server restarts**, the plan cache is emptied. Every query must be re-compiled. The new plans might be different from the old ones because:
- Statistics were updated (different row estimates)
- First execution has different parameter values (parameter sniffing)
- Memory pressure is different
- Available indexes changed

A plan that was "take 2 seconds" before restart can become "take 30 seconds" after restart if the optimizer makes a different choice. For NAV's posting operations, this difference determines whether locks are held for 2 seconds (no blocking) or 30 seconds (everyone gets blocked).

---

## 11. Statistics — how SQL Server estimates before executing

SQL Server maintains **statistics** (histograms) on index columns. When optimizing a query, it uses statistics to estimate: "how many rows will match this WHERE clause?"

If statistics are stale (the data changed a lot since last update), the estimates can be wildly wrong:
- Estimate says 10 rows → optimizer picks nested loop join (fast for small sets)
- Actual result is 100,000 rows → nested loop executes 100,000 times → catastrophically slow

`sp_updatestats` forces SQL Server to refresh all statistics. After a server restart, this can help the optimizer make better choices for the first wave of queries.

---

## 12. Authentication: SQL logins vs. Windows accounts

SQL Server supports two authentication modes:

| Mode | Example | Where it works |
|---|---|---|
| SQL Authentication | `db_admin` / `[password]` | Only SQL Server (port 1433) |
| Windows Authentication | `DOMAIN\Administrator` | SQL Server, SMB, RDP, NAV — anything using Windows security |

The `db_admin` account is SQL Server's built-in superadmin. It exists only within SQL Server's own identity system. Windows doesn't know about it; SMB doesn't know about it. That's why `db_admin` credentials let me query the database but not browse the server's file system.

NAV Service runs as `DOMAIN\Administrator` (a Windows account). It connects to SQL Server using Windows Authentication. All its SQL connections show `login_name = DOMAIN\Administrator`.

---

## 13. Automatic Cost Adjustment — why one NAV setting can cripple a business

NAV tracks inventory costs using a two-phase approach:
1. **At posting time:** record the quantity movement and an estimated cost
2. **Later:** run a batch to calculate the true cost (FIFO, LIFO, Average, Standard) and post corrections

The "Automatic Cost Adjustment" setting controls WHEN phase 2 runs:

| Value | Behavior | Impact on locking |
|---|---|---|
| Never | Phase 2 only runs when manually triggered | Zero impact during posting |
| Day/Week/Month | Phase 2 runs if entries are older than threshold | Moderate |
| **Always** | Phase 2 runs **inline, within the posting transaction** | **Catastrophic** — every post triggers a mini-batch that holds locks for minutes |

With "Always," the posting transaction becomes:
```
BEGIN TRAN
  Insert Item Ledger Entry (fast)
  Insert Value Entry with estimated cost (fast)
  ▸ RUN FULL COST ADJUSTMENT for affected items (SLOW — minutes)
    Takes UPDLOCK/XLOCK on Item Application Entry, Value Entry, etc.
    Walks the entire application chain for affected items
    Updates corrections across potentially thousands of rows
  ◂ 
  Insert G/L Entry (fast)
COMMIT
```

During those minutes, the transaction holds exclusive locks on costing tables. Any other user trying to post an inventory transaction hits those locks and gets the "locked by another user" error.

> **Key insight:** This is a design-time decision (when to run cost adjustment) that has run-time consequences (lock duration). Microsoft explicitly recommends "Never" for production environments with concurrent users. "Always" is suitable only for single-user or demo databases.

---

## 14. The vicious cycle — how a small problem becomes a multi-day crisis

The most subtle concept: how a transient problem (a few seconds of blocking) can become a self-reinforcing crisis.

```
Initial trigger (e.g., external app holding locks for a few seconds)
  → NAV posting times out and ROLLS BACK
  → Rolled-back posting leaves inventory entries in intermediate state
  → Next posting triggers cost adjustment on MORE entries (cleanup of the rollback)
  → Cost adjustment takes LONGER (more work)
  → Locks held LONGER
  → MORE users time out and roll back
  → MORE intermediate entries accumulate
  → EVEN MORE cleanup needed next time
  → SPIRAL
```

The amplifier in this loop is "Automatic Cost Adjustment = Always." Remove the amplifier (set to "Never"), and the loop breaks: a failed posting is just a failed posting — retry and it works. No cascading cleanup, no accumulated debris.

---

## 15. Writer-Writer vs. Reader-Writer contention

This distinction is crucial and I initially confused them:

**Reader-Writer contention:** One session reads, another writes. Solved by:
- `WITH (NOLOCK)` — reader skips locks entirely
- RCSI — reader uses row versioning, never blocks writer
- Both are **configuration fixes** — no code change needed for RCSI

**Writer-Writer contention:** Two sessions both write to the same rows. **Cannot be solved by any isolation setting.** When two transactions need exclusive access to the same row, one MUST wait. This is fundamental — not a bug, not a misconfiguration, but a mathematical necessity.

The NAV "locked by another user" error, when it involves two users both posting, is writer-writer contention. The fix isn't a database setting — it's ensuring that each posting operation completes quickly so the lock window is short (milliseconds, not minutes).

---

## 16. Backups — what they are and aren't

`BACKUP DATABASE` creates a self-contained `.bak` file that captures the entire database at a point in time. It's NOT a file copy — it's a structured export that includes:
- All data pages
- The active transaction log (for point-in-time recovery)
- Schema, indexes, permissions
- Metadata needed for RESTORE

Key properties:
- **Non-blocking:** BACKUP runs while users are working (uses snapshot isolation internally)
- **Consistent:** The backup represents a single point in time, even if it takes 30 minutes to complete
- **Portable:** Can be restored on any SQL Server of the same or newer version
- **Compressible:** `WITH COMPRESSION` typically reduces size 60-80%

**`COPY_ONLY`:** A backup that doesn't affect the backup chain. Normal backups update the "last backup" marker; COPY_ONLY takes a snapshot without touching the marker. Use this for ad-hoc copies (like sending to Google Drive) without disrupting automated backup schedules.

---

## 17. Drive mappings and user sessions — a Windows concept that tripped me up

On Windows, drive letters (M:, N:, etc.) can be **mapped network drives** — shortcuts to folders on other servers. But mapped drives are **per-user-session**, not global.

When someone runs `net use M: \\192.168.x.z\navlive`, that M: mapping exists ONLY for their Windows login session. Other users logged into the same machine don't see it. Crucially:
- SQL Server Agent runs as `NT SERVICE\SQLSERVERAGENT` — its own session
- SQL Server engine runs as `NT SERVICE\MSSQLSERVER` — different session
- A drive mapped in Agent's session isn't visible to the engine's session

This is why the backup files on "M:" were invisible to my queries — the M: drive was mapped by SQL Agent (for the nightly backup job) but not by the SQL engine (which runs my SELECT statements).

> **Key insight:** In Windows, the "file system" isn't a single shared reality — it's per-user. Two processes on the same machine can see different drive letters, different network shares, different permissions. This is a security feature (isolation between services) that becomes a debugging puzzle when you expect everything to share the same view.

---

## 18. The "same database, different outcome" diagnostic — narrowing root cause by comparison

After writing the sections above, we kept debugging and hit the most powerful clue of the session: the "locked by another user" error was happening ONLY on the Company A company, not on Company B — even though both companies live in the same database (NAV_Production_DB), on the same SQL Server, with the same configuration.

This is a **natural experiment** — two subjects sharing every environmental variable except their own internal data and settings. Whatever explains Company-A-only errors must be something specific to that entity.

**What it ruled out (shared between both companies):**
- SQL Server restart → same server → can't explain the difference
- RCSI setting → database-level → applies to both
- ExtApp queries → the Payment Reminder scanned BOTH companies → both would be affected
- Plan cache, tempdb, server RAM → all shared

**What it ruled in (per-company in NAV):**
- Each company has its own copy of every table (`[CompanyName$G_L Entry]` vs `Company_B$G_L Entry`)
- Each company has its own Inventory Setup, its own index fragmentation, its own data volume

We then checked `Automatic Cost Adjustment` across all four companies — expecting Company A to be "Always" and Company B to be "Never." The result: **all four companies had "Always" (6).** The hypothesis that the setting alone was the differentiator was wrong.

But this led to a deeper insight.

---

## 19. Mechanism vs. trigger — compound causation and interaction effects

The same setting (`Always`) produces different outcomes at different scales:

| Factor | Company A | Company B |
|---|---|---|
| Automatic Cost Adjustment | Always (6) | Always (6) |
| G/L Entry rows | 1,152,366 | ~50,000 |
| Annual invoices | 7,430 | 644 |
| Concurrent users | 20-30 | 3-5 |
| Index fragmentation | 60-90% | Low (small tables) |
| **Outcome** | **Errors daily** | **No errors** |

`Automatic Cost Adjustment = Always` is the **mechanism** — it causes inline cost adjustment on every inventory post. But the mechanism only becomes a **problem** when combined with scale factors (data volume, user count, fragmentation) that make the adjustment SLOW.

For Company B: adjustment runs on tiny tables, completes in milliseconds. Two users would need to click Post within the same 50ms window to collide. With 3-5 users, this essentially never happens.

For the larger entity: adjustment runs on massive fragmented tables, takes seconds to minutes. With 20-30 concurrent users, someone is always mid-adjustment when someone else tries to post. Collision is guaranteed.

> **Key insight:** In complex systems, single-variable explanations often fail. The real explanation is an INTERACTION EFFECT — factor A × factor B × factor C. Each factor alone is harmless; their combination is catastrophic. The "Always" setting is fine at small scale. High fragmentation is tolerable without inline adjustment. Many users don't collide if transactions are fast. But Always + fragmentation + scale = crisis. This is why the Deutsch "hard to vary" test matters — you need ALL elements in the explanation to be load-bearing, and removing any ONE should break the predicted outcome.

---

## 20. The buffer pool — why a server restart can feel like a regression

SQL Server keeps frequently-accessed data pages cached in RAM, in a structure called the **buffer pool**. On a server with sufficient RAM, the entire "hot" dataset lives in memory. Queries read from RAM (nanoseconds) instead of disk (milliseconds) — orders of magnitude faster.

When SQL Server restarts, the buffer pool is **wiped clean**. Every query after restart must read from disk. The performance difference is dramatic:

```
Before restart (warm cache):
  Query reads 10,000 pages from RAM → 5 milliseconds

After restart (cold cache):
  Query reads 10,000 pages from disk
  With healthy indexes (sequential I/O): → 200 milliseconds
  With 90% fragmented indexes (random I/O): → 5,000 milliseconds (5 seconds!)
```

Over hours and days, the buffer pool gradually "warms up" — frequently-used pages get cached again. But if the hot dataset exceeds available RAM, some queries always hit disk, and fragmentation permanently degrades performance.

This explains why a SQL Server restart can SUDDENLY make a tolerable system intolerable: the same queries that were running from RAM now hit fragmented disk, taking 10-100× longer. Lock hold times increase proportionally, and blocking collisions that were rare become constant.

---

## 21. NAV's internal design: READUNCOMMITTED by default

While investigating cached query plans, I discovered that NAV's own internal queries already use `WITH(READUNCOMMITTED)`:

```sql
-- NAV's own generated SQL (from sys.dm_exec_query_stats):
SELECT SUM("SUM$Sales (LCY)")
FROM "[CompanyName$Cust_ Ledger Entry]$VSIFT$1"
  WITH(READUNCOMMITTED, NOEXPAND)
```

NAV was **designed to never block itself** with reader-writer contention. Its reads use dirty-read isolation so they never take shared locks. The ONLY blocking scenario within NAV is writer-writer (two users posting simultaneously), which is brief and self-resolving.

The ExtApp introduced a **new category of contention** that had never existed in this database's history: an external application running READ COMMITTED queries (with shared locks) against the same tables NAV writes to. For the first time, readers were blocking writers.

> **Key insight:** When you add a new application to an existing database, you're not just adding load — you may be introducing a new PATTERN of access that the existing system was never designed to handle. NAV's architecture assumed all readers use READUNCOMMITTED. The ExtApp violated that assumption. Understanding the existing system's design assumptions before adding new clients is critical — it's not about "will my queries be fast enough?" but "will my locking pattern conflict with the existing workload?"

---

## 22. The limits of diagnosis — honesty about what you can and can't prove

After two days of debugging, I had to confront an uncomfortable truth: I could identify the **mechanism** (inline cost adjustment + fragmented indexes + scale = long locks = blocking errors) and the **fix** (rebuild indexes + change setting + add NOLOCK), but I could not definitively prove **what specific event 2-3 days ago tipped the system from working to broken.**

Three candidates remained:
1. **ExtApp deployment** added new shared-lock queries (new contention pattern)
2. **SQL Server restart** flushed the buffer pool (warm cache → cold cache)
3. **Index fragmentation** crossed a tipping point (gradual degradation hit a threshold)

Probably all three contributed simultaneously, which makes isolating one as "THE cause" impossible without a time machine.

The temptation was to pick the most plausible candidate and present it confidently. But that would be intellectually dishonest. In Deutsch's framework: an explanation that could accommodate multiple different triggers is "easy to vary" — I could swap any trigger into the narrative and it would still sound plausible. That's a sign the explanation is incomplete.

What IS hard to vary: the mechanism itself. Remove inline cost adjustment → posting is fast → no errors (regardless of trigger). Remove fragmentation → adjustment is fast → no errors. Remove scale → collisions are rare → no errors. Each element is load-bearing. The fix follows from the mechanism, not from identifying the trigger.

> **Key insight:** In complex system failures, identifying the exact trigger is sometimes less valuable than understanding the mechanism. The trigger is historical (it happened, it's done). The mechanism is structural (it will keep causing problems until fixed). Fixing the mechanism protects against ALL possible triggers — past, present, and future. This is the difference between "root cause analysis" (what happened?) and "systemic fix" (what prevents it from ever happening again?). Both matter, but when you can't conclusively answer the first, the second is sufficient for action.

---

## 23. The problems that created these solutions — why each concept exists

Every concept in this document exists because someone, somewhere, hit a real problem and invented a solution. Understanding the original problem makes the solution feel inevitable rather than arbitrary.

### Why locks were invented

**The problem (1960s):** Two bank tellers process withdrawals from the same account simultaneously. Each reads the balance ($1,000). Each subtracts $500. Each writes $500 back. Result: only $500 was withdrawn, but the balance shows $500 — the bank lost $500. This is called the **lost update problem.**

Without locks, any concurrent system that allows reads and writes to the same data will produce this bug. It's not a software bug — it's a mathematical inevitability of unsynchronized concurrent access.

**The solution:** Before modifying a row, acquire an **exclusive lock** on it. Anyone else trying to access that row must wait. The lost update becomes impossible because the second teller's read is blocked until the first teller's full read-modify-write cycle completes. The trade-off: some operations must wait.

### Why transactions were invented

**The problem (1970s):** You transfer ₹1,000 from Account A to Account B. The system debits A (balance goes from ₹5,000 to ₹4,000). Then the power fails. Account B was never credited. ₹1,000 disappeared from the universe. This is called a **partial failure.**

Jim Gray formalized the solution in his 1976 paper: group related operations into a **transaction** with an all-or-nothing guarantee. Either ALL operations succeed (commit) or NONE of them persist (rollback). Gray later won the Turing Award for this work. Virtually every database, file system, and distributed system built since uses his model.

### Why the transaction log was invented (Write-Ahead Logging)

**The problem:** Transactions need to be durable (survive crashes) AND fast. Writing to disk on every operation is slow (disk seek: ~10 milliseconds). If you wait for disk on every row update, the system crawls.

**The insight (IBM IMS, 1970s):** Don't write data pages to disk immediately. Instead, write a **sequential log entry** first (much faster — sequential disk writes are 100× faster than random). The log entry says: "changed row X from A to B." The actual data pages can be written to disk later, in batches, at the system's convenience.

If the system crashes before data pages are flushed, no problem — replay the log on restart. If a transaction needs to roll back, read the log backwards and undo each change. The log is the single source of truth. This is called **Write-Ahead Logging (WAL)** and is used by every serious database: SQL Server, PostgreSQL, Oracle, MySQL/InnoDB, SQLite.

### Why multiple isolation levels exist

**The problem:** Full isolation (every transaction behaves as if it's the only one running) requires every read to take locks and hold them until the transaction ends. This is **serializable** isolation — correct but catastrophically slow under concurrent load. But zero isolation means dirty reads, phantom rows, and non-repeatable reads.

**The insight (1992, ANSI SQL standard):** Different applications need different points on the correctness-vs-performance spectrum. A financial audit needs serializable. A dashboard needs READ UNCOMMITTED. A typical web app needs READ COMMITTED. Rather than forcing one choice, let the application CHOOSE its isolation level. Each level has well-defined semantics and well-defined anomalies it permits.

### Why NOLOCK / READ UNCOMMITTED was invented

**The problem (practical, not theoretical):** A manager runs a monthly report that scans the entire Sales table. The report takes 3 minutes. During those 3 minutes, the report holds shared locks on every row it reads. Every salesperson trying to enter a new order is blocked. The entire company stops for 3 minutes every time someone runs a report.

**The solution:** Let the report read WITHOUT taking any locks. Yes, it might see a partially-written row (a "dirty read"). But for a summary report showing total monthly sales, being off by one in-flight transaction doesn't matter. The report runs fast, salespeople aren't blocked, everyone's happy. The trade-off is explicit: you accept potentially stale data in exchange for zero contention.

### Why RCSI was invented

**The problem (competitive, 2000s):** Oracle had always used **Multi-Version Concurrency Control (MVCC)** — readers see a snapshot of the data as of their transaction's start time, without taking any locks. Readers never block writers, writers never block readers. SQL Server, by contrast, used lock-based concurrency. When Microsoft tried to sell SQL Server to Oracle shops, customers complained: "your readers block our writers!"

**The solution (SQL Server 2005):** Microsoft added Read Committed Snapshot Isolation (RCSI). When enabled, SQL Server keeps old versions of rows in tempdb. Readers see the committed version as of their statement's start — no locks needed. The brilliance: it's a database-level setting, not a code change. Enable it, and every existing application automatically gets Oracle-style non-blocking reads without changing a line of code.

### Why connection pooling was invented

**The problem:** Opening a new database connection is expensive: TCP three-way handshake (~1ms), TLS negotiation (~5ms), authentication (~2ms), session setup (~1ms), memory allocation. If a web server opens and closes a connection for every HTTP request, connection overhead dominates actual query time.

**The solution:** Open N connections at startup, keep them alive, and **reuse** them across requests. A request grabs a free connection from the pool, uses it, returns it. The connection is never closed. This turns a 10ms connection setup into a 0.01ms pool checkout. Every modern web framework uses connection pooling by default.

### Why statistics and histograms exist

**The problem:** The query optimizer must choose a plan BEFORE executing the query. Should it use an index seek (fast for 10 rows) or a full table scan (fast for 1 million rows)? The answer depends on how many rows match the WHERE clause — but the optimizer doesn't know that without running the query, which is what it's trying to plan.

**The solution:** Maintain **histograms** — pre-computed summaries of data distribution. A histogram for the `PostingDate` column might say: "January has 5,000 rows, February has 8,000, March has 3,000." Now the optimizer can estimate: "WHERE PostingDate = '2026-03-15' will match ~100 rows → use index seek." Without statistics, the optimizer guesses blindly and frequently picks terrible plans. The system auto-maintains these, but if they go stale (our Company A tables had stats from 2020!), the optimizer makes decisions based on 5-year-old data distribution.

### Why the plan cache exists

**The problem:** Query optimization is NP-hard in the general case. For a query joining 10 tables, there are over 3.6 million possible join orderings to evaluate. Even with heuristics, compiling a plan takes 5-50 milliseconds. If the same query runs 1,000 times per second (typical for an ERP), spending 50ms compiling each time wastes 50 seconds of CPU per second — impossible.

**The solution:** Compile the plan once, **cache** it, reuse it for subsequent executions with different parameter values. The plan cache turns optimization from a per-execution cost into a one-time cost. This is why `DBCC FREEPROCCACHE` (clearing the cache) causes a brief performance dip — every query must recompile — followed by recovery as new plans are cached.

### Why index defragmentation is needed

**The problem:** When you create a table and insert rows in order, index pages are sequential — each page follows the previous one on disk. Sequential reads are fast (the disk head reads continuously without seeking). But after months of inserts, updates, and deletes, pages get shuffled: page 1 is followed by page 847, then page 23, then page 512. The index is **fragmented.** A sequential scan now requires hundreds of random disk seeks — each one costs 5-10ms, turning a 200ms scan into a 30-second ordeal.

**The solution:** Periodically **rebuild** the index — read all data, sort it, write it back in sequential order. Like defragmenting a hard drive. `ALTER INDEX ... REBUILD` does exactly this. `FILLFACTOR = 90` leaves 10% free space on each page so future inserts have room without immediately causing fragmentation again (called **page splits**).

### Why intent locks exist

**The problem:** Session A wants to lock an entire table exclusively (for a schema change or bulk update). It needs to verify no other session holds ANY row-level lock on that table. Checking every row for locks on a million-row table would take seconds.

**The solution:** When taking a row-level lock, ALSO take a lightweight **intent lock** at the table level. Intent Shared (IS) means "I have shared locks on some rows in this table." Intent Exclusive (IX) means "I have exclusive locks on some rows." Now checking for table-level conflicts requires examining ONE lock (the table-level intent), not millions of row locks. It's a hierarchical summary — the same idea as a table of contents in a book.

### Why NAV has Automatic Cost Adjustment at all

**The problem (specific to distribution/manufacturing ERP):** You buy 100 widgets at ₹5, then 100 more at ₹6. You sell 150 widgets. What's your cost of goods sold? Under FIFO, it's (100 × ₹5) + (50 × ₹6) = ₹800. Under Average, it's 150 × ₹5.50 = ₹825.

Computing the true cost requires **tracing back through the entire purchase history** — matching each sale to specific purchases. This is computationally expensive. If you do it on every transaction, posting becomes slow. If you never do it, your P&L is wrong.

**NAV's solution:** Defer the cost calculation. At posting time, use an estimated cost (the item's `Unit Cost` field). Later, run a batch ("Adjust Cost - Item Entries") that traces through the application chain and corrects the estimates. The `Automatic Cost Adjustment` setting controls WHEN that batch runs. `Never` = manual only. `Always` = inline on every post (convenient for small businesses but disastrous at scale).

### Why the Blocked Process Report exists

**The problem (DBA pain):** Lock blocking is **transient** — it lasts seconds to minutes, then resolves. By the time a DBA notices users complaining and opens SSMS to run diagnostic queries, the blocking episode is over. The evidence is gone. The DBA is always "too late."

**The solution (SQL Server 2005+):** Tell the engine to **automatically record** every blocking event that exceeds a threshold. The engine is always watching — it never misses an event. The DBA reviews the recordings afterward, like security camera footage. This transforms diagnosis from "catch it live" to "review the tape."

### Why three-tier architecture exists

**The problem (1990s client-server era):** Every user's PC connects directly to the database. With 100 users, that's 100 persistent connections, each consuming server memory. Business logic lives on each PC's application — updating logic means deploying to every PC. If one PC has a bug, it can corrupt the database directly.

**The solution:** Insert a **middle tier** (application server) between clients and database. Clients talk to the middle tier using a lightweight protocol. The middle tier talks to the database using a pooled set of connections (maybe 15 instead of 100). Business logic lives centrally on the middle tier — deploy once, every client gets the update. The database is shielded from direct client access. NAV's "Service Tier" is exactly this architecture.

---

## 24. Sequential search vs. binary search — why sorted data is everything

**Sequential search:** check every item, one by one. Finding Entry No. 847,203 in 1,152,366 entries requires checking ~576,000 entries on average. Double the data, double the time. This is **O(n)** — linear.

**Binary search:** requires SORTED data. Look at the middle entry. Is your target bigger or smaller? Eliminate half. Repeat. Finding Entry No. 847,203 in 1,152,366 sorted entries takes **21 checks.** Not 576,000. Twenty-one.

| Collection size | Sequential search | Binary search |
|---|---|---|
| 1,000 | 500 checks | 10 checks |
| 1,000,000 | 500,000 | 20 |
| 1,152,366 (production G/L Entry table) | 576,000 | **21** |
| 1,000,000,000 | 500,000,000 | **30** |

This is **O(log n)** — logarithmic. Double the data, add just ONE more check.

**This is the entire reason indexes exist.** An index keeps data sorted so binary search is possible. Without an index, SQL Server must scan every row (sequential search). With an index, it jumps to the answer in ~20 steps regardless of table size.

### The B-tree — how SQL Server does binary search in practice

SQL Server doesn't literally "open to the middle." It uses a **B-tree** (balanced tree) — a pre-built hierarchy:

```
                        [Root Page]
                    Entry 400,000 | Entry 800,000
                   /              |              \
          [Branch Page]    [Branch Page]    [Branch Page]
          /    |    \        /    |    \        /    |    \
       [Leaf] [Leaf] [Leaf] [Leaf] [Leaf] [Leaf] [Leaf] [Leaf]
       actual data rows live here (the 76,322 pages)
```

Finding Entry 847,203: read root page → go right (847K > 800K) → read branch → read leaf → found. **3 page reads.** For 1.15 million rows.

---

## 25. Pages, clustered indexes, and nonclustered indexes — how data physically lives on disk

### Pages: SQL Server's atom of storage

SQL Server stores everything in fixed-size **8 KB pages**. Every table, every index — all made of 8 KB pages. If a G/L Entry row is ~400 bytes, one page holds ~20 rows. A table with 1.15M rows needs ~76,000 pages = ~596 MB.

### Clustered index: the table itself, sorted

A clustered index IS the table data, physically sorted by the index key. There can be only ONE per table — data can't be physically sorted two ways simultaneously.

```
G/L Entry clustered index (sorted by Entry No_):
Page 1:  [Entry 1] [Entry 2] ... [Entry 20]       ← rows stored IN ORDER
Page 2:  [Entry 21] [Entry 22] ... [Entry 40]
Page 3:  [Entry 41] [Entry 42] ... [Entry 60]
...
Page 76322: [Entry 1152470] ... [Entry 1152494]
```

### Nonclustered index: a separate lookup table

A nonclustered index is a SEPARATE, smaller structure containing just the indexed column(s) + a pointer back to the clustered index. Like the index at the back of a textbook — keywords + page numbers, not the content itself.

```
Nonclustered index $4 on [Posting Date]:
Page 1: [2016-04-30 → Entry 1] [2016-04-30 → Entry 2] ...
Page 2: [2016-05-01 → Entry 46] ...
...sorted by date, not by Entry No_
```

To find all G/L entries from March 2026: binary search the nonclustered index (fast, sorted by date) → get Entry No_ pointers → look up full rows in the clustered index. This two-step process is called a **bookmark lookup**.

### The "$" naming convention in NAV

NAV names its indexes: the primary key gets the table name (clustered index), secondary keys get `$1`, `$2`, `$3`, etc. So `$8` on the Customer table = the 8th secondary key defined in NAV's development environment.

### What fragmentation means physically

**Before rebuild (77% fragmented):** Pages exist but are scattered randomly on disk. Page 1 is at disk location 47,000, page 2 at location 12,000, page 3 at location 63,000. Reading them in order requires random disk seeks — each one costs 5-10ms.

**After rebuild (0.01% fragmented):** Pages are sequential on disk. Page 1 at location 1, page 2 at location 2, page 3 at location 3. Reading is continuous — no seeking.

**Same data. Same rows. Same logical order. Just physically rearranged on disk.** That's all a rebuild does.

### Index rebuild results from a production system

After running a maintenance script on 121 indexes across 8 hot tables:

| Category | Before rebuild | After rebuild |
|---|---|---|
| Worst indexes | 95-98% fragmented | 0-4% |
| Large hot tables (G/L Entry, Value Entry) | 70-90% | 0.01-0.1% |
| Average improvement | | ~80 percentage points |

Sequential I/O is 100× faster than random I/O on spinning disks. This single change can turn a 30-second query into a sub-second query.

---

## 26. Why lock duration × user count = collision probability (the non-intuitive math)

The insight that changed how I think about the locking problem: **it's not the adjustment time that matters — it's the collision probability, which scales with the SQUARE of lock duration.**

If 30 users each post once every 5 minutes (300 seconds):

| Lock duration per post | Collision probability | User experience |
|---|---|---|
| 2 seconds (no adjustment) | ~18% per post, resolves in <2s | Occasional brief wait |
| 12 seconds (with adjustment) | ~70% per post, cascading | Constant errors |
| 60 seconds (heavy adjustment) | ~99% per post | System unusable |

Going from 12 seconds to 2 seconds isn't a 6× improvement — it's roughly **36×** fewer blocking incidents (6² = 36), because both the probability of encountering a lock AND the duration of your own lock contribution decrease.

---

## 27. Choosing the right Automatic Cost Adjustment value — a decision framework

The setting controls WHEN NAV recalculates true inventory costs:

| Value | Name | Adjustment trigger | Lock impact | Cost staleness |
|---|---|---|---|---|
| 0 | Never | Only manual/scheduled batch | Zero (during day) | Up to 24h (with nightly batch) |
| 1 | Day | Inline, if entries >1 day old | Low (morning crunch) | Max 24h (self-healing) |
| 2 | Week | Inline, if entries >7 days old | Very low | Up to 7 days |
| 3 | Month | Inline, if entries >30 days old | Negligible | Up to 30 days |
| 4 | Quarter | Inline, if entries >90 days old | Negligible | Up to 90 days |
| 5 | Year | Inline, if entries >365 days old | Negligible | Up to 365 days |
| 6 | Always | Inline, every single post | Catastrophic at scale | Zero (always current) |

**The key trade-off:** real-time cost precision vs. posting performance.

For a 30-user system with 1M+ G/L entries and 20K+ items: **Never (0) with a nightly batch.** The 0.1-0.5% intraday cost imprecision is invisible to the business. The nightly batch produces identical final numbers. The performance difference (2 seconds vs. minutes) is felt by every user every day.

"Day" (1) is the safer alternative if you don't trust nightly batch monitoring — it self-heals without any scheduled job. But it creates a brief "9 AM crunch" when the day's first posts trigger yesterday's adjustments.

> **Key insight:** The final cost numbers are IDENTICAL regardless of which setting you choose. The only question is WHEN the calculation happens. "Always" = during your post (blocking everyone). "Never" = at 2 AM (blocking nobody). Same math, same result, radically different user experience.

---

## 28. What stayed with me

Five things from this deep dive that changed how I think about databases and complex systems:

**1. Locks are the price of concurrency.** Every multi-user system faces the same tension: let users work simultaneously (concurrency) while ensuring they don't corrupt each other's data (isolation). Locks are the mechanism that resolves this tension. Understanding locks means understanding the fundamental trade-off in any shared system — not just databases, but file systems, version control, even human organizations (meeting room bookings are locks).

**2. Mechanism matters more than trigger.** We spent two days chasing "what changed 2-3 days ago?" and never found a single definitive trigger. But we fully identified the mechanism: inline cost adjustment on fragmented indexes at scale. Fixing the mechanism (rebuild indexes, change the setting) protects against ALL triggers — known and unknown. In Deutsch's terms: the mechanism is the deep explanation; the trigger is a surface-level initial condition.

**3. Interaction effects are the hardest bugs to diagnose.** `Automatic Cost Adjustment = Always` was set identically across four companies. It only caused problems on Company A — because Company A had the unique combination of scale + fragmentation + concurrency that turned a harmless setting into a catastrophe. Single-variable thinking ("find THE cause") fails for interaction effects. You need to think in terms of factor combinations and thresholds.

**4. Transactions are a design pattern for an unreliable world.** The all-or-nothing guarantee means you can design systems that assume failure is normal. KILL a stuck process — the log guarantees clean recovery. This "assume failure, design for recovery" mindset extends beyond databases into distributed systems, API design, and business process design.

**5. When adding a new application to an existing database, understand the existing access pattern assumptions.** NAV was designed with all readers using READUNCOMMITTED — it assumed readers never block writers. The ExtApp violated that assumption by using READ COMMITTED. The most dangerous bugs come from violating assumptions you didn't know existed.

---

## Sources

- Hands-on debugging of Company A' Dynamics NAV 2016 production system (NAV_Production_DB)
- Microsoft SQL Server documentation on [Transaction Locking and Row Versioning](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide)
- Microsoft Dynamics NAV documentation on [Automatic Cost Adjustment](https://learn.microsoft.com/en-us/dynamics-nav/inventory-setup)
- Paul Randal's blog on [KILL and transaction rollback internals](https://www.sqlskills.com/blogs/paul/)
- Brent Ozar's [sp_BlitzLock and blocking diagnostics](https://www.brentozar.com/)

---

What I studied next: Need to understand [distributed transactions and two-phase commit](https://en.wikipedia.org/wiki/Two-phase_commit_protocol) — what happens when a transaction spans two databases (like NAV posting to both NAV_Production_DB and the Singapore entity's books simultaneously).
