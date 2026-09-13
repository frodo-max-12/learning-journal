# Mapping the AI browser-agent ecosystem --- what fits where in the stack

*Learned on April 2026. After writing [the headless-browsers entry](./headless-browsers-and-ai-agent-browsing.md), I had a clean mental model of three tools (Lightpanda, Browser Use, Stagehand) and a 5-level spectrum from "human browses Chrome" to "LLM drives Lightpanda." Then Claude did a deep GitHub search for me and came back with forty more projects in this space, grouped into five categories I had never heard of: SDK frameworks, purpose-built browsers, MCP servers, computer-use agents, natural-language automation. My immediate question: where does all of this fit in the mental model I already built?*

---

## The starting point --- the stack I already understood

In [the previous entry](./headless-browsers-and-ai-agent-browsing.md) I drew a three-layer stack: agent framework on top (Browser Use, Stagehand), automation library in the middle (Playwright / CDP), browser at the bottom (Chrome, Lightpanda). That stack is still correct. The bad news: each layer has an entire *category* of projects competing inside it, and there are two new layers above the stack that I didn't know about. Let me map them in.

## The expanded stack

Here is the same stack, but zoomed out to show every category I now know exists:

```
┌─────────────────────────────────────────────┐
│  Orchestration / protocol layer             │  ← Claude Code, Cursor, IDE agents
│  (MCP servers live here)                    │    connect to browsers via MCP
├─────────────────────────────────────────────┤
│  Agent framework (SDK)                      │  ← Browser Use, Stagehand, Skyvern,
│                                             │    LaVague, Magnitude, Agent-E
├─────────────────────────────────────────────┤
│  Vision / perception overlay (optional)     │  ← UI-TARS, OmniParser, Tarsier
│                                             │    (only for vision-first approaches)
├─────────────────────────────────────────────┤
│  Automation library                         │  ← Playwright, Puppeteer, Selenium
├─────────────────────────────────────────────┤
│  Browser                                    │  ← Chrome, Lightpanda, Steel Browser,
│                                             │    BrowserOS, Firefox, WebKit
├─────────────────────────────────────────────┤
│  Operating system / device                  │  ← Linux / macOS / sandboxed container
└─────────────────────────────────────────────┘
```

Three things to notice:

1. **The agent layer split in two.** There's the *framework* (Browser Use, Stagehand) that gives you a programming API, and there's the *perception overlay* --- separate projects whose only job is to convert a screenshot into "what's clickable on this page?"
2. **A new layer on top.** MCP servers sit *above* agent frameworks. They let an external agent (like Claude Code in my terminal) reach into a browser without me writing any Python or TypeScript code.
3. **Below the browser, the OS shows up.** Some tools don't just drive a browser --- they drive the whole desktop. That's a larger category ("computer-use agents") that contains browser automation as a special case.

Now let me walk through each category with the specific projects that live there.

## Category 1 --- SDK frameworks (the Browser Use / Stagehand category)

These are libraries you import in Python or TypeScript. They wrap Playwright and add an LLM brain. You describe a goal, they figure out the steps.

| Project | Stars | Language | What makes it distinct |
|---------|-------|----------|------------------------|
| browser-use | ~86k | Python | The reference implementation; supports local models |
| Stagehand | ~22k | TypeScript | Three clean primitives (`act`, `extract`, `observe`) you mix with raw Playwright |
| Skyvern | ~20k | Python | Vision-first, plus a no-code workflow builder on top |
| Midscene (ByteDance) | ~12k | TypeScript | Works on web *and* Android / iOS / desktop |
| LaVague | ~6.3k | Python | Compiles natural language into actual Selenium / Playwright code |
| Magnitude | ~4k | TypeScript | Pure vision --- never looks at the DOM, only at screenshots |
| Notte | ~1.8k | Python | Turns a page into a text-based "action API" the LLM calls |
| HyperAgent | ~1.2k | TypeScript | Extends Playwright with `page.ai()` and `page.extract()` |
| Agent-E | ~1.2k | Python | Research project, hierarchical DOM-distillation |

**The axis of variation inside this category:** how does the framework show the page to the LLM?

- *DOM-serialization* (Browser Use, Stagehand) --- send a cleaned-up text version of the HTML
- *Vision* (Magnitude, Skyvern) --- send a screenshot
- *Hybrid* (most of the others) --- send both and let the model choose

This matters for cost and latency. A DOM text is ~5k tokens for a typical page. A screenshot plus the DOM is ~20k tokens. Ten steps into a task, the difference compounds.

## Category 2 --- Purpose-built browsers (the Lightpanda category)

These are browsers rebuilt from the ground up for machine consumers. Lightpanda is the most radical example (no rendering at all), but there are softer versions too.

| Project | Stars | Language | What makes it distinct |
|---------|-------|----------|------------------------|
| Lightpanda | ~23k | Zig | Extreme version: no rendering, no CSS, no images --- just DOM + V8 |
| Steel Browser | ~6.8k | TypeScript | Full Chromium + built-in stealth, proxies, sessions, Docker deploy |
| BrowserOS | ~5-7k | C++/TS | Full Chromium fork with a built-in agent runtime baked in |

**The axis of variation:** how much of Chrome do they keep?

- *Strip everything* (Lightpanda) --- fastest, cheapest, breaks on visual-only sites
- *Keep everything, add agent plumbing* (Steel, BrowserOS) --- slower, but handles any site Chrome can

This is the classic engineering trade-off: specialization vs. generality. Lightpanda is like a Formula-1 car --- perfect on a clean track, useless in traffic. Steel is like a rally car --- slower on the track but handles any terrain.

## Category 3 --- MCP servers (the new layer I hadn't seen)

This is the category that genuinely extends my model. An MCP server is a small program that exposes browser-control tools (navigate, click, screenshot, extract) over the Model Context Protocol --- the same protocol I wrote about in [mcp-vs-cli](./mcp-vs-cli-how-ai-tools-connect-to-the-world.md).

The difference from a framework: with Browser Use I write Python code that calls the LLM. With an MCP server I do nothing --- I configure Claude Code (or Cursor, or any MCP-speaking agent) to connect to it, and now *Claude Code itself* can browse the web while it helps me.

| Project | Stars | Who maintains it | Distinct angle |
|---------|-------|------------------|----------------|
| chrome-devtools-mcp | ~33k | Official Chrome team | CDP-level inspect + control, aimed at coding agents |
| playwright-mcp | ~30k | Official Microsoft | Accessibility-tree snapshots instead of screenshots |
| Browser MCP | ~5.7k | Community | Uses *your* logged-in Chrome profile (so cookies, sessions work) |
| mcp-server-browserbase | ~2.5k | Browserbase | Cloud Stagehand behind an MCP interface |

**Where this fits in my existing knowledge:** this is the same pattern as [how MCP connects LLMs to tools](./tcp-ip-protocols-and-how-mcp-fits-in.md), just specialized for browsers. The MCP server is the universal adapter; the browser is the device being adapted.

> The mental shift: **an MCP server turns a browser into a callable tool.** Everything I already know about MCP for file systems, databases, or APIs applies directly --- the "resource" this time just happens to be a running Chrome.

## Category 4 --- Computer-use agents (one level of abstraction larger)

These don't just drive a browser. They drive the whole desktop. The browser is one window among many.

| Project | Stars | Language | Distinct angle |
|---------|-------|----------|----------------|
| UI-TARS (ByteDance) | ~27k | Python | GUI-native vision-language model --- screens as input, not DOM |
| OmniParser (Microsoft) | ~24k | Python | Screenshot → structured element list for any GPT-4V-class model |
| open-interpreter | ~62k | Python | Natural-language interface for the whole computer |
| self-operating-computer | ~10k | Python | Multimodal agent framework with OCR mode |
| bytebot | ~7-10k | TypeScript | Self-hosted Linux desktop agent in a container |

**Why this category exists:** some tasks can't be done in a browser. Opening a PDF, running a local script, manipulating a spreadsheet, dragging files between apps. A computer-use agent treats the browser as just-another-app it can click through.

**The trade-off:** computer-use agents are slower, more expensive (every step is a screenshot + VLM call), and less reliable than browser-specific agents. But they generalize to anything you can do with a mouse and keyboard, including things nobody built an API for.

## Category 5 --- Perception / vision overlays (components, not end-tools)

These aren't agents you'd use directly. They're *pieces* that other agent frameworks plug in. I'm listing them so the names don't confuse me when they appear in other projects' documentation.

- **Tarsier** (~1.8k) --- adds `[23]` style bracket labels to every interactive element on a page, so the LLM can say "click element 23" unambiguously
- **OmniParser** (~24k) --- turns a raw screenshot into a list of structured elements with bounding boxes
- **reworkd/AgentQL** (~1k) --- a natural-language query language for finding elements

If you see these mentioned inside another project's dependencies, they're probably doing the "help the LLM see the page" job.

## Where each category sits in the stack (consolidated)

Returning to the layered picture, here's where the categories live:

| Layer | Category | Example projects |
|-------|----------|------------------|
| Orchestration | **MCP servers** | playwright-mcp, chrome-devtools-mcp |
| Agent framework | **SDK frameworks** | Browser Use, Stagehand, Skyvern |
| Perception overlay | **Vision components** | Tarsier, OmniParser |
| Automation library | **Playwright / Puppeteer / Selenium** | Playwright (dominant) |
| Browser | **Purpose-built browsers** | Chrome, Lightpanda, Steel |
| OS / desktop | **Computer-use agents** (wraps browser) | UI-TARS, bytebot |

Reading this table top-to-bottom is reading the stack from "closest to the user's intent" to "closest to the metal."

## Where this fits in my overall CS learning

Stepping back, I can now see how this ecosystem connects to the foundations I've been building up:

- **[State](./state-the-concept-behind-all-of-computing.md)** --- every layer in the stack has state (Chrome has DOM state, Playwright has session state, the LLM has conversation state). Debugging agents is mostly about figuring out *which layer's state is wrong*.
- **[MCP and protocols](./mcp-vs-cli-how-ai-tools-connect-to-the-world.md)** --- CDP, WebDriver, and MCP are the three protocols binding this stack together. Each one was invented to solve a specific coupling problem.
- **[Frontend architecture](./frontend-architecture-html-css-js-and-frameworks.md)** --- the DOM I learned about there is the same DOM these agents read. The reason vision-first agents exist is that modern frontends are increasingly canvas-rendered (think Figma, Linear) and the DOM is empty.
- **[Transformers](./how-transformers-work-attention-is-all-you-need.md)** --- the "brain" in every agent framework is a transformer. The fact that transformers are expensive per token is why DOM-serialization vs. vision matters so much.
- **[Multi-agent orchestration](./multi-agent-orchestration-and-subagent-architecture.md)** --- the larger frameworks (Skyvern, Agent-E) use sub-agents internally. A planner agent decides the high-level steps, an executor agent drives the browser, an extractor agent pulls structured data.
- **[Turing / theory of computation](./theory-of-computation-turing-church-and-the-halting-problem.md)** --- an interesting aside: a web agent is a *universal interface* in the Turing sense. It can, in principle, perform any task a human can do in a browser. Whether it *reliably* does so is the whole open research problem.

## The question that unlocked the whole map

What stuck with me is that the categories aren't really competing --- they're answering *different questions*:

- SDK frameworks answer: "How do I write code that lets an LLM browse?"
- Purpose-built browsers answer: "How do I make browsing cheaper for machines?"
- MCP servers answer: "How do I let my existing agent (Claude Code, Cursor) browse without writing new code?"
- Computer-use agents answer: "What if browsing isn't enough and I need the whole desktop?"
- Vision overlays answer: "How do I help the LLM actually see the page?"

A mature stack ends up using pieces from all five. For example, a real production setup might be:

> A **Skyvern** agent (SDK framework, vision-first) driving **Steel Browser** (purpose-built browser with stealth) in a container, exposed to Claude Code via a custom **MCP server**, with **Tarsier** labeling elements for the LLM.

That's a five-layer cake. Six months ago I would have seen "AI browser automation" as one thing. Now I see it as a small, well-defined ecosystem where each layer has a name, a trade-off, and a reason to exist.

## What I want to try next

Given I already have browser-use, Stagehand, and Lightpanda, the highest-value additions look like:

1. **Skyvern** --- genuinely different approach (vision-first + workflow builder), closest in spirit to what I already run
2. **Steel Browser** --- pairs with Lightpanda as the full-Chromium fallback for sites that Lightpanda can't handle
3. **playwright-mcp or chrome-devtools-mcp** --- lets Claude Code drive a browser directly, no SDK code required from me
4. **UI-TARS or bytebot** --- step outside the browser-only world and see how much harder full-desktop agents actually are

The bookmark to keep: **steel-dev/awesome-web-agents** on GitHub --- the most-maintained running list of this entire ecosystem.

---

*What I studied next: [to be decided] --- probably the MCP wire protocol in detail, since four of the projects above are MCP servers and I want to know what actually flows over that wire.*
