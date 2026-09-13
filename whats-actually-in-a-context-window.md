# What's Actually in a Context Window — and Whether I'm Polluting Mine

**Context:** I have a habit of sending a prompt, thinking of something better, rewinding, and re-sending — four or five times for one question. I assumed I was stuffing the context window with junk and degrading the answers. So I asked what actually happens. The answer was that my premise was wrong in an interesting way, and chasing it properly meant first finding out what's in a context window *before I type anything at all*.

---

## 1. First, the units

A rough conversion for English prose: **1 token ≈ 0.75 words**, or 1 word ≈ 1.3 tokens.

So a conversation that hit 460k tokens was roughly **345,000 words** — about four full-length novels, or ~1,150 pages of standard prose.

That's an upper bound though, and the caveat matters more than the number. Code, JSON, and non-English text are *denser* — closer to 1:1 tokens-to-words or worse, because tokenizers are trained on natural language and fragment everything else. In an agent conversation, most of the volume is tool output, file contents, and code, so the human-readable share is far smaller than the headline number suggests.

That reframed the ceiling for me. A large context window isn't "four novels of my thinking." It's mostly machine exhaust.

---

## 2. What loads before you say anything

The zero-cost-to-me assumption I'd been carrying — that a fresh session starts empty — is false. Several things arrive before the first prompt:

| what | notes |
|---|---|
| the system prompt | defines the tool's behaviour, formatting rules, safety rules |
| tool definitions | one JSON schema per available tool — these are not small |
| project instructions | a `CLAUDE.md`-style file, if one exists for the working directory |
| memory index | a persistent index of user-level facts, if the feature is on |
| environment | working directory, OS, date, git status — but **not** a directory listing |

That last one corrected a real misconception of mine. I had assumed that because I'd built dozens of scripts on this laptop, an agent starting a new session would *know they exist*. It doesn't. The filesystem is invisible until something runs `ls`, `read`, or `grep`.

Which has a direct practical consequence: whether an agent reuses a script you already wrote or writes a fresh one from scratch is determined almost entirely by **whether something in the always-loaded context points at it**. Memory and project files aren't a cache of your code — they're a *directory of where to look*, compensating for the fact that the filesystem isn't visible. When the pointers are stale or missing, the symptom is re-implementation of things that already exist.

---

## 3. Progressive disclosure — the pattern worth stealing

Then I found the mechanism that makes the always-loaded part affordable, and it's the best design idea in this entry.

Extensions — skills, in this tool's vocabulary — are folders containing a definition file. That file has YAML frontmatter with a `name` and a one-line `description`, then a body with the actual instructions.

At session start, the harness scans every extension folder and injects **only the name and description** into context. Everything below the frontmatter stays on disk until the extension is actually invoked.

So the always-loaded cost of having fifty extensions installed is fifty one-line descriptions. The full instructions — which might run to hundreds of lines each — cost nothing until needed.

Two consequences follow, and both are load-bearing:

**The description is the trigger.** It's the only thing visible when deciding whether to invoke the extension. That makes it do double duty: it's documentation *and* it's the routing key. A vague description means the capability exists and never fires — which is a much more annoying failure than a broken one, because nothing errors, the thing just quietly never gets used.

**Edits land next session, not this one.** The frontmatter was read at startup. Changing it mid-session changes the file, not the loaded context.

The general pattern — **load an index eagerly, load the content lazily, and make the index entry good enough to route on** — is the same shape as a database index, a library card catalogue, or a table of contents. What's new is applying it to instructions for a model, where the index lives *in* the scarce resource and the content lives outside it.

---

## 4. My actual question: does drafting pollute the context?

Here's where my premise turned out to be wrong, and the two scenarios I'd conflated separate cleanly.

**Scenario A — editing before pressing Enter.** Nothing leaves the terminal. Drafts `v1`, `v2`, `v3` live entirely in the local input buffer. No partial sends, no diffing, no token cost, no cache activity. Only `v4` is ever transmitted, and the model has no idea the earlier versions existed.

So there's no "Claude was processing the old prompt and then it got deleted." There was never anything to delete. **This style is free.** I'd been managing a cost that didn't exist.

There is also no diff-based prompt analysis anywhere in the protocol. A message is sent complete or not at all; nothing compares `v3` to `v4` and processes only the delta. That abstraction, which I'd assumed existed, isn't part of how any of this works.

**Scenario B — sending, then rewinding, then re-sending.** This is what I was *actually* doing, and it's genuinely different.

The good news is that the context question still comes out fine: rewound turns are removed from what gets sent on the next call. From the model's perspective at `v4`, it looks like `v4` was the only message at that turn. Output quality isn't degraded by the earlier attempts.

But there are real costs the drafting pattern doesn't have:

- **You pay for every send.** Each one was a complete API call — full input prefix, plus the prompt, plus whatever output was generated before you interrupted. Four sends is roughly four times the tokens for one question.
- **You disturb cache warmth.** The prompt cache is prefix-keyed. Rewinding changes the prefix that subsequent calls build on.

So: draft freely, but if you find yourself sending-and-rewinding as a *drafting* technique, move that iteration into the input buffer instead. Same result, a quarter of the cost.

---

## 5. What actually does pollute a context window

Since my drafts weren't the problem, I asked what is. The real space-eaters are accumulated *turns*, not inputs:

- old tool results — reading large files, searches with many hits, commands with long output
- long earlier responses
- sub-agent outputs returned into the main thread
- the fixed startup cost of project instructions and memory

A working session with heavy file reading sits at tens of thousands of tokens of accumulated context easily. And the important part: **that degrades quality well before you hit any ceiling.** Attention dilutes and earlier instructions drift. "I still have room" is not the same as "this is still working well" — the failure is gradual and silent, which is why it's worth managing deliberately rather than at the limit.

The clearest tell is behavioural: *the agent starts making mistakes it wouldn't make in a fresh window.* That's the signal to reset, and it arrives long before any counter turns red.

---

## 6. The hygiene rules I settled on

Reset is not binary — there's a ladder between "keep going" and "start over," and knowing the rungs is most of the benefit:

| situation | move |
|---|---|
| same task, same files | continue — accumulated understanding is worth real money |
| same project, long session, tool-result bloat | compact in place: summarize, keep the useful state |
| went down a wrong path | rewind to the last good checkpoint rather than arguing in place |
| new sub-task, same project | clear the conversation, keep project context |
| genuinely unrelated task | new session — you probably want a different working directory anyway |

The two mistakes to avoid sit at opposite ends.

**Don't reflexively start fresh.** Cache warmth and accumulated project understanding have real value, and re-loading a large set of project files on every new session is a cost you pay for nothing if the task is continuous.

**Don't try to correct a confused conversation in place.** If earlier turns contain a wrong turn, the model keeps pattern-matching against them. Rewinding to before the mistake is cheaper and more reliable than adding a turn that says "ignore what I said earlier" — you're competing with the text rather than removing it.

---

## 7. What I took away

**The context window is a budget, not a container.** I'd been thinking of it as a box that fills up, where the only question is whether you overflow. It's better understood as a resource where *everything present competes for attention*, so relevance density matters more than occupancy. Half-full of junk is worse than three-quarters full of relevant material.

**The invisible-filesystem fact changed how I write project instructions.** An agent's default state is knowing nothing about your machine. Every capability you want reachable has to be pointed at from something that loads eagerly — which reframes memory files and project instructions from "notes" into *routing tables*.

**Progressive disclosure is the general solution to a scarce always-loaded budget.** Index in the window, content on disk, and the index entry has to be good enough to route on. That's a design constraint I now recognize in a lot of places I hadn't been reading as index-versus-content problems.

And the meta-lesson, which is the one I'd keep: I optimized my drafting habit for months against a cost model I'd never checked. The fix wasn't a better habit — it was asking what actually happens.
