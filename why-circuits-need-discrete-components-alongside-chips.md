# Why circuits need discrete components alongside chips

*Learned on March 26, 2026. This question came from the overlap between my CS learning and my family's electronics trading business. If chips contain billions of transistors, resistors, and capacitors inside them, why does every circuit board still have hundreds of separate resistors, capacitors, and diodes soldered around the chips?*

---

## What is actually inside a chip

Before understanding why discrete components still exist, I needed to understand what is already inside a chip. The answer surprised me with its scale.

Every single chip — Apple's M-series, Nvidia's GPUs, even the simple microcontroller in a microwave — is built entirely from tiny transistors, resistors, and capacitors fabricated directly into the silicon. An Apple M-series chip has something like 20+ billion transistors. An Nvidia Blackwell GPU has over 200 billion.

But these are not separate little parts soldered in. They are formed by the silicon itself during manufacturing. A thin strip of certain material acts as a resistor. Two conductive layers separated by an insulator act as a capacitor. They are all built during the same photolithography process that creates the transistors — patterns of light etching structures into silicon wafer after wafer.

The chip is a dense city. Millions of tiny, efficient structures packed together at nanometer scale, all working in concert. The transistors form logic gates, the logic gates form arithmetic units, the arithmetic units form processing cores. The on-chip resistors and capacitors support the analog circuitry that keeps everything synchronized and referenced to the right voltages.

## The sharp follow-up: is it really all just transistors?

I pushed back on this. Modern digital logic — the core "thinking" part of a chip — is almost entirely just transistors. CMOS logic gates use complementary pairs of transistors (NMOS and PMOS), and they do not need resistors at all for their basic switching function. So the digital core really is just transistors switching on and off, billions of times per second.

But chips are not purely digital logic. Here is where the other components come in:

**Memory inside the chip.** SRAM cache — the fast memory on every CPU and GPU — uses transistor-based flip-flops to store bits. DRAM, which sometimes appears on-chip in specialized designs, is literally just a transistor plus a capacitor per bit. The capacitor holds the charge that represents a 1 or 0.

**Analog circuits on-chip.** Every chip needs some analog circuitry: clock generators (PLLs — phase-locked loops) that keep everything in sync, voltage references that provide stable reference points, analog-to-digital converters for sensor inputs. These analog blocks absolutely require resistors and capacitors to function. They are doing things like filtering signals and setting precise timing that pure transistor logic cannot handle.

**Parasitic effects.** Even when you do not want them, every tiny wire on a chip acts as a small resistor (because it has nonzero electrical resistance), and every junction between layers acts as a small capacitor (because any two conductors separated by an insulator form a capacitor). Engineers have to carefully account for these "accidental" components in their designs. At nanometer scales, the parasitics can dominate the behavior of the circuit.

**I/O and power delivery on-die.** The parts of the chip that talk to the outside world need impedance matching, ESD (electrostatic discharge) protection, and on-chip voltage regulation — all of which use resistors and capacitors built into the silicon.

So the logic is almost all transistors. The resistors and capacitors inside are mainly there for memory, analog support circuitry, and interfacing.

## Why on-chip components have limits

This is the core of why discrete components still exist on every circuit board. On-chip resistors and capacitors have fundamental limitations that come from being fabricated in silicon at nanometer scale:

**Size constraints.** A large capacitor — say, 100 microfarads for power filtering — would be physically enormous if built in silicon. The capacitance you can achieve on-chip is measured in picofarads or at most nanofarads. That is a million-fold gap. It is far cheaper and physically smaller to just solder a ceramic capacitor next to the chip. The same applies to high-value resistors — the resistance per unit area on a chip is limited by the materials available in the fabrication process.

**Tolerance and precision.** On-chip resistors and capacitors have relatively poor tolerance — their actual values can vary by 10-20% from the design target due to manufacturing variations in the fabrication process. Discrete components can be manufactured to 1% or even 0.1% tolerance. When a circuit requires precise values (for setting a reference voltage, tuning a filter frequency, or establishing a timing constant), discrete components are far more reliable.

**Power handling.** This is perhaps the most fundamental limitation. Chips operate at low voltages (often under 1 volt for the core logic) and their internal components handle tiny currents — microamps or milliamps. But the chip as a whole might draw 50, 100, or even 300+ amps from the power supply (a high-end GPU can consume 700 watts). The components that manage this power — smoothing it, regulating it, filtering it — need to handle currents and voltages that would instantly destroy any on-chip structure.

**Parasitic effects at scale.** On-chip capacitors suffer from parasitic capacitance to the substrate and neighboring structures. On-chip resistors are temperature-sensitive in ways that discrete components, designed specifically for stability, are not.

## The specific jobs discrete components do

With the limitations understood, the roles of board-level discrete components become clear. They fall into several categories:

### Power delivery and smoothing

This is the biggest category. A modern chip needs extremely clean, stable power. Even tiny voltage fluctuations — measured in millivolts — can cause logic errors or timing failures. But the power supply feeding the board is noisy, and the chip's own switching activity creates noise (when billions of transistors switch simultaneously, they cause momentary current spikes that ripple through the power supply).

**Decoupling capacitors** are the workhorses here. These are the small ceramic capacitors you see clustered around every major chip on a circuit board — sometimes dozens or hundreds of them. Their job is simple but critical: they act as tiny local reservoirs of charge. When the chip suddenly demands a spike of current (because a large block of logic just switched state), the decoupling capacitor supplies it instantly from its stored charge, rather than waiting for the current to travel all the way from the power supply. Think of them as local water tanks — the main water supply is far away and slow to respond, but the tank right next to the faucet handles the instant demand.

**Voltage regulators** (VRMs — Voltage Regulator Modules) convert the main board voltage (typically 12V) down to the specific voltages each chip needs (1.0V for core logic, 1.8V for I/O, 3.3V for certain interfaces). These are complex circuits in their own right, built from discrete MOSFETs, inductors, and capacitors.

### Signal integrity

When signals travel along traces on a circuit board, they behave like waves. They can reflect off impedance mismatches (like echoes in a tunnel), pick up interference from neighboring traces (crosstalk), and degrade over distance. Discrete components manage this:

**Termination resistors** match the impedance at the end of a signal trace to prevent reflections. Without them, a high-speed signal bouncing back and forth along a trace creates ghost signals that corrupt data.

**Ferrite beads** act as frequency-selective resistors — they pass DC and low-frequency signals but absorb high-frequency noise. They are commonly placed on power lines to filter out switching noise.

### Protection

**ESD protection diodes** sit at every input and output pin, ready to shunt a static discharge spike safely to ground before it can reach the delicate transistors inside the chip. A static shock from your finger can be thousands of volts — the transistors inside a chip operate at under 1 volt and are a few nanometers across. Without ESD protection, a single touch could destroy the chip.

**TVS (Transient Voltage Suppressor) diodes** protect against larger voltage spikes from the power supply or external events (lightning, inductive kickback from motors).

### Impedance matching and interfacing

When a chip needs to communicate with the outside world — driving an antenna, connecting to a sensor, interfacing with a different voltage domain — discrete components bridge the gap. **Pull-up and pull-down resistors** define default logic levels on communication buses. **Level shifters** (built from discrete transistors or small ICs) translate between different voltage standards.

## The city analogy

The way I think about it now is this: the chip is like a dense downtown — millions of tiny, efficient offices packed together, all working on information. But you still need external infrastructure: power stations (voltage regulators), water towers (bulk capacitors storing charge), lightning rods (ESD protection), highways connecting to other cities (interface components). Those things are too big, too power-hungry, or too specialized to fit downtown.

An Nvidia Blackwell GPU might have 200+ billion transistors inside, but it still sits on a board surrounded by discrete capacitors, resistors, and voltage regulators. The chip is the brain. The discrete components are the life-support system that keeps the brain alive and connected.

> Chips internalized the logic — the thinking. What they cannot internalize is the infrastructure — the power, the protection, the physical interface with a messy, high-voltage, high-current, static-charged real world. That boundary between nanometer-scale logic and centimeter-scale infrastructure is where discrete components live, and it is not going away.

This matters for my work in components distribution because discrete components — MLCCs (multi-layer ceramic capacitors), chip resistors, Schottky diodes, MOSFETs — are a huge part of every BOM (bill of materials) we see. They are individually cheap (fractions of a cent) but used in enormous quantities. A single server board might have 2,000+ discrete capacitors. Understanding *why* each one is there makes me better at reading BOMs and understanding which components are truly critical versus which have easy substitutes.

---

*This connects to [HBM and AI accelerators](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md) — the board-level discrete components are part of the same physical system that includes the GPU package, HBM stacks, and interposer. See also [computer architecture fundamentals](computer-architecture-why-cpu-ram-and-storage-exist.md) for why the memory hierarchy creates demand for different types of capacitors at every level.*
