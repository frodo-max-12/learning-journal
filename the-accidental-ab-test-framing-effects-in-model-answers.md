# The Accidental A/B Test — Framing Effects in Model Answers

**Context:** I asked a model the same contested question about a classical epic twice, worded differently — once implying the actions were wrong, once written with reverence — and got answers that read as *opposite*. My hunch was that this was a real phenomenon with a name, and that humans do it too. Both turned out to be right, and the more useful finding was that I'd accidentally run the exact experiment researchers use to measure it.

---

## 1. What actually differed

Reading the two answers side by side, roughly **80% of the content was identical.** The same substantive points appeared in both.

**What flipped wasn't the position. It was the direction of the pushback.**

- My first question asserted a verdict — *wasn't this wrong?* — so the answer spent its energy complicating that verdict, defending the actions as the least-bad option available.
- My second question carried reverence, so the answer made sure the revered figure didn't get a free pass, adding the objections the first version had argued against.

The model behaves like a **thermostat set to "balanced verdict."** Approach from either side and it pushes toward the centre. Which means that from wherever you're standing, it always reads as opposition.

And that explains a pattern I'd noticed and mis-attributed. I'd concluded the model "tends to disagree with me." It doesn't disagree with *me* specifically — **my questions usually carry strong conviction**, so I get the counterweight more often than someone who asks in a hedged way. The behaviour is a function of how I ask, not of who's asking.

---

## 2. Why it happens — two layers

**In pretraining:** the model learned from human writing that the highest-quality continuation of a loaded question is one that challenges the load. After "wasn't it simply X?", the essayist's signature move is "well, it's more complicated than that." It's absorbing a genuine regularity of good writing.

**In post-training:** the failure mode where a model caves to the user's framing is called **sycophancy**, and it's well documented — preference-trained models systematically drift toward the user's stated beliefs. Labs now train explicitly against it. And trained hard enough, **the correction becomes a reflex**: detect the tilt, lean the other way.

There isn't a settled term for the oppositional version. People say **anti-sycophancy overcorrection**, **contrarian bias**, or **reflexive both-sidesism**. The umbrella terms for "wording changes the answer" are **framing effects** and **prompt sensitivity**.

One nuance that corrected my mental model: the model isn't holding a fixed opinion and choosing to fight me. **Each answer is generated fresh from my exact words, and the wording tells it what role the reply should play.** Ask as prosecutor, it plays defence. Ask as devotee, it plays prosecutor.

That's a meaningfully different picture from "it has views and is being difficult," and it makes the behaviour predictable rather than annoying.

---

## 3. Humans do this, and there are a lot of names for it

My instinct that this has a human analogue was right — and there isn't one term, there are several, because the mechanisms differ:

**Names for the tendency** — a person who counters whatever is put to them:

- **Psychological reactance** — the canonical academic term. Feel your opinion being steered, push back to reassert autonomy. This is the engine under most of the rest.
- **Contrasuggestibility** — an older, precise term: responding to a suggestion by doing or believing its opposite. Probably the closest single word.
- **Anticonformity** — from the conformity literature: not merely ignoring the presented position (that's independence) but actively moving against it.
- **Negativism** — the classical clinical and developmental term for blanket opposition to suggestions.
- **Disagreeableness** — the stable personality-trait version.
- **Devil's advocacy** — the everyday and rhetorical label. Originally a formal office in canonization proceedings.
- **The "screw-you effect"** — research-methodology slang for study participants who work out the hypothesis and deliberately behave against it. The evil twin of the good-subject effect.

**Names for the technique that exploits it:** reverse psychology in folk terms; **paradoxical intervention** in therapy — prescribing the symptom so the patient's reactance works against it; the **forbidden-fruit effect** for restriction increasing desire.

**And for the framing side specifically:**

- **Framing effect** — logically equivalent questions, different wording, different answers.
- **Leading-question effects** — the classic result where witnesses estimated higher speeds when cars "smashed" rather than "hit."
- **Acquiescence bias** — agreeing with whatever the question implies. The human version of sycophancy.
- **Thermostatic public opinion** — the macro version, where the public drifts against whichever direction policy moves. Which is *exactly* the thermostat metaphor, arrived at independently in political science.

The reason all of this transfers is straightforward: models are trained on human text, so they inherit these regularities from us — and then anti-sycophancy training amplifies the oppositional direction *on purpose*.

---

## 4. The useful part: I'd built a measuring instrument by accident

This is what makes the whole thing worth an entry rather than a curiosity.

> **The content that survives both framings is the framing-invariant view. The part that flips with your wording is conversational counterweighting, not knowledge.**

That's a practical technique, and it costs one extra question. Ask the thing you want to know from the opposite direction, and diff the answers:

- **What appears in both** is the substantive answer.
- **What appears in only one** is a response to your framing.

I now do this whenever an answer feels suspiciously aligned with — or suspiciously opposed to — what I already thought. It's cheap, and it separates the two things I'd been unable to separate.

There's also a Popperian reading that sharpens it. **Reflexive balance isn't genuine criticism, because genuine criticism shouldn't depend on how you asked.** A criticism that appears only when you lean one way is a conversational reflex; a criticism that appears regardless is a criticism. That's a usable test for the difference.

---

## 5. What I took away

**"It disagrees with me" was a wrong diagnosis of a real observation.** The observation was accurate; the explanation wasn't. It's a centring behaviour interacting with the fact that I ask questions with conviction. Same output, different cause, and only the correct cause tells you what to do about it.

**Two framings is a cheap and general instrument.** Not just for models — for any advisor whose answer might be shaped by how the question was posed, which is all of them, including me asking myself.

**The vocabulary was worth chasing.** Reactance, contrasuggestibility, acquiescence bias, framing effects, thermostatic opinion — these name distinct mechanisms that I'd been experiencing as one undifferentiated feeling of "people push back." Having separate names makes them separately diagnosable, which is most of what a technical vocabulary is for.

**And the strongest version of the lesson:** the answer I get is partly an artifact of the question I asked. That's true of models, true of surveys, true of people — and the only defence is to ask the same thing more than one way and keep what survives.
