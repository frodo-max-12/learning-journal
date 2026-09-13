# How an Always-On Agent Stays Alive — Three Layers and a Restart Paradox

**Context:** I'd worked out conceptually that the interesting question about agent autonomy isn't "cron or events?" but "what generates the next action?" Then I found an open-source personal-agent project that's actually always-on, and read its code to see how the abstract answer looks in practice. It's neither purely scheduled nor purely event-driven — it's **three layers**, each solving a problem the layer below can't. And there's one small file in it that solves a genuinely cute paradox.

---

## 1. Layer 1 — the OS keeps the process alive

The first thing I expected to find was a supervision loop: some watchdog that checks whether the agent is running and restarts it. There isn't one.

Instead the project delegates entirely to the host operating system's service manager — a LaunchAgent on macOS, a user-mode systemd unit on Linux, a scheduled task on Windows. An install command writes the appropriate config and lets the OS handle *"if this dies, start it again."*

**The agent process does not poll or self-monitor at all.**

That's a better decision than it first looks. A self-monitoring process has an obvious hole: if it dies, the thing that would have noticed died too. Any watchdog you write inside the process is monitoring everything except the failure mode you actually care about. Every OS already ships a supervisor that runs *outside* your process, has been debugged for decades, and survives reboots. Writing your own is strictly worse.

This layer is **OS-driven event handling**: the OS fires "process died → restart it," and the agent doesn't decide anything.

---

## 2. The restart paradox, and the trick that resolves it

Here's the piece I liked most.

Sometimes the agent needs to restart *itself* — a config change, an upgrade. And **a process cannot restart itself**, because exiting and re-running are two different processes. Whatever code would do the re-running dies at exactly the moment it's needed.

The resolution: before exiting, spawn a **detached shell child** that

1. waits for the current process ID to disappear —
   ```sh
   while kill -0 "$wait_pid"; do sleep 0.1; done
   ```
2. then asks the OS service manager to start the service again.

The child is explicitly detached from the parent so the parent can die freely.

I found this genuinely delightful, and it generalizes: **when an actor can't perform an operation on itself, hand the operation to something whose lifetime outlives it.** A tiny, dumb shell script that does nothing but wait and then issue one command is more reliable than any clever in-process scheme, precisely *because* it's outside the thing being restarted.

`kill -0` is the other small pleasure — it sends no signal at all and just tests whether the process exists. A "kill" command used as a liveness probe.

---

## 3. Layer 2 — several schedulers inside one process

Once running, the process hosts **three concurrent scheduling mechanisms** side by side:

- a **cron service** for genuinely time-based work,
- a **heartbeat runner** for the periodic "is there anything to do?" pass,
- **inbound channel listeners** for externally triggered work — a message arriving, a webhook firing.

This is the concrete version of the abstract answer I'd reached before. The taxonomy isn't a menu you choose from; **a real autonomous system runs all of them at once**, because it has all three kinds of trigger. Something must happen at 9am. Something must happen when a message arrives. And something must happen "periodically, when warranted" — which is neither of the first two.

---

## 4. Layer 3 — the heartbeat as mediator

The heartbeat is the layer that maps onto the thing I'd concluded was missing from most agents: the continuous goal-pursuit loop that runs *between* external events.

It's a first-class concept in the codebase, spread across dozens of files, and its job is to **mediate all the different ways an agent can be woken** — turning scheduled ticks, external events, and self-initiated wake-ups into one uniform "something might need doing" pass.

That mediation role is the design insight. Without it, every trigger type would need its own path into the agent's decision logic, and each would drift. With it, there's exactly one place where "the agent considers acting" happens, and the trigger sources are interchangeable inputs to it.

Which also means you can add a new kind of trigger without touching the decision logic — the property you'd want, and the one you only get by having built the mediating layer first.

---

## 5. The stack, and why each layer is necessary

| layer | who drives it | the problem it solves | why the layer below can't |
|---|---|---|---|
| OS service manager | the OS | keeping the process existing at all | a dead process can't restart itself |
| in-process schedulers | the process | firing work at the right times | the OS doesn't know your domain schedule |
| heartbeat runner | the agent | deciding whether to act | a scheduler fires; it doesn't judge |

Read bottom-up, that's a clean separation: **existence**, then **timing**, then **judgment.** Each layer is dumb about the concerns of the layer above and reliable about its own.

And it explains something that had puzzled me about the difference between an agent and a cron job. A cron job has layers one and two and *no layer three* — it fires and executes, unconditionally. The heartbeat layer, where something wakes up and decides whether the situation warrants acting, is the entire difference. It's also where the expensive model call lives, gated by cheap deterministic code — the same conclusion I'd reached from the cost model, arrived at here from an architecture diagram.

---

## 6. Reading strategy that made this tractable

One thing worth recording about method, because the codebase was large and this made it manageable:

**Read the small files first.** In a well-structured project, the small files hold the *contracts* — interfaces, type definitions, the shape of the thing. The large files hold implementation and boilerplate. Reading every small file plus the opening of each large one gives you the architecture at a fraction of the reading.

And **grep for the concept name before theorizing.** I could have guessed how "always-on" was implemented and written something plausible. Searching for the term found roughly forty files organized around it as a first-class concept, which immediately told me it was central rather than incidental. The volume of code attached to a name is itself information about the design.

---

## 7. What I took away

**Delegate liveness to something that outlives you.** True of the OS supervising a process, true of the detached shell child performing the restart, and true of durable state outliving an ephemeral context. Same shape three times: the thing responsible for recovery must not be the thing that fails.

**The taxonomy was a false choice.** Scheduled, event-driven, and continuous aren't alternatives — a real system runs all three and needs a mediating layer so they converge on one decision point.

**"How does it stay alive?" is a better question than "how does it work?"** for anything long-running. The interesting engineering is in the failure and recovery paths, and those are exactly the parts you never see while it's working.
