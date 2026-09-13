# Where Does My Code Actually Run? — Displays, Interpreters, and Environments

**Context:** I had a script and asked what felt like a beginner's question: *where exactly do I run this?* The chain of follow-ups that produced — can I use a notebook instead, why does it break in a cloud notebook, why does my editor's Run button fail on code that works in the terminal — turned out to be about three genuinely separate things I'd been treating as one. Every one of them cost me time before I understood it, and none is about the code.

---

## 1. The first split: is there a screen on the other end?

The script asked for a live animation window. On my own machine that just works — a window opens.

In a cloud notebook it doesn't, and the reason is not a configuration problem:

> **My browser is here. The Python is on a server in a datacentre with no screen attached.**

Asking that server to open a window is asking it to draw on a display that does not exist. The graphics library fails with a complaint about having no video device.

Nothing about the code is wrong. Nothing about the setup is wrong. **The execution is simply happening somewhere with no display.**

That's the concept I'd been missing: a notebook in your browser is a *user interface*, and where the code runs is a separate question. Local notebook → your machine, your screen, windows open. Cloud notebook → someone else's machine, no screen, no windows. The interface looks identical in both cases, which is exactly why the distinction is invisible until something breaks.

The fix is one word — switch from a mode that *draws* frames to one that *returns* them as arrays of pixels, then play them back inline:

| mode | what it does | works headless? |
|---|---|---|
| draw-to-window | opens an OS window, animates live | no |
| return-frames | hands back each frame as pixel data | yes |

And there's a trade-off worth knowing beyond the compatibility one. Live drawing animates as it runs and is locked to the frame rate. Returning frames collects everything and plays it back afterwards. For watching a short run they're equivalent; **for a long training run, returning frames is actually better**, because you aren't stuck watching it in real time.

This is the same "headless" concept that shows up in browser automation, and seeing it in two places is what made it stick: **headless doesn't mean invisible, it means there is no display device attached.** Everything else follows.

---

## 2. The second split: which interpreter is running it?

Then the same code that worked from my terminal failed from my editor's Run button. My assumption was that something in the code was environment-sensitive.

**Nothing was wrong with the code. The editor was running it with a different Python.**

My editor had auto-selected a virtual environment I'd built months earlier for an unrelated database project. That environment had database libraries and not the ones this script needed. And crucially its config said `include-system-site-packages = false`, so it was **sealed off** from the system Python where the needed package actually lived.

Two things I learned from that:

**A virtual environment is a deliberate wall, not just a folder.** That one flag decides whether the environment can see packages installed outside it. Sealed is usually the right default — it's what makes an environment reproducible — but it means "the package is installed on my machine" and "the package is importable from this interpreter" are completely different statements. I'd been treating them as the same statement.

**The editor picked it because my workspace was my entire home folder.** It scanned, found one virtual environment, and used it. This is the root cause and it's a workflow problem rather than a tooling bug.

The habit that makes the problem stop happening:

> **One virtual environment per project folder. One project folder per editor window.**

Open the *project* folder rather than the folder containing everything, and the editor finds the environment sitting next to the code. Switching the interpreter globally would have fixed this project and broken the other one in exactly the same way — the fix that seems obvious is the one that creates the next incident.

---

## 3. The third thing: `python`, `python3`, `python3.14` — and `𝜋thon`

While looking at the environment I noticed four executables that all appeared to be Python, and asked which one I should be using.

They're **all the same interpreter.** Three of them are ten bytes — that's not a program, that's a **symlink**, a signpost holding the ten characters of the real name. And that one is itself a signpost to the actual binary:

```
python  ─┐
python3 ─┼─→ python3.14 ─→ …/bin/python3.14   ← the actual program
𝜋thon   ─┘
```

The historical reason for `python3` existing at all: on a system-wide install, bare `python` used to mean Python 2, so a generation learned to type `python3` to be safe. **Inside a virtual environment there's only one Python, so the ambiguity is gone** and plain `python` is unambiguous.

And `𝜋thon` is real — the mathematical italic small pi character, created as an Easter egg by the environment tooling. It executes perfectly.

The reason this is more than trivia: it's a clean, inspectable example of **indirection**. A name pointing at a name pointing at a binary, where you can swap what the middle name points to and everything above it follows without changing. That's the same mechanism behind version managers, `/usr/local/bin`, and most of how software gets swapped underneath you without anything appearing to change. Ten bytes is a strong hint that you're looking at a signpost rather than a thing.

---

## 4. Three questions, one confusion

What I'd been treating as "will my code run?" is really three independent questions:

| question | what it's about | how it fails |
|---|---|---|
| **where** does the process execute? | your machine vs a remote server | no display, no local files, different hardware |
| **which** interpreter runs it? | system Python vs a virtual environment | import errors on packages you know are installed |
| **what** is that name pointing at? | symlinks and indirection | you're running something other than what you named |

Each has its own failure signature, and the signatures are distinguishable once you know there are three of them. Missing display device → the first. Import error for an installed package → the second. Wrong version reported → the third.

Before this, all three presented to me as "it works in one place and not another," which is not a diagnosis.

---

## 5. What I took away

**The interface and the execution environment are different things.** A notebook in a browser tells you nothing about where the code runs. That single distinction explains the entire class of "works locally, breaks in the cloud" problems, and it's not really about notebooks — it's about remembering to ask which machine is doing the work.

**"Installed on my machine" is not a meaningful statement.** The meaningful one is "importable from the interpreter that will actually run this file." Virtual environments make those diverge on purpose, and that's a feature until you forget it's happening.

**Fix the workflow, not the incident.** Repointing the interpreter would have fixed this project and broken the other one. One environment per project folder, one folder per window, makes the whole category of problem disappear rather than rotating it between projects.
