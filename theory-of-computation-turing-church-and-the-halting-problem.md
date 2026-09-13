# Theory of computation — Turing, Church, and the halting problem

*Learned on March 1, 2026. I was studying the foundations of computer science and asked two separate questions: one about Alan Turing's theory of computation, and another about the Church-Turing thesis. The answers connected into a single, coherent story about what computation fundamentally is — and what it cannot do.*

---

## The question that started it all

In 1928, the mathematician David Hilbert posed what he called the **Entscheidungsproblem** — German for "decision problem." The question was deceptively simple: is there a mechanical procedure that can determine the truth or falsity of any mathematical statement?

Hilbert believed the answer was yes. Mathematics, in his view, should be complete (every true statement is provable), consistent (no contradictions), and decidable (there exists a procedure to determine truth). Kurt Godel had already demolished the first two hopes in 1931 with his incompleteness theorems. The Entscheidungsproblem was the last piece standing.

In 1936, two people independently proved Hilbert wrong about decidability — and in doing so, created the theoretical foundations of computer science. One was Alan Turing, a 23-year-old graduate student at Cambridge. The other was Alonzo Church, a professor at Princeton. They used completely different approaches and arrived at the same answer: **no**, there is no such mechanical procedure. Some well-defined mathematical questions are fundamentally unanswerable by any algorithm.

But to prove this, Turing first had to answer a more basic question: what *is* a "mechanical procedure"?

## The Turing machine — an absurdly simple idea

Turing's answer was to invent the most stripped-down possible model of computation. His 1936 paper, "On Computable Numbers," describes a device now called a **Turing machine**. It has:

1. **An infinitely long tape** divided into cells. Each cell holds a symbol from a finite alphabet (say, 0 and 1, plus a blank).
2. **A read/write head** that sits over one cell at a time. It can read the symbol, write a new symbol, and move one cell left or right.
3. **A finite set of states** the machine can be in (like "state A," "state B," etc.), including a designated start state and halt states.
4. **A transition table** — a set of rules that say: "If you're in state X and you read symbol Y, then write symbol Z, move left/right, and switch to state W."

That is the entire machine. No memory beyond the tape. No arithmetic unit. No operating system. Just a tape, a head, some states, and rules.

I find it helpful to think of it as the world's most patient bureaucrat. The bureaucrat sits at a desk with an endless roll of paper. They look at the current square, consult their instruction manual (the transition table), write something down, slide the paper one square left or right, and update their mental state. They do this over and over until the instructions say "stop" — or they keep going forever.

Here is a concrete example. A Turing machine that adds 1 to a binary number written on the tape:

```
State: Start, reading: 0 → write 0, move right, stay in Start
State: Start, reading: 1 → write 1, move right, stay in Start  
State: Start, reading: blank → move left, go to Add
State: Add, reading: 0 → write 1, go to Halt
State: Add, reading: 1 → write 0, move left, stay in Add
State: Add, reading: blank → write 1, go to Halt
```

This machine scans right to the end of the number, then walks left, flipping 1s to 0s (the carry) until it finds a 0 to flip to 1. Simple, mechanical, mindless — and it correctly performs binary addition.

## The breathtaking claim

Here is what makes Turing's idea so powerful: **this absurdly simple device can compute anything that is computable.** Any calculation that any computer program can perform — sorting a list, rendering a web page, training a neural network, computing digits of pi — can in principle be done by a Turing machine.

It will be unimaginably slow. It will use unimaginably much tape. But it can do it.

This is not just a theoretical curiosity. It means that computational power does not come from hardware sophistication. It comes from the logical structure of following rules. A modern processor with billions of transistors and a Turing machine with a paper tape compute the same class of functions. The difference is speed, not capability.

## The universal Turing machine — the idea that became every computer

Turing then asked: can I build a single Turing machine that simulates any other Turing machine? The answer is yes. You encode the description of any Turing machine (its states, rules, and input) onto the tape of a **universal Turing machine**, and the universal machine reads that description and faithfully executes it.

This is the conceptual leap that led to modern computers. A universal Turing machine is a machine whose behavior is determined by its input — the program stored on its tape. Before this, machines were designed for single purposes: a calculator calculates, a loom weaves a specific pattern. Turing showed that a single machine could do anything, if given the right instructions.

> The computer I am typing on right now is a physical realization of Turing's universal machine. It is hardware that reads software — a general-purpose device whose behavior is determined by the program you feed it.

## The halting problem — the wall computation cannot cross

With the universal Turing machine in hand, Turing proved something astonishing about its limits.

**The halting problem:** Is there a Turing machine that can examine any other Turing machine (and its input) and correctly decide whether that machine will eventually halt or run forever?

The answer is no. Here is the argument, which is a beautiful example of proof by contradiction.

Suppose such a machine exists. Call it H. Given any program P and input I, H(P, I) outputs "halts" or "loops forever," and it is always correct.

Now construct a devious new program D that does the following:
- D takes a program P as input
- D runs H(P, P) — asking whether P halts when given itself as input
- If H says "halts," then D goes into an infinite loop
- If H says "loops forever," then D halts

Now run D on itself: D(D).

- If H says D(D) halts, then by D's construction, D goes into an infinite loop — contradiction.
- If H says D(D) loops forever, then by D's construction, D halts — contradiction.

Either way, H gives the wrong answer. Therefore H cannot exist. No program can solve the halting problem in general.

This reminds me of the liar paradox — "this sentence is false" — but made mathematically rigorous. The trick is self-reference: feeding a program its own description creates a paradox that no decision procedure can resolve.

The implication answered Hilbert's question. Since there are programs whose halting behavior cannot be decided by any algorithm, there are mathematical questions (framed as "does this program halt?") that no mechanical procedure can answer. The Entscheidungsproblem has no solution.

## Church's parallel path — lambda calculus

While Turing was building his abstract machines, Alonzo Church at Princeton was taking a completely different approach. Church invented the **lambda calculus** — a formal system based on function abstraction and application. Where Turing's model is mechanical (tapes, heads, states), Church's is mathematical (functions that take functions as inputs and produce functions as outputs).

Lambda calculus has no variables being mutated, no memory cells being overwritten. Everything is a function. Even numbers can be encoded as functions (Church numerals). The number 2, for instance, is "a function that applies another function twice."

Church proved that there are functions in the lambda calculus that cannot be computed — reaching the same conclusion as Turing through entirely different means.

The remarkable thing is that these two formalisms — one built from imagining a person mechanically following rules on paper, the other from pure mathematical abstraction about functions — turned out to compute exactly the same class of functions. Everything computable by a Turing machine is computable in lambda calculus, and vice versa.

## The Church-Turing thesis

This convergence led to the **Church-Turing thesis**: any function that is "effectively computable" — meaning it can be calculated by some systematic method — is computable by a Turing machine.

This is not a theorem. It cannot be formally proved because "effectively computable" is an informal, intuitive notion, not a mathematical definition. The thesis is a bridge between human intuition ("I know an algorithm when I see one") and mathematical precision ("a Turing machine can compute it").

What gives the thesis its force is inductive evidence. Every alternative model of computation that has ever been proposed — lambda calculus, recursive functions, register machines, cellular automata, Post machines, tag systems — has turned out to compute exactly the same class of functions as a Turing machine. Nobody has ever found a counterexample: a reasonable model of computation that is either strictly weaker or strictly more powerful.

| Model of computation | Inventor | Year | Equivalent to Turing machine? |
|---------------------|----------|------|------------------------------|
| Lambda calculus | Alonzo Church | 1936 | Yes |
| General recursive functions | Godel/Herbrand | 1934 | Yes |
| Post machines | Emil Post | 1936 | Yes |
| Register machines | Various | 1960s | Yes |
| Cellular automata | Von Neumann | 1940s | Yes |
| Game of Life | John Conway | 1970 | Yes |

Even quantum computers, which can solve certain problems exponentially faster than any known classical algorithm, do not compute anything a Turing machine cannot compute given sufficient time. They challenge the **efficient** version of the thesis (which says a Turing machine can efficiently simulate any physical computation), but not the thesis itself.

## What "computable" means — and what it doesn't

The theory of computation gave us a precise boundary. On one side: problems that algorithms can solve. On the other: problems that no algorithm can solve, not because we haven't found the right algorithm yet, but because *no such algorithm can exist*.

The halting problem is the most famous undecidable problem, but there are many others: determining whether two programs compute the same function, whether a given statement in first-order arithmetic is true, whether a set of tiles can tile the plane. These are not open problems awaiting clever solutions. They are provably, permanently beyond the reach of computation.

I find this simultaneously humbling and clarifying. Humbling because it means there are hard limits to what software can do — no matter how fast the hardware, no matter how clever the programmer. Clarifying because it tells me exactly where those limits are. Knowing what cannot be computed is as valuable as knowing what can.

The work that Turing and Church did in 1936 did not just answer Hilbert's question. It defined what it means to compute, gave us the blueprint for programmable computers, and drew the permanent boundary of algorithmic problem-solving. Everything in computer science since — programming languages, operating systems, complexity theory, artificial intelligence — is built on the foundation they laid in that single remarkable year.

---

*What I studied next: von Neumann's stored-program architecture and how Turing's theoretical universal machine became the design principle behind every physical computer.*
