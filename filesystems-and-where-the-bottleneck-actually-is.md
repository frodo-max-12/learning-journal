# Filesystems, and Finding Where the Bottleneck Actually Is

**Context:** I plugged in an external SSD to move some very large files off my laptop, and hit three questions in a row I couldn't answer: which format should I choose when erasing it, why did copying 141 GB take eight minutes, and does that mean all the processing work I planned to do on those files will be equally slow? The third question turned out to have the most useful answer, because my reasoning about it was wrong in a way that generalizes.

---

## 1. Choosing a filesystem

The formatting dialog offers several options and gives you no basis for choosing. The real trade-off is **cross-platform compatibility versus everything else**:

| factor | APFS (macOS-native) | exFAT (universal) |
|---|---|---|
| large-file read speed | notably faster | slower |
| Unix permissions | preserved | **not supported** |
| symlinks and hard links | work | **broken** |
| journaling | yes | no |
| crash safety mid-write | safe | can corrupt |
| Windows compatibility | no | yes |

exFAT exists for one reason: to be readable by everything. It achieves that by being minimal, and the minimalism is what costs you.

The permissions point is the one that decides it for actual work. **exFAT has no concept of Unix file permissions**, so any script you write to the drive loses its executable bit, virtual environments break, and tooling that expects permission bits behaves strangely. Symlinks silently fail rather than erroring, which is worse. And with no journaling, a crash or unplug mid-write can corrupt the volume rather than losing just the in-flight file.

So the rule is simply: **exFAT only if the drive genuinely needs to be readable on Windows.** If it's working storage for one machine, use the native filesystem — the compatibility you're buying with exFAT is compatibility you aren't going to use, and you're paying for it in speed, safety, and correctness.

A journaling filesystem writes its *intent* before performing an operation, so an interrupted write can be rolled back or completed on the next mount instead of leaving the volume in an undefined state. That's the same durable-state-versus-in-flight-state idea that shows up everywhere — write down what you're about to do, so that being interrupted is recoverable.

---

## 2. "Why is this copy so slow?" — it wasn't

141 GB in about 8 minutes works out to roughly **300 MB/s**.

That's not slow. USB 3.0 tops out around 350–400 MB/s in practice, so I was getting 75–85% of the theoretical ceiling of the link.

The genuinely useful part was locating *which* component set that ceiling. The SSD inside the enclosure is natively capable of many times that. The laptop's ports support far more. **The bottleneck was the plastic box around the drive** — a USB 3.0 enclosure, sitting between two components each capable of much more.

| link | practical speed | time for 141 GB |
|---|---|---|
| USB 3.0 enclosure | ~300–400 MB/s | 6–8 min |
| USB 3.2 Gen 2 | ~1,000 MB/s | ~2.5 min |
| Thunderbolt / USB4 | ~2,800 MB/s | ~50 sec |

**A chain runs at the speed of its slowest link, and the slowest link is often the least interesting component.** I'd been mentally attributing the speed to the SSD (expensive, branded, specified in the product name) and the laptop (new, fast). The determining factor was the adapter, which has no marketing and which I'd never thought about.

Two smaller contributors worth knowing: many small files copy far slower than one large file of the same total size, because each file costs directory-entry and metadata work regardless of its size. And a journaling filesystem adds a few percent overhead on writes — which is the price of the crash-safety above, and worth it.

---

## 3. The question I got wrong

My follow-up was the natural one: if moving the data is this slow, will processing it be slow too?

**No — and the reason is that they're bottlenecked by completely different things.**

- **Bulk copy is pure I/O.** No computation at all, just moving bytes. Speed equals whatever the slowest link can push: ~400 MB/s.
- **Parsing is mostly CPU.** Disk reads happen in bursts; most of the wall-clock time goes into actually interpreting the data — parsing structure, building data structures, matching patterns, deduplicating.

And the numbers invert:

```
what the drive can deliver:   ~400 MB/s   ← faster than needed
what the parsing consumes:    ~50–100 MB/s ← the actual constraint
```

During processing **the disk sits idle most of the time, waiting for the CPU to catch up.** A faster enclosure would speed up bulk transfers and do essentially nothing for the processing work.

That's the generalizable mistake, and I think it's a common one. I had observed a bottleneck in one operation and assumed it was a property of *the setup*. It's a property of *the operation*. Two tasks touching the same data through the same cable can be limited by entirely different components, and optimizing the one you just measured can be completely irrelevant to the one you're about to run.

The habit I took from it: before spending anything to fix a bottleneck, ask **which resource is actually saturated during the workload I care about** — not the one I happened to be watching. The instinct to answer "the drive is slow, get a faster drive" was reasonable, fast, and would have bought nothing.

---

## 4. What I took away

**Filesystem choice is a decision about semantics, not just speed.** Permissions, symlinks, and journaling either exist or don't. Speed differences are recoverable by waiting; a filesystem that can't represent an executable bit will break tooling in ways that look like unrelated bugs.

**Always identify the limiting link by name.** "It's slow" isn't a diagnosis. Drive, enclosure, cable, port, filesystem, and CPU are six separate candidates, and the answer is frequently the cheapest, least visible one.

**Measure the workload you care about.** A benchmark of the wrong operation is worse than no benchmark, because it comes with confidence attached.
