# The Physical Limits of Computation — Lloyd's Ultimate Laptop, and What Actually Runs Out

**Context:** I'd been carrying a worry from *The Beginning of Infinity*: progress is supposed to continue without bound, but progress needs computation, and computation needs physical resources. At some point don't you hit a wall? I asked what the actual limits are, whether Deutsch has an answer, and whether Frank Tipler's immortality argument is what I remembered it being. Along the way I caught the explanation being sloppy about something, and the correction turned out to be the most useful part.

---

## 1. The catch: it's memory *and* time

The claim I pushed back on was that the analogy to a universal Turing machine is mainly about *speed*. It isn't. **A UTM assumes an infinite tape — that's unbounded memory — and unbounded run-time.** Any physical realization is bounded on both, by two different physical laws:

| bound | law | what it limits |
|---|---|---|
| **memory** | Bekenstein–Hawking | maximum bits storable in a region — scales with the region's *surface area* at Planck resolution |
| **speed** | Margolus–Levitin | maximum operations per second for a system with energy `E` above its ground state: `2E/πℏ` |

The surface-area part of the memory bound is the strange one. Information capacity doesn't scale with volume, as you'd expect from stacking storage in three dimensions — it scales with the *boundary area*. A one-litre region tops out around 10⁶⁷ bits, and even that is only saturated if the litre is a black hole. Ordinary matter is far below it.

This is why the correction matters rather than being pedantry. **The two bounds bite at different times.** A computer with N bits of memory can only distinguish 2^N states, so simulating something with K bits of state requires N ≥ K, full stop — no amount of extra time helps. "The universe simulating itself in full fidelity" fails for *memory* reasons long before it fails for *speed* reasons.

Deutsch's own careful formulation builds this in: any **finitely realizable** physical system can be simulated by a universal quantum computer. The "finitely realizable" caveat is doing exactly this work. Universality was settled *qualitatively* long ago; quantitatively we are memory- and speed-bounded, and both bounds matter for the question I was actually asking.

---

## 2. Lloyd's ultimate laptop

Seth Lloyd's 2000 paper computes the absolute physical limits for a 1 kg, 1 litre computer — not an engineering estimate but a bound from physics.

**The speed bound.** The Margolus–Levitin theorem says that for a quantum system with average energy `E` above its ground state, the minimum time to evolve into an *orthogonal* (i.e. reliably distinguishable) state is `t ≥ πℏ/2E`.

The intuition is what makes this feel like physics rather than numerology: to perform a logical operation, the system must move into a state you can tell apart from the one it was in. Orthogonal states are the most distinguishable ones there are. The energy–time uncertainty relation bounds how fast that transition can happen. **More energy buys more operations per second, and that's the only thing that does.**

For 1 kg you take `E = mc²`, and the number that falls out is roughly **10⁵⁰ operations per second**.

Two things about that number changed how I think about it. First, it uses `mc²` — the bound assumes you convert the *entire mass* to usable energy. This isn't a laptop with a better battery; it's a kilogram operating as pure energy. Second, it doesn't care what the computer is *made of*, only how much energy it has. That's substrate-independence appearing as a physical bound rather than a philosophical claim.

**The memory bound** comes from the Bekenstein limit, and the same "1 litre" figure applies: around 10⁶⁷ bits, saturated only in the black-hole limit.

Which yields the picture I hadn't expected: the ultimate computer isn't a very good chip. **It's a black hole.** The physical configuration that maximizes computation per kilogram is matter compressed to its densest possible state — and every real computer is a compromise made because we'd like to read the answer out afterwards.

---

## 3. Tipler, and the one fully specified escape

I half-remembered Tipler claiming immortality requires ever-increasing compute. That's right, and the structure is worth stating because it's the only fully worked-out scenario in which *literally infinite* cumulative computation is achievable:

- The universe must be closed and recollapse. (Current cosmology disfavours this — which is the load-bearing weakness.)
- The final singularity is **anisotropic** — collapsing at different rates along different axes. The shear from that anisotropy is a source of arbitrarily large energy density as you approach it.
- A civilization harvests that shear energy to power computation. As proper time approaches the end, available energy per unit proper time *diverges*.
- Subjective time is measured in *operations experienced*, not seconds. So even though the physical time remaining is finite, the integral of operations-per-second over that time can diverge if the rate grows fast enough.

Infinite subjective experience inside finite physical time. And with literally infinite computation you can simulate every possible past mind — which is where the resurrection claim comes from, and where I'd get off the bus, since it quietly equates simulating someone with them.

So there are two ways the unbounded-progress picture survives:

- **Deutsch's open option** — future physics extends the cosmological compute bound somehow. Agnostic about mechanism, and consistent with his general stance that unsolved isn't unsolvable.
- **Tipler's specific mechanism** — the Omega Point, with a diverging integral in a closed recollapsing universe.

Almost everyone else thinks the picture hits a wall. Tipler is notable not for being likely but for being *specified* — he wrote down a scenario detailed enough to be checked against cosmology and found wanting, which is more than a vague optimism offers.

---

## 4. What I actually updated

**"Compute" is two resources, not one, and they fail differently.** Speed is bounded by energy; memory is bounded by area. Running out of time means waiting longer; running out of memory means the computation is *impossible*, not slow. I had been treating "more compute" as a single dial.

**The bounds are absurdly far away, and that's the practical answer to my worry.** All the computers on Earth combined don't approach a single kilogram operated at the Lloyd bound. Whatever limits progress in any timeframe I can reason about, it isn't physics — it's knowledge, energy economics, and engineering. The wall exists and is not the thing to worry about.

**Being wrong precisely is worth more than being right vaguely.** Tipler's scenario is probably false, and it's *checkable* — closed universe or not, diverging integral or not. That's a better contribution than an untestable assurance that something will turn up. It's the hard-to-vary criterion applied to a cosmological claim: a specific mechanism that fails for a specific reason beats a flexible optimism that can absorb any outcome.

**And the correction was the best part of the exchange.** I caught a real omission — memory, not just time — and it wasn't a detail. It changed which bound binds first, and it's the reason "simulate the universe inside the universe" is impossible in a way that has nothing to do with being fast enough.
