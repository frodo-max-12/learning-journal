# What a Harness Actually Is — the Model Has No Hands

**Context:** I wanted to build my own agent harness, and opened with what I thought was a safe assumption: "Claude Code and Hermes are both harnesses, right?" Half of that was wrong, and the wrong half turned out to be the cleanest way into the whole concept. Hermes is a *model*. Claude Code is a *harness*. The distinction between those two things is exactly what a harness is.

---

## 1. Start from what a model actually is

When you reach a language model over an API, it is a **stateless function**. You POST a list of messages, you get one message back. That's the entire interface.

It cannot read a file. It cannot run a command. It cannot remember yesterday. Twenty API calls in a row share nothing unless *you* resend the history each time.

So how does a coding agent edit files on my laptop?

The API lets you declare **tools** — JSON schemas describing functions that *your* program implements. The model can't run them. It can only reply: *"I'd like to call `bash` with `command='ls'`."* Your program actually runs `ls`, appends the output to the message list as a tool result, and calls the API again. The model reads the result and decides the next step. Repeat until it replies with plain text instead of a tool request.

**That loop is the harness's beating heart.** A harness is everything wrapped around the model call: the loop, the tool implementations, the context assembly, the permission gates, the interface.

> model + harness = agent

---

## 2. The whole thing in about 40 lines

This is the part that made it concrete. Stripped to essentials, a coding agent is:

```python
import os, subprocess
import anthropic

client = anthropic.Anthropic()

TOOLS = [{
    "name": "bash",
    "description": "Run a shell command and return its combined stdout and stderr.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

def run_bash(command):
    if input(f"  run `{command}`? [y/N] ").strip() != "y":   # the permission system, v0
        return "User declined to run this command."
    r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
    return ((r.stdout + r.stderr).strip() or "(no output)")[-5000:]   # context is finite

messages = []
while True:
    if not messages or messages[-1]["role"] == "assistant":
        messages.append({"role": "user", "content": input("\n> ")})

    resp = client.messages.create(
        model="...", max_tokens=16000,
        system=f"You are a coding agent. cwd: {os.getcwd()}",
        tools=TOOLS, messages=messages,
    )
    messages.append({"role": "assistant", "content": resp.content})

    results = []
    for block in resp.content:
        if block.type == "text":
            print(block.text)
        elif block.type == "tool_use":
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": run_bash(**block.input)})
    if results:
        messages.append({"role": "user", "content": results})   # loop continues, no user input
```

Structurally, that *is* a coding agent. Run it, ask it to find and fix a bug, and watch it chain `cat` → reason → edit → rerun the tests without you touching anything. Watching that first self-chained run is the moment the mystique evaporates.

Two lines in there are load-bearing in a way that isn't obvious:

- The `input()` gate is **the entire permission system in embryo**.
- The `[-5000:]` truncation is **context management in embryo**.

And that observation generalizes into the most useful frame I got out of this: every serious harness feature is a *hardening of one line of this program*.

---

## 3. The refinement ladder

Each famous agent feature exists because the naked loop fails in a specific, reproducible way. Once you see the failure, the feature stops being a product decision and becomes an obvious consequence:

| the naked loop fails because… | so you build |
|---|---|
| it forgets everything between runs | persistence, memory files, project instructions |
| tool output blows past the context limit | truncation, summarization, compaction |
| a single `bash` tool is a blunt instrument | purpose-built read/edit/search tools with tighter schemas |
| `rm -rf` executes as happily as `ls` | permission tiers, allowlists, sandboxing |
| one long task pollutes context with irrelevant detail | sub-agents with their own context windows |
| the loop can't tell when it's done | stop conditions, task lists, explicit completion criteria |

This is a much better way to learn agent design than reading a feature list, because the feature list is the answer sheet and the failure list is the exam.

---

## 4. Harness vs agent vs model — the distinction that actually matters

I kept using "agent" and "harness" interchangeably. They belong to different categories:

- The **model** can decide but can't do. Stateless text function: given the conversation so far, it emits the next move. No hands, no memory, no persistence.
- The **harness** can do but can't decide. Ordinary software — loop, tools, context assembly, permission gates. Run it without a model and it just sits there.
- The **agent** is the two joined by the loop, running toward a goal. The model proposes, the harness executes, the composite perceives and acts.

**"Agent" is a behavioural word** — defined by what the thing does. **"Harness" is a structural word** — defined by what it's made of. That's why the confusion is so persistent: they're not competing labels for the same object, they're descriptions at different levels.

Two tests make it concrete:

**The swap test.** Hold the harness fixed and change the model — you get a *different agent*, better or worse at the same tasks. This is literally how agent benchmarks are run now: one harness held constant, each model dropped into it yielding a different score. Same harness, many agents. It also explains why labs obsess over "scaffolding" when reporting benchmark numbers — the same model in a different harness performs wildly differently, so a score without a named harness is close to meaningless.

**The repo test.** What's on GitHub is a *harness* — code at rest, plus a config line naming a model. The agent only exists at runtime, when there's a live context window, a goal, and tool access. **You can `git clone` a harness; you can't `git clone` an agent.** Sub-agents make this vivid: each spawn is a new agent *instance* running the same harness *code*.

Everyone blurs the two anyway, and there's a reason: the model is bought, not built, so "building an agent" is ~100% harness work in practice.

---

## 5. Where the words come from

I assumed both terms came from machine learning. Neither does.

**"Harness" comes from software testing**, not ML — the *test harness* / *eval harness* tradition, where a harness is the scaffolding that sets up an environment, feeds inputs to the thing under test, and collects results. That lineage explains the word's connotation precisely: a harness is *not* the interesting part. It's the rig around the interesting part.

And before software, it's horse tack: the straps and fittings that connect an animal to a cart. Which turns out to be an unusually good metaphor, because it maps cleanly onto the trichotomy above — **the horse is the model, the straps and cart are the harness, and the team actually pulling a load down the road is the agent.**

**"Agent" comes from classical AI and economics**, both of which took it from the Latin *agere*, "to do" — the same root as *act*, *agenda*, *agile*. In classical AI it's the textbook definition: something that perceives its environment and acts upon it. In economics it's the actor in a principal–agent relationship — someone acting on another's behalf, whose incentives may not match the principal's.

That second lineage is quietly the more useful one. Every hard problem in agent design — whether it did what you meant, whether you can verify its work, how much autonomy to grant — is a principal–agent problem, and economists have been writing about those since the 1970s.

---

## 6. Where the prebuilt SDK fits

An **agent SDK** is a prebuilt harness: a production loop extracted from a shipped product and packaged as a library. In the trichotomy it fills the **harness slot** with someone else's machinery instead of your hand-rolled loop. It isn't a model (you still choose one) and it isn't an agent (nothing acts until you call it with a goal).

Which clarified something I'd found genuinely confusing — the layers people name interchangeably are actually a stack, and the useful question is *which slot am I filling myself?*

| layer | what it is | who supplies it |
|---|---|---|
| raw model API | stateless message-in/message-out | the lab |
| your own loop | ~40 lines, above | you |
| an agent SDK | production harness as a library | the lab |
| a terminal/IDE product | that harness + a UI + defaults | the lab |

Building your own is not a competitive act against the SDK. The reason to write the 40 lines is that afterwards you can *read* the SDK, because you know what each part is compensating for.

---

## 7. There's no textbook, and that's the finding

I went looking for the canonical course or textbook on harness design. There isn't one. The field is only a few years old, and its actual canon is a couple of founding essays, a handful of sub-300-line reference implementations, one conference paper, and several production codebases you read like source-code literature.

The paper worth knowing is the one that formalizes exactly the design question — hold the model fixed, vary the tool and feedback design, and measure how much performance swings. That framing, the **agent–computer interface**, is the closest thing to an academic treatment: it treats "what should an edit tool return?" and "how much output should the agent see?" as first-class research questions rather than implementation details.

Which is a strange and useful thing to discover mid-way through learning something. Usually the frustration is that a field has a canon you haven't read yet. Here the frustration is the opposite, and it changes what "learning it" means: read the small number of primary sources, then read production code directly, because there is no secondary literature to hide behind.

---

## 8. One reading habit that came out of this

Chasing the source code took me into unfamiliar Python package layouts, and two conventions kept confusing me until I asked directly:

**`__init__.py`** — the double-underscore-wrapped names ("dunder" names) are Python's reserved namespace for things the *language* uses, not things you call. `__init__.py` marks a directory as a package and defines what `import package` exposes. It's the front door: read it first, because it's the curated public surface, and everything not re-exported there is internal.

**Leading single underscores on filenames and functions** (`_client.py`, `_helper()`) are a convention, not enforcement — "this is internal, don't depend on it." Python won't stop you. It's a promise about what may change without warning.

Together those give a genuinely useful strategy for reading an unfamiliar package: start at `__init__.py` to see what's public, follow those names into the non-underscored modules, and treat the underscored files as implementation you read only when you need to know *how* rather than *what*.

The other habit — worth more than the Python trivia — is that when I asked for the repo layout and got a confident answer that felt off, I pushed back and asked for it to actually open the repository rather than recall it. It had drifted. Structural details of a specific codebase are exactly the kind of thing that gets confidently approximated, and "go look, don't recall" is the correction that matters more than any single fact it produced.
