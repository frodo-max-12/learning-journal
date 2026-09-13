# Training vs inference — the economics that decide which AI labs survive

---

## The two fundamentally different things AI chips do

I had been using "AI compute" as one bucket. It is not one bucket. It is two completely different workloads that happen to use similar-looking silicon. They have different economics, different chip designs, different deployment patterns, and different customer bases.

| | Training | Inference |
|---|---|---|
| What it does | Teaches the model from scratch by feeding it trillions of tokens | Uses the trained model to answer a single query |
| When it happens | Once (or periodically) — months of compute per run | Every time a user asks the model anything |
| Cost profile | Massive upfront cost — hundreds of millions to billions per model | Small per query, but happens billions of times |
| Analogy | Writing a textbook | Looking up an answer in the textbook |

This split is the most important economic boundary in the AI infrastructure market.

## What "training" actually involves

Training is the process of taking a randomly initialised neural network and showing it enormous amounts of data so it learns patterns. For something like GPT-4 or Gemini Ultra, this means:

- Trillions of tokens of text (and images, audio, video for multi-modal models).
- Months of compute on tens of thousands of GPUs or TPUs running in parallel.
- A single training run for a frontier model costs somewhere in the range of $100 million to $1 billion or more.
- All of that cost is upfront. No revenue is generated during training.

The chip requirements are extreme. You need enormous memory bandwidth, ultra-fast interconnect between chips (so they can share gradients during backpropagation), and massive parallel compute. Training chips like Google's 8T (the eighth-generation training TPU) come in pods of 9,600 chips connected on a single high-bandwidth network. That entire pod is one training cluster.

## What "inference" actually involves

Inference is what happens after training is done. The model exists, its weights are fixed, and now you use it to answer queries.

- Each query takes milliseconds to seconds, not months.
- Each query costs fractions of a cent, not millions of dollars.
- But each successful AI product runs **billions of inference queries per day**.

The chip requirements are different. You need lower latency (the user is waiting), more locations (so latency is low everywhere in the world), and you can use smaller pods because each query only needs a few chips to run. Google's 8I (eighth-generation inference TPU) comes in pods of about 1,152 chips and can be air-cooled, so it can be deployed in many more data centres than the liquid-cooled training chips.

## The economic pressure that nobody escapes

Here is the sentence Kurian dropped that I keep coming back to:

> "No matter how rich you are, you cannot fund training without making money on inference."

The math behind this sentence is brutal.

1. Training a frontier model costs roughly $100 million to $1 billion. Pure cost. No revenue generated during training.

2. The only way to make that money back is by selling **inference** — charging users or enterprises per query (per token output) once the model is deployed.

3. If inference revenue is less than the cost of running inference *plus* amortised training cost, the lab burns cash and eventually dies.

4. Frontier AI labs today survive by raising large rounds of venture capital to bridge this gap while their inference revenue is still ramping. **Kurian's point: VC funding eventually runs out**. You cannot train forever on someone else's dime.

This is why some AI labs are growing and others are quietly hitting walls. The growing ones — OpenAI, Anthropic, Google — have inference businesses that are scaling fast enough to start covering training costs. The struggling ones cannot show that path and have to keep raising at increasingly difficult terms.

## Why Google has a structural edge here

This is also where Google's edge becomes obvious. They own their silicon. Their training cost per token is dramatically lower than rivals who pay NVIDIA's gross margin on every H100. Their inference cost per token is dramatically lower than rivals who pay NVIDIA's margin on every inference GPU.

That means the breakeven on inference covering training comes faster for Google than for any lab that does not own its silicon. It is not that Google is more efficient at AI research — it is that they are vertically integrated at the silicon layer, and that integration changes the unit economics at every level above it.

Kurian was almost casual about this in the interview, but it is the reason every other major hyperscaler is racing to build their own chips. Owning the silicon is the only way to make the inference-must-pay-for-training math work in your favour.

## Why this drove a chip split

Here is where the chip-design story connects back to the economic story.

For a long time, the same chip was used for both training and inference. (Google's prior generation, Ironwood, was used for both — training during the day-long batch jobs, inference during the daytime traffic peaks.) That made sense when AI workloads were small enough that one chip family was good enough for everything.

It stops making sense at scale. Training and inference want different things from a chip:

- Training wants huge memory, ultra-fast interconnect between many chips, liquid cooling, concentrated in a few enormous data centres.
- Inference wants fast individual chip execution, low latency, smaller chip groups, air cooling so it can be deployed in many more locations close to users.

Google's eighth generation split these into two separate chip designs. **8T** is purpose-built for training. **8I** is purpose-built for inference. The split is not a marketing move; it is a recognition that the workloads have diverged enough that one design cannot serve both well.

The rest of the industry is following. NVIDIA designs different products for training (H100, B200) versus inference (L4, L40S, smaller variants). AMD has separate training and inference SKUs. Even AWS has separate Trainium (training) and Inferentia (inference) chips. Specialisation has won.

## The agentic workload twist

The Kurian interview added one more layer that I had not fully internalised. Agents — AI systems that take actions autonomously over many steps — change the inference workload yet again.

Traditional inference: a user asks one question, the model answers, done. Maybe a thousand tokens generated. Done in seconds.

Agentic inference: an agent gets a task ("plan my vacation, book the flights, send confirmation"), runs for hours, calls tools dozens of times, holds intermediate state in memory the whole time. Inference pattern is wildly different — long-running, stateful, calling general-purpose compute (browsers, databases, APIs) alongside the AI model.

This is why Google built Axion (ARM CPUs) alongside the TPUs. Agents need general-purpose compute to run the tools they call, sitting next to the AI accelerators that run the model. The full agent loop touches both kinds of silicon.

It is also why Kurian named "consumer agent VMs" as the next infrastructure bottleneck. The economics of running an agent for hours per task — keeping VMs hot, holding state in memory, calling tools — are very different from chat. If consumer agents become as common as ChatGPT, the inference layer needs cheaper on-demand compute, denser servers, faster startup times. None of which the current infrastructure was designed for.

## What this taught me about the AI capex story

The narrative I had absorbed from headlines was something like: "everyone is buying GPUs, AI capex is going up forever, NVIDIA wins." That narrative is *partially* right but misses the structural split.

The right way to think about AI capex is two distinct curves:

**Training capex** — concentrated, lumpy, mega-orders to a few labs. Driven by the foundation-model arms race. A handful of buyers (OpenAI, Anthropic, Google, Meta, xAI, a few sovereign-scale players). Multi-billion-dollar contracts negotiated quarterly.

**Inference capex** — diffuse, recurring, deployed everywhere. Driven by user adoption of AI products. Many more buyers (every cloud provider, every enterprise running AI internally, every neocloud serving inference workloads). Smaller individual orders, but vastly more volume in aggregate.

These two curves move on different cadences and respond to different signals. Training capex is sensitive to "is the next-generation model going to be commercially viable?" Inference capex is sensitive to "are users actually using AI products at scale?" When training capex pauses (because a generation hits diminishing returns), inference capex can keep growing if user demand is strong.

This split also explains why some chip vendors do better in some periods than others. NVIDIA dominates training. The inference layer is more contested — Google TPUs, AMD MI300s, AWS Inferentia, custom chips — because inference workloads are more varied and the value of optimisation is higher when you ship the same chip in millions of locations.

> Training and inference look like the same workload from outside, but they are completely different economic engines. Training is the upfront capex bet. Inference is the recurring revenue. Every AI lab survives only if the second one eventually pays for the first one — and the labs that own their silicon get there fastest.

---

*This pairs with [why hyperscalers build their own chips and why Intel lost](why-hyperscalers-build-their-own-chips-and-why-intel-lost.md), which explains why owning the silicon is the underlying advantage. The hardware side is in [HBM and AI accelerators](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md), which describes what is actually inside the chips that do this work.*
