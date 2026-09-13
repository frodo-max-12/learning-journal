# Information, Knowledge, Explanatory Knowledge — Three Nested Circles

**Context:** I was watching Deutsch argue that genetic knowledge doesn't count as explanatory knowledge, and I couldn't see why not. A gene clearly *knows* how to build an eye. Working through it, I proposed a structure — three nested circles, information containing knowledge containing explanatory knowledge — and asked whether I had it right. I did, with one correction to the middle boundary that turned out to be the interesting part of the whole hierarchy.

---

## 1. The structure

> information ⊃ knowledge ⊃ explanatory knowledge

Each strictly inside the last. What makes this useful rather than decorative is that **each boundary has a specific admission criterion** — you can say exactly what gets added when you cross inward.

---

## 2. The first boundary: information → knowledge

My first guess was that knowledge is information with **causal power**. That's close, and the correction sharpens it a lot.

Everything physical has causal effects. A rock dents the ground; one domino topples the next. But a rock isn't knowledge. So causal power in general can't be the criterion.

Deutsch's actual criterion is narrower:

> **Knowledge is information that, once embodied in a suitable environment, tends to cause *itself* to remain embodied.**

Not causal power — **self-perpetuating** causal power.

A gene's information causes the organism to survive and reproduce, which *copies the gene*. It causes its own continuation. An idea that's useful or true gets acted on, spoken, written down — it also causes its own continuation. That self-referential, adapted quality is what lifts information into knowledge.

The refinement matters because it explains the *strictness* of the nesting. The overwhelming majority of physical patterns — the microstate of a gas, thermal noise, the exact shape of a rock — carry information and cause nothing to perpetuate itself. Most information is not knowledge, and it's not a close call.

It also handed me a definition of knowledge with no minds in it at all, which was the part I'd been resisting. A gene is knowledge in the fullest sense — created by variation and selection, adapted, self-perpetuating — and nobody knows anything.

---

## 3. The second boundary: knowledge → explanatory knowledge

What gets added here is an **encoded reason** — the *why*, stated in a code, in symbols.

And this is exactly the line from the argument I couldn't follow. The gene *has* the causal power, so it's inside the knowledge ring. But it "does not express its causal power in a code" — it doesn't state *why* it works. So it never reaches the inner ring.

The gene knows *how* in the only sense that matters operationally: it builds the eye, reliably, every time. What it doesn't contain anywhere is *why an eye works* — no representation of optics, of refraction, of the relationship between lens curvature and focal length. Evolution discovered a solution to an optics problem without ever representing the optics.

That distinction is the one I'd been missing, and it isn't a quibble about the word "knowledge." It's a claim about **reach**. A gene's solution is confined to the situations selection actually encountered. An explanation of optics applies to telescopes, cameras, and eyes on planets nobody has visited — because it states the reason, and reasons transfer to cases that were never tested.

Which makes the nesting strict again, and much more dramatically than at the first boundary:

**The entire biosphere sits in the middle ring only.** Every gene, every instinct, billions of years of accumulated adaptation — all of it knowledge, none of it explanatory. As far as we know the inner ring is occupied *solely* by the contents of minds.

That's why the centre is so sparse and so consequential. Almost all the knowledge that has ever existed never reached it.

---

## 4. The fourth ring

There's arguably one more circle inside: **good explanations** — the ones that are **hard to vary**, where you can't change the details without wrecking how they account for what they explain.

The seasons come from the Earth's axial tilt, versus the seasons come from a goddess returning from the underworld. Both are *explanatory* knowledge — both state a why, in a code. Only the first is hard to vary: change any detail of the tilt account and it stops predicting the hemispheres being opposite, or the tropics behaving differently. The myth can absorb any observation by adjusting the story, which is precisely why it explains nothing.

Hard-to-vary is the property that gives knowledge unbounded reach. A theory with no slack in it, that survives criticism anyway, is one that's tracking something real.

---

## 5. Where LLMs sit, on this map

The obvious follow-up: why does Deutsch keep saying language models don't have explanatory knowledge? Once the hierarchy is built, the answer is nearly definitional — and it's a claim about *process*, not output.

For Deutsch, explanatory knowledge is the product of one specific method: **conjecture and criticism.** Guess an explanation that goes beyond the evidence — positing unseen mechanisms — then try to refute it, and keep what survives.

A language model runs a different process: model the statistical regularities of a corpus, emit the likely next token. That is precisely the **inductivist** picture — derive truths by extrapolating from observations — that Popper spent a career arguing is impossible. So the claim is close to a definition: it can't be *creating* explanatory knowledge, because it's doing the thing that never creates explanations.

Mapped onto the circles, the position is sharper than "it doesn't really understand":

- **The model's own knowledge — its weights — sits in the middle ring.** An extraordinarily sophisticated rule of thumb for producing plausible text. Structurally it is the gene again: it produces the right output without representing or creating the *why*.
- **The explanatory content in its output is real, but second-hand.** Those explanations were created by humans who did run conjecture and criticism, and they sit in the corpus. The model recombines them. It **quotes the inner circle without entering it.**

The "tells" that get cited follow from the process rather than being separate complaints: hallucination as the natural behaviour of something tracking textual likelihood rather than truth, since nothing was ever subjected to criticism *aimed at truth*; the absence of a problem being solved, when for Popper knowledge growth *starts* from a problem; and preference training rewarding agreeableness, which is close to the opposite of the willingness to conjecture against the grain and defend an unpopular-but-true explanation.

Worth being fair about what the position is *not*. He isn't a mystic about machine minds — he thinks AGI is possible and perhaps not far off in principle, because universality means the program exists and nothing in physics forbids it. The claim is narrower: this is the wrong paradigm, because it bakes in the inductivist mistake, so scaling it pursues a difference of *degree* when what's missing is a difference of *kind*.

---

## 6. What I took away

**A hierarchy is only useful if each boundary has a criterion.** Three nested circles is a picture; *self-perpetuation* at the first boundary and *an encoded reason* at the second is a tool. I can now sort a candidate — a gene, a habit, a trained model, a proof — by asking two questions in order.

**"Knowledge" without minds stopped bothering me.** I'd been reading the word as requiring a knower. Defining it by self-perpetuation instead makes evolution and thought two instances of one process — variation and selection of information that causes its own survival — differing in whether the variation is blind.

**The reason the inner ring matters is reach.** Not prestige, not consciousness — the fact that a stated reason applies to cases nobody tested. Everything else in the hierarchy is confined to the circumstances that produced it. That's the whole argument for why explanation is special, and it's an argument about *scope*, which I find much more persuasive than the versions that appeal to what it feels like from the inside.

**And the honest caveat I'd attach:** this is one epistemology, argued from within itself. The claim that a process which never runs conjecture-and-criticism can't produce explanatory knowledge is close to true by construction, which makes it hard to falsify — and that's precisely the property Deutsch's own criterion would flag. I hold the map because it's clarifying, not because it's settled.
