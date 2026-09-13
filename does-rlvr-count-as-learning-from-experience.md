# Does RLVR Count as "Learning from Experience"? — and What Breaks When You Try

**Context:** Sutton and Silver keep describing the next paradigm as agents that learn from *experience*, in contrast to LLMs that learn from human data. I had a theory about this and wanted it checked: surely only pretraining uses human data, the RL afterwards uses real-world data, and so the LLM is just providing a head start before the same RL that Sutton and Silver want to run. I asked whether that was right. It was about 70% right, and the two places it was wrong are the interesting part — one of them is an unsolved problem I hadn't known existed.

---

## 1. The distinction isn't where I thought it was

My mental model located the human-data/experience split at the **pretraining vs post-training** boundary. That's the wrong seam.

In *all* post-training RL the model generates its own attempts, so "who produced the rollouts" doesn't separate anything. The actual distinction is:

> **where the reward comes from**, and **when the learning happens.**

Sort the pipeline on those two axes and it comes apart differently than I'd assumed:

| stage | reward source | in their frame |
|---|---|---|
| pretraining | none — imitation of human trajectories | not "experience" at all: no actions, no consequences, no reward |
| RLHF | a human, or a reward model distilled from humans, judging which output *looks* better | **still human data** |
| RLVR | an answer checker, a test suite, a proof checker — what actually happens when the attempt is run | genuinely a slice of experience |

**The correction to my theory: RLHF is not real-world data.** The response is never executed; nothing happens in the world. Silver files fine-tuning on human feedback and preferences squarely inside the era of human data, and later defines experience-grounded reward in explicit opposition to it — the reward should come from *the consequence an action has on the world*, not from a rater's opinion of the text.

So RLHF is arguably *more* human-derived than pretraining, not less. It's human judgement compressed into a scalar, then optimized against.

**Where my instinct was right: RLVR.** Here the reward does come from what actually happens when the attempt is checked or executed. Silver's own centrepiece example is exactly this shape — treat theorem-proving as a game, let the proof checker be the reward, run a self-play-style loop. He's careful that this starts "not quite from scratch" but from minimal knowledge, and he explicitly acknowledges LLM-based systems reaching comparable results, so he isn't claiming from-scratch is the only path.

---

## 2. The axis I'd missed entirely: design time vs runtime

This is Sutton's central distinction and the second place my theory broke.

An LLM does everything at **design time**. Once deployed, it learns nothing. And that's factually true of the current stack, in a way I hadn't traced through:

- RLVR happens in a training farm *before* shipping.
- Whatever a deployed model picks up in-context evaporates when the context ends.
- The lab's outer loop — harvest deployment data, fold it into the next training run — is centralized and months long. That's a company learning, not an agent learning from its own stream.

His argument for why this matters is the **big world** argument: the world is vastly larger than any dataset, so the part of it *you specifically* encounter — this project's quirks, this environment's conventions — can never have been in the training data. An agent that can't learn at runtime can't ever accumulate that.

Laid out as a table, the gap between the two programs is wider than "same RL, different starting point":

| axis | LLM post-training today | the Sutton/Silver program |
|---|---|---|
| reward source | human preference, or human-built verifiers | consequences in the environment |
| who poses the problems | humans curate every task and grader | the agent poses its own subproblems |
| when learning happens | training phase, then weights freeze | continually, during deployment, forever |
| horizon | short episodes that reset | a lifelong stream |
| form of knowledge | a frozen input→output mapping | options and models of options, used for planning |

So "LLMs provide the head start and then it's the same RL" understates the distance. The head-start framing is roughly Silver's position and roughly the frontier labs' working bet. Sutton explicitly rejects it — and the reason isn't philosophical stubbornness. It's that the missing ingredient is an **unsolved algorithms problem**.

---

## 3. The scope correction that reframed everything

Here's the sentence that made this worth an entry:

> Deep RL as you know it is **not** unsolved. *Continual* deep RL is.

Everything that works today — self-play game agents, RLVR, all of post-training — leans on the same three crutches:

1. start from a fresh random initialization,
2. train on shuffled or replayed data until convergence,
3. then freeze the weights forever.

Sutton's program requires learning from a never-ending stream: no resets, no replay of the full past, no freeze. Remove those three crutches and plain gradient descent fails in **two dual ways.**

---

## 4. Failure one: catastrophic forgetting — the network can't retain

Gradient descent updates weights to reduce loss on whatever data is in front of it *right now*. Nothing in the update rule protects old knowledge that isn't in the current batch.

Normal training hides this completely, because shuffled replay keeps re-presenting everything. On a stream, the past never comes back — so new learning physically overwrites the weights that encoded old learning.

This has been known since 1989 and is still unsolved in general.

---

## 5. Failure two: loss of plasticity — the network can't acquire

This one I'd never heard of, and it's the better story.

Train a network on a long sequence of tasks and it gradually loses the ability to learn *anything new* — eventually learning worse than a shallow linear model would. Not forgetting the old; **losing the capacity to absorb the new.**

The mechanism is genuinely elegant and slightly disturbing. A real portion of deep learning's magic lives in the **fresh random initialization** — small, diverse, uncorrelated weights that give gradients traction. Training *spends* that diversity: units saturate and go dead, weights grow, features become correlated, the representation's effective rank collapses.

**Gradient descent consumes the randomness and never replenishes it.**

And the reason nobody noticed for thirty years is the best part: we always train once from a fresh initialization and then stop. That's precisely the regime continual learning forbids. The bug was invisible because the standard practice never enters the region where it appears.

Notice the two failures are mirror images — *can't keep the old, can't absorb the new* — and both trace to the same crudeness: vanilla gradient descent treats every weight identically at every moment.

---

## 6. The fixes, and why they're the same idea twice

Once the diagnosis is "every weight treated identically," the proposed fixes read as obvious, which is the mark of a good diagnosis:

**Continual backprop.** Track a utility score for every unit — how much it actually contributes to outputs. Periodically reinitialize a tiny fraction of the *least useful* units to fresh random values. Rather than spending the free lunch of random initialization once at birth, **meter it in continuously, forever.** In the published experiments this keeps plasticity intact indefinitely.

**Per-weight learning rates, learned online.** Learn a step size for every weight, from the stream itself. Weights encoding proven, reliable knowledge earn tiny step sizes — protected from being overwritten, which attacks *forgetting*. Weights that haven't proven useful keep large step sizes — staying plastic, which attacks *rigidity*.

That second one is the elegant bit: **the stability-versus-plasticity dilemma stops being one global trade-off and becomes a per-weight decision that is itself learned.** You don't pick a point on the trade-off; you let the system pick a different point for every parameter.

**Generate-and-test feature discovery.** The general frame: generate candidate features, test them by tracked utility, cull the useless, repeat forever — a self-organizing economy of features rather than one monolithic gradient flow. Continual backprop is one instance of it. And the honest gap is acknowledged: for genuinely *novel* feature generation there's no complete proposal yet.

---

## 7. What I actually updated

**My theory was structurally right and wrong about the hard part.** LLM-as-head-start is a reasonable description of the current bet, and it is roughly what one of the two people I was reading actually thinks. What it misses is that the remaining gap isn't a staging decision anyone could make tomorrow — it's two named failure modes of gradient descent that have resisted solution for decades.

**"Learning from experience" has a sharp technical meaning here.** Not "trained on real data" but *reward from consequences* plus *learning during deployment*. By that definition RLHF isn't experience at all, RLVR is experience with the second half missing, and nothing shipped today has both.

**The best epistemic lesson is the loss-of-plasticity one.** A failure mode sat undiscovered for thirty years because standard practice never entered the regime where it appears. Every methodology has a shape, and the shape determines which bugs are *observable* — which is a much more general worry than continual learning, and the reason I've started asking of any process I rely on: what would this be structurally incapable of showing me?
