# Playwright, Selenium, and Puppeteer --- the evolution of browser automation

*Learned on April 2026. I kept encountering these names --- Playwright, Selenium, Puppeteer --- without understanding how they relate to each other or why there are three tools that seem to do the same thing. The question that triggered this was simple: "I use Claude's MCP-in-Chrome extension. How does that fit into all of this?"*

---

## What browser automation actually means

Before getting into the tools, I needed to understand the problem they solve. Sometimes you need a program to control a web browser --- open a page, click buttons, fill in forms, read text, take screenshots, run through a checkout flow. The reasons vary: testing (does our website actually work?), scraping (extract data from a site), monitoring (check if a page is down), or increasingly, letting an AI agent navigate the web.

The fundamental challenge: browsers are designed for humans. They expect mouse clicks and keyboard input. Making software drive a browser requires some protocol that translates "click the Submit button" into something the browser understands. That protocol, and the libraries that speak it, is what we mean by browser automation.

## Selenium --- the pioneer (2004)

Selenium is the oldest of the three, and for a long time it was the only serious option. It was created in 2004 by Jason Huggins at ThoughtWorks, originally as an internal testing tool.

Selenium works through a protocol called **WebDriver**. Think of WebDriver as a standardized remote control for browsers. The idea is elegant in principle: instead of having a different tool for Chrome vs Firefox vs Safari, WebDriver defines a standard set of commands (navigate to URL, find element, click, type text), and each browser provides its own "driver" that translates these commands into browser-specific actions.

```
Your test script
    → Selenium library (Python, Java, JS, etc.)
        → WebDriver protocol (HTTP commands)
            → Browser Driver (chromedriver, geckodriver, etc.)
                → The actual browser
```

The strength of this architecture is breadth: Selenium supports every major browser and works with practically any programming language. It's been the industry standard for automated web testing for twenty years.

The weakness is everything else. The multi-layer architecture introduces latency and flakiness. You need to download the correct browser driver and keep it in sync with your browser version (Chrome 124 needs chromedriver 124, etc.). Tests often fail not because the website is broken but because the automation is unreliable --- elements not being found, timing issues, stale references. Developers have spent millions of collective hours writing "wait for element to appear" workarounds.

## Puppeteer --- Chrome gets a direct line (2017)

Google released Puppeteer in 2017, and it took a fundamentally different approach. Instead of going through the WebDriver abstraction layer, Puppeteer talks to Chrome directly using the **Chrome DevTools Protocol (CDP)**.

CDP is the same protocol that powers Chrome's developer tools --- when you hit F12 and inspect elements, that's CDP at work. It provides deep, low-level access to everything Chrome is doing: the DOM, network requests, JavaScript execution, performance metrics, even screenshot capture. By speaking CDP directly, Puppeteer cuts out the middleman.

```
Your test script
    → Puppeteer (Node.js library)
        → Chrome DevTools Protocol (WebSocket)
            → Chrome/Chromium
```

The result: Puppeteer is faster, more reliable, and more capable than Selenium for Chrome-based automation. It has native support for things Selenium struggles with --- intercepting network requests, emulating mobile devices, generating PDFs, capturing performance traces.

The tradeoff is scope. Puppeteer only works with Chrome/Chromium. If you need to test on Firefox or Safari, Puppeteer can't help. And it only has a Node.js (JavaScript) API, so if your team writes tests in Python or Java, you're out of luck.

## Playwright --- the best of both worlds (2020)

Playwright was released by Microsoft in 2020, and here's the twist: it was built by the same engineers who created Puppeteer at Google. They left Google, joined Microsoft, and essentially built "Puppeteer 2.0" --- fixing the limitations while keeping the strengths.

```
Your test script
    → Playwright (JS, Python, Java, or .NET)
        → Browser-specific protocol (CDP for Chromium, internal for Firefox/WebKit)
            → Chrome, Firefox, or Safari
```

Playwright brings several key improvements:

**Cross-browser support.** It works with Chromium (Chrome, Edge), Firefox, and WebKit (Safari's engine). Unlike Selenium, which uses the generic WebDriver protocol, Playwright maintains deep integration with each browser's internals. This means you get Puppeteer-level reliability across all three engines.

**Auto-waiting.** This is perhaps the most developer-friendly feature. In Selenium, if you try to click a button that hasn't loaded yet, the test fails. Developers write explicit "wait for element" code everywhere. Playwright automatically waits for elements to be visible, enabled, and stable before interacting with them. It just works.

**Modern async API.** Playwright was designed from scratch for modern async/await patterns. It handles multiple pages, iframes, and browser contexts natively, without the awkward workarounds that Selenium requires.

**Built-in test runner.** Playwright comes with its own test framework, including parallel test execution, automatic retries, HTML reports, and trace viewing (a recording of exactly what happened during a test, with screenshots at each step).

## The evolution at a glance

| | Selenium | Puppeteer | Playwright |
|---|---|---|---|
| Released | 2004 | 2017 | 2020 |
| Created by | ThoughtWorks | Google | Microsoft (ex-Puppeteer team) |
| Protocol | WebDriver | CDP (Chrome DevTools) | CDP + browser-specific protocols |
| Browsers | All major | Chrome only | Chrome, Firefox, Safari |
| Languages | Many (Python, Java, JS, C#, Ruby) | JavaScript only | JS, Python, Java, .NET |
| Auto-waiting | No (manual waits) | Partial | Yes (built-in) |
| Speed | Slowest | Fast | Fast |
| Best for | Legacy projects, broad compatibility | Chrome-specific tasks, Google ecosystem | New projects, modern testing |

The pattern is clear: each generation solves the previous generation's pain points while keeping its strengths. Selenium proved the concept but was clunky. Puppeteer proved that direct browser communication was better but was too narrow. Playwright took the best of both and made it work everywhere.

## Headless vs headed --- a concept that keeps coming up

All three tools can run browsers in two modes:

**Headed mode** means the browser window is visible on screen. You can literally watch the automation clicking through pages. This is useful for debugging --- you can see exactly where things go wrong.

**Headless mode** means the browser runs invisibly in the background. No window appears. The browser still renders pages, executes JavaScript, and processes everything normally --- you just can't see it. This is what you want for automated testing in CI/CD pipelines, for web scraping, or for any situation where you don't need a human watching.

Headless mode is also significantly faster because the browser doesn't need to spend resources actually painting pixels on screen.

## Where Claude's MCP-in-Chrome fits

This is where it gets interesting and where my original question came from. Claude has a Chrome extension that lets it see and interact with web pages. How does that relate to Playwright and friends?

The answer involves understanding the *layers* of the stack:

```
Claude (the LLM)              --- decides WHAT to do
    ↓
MCP server (interface)         --- translates intent into tool calls
    ↓
Browser automation layer       --- actually controls the browser (CDP/Playwright)
    ↓
Chrome browser                 --- renders and displays web pages
```

Selenium, Puppeteer, and Playwright are all **hands** --- they execute specific, pre-defined actions. "Click this button." "Type this text." "Navigate to this URL." They do exactly what you tell them, no more.

Claude's MCP-in-Chrome extension adds a **brain** on top. Claude *sees* the page (via screenshots or DOM extraction), *understands* what's on it, and *decides* what to do next. The MCP (Model Context Protocol) layer provides a standardized interface between Claude's intelligence and the browser's capabilities --- exposing actions like "navigate," "click," "get page text," and "screenshot" as tools Claude can call.

> The insight: Playwright and friends automate browsers. Claude automates the *thinking about what to automate*. MCP is the bridge between the two.

This is a qualitative shift. With Playwright, you write a script: "go to this URL, find the element with ID login-button, click it, wait for the next page, find the element with ID username..." It's brittle --- if the page changes, your script breaks. With an LLM in the loop, the system can adapt: "I see a login button in the top right. Let me click it." It doesn't matter if the button's ID changed or if the layout shifted.

## When to use which

After understanding all of this, the decision framework became clear:

**Use Playwright** when you're writing automated tests for a web application, building a web scraper with predictable targets, or doing any browser automation where you know in advance what steps to take. It's the modern default and there's no good reason to choose Puppeteer or Selenium for new projects (unless you're maintaining a legacy Selenium test suite).

**Use Selenium** only if you're working with an existing codebase that already uses it, or if you need a language binding that Playwright doesn't support (Ruby, for instance).

**Use Puppeteer** if you're doing Chrome-specific work (generating PDFs, capturing performance traces) and you're already in a Node.js environment. Even here, Playwright can usually do the same thing.

**Use Claude + MCP** when the task requires judgment, adaptation, or understanding of content --- when you can't write the steps in advance because they depend on what's actually on the page. This is the frontier: AI-driven browser automation where the agent figures out the steps itself.

## The bigger pattern

What struck me about this evolution is how it mirrors a pattern I've seen elsewhere in software: tools start as general-purpose but clunky (Selenium), get refined for specific use cases (Puppeteer for Chrome), then get generalized again at a higher level of abstraction (Playwright for all browsers), and finally get an intelligence layer on top (LLM-driven automation).

It's like the history of transportation: walking (general but slow), trains (fast but fixed routes), cars (fast and flexible), self-driving cars (fast, flexible, and they figure out the route themselves). Each generation doesn't replace the previous one entirely --- trains still exist --- but the frontier keeps moving toward more autonomy and adaptability.

---

*What I studied next: How MCP (Model Context Protocol) works under the hood --- the standard for connecting LLMs to external tools*
