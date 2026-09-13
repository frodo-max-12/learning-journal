# Git Blame, Gists, and Sponsors — lesser-known GitHub features from first principles

*Learned on March 21 and April 11, 2026. I was browsing GitHub — first Andrej Karpathy's profile, then a code file in a repo — and kept noticing features I had never clicked on. What does "Blame" mean on a code file? What are Gists? What does "Sponsoring 1" mean on someone's profile? Each one turned out to be a window into how open-source culture actually works.*

---

## The "Blame" button — why does GitHub want me to blame someone?

I was looking at a code file on GitHub and noticed a tab to the right of the code view that just said "Blame." My first reaction was — that sounds aggressive. Why would a development tool have a button called blame?

When you click it, what you see is the same file, but now every line has extra information attached: who last changed that line, when they changed it, and which commit it was part of. So instead of seeing clean code, you see a kind of annotated history — a forensic view of the file.

The use case is straightforward. Say you are looking at a line of code and it is broken, or confusing, or you want to understand why it was written a certain way. Blame tells you exactly who touched that line last and when. You can then go look at the commit to see the context — what else changed at the same time, what the commit message said, what problem was being solved.

This is why it is called "blame" — tongue-in-cheek, from the early days of version control. The idea is: if this line is causing a bug, who do we "blame"? Who do we go ask about it?

## The etymology — CVS, annotate, and why "blame" won

The history here is interesting. The original version control systems like CVS (Concurrent Versions System, which predates Git by decades) had this same feature but called it `annotate`. That is a perfectly neutral, descriptive name. When Git came along, Linus Torvalds and the Git developers chose the more colorful name `git blame`. It stuck because programmers tend to enjoy slightly irreverent naming.

Git actually does offer `git annotate` as an alias — it does the exact same thing as `git blame`. But nobody uses it. The culture adopted the blunter term.

> The name "blame" sounds harsh, but it is just about tracing authorship and history. It is one of the most useful tools for understanding why code looks the way it does.

I think there is something revealing about this naming choice. In software engineering, code is not sacred — it is expected to change constantly, and when something breaks, the first question is always "what changed recently?" Blame is the tool that answers that question instantly, line by line. The name reflects a culture where accountability is built into the workflow, not treated as something uncomfortable.

## Gists — GitHub's lightweight sharing tool

This one came up when I was looking at Andrej Karpathy's GitHub profile and noticed it said "11 gists" alongside his repositories. I had no idea what a gist was.

It turns out a Gist is essentially a mini-repository. It is a way to share a small piece of code — a single file, a script, a configuration snippet — without creating a full repository with all the overhead that comes with it (folder structure, README files, CI pipelines, licensing, etc.).

The best way to understand it is by example. One of Karpathy's gists is called `microgpt.py` — a single Python file that implements GPT training and inference. That is it. One file. But because it is a Gist, it still has all the essential GitHub features:

| Feature | Full Repository | Gist |
|---|---|---|
| Version history | Yes | Yes |
| Can be forked | Yes | Yes |
| Can be starred | Yes | Yes (microgpt.py has 8,631 stars) |
| Multiple files | Yes | Yes, but typically few |
| CI/CD pipelines | Yes | No |
| Issues, PRs, Wiki | Yes | No |
| Folder structure | Yes | Flat (no directories) |

So a Gist is what you use when you want to share a self-contained piece of code and you want it to be version-controlled, forkable, and discoverable — but you do not want the ceremony of a full repository.

I think of it like this: a repository is like publishing a book. A Gist is like pinning a note to a community bulletin board. The note is still yours, people can copy it, and you can update it — but there is no table of contents, no chapters, no index.

## Public vs. secret Gists — a subtle distinction

Gists can be either public or secret, and the distinction is important to understand because "secret" does not mean "private" in the way you might expect.

A **public Gist** is searchable and shows up on your profile. Anyone can find it by browsing or searching GitHub.

A **secret Gist** is not searchable and does not appear on your profile, but — and this is the key part — anyone who has the URL can view it. It is security through obscurity, not through access control. If you share the link, or if someone guesses the URL, they can see it.

This is a useful mental model for thinking about security in general: there is a difference between something being *unlisted* and something being *locked*. A secret Gist is unlisted. It is not locked. YouTube has the same concept with "unlisted" videos — not searchable, but accessible to anyone with the link.

## Finding someone's Gists

One thing I found slightly odd is that Gists are not prominently linked on a GitHub profile page, especially on mobile. If you want to browse someone's Gists, the most reliable way is to go directly to `gist.github.com/<username>`. For Karpathy, that would be `gist.github.com/karpathy`. It is almost like Gists live in a parallel universe on GitHub — same infrastructure, same account, but a slightly separate surface.

## GitHub Sponsors — patronage for open source

On Karpathy's profile, I also noticed a small section that said "Sponsoring 1" with Simon Willison listed. My first question was: who is paying whom?

The answer is that Karpathy is paying Simon Willison. "Sponsoring 1" means he is sponsoring one person. GitHub Sponsors is essentially a patronage system built into the platform — you can make recurring monthly payments to open-source developers whose work you value.

The mechanics are simple: a developer sets up tiers (say $5/month, $10/month, $25/month), and supporters pick a tier. GitHub does not disclose the amounts, so you can see *that* Karpathy sponsors Willison, but not *how much* he gives.

Simon Willison is well known for building tools like **Datasette** (for exploring and publishing data) and **llm** (a CLI for interacting with language models). These are open-source tools that many developers rely on, built largely by one person. Sponsorship is how the community says "this work matters, keep going."

> GitHub Sponsors is patronage for the modern era — financial support flowing directly from users to creators, without publishers, advertisers, or intermediaries.

## Why these features matter together

Looking at Blame, Gists, and Sponsors together, I see three different facets of what makes open-source culture work:

**Blame** is about accountability and history. Code is not anonymous — every line has an author and a story. This makes collaboration possible at scale because you can always trace back to intent.

**Gists** are about lowering the barrier to sharing. Not every idea deserves the ceremony of a full repository. Sometimes you just want to share a clever script, and Gists make that frictionless while preserving the properties that matter (versioning, forking, discovery).

**Sponsors** are about sustainability. Open source has a well-known problem: hugely valuable software maintained by individuals who are not compensated for it. Sponsors is GitHub's attempt to build economic sustainability directly into the platform where the work happens.

Each one is small on its own, but together they reveal a platform that is trying to support the full lifecycle of open-source work — from sharing a quick idea (Gist), to building something serious (repository), to understanding its history (Blame), to sustaining the people who build it (Sponsors).

---

*What I studied next: I went deeper into how Git itself works under the hood — commits, branches, and merging. Those notes are in [how-git-tracks-changes.md](how-git-tracks-changes.md).*
