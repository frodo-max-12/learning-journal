# RAG vs Long Context — The Economics of Retrieval

*Frontier LLMs now ship with million-token context windows — enough room for several entire books in a single prompt. That raises an obvious challenge to [the retrieval system I built](building-a-local-notebooklm-semantic-search-from-scratch.md): why bother with chunks, embeddings, and top-10 search at all? Why not just load the whole library into the context window and ask? I worked through the counterfactual properly — token math, current API pricing, caching mechanics — and the answer turned out to be one of the cleanest cost-architecture lessons I've hit so far.*

---

## The two architectures

My system is RAG — retrieval-augmented generation. A tiny local embedding model finds the 10 most relevant passages out of thousands, and only those ~3,000 words enter the LLM's context to be quoted and cited. The retrieval step costs nothing and runs on my laptop.

The long-context alternative deletes the retrieval layer entirely: put *all* the books in the prompt, every time, and let the model's attention find what matters. No chunking, no embeddings, no possibility of retrieving the wrong passages. It's the architecture the million-token window seems to invite.

## First problem: it doesn't even fit

My corpus is ~950k unique words across the seven David Burns books I'd indexed. English runs ~1.3 tokens per word, so that's **1.2–1.3 million tokens** — over the 1M limit. The request would simply be rejected; I'd have to drop roughly two books per question. The "just load everything" architecture starts by not being able to load everything. (And this is a modest corpus — seven books. A real document base blows past a million tokens immediately.)

## Second problem: the per-question price

Frontier-model input pricing at the top tier runs **$5–10 per million tokens**. Loading ~1M tokens of books per question:

| | Per question |
|---|---|
| Uncached long-context question | ~$5–10 |
| First question with prompt caching (write premium ~1.25×) | ~$6–12 |
| Follow-up within the cache window (reads ~0.1×) | ~$0.50–1 |
| My retrieval pipeline | $0 |

Prompt caching is the standard mitigation — providers let you cache a stable prompt prefix so repeat requests reprocess it at ~10% of the price. But the default cache lifetime is measured in *minutes* (longer TTLs cost a higher write premium). That fits a burst of questions in one sitting; it does not fit my actual usage pattern, which is one question every few days. For me, nearly every question would pay the full write price.

The output side barely matters — answers are a few thousand tokens — the cost is overwhelmingly the *input*: re-reading the library on every question.

> The punchline that made the economics click: **building my entire knowledge base — parsing, chunking, and embedding all seven books — cost less than asking a single long-context question would.** All the expensive work in RAG happens once, at index time. The long-context design pays for the whole corpus on every query, forever.

There's a latency mirror of the same asymmetry: time-to-first-token on ~1M uncached input tokens is measured in minutes; my pipeline answers in ~3 seconds, nearly all of which is loading the local embedding model.

## What long context would genuinely buy

This isn't one-sided, and the honest version of the comparison is more interesting than "RAG wins."

Retrieval has a structural blind spot: **whole-corpus questions**. "How did Burns' treatment of perfectionism evolve between *Feeling Good* (1980) and *Feeling Great* (2020)?" is a question my system handles badly — the answer isn't in any 10 chunks; it's in the *relationship between hundreds of them*. Top-k retrieval can only ever see k passages. A long-context model sees everything at once and can synthesize, compare, and trace themes across the entire corpus. It also has no retrieval-miss failure mode — my system fails precisely when the right passage doesn't crack the top 10.

## What it would break

My system's design contract is **verbatim quoting with citations** — return the author's exact words, tagged with book and chapter. Hand a model exactly 10 passages and faithfulness is trivially checkable: the quote either matches a passage or it doesn't.

With a million tokens in context, the model quotes from its *attention over the haystack*. Mostly accurate — but paraphrase drift and chapter misattribution become live risks, and verifying a quote means searching the books again anyway. There's also an empirical effect I'd written about in [my transformers entry](how-transformers-work-attention-is-all-you-need.md): attention over very long contexts measurably softens in the middle ("lost in the middle"). My retrieval's `argsort` is *exact* about ranking; attention is not.

So the failure modes don't disappear — they swap:

| | RAG | Long context |
|---|---|---|
| Fails by | missing the right passage (not in top-k) | mis-weighting or misquoting it (attention dilution, paraphrase drift) |
| Citations | trivially verifiable | hard to verify |
| Cross-corpus synthesis | structurally weak | the headline strength |
| Cost per question | ~$0 | dollars |

## Where this leaves the architecture

For my use case — recurring, personal, verbatim-by-design — retrieval is the right call and the economics aren't close. But the conclusion isn't "RAG always wins"; it's that the two designs serve different question shapes, and nothing forces a choice. The pattern I've landed on: retrieval as the default path, and the occasional deliberate "deep-dive mode" — load five books into a long-context model and ask the big thematic question — treated as what it is: a few dollars of compute spent knowingly, not a default architecture.

The transferable lesson is about *where work happens*. Every system that answers questions over a corpus has to pay the cost of reading that corpus at some point. RAG pays it once, at index time, in a form that compounds (the index serves every future question). Long context pays it on every single request. Whenever I evaluate an architecture now, I ask: which costs are one-time and which are per-request — and is anything per-request that could be made one-time?
