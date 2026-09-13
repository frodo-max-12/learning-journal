# Why Markdown Costs Fewer Tokens Than HTML

**Context:** I'd seen the claim that serving documentation as markdown instead of HTML cuts token usage by roughly 10×, and I didn't follow the logic. Same information either way — where do the tokens go? The answer decomposes into four separate effects, and one of them isn't about length at all.

---

## 1. The core idea: scaffolding versus content

To make "Hello, world" bold:

```
markdown:  **Hello, world**
HTML:      <p class="text-lg font-semibold leading-6 text-gray-900"><strong>Hello, world</strong></p>
```

Identical visible content. Wildly different character counts, and therefore token counts.

That's the whole thing in one comparison, and everything below is why the gap is bigger in practice than that example suggests.

---

## 2. Tags are verbose and paired

Every `<div>` needs a `</div>`; every `<span>` needs a `</span>`. Markdown uses short symbols — `#`, `*`, `-`, backticks — that mostly don't need closing.

A heading is `# Title` in markdown. In HTML it's `<h1>Title</h1>`, and on a real documentation site it's more like:

```html
<h1 id="title" class="scroll-mt-20 text-4xl font-bold tracking-tight">Title</h1>
```

Four words of content wrapped in seventy characters of machinery.

---

## 3. Real pages carry enormous amounts of non-content

This is where the multiplier comes from, and it's the part I'd underestimated. Fetching a documentation page gets you far more than the prose:

- the navigation sidebar and the footer
- the search widget
- analytics scripts
- CSS class names on essentially every element
- accessibility attributes
- SVG icons inlined as raw markup
- meta tags and structured-data blobs for search engines

Most of that is invisible chrome or styling that a reader of the *content* has no use for. You're paying tokens for the page's furniture.

---

## 4. Tokenizers actively dislike HTML

This is the effect that isn't about length, and it's the one that made the whole thing click.

Tokenizers are trained mostly on natural language and code. A string like:

```
class="prose prose-slate dark:prose-invert"
```

gets chopped into **many small tokens**, because none of it resembles common English words. Ordinary prose tokenizes far more efficiently — roughly one token per four characters.

So HTML is penalized *twice*: it has more characters, **and** its characters convert to tokens at a worse rate. The two effects multiply rather than add.

I'd been reasoning about this as a length problem. It's a length problem *and* a density problem, and the density half is invisible unless you know how tokenizers work.

---

## 5. Client-side rendering makes it worse

The final twist. Many modern documentation sites ship a **mostly-empty HTML shell plus a large bundle of JavaScript** that builds the page in the browser.

Fetch the raw HTML and you get all the scaffolding and all the scripts — and very little of the actual documentation, because the text doesn't exist until the JavaScript runs.

So you pay a lot of tokens for almost no useful content. That's the worst case: maximum packaging, minimum payload.

Which also explains something I'd noticed and not connected — why a fetched page sometimes comes back looking empty of the thing you wanted. It isn't a fetch failure. The content was never in the document.

---

## 6. What this adds up to

"10× smaller" isn't magic. It's the removal of:

| what's removed | why it was there |
|---|---|
| tags and closing tags | structure for a rendering engine |
| class attributes | styling |
| scripts | interactivity |
| navigation, footer, widgets | site chrome |
| meta and structured data | search engines and social previews |

**Same information, far less packaging.** The markdown version is the document; the HTML version is the document plus instructions for drawing it, plus the rest of the website.

---

## 7. What I took away

**Markup is instructions for a renderer, and a model isn't a renderer.** HTML is doing a job — it tells a browser how to lay out and style a page. Handing that to something that only wants the prose means paying for a job nobody asked for.

**Token cost has two independent components: how many characters, and how well those characters tokenize.** I'd only been thinking about the first. Machine-oriented strings — class names, identifiers, base64, minified code — are expensive per character in a way plain prose isn't, which is the same reason a compression ratio told me what was inside an archive.

**And "serve markdown for machines" is a real design pattern**, not a preference. Increasingly, sites publish a markdown version of their docs alongside the HTML for exactly this reason: one representation for browsers, another for programs. Which is the same separation as an API versus a web page — structured for the consumer that's actually asking.
