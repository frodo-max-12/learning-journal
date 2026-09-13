# Headless browsers and AI-agent browsing --- why Lightpanda, Browser Use, and Stagehand exist

*Learned on April 2026. I installed three tools that all promised to make the web "accessible to AI agents" --- Lightpanda, Browser Use, and Stagehand --- and immediately hit a wall: two of them asked for an LLM API key. Why does a browser need an API key? What does "headless" even mean? And how do these relate to Playwright and Puppeteer, which I already wrote about [here](./comparing-browser-automation-playwright-selenium-puppeteer.md)?*

---

## What a browser actually is (unpacking the thing I use every day)

When I open Chrome and visit a page, I experience it as one smooth motion: I type a URL, the page appears, I read it, I click things. But Chrome is actually a stack of completely separate systems bolted together. To understand headless browsers, I had to see this stack clearly.

1. **Networking** --- makes HTTP requests to servers, gets HTML / CSS / JavaScript back
2. **HTML parser** --- turns the raw HTML text into a DOM (Document Object Model), which is a tree structure of elements
3. **CSS engine** --- figures out how each element should look: colors, sizes, fonts
4. **Layout engine** --- calculates *where* everything goes on the page in pixels
5. **Renderer / compositor** --- actually paints pixels onto the screen, using the GPU
6. **JavaScript engine** --- V8 in Chrome, JavaScriptCore in Safari --- runs all the JS that websites ship
7. **Font rendering, image decoding, audio, video codecs, GPU acceleration...**

Chrome does ALL of this because a human needs to *see* the page. About 70% of the code in a modern browser is dedicated to making the page look right for human eyes.

## What "headless" means

**Headless** means "no visible window." The browser runs completely invisibly --- it still downloads pages, still parses HTML, still runs JavaScript, still builds the DOM --- but it doesn't render anything to a screen. There's no window to look at.

Why would anyone want a browser nobody can see? Three reasons:

1. **Automated testing.** If I've built a website, I want a robot to click through the checkout flow every night and confirm it still works. The robot doesn't need to see pretty pixels --- it just needs to know "did the order go through?"
2. **Web scraping.** Extract structured data from thousands of pages. The computer doesn't need to see the page to read the HTML.
3. **AI agents browsing the web.** A language model needs to read pages, click links, fill forms --- but it doesn't look at pixels. It reads the DOM.

Chrome itself has a headless mode: run `chrome --headless` and it behaves the same as normal Chrome, just without the window. This is what Playwright and Puppeteer have been driving for years.

## The observation that changed things

If an LLM is going to browse the web, it doesn't care about colors, fonts, images, animations, or GPU compositing. It only reads the DOM. So why are we paying the cost of rendering all those pixels just to throw them away?

This is the insight behind **Lightpanda**.

## Lightpanda --- rethinking the browser for machines, not humans

Lightpanda is a headless browser built from scratch in Zig (a newish low-level language, like C but safer). The founders looked at Chrome and stripped out every system that exists purely for humans:

- No CSS parsing --- machines don't care if text is red
- No image decoding --- an LLM doesn't look at images (the Vision models get images differently)
- No GPU compositing --- there's no screen to composite to
- No font rendering --- text is just text to a DOM consumer

What's left? Just the networking, HTML parsing, DOM construction, and the V8 JavaScript engine. The parts a machine reader actually uses.

**Results they claim:** ~11x faster than Chrome headless on the same workload, ~9x less memory. If both claims hold together, that's ~100x less compute per page. Real-world numbers are smaller but still dramatic.

**Compatibility trick:** Lightpanda still speaks the Chrome DevTools Protocol (CDP). So any existing tool that was built to drive Chrome --- Playwright, Puppeteer, my Claude-in-Chrome extension, MCP tools --- can just point at Lightpanda instead of Chrome and keep working. Drop-in replacement.

**The trade-off.** Because Lightpanda doesn't render, it can't help when a site uses canvas rendering, icon-only buttons without accessible labels, or other visual-only affordances. For text-heavy sites (news, docs, Reddit, HN, GitHub) it flies. For image-heavy or canvas-based UIs, it falls back.

## What Browser Use and Stagehand actually do (and why they're different from Lightpanda)

This is where I was confused. Lightpanda is a *browser*. Browser Use and Stagehand are *not* browsers --- they're **agent layers** that sit on top of a browser (usually Chrome via Playwright) and add intelligence.

### The stack, cleanly separated

```
┌─────────────────────────────────────────────┐
│  Agent layer (Browser Use / Stagehand)       │  ← uses an LLM to decide what to do
├─────────────────────────────────────────────┤
│  Automation library (Playwright / CDP)       │  ← translates decisions into clicks
├─────────────────────────────────────────────┤
│  Browser (Chrome / Lightpanda / WebKit)     │  ← does the actual HTML / JS work
└─────────────────────────────────────────────┘
```

Each layer is independent. You can mix and match.

### Why Browser Use and Stagehand need an LLM API key

**Because the LLM is the brain.**

With raw Playwright, I have to write the brain myself:

```python
# I write the specific logic
await page.goto("https://news.ycombinator.com")
top_story = await page.locator(".titleline a").first
title = await top_story.text_content()
```

I had to know that the CSS class is `.titleline`. If HN redesigns tomorrow, my code breaks.

With Browser Use, I describe a goal in natural language:

```python
agent = Agent(
    task="Go to Hacker News and tell me the title of the top story",
    llm=ChatAnthropic(model="claude-opus-4-6")
)
await agent.run()
```

What actually happens inside:

1. Browser Use opens a real browser (via Playwright)
2. It navigates to news.ycombinator.com
3. It takes the DOM of the page and serialises it into a simplified text representation the LLM can read
4. It sends that representation + the task to Claude via the Anthropic API
5. Claude responds with a decision: *"I can see a list of stories. The first title I find is 'Show HN: Lightpanda...'. The task is complete."*
6. Browser Use returns that answer

**Every decision step is an API call.** Every time the agent needs to figure out "what should I do next?", it sends the page state to an LLM, pays for the tokens, and waits for the response. That's why I need an API key --- it identifies me and bills my account.

Stagehand works the same way. It exposes three primitives:
- `act("click the login button")` --- LLM figures out which element that means
- `extract("get the price", schema)` --- LLM reads structured data from the page
- `observe("what interactive elements are on this page?")` --- LLM introspects

Each primitive call is an LLM API call under the hood.

### Lightpanda doesn't need an API key because it's not intelligent

Lightpanda is just a browser. It does exactly what you program it to do: fetch this URL, run this JS, return this DOM. There's no decision-making --- no "brain" --- so there's nobody to pay for thinking. You could pair Lightpanda with an LLM to build your own agent (and that would need an API key), but Lightpanda itself is a pure execution engine.

## The spectrum --- from Chrome to AI agents

This is the mental model I finally arrived at:

| Level | What I use | Who decides | Example |
|-------|------------|-------------|---------|
| 0 | Chrome, day-to-day | **Me** (human) | Browsing news, reading docs |
| 1 | Chrome headless | **My code** (hardcoded) | A cron job that screenshots my homepage daily |
| 2 | Chrome + Playwright | **My code** (structured) | Automated tests for a website |
| 3 | Chrome + Playwright + LLM (Browser Use, Stagehand) | **An LLM** (dynamic) | "Book me the cheapest flight from Pune to Delhi next Friday" |
| 4 | Lightpanda + Playwright + LLM | **An LLM** (dynamic, faster) | Same as Level 3 but 10x cheaper per page |

Going from Level 0 to Level 4 is a journey of moving the decision-making from a human brain, to hand-written code, to an LLM. At each step, the browser itself became less important (just a mechanism) and the "who decides what to click" question became more interesting.

## Playwright and Puppeteer revisited --- the plumbing layer

I wrote [a separate entry](./comparing-browser-automation-playwright-selenium-puppeteer.md) on Selenium, Puppeteer, and Playwright, but here's the short version in context:

- **Puppeteer** (2017, Google, Node.js) --- the first library to drive Chrome via the Chrome DevTools Protocol directly, instead of going through WebDriver. Fast, clean, but Chrome-only and JavaScript-only.
- **Playwright** (2020, Microsoft, mostly ex-Puppeteer team) --- the same idea but supporting Chromium, Firefox, and WebKit, in Python, Node, Java, C#. Cleaner auto-waiting, modern API. It has become the industry default.

Browser Use is built on Playwright. Stagehand is built on Playwright. Even my Claude-in-Chrome extension is essentially a Playwright-ish driver under the hood.

**Playwright is the plumbing layer that connects the decision-making (code or LLM) to the actual browser.** Without it, every agent library would have to re-implement "how do I click an element, wait for navigation, extract text" from scratch.

## Putting it together --- what I actually installed today

I now have three tools in `~/agent-browsers/`:

1. **Lightpanda (60 MB binary).** A pure headless browser, no brain. I ran `./lightpanda fetch --dump https://example.com` and it returned the HTML instantly. No API key needed.

2. **Browser Use (365 MB Python env).** Agent framework. Uses Playwright to drive Chrome + an LLM to decide. Won't do anything useful until I add an Anthropic / OpenAI / Google API key.

3. **Stagehand (224 MB Node project).** Agent SDK by Browserbase. Three clean primitives (`act`, `extract`, `observe`). Same architecture: Playwright + LLM. Same API key requirement.

The interesting experiment now: pair Lightpanda (level 4 browser) with Browser Use (agent layer) and see if it works. Browser Use was built assuming Chrome, but since Lightpanda speaks CDP, it should be a straight swap. If that holds, I've got the cheapest-per-page AI agent stack possible today.

## Why all this matters

The web was designed for humans. Browsers were designed for humans. For the last 30 years, every engineering decision in browser development was about making pages look and feel better for eyeballs. The "AI agents browsing the web" use case is so new that most browsers are wildly over-engineered for it.

This is why the category exploded in 2025–2026. Three things converged:

1. LLMs got good enough at reasoning over DOMs to actually make decisions
2. Infrastructure providers (Browserbase, Steel) made cloud-hosted browsers cheap and reliable
3. Someone finally asked: "What if we built a browser *only* for machines?" → Lightpanda

The next interesting question is whether the web itself starts changing to be machine-friendly (structured data, agent-optimized APIs) or whether browsers keep adapting to scrape an increasingly hostile visual web. Probably both, for a while.

## Key concepts to remember

- **Headless** = browser without a screen. Still a real browser, just invisible.
- **DOM** = the tree structure a browser builds from HTML. This is what both rendering code and LLMs actually read.
- **CDP (Chrome DevTools Protocol)** = the JSON-over-WebSocket API that Chrome exposes so outside programs can control it. Puppeteer, Playwright, and Lightpanda all speak it.
- **Playwright / Puppeteer** = libraries that speak CDP so your code can drive a browser.
- **Browser Use / Stagehand** = agent frameworks that put an LLM on top of Playwright. The LLM is the brain, Playwright is the body, the browser is the hands.
- **Lightpanda** = a new browser built only for machines. Skips everything humans need. Talks CDP, so existing tools work against it.
- **Why LLM-based agents need API keys** = the LLM is what thinks, and the LLM runs in Anthropic / OpenAI / Google's data centers. Every decision is a paid API call.
