# Computer architecture — why CPU, RAM, and storage all exist

*Learned on March 26, 2026. Started with a deceptively simple question — why can't a computer just be a CPU and a hard disk? Why does RAM exist? The conversation went 24 messages deep, into Turing machines, automata theory, the nature of computation itself, and circled back to why all of this matters for semiconductor trading.*

---

## The speed mismatch problem

A CPU executes instructions by flipping transistors — tiny switches etched into silicon at nanometer scale. Electrical signals travel across these at near-light speed. A modern CPU can complete an operation in roughly 0.3 nanoseconds (one clock cycle at 3GHz). The entire CPU die is maybe 1-2cm across, so signals do not travel far.

A hard disk stores data by magnetizing tiny regions on a spinning metal platter. To read a byte, you need to physically move a mechanical arm to the right track, then wait for the platter to rotate to the right sector. That takes about 5-10 milliseconds — roughly **30 million times slower** than a CPU cycle.

If the CPU had to fetch every instruction and every piece of data directly from the hard disk, it would spend 99.9999% of its time waiting. It is like a Formula 1 engine connected to wheels via a horse-drawn cart.

Why not just make hard disks faster? Because the speed comes from persistence. Hard disks and SSDs use physical and chemical mechanisms to retain data without power — magnetic orientation or trapped electrons. These mechanisms are inherently slow to read and write compared to pure electrical switching. You are trading speed for non-volatility.

RAM solves this impedance mismatch. DRAM stores bits as charge in tiny capacitors. No mechanical parts, no magnetic fields — just electrons in a circuit. This gets you roughly 50-100 nanosecond access times, about 100,000 times faster than a hard disk. The tradeoff: capacitors leak charge, so the data disappears when power is cut. That is why it is "volatile."

The architecture is a speed hierarchy:

```
CPU registers (~0.3ns, tiny, volatile)
  → L1/L2/L3 Cache (~1-10ns, small, volatile)
    → RAM (~50-100ns, medium, volatile)
      → SSD (~0.1ms, large, persistent)
        → HDD (~5-10ms, huge, persistent)
```

Each layer is slower but bigger and more persistent. No known physical medium is simultaneously fast, large, and non-volatile. The three-tier architecture is a direct consequence of this physical reality.

## Why the CPU cannot exist alone

This was my next question: why not just have a CPU? Why is memory needed at all?

The answer goes to the foundation of computer science. **Computation IS state transformation.** Think about what a CPU actually does. It takes some input bits, applies a logical operation (AND, OR, ADD), and produces output bits. But those output bits need to go somewhere so they can be used as input to the next operation.

Even the simplest useful computation — adding a list of 10 numbers — requires you to hold a running total while you process each new number. That running total is memory. Without it, each operation is isolated and stateless. You would have a glorified calculator that can do one operation but cannot chain them.

This is not an engineering limitation — it is mathematical. A Turing machine (the theoretical foundation of all computation) has two components: a head that reads and writes (the processor) and a tape that stores symbols (memory). Remove the tape and you get a finite automaton, which is provably less powerful — it literally cannot compute things a Turing machine can.

"But the CPU has registers — aren't those memory?" Exactly. They are. A CPU already contains memory. Registers are tiny, ultra-fast storage cells right next to the logic gates. A modern CPU has maybe 16-32 general-purpose registers, each holding 64 bits. That is roughly 256 bytes.

So the real question becomes: why not just put MORE registers inside the CPU? Why not make it 16GB of registers instead of 256 bytes?

Physics says no. Each register bit is built from about 6 transistors (SRAM). 16GB of registers would require roughly 860 billion transistors just for storage — the entire CPU today has maybe 10-50 billion transistors total. The die would be enormous. And the larger the die, the longer signals take to travel across it, the slower everything runs. You would also hit thermal limits and manufacturing yield problems (bigger die means higher probability that a defect makes the whole chip useless).

External memory is not a design choice. It is a physical inevitability.

## SRAM versus DRAM: what they actually are at the circuit level

This is where I went to the transistor level, which connects directly to my family's semiconductor business.

**SRAM (Static RAM)** stores a bit using two inverters connected in a loop. An inverter outputs the opposite of its input. Connect two in a circle: the output of inverter A feeds the input of inverter B, and the output of B feeds the input of A. This creates a stable feedback loop — the circuit locks into one of two states. It will sit there as long as power is on, without any refresh needed, because the loop actively sustains itself. Add access transistors and you get a full SRAM cell: **6 transistors per bit**.

**DRAM (Dynamic RAM)** stores a bit using just **1 transistor + 1 capacitor**. A capacitor is two metal plates separated by an insulator — it holds charge. Charged equals 1, discharged equals 0. The transistor is a gate that controls access.

The problem: capacitors leak. The charge drains away in milliseconds through imperfections in the insulator. So a DRAM controller must read every cell and rewrite it roughly every 64 milliseconds — this is called **refresh**, and it happens thousands of times per second across the entire chip.

| | SRAM (registers, cache) | DRAM (main memory) |
|---|---|---|
| **Transistors per bit** | 6 | 1 (+ capacitor) |
| **Density** | Low — big cells | High — tiny cells |
| **Speed** | ~1-2ns | ~50-100ns |
| **Needs refresh?** | No | Yes (every ~64ms) |
| **Cost per GB** | Extremely expensive | Cheap |

SRAM is fast and stable but physically large per bit. DRAM is dense and cheap but slow and leaky. Neither is "better" — they optimize for different points on the speed-density curve. This is why the memory hierarchy exists: SRAM for the cache layers close to the CPU, DRAM for main memory.

## What "speed" really is: the Turing machine perspective

I wanted to understand speed more fundamentally. The reframing that clicked for me came from thinking about Turing machines.

In a pure Turing machine, there is no "speed." There is a head and a tape. Each step, the head reads one cell, consults its transition table, writes a symbol, moves one cell left or right, and changes its internal state. Steps are discrete and abstract — no clock, no nanoseconds. Just step after step.

Now realize it physically, and something new appears. When you build a Turing machine out of actual matter, each transition takes time. And here is the critical insight: **not all time is spent computing.**

Imagine the Turing machine head needs to add two numbers written far apart on the tape. The head must physically shuttle back and forth — move left 10,000 cells, read a digit, move right 10,000 cells, write something. Most of the steps are not doing the addition. They are just moving to where the data is.

> Speed is access time. It is the cost of bridging the gap between where the logic is and where the state is.

The computation itself is almost free. What you are actually paying for, almost always, is fetching the state to where the computation happens. The entire memory hierarchy — registers, SRAM cache, DRAM, SSD, hard disk — is humanity's engineering response to one problem: the tape is too long, and the head can only be in one place at a time. Each layer is a strategy for keeping the most likely-to-be-needed state as close to the head as possible.

## Automata: the hierarchy that IS computation theory

The word "automaton" comes from Greek — *automatos*, meaning "self-moving." In computation theory, an automaton is a machine that follows rules without human intervention. You give it input and it processes that input step by step according to fixed rules.

What matters is the hierarchy:

**Finite automaton** — has a finite number of states, reads input one symbol at a time, transitions between states. No memory, no scratch paper. It can recognize patterns like "does this string end in 01?" but it cannot count. It literally cannot determine if a string has equal numbers of 0s and 1s, because counting requires unbounded memory and it has none.

**Pushdown automaton** — same as a finite automaton, but with a stack (a single pile where it can push and pop symbols). This gives it limited memory. Now it can count, match parentheses, verify balanced brackets. But it can only access the top of the stack.

**Turing machine** — a finite automaton with a full read-write tape. Unlimited, random-access memory. This is where you get universality.

Each level is strictly more powerful than the previous one, and the only difference between them is **how much memory they have access to**. The processing rules are the same kind of thing — finite states, deterministic transitions. The only variable is the tape. Memory is not an accessory to computation. The hierarchy of automata proves that memory is the axis along which computational power increases.

## The infinite tape problem: is my MacBook actually a Turing machine?

A universal Turing machine has an infinite tape. My MacBook Air has 24GB of RAM and some SSD storage. Finite. My brain has roughly 86 billion neurons. Huge, but finite.

Strictly speaking, neither is a universal Turing machine. Both are, in mathematical terms, finite automata — very large ones, with an astronomically large number of states, but finite automata nonetheless. There exist computations a Turing machine can do that my MacBook literally cannot, because it would run out of memory before finishing.

So why does everyone call them computers? Because the distinction is real but practically irrelevant for almost everything. My MacBook has roughly 2^200,000,000,000 possible states. The class of problems that require more states than that is so exotic that for every real-world task, the MacBook behaves as if it had an infinite tape.

David Deutsch reframes it physically rather than mathematically: if I run out of memory, I can plug in an external drive. If that fills up, I can buy another. There is no law of physics that places a hard upper bound on how much memory I can eventually access. The tape is not infinite — it is unbounded in principle. You can always add more. The constraint is engineering and resources, not physics.

## What computation actually is

This was the deepest part of the conversation, and the part I keep thinking about.

Computation is not something that emerges when matter gets complex enough — like temperature emerging from molecular motion. Computation is what matter does. Every physical system is transforming configurations of matter according to rules. State transitions governed by rules. That is exactly what a Turing machine does.

Turing did not invent a new kind of process. He formalized something that was already happening everywhere in nature. A river flowing downhill, a crystal forming, a star fusing hydrogen — these are all physical systems evolving from one state to the next according to the laws of physics.

But a rock sitting in the sun is "computing" only in a trivial sense. The profound thing Turing showed is that a very specific, very simple arrangement of matter — a tape with symbols, a head with finite states, a transition table — can simulate any physical process that any other arrangement of matter performs. That is universality.

Deutsch's version — the Church-Turing-Deutsch principle — goes further: every physical process can be simulated by a universal computing machine operating by finite means. This is not a mathematical statement. It is a physical claim about the nature of reality. It says the laws of physics are computable.

> Computation is not something that emerges when matter gets complex enough. It is what matter was doing all along. What emerges with complexity is universality — the ability of one physical system to simulate any other.

## Connecting it back to semiconductor trading

I asked whether all of this deep understanding would help me make money in semiconductor trading. The honest answer: indirectly.

The margins in trading come from information asymmetry — identifying that a particular SKU is about to become scarce before the market prices it in. Understanding that DRAM is a 1T-1C cell that needs refresh every 64ms will not tell me a specific DRAM SKU is about to go into allocation.

But deep technical understanding creates edge in three ways. First, pattern recognition across product categories: if I understand why DDR5 exists (higher data rates per pin, on-die ECC compensating for smaller capacitors), I can predict which DDR5 SKUs will face demand spikes when a new server platform launches. Second, customer credibility: OEM engineers can tell within 30 seconds whether I understand the component or I am just flipping part numbers. Third, BOM reading speed: when I understand the architecture, I can parse a bill of materials and spot the constrained components far faster.

The knowledge is a slow-compounding asset. It does not replace the pipeline — but it makes every interaction with the pipeline more informed.

---

*Resources I want to study next: Sipser's Introduction to the Theory of Computation for the formal automata framework, Petzold's Code for the physics-to-computation bridge, and The Annotated Turing for Turing's original reasoning. See also: [SRAM vs DRAM at the circuit level](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md) for how memory hierarchy plays out in GPU packages.*
