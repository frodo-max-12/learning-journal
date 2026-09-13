# Why SRAM Costs 1000× More Than DRAM — and the Two Things Called "Leakage"

**Context:** I'd learned that an SRAM cell is 6 transistors and a DRAM cell is 1 transistor + 1 capacitor. So SRAM should cost roughly 6× more per bit. The actual retail gap is **100–1000×**. My question was blunt: it's just six transistors, we miniaturized everything else, what's the big deal? The answer decomposes into three multiplying effects, none of which is the transistor count — and chasing it produced a second correction where an intuition of mine was right in a way that stopped being true.

---

## 1. Where the gap actually comes from

| effect | contribution |
|---|---|
| silicon area per bit (cell size) | ~10–15× |
| wafer cost (logic node vs DRAM node) | ~5–8× |
| yield, packaging, margin stack | ~2–4× |
| **combined** | **~100–500×**, stretching further at retail |

The transistor-count intuition only touches the first row, and even there it's wrong.

---

## 2. Cell area — the vertical capacitor is the trick

I assumed 6 transistors vs 2 components means roughly 6× the area. It's more like 10–15×, and the reason is a piece of manufacturing cleverness I didn't know about.

**The DRAM capacitor is built vertically, not horizontally.**

- The single transistor sits flat on the silicon surface, consuming horizontal area.
- The capacitor is etched as a deep vertical trench, or built as a tall stacked column *above* the transistor — typically 50–100× taller than it is wide.
- So in horizontal silicon area, **the capacitor takes essentially zero footprint.**

A DRAM cell therefore occupies roughly the area of one transistor, despite having 1T+1C of functionality. SRAM's six transistors all sit side by side on the surface, all consuming area.

Production numbers make it concrete:

| memory | node | cell area |
|---|---|---|
| SRAM | 5nm logic | ~0.021 μm² |
| SRAM | 3nm logic | ~0.0199 μm² |
| DRAM | ~10nm-class | ~0.0019 μm² |

Two things jump out. DRAM is about **10× denser** at cell level, not 6×. And SRAM cells barely shrank between 5nm and 3nm — about 5%. That second number is quietly one of the most consequential facts in modern chip design: **SRAM has largely stopped scaling.** Logic keeps shrinking, on-chip cache doesn't, so cache eats an ever-growing share of every new die.

---

## 3. The bigger factor: they aren't made in the same factories

This is the part I had no idea about. **SRAM and DRAM are not fabricated on the same processes at all** — the two have diverged so far they're now mutually incompatible.

**SRAM lives on logic nodes**, the same wafers as CPUs and GPUs. Those processes are optimized for fast transistors with high drive current, many metal layers (15–20 for routing), cutting-edge lithography, and tight logic design rules. A leading-edge logic wafer runs roughly $17,000–23,000, and the next node is heading past $30,000.

**DRAM lives on dedicated DRAM nodes** at the memory makers. Those processes are optimized for something completely different: high-aspect-ratio etching for those deep capacitor trenches (50:1), specialized high-k capacitor dielectrics, far fewer metal layers (4–6), and transistors that are *slow but low-leakage*, which is fine for the job. A DRAM wafer runs roughly $3,500–5,000.

Run the arithmetic per wafer and the gap stops being mysterious:

| | SRAM @ 3nm logic | DRAM @ 10nm-class |
|---|---|---|
| cell area | 0.020 μm² | 0.002 μm² |
| bits per wafer (theoretical) | ~3.5 trillion | ~35 trillion |
| wafer cost | ~$22,000 | ~$4,000 |
| **cost per Gbit** | **~$6.30** | **~$0.11** |

**~57× at the factory gate**, before yield, packaging, test, and every margin in the chain.

So "why can't we just miniaturize SRAM like everything else?" has a precise answer: SRAM *is* on the most miniaturized process that exists. That's the problem. It's riding the most expensive wafers on earth, and the wafer price is rising faster than the cell is shrinking.

And you can't fix it by mixing. A logic process has no high-aspect-ratio capacitor step, so you can't build efficient DRAM cells on it; a DRAM process has slow transistors and few metal layers, so you can't build a fast processor on it. The two optimization targets are genuinely opposed.

---

## 4. The correction: two different things are called "leakage"

Then I hit something that didn't add up. I was told SRAM has static power leakage — but *static* is right there in the name. Static RAM shouldn't leak. DRAM is the one that leaks, because a capacitor's charge drains away.

That intuition is correct, and it used to be the whole story. There are **two entirely different physical phenomena both called leakage**, operating on different timescales through different mechanisms:

| phenomenon | what leaks | timescale | affects |
|---|---|---|---|
| **storage-capacitor leakage** (the "dynamic" problem) | charge drains off the DRAM capacitor | ~64 ms | DRAM only |
| **transistor leakage** (the modern CMOS problem) | current flows through nominally "off" transistors | continuously | both |

**What "static" actually means.** SRAM's cell is a flip-flop of cross-coupled inverters — electrically *bistable*. Whichever state it's latched into, it stays there indefinitely while powered. The stored value doesn't decay. That's the retention property the name refers to, and on that axis the intuition is exactly right.

DRAM's capacitor drains through three paths — junction leakage at the reverse-biased PN junction, subthreshold leakage through the not-quite-off transistor, and dielectric leakage through the imperfect insulator. Combined, they empty the cell in tens of milliseconds, which is why DRAM needs refresh circuitry reading every row and writing it back roughly every 64 ms. That refresh requirement *is* the "dynamic."

**What changed.** As transistors shrank from ~250nm to ~3nm, the physics of "off" changed:

- The gate oxide is now a few atomic layers thick, so electrons **quantum-mechanically tunnel** through it even with the gate off — gate leakage.
- The channel is so short that "off" doesn't mean off; current still flows source to drain — subthreshold leakage.
- Both grow *exponentially* as nodes shrink.

A single 6T SRAM cell at 5nm leaks on the order of 10–100 picoamps continuously. Negligible alone. But scale it: a terabyte of SRAM at 3nm is ~8 trillion cells, and at ~50 pA each that's roughly **400 amps of leakage current — several hundred watts of power to store data that nobody is touching.**

So both parts are true, and the naming is a historical artifact:

> SRAM is static in the sense the 1970s meant — **the bit doesn't decay**. It is not static in the sense modern process nodes forced on us — **the transistors holding the bit draw current continuously**.

The word was coined to describe a *retention* property and is now routinely read as a *power* property. Those were the same claim at 250nm. They came apart somewhere around 90nm and nobody renamed anything.

---

## 5. What I took away

**"Why is X expensive?" is almost never answered at the schematic level.** The 6-vs-2 transistor comparison is true and explains under a tenth of the gap. The rest lives in geometry (a capacitor built upward), in manufacturing (two incompatible process families), and in economics (wafer prices set by a completely different market). Reading a circuit diagram tells you what something *does*, not what it *costs*.

**Density and cost are different questions.** SRAM is fast because it's on the fastest process, and expensive for exactly the same reason. Those aren't two facts; they're one fact seen from two sides.

**A word can outlive the distinction it was coined to draw.** "Static" was precise when it was introduced and is now actively misleading — which is why my objection was reasonable and the answer was still yes-it-leaks. When a technical term produces a confident-and-wrong intuition, the useful move is to ask *when* the word was coined and whether the world it described still exists.
