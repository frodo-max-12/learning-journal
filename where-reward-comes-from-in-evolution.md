# Where Reward Comes From — the Evolutionary Origin of Reinforcement Learning

**Context:** Watching Rich Sutton talk about reward as the basis of intelligence, I got curious about a question the theory doesn't address: **when did reward first appear?** Apes obviously have it. Cats and dogs presumably. How far back does it go — do bacteria have it? The answer required unbundling three different things I'd been treating as one, and the boundary between them turns out to be exactly the boundary Sutton's framework cares about.

---

## 1. Three things get called "reward"

**1. Gradient-following without learning.** *E. coli* chemotaxis: the bacterium compares the last second of sugar concentration against the previous few, and tumbles less when things are improving. That's a value signal driving action — genuinely.

But **the policy is hardwired in the genome.** Nothing is learned during the bacterium's lifetime. The optimizer was evolution; the reward was fitness; the training took a billion years and finished before this particular cell existed.

On Sutton's framing this isn't reward learning at all. It's **a fixed policy that happens to have been trained offline.**

**2. Lifetime learning from a scalar signal.** This is the real threshold, and it requires specific machinery: a **neuromodulator that broadcasts "what you just did was good" and gates synaptic change.** Something has to carry the signal globally, and something has to make the synapses listen.

**3. Prediction of future reward.** Not just responding to reward, but learning to *anticipate* it — the temporal-difference structure. This is the part that looks most like the algorithms.

Naming those three separately is most of the answer, because they have completely different answer dates.

---

## 2. The threshold is much earlier than I guessed

I'd assumed lifetime reward learning was a vertebrate thing, maybe a mammal thing. It isn't.

- **Roundworms** — *C. elegans*, **302 neurons** — learn food-and-odour and food-and-temperature associations, using dopamine and octopamine. Roundworms do reinforcement learning.
- **Sea slugs** — operant conditioning, with dopamine driving plasticity in a *single identified neuron*. You can point at the cell.
- **Insects** — the fruit-fly mushroom body is close to a textbook **actor-critic**. Dopamine neurons carry something very like a prediction error, and they teach a sparse-coded representation of odour.

The 302-neuron figure is the one that lands. A nervous system you could draw on one page does the thing.

And because worms, molluscs, and insects all use **the same monoamine machinery**, it plausibly dates to the last common bilaterian ancestor — roughly **550–600 million years ago**. Something small and wormlike, with no brain to speak of.

**Possibly earlier still:** box jellyfish, with no centralized brain and around a thousand neurons, were shown in 2023 to learn to avoid obstacles from experience. If that holds up it pushes some form of it back to cnidarians, around 700 million years ago.

So: **bacteria, no. Worms, yes. It's roughly as old as neurons themselves.**

---

## 3. Why the bacterium is the interesting case

The *E. coli* answer is the one worth sitting with, because it's a boundary case that clarifies the definition rather than just failing it.

The bacterium is doing something that satisfies almost every informal description of reward-driven behaviour: it senses a gradient, it acts to improve its situation, and the behaviour is adaptive. If you watched it without knowing the mechanism you'd say it *wants* sugar.

What it isn't doing is **changing as a result of what happened.** Run the same bacterium through the same experience twice and it behaves identically the second time.

That gives a clean test, and it's the same distinction Sutton draws between design time and runtime for machine learning systems:

> **Where does the adaptation live — in the genome, or in the lifetime?**

Evolution is an optimizer. It produces well-adapted policies. But the policy is fixed at birth, and improvement happens across generations rather than within an individual. Reinforcement learning, in the sense that matters, requires **the individual to be different tomorrow because of today.**

Which is exactly the property current AI systems lack — weights frozen after training, adaptation happening in the lab's next run rather than in the deployed agent's own stream. **A deployed model is, on this axis, closer to the bacterium than to the worm.** Both execute a policy optimized offline; neither updates from its own experience.

That parallel is the most useful thing I got from the question, and I didn't expect a question about bacteria to land there.

---

## 4. The machinery requirement

The second thing I hadn't appreciated: lifetime reward learning isn't just "having neurons." It needs a specific architectural feature — **a global broadcast channel that can say "that was good" to synapses that were recently active**, and synapses that change in response.

That's a real design requirement, and it's why the threshold is a threshold rather than a gradient. You either have a neuromodulatory system that gates plasticity or you don't. And the fact that worms, slugs, and flies all use the same chemical family for it is decent evidence the solution was found once and inherited, rather than invented repeatedly.

There's something satisfying about that: the credit-assignment problem — *which of my recent actions caused this outcome?* — was solved by evolution with a broadcast neuromodulator over half a billion years ago, and it's still the shape of the answer in the algorithms.

---

## 5. What I took away

**"When did X first appear?" is a good way to sharpen a definition.** I couldn't answer the question until I'd split reward into three things, and the split is more useful than the dates. Hardwired gradient-following, lifetime learning from a scalar signal, and prediction of future reward are genuinely different capabilities with different requirements.

**Learning during a lifetime is the line that matters**, and it's the same line that separates today's AI systems from the thing they're often described as. A system whose policy was optimized offline and frozen is doing what the bacterium does, however sophisticated the policy.

**Half a billion years is the age of the mechanism.** Reinforcement learning isn't a recent idea being tested on machines — it's roughly as old as nervous systems, and the algorithms are a rediscovery of a very old solution to credit assignment.
