# State — the concept behind all of computing

**Context:** While studying the [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) orchestration code, I kept seeing the word "state" — `AgentState`, `process state`, `React state`, `port state (LISTEN)`. I realized I'd bumped into this concept in almost every learning journal entry without understanding what it actually means. So I asked: who invented state, what problem were they solving, and can you do without it?

---

## 1. The simplest definition

**State is "the current situation" of anything.**

The word means the same thing it does in everyday English. Water can be in a solid state, liquid state, or gas state. A traffic light is in a red state, yellow state, or green state. In CS: **what is true about a thing right now, that might be different later?**

---

## 2. The real-world version I already understand

Think about the family distribution business at any given moment. It has a "state":

- How much cash is in the bank account
- Which purchase orders are open
- Which shipments are in transit
- How many units of each component are in the warehouse
- Which customers have pending invoices

A customer pays an invoice → cash goes up, accounts receivable goes down. The state changed. If someone asks "what's the state of the business?" — they want a snapshot of all those numbers right now. Tomorrow, the snapshot will be different. **State is always a snapshot in time.**

---

## 3. The origin: Turing watching a human do math (1936)

The concept of state in computer science was **not an engineering choice**. It was a **discovery** about the nature of computation.

### The problem

In 1935, a 23-year-old mathematician named **Alan Turing** at Cambridge was working on a problem posed by David Hilbert called the **Entscheidungsproblem** (decision problem): is there a mechanical procedure that can tell you whether any mathematical statement is true or false?

To answer this, Turing needed to define what "mechanical procedure" even means. Nobody had a precise definition. So instead of starting with machines, he watched a human doing math.

### What Turing observed

He imagined a person — he called them a "computer" (in 1936, "computer" meant a human who computes) — sitting at a desk, working through a calculation with pencil and paper. He asked: what is this person actually doing, stripped to the absolute minimum?

He noticed three things:

**1. The person looks at symbols on paper.** At any moment, they're reading a specific part of their worksheet — a number, a partial result.

**2. The person is in some "state of mind."** Maybe they're carrying a digit. Maybe they just finished a subtraction and are about to start a multiplication. Their mental state determines what they do next.

Turing wrote:

> "The behaviour of the computer at any moment is determined by the symbols which he is observing, and his **'state of mind'** at that moment."

**3. The number of possible mental states is finite.** A human can't maintain infinitely many distinct mental modes. At any point, you're in one of a limited set — "I'm adding," "I'm carrying," "I'm checking my answer," "I'm done."

Turing wrote:

> "The number of states of mind which need be taken into account is **finite**."

### The machine

From these observations, he built his theoretical machine (later named the "Turing machine" by Alonzo Church):

| Human doing math | Turing machine |
|---|---|
| Paper with symbols | A tape with symbols |
| Eyes and pencil | A head that reads/writes one cell at a time |
| Possible mental modes | A finite set of **states** (he called them "m-configurations") |
| "If I'm carrying and I see a 7, write 1 and carry again" | Rules: "In state X, seeing symbol Y → write Z, move, switch to state W" |

**State was a discovery about what it means to follow a procedure.** You can't follow a procedure without being in some "current situation" that changes step by step. That current situation is state.

Published November 1936: *"On Computable Numbers, with an Application to the Entscheidungsproblem."* Turing was 24.

---

## 4. Why "state" and not just "memory"

This confused me at first. Memory is **what you store**. State is **what you are**.

I have memories — facts I've learned, things that happened. But my state right now is different: am I focused or distracted? In the middle of this sentence or about to switch tabs?

My memories didn't change in the last 10 seconds, but my state did — I was at the top of this journal, now I'm in the middle. I've progressed. That progression — the "where am I in this process right now?" — is state.

In Turing's machine: the tape is memory (it stores symbols). The machine's current state is which mental mode it's in. Both are needed. **Memory without state** is a filing cabinet with nobody reading it. **State without memory** is a person with amnesia who can think but can't write anything down.

---

## 5. State becomes physical hardware (1943–1956)

Turing's work was pure theory — he was solving a math problem, not building hardware. But others took his concept and made it real:

| Year | Who | What | How state shows up |
|---|---|---|---|
| 1943 | McCulloch & Pitts (neurophysiologists) | Published *"A Logical Calculus Immanent in Nervous Activity"* | Showed **neurons** work like state machines — firing or not firing, and what they do next depends on current state plus inputs |
| 1945 | John von Neumann | Wrote the *First Draft of a Report on the EDVAC* | Designed the architecture every computer uses today. The CPU has **registers** — tiny pieces of state that track the current instruction, current data, where to go next. Turing's "states" made physical in silicon |
| 1955 | George Mealy | Created the Mealy machine | Practical finite state machines for designing electrical circuits and telephone switching systems |
| 1956 | Edward Moore | Created the Moore machine | Another variant of finite state machines, used in traffic lights, vending machines, elevators |

My M5 chip (from the CS big picture journal) has registers — literally Turing's "states" etched into a 3-nanometer piece of silicon, 89 years after the original paper.

---

## 6. Why state became central to ALL of computing

Because **every interesting system in the world changes over time**, and you need state to track those changes.

| System | What changes? | The state |
|---|---|---|
| A distribution business | Orders, payments, inventory | Cash balance, open POs, warehouse levels |
| A traffic light | Cars arrive, time passes | Red / Yellow / Green |
| A phone call | Dial → ring → answer → talk → hang up | Dialing → Ringing → Connected → Ended |
| A chess game | Players make moves | Position of every piece on the board |
| The AI hedge fund | Analysts run, risk calculated, decisions made | `AgentState` — the shared whiteboard |

If nothing ever changed, you wouldn't need state. A function that computes `2 + 2 = 4` has no state — same answer every time. But the moment you add a "memory" button that stores a number, the calculator now has a "current situation" that affects future behaviour. That's state.

---

## 7. Every time I've encountered state without knowing it

Looking back through my learning journals, state was hiding everywhere:

### Process state (CS big picture journal)
`ps aux` shows a `STAT` column: `S` = sleeping, `R` = running. Every process on my Mac is in a state. The OS uses this to decide what to do: "PID 425 is sleeping, skip it. PID 891 is running, give it CPU time."

### Port state (ports journal)
When I ran `lsof -i :8000` and saw `TCP localhost:irdmi (LISTEN)` — that `LISTEN` is a state. The port is waiting for connections. Other states: `ESTABLISHED` (active connection), `CLOSED` (nobody home).

### React state (frontend journal)
I wrote this definition myself: *"State: Data in a component that can change over time and triggers re-rendering."* When React says `useState`, it means: "I'm declaring a piece of data that will change, and when it changes, redraw the screen."

### AgentState in the hedge fund
The "whiteboard" in `src/graph/state.py`:

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    data: Annotated[dict[str, any], merge_dicts]
    metadata: Annotated[dict[str, any], merge_dicts]
```

At the beginning, `analyst_signals` is empty. After 18 analysts run, it has 18 entries. After the risk manager, 19. The state evolved over time — each agent reading the whiteboard and adding to it.

### Portfolio state
```python
portfolio = {"cash": 100000, "positions": {"NVDA": {"long": 0, "short": 0}}}
```

The same as "what's the state of the business?" — how much cash, what positions. After buying 8 shares of NVDA, cash goes down, `long` goes to 8. State changed.

**Same concept, five completely different contexts.** That's why it's fundamental.

---

## 8. Why state management is the hard problem of programming

When nothing changes, programming is easy. A function that converts Celsius to Fahrenheit — `f = c * 9/5 + 32` — has no state. Give it 100, always returns 212. Simple, predictable, never breaks.

But the moment data changes over time, four hard problems appear:

### Problem 1: "What's the current value?"
If 18 agents write to the same whiteboard at the same time, what happens if two write at the exact same instant? This is why the hedge fund uses `merge_dicts` — a rule for how simultaneous writes get combined.

### Problem 2: "What was the value before?"
Portfolio was `cash: 100000`, now it's `cash: 90400`. When did it change? Why? Can we undo it? Tracking history of state changes is an entire field of engineering.

### Problem 3: "Who else is looking at this value?"
If the portfolio manager reads analyst signals while an analyst is still writing, it might see a half-finished signal. This is called a **race condition** — one of the most notorious bugs in programming.

### Problem 4: "How do we keep it consistent across many places?"
My Gmail inbox runs on thousands of servers. If I read an email on my phone, the "unread" state needs to update on all of them. If it's "unread" on one server and "read" on another, that's **inconsistent state** — users see weird bugs like an email appearing twice or a notification that won't go away.

Every one of these problems has generated entire subfields of computer science.

---

## 9. Two categories of state

### In-memory state (temporary)
Lives in RAM. Fast, but disappears when the program stops.

| Example | The state | Lifetime |
|---|---|---|
| `AgentState` in the hedge fund | Analyst signals, portfolio | One run |
| React `useState` | A counter, a toggle | While the page is open |
| A Python variable `x = 5` | The value 5 | While the script runs |
| Process state (`R`, `S`) | Running or sleeping | While the process exists |

### Persistent state (permanent)
Lives on disk. Survives restarts.

| Example | The state | Lifetime |
|---|---|---|
| `.env` file | API keys | Until manually changed |
| `hedge_fund.db` | Saved flow runs | Until deleted |
| Git history | Every version of code | Forever |
| My learning journal files | What I've learned | Forever |

The engineering question is always: **should this state be in-memory or persistent?** Analyst signals are in-memory — you don't need old ones. Portfolio history is persistent — you want to track past performance.

---

## 10. Stateful vs Stateless

Two words I'll hear constantly:

**Stateless** = "I don't remember anything between calls." Like a calculator: punch in numbers, get answer, no history.

```python
# Stateless — same input always gives same output
def celsius_to_fahrenheit(c):
    return c * 9/5 + 32
```

The hedge fund's `calculate_intrinsic_value()` is stateless. Give it financial data, it returns a number. It doesn't remember the last stock it analyzed.

**Stateful** = "I remember what happened before, and it affects what I do next."

The portfolio manager is stateful. It checks "do we already hold NVDA shares?" before deciding whether to buy more. Same analyst signals, different decision — because the state was different.

**Why this matters:** Stateless things are easy to reason about, test, and scale. Google can run 1000 copies of a stateless function and they all give the same answer. Stateful things need all copies to agree on the current state — that's hard.

---

## 11. Can you do without state?

### The mathematical answer: Yes.

In the **same year** as Turing (1936), **Alonzo Church** at Princeton published a completely different approach called the **lambda calculus**. No state at all. No machine, no tape, no "current configuration." Just functions that take inputs and produce outputs, and functions that operate on other functions.

Church and Turing proved that both systems are **equally powerful** — anything computable with Turing's stateful machine is computable with Church's stateless functions. This is the **Church-Turing thesis**.

This led to **functional programming** — writing programs as chains of pure functions:

```
input → function A → function B → function C → output
```

No variable ever changes. No "current situation" exists. Languages like **Haskell** and **Erlang** are built on this. Even in Python and JavaScript, the `.map()`, `.filter()`, `.reduce()` patterns from my frontend journal are functional ideas that avoid state.

### The practical answer: Not entirely.

A program that never changes anything is useless. At some point, the real world must change:

- A pixel on screen must go from black to white
- A file must be created on disk
- A network packet must be sent
- A row must be written to a database

These are all state changes. You can avoid state inside your logic, but **at the boundaries where your program touches the real world, state is unavoidable.**

The functional programming strategy: push state to the edges. Keep 95% of code as pure stateless functions. Handle messy state changes in a thin outer layer.

The hedge fund does exactly this. The scoring functions (`calculate_intrinsic_value`, `calculate_owner_earnings`) are stateless — same input, same output. But the system as a whole is stateful — `AgentState` accumulates signals, the portfolio tracks positions. **Stateless pieces plugged into a stateful system.** That's how most real software works.

---

## 12. The deepest "why"

**State is important because time is important.**

If the universe were frozen — nothing ever changed — you wouldn't need state. Describe everything once and be done. But reality isn't frozen. Events occur in sequence. Causes lead to effects. The present is different from the past.

State is how computers track the passage of time and its consequences. When Turing watched a human doing math, he noticed that the person's mental state changed with each step. Each step depends on the previous one. You can't skip step 3 and jump to step 7, because step 7 depends on what step 3 produced.

David Deutsch (from my CS big picture journal) places computation alongside physics as a fundamental strand of reality. Computation — and therefore state — mirrors the structure of the physical universe: things change, and what they change into depends on what they are now.

> **State is the concept that lets computers participate in a world where things change.**

Without it, you have a calculator that answers one question and forgets. With it, you have a system that can track a business, manage a portfolio, remember a conversation, play a chess game, or run 18 AI analysts in parallel and combine their judgments into a trading decision.

---

**Sources:**
- [Stanford Encyclopedia of Philosophy — Turing Machines](https://plato.stanford.edu/entries/turing-machine/)
- [Turing's Landmark Paper of 1936](https://www.philocomp.net/computing/turing1936.htm)
- [History of Information — Turing's "On Computable Numbers"](https://www.historyofinformation.com/detail.php?id=619)
- [Wikipedia — Finite-state machine](https://en.wikipedia.org/wiki/Finite-state_machine)
- [Wikipedia — Von Neumann architecture](https://en.wikipedia.org/wiki/Von_Neumann_architecture)

**What I studied next:** Back to the AI hedge fund orchestration — understanding how `LangGraph` manages state transitions as agents run in parallel → see `from-broken-config-to-buffett-dcf.md` in the [ai-hedge-fund-learnings repo](https://github.com/frodo-max-12/ai-hedge-fund).
