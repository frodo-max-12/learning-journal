# A Global Workspace in a Model, and Deutsch's Three Kinds of Ideas

**Context:** I read some interpretability research describing a "global workspace" inside a language model — a place where information gets broadcast and made available to the rest of the system — and it struck me immediately as Deutsch's taxonomy of ideas: conscious explicit, conscious inexplicit, unconscious. I proposed a mapping between the two and asked whether it held. It half held. The correction was interesting, and the second question I asked turned out to rest on a premise Deutsch explicitly rejects — which was the most valuable thing in the whole exchange.

---

## 1. The two frameworks

**Deutsch's trichotomy** distinguishes three kinds of ideas:

- **Explicit** — expressible in language, and *language-shaped while you're having them*.
- **Conscious inexplicit** — you're aware of them, but they aren't in words. His example: a tennis player's theory of where the ball will land.
- **Unconscious** — no awareness at all, still doing necessary work.

**The interpretability finding** is that a model has an identifiable workspace whose contents are broadcast and reusable, distinguishable from local processing that isn't.

And one detail makes the parallel almost uncanny. **Deutsch's favourite example of inexplicit knowledge is grammar** — we have inexplicit rules regulating speech, and if asked to state them we either can't or state them wrongly. The interpretability result: delete the workspace contents and the model **keeps speaking grammatically.** Fluency, grammar, and automatic recall never route through the workspace; multi-step reasoning dies without it.

An armchair epistemological example from decades ago showing up as an intervention result in a neural network is the kind of convergence that makes me want to take both more seriously.

---

## 2. My mapping, and the correction that matters

I proposed: the workspace is the conscious explicit layer, and the model's emitted words are explicit ideas — like the tennis player who can later say "I thought it would land there."

**The output half is right. The tennis half contains a real error.**

For Deutsch, what makes an idea explicit is *not* that it can later be put into words. It's that the idea is **language-shaped while you are having it.** He's careful about this: when the player says afterwards "I thought it was going to land there," that sentence is a **new conjecture about** what the inexplicit theory was — and *you might be wrong about what your inexplicit theory was.*

The later verbalization doesn't retroactively make the trajectory-theory explicit. It's a fallible translation.

And if later-verbalizability counted as explicitness, **the inexplicit category would nearly vanish**, since almost anything can be conjectured about in words after the fact. My mapping would have quietly collapsed a three-way distinction into a two-way one.

The resolved version is that the workspace isn't one rung of the ladder — it's the **container**, and the ladder describes what's inside it:

| in the model | Deutsch's category |
|---|---|
| emitted tokens | explicit, expressed |
| workspace contents the lens can read (word-shaped) | explicit, *not yet expressed* — inner speech |
| workspace contents the lens can't read (no word-shaped form) | conscious inexplicit — the real tennis-ball analogue |
| local processing (grammar, fluency, automatic recall) | unconscious |

And there's a twist. The reported workspace runs almost entirely out of words, so **most of its contents are the inner-speech row** — silently held *explicit* thought, not tennis-ball inexplicit thought. A human workspace holds trajectories, imagery, and motor predictions alongside inner speech. This one seems dominated by the verbal channel.

**The part of my mapping that survived is the important part**: the relationship I'd noticed is real. Workspace → output is a lossy, reconstructive translation, exactly like inexplicit thought → later verbal report. When the model reports on an injected concept, that report can confabulate — the same epistemic situation as the tennis player's post-hoc account.

There's a lovely self-referential point buried here too. The interpretability lens reads out word-shaped patterns, so it *cannot see* concepts with no word-shaped form. **The lens is to the model what verbal introspection is to us — with the same failure mode.** The tool for making a system's knowledge explicit inherits exactly the limitation language has for our own inexplicit knowledge.

---

## 3. The question that had a false premise

My second question: Deutsch says we need to make ideas explicit so they can interact and be error-corrected — so why can't error correction happen directly on the unconscious ones?

**He says the opposite, and the tennis example is his proof.** The player is "creating a theory about where the ball's going to strike, then correcting the theory, and doing all the things error-correcting thinking does *without expressing it in sentences or words*." Solving a real problem, on his account, requires unconscious conjecture *and* inexplicit conjecture *and* explicit conjecture — and the same for criticism, at all three.

That's the Popperian move applied consistently: **the same epistemology — fallible conjecture, criticism, no justification — operates at every layer.** Ideas at all three levels evolve under selection pressure from each other and from outcomes.

And mechanically privileging the explicit layer is a position he specifically calls *irrational* — judging theories by their type rather than their content.

The modern existence proof is sitting right there, which is what made this click: **gradient descent.** The model's grammar was error-corrected into existence by billions of criticisms applied directly to unconscious structure, without the rules ever being explicit anywhere. That's Deutsch's grammar point run in reverse — not "we can't state the rules we use," but "the rules were learned, and corrected, and were never stateable at any point."

---

## 4. So what does explicitness actually add?

If every layer self-corrects natively, the interesting question is what making something explicit *buys* — which is a much better question than the one I asked.

**Logic becomes available.** Explicit ideas can be combined by rules of inference. You can hold two of them side by side and notice they contradict. An inexplicit theory can be *wrong*, and revised by feedback — but it can't be shown to be *inconsistent with another one*, because there's no shared form in which to place them next to each other.

**Criticism becomes shareable.** An explicit idea can be handed to someone else, who can attack it with knowledge you don't have. Inexplicit theories are corrected only by your own outcomes, which is a far smaller error-correcting community.

**Reach extends past experience.** Feedback-driven correction of an inexplicit theory only reaches situations you actually encounter. An explicit theory can be criticized against cases you've never met, including hypothetical ones.

None of that means explicitness is *required* for error correction. It means explicitness changes the *scale and speed* of it — from private and experience-bound to social and counterfactual.

---

## 5. The architectural asymmetry, which is the real finding

Here's where the comparison stops being an analogy and says something concrete about current systems.

The model's workspace exists within a single forward pass. So its error-correction loop **must route through tokens** — the visible reasoning scratchpad is where correction happens, because there's no other channel with time to operate.

A human tennis player revises trajectory-theories **wordlessly, in flight.** The model has to verbalize every update.

Which means current reasoning models are *structurally forced* into the posture Deutsch calls irrational: dragging everything into the explicit layer, not out of philosophical error but because that's **the only layer where correction can happen at all.**

That's a real architectural claim with an empirical shape, and it reframes what the visible reasoning trace *is*. It isn't the model showing its work for our benefit. On this reading it's the model's **only available error-correction channel**, externalized because it has nowhere internal to run.

A supporting result fits neatly: instructed *not* to think about a concept, the model only partially suppresses it — which is Deutsch's claim that the explicit layer cannot coerce the others by fiat, demonstrated causally rather than argued.

---

## 6. The honest gap

The frameworks are doing different jobs, and it's worth being clear about which.

The workspace theory is **architectural** — where information sits, how it's routed. Deutsch's point is **epistemological** — the same fallibilist rules apply to all three kinds of ideas.

And the sharpest admission in the research is: *we don't know what mechanism decides what enters the workspace in the first place.*

A Deutschian would say that gate is the whole ballgame. **Deciding what gets broadcast is conjecture-selection**, and understanding it means understanding creativity, not routing. Which lands in the same place as everything else in this line of thinking: the substrate is increasingly well-characterized, and the program that selects which conjecture to entertain is still missing.

---

## 7. What I took away

**"It can be verbalized later" is not the same as "it was verbal."** The post-hoc report is a fresh conjecture about the earlier thought, and it can be wrong. Once I had that distinction, self-reports — mine and a model's — stopped being evidence about what happened and became evidence about what the reporting layer *believes* happened.

**A mapping being half wrong is more informative than it being right.** The half that broke told me the correction I needed; the half that survived — lossy reconstruction from workspace to output — is the part that transfers.

**Check whether the question has a false premise.** I asked "why must everything be explicit for error correction?" and the answer was that it mustn't, and the person I was quoting says so explicitly. The good version of the question — *what does explicitness add, if every layer corrects natively?* — was hiding behind the bad one, and would have stayed hidden if I'd got a compliant answer to what I actually asked.
