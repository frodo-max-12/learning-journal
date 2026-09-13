# Mainframes — Scale-Up in a Scale-Out World

**Context:** I asked whether mainframes are still used, half expecting "no, that's history." The answer is that they run a large share of the world's most critical transaction systems, and my obvious follow-up — *but doesn't everyone use the cloud now?* — turned out to rest on a false assumption. **Cloud and mainframes aren't competing for the same job.** They're opposite architectures, and seeing why was worth more than the trivia about who still uses one.

---

## 1. They didn't go away

Mainframes still sit underneath core banking, card networks and wire transfers, insurance policy and claims systems, airline reservations, tax and social-security systems, and large-scale healthcare records. The commonly cited figures are that around 70% of the largest companies still run them, and that they handle the bulk of structured enterprise transaction volume worldwide.

The reasons they persist are specific rather than sentimental:

- **Reliability engineered at every level.** Built for uptime measured in five nines and beyond, with hardware redundancy throughout. Many run for years without an unplanned outage.
- **Transaction throughput of a particular shape** — enormous volumes of small, concurrent, I/O-heavy transactions. Which is exactly what payments and banking are.
- **Security** — pervasive hardware encryption and strong isolation.
- **Backward compatibility** — code written decades ago still runs. There are billions of lines of COBOL in production, and rewriting them is expensive and risky in a way that has nothing to do with the difficulty of the language.

They're also not frozen in 1985. Current models run Linux, containers, and orchestration alongside the traditional operating system, and have on-chip AI acceleration used for things like real-time fraud scoring *during* a transaction rather than after it.

---

## 2. The distinction that resolved my confusion

Here's the thing I had wrong. I'd been imagining the cloud as "a really big mainframe" — the modern, better version of one enormous computer.

It's the **opposite design philosophy**:

| | mainframe | cloud |
|---|---|---|
| direction of scaling | **scale-up (vertical)** — one enormous machine | **scale-out (horizontal)** — millions of ordinary servers |
| where resilience comes from | hardware redundancy inside the box | *software* spreading work across many cheap, individually unreliable machines |
| the unit | a single vertically integrated system, plus a backup | commodity servers, expected to fail |

A single modern mainframe might have hundreds of cores, terabytes of memory, and dedicated I/O processors, all engineered for extreme reliability **in one box**. A hyperscaler datacenter is a very large number of unremarkable servers, none of which is expected to be reliable, networked together by software that assumes failures constantly.

So when you rent a cloud instance you're getting a slice of a normal commodity server, not a piece of a mainframe.

Once that landed, a lot of things I'd read separately snapped into place. Distributed consensus, replication, and the whole apparatus of "design for failure" exist *because* the scale-out bet is that hardware will fail and software must absorb it. The mainframe made the opposite bet: make the hardware not fail. Both work. They're solutions to the same reliability requirement at different layers, and the entire culture of each world follows from which layer it chose.

---

## 3. How they actually coexist

The real-world pattern in a large institution is both, split by workload:

| on the cloud | on the mainframe |
|---|---|
| mobile app and website backends | the core ledger — the system of record |
| analytics, machine learning, fraud models | real-time transaction settlement |
| development and test environments | overnight batch reconciliation |
| anything new, elastic, or bursty | the decades-old code that cannot fail |

The concrete version: when you tap your bank's app, the front end is probably cloud-native, and the actual debit against your account often still lands on a mainframe transaction system underneath.

I like this example because it dissolves the framing I'd arrived with. There is no migration event to wait for. The two are already layered, and have been for years, with the boundary drawn along *what kind of failure each side can tolerate.*

---

## 4. Why not migrate everything?

People are genuinely trying, and it's instructive that it's hard:

**Migration is risky at a scale that's hard to convey.** These are multi-year, hundred-million-dollar programmes, and several high-profile attempts have been abandoned or rolled back publicly.

**The economics aren't automatic.** Cloud's pricing advantage is strongest for *variable and bursty* load — you pay for what you use, and elasticity is the product. For steady, predictable, permanently maxed-out throughput, a fully loaded mainframe can be cost-competitive, because the elasticity you're paying a premium for is worth nothing to you.

That's the sharpest business lesson here and it generalizes past mainframes: **the cloud's core value proposition is elasticity, so workloads with no variance capture the least of it.**

**And regulatory and risk inertia are rational, not merely cultural.** "It has worked flawlessly for 25 years" is a hard argument to override when the downside is a national payment network going down. The expected-value calculation genuinely favours not touching it.

The honest trend is hybrid rather than replacement. Both sides have conceded it — the cloud vendors sell migration tooling *and* partner with mainframe operators; the mainframe vendor pushes hybrid hard and has made its machines run the same container tooling as everything else, so the mainframe becomes a node in a cloud architecture rather than an island outside it.

---

## 5. What I took away

**"Obsolete" and "unfashionable" are different claims**, and I'd merged them. Nothing has displaced mainframes from high-stakes, high-volume transaction processing. What's true is that all the *growth* is elsewhere, the talent pool is aging, and they're expensive — none of which is the same as being outcompeted at the job they do.

**Scale-up versus scale-out is one of the more useful axes I've picked up.** It predicts where reliability engineering lives (hardware or software), what failure model the software assumes, and what the cost curve looks like. And it explains why "the cloud" is not the descendant of the mainframe but its architectural opposite.

**Elasticity is the cloud's actual product.** Not cheapness, not scale — the ability to not pay for capacity you aren't using. Which means the workloads that benefit least are precisely the constant, predictable, maximum-throughput ones. That reframing explains the migration decisions that otherwise look like inertia.
