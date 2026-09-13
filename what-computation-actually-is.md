# What computation actually is

*I had been using the word "computation" for years without ever pinning it down. I knew about substrate-independence — the same Game of Life can run in cells, in dominoes, or in saltwater — but knowing computation isn't *in* the silicon doesn't tell you where it *is*. Sat with the question until something clicked.*

---

## The first attempt — and why it wasn't enough

The pattern definition is the standard one: computation is a pattern of state transitions that a sufficiently rich physical system can instantiate. That covers substrate-independence cleanly. Conway's Game of Life run on cells, on dominoes, or in your head is the same computation, because the abstract dance of states is identical even though the physics underneath is not.

This frame is technically correct, but it leaves the deepest question unanswered: where does meaning come from? A rock rolling down a hill is also a sequence of state transitions, but nobody says the rock is computing. So substrate-independence is necessary but not sufficient. Something more is needed.

## The reframe — computation as a disciplined correspondence

The frame that finally landed: **computation is a lock between two layers that have nothing intrinsically to do with each other.**

Layer A — **the physical layer.** A real process in time. Voltages flipping, beads sliding, dominoes falling, neurons firing. This layer just obeys physics. Nothing in it knows what it means. Dominoes do not know about arithmetic.

Layer B — **the abstract layer.** A relationship that is true regardless of any physical thing. "2 + 3 = 5." "If P then Q." A function from inputs to outputs. This layer does not happen anywhere. It just is.

These two layers are normally strangers. Dominoes don't care about math; math doesn't care about dominoes. **Computation is what you have when you arrange the physical layer so carefully that, as it runs forward under its own physics, the abstract layer keeps perfect step with it.** Each physical state corresponds to an abstract state. Each physical transition corresponds to an abstract transition.

That correspondence — the lock — is the thing. That is computation.

A 4-bit adder makes this concrete. The transistors do not "know" they are adding. They are doped silicon switching on and off according to electric fields. But the layout of the transistors has been engineered so that each electrical configuration corresponds, by construction, to a specific arithmetic state, and each electrical transition corresponds to a specific arithmetic step. Doing the physics correctly produces the math correctly, automatically. **Meaning falls out of meaningless mechanism because the mechanism was shaped to mirror the meaning.**

A CPU is millions of such correspondences stacked: electrons → voltages → bits → numbers → variables → objects → "the spreadsheet recalculated." A brain is the same shape with a different substrate: ion channels → action potentials → patterns → percepts → thoughts → decisions.

## What this frame buys you

Two consequences fall out cleanly.

**Computation requires an interpretation, not just a process.** A rock rolling down a hill is doing pure physics. Nobody has built a correspondence between rolling-states and meaning-states, so it is not computing anything. Strap an interpretation onto it — say each metre rolled = one bit — and the rock is suddenly computing. The physics did not change. The lock did. This is also why "is the universe itself a computation?" is genuinely contested. It depends on whether you think the abstract layer is intrinsically there or only there when minds project it.

**The depth of what you can compute is the depth of correspondence you can build.** A thermostat's correspondence is shallow: temperature ↔ on/off. A CPU's is deep enough to lock onto any abstract rule-system. That is what universality really means. Not "powerful hardware" but "a correspondence flexible enough to be reshaped to fit any abstract structure you give it."

## The behavioural definition

Once the lock-frame is in place, the simpler behavioural definition makes sense: **computation is following rules to find out what you didn't already know.**

Both halves matter. *Following rules* — no creativity, no new information added beyond the inputs and the rule. *Finding out what you didn't already know* — even though the answer is fully determined by the rules and the input, you don't have access to it until something does the steps.

Take a trivial example. Start with 1 and double 30 times. The answer is fixed the moment you state the rule and the start state. No choice, no creativity. But you do not know it is 1,073,741,824 until something — a brain, a calculator, a row of dominoes — performs the doublings. The answer was always implied. **Computation is the labour that turns implied into visible.**

## Universality is cheap

The most surprising thing about computation, once the lock-frame is in place, is how *easy* it is to be universal. Turing showed in 1936 that some very simple systems — a tape, a head, a handful of state-transition rules — can simulate any other computation. Stephen Wolfram and Matthew Cook later showed that **Rule 110**, a one-dimensional cellular automaton with a 3-bit lookup table, is also universal.

Rule 110's complete specification:

| current pattern | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|---|---|---|---|---|---|---|---|---|
| next state | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |

That table is the entire program. Eight rules. Three bits of context per step. And it is Turing-complete — capable in principle of running any algorithm any modern CPU can run.

The lesson: once a rule-following system crosses a low complexity threshold, it can in principle do anything any computer can do. Universality is not a hard-won engineering achievement. It is closer to a generic property of sufficiently rich rule-systems. Avoiding universality is in some ways harder than achieving it.

## Computation discovered its own limits from the inside

The same theory that tells you universality is cheap also tells you certain things are forever out of reach. **The halting problem** — whether an arbitrary program will eventually halt or run forever — is provably undecidable. Not "we have not found an algorithm yet." None can exist. Turing proved it in the same 1936 paper that defined universality.

This is one of the strangest features of computation: it is powerful enough to formalise itself and then prove deep theorems about what no computation can do. A rule-system that knows its own limits.

## Computation is proof, literally

The deepest connection in the theory: **the Curry-Howard correspondence.** Programs are proofs. Types are propositions. Running a program and normalising a proof are literally the same operation.

This sounds like a metaphor on first reading. It is not. In dependently-typed languages like Coq, Agda, and Lean, you write programs whose type signatures are mathematical theorems, and the program itself is the proof of that theorem. The compiler verifies the proof by type-checking. There is no separate proof step.

Logic and computation are not analogies for each other. They are two views of one thing. *Implication* in logic and *evaluation* in computation are the same operation seen from different sides.

## The compressed definition

Pulling all of this together, the working definition becomes:

> **Computation is the disciplined conversion of logical determination into epistemic availability.** Implication is free — the answer is fixed the moment the rules and inputs are. Knowing is not free — extracting the answer requires physical work that mirrors the abstract structure. Computation is the price the universe charges to turn "is implied" into "is known."

The dominoes are not redundant when they fall to compute an addition. The arrangement determines the answer; the falling delivers it. Both are needed. The arrangement encodes the implication. The fall pays the bill.

---

*This pairs with [the dominoes-adder paradox — determined vs known](the-dominoes-adder-paradox-determined-vs-known.md), which presses on the gap between determined and available until it produces computational irreducibility. It also connects to [theory of computation — Turing, Church, and the halting problem](theory-of-computation-turing-church-and-the-halting-problem.md), which goes deeper on universality and decidability.*
