# Chollet's case against intelligence explosion --- and why "general" doesn't mean "infinite"

*Learned on April 2026. I was reading Francois Chollet's essay "The Implausibility of Intelligence Explosion" and wanted to understand his actual argument, not just the Twitter version of it. This turned into one of the more philosophically interesting things I've studied --- because Chollet's position is more subtle than it looks, and it directly challenges how most people (including me) think about what AI progress means.*

---

## The standard story I had heard

Before I read Chollet, the story I'd absorbed from Twitter and podcasts went something like this: we build an AI that's smart enough to improve its own code. That improved version is even smarter, so it improves itself faster. That version is smarter still. The cycle accelerates exponentially, and within days or weeks, you have a superintelligence that makes humans look like ants. This is the "intelligence explosion" or "recursive self-improvement" thesis, and it's central to a lot of thinking about AI risk.

It sounds logical. It has a kind of mathematical elegance to it. And Chollet says it's wrong --- not because AI won't get better, but because the entire framing is built on a misunderstanding of what intelligence actually is.

## Intelligence is not a dial you turn up

The core of Chollet's argument starts with a deceptively simple observation: your brain is not the whole story of your intelligence.

Think about it. A human brain placed in an octopus body would be useless. Feral children raised outside human culture --- no language, no tools, no other humans to learn from --- never develop what we'd recognize as human-level intelligence. Your intelligence isn't just neural tissue. It's your body, your senses, your language, the tools you use, the people you talk to, the accumulated knowledge of civilization sitting on your bookshelf and in your phone. Chollet's point is that intelligence is *situated*. It doesn't exist in a vacuum.

This matters because the intelligence explosion thesis treats intelligence like a single number on a single axis --- like a volume knob you can keep turning up. Chollet says that's a category error. You can't just "scale up" a mind without also scaling up the body it inhabits, the environment it operates in, and the problems it's adapted to solve.

## The No Free Lunch theorem --- the math behind the intuition

Chollet doesn't just make a philosophical argument. He invokes a result from computer science called the No Free Lunch theorem. The theorem says: no problem-solving algorithm is universally better than any other across all possible problems. Every algorithm that excels at one class of problems necessarily does worse at others.

This is counterintuitive. We're used to thinking that some things are just "smarter" than others --- a human is smarter than a mouse, a mouse is smarter than an ant. But the No Free Lunch theorem says that this hierarchy is always *relative to a particular domain*. AlphaGo is vastly superhuman at Go, but it can't make toast. A chess engine can beat any human alive, but it doesn't know what a kitchen is.

The implication for the intelligence explosion: even if you build an AI that can improve its own architecture, the improvements won't generalize across all problems. Getting better at one thing doesn't automatically make you better at everything. There's no single lever labeled "general smartness" that you can pull.

## Raw brainpower has diminishing returns --- the empirical evidence

This is where Chollet's argument gets really interesting, because he backs it up with data about humans.

IQ correlates with life outcomes --- up to a point. But the correlation breaks down at higher levels. Chollet cites the fact that many of history's most impactful scientists had IQs in the 120s-130s range, not the 170+ range. Feynman reportedly scored 126 on an IQ test. James Watson scored 124. Meanwhile, there are roughly 50,000 people alive today with IQs above 170, and most of them are not making epoch-defining breakthroughs.

If raw cognitive power were the bottleneck --- if intelligence were just a dial, and turning it higher always produced proportionally greater results --- then these 170+ IQ individuals should be dominating every field. They're not. The bottleneck, Chollet argues, is not brainpower but circumstance: access to the right problems, the right collaborators, the right moment in history, the right tools.

I found this deeply persuasive. It matches my experience from the business world. The smartest person in the room is not always the most effective. The most effective person is usually the one who's best situated --- right team, right problem, right timing.

## Recursive self-improvement already exists, and it doesn't explode

Here's the argument that sealed it for me. Chollet points out that recursively self-improving systems are not hypothetical. They already exist all around us.

Software development is recursively self-improving --- we build better tools to build better software. Scientific research is recursively self-improving --- each discovery enables the next. Investing is recursively self-improving --- returns compound. Even evolution is recursively self-improving --- better-adapted organisms create better-adapted offspring.

And none of these systems exhibit runaway exponential growth. They all hit diminishing returns. Each improvement makes the next improvement marginally harder, not easier. The curve is sigmoidal, not exponential --- fast growth in the middle, tapering off at the edges.

Chollet argues that an AI improving its own code would face the same pattern. The first improvements would be significant. But as the easy optimizations get picked off, each subsequent improvement would require more effort for less gain. You'd get an S-curve, not a hockey stick.

> The key insight: recursive self-improvement is real, but it's bounded by diminishing returns. We've seen this pattern in every recursively self-improving system we know of. There's no reason to expect AI to be the one exception.

## So... does Chollet think AGI is impossible?

This is where I got confused, and I think a lot of people do. Chollet argues against unbounded intelligence, invokes the No Free Lunch theorem to say "there is no general intelligence" in the domain-independent sense --- and then he spends years building the ARC benchmark to measure progress toward AGI.

The resolution is that Chollet uses "general intelligence" to mean something very specific. He's not talking about an omniscient system that's great at every possible problem. He's talking about *skill-acquisition efficiency* --- how quickly a system can pick up genuinely novel tasks with minimal experience.

Humans are remarkably good at this. Show a child three examples of a pattern and they can generalize to the fourth. Current AI systems (including LLMs) often need thousands or millions of examples to learn the same thing. ARC, Chollet's benchmark, specifically tests this kind of generalization --- each puzzle requires you to infer a rule from a handful of examples, and no two puzzles share the same rule.

So Chollet's actual position is nuanced:

| What he believes | What he rejects |
|---|---|
| General-*ish* intelligence is real --- some systems generalize far better than others | Intelligence as a single unbounded axis you can scale up infinitely |
| AGI is a meaningful goal worth pursuing | AGI as a stepping stone to explosive superintelligence |
| AI will continue to improve | Improvement will be explosive and recursive rather than incremental |
| Broad capability is possible | Domain-independent omniscience is possible |

## How this connects to David Deutsch

I had previously studied David Deutsch's views on AGI, and the contrast is striking. Deutsch argues that what makes human intelligence special is *explanatory universality* --- the ability to construct explanations for anything. He believes AGI is possible precisely because this is a qualitative threshold, not a quantitative one. Once you cross it, you have a universal explainer.

Chollet would likely agree that humans have a qualitatively different kind of generalization ability, but he'd push back hard on the idea that this ability can be amplified without bound. Deutsch sees the threshold as the important thing; Chollet sees the *ceiling above the threshold* as the important thing.

Both agree AGI is meaningful. They disagree on what happens after you get it.

## What I take away

I came away from this convinced that the intelligence explosion narrative, as popularly told, is probably wrong --- or at least dramatically oversimplified. Intelligence isn't a volume knob. It's embedded in bodies, environments, cultures, and tools. Making the "brain" part better has real but diminishing returns.

This doesn't mean AI progress will be slow or unimpactful. Chollet himself acknowledges that narrow AI capabilities can be extreme --- superhuman performance on specific tasks. And the accumulation of many narrow capabilities, combined with the right interfaces and tools, could be transformative. It's just not going to look like a sudden singularity. It's going to look like what it's already looking like: steady, compounding, incremental improvement that occasionally surprises us.

---

*What I studied next: David Deutsch's views on AGI and universal explanation --- see [deutschs-constructor-theory-and-agi.md](deutschs-constructor-theory-and-agi.md)*
