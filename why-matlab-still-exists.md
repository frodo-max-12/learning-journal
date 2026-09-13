# Why MATLAB Still Exists

**Context:** Python is free, general-purpose, and has a mature numerical stack. On the surface it should have finished MATLAB off years ago. It hasn't, and asking why turned out to be a good lesson in what actually determines whether a tool survives — plus a correction to my picture of the modern machine-learning stack that I hadn't seen coming.

---

## 1. The reasons MATLAB persists are mostly not about the language

**Simulink has no real Python equivalent.** This is the big one, and I didn't know it. Simulink is block-diagram modelling and simulation with **automatic generation of embedded C or HDL code** — you design a control system as a diagram, simulate the physical plant it will control, then generate code that runs on the actual embedded controller. That whole workflow is the backbone of automotive and aerospace engineering and exists essentially nowhere else. When people say "we use MATLAB," they very often mean Simulink.

**Validated, supported, certifiable toolboxes.** In regulated industries — aerospace, automotive safety, medical devices — you need tools backed by a vendor who supplies verification artefacts, accepts liability, and has a support line.

The line that landed: **you can't call NumPy when an auditor asks who validated your numerical library.**

That reframes the comparison entirely. In a certification context, "free and open source" is not a neutral advantage — the absence of a legally accountable vendor is a *cost*, because someone has to produce the evidence that the tool is fit for purpose. What you're buying isn't features; it's an entity that will stand behind the numbers.

**It works identically everywhere.** One installer, integrated editor, debugger, and profiler. No package manager, no virtual environments, no dependency resolution. A decade-old script tends to still run. Python's flexibility is also a recurring tax — and I've paid that tax myself, losing an afternoon to an editor running my code with the wrong interpreter.

**Entrenchment.** Decades of legacy code, textbooks written around it, university courses training each new cohort on it. For an organization with a million lines of validated code, the switching cost is enormous and the payoff is often "the same thing, but free" — which is not a compelling business case.

**Matrix-native ergonomics.** Built for linear algebra from day one, so numerical code reads cleanly. NumPy has largely closed this gap, but the culture stuck.

---

## 2. Where Python genuinely wins

It's free, it's general-purpose — your numerical code lives next to your web backend, your glue scripts, and your data pipeline — and it owns machine learning and data science outright.

The clean split: **Python won general-purpose computing and machine learning; MATLAB held onto core engineering**, especially model-based design, control systems, and signal processing in safety-critical industries, where the simulation toolchain, vendor support, and certification matter more than licence cost.

And increasingly they're used *together* rather than in competition — the engineering domain in one, the machine learning and software glue in the other.

---

## 3. The correction: "Python with NumPy" isn't the AI stack

I'd been carrying "modern AI is Python and NumPy," and that's wrong in a specific and useful way.

NumPy is the foundational CPU numerical library. It's everywhere for data preparation and classical machine learning. But it does **not** do the two things deep learning absolutely requires:

- **GPU acceleration** — NumPy is CPU-only.
- **Automatic differentiation** — computing gradients to train networks.

Those two absences are the entire reason deep-learning frameworks exist as separate things rather than as NumPy add-ons.

**Automatic differentiation is the one I'd underrated.** Training a network means computing the gradient of a loss with respect to millions of parameters. Doing that by hand for each architecture is infeasible — and it's exactly why my own experience of writing a random-search agent needed no framework at all. **Search never differentiates anything.** The moment I'd needed gradients would have been the moment NumPy stopped being enough, and installing a framework then would have been a conclusion I'd reached rather than a step I was told to take.

So the layered picture:

| layer | what it's for |
|---|---|
| NumPy | CPU arrays, data prep, classical ML — no gradients, no GPU |
| deep-learning frameworks | GPU execution + automatic differentiation |
| higher-level libraries | models and training loops built on those |

---

## 4. What I took away

**Tools survive on things that aren't features.** Certification, vendor liability, installed base, and an irreplaceable adjacent product kept MATLAB alive against a competitor that's free and technically capable. None of those appear in a language comparison, and all of them are decisive in the industries where it survives.

**"Free" is not automatically an advantage.** In a regulated context the absence of an accountable vendor is a liability someone has to absorb. That inverted a default assumption I hadn't noticed I was making.

**Know exactly which capability you need.** The dividing line between NumPy and a deep-learning framework is *gradients and GPUs*, not vague sophistication. That's a crisp test I can apply to a task: does this need derivatives? If not, the heavy dependency is buying me nothing.
