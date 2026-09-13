# Value Functions — and Why Every Symbol in the Equation Has to Be There

**Context:** I was watching a lecture on reinforcement learning and paused on the value-function equation. I could read it, but reading isn't understanding. So I asked the question I try to ask of every equation now: not "what does this say" but **"what would break if each symbol weren't there?"** Every piece of it turned out to be solving a specific problem, and one of them I already knew from a completely different life.

---

## 1. The equation

$$V_\pi(s) = \mathbb{E}_\pi\left[\sum_{t} \gamma^t r_t \mid s_0 = s\right]$$

In English: *the value of a state `s` is the total reward you should expect to collect from now until the end, if you start at `s` and let your policy `π` drive — with far-away rewards counting for less.*

There are two central objects in all of RL. The **policy** `π(s, a)` is one — the probability of taking action `a` in state `s`, i.e. what you *do*. The **value function** is the other — what a situation is *worth*. Almost every algorithm in the field is a scheme for learning one, the other, or both.

---

## 2. The thing I already knew

This is net present value.

A state is an asset. The future rewards `r₁, r₂, …` are its cash flows. `γ` is the discount rate. `V_π(s)` is the DCF valuation of holding that asset under a specific management strategy `π`.

RL didn't invent discounting; it borrowed it from economics, and the borrowing is exact — same geometric series, same intuition that a payoff further away is worth less today. Finding a piece of my old working life sitting inside a machine-learning equation was the moment the equation stopped being notation.

But the analogy also has a seam worth noticing. In finance you discount because of interest rates and risk — the discount rate is a *fact about the world* you try to estimate correctly. In RL, `γ` is a **hyperparameter you choose**. It's a fact about the agent, not the world. That difference is what section 4 is about.

---

## 3. Why a sum, and not just the next reward?

Because greedy fails, and the failure is the whole reason the field is interesting.

A queen sacrifice scores terribly on the next move and brilliantly over the game. Any agent that maximizes the immediate reward will never make one. Summing over all future timesteps is exactly what permits present pain to be justified by future payoff — it is the mathematical definition of playing the long game.

This is also the dividing line between full RL and its simpler cousins. If your action has no effect on the future, the sum has one term, and you're in bandit territory — a much easier problem with much better algorithms. Value functions become the whole point precisely when actions have delayed consequences.

---

## 4. Why γ? It's doing three jobs at once

The discount factor looks like a detail. It's load-bearing three times over.

**It keeps the math finite.** A chess-like game can run arbitrarily long. Without discounting, a state's value could be an infinite sum — and infinities can't be compared, so "which state is better?" would have no answer. With `γ < 1` you get a geometric series, and the value is bounded by `r_max/(1−γ)`. No γ, no well-defined V.

**It encodes "sooner beats later."** A reward promised 50 moves out is less certain and less useful than one available now — the same reason ₹100 today beats ₹100 next year.

**It's the planning-horizon dial.** This is the practical one. An agent with discount factor γ effectively "sees" about `1/(1−γ)` steps ahead:

| γ | effective horizon |
|---|---|
| 0.5 | ~2 steps — barely past the next move |
| 0.9 | ~10 steps |
| 0.99 | ~100 steps |
| 0.999 | ~1000 steps |

That's not a metaphor, it's where the geometric weights fall off. And it means γ is one of the knobs that actually changes an agent's *character*: a low-γ agent is myopic in a way that looks like impatience, and a high-γ agent will accept long stretches of negative reward for a payoff it can barely see.

The horizon framing also explains a practical trap. Raising γ toward 1 to make an agent "smarter" makes the value estimates higher-variance and slower to converge, because each estimate now depends on a longer chain of noisy future events. You are not just asking for more foresight, you're asking for more evidence per unit of confidence.

---

## 5. Why the expectation?

Because the future is a lottery, twice over.

**The policy is random.** Look at `π(s, a)` — it's a *probability* of choosing each action, not a fixed rule. Exploration means the agent itself is a stochastic process.

**The environment is random.** The opponent's reply, the dice, the slip on the ice. Even with a deterministic policy, where you end up isn't determined.

So "total future reward from `s`" isn't a number, it's a *distribution*. The value is defined as its mean: imagine playing out a million games from this position and averaging the discounted totals.

Worth flagging what this throws away. Two states with the same expected value can have wildly different spreads — one a safe trickle, the other a coin flip between triumph and ruin. Standard RL is indifferent between them, by construction. That's a choice baked into the equation, not an oversight, and it's the thing risk-sensitive RL exists to revisit.

---

## 6. Why the π subscript? (the one that's easy to skip)

This one is subtle and I'd been sliding past it: **states don't have values in isolation.**

"How good is this chess position?" has no answer until you say who is playing from it. The same position is worth far more with a grandmaster at the wheel than a beginner. Change `π` and *every* value in the table changes.

The subscript is a reminder that V is a joint fact about a situation and a strategy. This is also why the tic-tac-toe learner in Sutton & Barto is explicitly learning to beat *one particular imperfect opponent* — its value table is not a truth about tic-tac-toe, it's a truth about playing this opponent. Swap the opponent and the table is wrong.

And it's why **minimax can't do this job**. Minimax computes something opponent-independent: it assumes perfect play, so it refuses to enter positions that lose under perfect play — even against an opponent who will never find the refutation. It leaves free wins on the table. A value function, by being policy-relative, is *allowed to exploit* the specific opponent it faces.

---

## 7. The payoff — why this equation is the heart of RL

Here's what pulled it together for me.

**In chess, `r_t = 0` on almost every single move.** The only real reward lands at checkmate, possibly a hundred moves later. If you only had rewards, you'd have almost no signal to learn from.

The value function is the mechanism that lets that single far-off reward be **felt today**. A strong position 20 moves before mate has value ≈ `γ²⁰ ×` (probability your policy converts it). V turns "this looks winning" into a number.

And then: *learning that number from experience* is what Q-learning, TD learning, and the critic in actor-critic are all doing. They differ in how they estimate V, not in what it is.

The next thing that falls out — and the step every course takes right after this — is noticing that `V(s)` can be written in terms of `V(next state)`:

$$V_\pi(s) = \mathbb{E}\left[r + \gamma V_\pi(s')\right]$$

That's the **Bellman equation**, and it's the move that makes the whole thing computable. The infinite sum collapses into a relationship between a state and its immediate successor — one step of lookahead instead of a thousand. Everything tabular in RL is some scheme for enforcing that relationship until it holds everywhere.

---

## 8. What I actually took away

The habit, more than the content. Reading an equation left to right tells you what it says. Asking "why is this symbol here, and what breaks without it?" tells you what it *is*:

| symbol | delete it and… |
|---|---|
| the sum | greedy agents; no queen sacrifices, no long game |
| `γ` | infinite values you can't compare; no planning horizon |
| `𝔼` | a distribution where you needed a number |
| `π` subscript | the illusion that positions have values on their own |
| conditioning on `s` | no notion of a situation being worth something |

Five symbols, five distinct problems, none of them decorative. That's a well-designed equation, and I don't think I would have seen it by reading the sentence underneath it in the textbook.
