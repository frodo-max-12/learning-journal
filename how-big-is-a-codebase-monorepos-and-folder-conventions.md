# How Big Is a Codebase, Really — Monorepos and Folder Conventions

**Context:** I asked an idle question — how many lines of code is Windows? — and the answer led somewhere more useful than trivia. The numbers are large enough to break the intuitions I'd been carrying about how software is organized, and following them produced two things I now use constantly: what a monorepo actually is, and why almost every project I open has the same handful of folders in it.

---

## 1. The numbers

| system | approximate lines of code |
|---|---|
| Linux kernel | ~30 million |
| Windows | ~50–60 million |
| Google's entire codebase | **~2 billion** (as reported in 2015; larger now) |

The first two are the size I vaguely expected for "a big piece of software." The third is a different category, and it's the one worth sitting with.

Two billion lines in **one repository** — reportedly the largest in the world, spanning search, mail, video, maps, mobile, cloud, everything. And it can't be held in standard version control: off-the-shelf tools weren't designed for that scale, so it runs on a custom system built for the purpose.

That last detail is the interesting one. **The scale is large enough that the tooling itself becomes a research problem.** Version control is one of the most solved problems in software, and past a certain size it stops being solved and needs re-inventing.

---

## 2. What a monolithic repository means

It means all — or nearly all — of a company's code lives in **one single repository** rather than being split across many.

So rather than a separate repo for mail, another for maps, another for search, essentially everything sits in one shared codebase, and engineers across the company can see, search, and depend on each other's code directly.

**The advantages:**
- Code sharing is trivial — you import from another team's directory rather than publishing and consuming a package.
- Tooling is consistent, because there's one build system and one set of conventions.
- Dependency management is dramatically simpler: everything is at one version, the version in the repo. There is no "which release of the internal library are we on?"

**The cost:**
- It requires custom infrastructure. Standard tools buckle.

The alternative — what most companies do — is the **polyrepo** approach: each project or service gets its own repository.

---

## 3. Why the trade-off is more interesting than it looks

The thing that stuck with me is that this is a **dependency problem in disguise**, not a storage-layout preference.

In a polyrepo, code sharing happens through *published versions*. Team A publishes version 2.3 of a library; team B depends on 2.1; team C depends on 2.3. Now you have multiple versions of the same library live simultaneously, and upgrading one thing means checking what it breaks elsewhere. That's the familiar dependency-hell shape — and it's the price of independence.

In a monorepo, there's exactly one version of everything: the one at the head of the repository. Change a shared library and you change every caller, immediately and visibly. You can't ship a breaking change and leave others on the old version, because there is no old version.

So the monorepo doesn't eliminate the coordination cost — **it moves it from downstream to upstream.** Instead of every consumer eventually paying to migrate, the person making the change pays up front by fixing all the call sites. That's a real trade with a real answer: it depends on whether you can build tooling that makes "fix all call sites at once" feasible.

Which is the same shape as several trades I keep meeting — the cost doesn't disappear, it relocates to a different phase, and whether that's an improvement depends on which phase you can afford.

---

## 4. The folder conventions every project shares

The other half of this: I kept opening projects and seeing the same directories, and had assumed it was coincidence or copying. It's a convention, and each folder has a reason.

**`src/` — source.** The actual core logic. If it's a library, this is the code that gets published or imported. Sometimes called `lib/` instead, and the distinction is subtle: `src/` implies "this gets compiled or built," while `lib/` often means "this is ready to use as-is."

**`bin/` — binaries and entry points.** The scripts that actually get run from the command line. Typically a thin layer that parses arguments and then calls into `src/` for the real work. The name comes from Unix, where executables live in `/usr/bin`.

**`test/` — automated tests.** Unit and integration tests, plus fixtures. Also seen as `tests/`, `__tests__/`, or `spec/`, depending on which testing framework's conventions the project grew up with.

**`scripts/` — developer utilities.** Database migrations, build helpers, deployment scripts, seed data. And the distinction from `bin/` is precise and worth knowing: **`bin/` is for people running the tool; `scripts/` is for people working on it.**

Plus the ones you'll meet everywhere else: `dist/` or `build/` for compiled output, `docs/`, `config/`, `assets/`/`public/`/`static/` for files served as-is, and `.github/` for CI workflows.

**The organizing principle is separation of concerns by role** — source code, tests, build output, developer tooling, and entry points each get their own home.

---

## 5. Why the conventions are worth more than they look

A convention that's followed widely enough stops being a convention and becomes **navigation**.

When I open an unfamiliar repository now, I don't read it in file order. I know that `src/` is what the thing *is*, `bin/` is how it *starts*, `test/` is what it *promises*, and `dist/` is *generated and should be ignored*. That's most of an orientation before reading a single line.

And the same thing works in reverse, as a signal about the project itself:

- A project with no `test/` is telling you something.
- A project where `src/` is one enormous file is telling you something.
- A project with `dist/` committed to version control is telling you something.

The layout is documentation that nobody had to write and nobody can forget to update — which makes it more reliable than the documentation that *was* written.

---

## 6. What I took away

**Scale changes kind, not just degree.** Two billion lines isn't "a lot of code," it's a regime where solved problems become unsolved and you build your own version control. Worth remembering when reasoning about how big companies work — their constraints aren't my constraints multiplied.

**Monorepo vs polyrepo is a question about where dependency pain is paid**, not about file organization. Upstream, by whoever makes the change, or downstream, by everyone who eventually upgrades.

**Folder conventions are a shared map.** They exist so that a stranger can orient in an unfamiliar project in seconds, and following them is a courtesy to whoever opens your repository next — including yourself, later.
