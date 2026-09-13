# Local Models with Ollama, Hooks, and the Plugin I Uninstalled

*This one started as an irritation, not a curiosity. Claude's answers had been reading as dense — long qualified sentences, abstract nouns, the consultant register. Someone had written a Claude Code plugin that pipes every assistant message through a second, smaller model and appends a plain-English rewrite underneath. I wanted it. Getting it working took me through running large language models on my own laptop, what "12 billion parameters" costs in RAM, and how Claude Code's hook system actually works. Then I removed all of it, because the thing I built wasn't worth what it cost to run. The removal is the part I'd want to remember.*

---

## The problem I was actually trying to solve

Model output has a characteristic shape: hedges stacked into clauses, verbs turned into nouns ("perform an analysis of" instead of "analyze"), both sides of a trade-off presented when one side obviously wins. It's optimized to *look* thorough. It reads like sludge.

The plugin's premise is neat: don't fight the model's style, post-process it. Take the finished message, hand it to a second model, and show a simplified version alongside. The original stays untouched — you get both.

That premise requires a second model running somewhere. Which is how I ended up learning what that actually involves.

## What Ollama is

Ollama is two things wearing one name: a **model runner** and a **local HTTP server**.

The runner handles the mechanics of loading a model's weights into memory and executing inference against them. The server wraps that in an HTTP API on `localhost:11434`, so any program on your machine can send it a request and get generated text back — the same shape of interaction you'd have with a cloud API, minus the network.

```
ollama pull gemma4:12b-mlx     # download weights
ollama run  gemma4:12b-mlx     # load and chat
ollama ps                      # what's currently in memory
```

Models live in `~/.ollama/models` as content-addressed blobs plus manifests — the same design Docker uses for image layers. A model tag like `gemma4:12b-mlx` is a manifest pointing at blobs; pulling a second variant that shares layers won't re-download them.

The `-mlx` suffix matters on a Mac. MLX is Apple's array framework, built for Apple Silicon's unified memory. An MLX build of a model is compiled to run on the GPU cores of an M-series chip rather than through a generic CPU path.

## What "12 billion parameters" costs

This is the part I understood only after watching it happen.

A model is a large pile of numbers — weights — learned during training. `gemma4:12b` has roughly 12 billion of them. To generate even one token, the runner has to multiply your input through essentially all of those weights. **They must be in memory. All of them.** There's no meaningful way to stream a model from disk during inference; disk is orders of magnitude too slow, and every token touches the whole network.

So the arithmetic that governs everything:

| | |
|---|---|
| Parameters | ~12 billion |
| On disk | 7.7 GB |
| Resident in RAM when loaded | 8.5–10 GB |
| My machine | 16 GB total |
| Free memory while loaded | 23% |

If 12 billion parameters were stored at full 16-bit precision, that's 2 bytes each — about 24 GB, which simply would not fit. It fits in 7.7 GB because of **quantization**: the weights are stored at reduced precision, roughly 4–5 bits each instead of 16. You trade a small amount of output quality for a 3–4× reduction in size. Essentially every local model you'll run is quantized. It's the only reason consumer hardware can run these at all.

The resident figure exceeds the on-disk figure because loaded weights aren't the only cost. There's also the **KV cache** — the model's stored attention state for the current conversation — which grows with context length. A larger context window costs memory even with the same weights.

The constraint this creates is hard and unforgiving. The plugin's default model was an 18 GB one. On a 16 GB machine that isn't "slow", it's *impossible* — there is no configuration where 18 GB of weights fits in 16 GB of RAM. I had to pick a smaller model before anything could work at all. **Model size versus available RAM is the first question in local inference, and it's binary.**

### Unified memory, and why `ollama ps` says "100% GPU"

On Apple Silicon there's no separate video RAM. CPU and GPU address the same physical memory. When `ollama ps` reports `100% GPU`, it means the model is being executed by the GPU cores — but those cores are reading the same 16 GB the rest of the system is using. On a discrete-GPU PC, a model either fits in the graphics card's dedicated VRAM or it doesn't. On a Mac, the model competes directly with your browser and editor for the same pool.

### The cold-start tax

Ollama unloads a model after about five minutes idle, and it's right to — leaving 8.5 GB parked would starve everything else. But that produces a latency pattern that turns out to matter more than raw speed:

- **Warm** (model resident): ~4.5s for a short rewrite
- **Cold** (must reload from disk): 12–16s

In real use you're rarely warm. You read something, think, come back three minutes later — and pay the reload. I measured the warm number first and drew a conclusion from it, which was a mistake; the cold number is the one you actually live with.

## Hooks: how Claude Code lets you intercept things

The plugin does its work through a **hook**. Hooks are shell commands that Claude Code runs at defined lifecycle events. They're executed by the harness, not by the model — which makes them *deterministic*. The model can't forget to fire one or decide it isn't relevant.

There are events across the whole lifecycle: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`, and more. This plugin uses `MessageDisplay`, which fires while assistant text is being displayed.

The contract is simple: Claude Code sends the hook a JSON object on stdin; the hook writes JSON to stdout. To change what's shown, it returns:

```json
{"hookSpecificOutput": {"hookEventName": "MessageDisplay", "displayContent": "..."}}
```

Two design details in this particular hook were worth stealing:

**Fail open.** Every error path — no `jq`, model unreachable, timeout, empty response — exits 0 and emits nothing, which leaves the original text on screen. A display hook that could crash and swallow the assistant's answer would be worse than no hook. The failure mode is "you see the normal thing."

**Buffer to final.** `MessageDisplay` fires once per streamed chunk, and each fire is a separate process with only that chunk's fragment. To rewrite a whole message the hook writes each fragment to a temp file keyed by message ID, and only calls the model on the chunk flagged `final`, once the full text exists.

### The display layer is not the transcript layer

This was the most useful thing I learned, and I only learned it because I doubted a claim.

I assumed the appended rewrite would become part of the conversation and get re-sent as context on every subsequent turn — inflating my token usage. The plugin claimed to be "display-only." I checked instead of trusting it.

The hook always emits a distinctive separator before each rewrite. Searching every transcript `.jsonl` on my machine for that separator returned **zero matches** — including sessions where I'd watched the block render on screen. The stored assistant message ended exactly where the original text stopped.

So there are genuinely two layers:

- **`displayContent`** — what gets painted on your screen
- **the `.jsonl` transcript** — what gets replayed as context on every following turn

The hook only touches the first. The rewrite costs zero additional context and zero subscription usage. The mental model I'd been carrying — that anything appearing on screen is part of the conversation — was simply wrong.

## Hooks vs CLAUDE.md vs Skills vs Plugins

I'd worked through the distinctions in a separate conversation, and building this made them concrete:

| | What it is | Enforcement |
|---|---|---|
| **CLAUDE.md** | Instructions injected into context | Advisory — the model may drift |
| **Skill** | Instructions loaded on demand when relevant | Advisory, but only costs context when triggered |
| **Hook** | Shell command run by the harness at an event | **Deterministic** — always fires |
| **Plugin** | A package that can bundle hooks, skills, commands, agents | Delivery mechanism, not a mechanism itself |

The sharpest question I asked was whether a rule I keep in `CLAUDE.md` should become a hook instead, since hooks can't be ignored. The answer turned on cost: a `CLAUDE.md` instruction is stated once and sits in context; a hook that injects text fires on *every* message, and that repetition both burns context and over-constrains the model. Determinism isn't free. Use a hook when you need a guarantee and can pay for it every turn; use `CLAUDE.md` when advisory is good enough.

A plugin is a different category from the other three. It's packaging — a manifest, a `hooks/hooks.json`, some scripts, installed from a marketplace repo. It's how hooks and skills get *distributed*, not a separate kind of behaviour.

## Two debugging lessons

**Test the cheap gate before paying the expensive one.** The docs didn't state whether `MessageDisplay` renders in the desktop app or only in the terminal. Rather than download 7.7 GB and set up an API key to find out, I put the hook in a stub mode that emits fixed placeholder text with no model at all. One restart, thirty seconds, definitive answer. If it hadn't rendered, I'd have spent nothing. Isolate the variable that invalidates everything else, and test that first.

**Read the logs, don't trust that it worked.** The hosted path worked correctly and returned good output — but its log showed `retrying without thinkingLevel` on every request. The parameter I'd used to disable the model's internal reasoning was from a newer API surface; the endpoint I was calling wanted a different field name and rejected mine outright. My own "tolerate API drift" fallback was silently absorbing the failure and retrying. It worked, so nothing looked wrong. Fixing the field name took latency from ~9s to 1.7s. **A fallback that fires every time isn't resilience, it's a bug wearing a disguise** — so log it loudly enough to notice.

## Why I removed it

The honest cost-benefit, once it was running:

**The benefit was smaller than I expected.** The rewrites were competent — shorter sentences, plainer vocabulary, jargon expanded. But they came out roughly the *same length* as the original. It made text easier to parse, not shorter to read. On a message that was already reasonably clear, it just restated what I'd read thirty seconds earlier.

**The costs were real and recurring.** Two options, and each fails a different test:

- **Local model** — 8.5 GB of RAM on a 16 GB machine, GPU load, heat, and battery drain on every message, plus a 12-second stall whenever it had gone cold.
- **Hosted free tier** — no local cost, but every assistant message I generate gets sent to a third party, and free tiers are free precisely because the provider uses that content to improve their products. I work on things I don't want leaving my machine.

Which surfaced the structural point. **Free, private, no local compute — you can pick two:**

| | Free | Private | No local load |
|---|---|---|---|
| Local model | ✅ | ✅ | ❌ |
| Hosted free tier | ✅ | ❌ | ✅ |
| Hosted paid tier | ❌ | ✅ | ✅ |

There's no fourth row. Any tool that pipes your content through a second model inherits this, and no amount of engineering escapes it — it's a property of the arrangement, not the implementation.

Given a benefit I'd describe as *mild* and a cost that recurs on every single message, it doesn't clear the bar. So I uninstalled the plugin, removed the hooks, deleted the translation proxy and its background service, and stopped the model server. The 7.7 GB model stays on disk, inert, for the next time I want to experiment with something local.

### The thing worth keeping

The tool didn't survive; the map did. I now know what running a model locally actually demands, why quantization exists, why a 16 GB machine has a hard ceiling on model size, what unified memory changes, why cold-start latency dominates the felt experience, and how the deterministic layer of my own tooling works and where it can intervene.

And one more, which generalizes past this: **a claim in a README is a hypothesis.** "Display-only" was testable in about a minute, and testing it corrected a mental model I'd have carried around for months. The cheapest thing in the whole exercise was checking.
