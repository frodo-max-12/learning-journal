# What Are AI Agents, Really?

---

## Why This Matters

Everyone says "AI agents" but most people can't explain what one actually is. Today I decided to stop repeating buzzwords and actually understand the concept by reading real code — the same way Andrej Karpathy's nanoGPT teaches transformers through minimal code.

## The Core Idea

A **chatbot** can only talk. An **agent** can **do things**.

The agent loop is:

```
Goal → Think → Use Tools → Observe Results → Think Again → Act/Answer
```

That's it. If an AI can receive a goal, decide which tools to use, take actions, look at what happened, and keep going until the goal is done — it's an agent.

## What I Learned From Claude Code Itself

While using Claude Code, I noticed it spawned a **sub-agent** to do research for me. This led to a real-time lesson:

### Why sub-agents?

1. **Parallel work** — the sub-agent ran ~12 web searches simultaneously instead of doing them one by one
2. **Clean context window** — raw search results fill up the AI's "short-term memory." By delegating to a sub-agent, the main agent keeps its memory clean for conversation. The sub-agent digests everything and returns only a summary.

### The delegation pattern

```
User (me)
  └── Main Agent (Claude — talks to me)
        └── Sub-Agent (worker — does research, returns summary)
```

This is called **orchestration** — a manager agent breaks a big task into pieces and hands them to worker agents. This is a real design pattern used in production agent systems.

## Real-World Analogy

A CEO (user) tells their assistant (main agent) to research something. Instead of the assistant making 12 phone calls while also trying to talk to the CEO, they send an intern (sub-agent) to gather everything and bring back a one-page summary.

## Key Takeaway

An agent = AI + tools + a loop. That's the whole concept. Everything else is implementation details.
