# Physics and computation — locked, not nested

*Pushed back on a claim I had read several times: "quantum mechanics requires computation." It sounded too strong. Computation clearly needs a physical substrate to actually run, but does physics actually require computation in any reverse sense, or is that backwards? The honest answer turns out to be layered — and the layering matters.*

---

## The forward direction is unambiguous

**Computation requires a physical substrate. Always.**

Even abstract computation, when *actually run* anywhere, has to live somewhere — silicon, neurons, dominoes, ink on paper, atoms moving in space. There is no computation without something physical doing the work. **Landauer's principle** made this rigorous in the 1960s: information is physical. Erasing a single bit has a minimum unavoidable energy cost — proven, measurable, real. The Landauer limit at room temperature is *kT* ln 2, which works out to about 2.85 × 10⁻²¹ joules per bit erased. This is not a practical engineering limit. It is a thermodynamic theorem.

So that direction is solid bedrock. Computation, when it happens, *always* happens in physics. There is no Platonic free lunch. Computation pays rent in physics every time it runs.

## The reverse direction is more interesting

Does physics need computation?

This is where loose claims often get made. "Quantum mechanics requires computation" sounds dramatic, but on close inspection it is not quite right. What *is* true requires careful layering. Let me write out the four levels of certainty separately, because they are usually jumbled together when this gets discussed.

### Layer 1 — solid (mainstream Deutschian)

The **Church-Turing-Deutsch principle**. Deutsch's most famous physical postulate, from his 1985 paper:

> Every finitely realisable physical system can be perfectly simulated by a universal model computer operating by finite means.

This makes physics and computation **co-extensive**. Whatever physics can do, computation can in principle simulate. Whatever computation can do, some physical process can in principle realise. They cover the same territory.

But notice — this is not "physics *requires* computation as a substrate." It is "physics and computation cover the same territory." They constrain each other, neither is a substrate for the other. If anything, the dependence still runs forward (any actual computation needs a physical realisation).

### Layer 2 — solid, broadly accepted in foundations

Quantum mechanics, as a theory, is fundamentally **informational**. Modern quantum information theory — Bennett, Brassard, Wheeler, Bennett and DiVincenzo, others — treats QM as a theory about *what information operations are allowed in nature*. Entanglement, the no-cloning theorem, Bell inequalities, decoherence, superdense coding — these are theorems about information processing.

The formalism makes this concrete. Unitary operations on Hilbert spaces — the mathematical core of quantum mechanics — are essentially the math of reversible computation. Quantum gates are unitary operators. Quantum circuits are sequences of those gates. The deepest structural facts about QM and the deepest structural facts about reversible computing are the same facts in different vocabulary.

Wheeler (not Deutsch) coined the slogan **"It from Bit"** for this view: the physical world is fundamentally informational, and the laws of physics are best read as constraints on what information processing nature permits. This is the more honest version of "physics needs computation" — physics doesn't need computation as a *substrate*, but it is most naturally formulated in computational/informational language.

### Layer 3 — Deutsch's specific argument

Deutsch argues that **quantum computation is evidence for many-worlds**. The argument is striking once you see it.

Shor's algorithm factors an *n*-bit number in roughly polynomial time on a quantum computer, exponentially faster than any known classical algorithm. To factor a 500-digit number on a quantum computer, you would perform operations involving roughly 2^1700 distinct quantum states in superposition.

Deutsch's question: where, physically, does that computation actually happen?

The number 2^1700 is vastly larger than the number of atoms in the observable universe (about 10^80, or ≈ 2^266). So if a quantum computer actually factored that number, the computation cannot have happened "in" the atoms of the visible universe. Deutsch's answer: it happens across the branches of the multiverse. The quantum parallel computation is parallel across Everett branches.

Here, computation is not just *described by* physics. It is actually *telling us something about what physics must be like*. The fact that quantum computers can do what they do is, on Deutsch's view, evidence for a particular physical structure of reality. **Computation talks back to physics.**

This argument is defensible, taken seriously by serious physicists, and contested. It is not mainstream consensus. It is one of the most interesting interpretations of why quantum computing works, and not the only interpretation.

### Layer 4 — speculative (minority view, not mainstream)

Wolfram, Konrad Zuse, and a few others argue that **the universe literally *is* a computation** — that physics is the running of some simple computational rule, like a giant cellular automaton. Wolfram's *A New Kind of Science* (2002) and his more recent Physics Project pursue this seriously. The claim is much stronger than CTD. It says physics doesn't just *correspond to* computation; the bottom of physical reality is literally a computational process.

This goes well beyond Deutsch and beyond mainstream physics. Interesting to track, not settled, currently a minority view. The relevant point for honesty: this is *speculative*, and conflating it with the more solid layers above is where loose claims about "the universe is a computer" tend to come from.

## The layered picture, written out

| Claim | Status |
|---|---|
| Computation needs a physical substrate | Solid. Always. (Landauer's principle.) |
| Physics and computation are co-extensive (CTD principle) | Solid. Mainstream Deutschian. |
| QM is best formulated in informational/computational language | Solid. Mainstream in foundations. |
| Quantum computers tell us what physics must be like (multiverse) | Deutsch's view. Defensible, contested. |
| The universe literally *is* a computation | Speculative. Minority view. |

The honest version of the original loose claim: **quantum mechanics is best formulated and understood in computational/informational terms, and physics and computation co-constrain each other via the Church-Turing-Deutsch principle.**

The dependence is **not substrate-like** in the reverse direction. Physics does not "run on" computation the way computation runs on physics. Computation is anchored to physics in a stronger way than physics is anchored to computation. **The asymmetry is real.**

But the relationship is also not one-way. They are not independent. They are locked together — illuminating each other, constraining each other, neither fully reducible to the other. The right picture is **locked, not nested.**

## Why this matters for the four-strand picture

This is exactly *why* Deutsch keeps quantum and computation as **two separate strands** in *The Fabric of Reality* rather than collapsing them. If physics literally reduced to computation (Wolfram's view), he would need only one strand and could discard the other. If computation reduced to physics (the eliminativist view about abstract objects), the same.

He keeps two precisely because the relationship is **mutual constraint, not reduction**. Each illuminates what the other cannot say alone. Quantum mechanics adds structural facts (multiverse, entanglement, no-cloning) that computational theory does not derive. Computational theory adds structural facts (universality, irreducibility, halting undecidability) that quantum mechanics does not derive. Both are needed. Neither is enough.

Once this distinction is sharp, a lot of casual claims about "the universe is computational" become more interesting to evaluate. Most of them are conflating Layer 3 or Layer 4 with the more solid Layers 1 and 2. The solid claim is "physics and computation are deeply linked and probably best formulated together." The speculative claim is "the universe is literally running a cellular automaton at the bottom." These are not the same claim, and the difference matters.

## The compressed picture

> Computation always needs physics. Physics doesn't always need computation, but it is best formulated in computational/informational language. The Church-Turing-Deutsch principle locks the two domains as co-extensive. Whether physics is *literally* a computation at the bottom is an open speculative question, distinct from the solid claim that physics and computation deeply constrain each other.

The lesson for me, sitting with this, is mostly about epistemic hygiene. It is easy to make a claim like "the universe is a computation" sound profound and have it actually be a slide between four very different statements with very different evidential support. The four-layer breakdown is the cleanest tool I have come across for keeping those statements separate while still appreciating how tightly the two domains are linked.

---

*This is a pendant to [the four strands of *The Fabric of Reality*](the-four-strands-of-the-fabric-of-reality.md), which describes why physics and computation are kept as separate strands. It also depends on [what computation actually is](what-computation-actually-is.md) for the substrate-independence claim.*
