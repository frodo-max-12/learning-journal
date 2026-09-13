# Git worktrees, tmux, and parallel development --- from one repo to eight agents

*Learned on April 2026. I saw people on Twitter running 4-8 Claude Code agents simultaneously in split terminal panes, all working on different features of the same codebase. I wanted to understand how that actually works --- not just copy the commands, but understand the underlying concepts that make it possible.*

---

## The problem: multiple agents, one repo

I already knew how to use Claude Code for single tasks. But the real power move, I kept seeing, was running multiple agents in parallel --- one building authentication, another fixing a bug, a third writing tests, a fourth refactoring the database layer. All at the same time.

The obvious question: if they're all editing the same project, won't they step on each other's toes? If Agent 1 is editing `server.js` to add authentication and Agent 2 is editing the same `server.js` to fix a bug, you have a collision.

This led me to two tools I hadn't encountered before: git worktrees and tmux. Together, they solve the two fundamental problems --- code isolation and terminal management.

## Git worktrees --- the concept

I already knew the basics of git: repositories, branches, commits, merge, pull, push. But I had a mental model that I didn't even realize was limiting me: I thought of a repository as a single folder on disk.

And in the default setup, it is. Your repo lives in one directory. There's a `.git` folder containing all the history, and alongside it are your actual files. When you switch branches with `git checkout`, git rewrites the files in that single directory to match the target branch. Your entire folder transforms.

This means you can only be on one branch at a time. That's fine for a single developer, but it breaks down the moment you want multiple agents working simultaneously.

**A worktree is a second (or third, or eighth) working directory that shares the same underlying git repository.** Each worktree checks out a different branch and has its own independent copy of the project files, but they all point back to the same `.git` database.

The analogy I found helpful: imagine you're studying for four different exams. The "normal git" approach is having one desk --- you clear off the history notes before you can spread out the physics notes. A worktree setup is having four desks in four rooms, each with its own set of notes. But all four desks share the same bookshelf (the `.git` history).

## What the file system actually looks like

Before worktrees:

```
my-project/
├── .git/              # The actual git database (commits, history, all of it)
├── server.js          # Checked out from "main" branch
├── package.json
└── ...
```

After creating three worktrees:

```
my-project/                          # Worktree 1 --- on "main" branch
├── .git/                            # The shared git database lives here
├── server.js (main version)
└── ...

my-project/.claude-worktrees/
├── agent-1/                         # Worktree 2 --- on "claude/agent-1" branch
│   ├── .git                         # A tiny file pointing back to the real .git
│   ├── server.js (agent-1 version)  # Completely independent copy
│   └── ...
├── agent-2/                         # Worktree 3 --- on "claude/agent-2" branch
│   ├── .git                         # Points back to the same real .git
│   ├── server.js (agent-2 version)
│   └── ...
```

Each agent gets its own full copy of all the project files. Agent 1 can edit server.js one way, Agent 2 can edit it a completely different way, and they never interfere.

## How worktrees differ from cloning

My first thought was: couldn't you just `git clone` the repo four times? You could, but there's a key difference.

| | Worktrees | Multiple Clones |
|---|---|---|
| `.git` database | Shared (one copy) | Separate (four copies) |
| Branch visibility | All worktrees see all branches instantly | Each clone is isolated; need push/pull |
| Disk space | Lightweight --- only the files are duplicated | Heavy --- entire history duplicated |
| Merging | Trivial --- everything is already in one repo | Requires push/pull between repos |

Worktrees are lightweight because the heavy part of a git repo --- the entire commit history, all the objects --- lives in the `.git` database, and that's shared. The worktrees only duplicate the actual working files.

## The commands

```bash
# Create a worktree with a new branch
git worktree add ../agent-1 -b claude/agent-1
# This creates the directory ../agent-1,
# creates a new branch "claude/agent-1" from current HEAD,
# and checks it out in that directory.

# List all worktrees
git worktree list
# Shows main worktree + all extras

# Remove a worktree when done
git worktree remove ../agent-1

# Clean up stale references
git worktree prune
```

One important constraint: a branch can only be checked out in one worktree at a time. If `main` is checked out in your primary directory, no worktree can also have `main`. That's why each agent gets its own branch.

## tmux --- the other half of the puzzle

Git worktrees solve the code isolation problem. But you still need to actually run multiple terminal sessions and see them all on one screen. That's where tmux comes in.

tmux stands for "terminal multiplexer." The name sounds intimidating but the concept is simple: it lets you split one terminal window into multiple panes, each running its own independent shell session. It's what creates that impressive grid of small terminal windows people show on Twitter.

The mental model: your terminal is normally a single room with one desk. tmux lets you subdivide that room with dividers, creating multiple workstations. And crucially, tmux sessions persist even if you close the terminal window --- you can "detach" from a session and "reattach" later, finding everything exactly as you left it.

### The essential tmux commands

```bash
# Install
brew install tmux          # macOS

# Start a new session
tmux new -s agents         # -s names the session "agents"

# Split the current pane
Ctrl+b then %              # Split vertically (left/right)
Ctrl+b then "              # Split horizontally (top/bottom)

# Navigate between panes
Ctrl+b then arrow keys     # Move to adjacent pane

# Detach from session (it keeps running)
Ctrl+b then d

# Reattach to session
tmux attach -t agents

# List all sessions
tmux ls
```

The `Ctrl+b` is the "prefix key" --- it tells tmux that the next keypress is a command for tmux, not for whatever program is running in the pane. It takes some getting used to, but it becomes muscle memory quickly.

## Putting it all together: the parallel agent workflow

Here's the full workflow that produces those Twitter screenshots:

**Step 1: Create worktrees for each agent**

```bash
cd my-project
git worktree add .claude-worktrees/agent-1 -b claude/agent-1
git worktree add .claude-worktrees/agent-2 -b claude/agent-2
git worktree add .claude-worktrees/agent-3 -b claude/agent-3
git worktree add .claude-worktrees/agent-4 -b claude/agent-4
```

**Step 2: Start tmux and create a grid**

```bash
tmux new -s agents
# Then split into a 2x2 grid:
# Ctrl+b %    (split right)
# Ctrl+b "    (split bottom-left)
# Navigate to right pane, Ctrl+b "    (split bottom-right)
```

**Step 3: In each pane, cd into a worktree and launch Claude Code**

```bash
# Pane 1
cd .claude-worktrees/agent-1 && claude

# Pane 2
cd .claude-worktrees/agent-2 && claude

# ... and so on
```

**Step 4: Give each agent an independent task**

This is the critical part. The tasks must be independent --- if Task B depends on Task A's output, they can't truly run in parallel. Good candidates:

- Agent 1: Build the authentication system
- Agent 2: Fix the login page bug
- Agent 3: Write unit tests for the API
- Agent 4: Refactor the database queries

**Step 5: Let them cook, then merge**

When agents finish, each one's work is on its own branch. You merge them into main one at a time, just like merging any feature branch:

```bash
git checkout main
git merge claude/agent-1
git merge claude/agent-2
# ... resolve any conflicts as needed
```

## Claude Squad --- the managed version

There's also a tool called Claude Squad (`cs`) that wraps all of this into a nice terminal UI. Under the hood, it does exactly what I described --- tmux sessions plus git worktrees --- but it handles the setup and teardown automatically. Think of it as the "managed" version of what you'd otherwise do manually.

```bash
brew install claude-squad
cs
```

It gives you a dashboard where you can see all your agents, what they're working on, and their status. For someone who runs parallel agents regularly, it removes a lot of boilerplate.

## What clicked for me

The thing I find elegant about this setup is how cleanly it separates concerns. Git worktrees handle the *code isolation* --- making sure agents don't overwrite each other's files. tmux handles the *terminal management* --- letting you see and control multiple sessions from one screen. And Claude Code handles the *intelligence* --- actually understanding and modifying the code.

> Each tool does one thing well. Worktrees isolate code. tmux multiplexes terminals. Claude Code writes code. Composing them gives you something greater than the sum of parts.

There's a deeper lesson here about how developer tools work in general. Unix philosophy: small, sharp tools that compose well. A worktree isn't a complicated feature --- it's just "let me check out a branch in a different folder." tmux isn't magic --- it's just "let me have multiple terminals in one window." But together, they enable a workflow that feels almost futuristic --- watching eight AI agents simultaneously building different parts of your app.

I also realized that understanding worktrees taught me something about git itself. I'd been thinking of a git repo as "the folder on my computer." But a repo is really the `.git` database --- the history, the commits, the objects. The working directory is just one *view* into that database. Worktrees make this visible by giving you multiple views into the same database. Once you see it that way, git's architecture makes a lot more sense.

---

*What I studied next: Git internals --- how commits, trees, and blobs actually work under the hood*
