# Neurosymbolic AI — Type 1 vs. Type 2 abstraction

*Learned in April 2026. A Gary Marcus tweet linking to a Francois Chollet lecture slide, combined with what David Deutsch says about explanatory knowledge, triggered a conversation that connected three ideas I had been thinking about separately. The result was the clearest mental model I have found for how AI systems should be architected — and specifically, how MegaFuse should be built.*

---

## Two ways a mind can abstract

Chollet's framework divides abstraction into two types, and once I understood them, I started seeing the distinction everywhere.

**Type 1 — prototype-based, neural.** This is abstraction by averaging. You see a thousand faces and your brain builds an "eigenface" — a blurry composite that represents the category "face" without being any specific face. Current LLMs work this way. They have seen billions of examples and built incredibly rich prototype spaces. Ask one "what is a semiconductor?" and it gives you a fluid, context-appropriate answer synthesized from everything it has absorbed. This is powerful. It is also fundamentally fuzzy. There is no discrete procedure being followed — just a high-dimensional statistical average being navigated.

**Type 2 — program-based, symbolic.** This is abstraction by finding a discrete procedure that generalizes. Instead of a blurry average, you get a function: `process_item(x)`. It has explicit steps, explicit branches, and it either applies to a new case or it does not. There is nothing fuzzy about it. A for-loop that iterates over a list is Type 2. A pricing formula is Type 2. An if-then-else tree with 486 branch points is Type 2.

The key difference: Type 1 interpolates within what it has seen. Type 2 can extrapolate to genuinely novel cases because the procedure is abstract — it works on any input that fits its specification, not just inputs that resemble past data.

| Dimension | Type 1 (Neural) | Type 2 (Symbolic) |
|---|---|---|
| How it abstracts | Averaging across examples | Extracting a generalizable rule |
| Representation | Continuous, distributed | Discrete, structured |
| Strength | Handles ambiguity, fuzzy inputs | Guarantees correctness, traces logic |
| Weakness | Cannot explain its reasoning | Brittle when inputs are messy |
| Analogy | Recognizing a face in a crowd | Following a recipe step by step |

## Where David Deutsch deepens the picture

In *The Beginning of Infinity*, Deutsch argues that genuine knowledge creation requires **conjecture and criticism** — not induction from data. A hard-to-vary explanation is not a statistical average of past observations. It is a theory: a compact, causal model that could be wrong and can be tested. That is fundamentally Type 2. It is a discrete structure with moving parts where you can swap inputs and trace consequences.

This connection hit me hard. Type 1 alone can never produce a new explanation — it can only interpolate within existing knowledge. Type 2 is where genuine creativity happens, in the Deutschian sense. No amount of Type 1 sophistication gets you to universality. You can have an arbitrarily good interpolation engine and it still will not *explain* anything. Explanation requires a qualitatively different process — one that generates new conjectures that go beyond the data.

The practical takeaway: current LLMs are very sophisticated Type 1 machines. They approximate Type 2 reasoning by pattern-matching against similar programs they have seen in training data. This works surprisingly often, but breaks on truly novel abstractions. It is why Chollet keeps insisting that scaling LLMs alone will not reach AGI — and why his ARC benchmark (which tests whether a system can infer a novel rule from a few examples) remains unsolved by pure neural approaches.

## What neurosymbolic AI actually means

This is where it became concrete. Gary Marcus pointed to a real artifact: Claude Code's `print.ts` file — 3,167 lines of deterministic pattern-matching code with 486 branch points and 12 levels of nesting. Pure if-then-else logic. No neural network, no probabilities. Classical symbolic AI. And it sits right next to the LLM that handles the "understanding what the user wants" part.

That combination — neural system for perception and intent, symbolic system for execution and formatting — is neurosymbolic AI. Two subsystems with fundamentally different architectures working together.

**The neural part** (Type 1): the LLM itself. Trained on massive data, excellent at fuzzy pattern recognition, generating plausible text, understanding intent, handling ambiguity. But probabilistic, which means it sometimes hallucinates or gets details wrong.

**The symbolic part** (Type 2): deterministic, handcrafted rules. If the output is a Python file, format it this way. If the user asked for a diff, structure it that way. No probability involved. Just rigid logic trees that guarantee correctness for known patterns. Anthropic's engineers decided that for something as critical as how code gets rendered and presented, you cannot leave it to the LLM's probabilistic judgment. You write explicit rules.

Marcus has been arguing since at least 2001 that pure neural networks are insufficient — you need symbolic reasoning too. He sees Claude Code as proof that the industry is quietly conceding his point. The best-performing AI product is not pure deep learning; it is deep learning wrapped in classical symbolic scaffolding.

Where Marcus oversells it slightly: calling `print.ts` "neurosymbolic AI" is generous. It is really just good software engineering — wrapping an unreliable component in deterministic guardrails. True neurosymbolic AI in the research sense involves the neural and symbolic systems *learning together*, not just one checking the other's homework. DeepMind's AlphaProof, for instance, uses an LLM to conjecture formal mathematical statements and then a symbolic theorem prover to verify them — a much tighter integration where each system genuinely needs the other.

But the broader point stands: the path forward is not "just scale the LLM."

## What the code actually looks like

I wanted to see a real neurosymbolic system, not just read about one. The clearest example I found was the MIT-IBM Watson Visual Question Answering system. The scenario: you show the system an image with colored shapes and ask "What color is the shape closest to the blue circle?" The system needs to *see* the image AND *reason* about spatial relationships.

Three components, each mapping cleanly to the framework:

**`perception.py` — the neural part.** A convolutional neural network that looks at raw pixels and outputs a structured scene representation: "there is a red circle at position (50, 80), a blue rectangle at (120, 40)." Pure pattern matching. Probabilistic. Learned from data. This is Type 1 — perception.

**`semantic_parser.py` — the bridge.** A sequence-to-sequence transformer that takes the natural language question and converts it into a program. "What color is the shape closest to the blue circle?" becomes: `filter blue -> filter circle -> relate closest -> query color`. Still a neural network, but its output is symbolic — a sequence of function calls. This is where Type 1 hands off to Type 2.

**`program_executor.py` — the symbolic part.** A Domain Specific Language with deterministic functions: `filter_` (subset the scene by attribute), `query` (look up a property), `relate` (find closest/furthest object), `count`, `isLeft`, `isTop`. These are pure if-then-else operations. No neural network, no probability, no learning. The executor takes the program from step 2 and runs it against the scene from step 1, step by step, deterministically.

The neural net says "I see shapes." The symbolic executor says "I *know* what 'closest' means — it is `argmin(distances)`." No amount of training data teaches you what "closest" means as rigorously as a distance function does. That is Deutsch's point: the distance function is an explanation, not a statistical correlation. It is hard-to-vary — you cannot subtly tweak it and still have it work.

> The pattern is always the same: neural network for perception and understanding, deterministic program for reasoning and execution. The neural side handles the messy real world; the symbolic side handles the precise logic.

## What this means for MegaFuse

This is where the conversation became personally actionable. MegaFuse is a cross-border B2B semiconductor marketplace I am building — it involves parsing messy BOMs, interpreting RFQ emails, looking up prices from APIs, and making buy/sell decisions. The question was: where in this system should Type 1 live, and where should Type 2 live?

The answer crystallized into a simple architectural principle:

```
MESSY WORLD --> [Type 1: Parse/Perceive] --> STRUCTURED DATA --> [Type 2: Reason/Execute] --> ACTION
```

**Type 1 at the boundaries.** BOMs come in wildly inconsistent formats — different column names, merged cells, part numbers mixed with descriptions, manufacturer names abbreviated in a dozen ways. An LLM is the right tool to take messy, unstructured BOM data and extract structured fields: MPN, manufacturer, quantity, target price. No amount of if-then-else covers every BOM format. This is a perception problem. The same applies to RFQ email interpretation and demand signal detection — fuzzy pattern recognition over noisy inputs.

**Type 2 at the core.** Pricing logic is deterministic math: `if (buy_price * 1.3 < sell_price) AND (margin > threshold) AND (quantity_available >= quantity_requested)`. Inventory state is a database query, not a neural prediction. Trade execution rules are explicit conditionals: if lead time advantage exceeds X weeks, if competitor stock is zero, if demand signal is rising, then execute. P&L tracking is arithmetic. Never neural.

The four-layer architecture:

- **Layer 1 (Ingestion):** Mostly Type 1. BOM parser, email parser, messy-data cleaners.
- **Layer 2 (Intelligence):** Type 1 spots patterns ("this SKU is appearing in 3x more BOMs this month"). Type 2 scores and ranks them: `score = demand_velocity * margin_potential * supply_scarcity * lead_time_advantage`.
- **Layer 3 (Execution):** Pure Type 2. Buy/sell decisions, quantity calculations, risk limits, auto-quoting. All deterministic.
- **Layer 4 (Feedback):** P&L is Type 2 arithmetic. Analyzing why a trade worked or failed is a periodic Type 1 reflection task.

The key principle, and the one I keep coming back to:

> Never let Type 1 make a financial decision. Let it perceive, let it suggest, let it flag. But the moment money moves, Type 2 takes over.

My COVID proof-of-concept — spotting five SKUs nobody had in stock and fulfilling them at three-day lead time — was me performing both types in my head. The Type 1 was reading 200+ BOMs and intuitively sensing which parts were hot. The Type 2 was the explicit reasoning: zero stock everywhere plus active demand plus I have a source equals arbitrage. MegaFuse needs to separate these into distinct subsystems so the Type 1 part scales (I cannot read 200 BOMs a day forever) while the Type 2 part stays precise (I do not want a probabilistic system deciding my margin threshold).

## The broader lesson

The Chollet-Deutsch-Marcus convergence is this: intelligence requires both perception and explanation. Current AI is extraordinary at perception and terrible at explanation. The systems that work best in production — Claude Code, AlphaProof, the MIT Visual QA system — are the ones that honestly acknowledge this and architect accordingly, rather than pretending one type can do everything.

For anyone building with AI, the design question is not "should I use an LLM?" It is "where in my system do I need fuzzy perception, and where do I need deterministic reasoning?" Get that boundary right and the architecture follows naturally.

---

*What I studied next: the ARC benchmark and how it specifically tests Type 2 generalization. Also started mapping every MegaFuse module to Type 1 or Type 2 as part of the architecture design.*
