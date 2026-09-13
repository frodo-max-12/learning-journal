# HBM and AI accelerators — what is actually inside a GPU package

*Learned on March 26, 2026. I was reading a SemiAnalysis chart showing that HBM accounts for 50-60% of manufacturing cost in Nvidia's chips, and realized I did not actually understand what was physically inside these packages. Turns out a "GPU" is not just a chip.*

---

## The first misconception: a GPU is not a chip

Before this conversation, when I heard "H100" or "Blackwell," I pictured a single chip — a slab of silicon with billions of transistors. That is wrong, or at least radically incomplete.

A modern AI accelerator is a **complete system-on-a-package**. For Nvidia's Blackwell architecture specifically:

The **B200** is a single GPU package containing two GPU dies (connected via a chip-to-chip link), plus multiple HBM3e memory stacks, all sitting on a silicon interposer substrate. The **GB200** goes even further — it is a "superchip" combining one Grace CPU plus two B200 GPUs on a single board.

So when someone says "the B200 costs X to manufacture," they are not talking about a single piece of silicon. They are talking about:

- **GPU dies** — the actual compute silicon with thousands of CUDA cores
- **HBM stacks** — multiple towers of vertically stacked DRAM dies
- **A silicon interposer** — a thin silicon layer that connects the GPU dies to the HBM stacks with thousands of tiny wires
- **A substrate** — the base that everything sits on
- **Microbumps and through-silicon vias** — the physical connections holding it all together

This is why the word "package" matters. It is more like a small city than a single building.

## What HBM actually is

HBM stands for High Bandwidth Memory. The name tells you exactly what it optimizes for — not capacity, not cost, but the rate at which data can flow to and from the GPU.

Each HBM stack is a tower of 8-12 individual DRAM dies, physically stacked on top of each other and connected vertically through **TSVs (Through-Silicon Vias)** — tiny holes drilled straight through the silicon, filled with metal, creating electrical connections between layers. At the bottom sits a base logic die that manages the interface.

Think of it like a multi-story parking garage versus a single-level lot. The single-level lot (conventional DRAM on a motherboard) has one floor — one layer of memory cells, one set of connections. The parking garage (HBM) stacks 8-12 floors and connects them with elevators (TSVs) running straight through every level. Same footprint, dramatically more capacity and throughput.

The bandwidth numbers are staggering. Regular DDR5 memory sitting on a PCB motherboard, connected via traces, delivers roughly 50-60 GB/s per channel. HBM sitting millimeters away from the GPU die on a silicon interposer, connected via thousands of TSVs, delivers **8,000 GB/s** on GB200. That is not an incremental improvement — it is a different order of magnitude.

## Why AI workloads demand this

AI workloads are **memory-bandwidth bound**. A GPU has thousands of cores, all screaming for data simultaneously. Training a large language model means multiplying enormous matrices — billions of parameters times millions of data points — and every multiplication needs operands fetched from memory and results written back.

If the memory cannot feed the cores fast enough, the cores sit idle. All that expensive compute silicon does nothing while waiting for data. This is the same speed-mismatch problem from the CPU-RAM-disk hierarchy, just at a different scale.

An analogy from the trading world I know: it is like the difference between sourcing a component from a warehouse across town versus having it staged right at the assembly line. The throughput bottleneck is not the factory's processing speed — it is how fast you can feed it material. HBM is the staging area right next to the production line.

## The cost problem: memory eats the budget

Here is the number that surprised me. HBM accounts for over **50% of the total manufacturing cost** of an H100 package, and roughly **60% or more** for Blackwell.

To put that concretely: if the total cost to manufacture one H100 SXM module is roughly $3,000-3,500 (estimates that have circulated), then $1,500-1,750 or more is just the HBM chips. The actual GPU die, the substrate, the interposer, the assembly — all of that is the other half.

It gets worse for Blackwell. The GB200 uses HBM3e with higher capacity (up to 192GB per GPU), meaning more HBM stacks per package. HBM3e is also newer and more expensive per stack. The memory cost grows faster than the logic cost, shifting the ratio further toward memory.

This creates what I think of as an unstable equilibrium. The most expensive component in an AI accelerator is not the part that Nvidia designs — it is the part that SK Hynix and Micron manufacture.

## The value capture paradox: why Nvidia wins anyway

This led to my second question, and it is a classic strategy question — very BCG-flavored. If HBM is 50-60% of the cost and Nvidia does not make the HBM, why is Nvidia's stock price surging and not SK Hynix's?

The answer is **value capture versus cost structure** — two very different things.

Nvidia buys HBM from SK Hynix at some price X per stack. They package it with their GPU die and sell the complete module at 4-5 times total bill-of-materials cost. Nvidia's gross margins are roughly 73-75%. They capture the system integration and software platform premium, not the component margin.

The moat is **CUDA**. Every ML framework, every training script, every inference pipeline is written against CUDA. The switching costs are enormous. So Nvidia sets pricing, and component suppliers — even critical ones like SK Hynix — are price-takers in the relationship.

SK Hynix has done well — their stock roughly tripled from 2023 lows. But memory is historically a commodity boom-bust cycle industry, so the market prices in cycle risk. Samsung and Micron were also behind on HBM yields, which concentrated the upside specifically at SK Hynix.

The pattern is familiar: platform owners capture disproportionate value relative to component suppliers, even when the component is the majority of BOM cost. Apple versus its display and chip suppliers is the same dynamic. Nvidia is the Apple of AI infrastructure.

| | Nvidia (platform) | SK Hynix (component) |
|---|---|---|
| **What they provide** | GPU design + CUDA ecosystem | HBM memory stacks |
| **% of BOM cost** | ~40-50% | ~50-60% |
| **Gross margin** | ~73-75% | ~35-50% |
| **Pricing power** | Sets the price | Takes the price |
| **Moat** | Software ecosystem (CUDA) | Manufacturing yield lead |
| **Market perception** | Platform growth | Commodity cycle |

## What "AI accelerator" actually means

I realized I had been using the term loosely, so I pinned down the definition. An AI accelerator is any chip designed specifically to do the math that neural networks require — massive amounts of matrix multiplications and tensor operations, run in parallel.

A regular CPU is a generalist. It is great at running a browser, an operating system, sequential logic — but it processes things mostly one at a time. Training a model like GPT-4 requires trillions of multiply-accumulate operations. A CPU would take years.

A GPU was originally built to render pixels on a screen — which happens to also be massively parallel math (calculate color values for millions of pixels simultaneously). Researchers discovered around 2012 that this same parallel architecture was perfect for neural network training. That is when Nvidia accidentally became an AI company.

Today, "AI accelerator" is the umbrella term covering:

- **Nvidia GPUs** (H100, B200) — the dominant incumbents
- **Google TPUs** — custom silicon for Google's own workloads
- **AMD MI300X** — the main competitive alternative to Nvidia
- **AWS Trainium** — Amazon's custom inference chips
- **Microsoft Maia** — Azure's custom accelerator
- **Tesla Dojo** — built for autonomous driving training

They all do the same fundamental thing — massively parallel matrix math — but with different architectures and tradeoffs.

## The packaging revolution

What struck me most about this whole topic is that the innovation frontier in AI hardware is not just about making smaller transistors or faster logic. It is about **packaging** — how you physically assemble multiple dies, memory stacks, and interconnects into a single unit.

The terms to know are **2.5D stacking** (placing dies side by side on a silicon interposer, which is what HBM uses) and **3D stacking** (placing dies directly on top of each other, which is how the DRAM layers within each HBM stack are arranged). These packaging techniques are what make it possible to put terabytes-per-second of memory bandwidth millimeters away from the compute cores.

This is relevant to my world in electronics distribution. The semiconductor supply chain is not just about chips anymore — it is about advanced packaging capacity. TSMC's CoWoS (Chip-on-Wafer-on-Substrate) packaging is a bottleneck for AI accelerator production. Understanding this chain — who makes the interposers, who does the die stacking, where the capacity constraints are — is the kind of structural knowledge that could create trading edge.

> A modern AI accelerator is not a chip. It is a small city: GPU dies are the factories, HBM stacks are the warehouses staged right at the factory doors, the interposer is the road network connecting them, and the substrate is the land it all sits on. The most expensive part of the city is not the factories — it is the warehouses.

---

*This connects directly to [why circuits need discrete components alongside chips](why-circuits-need-discrete-components-alongside-chips.md) — the board-level components surrounding these packages are part of the same story. See also [computer architecture fundamentals](computer-architecture-why-cpu-ram-and-storage-exist.md) for the memory hierarchy that motivates HBM's existence.*
