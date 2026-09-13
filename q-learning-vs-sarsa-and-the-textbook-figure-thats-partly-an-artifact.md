# Q-Learning vs SARSA — and the Textbook Figure That's Partly an Artifact

**Context:** My RL path said "implement tabular Q-learning and SARSA yourself on FrozenLake and CliffWalking." I did it in raw NumPy — no RL libraries, ~35 lines of actual learning code each. What I expected was to reproduce Sutton & Barto's famous cliff-walking picture. What I got was the picture *plus* two standard claims about it that turned out to be false when I computed the exact answer. That second part is the reason this is worth writing down.

---

## 1. The two algorithms, and the one line between them

Both algorithms learn a table `Q[state, action]` — "how much total reward do I expect if I take this action from this state and behave normally afterward." Both update it after every step using the same shape: nudge the old estimate toward a better-informed one.

The entire difference is what "better-informed" means:

```python
td_target = r + gamma * Q[s2].max()    # Q-learning: value of the BEST next action
td_target = r + gamma * Q[s2, a2]      # SARSA:      value of the action it WILL take
```

That's it. One line.

Q-learning assumes that from the next state it will act optimally. SARSA uses the action it actually selected — which, because the agent explores, is sometimes a random one. This is the whole content of the phrase **off-policy vs on-policy**, and it took writing both to see that the distinction is not philosophy. It's `.max()` versus an index.

The name SARSA is just its own update written out: **S**tate, **A**ction, **R**eward, next **S**tate, next **A**ction. You need all five in hand before you can update, which is why SARSA has to choose the next action *before* it learns from the current one — a small structural difference in the loop that follows directly from the equation.

---

## 2. Cliff walking, and why the two behave differently

CliffWalking is a 4×12 grid. Start bottom-left, goal bottom-right, and the twelve cells between them are a cliff: step on one and you get **−100** and get teleported back to the start. Every other step costs **−1**.

The optimal path is obvious to a human — walk along the very edge of the cliff, 13 steps, total reward −13. Q-learning finds it. It's provably optimal; I verified it against an exact solver.

SARSA doesn't. It walks a longer route further from the cliff.

The reason is the one line. The agent is exploring with ε-greedy — a small chance of a random move at every step. Q-learning's target asks *"what's the best I could do from the next square?"* and the answer never includes falling off, because falling off is never the best action. So Q-learning learns the value of the edge path as if it walked it perfectly. Then it goes and walks it with a 10% chance of randomly stepping sideways into the cliff.

SARSA's target asks *"what will I actually do from the next square?"* — and sometimes the answer is "something random." The −100s that its own exploration causes get folded back into the values of the cells near the cliff. It learns that being near the cliff is dangerous *for an agent that explores*, which is true, because it is one.

The measured result over 10 seeds:

```
Q-learning   greedy policy: −13     (provably optimal)
Q-learning   online return: −46.0   (what it actually collected while learning)
SARSA        online return: −28.8
```

So the standard summary is right: Q-learning learns the better policy, SARSA behaves better while learning. Q-learning walks the cliff edge, and its own exploration keeps shoving it off.

---

## 3. The part I got wrong, and how I found out

Reproducing the figure isn't the same as understanding it. I had written two claims into my own summary, both of which I'd absorbed from tutorials and believed:

1. *"Decay ε toward zero and SARSA converges to Q-learning's optimal path."*
2. *"SARSA takes the top row"* — the safest possible route, as far from the cliff as the grid allows.

Then I built a dynamic-programming solver for the same MDP. Not a learner — a solver. Because the transition probabilities of CliffWalking are fully known, you can compute the exact value of any policy by solving a linear system, and the exact ε-soft optimum by policy iteration. That gives you the **right answer**, independent of anything the learners believe.

With ground truth in hand, both claims fell.

**Claim 1 is false.** Decaying ε doesn't move SARSA to the 13-step path. It stays at −17, and slowing the decay across 20,000 episodes doesn't change it. The reason is the good part: once ε is small, the agent stops visiting the cliff edge at all — so the pessimistic values it learned there are never revised. **It cannot un-learn a fear it no longer tests.**

That's not a quirk of my implementation. Aggressive ε decay quietly violates the premise the convergence theorem rests on — visit every state-action pair infinitely often. Break the premise and you don't get a slower convergence, you get convergence to something else.

**Claim 2 is false in a more embarrassing way.** SARSA only takes the top row when α = 0.5, which happens to be the learning rate the classic figure uses. The exact ε-soft optimum at ε = 0.1 — the genuinely best thing an agent exploring 10% of the time can do — is the **middle** row, 15 steps. When I dropped α to 0.02, SARSA landed on it exactly.

So part of the famous picture is a **learning-rate artifact**. With a constant α = 0.5, a single −100 destroys half of a Q-value in one update, and with no decay the scar never fully heals. The over-caution you see isn't purely the on-policy effect — it's on-policy caution amplified by a learning rate too coarse to average anything.

The on-policy effect is real. It's just smaller than the picture implies: 15 steps rather than 13, not 17.

---

## 4. The generalization that replaced my wrong mental model

I had been carrying "SARSA is the safe one, Q-learning is the greedy one" as if they were two personalities. That's not what's happening.

How far SARSA backs off the cliff is a **continuous function of how recklessly it explores**:

| exploration rate | SARSA's route |
|---|---|
| ε ≥ 0.2 | top row — 17 steps |
| ε ≤ 0.1 | middle row — 15 steps |
| ε → 0 | the cliff edge — 13 steps, same as Q-learning |

SARSA isn't cautious. SARSA is *accurate* — it correctly values a policy that includes its own randomness, and the caution is the honest consequence. Turn the randomness off and the caution disappears with it, because there was never anything to be cautious about.

That reframing is the thing I actually took away. The two algorithms aren't answering the same question differently. They're answering **different questions**: Q-learning asks "how good is the optimal policy?", SARSA asks "how good is the policy I am actually running?" Both answers are correct. They differ because the questions differ, and they converge when the exploration that separates the questions goes to zero.

---

## 5. FrozenLake, and what "slippery" does

FrozenLake is a 4×4 grid with holes; reach the goal for +1, everything else 0. In deterministic mode both algorithms solve it in exactly 6 steps, which is optimal.

Turn on `is_slippery` and the intended action only happens a third of the time — the other two thirds you slide perpendicular. My learners reached about **71%** success against a computed ceiling of about **74%**.

That ceiling is the point. Without the exact solver I'd have looked at 71% and had no idea whether my implementation was broken, my hyperparameters were bad, or the environment is simply that hostile. It's the third. The optimal policy on slippery FrozenLake *still fails a quarter of the time*, because you can be pushed into a hole while doing everything right.

Being able to say "71 against a ceiling of 74" instead of "71" is the difference between a number and a result. Writing the DP solver took an hour and it's the piece of that project I'd keep if I could keep only one.

---

## 6. Four silent bugs, none of which crash

Everything below runs cleanly, produces plausible numbers, and is wrong. These cost me more time than the algorithms did.

**`terminated` vs `truncated`.** Gymnasium's `step()` returns both. `terminated` means the episode genuinely ended (goal reached, fell in a hole). `truncated` means the time limit cut it off. Treating truncation as termination teaches the agent that the world *ends* at the time limit, so it stops valuing anything beyond it — it learns to be exactly as short-sighted as your episode cap. The value of a truncated final state should be bootstrapped, not zeroed.

**`np.argmax` on an all-zeros table.** At initialization every Q-value is 0, and `argmax` on ties returns the *first* index — always. So an untrained agent isn't acting randomly, it's marching in one fixed direction. The exploration you think you're getting from ε-greedy is diluted by a systematically biased greedy branch. Break ties randomly.

**FrozenLake and CliffWalking use different action index orderings.** Reuse your rendering or policy-printing code between them and you get an arrow map that is confidently, silently mislabelled. Nothing errors. You just spend an hour reading a picture that means something else.

**`CliffWalking-v0` is deprecated** in Gymnasium 1.3 — it's `-v1` now. Most tutorials still say v0. Worth knowing before you conclude your install is broken.

The general shape here is worth naming: in RL, a bug doesn't usually crash. It produces a learning curve. A wrong learning curve looks exactly like a right one, and the only defence is an independently computed answer to check against.

---

## 7. What I'd tell someone starting this

Implement both algorithms in the same file so the one differing line is visible on one screen. Then, before you tune anything, write the exact solver — the boring dynamic-programming one that nobody's tutorial includes, because it doesn't scale and isn't impressive.

It doesn't need to scale. It needs to be right, on a grid small enough that "right" is computable. Everything interesting I found came from having a number to disagree with.
