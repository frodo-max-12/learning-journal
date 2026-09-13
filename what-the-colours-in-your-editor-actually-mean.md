# What the Colours in Your Editor Actually Mean

**Context:** I was learning to code and noticed that my editor colours things, and that clicking on a variable highlights every other occurrence of it. I'd been treating this as decoration. The question I asked was practical — how do I actually *use* this while learning? The answer turned out to be that **two entirely different programs are colouring my file**, they know completely different amounts about my code, and knowing which one is talking to you is a genuinely useful skill.

---

## 1. Two systems, not one

**Layer 1 — the grammar. Dumb, fast, always on.**

Shipped with the language extension is a file containing a few hundred regular expressions. One says roughly: *the word `import` at the start of a statement is `keyword.control.import`.* Another says: *text between two quotes is `string.quoted.double`.*

Those labels are called **scopes**. And your colour theme is nothing more than a lookup table from scope to colour: `keyword.control` → blue, `string.quoted` → dark red, `comment` → green.

That's the whole mechanism. **This layer has zero understanding.** It doesn't know what a module is. It matched a pattern and attached a label.

Which explains something I'd noticed without questioning: it still colours your file correctly when the code is half-typed and syntactically broken. It has to, because it isn't parsing — it's pattern-matching, and a pattern doesn't care whether the file as a whole makes sense.

**Layer 2 — semantic tokens. Smart, slower, needs working code.**

This layer comes from a language server that actually parses your file, resolves imports, and builds a model of what the names refer to. It knows that this identifier is a *class* and that one is a *parameter* — a distinction no regular expression can make, because it depends on where the name was defined, possibly in another file.

Once you know the split, the behaviour becomes legible. If colours look right in a broken file, that's layer 1. If a name's colour *changes* a second after you finish typing — or after you fix an unrelated error elsewhere — that's layer 2 arriving with a real answer.

**And here's the part that turns this into a debugging tool:** when layer 2 fails to colour something it should, that's information. It means the language server couldn't resolve the name — a missing import, the wrong interpreter selected, a package installed in a different environment. The colour is reporting a real problem before you ever run the code.

---

## 2. So what does the highlighting actually buy me?

The reframe I took away:

> **The colours are not decoration. They're the output of a program that read your code and is telling you what it understood.**

Learning to read that channel is unusually high-leverage early on, because it's continuous, free, and arrives *before* you run anything. Concretely:

- **A string that isn't string-coloured** means you have an unterminated quote somewhere above. The colour tells you the mistake is earlier in the file than where you're looking.
- **A name coloured as an unresolved variable** when you expected a function usually means an import problem, not a typo.
- **Click-to-highlight-all-occurrences** is the one I'd been using without appreciating. On layer 2 it's not textual matching — it's *scope-aware*: it highlights the occurrences of **this particular variable**, not every appearance of that sequence of characters. A same-named variable in a different function stays dark. That's a live answer to "which of these are actually the same thing?", which is one of the genuinely hard questions when reading unfamiliar code.

---

## 3. A linter is a third thing

I assumed a linter was part of the same machinery. It isn't, and the distinction is clean once you have the two layers.

- **Grammar highlighting** asks: *what does this text look like?*
- **Semantic tokens** ask: *what do these names refer to?*
- **A linter** asks: *is this a good idea?*

A linter runs its own analysis and flags problems that are perfectly valid code — an unused import, a variable assigned and never read, a comparison that's always true, a style violation. None of that is a syntax error. The code would run.

So the three systems are answering escalating questions: is it well-formed, is it meaningful, is it wise. Errors from each mean different things, and I'd been lumping all the squiggles together as "the editor is complaining."

---

## 4. Watching code execute, one line at a time

The related thing I wanted was what I'd seen on a practice site: press a button, execute one line, watch the effect. That's **step debugging**, and it turns out the editor has it built in — I just hadn't connected the practice-site experience with the debugger panel.

The tool that finally made it click for small programs is a **visualizer** that runs your code and draws the interpreter's state at every step. It's not an animation of a pre-recorded program; it's genuinely executing and rendering what exists in memory at that instant.

Two limitations, and both are informative rather than annoying:

**It can't run code that imports third-party libraries.** The environment only has the standard library. That's why I couldn't visualize a script built on an external framework. Which is itself a useful lesson about what "a Python program" means — the language and its libraries are separable, and a lot of what feels like the language is actually packages.

**It only helps for small programs.** The value is watching state change step by step, and that stops being comprehensible past a few dozen lines.

---

## 5. Frames and objects — the distinction the visualizer forced on me

The display splits into two columns, and I had to ask what they meant. This turned out to be the most useful concept in the whole thread.

**Frames** are the left side: one box per active function call, holding that call's local variables. When a function is called a new frame appears; when it returns, the frame vanishes.

**Objects** are the right side: the actual values living on the heap — lists, dictionaries, class instances.

**Variables in frames don't contain objects. They point at them.**

That single picture explains a whole family of things I'd found confusing:

- **Two variables can point at the same list.** Change it through one name and it "changes" through the other — because there was only ever one object with two arrows into it.
- **Reassigning a variable moves an arrow.** Mutating a list changes the object at the far end. Those are different operations, and the frames/objects split is what makes them look different rather than identical.
- **A frame disappearing doesn't destroy the objects it pointed at.** If something else still points at them, they persist. That's the whole idea behind returning a value.

I'd previously imagined variables as boxes holding values. **Frames hold arrows; objects hold values.** Almost every aliasing and mutation surprise I'd had dissolved once I saw the two columns drawn separately.

---

## 6. What I took away

**The tool is talking to you continuously and I hadn't been listening.** Colours, squiggles, and highlight-all are all outputs of programs that read your code. Treating them as feedback rather than styling turns the editor into a live checker running between every keystroke.

**Knowing which layer produced a signal tells you what it means.** Right-looking colours in broken code, colour that arrives late, colour that never arrives — three different diagnoses, and the last one is usually an environment problem rather than a code problem.

**Ask what the tool can't do — the limits are informative.** The visualizer can't import third-party packages, which is a fact about the boundary between a language and its ecosystem. The grammar layer can't tell a class from a parameter, which is a fact about what regular expressions fundamentally cannot express. Both limits taught me more than the features did.
