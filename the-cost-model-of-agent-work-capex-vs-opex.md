# The Cost Model of Agent Work — When to Write a Script Instead of Thinking

**Context:** I asked an agent to walk me through a directory it had generated for me, step by step — which parts were done by the model and which by plain Python — because I wanted to achieve the same result using fewer tokens next time. The walkthrough described one script as "zero cost to run, but expensive to author," and I stopped on that phrase. I didn't know what it meant, and unpacking it gave me the clearest model I have for when an agent should write code versus just do the work.

---

## 1. The distinction I was missing

A script inside an agent-orchestrated pipeline has **two distinct token costs, and they live in different moments:**

- **Authoring cost** — the tokens spent the first time the model wrote *and debugged* the script. **Paid once.**
- **Runtime cost** — the tokens spent each time the script runs. For a pure Python script invoked through a shell, this is **effectively zero** — the model just sees "exit code 0."

I'd been thinking about token cost as a single number attached to a task. It's two numbers with completely different behaviour over time: one is capital expenditure, the other is operating expenditure.

---

## 2. What actually drives authoring cost

Three things, and they multiply rather than add.

**Input tokens spent understanding the problem.** To write a parser for messy semi-structured records, the model had to *read the raw records* to discover that the source used around twenty different layouts. Every time the parser hit an unfamiliar shape and dropped rows, another batch of failing examples had to be pulled into context to work out what the new shape was.

**Output tokens spent writing code.** Several hundred lines of Python is thousands of output tokens — plus revisions, since each new handler means re-emitting nearby code.

**Iteration cycles — the multiplier.** The parser was built over many rounds: write → run → see "57% unparsed" → read the failures → add a handler → re-run → "32% unparsed" → read more → add more. Each cycle is its own input-plus-output round trip.

The contrast between two scripts in the same directory made it concrete:

| | the parser | the analyzer |
|---|---|---|
| lines of code | ~850 | ~270 |
| input complexity | 20+ chaotic layouts inside raw human-written text | 3 clean CSVs with known headers |
| debug cycles | many — each new shape is a new cycle | 1–2 |
| sample data read into context | a lot — had to eyeball failures to invent each classifier | almost none — the schema is in the code |
| **authoring cost** | **~30–50K tokens** | **~5–10K tokens** |
| **runtime cost per run** | **~0** | **~0** |

Same runtime profile. Roughly a fivefold difference in one-time creation cost.

And the driver is visible: **authoring cost tracks how much of the input's messiness had to enter the context window.** Clean, schema'd input is cheap to write code for. Chaotic input is expensive, because discovering the chaos *is* the work, and discovery happens by reading.

---

## 3. Capex versus opex

Once framed that way, the decision rule falls out.

**Authoring cost amortizes across reruns.** A 50K-token script that runs 20 times costs 2.5K tokens per run.

**The break-even point arrives faster than you'd think.** If doing the same parse inline would cost ~20K tokens per refresh — reading the records, reasoning, emitting output — then a 50K-token authoring effort pays for itself **after three runs.**

**And there's a case where you should actively resist writing a script:** one-shot transforms. If you'll do this exactly once and never again, the authoring cost is pure overhead. Just have the model do it inline.

The mental model I took away:

> **The model writes code so that it doesn't have to think about the same problem twice.**

Every token spent authoring is a permanent reduction in the per-run cost. It's the same logic as compiling versus interpreting: pay once to translate the problem into a form that executes without further reasoning.

---

## 4. Why this is a real design principle, not just budgeting

What makes this more than an accounting curiosity is that **the cheap thing and the reliable thing are the same thing.**

A deterministic script does the identical thing every run. Model reasoning over the same input produces *similar* output, not *identical* output. So the move from "the model does it each time" to "the model wrote something that does it each time" buys reproducibility at the same moment it buys cost.

It also explains a pattern I'd noticed and not understood in well-built agent pipelines: they tend to look like **a thin layer of model reasoning wrapped around a thick layer of ordinary code.** That isn't the model being underused. It's the equilibrium the cost model predicts — anything done more than a handful of times migrates into code, and what's left for the model is the part that's genuinely different each time.

Which lines up exactly with the autonomy architecture I'd worked through separately: observation, state, and change-detection as plain programs, with the model as an expensive subroutine invoked when a cheap program decides it's warranted. Same conclusion reached from two directions — one from *what generates the next action*, this one from *what does it cost per run*.

---

## 5. The heuristic I now use

Before asking an agent to do a data task, ask two questions:

**How many times will this run?** Once → do it inline, skip the script. Three or more → write the script, even if authoring looks expensive. The break-even is low.

**How messy is the input?** This predicts authoring cost more than output complexity does. Clean input with a known schema is cheap to write code against. Chaotic input is expensive, because the model has to *read a lot of it* to discover the shape — and that reading is the bill.

There's a corollary worth stating: **cleaning the input is often cheaper than writing a parser that tolerates the mess.** If you can impose structure upstream, you're not saving parser complexity, you're saving all the discovery reading that would otherwise be needed to learn the mess.

---

## 6. What I took away

**"Expensive" needed a time dimension.** I'd been asking "does this cost a lot?" without asking "once, or every time?" Those are different questions with different answers and different fixes.

**Reading is the hidden cost.** I'd assumed writing code was the expensive part, since that's what's visible in the output. It's the *input* side — pulling failing examples into context, batch after batch, to discover the shape of the problem — that dominates. Output tokens are the small half.

**The right question isn't "how do I use fewer tokens," it's "what should be permanent."** Every problem an agent solves twice is a problem it should have written down as code the first time. That reframes the whole budget question from restraint into a straightforward capital-allocation decision.
