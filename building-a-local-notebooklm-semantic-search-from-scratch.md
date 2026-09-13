# Building a Local NotebookLM — Semantic Search From Scratch

*I wanted a NotebookLM-style tool I could point at a corpus I know deeply: ask a question in plain English, get back the exact passages that answer it, with citations. The corpus I chose was the books of psychologist David Burns — seven of them, anchored by* Feeling Good, *one of the best-selling psychology books ever written — partly because seven books (~1M words) is exactly the scale where search gets interesting, and partly because you can only judge a retrieval system on material you know well enough to spot a bad answer. What I ended up with is two short Python scripts and two data files totalling about 21MB, running entirely on my laptop. Understanding why that's all it takes — no vector database, no server, no cloud API for the search itself — taught me more about how modern ML systems actually work than anything I'd read before.*

---

## The problem keyword search can't solve

Say I search the corpus for help with "I keep procrastinating and then hate myself for it." The most relevant chapter in *Feeling Good* is the one on "do-nothingism" — Burns' name for the lethargy cycle — and it shares almost no words with my query. Keyword search (grep, SQL `LIKE`, even classic full-text search) matches *strings*. I needed something that matches *meaning*.

That one requirement is what the entire architecture exists to serve.

## Meaning as geometry

The core idea — the one everything else hangs on — is the **embedding**. An embedding model is a neural network that maps any piece of text to a point in high-dimensional space (768 dimensions in my case), trained so that texts with similar meaning land near each other. "Meaning" becomes geometry: my procrastination question and the do-nothingism chapter end up as nearby points, even though they share no vocabulary.

Two details make the math almost embarrassingly simple:

1. Every vector is normalized to length 1 at creation time. I verified this on my own index — the norm of row 0 is exactly 1.0.
2. For unit vectors, the dot product of two vectors equals the cosine of the angle between them. Small angle = aligned meanings = dot product near 1.

So "how relevant is passage P to question Q?" reduces to: multiply 768 pairs of numbers and add them up. Everything else in the system is bookkeeping around that one operation.

## The build phase: books → chunks → vectors

The first script runs once and turns books into a searchable index. The pipeline:

**Extract with structure.** EPUBs get parsed along their spine (the book's internal reading order), with `h1`/`h2`/`h3` headings marking chapter boundaries — that's how every chunk later knows which chapter it came from, which is what makes citations possible. One book (*Intimate Connections*) only existed as a PDF, so it goes through a different extractor that maps pages to chapters using the PDF's table of contents, with a regex fallback that reads running headers like "Chapter Title / 12".

**Pick the best source file automatically.** My folder had duplicate copies, summaries, and bad scans of each book. Each candidate file gets scored as `word_count × printable_ratio` — the printable ratio is the fraction of characters that are normal letters and punctuation, so a garbled OCR copy scores near zero and loses. No manual curation.

**Chunk with overlap.** Each chapter is sliced into 260-word pieces, and each window overlaps the previous one by 50 words (so the window slides 210 words per step). Two numbers worth understanding:

- 260 words ≈ 350–400 tokens, safely under the embedding model's 512-token input limit. Anything longer would get silently truncated.
- The overlap exists because a cut might land mid-idea. With overlap, any ~50-word neighbourhood of text appears intact in at least one chunk, so an idea straddling a boundary still gets a fair embedding somewhere. Tail fragments under 30 words get merged into the previous chunk instead of becoming junk rows.

**Embed everything.** All 4,380 chunks (seven books) go through the embedding model in batches, producing one 768-float vector each.

## Two files are the entire database

This was the part that rewired how I think about "infrastructure." The whole index is:

**`chunks.db`** — a plain SQLite file (8.2MB), two tables:

```sql
CREATE TABLE chunks(id INTEGER PRIMARY KEY, book TEXT, chapter TEXT, ord INTEGER, text TEXT);
CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT);
```

This is the human-readable half: the actual passage text plus its provenance (book, chapter, position). The tiny `meta` table holds exactly one row — the name of the embedding model used to build the index. The query script reads the model name from there instead of hardcoding it, because vectors from different models live in incompatible coordinate systems; comparing them produces geometrically meaningless numbers. The one-row table makes that mistake impossible.

**`embeddings.npy`** — numpy's binary format: a small header describing dtype and shape, then the raw bytes of a 4,380 × 768 float32 matrix. You can verify this is literally all the file is, down to the byte:

```
4,380 rows × 768 dims × 4 bytes/float = 13,455,360 bytes
actual file size                      = 13,455,488 bytes
difference                            =       128 bytes  ← the npy header
```

Row *i* of the matrix is the embedding of the chunk whose `id = i` in SQLite. That positional correspondence is the entire "join" between the two files — no foreign key, no index structure, just *same number*.

> Conceptually each chunk is one logical record: `(id, book, chapter, text, vector)`. It's split across two files because each format is best at one half — SQLite is great at text and metadata you want to query and cite, terrible at bulk float math; a numpy matrix is one `np.load()` away from a vectorized matrix multiply, but hopeless at storing text. Together they *are* a vector database, minus everything you don't need at this scale.

## The search engine is one line of linear algebra

The second script runs per question:

```python
V = np.load("embeddings.npy")        # (4380, 768), unit-normalized
qv = model.encode([query])[0]        # embed the question with the SAME model
sims = V @ qv                        # 4,380 dot products in one matrix multiply
top = np.argsort(-sims)[:10]         # best 10 passages
```

`V @ qv` is the magic line. A (4,380 × 768) matrix times a 768-vector gives 4,380 relevance scores — one per chunk across all seven books — in a single shot. That's about 3.4 million multiply-adds, which numpy finishes in well under a millisecond. The top hits get their text fetched back from SQLite by id and printed tagged `[Book — Chapter]`, ready to be quoted verbatim.

One subtle detail I'd never have guessed: the query gets a prefix prepended before embedding — `"Represent this sentence for searching relevant passages: "`. The embedding model was trained *asymmetrically*: short queries get this instruction, passages don't. Skip it and retrieval quality measurably drops. The lesson generalizes — embedding models have usage contracts, and you have to read the model card.

## What the model actually is

The embedder is `bge-base-en-v1.5` — decoding the name: BAAI (Beijing Academy of Artificial Intelligence, the lab that released it, MIT-licensed), General Embedding family, `base` size tier (~109M parameters — there's a `small` at 33M/384-dim and a `large` at 335M/1024-dim), English, version 1.5. The 768 dimensions of my vectors are literally the model's internal hidden width.

Architecturally it's a BERT-style transformer **encoder** — and the encoder/decoder distinction clicked for me here. GPT-class models are decoders: they read left-to-right and generate text token by token. An encoder reads the entire input at once with bidirectional attention and outputs a *representation* instead of words. This model cannot write a single sentence. It's not a small chatbot; it's a meaning compressor.

Why does dot product equal relevance? Because that's the training objective, literally. After pretraining, it was fine-tuned with **contrastive learning** over hundreds of millions of text pairs: pull true (question, passage) pairs together in the vector space, push mismatched pairs apart. The geometry my search exploits isn't an accident — it's the thing the model was optimized to produce.

And it's not pre-installed anywhere — the first run downloaded it from Hugging Face into `~/.cache/huggingface/hub/` (419MB, which is almost exactly 109M parameters × 4 bytes each — the file is nothing but the weight matrices). Since that one download, the whole system runs fully offline.

## The same dot product that powers attention

While building this I realized the retrieval step rhymes with something I'd written about before: [self-attention inside transformers](how-transformers-work-attention-is-all-you-need.md). In attention, every token's Query vector is dotted against every other token's Key vector to produce relevance scores. My search engine does the same primitive at corpus scale: one question vector dotted against 4,380 passage vectors, producing relevance scores, once per question. Different layer of the stack, same geometric idea — *relevance is a dot product between learned representations*. Once you see it in one place, you see it everywhere in modern ML.

## What building this taught me

The deepest lesson was the **asymmetry of work**. Parsing, chunking, and embedding 4,380 passages is expensive — minutes of compute — so it happens once, offline. A query costs one small embedding plus one matrix multiply. This index-time/query-time split is the same shape as every search engine ever built: crawl and index continuously so that serving a query takes milliseconds. When the per-query latency I actually feel is the 2–3 seconds of loading the model into memory — with the search itself at half a millisecond — the system is correctly designed: all the cost is parked where it runs once.

The second lesson: at this scale, "infrastructure" would have been a liability. No vector database, no embedding API, no server process — each would have added a dependency, a failure mode, and zero capability. FAISS and vector databases exist to solve a millions-of-vectors problem with approximate shortcuts; at 4,380 vectors, an exact linear scan costs a fraction of a millisecond, and the correct amount of infrastructure is none.
