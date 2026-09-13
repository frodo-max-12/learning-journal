# Git & GitHub — What I Know So Far

---

## Core Concepts

| Concept | What it means |
|---------|--------------|
| **Git** | Version control — tracks changes to files over time, like save points in a game |
| **GitHub** | Cloud storage for git repos — your code lives online |
| **Repository (repo)** | A folder tracked by git |
| **Commit** | A snapshot of your code at a point in time |
| **Staging** | Selecting which files go into the next commit (like a shopping cart before checkout) |

## Commands I'm Comfortable With

| Command | What it does |
|---------|-------------|
| `git init` | Start tracking a folder |
| `git add <file>` | Stage a file for commit |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push` | Upload commits to GitHub |
| `git pull` | Download latest changes from GitHub |
| `git status` | See what's changed / what's staged |
| `git log --oneline` | View commit history |
| `gh repo create` | Create a new GitHub repo from terminal |
| `gh auth login` | Connect terminal to GitHub account |

## Concepts I Understand

- **Push vs Pull** — push sends local commits to GitHub; pull downloads GitHub's commits to my Mac
- **Merge conflicts** — happen when two places edit the same thing; git needs you to choose which version to keep
- **Rebase** — re-stacking your commits on top of the latest changes
- **Remote (origin)** — the nickname for your GitHub repo's URL
- **Branches** — parallel versions of your code; `main` is the default branch
- **UTC timestamps** — git stores times in UTC; convert to IST by adding 5h 30m

## Lessons Learned the Hard Way

- If `git push` is rejected, run `git pull --rebase` first — GitHub had changes you didn't have locally
- "Add files via upload" on GitHub.com creates a commit too — can cause sync issues with your local repo
- `.schema` in SQLite shows the blueprint, not creating anything — same energy as `git log` showing history, not rewriting it

---

*Built up through hands-on terminal sessions.*
