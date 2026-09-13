# Inside a 74181 ALU — from schematic to silicon

*Was studying the 74181 4-bit ALU as part of getting concrete about how arithmetic actually happens in hardware. The chip's block diagram shows a clean logical structure — gates, inputs, outputs, control lines. The chip itself is a 24-pin DIP, the black rectangular package with two rows of pins. The question that bothered me: what does it actually look like *inside* the package? Does the silicon look anything like the block diagram, or something completely different? The answer turns out to be one of the cleanest demonstrations in computer science of how an abstract circuit becomes a physical 2D city.*

---

## Why the 74181 is the right chip to study

The 74181 was introduced by Texas Instruments in 1970 and was, at the time, one of the most complex integrated circuits in production. It is a 4-bit Arithmetic Logic Unit on a single chip — capable of 16 logic operations and 16 arithmetic operations (selectable via 4 mode-select pins) on two 4-bit operands.

Two reasons it has become one of the most-studied chips in CS pedagogy:

1. **Small enough to fully reverse-engineer.** Roughly 170 transistors on a 2–3 mm silicon die. You can map every transistor to its role in the schematic and see the entire chip as a single coherent design.
2. **Historically central.** It was used in the DEC PDP-11, the Xerox Alto, the Data General Nova, and many minicomputers. For a decade it was the canonical "ALU on a chip."

The 24-pin DIP package is the standard mid-1970s integrated circuit form factor — two rows of 12 pins each, 0.3-inch row spacing, easily socketed on a breadboard.

## Layer 1 — the package in your hand

Crack open the 24-pin DIP and you find:

- **Molded epoxy plastic** (or ceramic on premium variants) — the black rectangular shell. Pure protective housing. No computing happens here. This is roughly 95% of what you are physically holding.
- **Stamped metal lead frame** — a flat metal skeleton where the 24 pins extend inward and terminate at small landing pads near the centre. The pins themselves are tin-plated steel or copper alloy.
- **A tiny silicon die** mounted at the centre of the lead frame, glued down with conductive epoxy. For the 74181, this die is roughly **2–3 mm across** — about the size of a grain of rice. *That is the entire chip.* Everything that does computation is in this rectangle.
- **Bond wires** — extremely thin gold or aluminum wires, typically about **25 microns thick** (about 1/3 the thickness of a human hair), each connecting one bond pad on the silicon die to its corresponding pin on the lead frame.

So when you hold a 74181, the proportion of mass that is actually doing work is tiny. The vast majority is plastic and metal whose only job is to make the silicon mechanically and electrically accessible.

## Layer 2 — the silicon die

This is where the real question lives. And the answer is: **no, the die does not look like the Wikipedia block diagram.** It looks like something stranger.

The block diagram shows the *logical* structure — gates, inputs, outputs, what feeds into what. The die shows the *physical* structure — a microscopic 2D city etched onto silicon.

Under a microscope (or in a die-shot photograph), you see:

- **Doped silicon regions.** Patches of silicon implanted with phosphorus (n-type) or boron (p-type) to form transistors, resistors, and diodes. Different doping levels produce different colours under microscope illumination because the doping affects how light reflects. The 74181 uses **bipolar junction transistors** (TTL technology — predates the MOSFETs that dominate modern chips by about a decade).
- **Metal traces.** Thin aluminum lines deposited on top of the silicon, forming the wires between gates. These are the schematic's "wires" rendered in physical metal, snaking across the chip surface.
- **Oxide layers.** Silicon dioxide (SiO₂) insulation, separating metal from silicon and metal from metal. A modern chip has multiple metal layers stacked vertically with oxide between them; the 74181 mostly has one metal layer.
- **Bond pads.** Larger metal squares around the die's edge, where the bond wires attach. These are the only points on the die that connect to the outside world.

The 74181 contains roughly **170 transistors and 170 resistors** etched into that tiny rectangle, organised into the ~75 logic gates the spec lists. The transistor density on the 74181 is laughable by modern standards (an Apple M3 has around 25 billion transistors on a die roughly the same physical size), but the structure is identical in principle. Just more of it, smaller, on more layers.

If you want to see this with your own eyes, search for **"74181 die shot Ken Shirriff."** Shirriff is a hardware reverse-engineer who has published high-resolution photomicrographs of the 74181 with annotated overlays showing which silicon region implements which gate from the schematic. It is one of the cleanest demonstrations in computer science of "abstract logic becoming physical silicon."

## Layer 3 — schematic vs layout

The block diagram on Wikipedia is the **schematic** — a *logical* drawing. It tells you what computes what, with no commitment to physical arrangement.

The die is the **layout** — a *physical* 2D plan. Every gate in the schematic corresponds to a small cluster of doped silicon and metal traces somewhere on the die. Every wire in the schematic corresponds to an actual aluminum line snaking across the chip surface.

These are **two representations of the same circuit:**

| Representation | What it captures | Optimised for |
|---|---|---|
| Schematic | Logical structure (what computes what) | Human understanding |
| Layout | Physical arrangement (where things sit, how wires route) | Silicon area, manufacturability |

A chip designer maps one to the other. For the 74181 in 1970, this was done **by hand**, on giant sheets of red rubylith film, cut and inspected with magnifying glasses. A team of engineers would produce a layout that fit the schematic in a manufacturable shape. Today, the same conceptual move is automated by EDA software (Cadence, Synopsys, Mentor) doing place-and-route — taking a netlist of gates and connections and generating a physical layout that minimises area and meets timing constraints. The conceptual move is the same: project a logical drawing onto silicon real-estate.

The non-trivial constraints in this projection:

- **Wires take area.** Every connection in the schematic has to physically route from source to destination on a 2D plane. Crossings require multiple metal layers (or workarounds in single-layer designs).
- **Wires take time.** Signal propagation along a metal trace is finite. Long wires limit clock speed.
- **Wires take power.** Every wire has parasitic capacitance that must be charged and discharged on every transition. More wire = more dynamic power.
- **Yield depends on layout.** A defect anywhere on the die ruins the whole chip. Smaller layouts mean more chips per wafer and higher yield.

A bad layout can run 2x slower and cost 5x more to manufacture than a good layout of the same schematic. This is why chip layout is a discipline of its own.

## The connection back to first principles

The 74181 is a literal concrete example of the lock between abstract structure and physical mechanism that defines computation:

- The **schematic** = the abstract program-layer (what is being computed)
- The **silicon die** = the physical substrate (what is actually doing the work)
- The **lock between them** = the design discipline that makes the silicon's electrical behaviour faithfully mirror the schematic's logical behaviour

When current flows through the chip, the voltages move in patterns that are *isomorphic* to the abstract operations of an ALU. The silicon does not know it is adding numbers. But because the layout was *built* to mirror the schematic, **adding numbers is what is happening, structurally**, every time the chip is energised.

If someone asks "where does the addition actually happen?" — it is not in the schematic (just a drawing). It is not in the silicon alone (just doped regions). It is in the **lock** — the disciplined correspondence between them. The schematic tells silicon what *meaning* its physical motion carries; silicon tells the schematic what *substrate* makes it real.

This is one of the few cases in CS where you can hold the abstraction in one hand and the physical implementation in the other, look at both at the same time, and see the correspondence operating directly. Most computation is invisible — buried inside chips with billions of transistors that no human can fully map. The 74181 is small enough that the entire abstraction-to-physics mapping fits on a single page, which is why it has become the canonical pedagogical chip.

## Compressed picture of what is actually inside

> A 24-pin DIP is mostly black plastic. Inside, a silicon die roughly 3 mm across does all the work. Bond wires connect bond pads on the die to the package pins. On the die, doped silicon regions form ~170 transistors organised into ~75 logic gates, connected by aluminum traces routed across the surface. The schematic is a logical drawing; the die is a physical 2D plan implementing it. Both describe the same circuit. The chip *is* the lock between them.

The next time I hold any IC, I have a much sharper picture of what is inside. Most of the package is housing. The actual computation lives in a piece of silicon smaller than a grain of rice, with all the abstract structure of the schematic etched into it as a physical 2D arrangement of doped regions and metal wires. **The schematic and the silicon are not metaphor and reality. They are two faithful descriptions of the same physical circuit, each one optimised for a different purpose.**

---

*The 74181 is the cleanest concrete example of the abstraction-to-substrate lock described in [what computation actually is](what-computation-actually-is.md). For more depth on the broader computer-architecture context, see [why CPU, RAM, and storage exist](computer-architecture-why-cpu-ram-and-storage-exist.md) and [HBM and AI accelerators — what's inside a GPU package](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md), which extends the same kind of physical-package analysis to modern AI chips.*
