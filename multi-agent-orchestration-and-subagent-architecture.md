# Multi-Agent Orchestration & Sub-Agent Architecture

---

## What I learned today

### 1. Claude Code Agent Teams

Agent teams let you spawn **multiple Claude sessions** that work together like a dev team:

- **Team lead** — your main Claude session that coordinates everything
- **Teammates** — independent Claude sessions the lead spawns
- **Shared task list** — everyone sees what needs doing and claims tasks
- **Mailbox system** — teammates can message each other directly, not just through the lead

#### How to enable it

Agent teams are experimental. You enable them by adding this to `~/.claude/settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

#### How to use it

You describe what you want in plain English and Claude handles the orchestration:

```
Create an agent team with 3 teammates:
- One on backend API
- One on frontend UI
- One on database schema
```

Navigate between teammates with **Shift+Down** arrow.

### 2. The `settings.json` File

This is Claude Code's main config file, stored at `~/.claude/settings.json`. It's a hidden file (the `.` in `.claude` means hidden on Mac). To see hidden files in Finder: **Cmd + Shift + .**

My current settings and what each line does:

| Setting | What it does |
|---------|-------------|
| `effortLevel: "high"` | Tells Claude to think harder |
| `skipDangerousModePermissionPrompt` | Skips a confirmation screen |
| `attribution: { commit: "", pr: "" }` | No bot co-author tags on commits |
| `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Enables the agent teams feature |

### 3. Built-In Sub-Agent Types (Deep Dive)

Claude Code has **4 built-in sub-agents** it uses behind the scenes. I discovered these by watching the tool calls in my conversation:

| Agent | Tools it has | What it does |
|-------|-------------|-------------|
| **claude-code-guide** | Glob, Grep, Read, WebFetch, WebSearch | Researches Claude Code docs and features |
| **Explore** | Read-only tools | Searches your codebase quickly |
| **Plan** | Read-only tools | Designs implementation plans |
| **general-purpose** | All tools | Does everything — research + code changes |

#### Key insight: claude-code-guide is read-only

The `claude-code-guide` agent can **only look things up** — it cannot edit files, run commands, or spawn its own agents. It's locked down on purpose: its job is research, not action.

#### How it works (the flow I observed)

```
1. I asked Claude about agent teams
2. Claude thought: "I need to look this up"
3. Claude spawned: claude-code-guide sub-agent
4. Sub-agent: searched docs with WebSearch and WebFetch
5. Sub-agent: returned a summary to the main Claude
6. Main Claude: used that summary to answer me
```

This is the same **orchestration pattern** from the AI agent loop — a manager delegates to a specialist worker.

### 4. Sub-Agents vs Agent Teams

These are related but different concepts:

| | Sub-Agents | Agent Teams |
|---|-----------|------------|
| **Who uses them** | Claude (behind the scenes) | You (the user) |
| **Communication** | Report back to main agent only | Teammates message each other |
| **Best for** | Quick focused lookups | Complex collaborative work |
| **Cost** | Lower (summarized results) | Higher (each is a full session) |

## Key takeaway

Claude Code isn't one AI — it's a system of specialized AIs that delegate to each other. The same pattern (orchestration) powers both the hidden sub-agents and the user-facing agent teams feature. Understanding the tool calls reveals how the system actually works under the hood.
