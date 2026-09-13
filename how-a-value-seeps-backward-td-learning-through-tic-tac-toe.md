# How a Value Seeps Backward — TD Learning Through Sutton & Barto's Tic-Tac-Toe

**Context:** I was reading *Reinforcement Learning: An Introduction* and got stuck on §1.5 — the tic-tac-toe example in the first chapter. It's four pages, it's the book's opening demonstration, and I couldn't get it to click. The thing that eventually unlocked it wasn't a better explanation. It was simulating seven games by hand and watching how few numbers actually changed.

---

## 1. The one sentence the section exists to deliver

Keep one number per board position — your current guess at "probability I win from here" — pick moves that lead to the highest number, and after each move, **nudge the earlier number toward the later one**.

That's the whole thing. Everything else on those pages is either contrast (why not minimax, DP, or evolutionary search) or foreshadowing (backgammon, neural nets, model-free learning). Realizing that the section is a *trailer* rather than a lecture was itself half the unsticking — I'd been trying to fully absorb material the book rebuilds properly five chapters later.

---

## 2. What V(s) actually is

A lookup table. One row per board position. `V(s)` = your current estimate of P(you eventually win | you're at `s`).

It is **not** a truth about tic-tac-toe. It's a truth about *you playing this specific imperfect opponent*. Change the opponent and the whole table is wrong.

Initialized:

| board type | seeded value |
|---|---|
| you've already won | `1` |
| you've lost **or drawn** | `0` |
| everything else | `0.5` |

Two details worth pausing on. Draws are seeded as `0` — as bad as losses. That's a deliberate choice by the authors, not a fact about the game; they're building an agent that plays to win against a beatable opponent. And the `0.5` is a **shrug, not a claim** — it's "I have no idea," and it matters that it's a number you can move rather than a special "unknown" marker.

---

## 3. The update — and the part worth doing by hand

$$V(S_t) \leftarrow V(S_t) + \alpha\left[V(S_{t+1}) - V(S_t)\right]$$

Read it as: *"my old guess was off by this much from my next guess; move a fraction α of the way toward the next guess."*

That bracket is the **temporal-difference error** — the disagreement between two consecutive estimates made by the same agent. Not between a guess and the truth. Between a guess and a slightly later guess.

That is the strange and load-bearing idea. The agent has no access to truth on most steps. It learns by insisting that its own estimates be *consistent with each other over time*.

Now simulate it. α = 0.1, everything starts at 0.5:

**Game 1.** You wander (all values are tied at 0.5, so every move looks equally good) and you win. The final board is terminal with value 1. Its immediate predecessor updates:

```
0.5 + 0.1 × (1 − 0.5) = 0.55
```

Every *other* state you passed through that game:

```
0.5 + 0.1 × (0.5 − 0.5) = 0.5
```

**Nothing moved.** One state in the entire game learned anything.

That was the moment the section clicked. I had assumed a win propagates credit back through the whole game. It doesn't — because when consecutive estimates already agree, the bracket is zero and *no learning occurs*, regardless of how good or bad the position actually was.

**Game 2.** You happen to pass through that same state again. Now *its* predecessor gets:

```
0.5 + 0.1 × (0.55 − 0.5) = 0.505
```

The signal has moved one more link back, and much weaker.

Ground truth exists **only at terminal states**. It bleeds up the game tree one link per visit. When I ran this properly, the learning front reached the *first* state of the game only on **game 7**.

That's the picture of bootstrapping. Values are learned from other values, and the only thing anchoring the whole structure to reality is the terminal states where the truth is known by definition. Everything else is estimates leaning on estimates, with truth seeping in slowly from the edges.

Once I had that image, Chapter 6 read like review.

---

## 4. Reading Figure 1.1 correctly

This figure confuses nearly everyone, and the confusion is worth resolving because it's the first place the book makes a real distinction.

The decoder:

- `c c*` and `g g*` mean the move you took **was** the one you thought was best — a greedy move.
- `e*` is a separate hollow node you *didn't* take; you went to `e` instead. That move was exploratory.
- There are **two** red backup arrows: `c → a` and `g → e`. Not three.

The missing third arrow is the entire point. **You skip the backup for the exploratory move.** Why: `e` was reached by a move you believed was *worse*. Whatever happens after it isn't evidence about how good `c` was, so folding it back into `c` would corrupt the estimate with the consequences of a decision you deliberately made against your own judgment.

There's a second thing hiding in that figure that I misread completely at first: the arrows jump *over* the opponent's node. The states being valued are the positions **right after your own move** — not every board position. So `S_t` and `S_{t+1}` are successive *decision points of yours*.

The book names these later — **afterstates**, §6.8 — and the reason is neat: many different opponent replies can lead to the same situation for you, so valuing the position after your move (rather than before) collapses a lot of redundant states into one and learns faster.

---

## 5. Why not the three alternatives

The book contrasts three other approaches in passing. One line each is enough, and the third one is the most interesting.

| approach | why it's rejected |
|---|---|
| **Minimax** | Assumes the opponent plays perfectly, so it avoids positions that lose under perfect play — even against an opponent who never finds the refutation. Leaves free wins on the table. |
| **Dynamic programming** | Would work, but you must *hand it* the opponent's move probabilities in advance. You don't have them. |
| **Evolutionary search** | Grades the whole exam with a single score. |

That last one deserves unpacking, because it names the thing RL is actually for. An evolutionary method plays a policy for many games, gets one number (its win rate), and uses only that to decide whether the policy was good. A value-function method grades *each individual question* — every state gets its own estimate, updated from what happened after it.

Same search space, vastly better **credit assignment**. That phrase now means something concrete to me: it's the difference between "this strategy scored 6/10" and "these three specific moves are what cost you."

---

## 6. Building it, and the thing that surprised me

I wrote the full learner — afterstate table, ε-greedy, the update from §3. It reaches ~85–90% wins against the book's default opponent in **under a second** for 10,000 games, and discovers about **1,600 distinct states**.

Two things from actually running it:

**The opening-move values are less decisive than folklore suggests.** Across several training runs, the best opening square was a corner three times out of four and an edge once — corner-vs-centre is close to a coin flip here. What *is* consistent: the four edges settle clearly lowest (0.69–0.76) while corners and centre lead (0.77–0.86).

And the wobble among the top squares is itself instructive. The agent keeps playing its current favourite, so the alternatives stay under-sampled and their estimates stay stale. That's the exploration problem showing up uninvited in chapter 1, three pages before the book introduces it.

**The agent knows it has won before the game ends.** Fairly often it plays a square it rates **1.000** while the game is still in progress. Look at the board when that happens and it's two corners set up as a double threat — two ways to complete a line, and the opponent can only block one.

Nothing in the code searches ahead. There's no lookahead, no model of the opponent, no tree. The table has simply learned, from thousands of games, that this configuration always ended in a win. That's the "planning and lookahead without a model or an explicit search" line from the chapter — and watching a number turn to 1.000 several moves early is a much better demonstration of it than the sentence was.

---

## 7. A practical note on the book itself

The exercises exist and I couldn't find them, which turned out to be a formatting problem rather than a reading one. Sutton & Barto **don't use end-of-chapter problem sets**. The 145 exercises are dropped inline in the body text, set in italics, ending with a small open □ — no shaded box, no heading, no table-of-contents entry. Scan for a "Problems" section at the end of a chapter and you'll never see one.

Two markers worth knowing, both stated in the preface: a **⇤** means "more advanced, not essential to the basic material" — skippable on a first pass. And **`(programming)`** in an exercise title means implement-and-run. There are exactly nine of those, and they're the ones that build intuition rather than test recall.

The density is uneven in a way that tells you where the book thinks the substance is: Chapter 3 (finite MDPs) has 29 exercises, more than twice most others. Chapters 14–16 have none — they're the psychology, neuroscience, and applications surveys.
