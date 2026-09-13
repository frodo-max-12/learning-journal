# How Transformers Work — "Attention Is All You Need" from first principles

*Learned on March 10, 2026. I asked Claude to explain the Transformer paper because I kept hearing it referenced everywhere — "attention mechanism," "context window," "tokens" — and I wanted to actually understand what these words mean. This turned into one of the most illuminating conversations I have had about AI, because it forced me to separate three things I had been conflating: how LLMs read, how they write, and how they learned.*

---

## The paper that changed everything

In 2017, a team at Google published a paper called "Attention Is All You Need" (Vaswani et al.). The title was deliberately cheeky — previous AI language models used attention as one ingredient among many, and this paper said: throw out everything else, attention alone is enough. The architecture they introduced — the **Transformer** — is what powers essentially every large language model today. GPT, Claude, Gemini, Llama — all Transformers.

To understand why this paper mattered, I need to start with what came before it.

## The problem with reading one word at a time

Before Transformers, the dominant architecture for working with language was the **Recurrent Neural Network (RNN)** and its variants like LSTMs. These processed text sequentially — one word (or token) at a time, left to right, like a human reading.

This had two critical problems:

**Speed.** Because you had to process word 1 before word 2, and word 2 before word 3, the computation was inherently sequential. You could not throw more hardware at it to make it proportionally faster. If your sentence had 100 words, you needed 100 sequential steps no matter how many GPUs you had.

**Memory.** By the time the model reached word 100, its "memory" of word 1 had degraded. Information got compressed and diluted as it passed through each sequential step. Long-range dependencies — like understanding that a pronoun in paragraph three refers to a noun in paragraph one — were extremely difficult.

Think of it like a game of telephone. Each step introduces a tiny bit of information loss. Over a long chain, the original signal degrades beyond recognition.

## The core insight: self-attention

The Transformer's key innovation is called **self-attention**. Instead of reading words one at a time, the model looks at *all* the words in a passage simultaneously and figures out which words are most relevant to each other.

Here is a concrete example. Consider the sentence:

> "The cat sat on the mat because it was tired."

What does "it" refer to? A human instantly knows: the cat, not the mat. But for a computer, this requires understanding the relationships between words that are far apart in the sentence. Self-attention solves this by letting every word "look at" every other word and compute a relevance score. The word "it" would attend strongly to "cat" (high relevance score) and weakly to "mat" (low relevance score). The word "tired" would also attend to "cat" because tiredness is a property of animals, not mats.

The mathematical mechanism works like this — I will keep it conceptual rather than getting into the linear algebra. For each word, the model computes three things:

- A **Query**: "What am I looking for?"
- A **Key**: "What do I contain?"
- A **Value**: "What information do I carry?"

Every word's Query gets compared against every other word's Key to produce attention scores. Those scores determine how much of each word's Value gets incorporated. It is like each word asking every other word "are you relevant to me?" and getting a weighted answer.

The paper's title — "Attention Is All You Need" — was the claim that this mechanism alone, without the sequential processing of RNNs, is sufficient to build a powerful language model. And it turned out to be right.

## The analogy that made it click

The explanation that made this tangible for me was this: the old approach (RNNs) was like a person reading a book one word at a time while trying to hold everything in short-term memory. By the time you reach page 50, you have a vague sense of what happened on page 1, but the details are gone.

The Transformer approach is like having the entire book spread out on a huge table, where you can glance at any part at any time and draw connections between distant sections instantly. Every word has simultaneous access to every other word. There is no degradation over distance.

This is why Transformers scaled. Two wins at once: parallel processing (everything happens simultaneously, so you can use more hardware) and better quality (no information degradation over distance).

## The three phases: reading, writing, and training

This is where my understanding deepened significantly. I had been confusing three very different things, and separating them clarified the entire architecture.

### Phase 1: Reading your input (parallel)

When you send a message to an LLM, the model takes in your entire prompt at once. All of it, simultaneously. Every token in your input gets to "look at" every other token in parallel through the attention mechanism. If you paste in a 3,000-word essay and ask a question, the model is not reading it word by word. It processes the whole thing in one forward pass, building up a rich representation of how all the parts relate to each other.

This is the phase where the Transformer's advantage is most obvious. Parallel processing, no information loss, every word connected to every other word.

### Phase 2: Generating the response (sequential)

This is the part that *is* one token at a time, and it *has to be*. When the model writes its reply, it generates the first token, then uses that plus your input to generate the second token, then uses all of that to generate the third, and so on. Each token is chosen based on everything that came before it.

This is fundamentally sequential because each word the model chooses affects what the next word should be. You cannot write the end of a sentence before deciding the beginning. The whole point is that each token is *conditioned* on all previous tokens.

> There is a deep asymmetry: reading is parallel, writing is serial. The model absorbs your entire message in one gulp, but crafts its response one word at a time.

This asymmetry is why generation is slower than you might expect. The model has to do a full computation for every single token it outputs. For a 1,000-token response, that is 1,000 sequential steps. This is one of the active areas of research — people are working on "speculative decoding" and other techniques to make generation faster.

### Phase 3: Training (cleverly parallel)

Training is the most elegant of the three. During training, the model is shown massive amounts of existing text and asked to predict each next word. Because the training text already exists in full, the model can compute predictions for every position simultaneously.

It works like this: at position 1, predict word 2. At positions 1-2, predict word 3. At positions 1-3, predict word 4. All of these predictions happen in parallel, using something called a **causal mask** that ensures each prediction can only see the words before it — no cheating by looking ahead.

```
Position:  [The] [cat] [sat] [on] [the] [mat]
Predicts:   cat   sat   on   the   mat   .

Each prediction only sees words to its left (enforced by causal mask).
All predictions computed simultaneously.
```

This parallelism is what made training practical. If training had to be done one token at a time — generate a prediction, check it, update, move to the next position — building models with trillions of tokens of training data would have taken impossibly long. The causal mask trick lets you get the benefits of sequential dependence (each prediction only sees past context) with the speed of parallel computation.

| Phase | How It Works | Speed |
|---|---|---|
| Reading input | All tokens processed simultaneously | Fast (parallel) |
| Generating output | One token at a time, each conditioned on previous | Slow (sequential) |
| Training | All positions predicted simultaneously with causal mask | Fast (parallel) |

## The context window and "lost in the middle"

Once I understood the attention mechanism, I had a follow-up question that seemed like a gotcha: if the model reads everything at once, why do people say you should not put too much into the context window? Why do they recommend putting your key question at the beginning and end, not buried in the middle? If everything is processed in parallel, how can the model "miss" something?

The answer is nuanced, and the common folk explanation is wrong. The model does not "forget" or "run out of memory" the way people imply. The entire context is mathematically available at every step. But two real effects create practical limitations:

**The "lost in the middle" phenomenon.** Researchers have empirically demonstrated that language models attend more strongly to tokens near the beginning and end of the context, and are measurably worse at using information buried in the middle. This is not a hard limitation — the model *can* see the middle. It is a statistical bias that developed during training because the training data naturally had the most relevant information at prominent positions. The model learned to weight the edges more heavily.

Think of it less like forgetting and more like a tendency to skim. The information is on the table, but the model's eye is drawn to the top and bottom of the page.

**Signal-to-noise degradation.** Attention is a soft weighting system — the model has to decide what is relevant among everything it sees. The more material you put in the context, the harder that discrimination task becomes. Irrelevant context pulls attention away from what matters. It is like trying to hear a specific conversation in a quiet room versus a crowded party. You can technically hear everything, but more noise makes it harder to focus on the right signal.

> People say "do not overload the context window" and they are right — but not because the model forgets. It is because more input means more noise for the attention mechanism to filter through, and because of a trained statistical bias toward the edges of the context.

This is why practical prompt engineering advice works: putting important instructions at the beginning and end of your prompt, keeping context relevant and concise, repeating key constraints. You are not compensating for a memory limitation. You are working with the statistical tendencies of the attention mechanism.

## Why this matters for someone learning AI

Understanding the Transformer architecture is not optional for anyone who wants to work with AI seriously. Not because you need to implement one from scratch, but because so many practical decisions — prompt design, context management, cost optimization, choosing between models — flow from understanding how the underlying system works.

When I hear "context window," I now know it means the total number of tokens the model can attend to simultaneously. When I hear "tokens per second," I understand that is constrained by the sequential nature of generation. When someone says "put your instructions at the top of the prompt," I understand the empirical basis for that advice.

The most important thing I took away is the asymmetry. Reading is parallel, writing is sequential, training is cleverly made parallel. This asymmetry shapes everything — cost (generation is expensive because it is sequential), speed (input processing is fast), and the fundamental research frontier (making generation faster is a major open problem).

The paper was titled "Attention Is All You Need," and it turned out to be true. The attention mechanism — letting every part of the input communicate with every other part simultaneously — was the breakthrough that unlocked everything that followed. Every major language model since 2017 is, at its core, a scaled-up version of this idea.

---

*What I studied next: I wanted to understand the training process more deeply — what backpropagation actually does, how loss functions work, and why scaling up Transformers keeps making them better. Notes on that are in [how-neural-networks-learn.md](how-neural-networks-learn.md).*
