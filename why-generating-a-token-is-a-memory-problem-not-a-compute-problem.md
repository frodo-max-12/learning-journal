# Why Generating a Token Is a Memory Problem, Not a Compute Problem

**Context:** I got curious about "Flash"-tier models — the small fast ones every lab ships alongside its flagship — and asked what technically makes them fast. That pulled in FLOPs, quantization, and finally the sentence that reorganized my whole picture of AI inference: *the model is bottlenecked by memory and bandwidth.* I didn't know what that meant. Working it out produced an arithmetic result I found genuinely startling.

---

## 1. Two properties that get confused constantly

**Memory capacity** — how many bytes the accelerator can *hold* at once. Measured in GB.
**Memory bandwidth** — how fast bytes can *move* from memory into the compute units. Measured in TB/s.

A truck has a cargo capacity and a top speed. Both matter; they're different constraints and they bind in different situations.

Both are separate again from **compute** — how many arithmetic operations per second the chip can perform.

Three numbers, and I'd been collapsing them into "how powerful is the GPU."

---

## 2. The hierarchy inside an accelerator

The same trade every memory hierarchy makes, at a different scale:

```
registers        <1 KB per thread     instant          on the compute core
SRAM / L1        ~256 KB per unit     ~100s TB/s       on the die
L2 cache         tens of MB           ~10 TB/s         on the die, shared
HBM              80–192 GB            3–8 TB/s         stacked beside the die
host DRAM        hundreds of GB       ~50 GB/s         across the system bus
SSD              TBs                  1–7 GB/s         disk
```

Each tier down is roughly 10–100× more capacity and 10–100× less bandwidth.

What people mean by "the GPU's memory" is **HBM** — stacked DRAM on the same package as the compute die. It's the bottleneck tier because model weights are far too big for SRAM and must be read constantly.

And a fact that reframes the hardware market: **HBM is why frontier models can run at all.** Without it you'd be feeding the compute die through ~50 GB/s system memory and the chip would idle essentially all the time. Which is also why accelerator supply has tracked HBM supply — the pricing story is as much about stacked memory as about the logic die.

---

## 3. The capacity constraint: does it fit?

Straightforward, and it's what quantization is *usually* explained as solving:

| precision | 70B-parameter model | fits on |
|---|---|---|
| FP16 | 140 GB | needs two 80 GB accelerators, sharded |
| INT8 | 70 GB | one, with headroom |
| INT4 | 35 GB | a consumer graphics card |

Halve the bits per weight, halve the memory, and the deployment options change category. That's the familiar half of the story.

---

## 4. The bandwidth constraint — the part that surprised me

Here's what actually happens when a model generates **one token**, for a single user:

1. **Read all the weights** from HBM through the memory bus into the compute units.
2. **Do the matrix multiplications.**
3. **Write the result** — one token's worth of activations, negligible.

Now the arithmetic for a 70B model in FP16 on a high-end accelerator:

| step | time |
|---|---|
| compute — about 140 GFLOPs of arithmetic | **~0.14 ms** |
| moving 140 GB from HBM at ~3.35 TB/s | **~42 ms** |

**The data movement takes roughly 300× longer than the arithmetic.**

The compute units are idle almost the entire time, waiting for weights to arrive. Generating a token is not a computation problem. It's a **data-transport problem** with a small amount of arithmetic attached at the end.

I had this exactly backwards. I'd pictured inference as the chip working hard — that's the mental image the word "compute" invites. What's actually happening is a bus moving 140 GB across a wire, once per token, while the arithmetic units wait.

---

## 5. What follows from that, and it's most of the field

Once bandwidth is the ceiling, a long list of otherwise-unrelated engineering decisions becomes one decision.

**Quantization does two jobs, and the second is bigger.** Everyone explains it as making the model *fit*. But halving the bits also halves **the bytes you must move per token**, which directly doubles decoding speed. The speedup isn't a side effect of the size reduction — for single-stream generation it's the *main* effect.

**Batching is nearly free, which is why serving works the way it does.** You read the weights once and use them for every request in the batch. Two users cost almost exactly what one user costs, because the expensive part — the transfer — is shared. That's why inference APIs batch aggressively, and why per-token pricing can be as low as it is.

**Smaller models are fast super-linearly.** Fewer parameters means fewer bytes moved per token, on top of less arithmetic. That's a substantial part of what makes a Flash-tier model fast — not a fundamentally different architecture, but fewer bytes crossing the bus per token, usually combined with aggressive quantization.

**And it explains a hardware pattern I'd noticed and not understood.** Two chip generations can have identical peak arithmetic throughput and very different real-world inference performance, because the newer one has faster memory. If you only read the FLOPS number you'd conclude they're equivalent. For decoding, the bandwidth column is the one that matters.

---

## 6. The framing I'd keep

**A "Flash" model isn't a different kind of thing.** It's the same architecture with fewer parameters, usually quantized, tuned so that fewer bytes have to cross the memory bus per generated token. The marketing name describes a point on a bandwidth/quality curve, not a distinct technology — and the analogous tier exists at every lab, because the constraint is physical rather than proprietary.

**Roofline thinking is the general tool.** For any workload, ask: is it limited by arithmetic, or by moving data? Single-stream decoding is dramatically memory-bound. Training, with its large batches, is much closer to compute-bound. **Same hardware, same model, opposite bottleneck** — which is exactly why training and inference have diverged into separate chip designs.

---

## 7. What I took away

**"Compute" is a misleading name for the constraint.** The word points at the arithmetic, and the arithmetic is 0.3% of the time. I'd been reasoning about the wrong resource, and once I'd done the two-line calculation, a dozen previously arbitrary facts about the industry lined up behind one number.

**The interesting number is usually a ratio.** Not "how fast is the arithmetic" or "how fast is the memory," but the ratio between operations and bytes moved. That ratio decides which half of the machine is idle.

**Do the arithmetic yourself.** 140 GB ÷ 3.35 TB/s is a division I could have done at any point in the last two years, and it would have told me immediately that inference is a transport problem. I didn't do it because I assumed the answer was already reflected in how everyone talks about it — and it isn't, because everyone calls the whole thing "compute."
