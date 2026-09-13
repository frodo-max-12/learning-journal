# Terminal First Principles & Package Management

**Topic:** Setting up OpenClaw + Dev Environment + First GitHub Push

---

## Setting up OpenClaw

I wanted to set up OpenClaw — a personal AI assistant that works through messaging apps (WhatsApp, Telegram, iMessage). It can manage email, calendar, and other tasks.

### Quickest way to get started:
```bash
npm install -g openclaw
openclaw onboard --install-daemon
```

The onboarding wizard walks through:
1. AI provider — choose your model
2. Chat interface — pick your messaging platform
3. Skills — optional tools for email, calendar, etc.
4. Control UI — web-based or terminal

**Security note:** The Gateway is open by default — bind to localhost only.

---

## My approach: learn everything from scratch

I'm non-technical. I want to learn coding by understanding each line of code. Building understanding is the most important thing for me.

---

## Step 1: Checking prerequisites

Key concepts:
- **Node.js** — A program that lets your computer run JavaScript code
- **npm** — "Node Package Manager" — like an app store for code

**Commands run:**
```bash
node --version
# Output: v22.18.0

npm --version
# Output: 10.9.3
```

**What I learned:**
- `--version` is a "flag" — a modifier that changes what a command does
- Both Node.js and npm were already installed

---

## Step 2: Installing OpenClaw

**Command explained piece by piece:**
```bash
npm install -g openclaw
```

| Part | Meaning |
|------|---------|
| `npm` | Using the Node Package Manager |
| `install` | We want to install something |
| `-g` | "Global" — install for the whole computer, not just one folder |
| `openclaw` | The package name to install |

**Output explained:**
- `npm warn deprecated node-domexception@1.0.0` — A warning (not an error). One sub-package is old but still works. Like a "best by" date.
- `added 540 packages in 41s` — Downloaded 540 packages. OpenClaw depends on hundreds of helper packages (dependencies). Normal in JavaScript.
- `89 packages are looking for funding` — Many packages are built by volunteers. Just a note about donations.

**Verification:**
```bash
openclaw --version
# Output: OpenClaw 2026.3.13 (61d171a)
```
- Version number `2026.3.13` = released March 13, 2026
- `(61d171a)` = a "commit hash" — unique ID for the exact code snapshot

---

## Detour: Daily GitHub contributions (green squares)

I saw someone's GitHub profile where they commit daily — all green squares. Should I do that?

**My takeaway:**
- Consistency beats intensity — 30 min/day > 8 hours once a week
- Don't chase green squares with fake commits — let it happen naturally with real work

---

## Step 3: Setting up Git and GitHub

### Checking what we need:

```bash
gh --version
# Output: command not found — gh not installed

git config --global user.name
# Output: nothing — not configured

git config --global user.email
# Output: nothing — not configured

brew --version
# Output: Homebrew 4.6.0 — installed!
```

**What I learned:**
- **gh** = GitHub CLI — lets you manage GitHub from the terminal
- **Homebrew** = package manager for macOS — like npm but for general Mac tools
- "command not found" means the program isn't installed
- Exit code 1 with no output means "nothing found" (for config commands)

### Configuring git:

```bash
git config --global user.name "Your Name"
# No output = success (silence means everything went fine)

git config --global user.email "you@example.com"
# No output = success
```

**What I learned:**
- `--global` means the setting applies everywhere on my computer
- `user.name` is in quotes because there's a space — without quotes, the terminal thinks "Jain" is a separate command
- The email must match my GitHub account email for green squares to count
- `&&` in commands means "run the next command only if the first one succeeds"

### Installing GitHub CLI:

```bash
brew install gh
# Output: lots of downloading and installing
# Result: gh version 2.88.1 installed

gh --version
# Output: gh version 2.88.1 (2026-03-12)
```

### Logging into GitHub:

```bash
gh auth login
# (Interactive — I ran this in a separate terminal)
# Selected: GitHub.com → HTTPS → Yes → Login with web browser
```

**What I learned:**
- Some commands are "interactive" — they need back-and-forth input
- `Cmd + T` opens a new terminal tab, `Cmd + N` opens a new window
- Tokens are like temporary passwords for terminal-to-GitHub access
- Token "scopes" are permissions — `repo` lets you create and push to repositories

**Verification:**
```bash
gh auth status
# Output: ✓ Logged in to github.com account your-username
```

---

## Step 4: Creating the project and pushing to GitHub

### Creating a folder and initializing git:

```bash
mkdir /Users/you/learning-journal
# mkdir = "make directory" (directory = folder)

cd /Users/you/learning-journal && git init
# git init = start tracking this folder with git
# Created a hidden .git/ folder where git stores all tracking data
```

### Created day-01-setup.md
A summary file documenting everything I set up today, written in Markdown (.md format).

### Staging and committing:

```bash
git add day-01-setup.md
# "Add to shopping cart" — selecting what to include in the next snapshot
# No output = success

git commit -m "Day 01: Set up dev environment - Node.js, npm, OpenClaw, git, GitHub CLI"
# Output: [main (root-commit) 8297590]
# root-commit = very first commit ever
# 8297590 = unique ID for this snapshot
# 1 file changed, 51 insertions(+)
```

### Creating private repo and pushing:

```bash
gh repo create learning-journal --private --source=. --remote=origin --push
```

| Part | Meaning |
|------|---------|
| `gh repo create` | Create a new repo on GitHub |
| `learning-journal` | Repo name |
| `--private` | Only I can see it |
| `--source=.` | Use current folder (`.` = "here") |
| `--remote=origin` | Name the GitHub connection "origin" |
| `--push` | Push the code up immediately |

**Result:** https://github.com/your-username/learning-journal

---

## Key concepts I learned today

1. **Terminal** — Text-based way to control your computer
2. **Flags** (`-g`, `--version`, `--global`) — Modifiers that change how commands behave
3. **Package managers** — App stores for code (npm for JavaScript, Homebrew for macOS)
4. **Dependencies** — Packages that other packages need to work
5. **Git** — Tracks changes to files over time (version control)
6. **Commit** — A snapshot of your code at a point in time
7. **GitHub** — Website that stores git repos online
8. **Repository (repo)** — A folder tracked by git
9. **Staging** — Selecting which files to include in a commit (like a shopping cart)
10. **Markdown** — Simple text formatting using symbols (#, **, -, etc.)
11. **Silence = success** — Many terminal commands produce no output when they work
12. **`&&`** — Run next command only if the previous one succeeded

---

## Next steps
- [ ] Complete OpenClaw onboarding (`openclaw onboard --install-daemon`)
- [ ] Learn more git commands
- [ ] Start using OpenClaw daily
