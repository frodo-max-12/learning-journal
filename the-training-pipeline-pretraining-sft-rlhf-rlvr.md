# Pretraining, SFT, RLHF, RLVR — the Four Stages, and the Cliff They Leave Behind

**Context:** I kept seeing "pre-training", "training", "fine-tuning" and "RL" used as if everyone knew which was which, and I didn't. So I asked for the actual distinctions. What made it stick was a second question I'd been carrying separately — I'd seen a claim that coding agents perform brilliantly inside their "RL-maxed regions" and badly outside them. Checking whether that premise was even true turned out to be the best way to understand what each training stage actually deposits in a model.

---

## 1. The pipeline is sequential — each stage consumes the last

The key structural fact, which none of the casual usage conveys: these are **stages executed in order**, each taking the previous stage's model as input.

### Pretraining

**Objective:** predict the next token, across an enormous corpus.

- **Data:** on the order of 15–30 trillion tokens — web text, books, code, papers, forums — heavily filtered and deduplicated.
- **Compute:** where the bulk of the money goes. Tens to hundreds of millions of dollars for a frontier run, thousands of GPUs for weeks to months.
- **Output:** a **base model**. It "knows" an enormous amount but isn't useful as an assistant — ask it "What is RL?" and it may continue with "What is supervised learning? What is…" because it's predicting plausible next text, not answering.
- **What it deposits:** latent world knowledge, fluency, code syntax, mathematical patterns.

The consequence that matters most: **you cannot fine-tune in knowledge that wasn't pretrained in.** Everything downstream sharpens what's already latent. That single sentence explains most of what follows.

### "Training"

Usually means the whole pipeline; sometimes specifically pretraining. It's not a distinct technical stage, which is exactly why the word confused me.

Worth knowing that labs also do **mid-training** — continued pretraining on a smaller, higher-quality, reasoning-heavy corpus before fine-tuning. The boundaries here are genuinely blurry, not just under-explained.

### Supervised fine-tuning (SFT)

**Objective:** the *same* next-token prediction — just on curated (prompt, ideal response) pairs.

- **Data:** hundreds of thousands to a few million examples. "Here's an instruction, here's the ideal response."
- **Compute:** three to four orders of magnitude smaller than pretraining. Hours to days.
- **What it deposits:** format, behaviour, tone — *how to respond*. It adds little new knowledge.

The compression that made it click: **pretraining decides what the model knows; SFT decides what shape it answers in.**

### Reinforcement learning

**Objective:** the model *generates* responses and receives a scalar reward. Weights update to make high-reward outputs more likely. This is the first stage that isn't imitation.

Two flavours, and the distinction between them matters more than the acronyms suggest:

**RLHF — from human feedback.** Humans rank pairs of outputs ("A is better than B"), you train a reward model on those preferences, then optimize the model against the reward model. Used for helpfulness, tone, harmlessness — the things with no programmatic definition.

**RLVR — from verifiable rewards.** For domains with a *programmatic* correctness check: does the math answer match, do the unit tests pass, does the proof check. **No reward model — the environment itself is the reward.** Much cleaner signal, and this is what drove the reasoning-model leap.

- **Compute:** highly variable. For reasoning-heavy models, RL can rival pretraining cost.
- **What it deposits:** optimization toward *measurable* quality — reasoning, tool use, long-horizon agentic behaviour. Things SFT struggles with precisely because there's no canonical ideal trajectory to imitate.

| stage | objective | data scale | what it adds |
|---|---|---|---|
| pretraining | next-token on raw text | 15–30T tokens | world knowledge, fluency |
| SFT | next-token on curated pairs | 10⁵–10⁷ examples | format, instruction-following |
| RLHF | maximize a learned preference score | preference pairs | tone, helpfulness, "vibes" |
| RLVR | maximize a programmatic check | task environments | reasoning, tool use, correctness |

---

## 2. The cliff — is the "RL-maxed regions" claim true?

The claim I'd seen: coding agents are excellent inside the distribution their RL environments cover, and fall off sharply outside it.

**The core claim is right, and the cliff is visible in benchmark numbers.**

Strong regions: Python (data and web), TypeScript/JavaScript, standard software patterns (CRUD, REST, front-end components, CLI tools), shell, SQL — anything with a clean test suite.

Weak regions: borrow-checker edge cases in Rust, C++ template metaprogramming, legacy languages, kernel and driver code, hardware description languages, custom internal DSLs, performance work at the SIMD/cache/branch-prediction level, formal verification, hard-real-time systems, and numerically delicate code.

The gap in the numbers is stark — Python bug-fixing benchmarks sit in the 65–75% range and Python algorithm benchmarks are effectively saturated above 90%, while hard-tier performance-engineering tasks sit under 20%. Part of the signal is the *absence* of canonical benchmarks for systems languages, partly because building them is hard.

But two refinements change what you do about it:

**It isn't purely RL.** Pretraining-distribution coverage does most of the heavy lifting; RL sharpens what's already latent. So "RL-maxed" conflates two things — pretrain coverage *and* RL environment coverage. A language with a rich public corpus but no RL environments still performs decently, because the base model has seen a lot of it. This is the "you can't fine-tune in what wasn't pretrained in" rule showing up as an observable effect.

**In-context learning blunts the cliff.** Put a good README, an examples folder, and a few representative files into context and the agent recovers a surprising amount of the gap even in a weak language. **The cliff is sharpest when you ask cold.**

And the shape is moving. The set of public coding RL environments has grown by roughly an order of magnitude in two years, and the weak list from a couple of years ago already looks different. The cliff is a snapshot of where environments have been built, not a statement about what's possible.

---

## 3. Why the cliff is the best explanation of the pipeline

This is the part I actually took away. The four stages aren't just a sequence of costs — they're four different *kinds of deposit*, and you can see each one by finding where it runs out:

- Ask about something absent from the pretraining corpus and you get confident nonsense — a **knowledge** failure, and no amount of downstream training fixes it.
- Ask a base model a question and get a plausible continuation rather than an answer — an **SFT** failure. Format, not knowledge.
- Get a technically correct answer delivered uselessly — an **RLHF** failure.
- Get code that looks right, reads well, and doesn't pass the tests, in a domain with no test-based training environment — an **RLVR** failure.

That last one is the interesting failure mode, because it's the one you're most likely to mistake for competence. RLVR is what converts "produces plausible code" into "produces code that runs," and in a domain where nobody built the verifier, you're getting the SFT-quality output with the RLVR-era confidence.

Which is a practical rule, not just a taxonomy: **when working outside the well-covered regions, supply the verification yourself.** The tests, the tight context, the fast feedback loop — you're standing in for the training stage that wasn't run for your domain.

---

## 4. Small thing that clarified a lot

I'd assumed the acronyms named competing techniques and that the field would eventually settle on one. They don't compete — they're solving problems that appear at different points, and the reason there are two RL flavours is simply **whether a programmatic checker exists**.

Where a checker exists, use it: the signal is exact and cheap. Where one can't exist — "was this helpful?", "is this the right tone?" — you have to learn a proxy for human judgement and optimize against the proxy, with all the risk of optimizing against a proxy.

The whole industry's push toward verifiable domains reads differently once you see that. It's not that math and code are considered more important. It's that they're the domains where the reward is *real* rather than modelled.
