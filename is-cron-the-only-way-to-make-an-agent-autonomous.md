# Is Cron the Only Way to Make an Agent Autonomous?

**Context:** I asked what I thought was a yes/no question — cron is the only way to make an agent autonomous, right? The answer was no, and the list of alternatives was useful. But the follow-up question I asked next turned out to be the interesting one: *what do humans use?* We're awake all day; are we event-based or time-based? That question dissolved the taxonomy I'd started with, and replaced it with a better axis.

---

## 1. The taxonomy I got first

Autonomy mechanisms sort into three families, and the useful thing is that the right choice is determined by the *trigger you actually have*, not by preference.

**Time-triggered** — cron, launchd, CI schedules, a scheduled agent run, or an in-session loop on a fixed interval. The clock fires; the agent wakes.

**Event-triggered** — hooks that fire on tool events, prompt submission, or session end. Webhooks from an external system. File watchers. Something happens; the agent wakes.

**Long-running / continuous** — a custom event loop in your own process, or background workers. Nothing external fires; the process is simply always up.

The selection rule:

| your trigger | the mechanism |
|---|---|
| "every N minutes / at 09:00" | cron or a scheduled run |
| "when an email arrives / a file changes / a webhook fires" | hooks or a webhook trigger |
| "keep iterating until it's done, no fixed interval" | a self-paced loop |
| "run forever, react to many event types" | your own SDK loop |

That's a complete and practical answer. It's also the answer that made me ask the next question, because *none of those descriptions sounded like being a person*.

---

## 2. The question that broke the taxonomy

I'm awake ~16 hours a day and I don't feel like a cron job. So which one am I?

The first correction is a small one: humans aren't always-on. Sleep is a mandatory ~8 hours in 24, which is very much scheduled. We're not even a pure daemon.

The real answer is that we're **all of them stacked**:

| layer | in human terms | agent analogue |
|---|---|---|
| event-driven I/O | sound, touch, sudden motion — attention switches | hooks, interrupts |
| time-driven maintenance | circadian sleep/wake, hunger, ~90-min ultradian focus cycles, hormonal pulses | cron |
| continuous goal-pursuit | the internal monologue that keeps driving action with zero external trigger | a self-paced loop |
| background workers | breathing, heartbeat, digestion, immune system | spawned once, run forever |

Laying it out that way immediately identified the gap. The thing current agents most lack isn't cron and isn't hooks — **it's the continuous goal-pursuit loop that keeps running between external events.** Almost every deployed agent is dormant until something pokes it. Nothing in the standard toolkit corresponds to "sitting there, thinking about what you're trying to achieve."

---

## 3. The better axis

Pushing further produced the reframe that made the whole question worth writing down.

The brain is not polling, and it is not purely interrupt-driven either. On the predictive-processing view, it runs a continuous generative model that *predicts* incoming sensory and internal input. "Events" are **prediction errors** — the gap between what the model expected and what arrived. Attention gets allocated where the model is most surprised, weighted by how much you currently care.

So the right axis isn't event-vs-time. It's:

> **What generates the next action?**

| system | what generates the next action |
|---|---|
| cron | a clock fires |
| event-driven | an external signal fires |
| humans | a continuously-running world-model fires when reality diverges from its prediction, biased by an active goal stack |

That's a genuinely different design. Cron is a thermostat by comparison — and I mean that precisely, not dismissively: a thermostat is a fine machine, it just has no model of the room and no goals beyond one setpoint.

---

## 4. What that looks like as an actual loop

The engineering translation is short, and the shape of it is the point:

```python
while True:
    obs      = observe()               # poll inputs — cheap, no model call
    expected = world_model.predict()   # what state did we expect?
    surprise = diff(obs, expected)

    if surprise > threshold or goal_stack.demands_now():
        wake()                         # invoke the model — expensive
    else:
        sleep_short()                  # 30s – 5min idle

    if time_to_consolidate():
        consolidate()                  # periodic batch
```

The key principle, and the reason this is an architecture rather than a trick:

**The model is the expensive, sparingly-invoked layer.** Most of the agent is boring deterministic code. The model gets allocated only when surprise or goals demand it — which is, not coincidentally, roughly how attention works in the analogy that generated the design.

Five components fall out of it:

1. **Observation layer** — ordinary code. Poll an inbox, hit APIs, read files, listen on a webhook. Emits structured facts. Zero tokens.
2. **World-model state** — an external store (SQLite, JSON, whatever). Expected values, open items, predicted response windows. **Not** in the context window; read and written through tools.
3. **Surprise detector** — also ordinary code. Diffs and thresholds. "This moved more than 5%." "No reply inside the expected window." "Deadline within 48 hours." This is the *gate* in front of the expensive call.
4. **The wake** — the actual model invocation, handed the current observation, the expectation, a summary of the surprise, the goal stack, and the available tools. It decides: ignore, update the model, act, or spawn a sub-goal.
5. **Tools** — the actions it can take, each with an explicit schema, each logged.

And then the part I didn't expect to be load-bearing: **consolidation**, the sleep equivalent. A periodic batch job that compresses the observation log into long-term storage, updates the priors in the world model, retires stale goals, and sets the next period's priorities.

I initially read "sleep equivalent" as a cute analogy. It isn't. Without it, the world model's priors never update and the goal stack only grows — the agent accumulates state it never digests, which is a specific and predictable failure mode rather than a metaphor.

---

## 5. What I actually took from this

**The mechanism question was the wrong question.** I asked "cron or something else?", which is a question about *how the wake-up happens*. The design question underneath is *what decides that a wake-up is warranted* — and that's answered by a world model and a goal stack, both of which live outside the model context entirely.

**Most of an autonomous agent should be deterministic code.** This inverts the naive picture, where the model is the system and the code is glue. The observation layer, the state store, and the surprise detector are all plain programs. The model is a costly subroutine you call when a cheap program has decided it's worth it. That's an economic argument as much as an architectural one — every wake-up has a price, so the gate in front of it is doing real work.

**"Always on" and "always thinking" are different claims.** A process can be up permanently and still be a thermostat. The gap between the agents I can build today and the thing I was actually imagining when I asked the question is the persistent goal stack — an intention that survives between wake-ups and biases what counts as surprising.

Which is a much more interesting problem than picking a scheduler, and I would not have found it by asking about schedulers.
