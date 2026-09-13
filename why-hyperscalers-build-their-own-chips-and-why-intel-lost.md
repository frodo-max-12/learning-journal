# Why hyperscalers build their own chips — and why Intel lost

---

## The thread that started everything

Kurian mentioned, almost in passing, that Google had built its own ARM chips because agent workloads need general-purpose compute alongside the AI accelerators. My first instinct was: wait, ARM chips? Like the ones used in Bosch sensors and microcontrollers?

That was a category error. The word "ARM chip" spans an enormous range — from a $0.50 microcontroller to a $10,000 datacentre CPU. They share an instruction set architecture, but they are wildly different products.

| Tier | Example | Use case | Price |
|---|---|---|---|
| Microcontroller (MCU) | STM32, PIC32, nRF52 | Embedded — washing machines, IoT, sensors | $0.50 – $10 |
| Mobile / edge SoC | Apple A18, Snapdragon, MediaTek | Phones, tablets, edge AI | $20 – $200 |
| Datacentre server CPU | AWS Graviton, Ampere Altra, NVIDIA Grace, Google Axion | Cloud servers, hyperscaler workloads | $1,000 – $10,000+ |

Kurian was talking about the third tier. Google's chip is called **Axion**, announced in April 2024, designed for general-purpose compute alongside their TPU accelerators. Not an MCU. Not a phone chip. A full datacentre-class CPU.

That was the moment I realised this is a much bigger story than I had appreciated.

## The hyperscaler chip explosion

It is not just Google. Almost every major hyperscaler now designs its own silicon. Many of them have been doing it longer than Google has. The list is far bigger than I knew:

| Company | Custom CPU | Custom AI chip | First shipped |
|---|---|---|---|
| AWS | Graviton 1/2/3/4 | Trainium, Inferentia | Graviton 1: 2018 |
| Google | Axion | TPU (8 generations) | TPU: 2015, Axion: 2024 |
| Microsoft | Cobalt | Maia | Both 2024 |
| Meta | (in development) | MTIA v1 / v2 | MTIA: 2023 |
| Apple | M-series | Neural Engine | M1: 2020 |
| Tesla | — | FSD chip, Dojo, HW4 | FSD: 2019 |
| Alibaba | Yitian | Hanguang | Yitian: 2021 |
| Huawei | Kunpeng | Ascend | 2019 |

Apple has been at this longest — they have been designing their own chips since the original iPad in 2010. AWS came next, with Graviton in 2018, and proved that an internet company could design competitive datacentre CPUs. Once that proof of concept landed, the floodgates opened. By 2024, Microsoft was the *last* of the big US hyperscalers to ship its own chips.

Even Tesla is on this list. Their FSD chip sits in every Tesla, doing the neural network inference for self-driving in real time, while Dojo trains the underlying models. They are vertically integrated all the way down to silicon.

The companies that are *not* on this list are the ones that did not need to be. Netflix runs on AWS, so they buy compute through Amazon's stack. Twitter, Uber, DoorDash, Stripe — too small to justify a chip program. NVIDIA, AMD, Qualcomm — they are chip companies already.

The pattern is clean: **once a company hits roughly $10 billion per year in compute spend, custom silicon ROI flips positive**. Below that, you buy from Intel, AMD, and NVIDIA. Above it, you design your own.

## The puzzle — how do "software companies" beat Intel at chips?

This was the question I kept coming back to. Intel's full-time job was to design chips. AWS, Google, Apple, Microsoft are software companies in their cores. How is it that the software companies are now shipping better chips than the chip company?

The answer surprised me, because the obvious explanation — "they hired better engineers" — is *not* the real reason. There are three structural advantages that hyperscalers have which Intel could never replicate, and the engineering quality is downstream of those structural advantages.

## Structural advantage 1 — they do not manufacture, TSMC does

This was the biggest piece I had wrong in my mental model. The mental model "Intel makes chips, AWS writes software" is outdated by at least a decade. Modern chip-making has split into two completely separate industries.

**Design** — the architecture, the logic, the intellectual property. Done by ARM, NVIDIA, AWS, Apple, Google, AMD. This is design IP work.

**Fabrication** — actually etching transistors onto silicon. Done almost entirely by **TSMC** in Taiwan, with Samsung as a distant second.

Intel was vertically integrated — design plus fab. That was Intel's *advantage* for decades when fabrication was the leading edge. **It became a fatal weakness when Intel's fab fell behind TSMC's around 2018-2020.** TSMC reached 5nm and 3nm process nodes while Intel was stuck at 10nm and 7nm. The gap was a generation or more.

So when AWS wanted Graviton, they did not build a fab. They:

1. Licensed ARM's instruction set architecture from ARM Holdings.
2. Hired chip designers — many ex-Intel, ex-AMD, ex-Apple.
3. Sent the design to TSMC for fabrication.
4. Got back a chip on the **same leading-edge process node Intel could not access**.

This is the part most non-technical people miss. AWS, Apple, Google, NVIDIA all design chips — and they all manufacture at TSMC. Intel had been competing against companies that were free to use whichever foundry was best, while Intel itself was locked into its own foundry, which was no longer best.

## Structural advantage 2 — they have one customer: themselves

Intel had to design CPUs that worked for everyone. Gamers, enterprises, laptops, servers, AI, embedded systems. Every workload, every operating system, every customer. That meant compromises everywhere — every transistor had to earn its place across an enormous range of use cases.

AWS designs Graviton to run **exactly one workload mix**: AWS's own customer base running Linux on EC2. They can:

- Skip features that no one in their workload uses (eliminate transistors, save cost, reduce heat).
- Optimise for the specific software AWS runs.
- Iterate every two years based on telemetry from millions of EC2 instances.

This is the same reason Apple's M-series chips beat Intel in laptops. Apple optimised for *macOS specifically*, not "every operating system in the world." Constraint creates focus. Focus creates better chips for that one focus.

## Structural advantage 3 — they capture the entire margin stack

This is the piece that should make every Intel investor nervous.

When AWS bought Intel Xeons, AWS paid Intel something like $10,000 per chip. Intel kept the margin.

When AWS uses Graviton, AWS pays TSMC something like $2,000 to manufacture. **AWS keeps the $8,000 of margin** that used to flow to Intel.

Multiplied across millions of servers, this is **tens of billions of dollars per year** that Intel used to extract from hyperscalers and now does not. That margin did not disappear — it was captured by the hyperscalers themselves. Intel's customers became Intel's competitors, and they are not just buying less Intel silicon, they are also keeping the margin that used to flow to Intel.

## Why "software company" is the wrong frame

This is the deepest point I came away with.

AWS, Google, Apple, Microsoft are not "software companies that started making chips." They are **vertically integrated computing companies**. The old taxonomy — hardware company versus software company — broke down a decade ago.

What they have that Intel does not:

- A captive customer base (their own cloud services or device ecosystem).
- Cash flow to fund $1 billion-plus chip programs without venture capital.
- Software stacks they control end-to-end, so hardware and software can be co-designed.
- Access to TSMC's leading-edge process nodes.

What Intel had that they do not have:

- A fab. Which became a liability rather than an asset.

Intel today trades at roughly $30 per share, with a market cap below AMD and far below NVIDIA. They are spinning out their foundry. They received a $7.86 billion CHIPS Act grant essentially because the US government cannot tolerate TSMC being the only leading-edge fab on Earth. Intel did not lose because hyperscalers were better at chip design. **Intel lost because their fab fell behind, their customers became their competitors, and their margins got captured.**

## What this looks like as an industry-level shift

Over a 40-year arc, the semiconductor industry has gone through a structural reversal.

**1980s–2000s.** Vertical integration was king. IBM made everything in-house. DEC made everything. Intel made chips and sold to everyone. ARM split design from manufacturing in the 1990s, TSMC was founded as a pure-play foundry in 1987, but systems companies still bought merchant silicon from Intel.

**2010–2020.** TSMC's process leadership became insurmountable. Apple proved on the M1 that you could design world-class chips on TSMC and beat Intel. The playbook became repeatable.

**2020–2026.** Every company with sufficient scale, cash, and a software stack started designing silicon. Intel's customers became Intel's competitors.

**2026–2030 (where we are now).** AI workloads are so different from traditional CPU workloads that the application increasingly dictates the silicon. General-purpose chips lose; workload-specific chips win. This is why TPUs beat GPUs for some workloads, why Meta's MTIA beats GPUs for recommendation systems, why Tesla's FSD chip beats GPUs for autonomous driving inference.

## The thing most people miss

The value in AI is not in the chips. It is in the **vertical stack** — chip plus software plus data plus customer.

Hyperscalers build chips not because chips are profitable on their own (they are not — TSMC, ASML, and ARM capture most of that margin), but because owning the chip lets them **capture the entire stack of value above it**.

This is why NVIDIA is worth $3 trillion while Intel is worth $130 billion. NVIDIA owns the CUDA software stack on top of its chips. The chip is the wedge; the software stack is the moat. Every hyperscaler has internalised this lesson and is building their own version of that wedge.

> Intel did not lose because the hyperscalers were better engineers. Intel lost because vertical integration plus access to the leading-edge fab plus captive demand beats merchant silicon every time. The companies that "just write software" now design better chips than the company whose only job was to make chips — because chips are not really the product. The whole stack is.

---

*This connects to [hyperscalers explained — the pyramid of cloud computing](hyperscalers-explained-the-pyramid-of-cloud-computing.md) which sets up who these companies are and why they sit where they sit. It also connects to [HBM and AI accelerators](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md), which explores another dimension of the same value-capture story — why NVIDIA wins even though SK Hynix supplies most of the bill of materials.*
