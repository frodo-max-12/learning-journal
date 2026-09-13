# Model distillation — how small models learn from big ones

*Learned on March 26, 2026. I was reading about the DeepSeek controversy and Apple's billion-dollar Gemini deal, and realized I didn't actually understand what "distillation" meant at a technical level. So I dug in.*

---

## The basic idea: a teacher and a student

Distillation is one of those ML concepts that has a perfect everyday analogy. Imagine a master chef who has spent decades learning to cook. Now imagine trying to train a new cook — not by sending them through the same decades of experience, but by having them watch the master chef work and imitate everything they do. The apprentice never reads the same cookbooks, never makes the same mistakes, never spends years experimenting. They just learn to replicate the master's outputs.

That is model distillation. You have a large, powerful AI model (the "teacher") that is very expensive to run — it might have hundreds of billions of parameters and require massive GPU clusters. You then train a smaller, cheaper model (the "student") by feeding it the teacher's outputs. The student learns to mimic the teacher's behavior without needing all the same computational power. The result is a smaller model that performs surprisingly close to the big one, but runs faster and costs a fraction as much to operate.

This is how companies create lightweight versions of their frontier models — the ones that can run on phones, handle simple tasks efficiently, or serve millions of API calls without burning through a data center's worth of electricity.

## Why probability distributions matter more than answers

Here is where distillation gets genuinely clever, and where I had to slow down and think.

When a large trained model processes a prompt, it does not just output a single answer. It produces a **probability distribution** over all possible next tokens. If you ask "What is the capital of France?", the teacher model might internally compute something like:

| Token | Probability |
|-------|------------|
| Paris | 92% |
| Lyon | 3% |
| Marseille | 1% |
| Berlin | 0.1% |
| ... | ... |

The final answer you see is "Paris" — the highest-probability token gets selected. But that full distribution contains far richer information than just the correct answer. The fact that Lyon got 3% tells you something: the model understands Lyon is a major French city, more plausible as a capital than, say, a random village. The fact that Berlin got 0.1% rather than 0% tells you the model knows Berlin is a capital, just not France's.

These full distributions are called **soft labels** or **soft targets**. The alternative — just the correct answer "Paris" with no probability information — is a **hard label**.

In distillation, you train the student to match the teacher's soft probability distributions, not just the hard correct answer. This was the key insight from Geoffrey Hinton's 2015 paper that formalized the technique. The student absorbs not just "what is right" but "what is how-wrong and in what way" — a much denser learning signal.

## Temperature scaling and "dark knowledge"

This is the part that I found most interesting. There is a parameter called **temperature** that controls how spread out the probability distribution is.

At normal (low) temperature, the teacher might be 99% confident in one answer. That gives the student almost nothing to learn beyond the right answer — it is effectively a hard label in disguise. At higher temperature, the distribution softens. Maybe it becomes 60% / 15% / 10% / 5% / ... Now the student can see the structure of the teacher's understanding.

Hinton called this **"dark knowledge"** — the subtle relationships the teacher learned but that are not visible in its top predictions. The teacher "knowing" that a BMW is more similar to an Audi than to a carrot is encoded in those soft probabilities, even though both BMW and Audi are wrong answers to most questions. The student absorbs these structural relationships, learning not just facts but the topology of the concept space.

Think of it this way: if I ask a master chess player to just tell me the best move, I learn one fact. But if I ask them to rank the top five moves and explain how close the decision was, I learn their entire way of evaluating positions.

## The training objective: two losses blended together

The student model is typically trained with a combined loss function — two goals blended together:

1. **Distillation loss**: measures how closely the student's soft output distribution matches the teacher's soft output distribution. This uses something called KL divergence, which quantifies the difference between two probability distributions.

2. **Hard label loss**: measures whether the student actually gets the correct answer right, using standard cross-entropy against the ground truth.

You weight these two objectives with a hyperparameter, usually favoring the distillation loss. The student is simultaneously trying to be correct *and* trying to think like the teacher.

## The DeepSeek controversy: black-box distillation

This is where I had what felt like a genuine insight. I asked: if DeepSeek was distilling from Claude, how did they get the probability distributions? They only had API access — prompts go in, text comes out. No soft labels. No internal probabilities.

The answer is that what DeepSeek reportedly did is fundamentally different from classical Hinton-style distillation. It is sometimes called **imitation learning** or **behavioral cloning**.

Anthropic accused DeepSeek, Moonshot AI, and MiniMax of using roughly 24,000 fake accounts to generate over 16 million exchanges with Claude. They sent in carefully designed prompts, collected Claude's high-quality responses, and built a massive synthetic dataset where Claude was essentially the labeler. Then they fine-tuned their own models on this dataset, treating Claude's responses as ground truth to imitate.

This is a degraded form of distillation. You lose the dark knowledge — those soft probability relationships between tokens. You only see Claude's top-1 choice at each step, not the full ranking. But it still works surprisingly well for three reasons:

**Sheer volume compensates.** Sixteen million exchanges across diverse topics creates enough coverage that the student can infer patterns statistically. If you see thousands of examples of how Claude handles a particular type of reasoning, you can learn the pattern even without soft labels.

**The text itself carries implicit information.** The way Claude structures an argument, the caveats it includes, the vocabulary it chooses — all of this encodes something about the model's understanding, even in hard output form.

**Chain-of-thought extraction is the key move.** DeepSeek reportedly prompted Claude to externalize its reasoning — asking it to show step-by-step thinking. This effectively turns internal knowledge into explicit text, partially recovering the information you would lose by not having soft distributions. You are asking the teacher to explain their thinking out loud rather than just give the answer. It is an elegant workaround.

## The Apple-Gemini deal: authorized distillation

The Apple deal is the legitimate, authorized version of the same technique. Apple's agreement with Google gives it complete access to Gemini within its own data centers. Apple can use that access to create smaller models suited for on-device processing — models that perform like Gemini but require far less power, running directly on an iPhone without needing the cloud.

This is clearer-cut distillation because Apple is explicitly taking Google's existing model and training smaller models from its outputs, with full permission and likely access to deeper internals than just the API.

## Is Gemini Flash a distilled version of Gemini Pro?

I assumed so, but the answer is more nuanced. Google has not publicly confirmed that Flash is distilled from Pro. They describe the 2.5 lineup as a "family of hybrid reasoning models" designed together, with Pro optimized for maximum capability and Flash optimized for speed and cost.

The distinction matters: distillation specifically means training a smaller model on a larger model's outputs. What Google likely does with Flash is more nuanced — it could involve distillation as one technique among many, alongside training a smaller architecture from scratch on the same data, using different model sizes, or pruning.

That said, in the broader AI industry, it is very common for the lighter version of a model family to use some form of distillation from the flagship. The Apple-Gemini situation is clearer because Apple is explicitly taking an existing model and training smaller models from it. With Flash versus Pro, they were more likely developed in parallel.

## Why this matters: the economics of AI access

The reason distillation sits at the center of AI geopolitics right now is that it directly threatens the business model of frontier labs. If you spend billions training a model and someone can replicate most of its capability by querying your API 16 million times — at a cost orders of magnitude lower than your training budget — then your moat is not the model itself but your ability to prevent distillation.

This is why API-only access is a deliberate strategic choice. If you never release model weights, no one can do classical distillation with soft labels. But as DeepSeek showed, black-box behavioral cloning through the API is still effective enough to be threatening. The defense becomes rate limiting, terms of service enforcement, and detecting automated extraction patterns — an arms race between access and protection.

> The core technique is always the same: a smaller model learns from a bigger model. The difference that matters — legally, technically, commercially — is whether you have permission, and how much of the teacher's internal knowledge you can access.

---

*This connects to my broader interest in understanding the AI stack from first principles — not just what these models do, but how they are built, copied, and defended. Next I want to understand fine-tuning and RLHF, which sit upstream of distillation in the training pipeline.*
