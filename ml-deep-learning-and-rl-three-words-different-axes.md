# ML, Deep Learning, and RL — Three Words That Cut Along Different Axes

**Context:** I'd been using machine learning, deep learning, and reinforcement learning as though they were three items on one list, and could never quite say how they related. They aren't siblings. **The three words classify along completely different axes**, and once I saw which axis each one is on, a lot of otherwise-confusing phrases — "deep reinforcement learning" chief among them — became obvious. Then I asked the follow-up that turned out to matter more: is machine learning even possible without neural networks?

---

## 1. The three words, and what each is actually classifying

**Machine learning is the umbrella.** Algorithms that learn patterns from data instead of being explicitly programmed. Linear regression, decision trees, support vector machines, neural networks — all of it.

**Deep learning is a *method* within ML.** Neural networks with many layers. And the distinction that matters isn't depth for its own sake, it's **how features are obtained**: classical ML usually needs you to hand-engineer the features; deep learning learns its own representations from raw input. You pay for that in data and compute.

**Reinforcement learning is a *problem setup* within ML** — parallel to supervised and unsupervised learning, not parallel to deep learning. An agent takes actions in an environment and learns from a reward signal rather than from labelled examples.

So:

| word | what kind of thing it names |
|---|---|
| machine learning | the field |
| deep learning | a **method** — how you represent the function |
| reinforcement learning | a **problem setup** — what kind of feedback you get |

**The axes are orthogonal, which is exactly why "deep reinforcement learning" exists as a phrase.** RL is *what* you're learning; deep networks are *how* you represent the policy or value function. Game-playing agents and preference-trained language models both sit in that intersection.

That single observation resolved the confusion. I'd been trying to order three things on one line, and two of them are on different lines.

---

## 2. The problem-setup axis, properly

The other half of the picture is the three problem setups, which *are* genuine siblings:

| setup | learns from | example |
|---|---|---|
| supervised | labelled examples | a spam classifier |
| unsupervised | unlabelled structure | grouping customers |
| reinforcement | reward from its own actions | a robot learning to walk |

And **deep learning can implement any of the three.** That's what makes it a method rather than a category — it's an answer to "how do I represent this function," and the question is asked in all three settings.

What defines RL against the other two is not the algorithm but **two structural difficulties**: feedback is delayed (which move lost the game?), and the agent's own actions determine what data it subsequently sees. Neither of those appears in supervised learning, where the data is fixed and the label is immediate.

Those two properties are the entire source of RL's difficulty, and they're properties of the *situation*, not of any method you bring to it.

---

## 3. Machine learning without neural networks

My follow-up: is classical ML — no neurons anywhere — still a real thing?

**Yes, and for a long stretch it was the default.** Neural networks only became dominant around 2012.

Classical ML covers a lot of ground with no neural networks involved:

- **linear and logistic regression** — fit coefficients directly
- **decision trees**, and ensembles of them: **random forests**, **gradient boosting**
- **support vector machines** — find the maximum-margin boundary, with a kernel trick for non-linearity
- **k-nearest neighbours** — no training at all, just look up similar points
- **naive Bayes** — probabilistic; powered spam filters for years
- **k-means and PCA** — unsupervised clustering and dimensionality reduction

---

## 4. And they aren't legacy — they win in a specific regime

This is the part that changed my picture.

**On tabular data — spreadsheets, transaction logs, records, most business problems — gradient-boosted trees still usually beat neural networks**, train in seconds rather than hours, and run on a laptop. Competitions on tabular data are still largely won by boosted-tree methods.

The split is roughly about **structure in the input**:

- **Neural networks win where the raw input has spatial or sequential structure worth learning representations from** — images, audio, text. There's something to discover in the raw pixels or tokens, and learning the representation is most of the value.
- **Classical methods win where the features are already meaningful columns**, where data is limited, or where you have to explain the model to someone who can reject it.

Which reframes the choice. It isn't old versus new, or simple versus powerful. It's **"does my input have latent structure that's worth learning, or are my columns already the features?"** If someone already did the representation work — by designing the schema — a method that learns representations is solving a problem you don't have.

---

## 5. The feature-engineering trade

The cost of classical ML is that **you decide what the model sees**: day of week, ratio of X to Y, days since last event. That's real work.

But it's also **where domain knowledge enters, and why the result is interpretable.** If a boosted tree says a feature matters, that feature is something a person named and understands. A learned representation is more powerful and mute — it can't tell you what it found in terms you already have words for.

So the trade is: hand-build the features and get interpretability, or learn them and get performance on inputs where nobody could have hand-built them. And "explain this to a regulator" is a genuine requirement in enough domains that interpretability is a feature rather than a consolation.

---

## 6. What I took away

**Check which axis a word is on before comparing it to another word.** My whole confusion came from lining up a field, a method, and a problem setup as if they were alternatives. Names in a technical field are often classifying along different dimensions, and the confusion is in the list, not in the concepts.

**"Deep RL" is a compound because the two words are independent choices.** Once you know one is *what you're learning* and the other is *how you represent it*, the compound is the only sensible name for the combination.

**Neural networks are the answer to a specific question — do my inputs need their representation learned?** Most business data arrives as columns someone already designed, which is precisely the case where the answer is no. That's a much better decision rule than "use the most advanced thing," and it points at the older methods far more often than I'd assumed.
