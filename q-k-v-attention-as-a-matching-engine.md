# Q, K, V — Attention as a Matching Engine

**Context:** I understood the transformer paper at a high level and wanted to understand it the way I actually learn things — by building it. What made the whole architecture click wasn't a better explanation of self-attention. It was noticing that the query/key/value structure **is a matching engine**, and that if you have a domain where matching one set of things against another *is* the problem, you can apply attention to it directly and watch every part of the mechanism do visible work.

---

## 1. The reframe: Q, K, V is retrieval

The three letters are usually introduced as an implementation detail — three learned projections of the input. Read them as what they're named after and the whole thing becomes intuitive:

> **A query attends over keys and pulls back their values.**

That's a lookup. It's the shape of a dictionary, a database index, a search engine. The difference is what makes attention interesting:

| | exact lookup | attention |
|---|---|---|
| matching | the key matches or it doesn't | every key gets a **similarity score** |
| result | one value | a **weighted blend of all values** |
| the weights | implicit, binary | `softmax` over the scores |

**Softmax is doing soft matching and ranking.** It converts raw similarity scores into weights that sum to one — so a strongly matching key dominates, weaker ones contribute a little, and irrelevant ones contribute nearly nothing. It's a *differentiable* version of "pick the best match," which is exactly what makes it trainable. A hard argmax has no useful gradient; a softmax does.

Once I had that, the equation stopped being notation. `Attention(Q, K, V)` says: score every key against the query, normalize the scores into weights, return the weighted sum of values.

---

## 2. Why the scaling factor exists

The scaled dot-product attention formula divides the scores by the square root of the key dimension before the softmax, and I'd been treating that as arbitrary.

It isn't. Dot products of high-dimensional vectors grow with dimension, so without scaling the scores get large, and **softmax of large numbers saturates** — one weight goes to ~1, the rest to ~0, and the gradient nearly vanishes. Dividing keeps the scores in the range where softmax stays soft and gradients keep flowing.

So the scaling factor is there to keep the *soft* in soft matching. That's a nice example of the pattern I keep finding in equations: every symbol is solving a specific problem, and this one is solving "the mechanism stops learning if you don't."

---

## 3. Applying it to something that isn't language

The bit that made this concrete for me: **if your domain is matching, attention maps onto it directly.**

Take any setting where you have a stream of requests on one side and a pool of available options on the other, and the job is to pair them:

- the **query** is what's being asked for,
- the **keys** are the available options,
- the **values** are those options' details and terms,
- the **softmax** is the soft match-and-rank.

That's not an analogy stretched over a machine-learning technique. It's the same computation. Which means you can implement *scaled dot-product attention on its own*, with no transformer around it, and it does a genuinely useful job — soft matching that learns what similarity means from data rather than from a hand-written rule.

That was the moment "attention is all you need" stopped being a slogan for me. If matching is what you're doing, the mechanism is the task.

---

## 4. Four shapes, and which part of the architecture each uses

The other thing building it taught me is that the famous architecture diagram is not one model. It's a **menu**, and the well-known variants are different subsets of it:

| shape | what it uses | typical task |
|---|---|---|
| **attention alone** | scaled dot-product attention, nothing else | matching, retrieval, ranking |
| **encoder-only + one output head** | the encoder stack, plus a head producing a single number or label | classification, regression over a sequence |
| **encoder-only + per-token head** | the encoder stack, plus a head producing an output *per position* | tagging, extraction, labelling spans |
| **full encoder–decoder** | everything, including the decoder's **masked** self-attention and **cross**-attention | generating a sequence conditioned on another |

Laying it out this way answered several things I'd wondered about separately.

**Why the decoder's self-attention is masked:** during generation, a position must not attend to positions after it, or it would be using the answer to produce the answer. Masking enforces "you can only look left." The encoder has no such constraint because it sees the whole input at once — which is the same fact as "encoding is parallel, generation is sequential," stated as a property of the attention mask rather than as a mysterious asymmetry.

**What cross-attention is for:** it's the decoder querying the *encoder's* output — the query comes from what's being generated, the keys and values from what's being conditioned on. Same mechanism, two different sources. Which is why it maps so cleanly onto matching: it's literally "given what I want, look over what's available."

**Why encoder-only architectures exist as a family.** If your task is understanding rather than generating, you don't need the half of the diagram that generates.

Building several small heads on one shared core, rather than one model, was what surfaced this — each shape exercises a different region of the diagram, and by the end there was no block I hadn't had to make work.

---

## 5. The honest caveat about scale

Worth recording because it shaped the whole exercise, and because it's the kind of thing that's easy to leave out.

**A few thousand training examples is tiny for training a transformer from scratch.** The original work used millions of sentence pairs. So the right framing is: build the **full architecture faithfully**, and run it at a fraction of the original size — a much smaller model dimension, two layers instead of six.

You get to see every block work, watch the loss drop, and visualize the attention weights. What you do *not* get is a model that beats a simple rule-based baseline on the same data. Those are different claims, and conflating them is how people end up believing a from-scratch model is competitive when it's a teaching rig.

Being explicit about that up front is what made the exercise worth doing. **The goal was to understand every block, and stating that plainly meant I never had to pretend the output was something it wasn't.** The alternative — building it while quietly hoping it would also be useful — is how you end up defending a result you don't believe.

---

## 6. What I took away

**Q, K, V is retrieval with soft weights.** That's the sentence I'd give someone stuck on attention. Not "each word looks at every other word" — that's the *consequence* — but "a query scores every key and pulls back a weighted blend of their values."

**Softmax is what makes matching learnable.** Hard selection has no gradient. The entire mechanism depends on being a differentiable approximation of "pick the best," and the scaling factor exists to keep it from collapsing into hard selection by accident.

**The architecture diagram is a menu, not a model.** Encoder-only, decoder-only, attention-alone, and the full encoder–decoder are subsets chosen to fit a task, and the masking is what distinguishes generating from understanding. Once you see that, the zoo of model families stops being a list to memorize and becomes four choices about what your task needs.
