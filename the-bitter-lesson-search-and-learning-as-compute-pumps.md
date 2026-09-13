# The Bitter Lesson — Search and Learning as Compute Pumps

**Context:** I read Rich Sutton's 2019 essay *The Bitter Lesson* and went through it paragraph by paragraph, because the summary version everyone quotes ("just scale it") is a worse idea than the essay actually contains. The sentence that turned out to be load-bearing is the one about search and learning being the two methods that "scale arbitrarily with computation" — and unpacking *why* those two specifically is where the essay stops being a slogan.

---

## 1. The thesis, and the mechanism underneath it

Sutton's claim: across roughly 70 years of AI research, general methods that leverage computation have beaten methods built around human domain knowledge — and by a large margin.

The reason he gives is **economic, not algorithmic.** Compute per unit cost has fallen exponentially for decades. That creates a trap in how research actually gets done:

- Within one research project — a few years — available compute is roughly *constant*.
- If compute is fixed, the only lever left is cleverness: encoding what you, the expert, know about the domain.
- So researchers rationally optimize for the short term by adding human knowledge.
- But over a slightly longer horizon, compute grows by orders of magnitude, and then the only thing that matters is whether your method can *absorb* it.

The subtle part, which the slogan version drops: in principle human knowledge and computation-leveraging could coexist. In practice they conflict, for three reasons — researcher time spent on one isn't spent on the other; people become psychologically and professionally invested in an approach; and, most technically, **knowledge-heavy systems become complicated and full of special cases, which makes them structurally bad at exploiting more compute.**

That last one is the actual argument. A hand-tuned rule doesn't get better when you give it 1,000× the cycles. A search or learning procedure does.

---

## 2. The concept I'd been skating over: what "scales with computation" means

Here's the question that reframed the essay for me. If compute doubles every couple of years, **what kinds of methods can actually absorb that?**

A hand-written rule — "control the centre of the board" — is a *constant*. Give it a thousand times the cycles and it plays exactly as well as before. Extra compute has nowhere to go.

What you want are procedures that behave like **compute pumps**: feed in more cycles, get out better decisions, indefinitely. Sutton names two families with that property, and they differ in *when* the compute is spent and *what the spending buys*.

---

## 3. Search — paying at decision time

Search means that when you face a specific situation, you spend compute *right then*, simulating possible futures. In chess: from the current position, try each legal move, then each opponent reply, then each reply to those. Evaluate the positions at the tips of the tree, propagate the evaluations back up, play the move leading to the best outcome.

Why this absorbs unlimited compute: **the tree is effectively bottomless.** Chess has ~35 legal moves per position, Go ~250, so the tree grows exponentially with depth — more positions than atoms in the universe. No amount of compute exhausts it. Which means every doubling buys real depth: you see further ahead, or consider more alternatives, and the decision genuinely improves.

Two defining properties:

- **The compute is spent per decision and then it's gone.** Face a new position tomorrow, pay again. Nothing is retained.
- **It's exquisitely specific.** All the effort goes into reasoning about *exactly this situation*, which is why search handles novel, weird positions that no prior experience covers.

What it requires is a **model** — the rules, a simulator — so you can generate hypothetical futures at all.

---

## 4. Learning — paying in advance

Learning spends the compute *before* any particular decision arises. Take a mass of experience — millions of games, thousands of hours of audio — and use compute to fit a **function** mapping situation to judgment. A value function is the canonical case: board position in, "how good is this for me" out.

This scales just as bottomlessly, along different axes: more data, a bigger model, more training steps all keep buying accuracy.

The payoff structure is the *mirror image* of search. The huge cost is paid once, up front, and then answering is nearly free — a single forward pass, microseconds. That one-time cost is amortized over every decision the system will ever make.

The trade-off is that the answer is a **generalization from past experience rather than fresh reasoning about the present case**: instant, broadly right, approximate, and potentially wrong in situations unlike anything in training. And where search needed a simulator, learning needs data.

| | search | learning |
|---|---|---|
| when compute is spent | at decision time, every time | once, in advance |
| what it needs | a model / simulator | experience / data |
| cost per decision | high, recurring | almost zero, after training |
| handles novel situations | yes — reasons about this case | poorly — extrapolates from the past |
| what more compute buys | depth, breadth of lookahead | accuracy, capacity, generalization |
| retained afterwards | nothing | everything |

Seeing them as complementary rather than competing is what made the modern systems make sense. AlphaGo is both: a learned value/policy network (paid in advance) guiding a Monte Carlo tree search (paid at move time). And "test-time compute" — reasoning models that think longer on harder problems — is the search column reappearing in a field that had spent a decade almost entirely in the learning column.

---

## 5. The case studies, and the part that's about people

**Chess.** Deep Blue beat Kasparov in 1997 using massive brute-force search — around 200 million positions per second on custom hardware. For decades most computer-chess researchers had pursued the opposite: programs playing "the way grandmasters do," with selective, knowledge-guided search modelled on human cognition. Sutton's line is that when simple search plus special hardware crushed that program, the researchers "were not good losers" — brute force won *this time*, they said, but it isn't general and it isn't how humans play.

His implicit rebuttal: the criticism had it exactly backwards. **Search is the general method; the human-knowledge approaches were the parochial ones.**

**Go.** The same story ~20 years later. Go was thought immune to search — 19×19 board, ~250 moves per position, and a hand-written evaluation function is notoriously hard because a stone's value depends on the whole board. So Go became the flagship domain for pattern libraries and expert rules, which plateaued at strong-amateur level for decades. Then Monte Carlo tree search (which converts raw compute directly into position evaluation by playing out many random games) and then AlphaGo.

What I hadn't appreciated is that MCTS is the purest illustration of the whole thesis: instead of a hand-crafted formula judging a position, it plays thousands of fast semi-random games from that position and counts the wins. **The evaluation is raw computation.** No knowledge at all.

The essay's real subject, though, is the psychology. Sutton keeps returning to the observation that researchers *wanted* the human-knowledge methods to win, and that preference shaped their scientific judgment. That's what makes the lesson bitter rather than merely surprising — it isn't a fact about algorithms, it's a fact about how we keep evaluating algorithms.

---

## 6. Where I'd push back

The essay is genuinely strong, and I think the slogan it gets compressed into is much weaker than the argument.

**"Scale is all you need" is not what it says.** The claim is about *methods that can absorb computation* beating methods that can't. Inventing a method with better scaling properties is entirely inside the thesis — arguably it's the thesis's main implication. Transformers over LSTMs is a bitter-lesson-compliant *architectural* insight, not a repudiation of one.

**It's an observation about a period, presented as a law.** Seventy years of exponentially falling compute cost is the premise doing all the work. The argument's own logic says that if that curve flattens, the conclusion weakens — which makes it an empirical claim with an expiry condition rather than a principle.

**It doesn't say human knowledge is useless — it says knowledge that can't be absorbed by a scalable method loses.** The distinction matters in practice. Encoding a domain rule as a special case is the losing move; encoding it as training data, an environment, or a verifiable reward is the winning one. Same knowledge, different container.

Which is the reading I've kept: the essay isn't an argument against thinking hard about a domain. It's an argument about **where** to put what you know — into the structure of the method, where it becomes a ceiling, or into the data the method consumes, where it becomes fuel.
