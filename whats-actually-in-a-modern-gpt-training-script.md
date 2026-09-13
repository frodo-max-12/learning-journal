# What's Actually in a Modern GPT Training Script

**Context:** I'd read the transformer paper and understood the architecture in the abstract. Then I opened a real single-file GPT training script — the kind that actually trains a model on a single GPU — and asked for it line by line. The gap between the 2017 paper and the 2026 code is the entry: **almost nothing in the attention block is exactly as the paper described it**, and every difference is a specific fix for a specific problem discovered since.

---

## 1. What the file is

A single-file, single-GPU pretraining script. One file containing the config, the model definition, and the training loop, meant to be read end to end.

That format is itself a choice worth noticing. There's a whole genre of deliberately minimal training scripts written to be *read* rather than extended — the same philosophy as the minimal agent harnesses I'd looked at. **Small enough to hold in your head beats general enough to handle every case**, when the goal is understanding.

---

## 2. Two lines before any imports

The first surprise was at the top of the file, before a single import:

```python
os.environ["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
```

The first tells the GPU memory allocator to use expandable segments, which reduces **memory fragmentation** — over a long run, repeated allocations of varying sizes can leave the memory pool full of unusable gaps, and you hit an out-of-memory error while nominally having memory free. The second just suppresses download progress bars.

The important part is the placement: **these are set *before* importing the libraries**, because those libraries read the environment at import time. Set them after and they're ignored.

That's a small, generalizable trap. Configuration by environment variable is order-dependent in a way configuration by function call isn't, and nothing warns you.

---

## 3. The kernel is chosen by GPU architecture at runtime

```python
if torch.cuda.get_device_capability() == (9, 0):   # Hopper
    ... use one FlashAttention 3 kernel
else:
    ... use a fallback
```

The script asks the GPU what it is and loads a different attention implementation depending on the answer, because **FlashAttention implementations are architecture-specific** — they're hand-tuned to a particular chip's memory hierarchy and instruction set.

This connects directly to the bandwidth result I'd worked out separately. FlashAttention exists because naive attention writes a large intermediate matrix out to main GPU memory and reads it back; the whole optimization is *avoiding that round trip* by keeping tiles in fast on-chip memory. It's a memory-movement optimization, not an arithmetic one — which is why it matters so much, and why it has to be written per-architecture.

---

## 4. The architecture, and how far it has drifted from the paper

The config is a dataclass of hyperparameters, and reading it is a tour of everything that changed since 2017:

| in the config | what it means | vs the paper |
|---|---|---|
| `n_layer`, `n_head`, `n_embd` | depth, heads, model width | unchanged in spirit |
| `n_kv_head` | separate count of key/value heads | **new** — when fewer than `n_head`, this is grouped-query attention |
| `window_pattern="SSSL"` | which layers use a short sliding window vs full attention | **new** |
| `sequence_len`, `vocab_size` | context length and vocabulary | unchanged |

And in the model body, five modifications, each a fix for something:

**RMSNorm instead of LayerNorm.** Normalizes by the root-mean-square of the last dimension rather than by mean and variance. Fewer operations, no mean subtraction, and it works as well — so it's now standard.

**Grouped-query attention.** Multiple query heads share a smaller number of key/value heads. The reason is exactly the bandwidth constraint: during generation you must read the cached keys and values for every past token, every step. Fewer distinct KV heads means **less data to move per token**, which is the thing that actually bounds decoding speed. This is a memory-bandwidth optimization wearing an architecture costume.

**Rotary position embeddings (RoPE).** Instead of adding a position vector to the input, positions are encoded by *rotating* pairs of dimensions in the query and key vectors by a position-dependent angle. Position becomes a geometric transformation applied at attention time rather than a value added at the start — which is why it extrapolates to longer sequences more gracefully.

**QK-norm.** Normalizing queries and keys separately before computing attention scores, to stop attention logits exploding during training. Which is the same failure the scaling factor in the original formula was protecting against — the problem didn't go away, it just needed a second, stronger defence at scale.

**Sliding-window attention on some layers.** The `SSSL` pattern means most layers attend only within a short window and every fourth attends across the full sequence. Since attention is quadratic in sequence length, restricting most layers to a window makes long contexts affordable, while the occasional full-attention layer preserves the ability to move information across the whole sequence.

**And a value residual** — a gated path mixing an embedding into the value pathway on alternating layers, with the gate learned and input-dependent, initialized to neutral so the model starts from the unmodified behaviour and learns whether to use it.

---

## 5. The pattern across all of them

Two things struck me reading that list.

**Every modification is a fix for a named problem.** LayerNorm was doing unnecessary work → RMSNorm. Decoding is bandwidth-bound → grouped-query attention. Position embeddings didn't extrapolate → RoPE. Attention logits exploded at scale → QK-norm. Quadratic cost at long context → sliding windows. None of them is a general improvement to intelligence; each is a specific defence against a specific failure someone hit.

Which means **the architecture is an accumulation of scar tissue**, and the paper is the shape before any of the scars. Reading the paper tells you the idea. Reading the code tells you what happened when people ran the idea for eight years.

**And gates are initialized to neutral.** That gating value is set so the model starts out behaving as if the new pathway weren't there, and can learn to use it. That's a genuinely good engineering habit: **add a mechanism in its disabled state and let training decide**, so the change can't hurt you and the model discovers whether it helps.

---

## 6. What I took away

**Read the paper for the idea, the code for the practice.** I could have explained self-attention before this and would have described something that no current implementation actually runs. Neither view is sufficient — the paper is the concept, the code is the concept plus everything learned since.

**A surprising amount of "architecture" is memory-movement optimization.** Grouped-query attention, FlashAttention, and windowed attention are all fundamentally about moving fewer bytes. Once I'd worked out that decoding is bandwidth-bound rather than compute-bound, half the design decisions in this file stopped looking like modelling choices and started looking like consequences of one hardware fact.

**Configuration order matters when configuration is environmental.** Two lines above the imports, silently ineffective if moved below them. That's the sort of thing you only learn by reading real code, because no explanation of transformers would ever mention it.
