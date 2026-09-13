# MCP vs CLI -- how AI tools connect to the world

*Learned on March 27, 2026. A Composio tweet went viral pitting CLI against MCP, with street interviews in San Francisco and quotes from Garry Tan. I could not tell if they were describing a real debate or just farming engagement. Turns out it was mostly the latter, but untangling the manufactured confusion taught me something real about how AI systems are built.*

---

## The tweet that confused me

Composio, a YC-backed startup, posted a video where they asked developers in San Francisco whether they preferred CLI or MCP. It got 1.1 million views. People were picking sides. Garry Tan and Greg Brockman weighed in. The framing was unmistakable: CLI versus MCP, pick your fighter.

My question was simpler: what the hell are these two things, and why would they be competing?

The answer, after a long conversation, turned out to be: they are not competing. They solve different problems entirely. The "versus" was manufactured -- good marketing, bad education. But the two concepts themselves are genuinely important to understand, especially if you are working with AI tools every day the way I am.

## What CLI actually is

CLI stands for Command Line Interface. It is the way humans talk to computers by typing text commands into a terminal.

When I open my terminal and type `git status`, I am using a CLI. When I type `claude` to start Claude Code, I am using a CLI. The pattern is always the same: a human decides what to do, types a command, and the computer executes it and shows the result.

The key characteristic of a CLI is that **the human is in the loop at every step**. I choose what command to run. I read the output. I decide what to do next. The computer is a tool that waits for my instructions.

This is the oldest and most fundamental way of interacting with a computer. Before graphical interfaces with windows and buttons, the CLI was all there was. And it persists because, for many tasks, it is still the fastest and most precise way to get things done. No hunting through menus, no clicking through dialogs. You type exactly what you want and hit Enter.

## What MCP actually is

MCP stands for Model Context Protocol. Anthropic created it and open-sourced it in late 2024. It is a standardized way for AI models to discover and use external tools.

The problem it solves is straightforward. Imagine you want Claude to interact with your Gmail, Google Drive, Slack, GitHub, and ten other applications. Without a standard, someone would have to write custom integration code for every single combination -- Claude-to-Gmail, Claude-to-Slack, GPT-to-Gmail, GPT-to-Slack, and so on. Every AI platform reinventing the same wheel for every app.

MCP says: here is one standard protocol. If you are an app, build one MCP server. If you are an AI platform, support MCP as a client. Now every app works with every AI platform through the same connection.

The analogy that landed for me was USB. Before USB, every device had its own proprietary connector. Printers had one plug, keyboards had another, cameras had a third. USB said "here is one standard connector, everyone use this." MCP is USB for AI-to-tool connections.

**At the protocol level**, MCP uses JSON-RPC -- structured JSON messages sent over a transport layer (usually stdio or HTTP). It standardizes three things:

1. **Tool discovery** -- the AI agent asks "what can you do?" and the MCP server responds with a list of available tools and their parameter schemas
2. **Tool execution** -- the agent says "call this tool with these parameters" and gets back structured results
3. **Context and authentication** -- handling who is calling, with what permissions

## The fundamental difference: who is driving

This is the crux of it. CLI and MCP answer different questions.

**CLI answers:** How does a human tell a computer what to do?

**MCP answers:** How does an AI agent tell external tools what to do?

Think of it concretely. I have 50 SaaS apps I use for work.

With CLI, I type `composio gmail send --to bob@example.com --body "meeting at 3"`. I chose Gmail. I wrote the arguments. I hit Enter. The CLI is a convenient unified interface so I do not need 50 different command-line tools, but I am still the one making every decision.

With MCP, I tell Claude "email Bob about the meeting tomorrow." Claude queries the MCP server, discovers there is a Gmail tool with a `send_email` function, sees the parameter schema (to, subject, body), constructs the call itself, executes it, and returns the result. The agent chose the tool, figured out the arguments, and handled the execution. I just stated the intent.

| | CLI | MCP |
|---|---|---|
| **Who drives** | Human types commands | AI agent selects tools |
| **Discovery** | Human already knows what to type | Agent queries available tools at runtime |
| **Best for** | Direct, manual, one-shot tasks | Autonomous, multi-step, agent-driven workflows |
| **Speed** | Fast for experts (no overhead) | Overhead of discovery, but scales to complex tasks |
| **Debugging** | Easy (you see exactly what ran) | Harder (agent's reasoning is a black box) |

## Claude Code: the proof they are complementary

The thing that made the relationship between CLI and MCP completely clear was looking at Claude Code itself -- the tool I use every day.

Claude Code is a CLI. I open my terminal, type `claude`, and interact with it by typing prompts. That is the CLI layer -- I am the human steering the ship.

But Claude Code also uses MCP under the hood. When it reads files, runs bash commands, or searches my codebase, it is using tools. And I can extend those tools by connecting MCP servers. I have Google Workspace connected through MCP right now -- Gmail, Drive, Calendar. Claude can search my emails, read my documents, check my schedule. Not because someone hardcoded Google support into Claude Code, but because the agent discovers the tools via MCP at runtime.

So the architecture is layered:

```
Me (human) ---> CLI ---> Claude Code (agent) ---> MCP ---> External tools
                                                            (Gmail, GitHub, Drive, etc.)
```

The CLI is my steering wheel. MCP is the engine's connection to the road. They are not competing any more than a steering wheel competes with an axle. You need both, and they do different jobs.

## So why did Composio manufacture the debate?

Once I understood the technical distinction, the marketing play became obvious.

**Composio's backstory:** Founded in 2023 by Soham Ganatra and Karan Vaidya, both IIT Bombay alumni. Their original product was an MCP/integration platform -- they built connectors to 250+ apps so AI agents could use them via MCP. That was their entire business.

**The problem they hit:** Most developers today are not building fully autonomous agents. They are using Claude Code, Cursor, Copilot -- tools where the human is still driving. These developers do not need MCP's discovery layer for simple tasks. An MCP server running in the background feels like overhead when you just want to type one command.

**Their solution:** They built a CLI wrapper on top of the same integration platform. Now instead of needing an agent to call their MCP server, you can type `composio execute "send a Slack message to #engineering"` directly from your terminal.

**The marketing play:** Instead of announcing "we added a CLI," they turned it into a culture war. CLI vs MCP, street interviews, founder quotes. 1.1 million views. That is not a product announcement; that is a viral campaign.

> The irony is that their CLI almost certainly calls their own integration layer internally -- the same infrastructure built on MCP principles. The CLI is a human-friendly front door over agent-friendly plumbing. They did not replace MCP. They added a second entrance.

Standard startup playbook: pick a fight, ride the discourse, ship the product while everyone is watching. It raised $29 million in two rounds -- a $4M seed in July 2023 from Together Fund and Elevation Capital, and a $25M Series A in July 2025 led by Lightspeed US with Yohei Nakajima (the BabyAGI creator) participating through his agent-focused fund. The "versus" narrative probably helped.

## What MCP means at the protocol level

Since I am trying to understand things at a mechanical level rather than just the vibes, I wanted to go one layer deeper. What actually happens when Claude uses an MCP tool?

The protocol is built on JSON-RPC -- a simple standard for remote procedure calls using JSON. When Claude Code starts up and connects to an MCP server (say, the Google Workspace server), the conversation looks roughly like this:

**Step 1 -- Discovery.** Claude sends a message like: "What tools do you have?" The MCP server responds with a structured list:

```json
{
  "tools": [
    {
      "name": "search_gmail_messages",
      "description": "Search emails by query",
      "parameters": {
        "query": { "type": "string" },
        "max_results": { "type": "integer" }
      }
    },
    {
      "name": "get_events",
      "description": "Get calendar events",
      "parameters": {
        "date_range": { "type": "string" }
      }
    }
  ]
}
```

**Step 2 -- Selection.** Claude reads the schemas, understands what each tool does, and decides which one to call based on my request.

**Step 3 -- Execution.** Claude sends a structured call:

```json
{
  "method": "search_gmail_messages",
  "params": {
    "query": "from:supplier subject:quote",
    "max_results": 5
  }
}
```

**Step 4 -- Response.** The MCP server executes the search, talks to Gmail's API, and returns the results as structured JSON.

The entire exchange is text. Structured, machine-readable text. The AI agent never "sees" Gmail directly -- it sends and receives JSON messages through a standardized protocol. This is why MCP is powerful: any AI model that speaks JSON-RPC can use any MCP server, just like any device with a USB port can use any USB accessory.

## Why both will survive

The San Francisco developers who voted for CLI in that Composio poll were not wrong. For human-driven workflows -- writing code, running tests, deploying apps -- CLI is faster, more predictable, and easier to debug. You do not need the overhead of a discovery protocol when you already know exactly what command to run.

But the agent-infrastructure crowd was not wrong either. As AI agents become more autonomous -- handling multi-step tasks, making decisions about which tools to use, chaining together complex workflows -- MCP becomes essential. An agent cannot type CLI commands. It needs structured schemas, standardized communication, and programmatic tool discovery.

The real architecture of the future is not one or the other. It is:

1. **Human wants to do something manually** -- CLI. Direct, fast, no overhead.
2. **Human wants an AI agent to do something autonomously** -- MCP. The agent needs a structured way to discover and call tools.
3. **Human wants to orchestrate agents via terminal** -- CLI that internally uses MCP. Which is, ironically, exactly what Composio built.

The best tools will support both, because they serve different users at different moments. Sometimes I want to steer. Sometimes I want to say where I am going and let the agent drive.

---

*What I studied next: [CI/CD pipelines and Hugging Face -- the ML developer workflow](cicd-pipelines-and-hugging-face-the-ml-developer-workflow.md), exploring how developers automate testing and deployment, and why ML models need their own platform separate from GitHub.*
