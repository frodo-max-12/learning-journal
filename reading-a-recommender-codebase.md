# Reading a Recommender Codebase — What a Feed Actually Does Per Request

**Context:** A large social platform open-sourced its recommendation system, and I wanted to actually read it rather than read *about* it. It's four services across two languages, and I'd never navigated a system that size. The two things I got out of it: a repeatable method for reading an unfamiliar large repo, and one architectural bet stated so plainly in the README that it reframes the whole system.

---

## 1. The method that worked

Reading a big repository top to bottom doesn't work — there's no top. What worked was three passes at increasing depth:

**Pass 1 — the README of the root, then the README of every subdirectory, in parallel.** These were written closer to the design intent than the code, and they tell you what the *authors think* the parts are. Where they disagree with the code, that gap is where the interesting questions live.

**Pass 2 — find the entry point and the shared contract.** In this system the load-bearing file was a trait definition describing the pipeline stages every request flows through. One file, and it's the skeleton of everything.

**Pass 3 — sample one file per service** rather than reading any service fully. The orchestration core, the model port, the pipeline entry, the content service. Enough to know what each is *for*.

The general rule I extracted: **read for the shape before reading for the detail**, and find the file that defines the contract every other file implements. In a service architecture that's usually an interface, a trait, or a protocol definition — and it's a much better starting point than `main`.

---

## 2. The bet that defines the system

The README states it outright:

> Every single hand-engineered feature and most heuristics have been eliminated. The transformer does the heavy lifting.

That is the "let the model learn it" wager applied to recommendation. The **previous** generation of this system, open-sourced years earlier, had hundreds of hand-engineered features — author reputation, engagement velocities, social-graph signals, all computed by dedicated pipelines.

This version feeds the model **three things per history entry**: a post ID hash, an author ID hash, and an action vector. No content features. No graph features. The attention layers are expected to work out what matters.

What makes this a genuinely interesting case study is that the trade-off is legible and falsifiable:

- **If the bet works**, the system gets dramatically simpler — no feature store, no feature pipelines, no training/serving skew from features computed differently offline and online. An entire category of infrastructure and an entire category of bug disappear.
- **If it doesn't**, recall on cold and niche content collapses, because hand-engineered features are precisely what carry signal when there's little interaction history to learn from.

It's also the Bitter Lesson as a production decision rather than an essay. The essay says general methods that absorb computation beat hand-encoded domain knowledge. Here's a team deleting a decade of accumulated domain knowledge on that thesis, in a system serving live traffic, where being wrong is measurable.

---

## 3. What a feed request actually does

The pipeline runs eight stages, and seeing them laid out demystified the whole category for me:

1. **Query hydration** — fetch user state in parallel: engagement history, follow graph, muted keywords, an impression filter of things already seen, previously served items, topics.
2. **Sources** — kick off every candidate source in parallel. The two interesting ones are *in-network* (recent posts from people you follow) and *out-of-network* retrieval (embed the user, dot-product against the corpus, take the top K).
3. **Hydrators** — enrich each candidate in parallel: body, author info, engagement counts, safety flags, language, media, relationship scores.
4. **Pre-scoring filters** — drop duplicates, stale items, blocked and muted authors, already-seen.
5. **Scorers** — the model call, then weighted scoring, then diversity attenuation so one author can't dominate.
6. **Selector** — sort by final score, take the top K.
7. **Post-selection filters** — visibility and policy checks, conversation deduplication.
8. **Side effects** — fire-and-forget caching and logging.

The shape underneath is **retrieve → rank → filter**, and once you see it you see it everywhere — search engines, ad systems, retrieval-augmented generation. Cast a wide cheap net, then spend expensive computation only on the survivors.

Two structural details worth noticing:

**What runs in parallel and what runs sequentially is not an optimization detail — it's forced by the data flow.** Sources, hydrators, and side effects fan out concurrently because they're independent. Filters and scorers run sequentially because each operates on the *survivors* of the previous one. You can read the concurrency and infer the dependencies.

**Filtering happens twice, before and after scoring, and the split is economic.** Cheap filters run first to reduce how many candidates reach the expensive model. Expensive checks — policy, visibility, conversation-level deduplication — run last, on the handful that will actually be shown. Same operation, placed on either side of the costly step depending on what it costs to evaluate.

---

## 4. The simplest service taught me the most

The in-network candidate source is a Kafka consumer maintaining an **in-memory store keyed by author**. Given a user's follow list, it looks up recent posts per followed author, sorts by recency, returns the top N.

No ML. No ranking. Sub-millisecond because it's all in RAM.

I'd assumed a system like this would be machine learning throughout. Half of the candidate generation is a hash map and a sort. The sophistication is concentrated in one place — retrieval over the corpus you *don't* follow, and ranking — and everything else is deliberately, aggressively boring.

That's the lesson I'd keep from the whole exercise. **The impressive part of a well-built system is usually small and surrounded by unglamorous machinery that exists to keep the impressive part cheap.**

---

## 5. Two languages, split along a real seam

The system is Rust for serving and orchestration, and Python/JAX for the models, connected by RPC.

The seam isn't arbitrary. The serving path is latency-critical, highly concurrent, and mostly I/O coordination — fan out, wait, merge, filter — which is exactly what a systems language with good async support is for. The model path needs the numerical ecosystem and researcher iteration speed.

Splitting along "what each half is actually good at" and paying an RPC hop between them is a trade I'd have found arbitrary before reading this. It's the same shape as the cost-model conclusion I'd reached elsewhere: put the expensive, specialized thing behind an interface, and make everything around it cheap and predictable.

---

## 6. What I took away

**Find the contract file first.** The pipeline trait was worth more than any other file in the repository — it's the one place where the *shape* of a request is stated once and everything else conforms.

**Read the README for intent, the code for reality, and the gap for insight.** The README told me about the architectural bet. The code told me how much boring infrastructure that bet is embedded in. Neither alone would have been the right picture.

**Ordering in a pipeline is an economic argument.** Which filters run before scoring and which after is a statement about the relative cost of evaluating each check versus running the model. Once I read it that way, the ordering stopped looking like convention and started looking like a decision someone could defend — or get wrong.
