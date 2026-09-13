# The Memory Hierarchy — From Registers to Spinning Disks

**Context:** I was watching a first-principles computer-architecture playlist and asked what I thought was a small question: what's the difference between a register and RAM? The honest answer required laying out the whole ladder, and once it was laid out, two things I'd been treating as separate topics — "why does a CPU have cache" and "why is my SSD not just more RAM" — turned out to be the same question asked at different rungs.

---

## 1. The ladder

| level | technology | volatile? | latency | typical size | visible to the programmer? |
|---|---|---|---|---|---|
| registers | flip-flops wired into the ALU | yes | ~0.25 ns (1 cycle) | ~2 KB | **yes — by name** |
| L1 cache | fastest SRAM | yes | ~1 ns (3–5 cycles) | 64–128 KB per core | no — transparent |
| L2 cache | SRAM | yes | ~4 ns (10–20 cycles) | 0.25–4 MB per core | no |
| L3 cache | denser SRAM | yes | ~12 ns (30–60 cycles) | 8–128 MB shared | no |
| main memory | DRAM | yes | ~70 ns (200–300 cycles) | 16 GB – 1 TB | **yes — by address** |
| SSD | NAND flash | **no** | ~100 μs | 256 GB – 8 TB | through the OS |
| HDD | magnetic disk | **no** | ~10 ms | 1–20 TB | through the OS |

Two patterns run down the whole table.

**Each level is roughly 10× slower and 10–100× larger than the one above.** That's the entire reason the hierarchy exists: **no single storage technology is simultaneously fast, dense, and cheap**, so you stack several technologies each optimized for a different point on the trade-off curve and paper over the seams.

**The span is absurd.** A register access is 0.25 nanoseconds; a hard-disk seek is 10 milliseconds. That's a factor of **forty million**. If a register access took one second, the disk seek would take over a year. Every piece of cleverness in caching, prefetching, and scheduling exists to keep you away from the bottom of that table.

---

## 2. Registers — named storage inside the arithmetic unit

A register is a fixed, hardwired storage location built directly into the CPU's execution units. Physically it's a small set of flip-flops — the same kind of cell as SRAM — wired straight into the ALU's inputs.

Four properties that separate them from everything below:

- **Fixed in number and named by the instruction set.** x86-64 has exactly 16 general-purpose 64-bit registers, plus vector registers. ARM64 has 32. RISC-V has 32. Software cannot create more — the architecture defines them.
- **Addressed by name, not by address.** `MOV RAX, 5` says "put 5 in the register called RAX." There's no memory address involved; RAX is a specific physical location.
- **Tiny.** The whole register file is on the order of a couple of kilobytes.
- **One cycle to access**, because the registers are wired directly to the ALU inputs — reading them is part of the same electrical path that does the arithmetic.

The analogy that made it click: **registers are the few items on your desk right now, and the ALU is your hands** — your hands can only manipulate what's already on the desk. Everything else in the table is about how quickly you can get something onto the desk.

That's also why the *count* is architecturally load-bearing. Too few registers and the CPU spends its life shuttling values to and from memory; too many and every instruction needs more bits to name one, and context switches get expensive.

---

## 3. Cache — the level nobody asked for

The sharpest distinction in the whole table:

> **Registers are managed by software. Caches are managed by hardware.**

The compiler decides what goes in which register. Nothing decides what goes in L1 except the CPU itself — not the programmer, not the compiler, not the OS. Cache is *automatic*, and it's automatic because it has to be: it must react to what the program is actually touching at runtime, which nobody knows in advance.

**L1** sits within millimetres of the execution units, is per-core, and is almost always split in two — an instruction cache and a data cache. Splitting them lets the CPU fetch the next instruction and load data *in the same cycle* without contention, and lets each half be tuned for its access pattern.

**L2** is larger, still usually per-core, and unified. **L3** is bigger again and shared across cores, which also makes it the mechanism by which cores see each other's recent writes.

This whole apparatus exists to hide the DRAM latency in the row below. ~70 ns doesn't sound like much until you convert it: at 4 GHz that's **~280 cycles of doing nothing**. Modern CPUs execute several instructions per cycle, so a single cache miss to main memory costs on the order of a thousand instruction slots. The cache hierarchy is a bet that the data you want next is data you recently wanted — and the bet is correct often enough that the whole edifice works.

---

## 4. The most important line in the table isn't SRAM vs DRAM

I'd assumed the big divide was fast-vs-slow. It isn't. The deepest division in memory technology is **volatile vs non-volatile**:

| | meaning | examples |
|---|---|---|
| volatile | loses everything when power is removed | SRAM, DRAM, HBM |
| non-volatile | retains data without power, for years | NAND, NOR, EEPROM, ROM |

Everything from registers down through main memory is volatile. Pull the plug and it's gone — instantly, completely. Flash keeps its data for typically 10+ years with no power at all.

So flash isn't a faster disk or a slower RAM. **It's a different kind of thing**, and the line between rows 5 and 6 of the table is a change of category, not a change of degree.

---

## 5. How flash remembers with the power off

The mechanism is a **floating-gate transistor**, and it's the neatest piece of physics in the whole ladder.

A normal transistor has a gate that controls whether current flows. Flash adds a *second* gate buried inside the insulator stack — surrounded on all sides by oxide, electrically connected to nothing. That's the floating gate.

- **Write:** apply a high voltage to the control gate. Electrons **tunnel** through the thin oxide and get trapped on the floating gate, where they have nowhere to go.
- **Read:** apply a moderate voltage. Whether electrons are trapped changes the transistor's threshold voltage, so the cell either conducts or doesn't. That's your 1 or 0.
- **Erase:** high voltage, reverse polarity. The electrons tunnel back out.

Line the three technologies up and the difference is exactly *what physically holds the bit*:

| | what holds the bit | how long |
|---|---|---|
| DRAM | charge on a capacitor | milliseconds — needs refresh |
| SRAM | a state in a powered feedback loop | as long as power is on |
| flash | charge trapped behind an insulator | a decade, unpowered |

The insulator that makes flash non-volatile is also why writing is slow and why cells wear out: you're forcing electrons through a barrier designed to stop them, and every pass damages it slightly.

---

## 6. NAND vs NOR — same physics, different wiring

This is a *separate* axis from volatility, and it's purely about how the cells are connected.

**NOR flash** wires each cell directly to the bit line, so every cell is individually addressable. Random reads at ~50–100 ns — close to DRAM. But slow writes, slow erases, low density, high cost per bit.

**NAND flash** wires cells in series strings, which is what makes it dense and cheap — but you read and write in pages and erase in blocks, never a single byte.

The property NOR has that NAND doesn't is the one that matters: **you can execute code directly out of NOR**, byte by byte, with no buffering. That's called execute-in-place, and it's why NOR holds boot firmware — a computer has to start running *before any DRAM has been initialized*, so the boot code must live somewhere the CPU can read like memory.

Which resolves something I'd wondered about vaguely: why does a machine with a huge fast SSD still have a small separate firmware chip? Because at power-on there is no SSD driver, no memory controller, and no OS. Something has to be directly executable at the first instruction, and that job goes to the one flash architecture that can be read like RAM.

The same logic puts NOR in microcontrollers, automotive controllers, and industrial equipment — anywhere the firmware must be directly executable and reliability beats density.

---

## 7. What I actually took away

**The hierarchy is one idea applied repeatedly.** Every adjacent pair of rows is the same bargain: the faster thing is too expensive to be big, so keep the hot subset there and the rest one level down, and make the boundary as invisible as you can. Registers-vs-cache, cache-vs-DRAM, DRAM-vs-SSD, SSD-vs-disk — same trade, four times, different constants.

**"Visible to the programmer" is the column I'd have skipped and shouldn't.** Registers are named by software, cache is invisible and automatic, main memory is addressed explicitly, storage is reached through the OS. That column tells you *who is responsible for placement* at each level, which is the practical thing you need to know.

**Category divisions hide inside continuous-looking tables.** The ladder looks like a smooth gradient from fast to slow, and one row in the middle is actually a change of physics — from "a bit is a state that exists while energized" to "a bit is charge locked behind an insulator." I'd been reading the table as one axis when it's two.
