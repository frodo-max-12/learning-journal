# The dominoes-adder paradox — determined vs known

*Watched a YouTube video where someone built a 4-bit binary adder out of 10,000 dominoes. The thing actually computes. You set the input dominoes, knock the start, the cascade runs for a few seconds, and the output is the correct binary sum. It bothered me. If the arrangement of dominoes plus the inputs already determines the answer, then in what sense is the falling doing any "work"? The answer was already there before any domino fell. Pulling on this thread led to one of the most important ideas in computer science: computational irreducibility.*

---

## The paradox stated cleanly

The dominoes-adder is a physical machine that performs binary addition. The configuration of standing dominoes encodes the *function* — a generic adder. Once you also set the input dominoes (representing the two numbers to add), the answer is *logically* fixed. No additional information is being introduced when the cascade runs. Every output domino's final state is implied by the configuration plus the inputs.

So the natural question: if the answer is already determined, what is the falling actually *doing*? Why is the cascade not redundant?

The instinct is to say "the falling makes the answer visible" or "the falling delivers the answer." Both are right but vague. Pressing harder produces a sharper answer.

## Determined and available are not the same thing

Write `47 × 83` on paper. The answer is determined the moment ink hits page. But you do not know it. You cannot use it. To convert it from "logically implied by what is written" to "an actual number in your hands," something — your brain, a calculator, a row of dominoes — has to do the work.

That gap, between **logically implied** and **actually available**, is exactly where computation lives. **Computation is the labour of making the implicit explicit.**

The test that makes this visceral: try to skip the dominoes. Look at the configuration plus the input dominoes and just *see* the sum. You cannot. The moment you try, your brain starts simulating the cascade — tracing which dominoes would fall, which carries would propagate, which output bits would end up high. **The work did not vanish. It got relocated.** The labour can move from dominoes to brain to silicon to abacus, but it cannot be eliminated. Something, somewhere, has to traverse the path from premise to conclusion.

## What the arrangement actually encodes

A subtler observation: the arrangement of dominoes does not encode an *answer*. It encodes a *function*. A frozen machine waiting to be unfrozen by inputs.

Set the input dominoes to "5 + 3" and the function evaluates to one specific output. Set them to "11 + 7" and the same arrangement evaluates to a different output. The arrangement is general; the inputs select a specific instance; the cascade computes that instance.

Once the inputs are placed alongside the arrangement, the specific answer becomes logically pinned down. But "pinned down" is not "delivered." The falling is the delivery.

This distinction matters because it explains why programs and data are different things even though they are both information. A program is a function — a frozen specification of how to transform inputs into outputs. Data is the input that, combined with the program, produces a specific computation. Both are needed. Neither alone produces an answer.

## The deep version — computational irreducibility

For a 4-bit adder, you could in principle skip the dominoes and do the addition in your head. The work moves but you can do it. But for many systems, **there is no shortcut at all.** No formula, no clever inspection, no faster simulation. To know what the rules produce, you must run them, step by step, all the way.

Stephen Wolfram named this **computational irreducibility**. It shows up everywhere once you know to look for it.

**Rule 30**, a one-dimensional cellular automaton with the same kind of 8-row lookup table as Rule 110, generates a pattern that has been shown to pass essentially every statistical test for randomness. Wolfram has used Rule 30 as a pseudo-random number generator in *Mathematica* for decades. There is no closed-form expression for "what is the value of cell *n* at step *t*?" The only way to know is to run the rule for *t* steps and look. Even though every cell's value is fully determined by the initial condition and the rule.

**The halting problem.** Asking "does this program halt?" is undecidable in general. There is no algorithm that, given an arbitrary program and input, can decide in advance whether the program will eventually stop or run forever. Sometimes the only way to know whether a program halts is to run it. And if it doesn't halt, you wait forever.

**Three-body gravitational systems.** Newtonian mechanics is fully deterministic. Three masses interacting gravitationally produce a trajectory that is uniquely determined by the initial conditions. There is no closed-form solution. Numerical integration is the only way to compute future positions, and small errors in initial conditions amplify exponentially.

**Protein folding** until very recently. Given an amino acid sequence, the final folded structure is determined by physics. But for decades there was no shortcut. You had to simulate the folding, which was slow and approximate. AlphaFold did not so much *solve* the irreducibility as *learn an approximation* by training on known structures — and even AlphaFold occasionally fails on novel folds, because the underlying problem is computationally hard.

The pattern in all these cases: **the system is fully deterministic, the answer is fully implied by the inputs and the rules, and yet running the rules is the cheapest possible way to extract the answer.** No oracle exists. No formula exists. No prediction exists that does not, in effect, simulate the system.

## What this means for the dominoes

Coming back to the original paradox: the dominoes are not redundant. They are paying the irreducibility bill.

For a 4-bit adder, the bill is small enough that you could pay it in your head. The dominoes are doing it because they are a physical demonstration of how the lock between physical motion and abstract operation works, not because the addition is hard. But the same structural argument applies to systems where the bill *cannot* be skipped, only paid in different currencies (silicon, neurons, dominoes, paper).

The arrangement contains the answer the way a sealed envelope contains its message — fully, completely, but inaccessibly. Opening the envelope is not redundant work. **It is the only way the message gets out.**

## The compressed punchline

> Computation is the conversion of logical determination into epistemic availability. Implication is free — the answer is fixed the moment the rules and inputs are. Knowing is not free — extracting the answer requires physical work. For some problems the work can be relocated to a faster substrate. For others, computational irreducibility means *the work itself is the cheapest possible representation of the answer*. The dominoes do not just deliver the result. They are the result.

The thing that surprised me most, sitting with this, is how *physical* the consequence is. Computational irreducibility is not a fact about minds or about our limitations. It is a structural fact about what kinds of patterns the universe contains. Some patterns admit closed-form shortcuts. Most do not. For the ones that do not, **running the system is not just our best method. It is the only method that can possibly exist.**

---

*This is a sharpening of [what computation actually is](what-computation-actually-is.md), which sets up the two-layer lock between physical mechanism and abstract structure. The free-will argument in [you are the program — Deutsch on identity and free will](you-are-the-program-deutsch-on-identity-and-free-will.md) builds directly on computational irreducibility — it is the reason a person's next thought cannot be predicted from the outside even in a deterministic universe.*
