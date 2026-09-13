# Turing's 1936 Paper, Universality, and Which ICs Are Universal

*I read Turing's original 1936 paper — "On Computable Numbers, with an Application to the Entscheidungsproblem." Instead of just studying what the paper says, I explored what it looks like through David Deutsch's lens, then followed the thread into hardware: which ICs are universal, why GPUs exist if CPUs are also universal, and how to classify any part number in the world as universal or not.*

---

## Reading the actual paper

I had already studied the Turing machine, the halting problem, and the Church-Turing thesis in an earlier journal entry. This time I went to the source — Turing's actual 1936 paper. It is 36 pages, published in the Proceedings of the London Mathematical Society, written when Turing was 24.

The paper does three things:

1. **Defines what computation is.** Turing invents the simplest possible computing device — a tape, a head, a state, and a rule table. He calls it an "automatic machine." The rule is: "if I'm in state X and I see symbol Y, write Z, move left or right, switch to state W." That is the entire machine.

2. **Constructs a universal machine.** Every Turing machine can be described as a number (a "description number" — its rule table encoded as digits). Turing shows you can build one machine that reads any other machine's description and faithfully executes it. This is the stored-program computer. My MacBook is a physical realization of this idea.

3. **Proves the Entscheidungsproblem is unsolvable.** Using a diagonal argument — feeding a machine its own description to create a paradox — Turing shows there is no general algorithm that can decide whether any mathematical statement is provable.

What struck me reading the original: Turing's examples are extremely concrete. He gives actual rule tables for machines that print 010101... and 001011011101111... He works through every step. The paper is dense but not abstract — it is a builder showing you exactly how the machine works before proving what it cannot do.

## Deutsch's reading: everyone focuses on the wrong result

I then asked: how would David Deutsch explain this paper? His answer, based on what I have read of his work, is that the conventional telling is backwards.

Most accounts focus on the negative result — the halting problem, the limits of computation. Deutsch says the real discovery is the **positive** one: that a single, finite machine can perform any computation that any other machine can perform. That is the Universal Turing Machine.

Deutsch goes further. He says this is not just a mathematical result — it is a fact about physics. Computation is a physical process. The question "what can be computed?" is really "what do the laws of physics allow?" Turing's model assumes classical physics. Deutsch asked: what if we use quantum physics? That question led him to invent the quantum computer in 1985.

Deutsch also emphasizes that universality is a **threshold, not a spectrum**. Below it, machines do specific tasks. Cross it, and suddenly you can do everything that is computable. There is no gradual middle ground. A thermostat and a calculator are below the threshold. A Raspberry Pi and a supercomputer are above it. The difference between a Raspberry Pi and a supercomputer is speed. The difference between a calculator and a Raspberry Pi is kind.

> Deutsch's core move: take a result everyone treats as mathematics, insist it is actually physics, and show that reframing it unlocks something deeper.

## The practical question: which ICs are universal?

This led me to a concrete question I had never asked before. I deal with IC part numbers every day in the distribution business. If I were to list every IC in the world, how would I know which ones are universal and which are not?

The answer turned out to be a simple test: **can you write a program for it — with if/else, loops, and memory access?** If yes, it is universal. If the datasheet says "instruction set" or you need a compiler to use it, it is universal.

**Universal (laptop side of the line):**
- All microcontrollers: PIC16F877A (Microchip), MSP430 (TI), ATmega328 (Arduino), STM32
- All CPUs: Intel Core, ARM Cortex, AMD Ryzen
- All GPUs: NVIDIA, AMD — you write CUDA or compute shader code for them
- DSPs: TMS320 (TI) — programmable signal processors
- FPGAs: Xilinx, Altera — you can rewire the hardware itself

**Not universal (calculator side):**
- Timer ICs: NE555 — generates pulses, nothing else
- Op-amps: LM741 — amplifies signals, cannot be programmed
- Voltage regulators: LM7805 — one job
- Logic gate ICs: 74HC00 — fixed logic operations
- Sensor ICs: LM35, MPU6050 — measures something, no programmability
- Memory chips: EEPROM, SDRAM — stores data, does not process it
- Dedicated ASICs: Bitcoin miners, old calculator chips

The interesting edge case is calculators. A basic Rs. 200 office calculator has a dedicated ASIC — hardwired for arithmetic, not reprogrammable. Not universal. But a TI-84 graphing calculator has a Zilog Z80 general-purpose CPU inside. People have written games on TI-84s. The hardware is universal — it is the software that makes it look like "just a calculator."

> The cheap office calculator is limited by its hardware. The TI-84 is limited by its software. That distinction is everything.

## Why NVIDIA GPUs exist if CPUs are also universal

Both a CPU and a GPU are universal. Both can compute anything the other can. So why is NVIDIA a $3 trillion company?

Because universality answers "what can be computed?" but says nothing about "how fast?"

A CPU has roughly 12 powerful cores, each capable of complex, varied, sequential tasks. A GPU has roughly 18,000 simple cores, each capable of basic math. For AI training — which is millions of identical matrix multiplications done simultaneously — the GPU is absurdly faster. Not because it can compute things the CPU cannot, but because its architecture does this particular type of work in parallel.

The analogy that made it click: grading 10,000 exam papers. A CPU is 10 brilliant professors — they can grade papers, write essays, have nuanced discussions, but there are only 10 of them. A GPU is 10,000 school students who can only compare answers against an answer key — but you hand one paper to each student and they are all done simultaneously.

NVIDIA got into this position partly by luck. They built GPUs for gaming — which also requires the same simple math operation applied to millions of pixels simultaneously. Around 2012, AI researchers realized that matrix multiplication for neural networks is structurally identical to the math GPUs already do for rendering. NVIDIA then built CUDA (a programming language for GPUs), locked in the software ecosystem, and the rest is history.

> A CPU and a GPU are like two trucks that can both carry any cargo. But one is a single large truck, and the other is a fleet of 10,000 small vans. For one complicated delivery — use the truck. For 10,000 identical packages — use the vans.

---

*This entry connects to [Turing, Church, and the Halting Problem](theory-of-computation-turing-church-and-the-halting-problem.md) for the formal theory, [David Deutsch Reimagines Data Structures](david-deutsch-reimagines-data-structures.md) for more Deutsch-ian thinking, and [HBM and AI Accelerators](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md) for the hardware side of why GPU architecture matters.*
