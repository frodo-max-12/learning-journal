# What `/v1/` Is Doing in a URL — and the Stack From Raw HTTP to a GUI

**Context:** I was reading through an API reference and stopped on something small: `GET /gmail/v1/users/{userId}/messages/{id}`. Why is `v1` in there? Chasing that turned into a much better question — I'd been confused for a while about how an API, an SDK, and a command-line tool relate to each other, and whether the CLI was "using the API underneath." The answer is a four-layer stack, and once I saw it the whole category stopped being a jumble of acronyms.

---

## 1. Why the version is in the URL

`v1` is the API's version number, and it exists to solve a specific and severe problem.

A company publishes an API. Thousands of developers write code against it — expecting specific URL patterns, specific field names, specific response shapes. Now the company wants to improve it: restructure a response, rename a field, change how authentication works.

**If they change the existing URLs, every application using that API breaks at once.**

So instead, the current API lives at `/v1/`, and a fundamentally redesigned version would live at `/v2/`. Both run simultaneously through a transition. Code written against v1 keeps working; teams migrate at their own pace.

The concrete failure it prevents — suppose v1 returns:

```json
{ "part_number": "STM32F103", "price": 2.50, "currency": "USD" }
```

and you later want multi-currency support:

```json
{ "part_number": "STM32F103",
  "pricing": [ {"amount": 2.50, "currency": "USD"},
               {"amount": 210,  "currency": "INR"} ] }
```

Replace the first with the second and **every consumer reading `response.price` crashes**, because that field no longer exists. Run them side by side at different paths and nobody breaks.

---

## 2. The detail I found most interesting

The Gmail API has been on `v1` since it launched around 2014 — over a decade without a version bump.

That tells you something real: **additions don't break existing code; only removals and restructurings do.** They've added whole new capabilities over the years, and every one of them was a new field or a new endpoint, which existing consumers simply ignore.

So a stable version number isn't stagnation. It's evidence that the original design was good enough that a decade of new features fit inside it — and that the team held the discipline of *adding* rather than *rearranging*.

That reframes API versioning from bureaucracy into a visible record of design quality. A service on `v7` has either learned a lot or designed badly, and you can't tell which from outside — but a service still on `v1` after ten years is making a claim about its original design that's hard to fake.

---

## 3. Why use an API at all, rather than just reading the web pages?

This was the naive question I asked, and it has a real answer.

A web page is **HTML meant for human eyes** — layout, styling, navigation, ads, all mixed in with the data you want. To use it programmatically you have to *scrape*: fetch the page and dig the data out of markup that was never designed to be dug into. Then someone redesigns the page and your code breaks, silently, with no notice.

An API returns **structured data meant for programs** — usually JSON, with named fields, a documented shape, and a stability contract expressed by that version number.

So the difference is not merely convenience. It's that one of them is a **contract** and the other is an accident you're depending on. The version number is the contract being explicit about when it may change.

---

## 4. What "parse" means, since I had to ask

To parse is to take input in some format and turn it into a structure your program can work with.

The API sends you a JSON *string* — literally characters, `{"price": 2.50}`. Parsing turns that text into an object your language understands, so you can ask for `response["price"]` and get a number rather than a substring.

Once I had that, a lot of vocabulary settled: a PDF parser turns bytes into text and tables, a regular expression parses structure out of a string, a compiler parses source code into a tree. **Same operation at different scales — text in, structure out.**

---

## 5. The stack: raw HTTP → SDK → CLI → GUI

Here's the answer to the confusion I'd actually been carrying. These aren't alternatives. They're **four layers over the same thing**, and the API sits underneath all of them.

**Layer 1 — the raw API.** The contract: send a POST request to this URL, with these headers and this JSON body, and you'll get this JSON back. You can do this yourself with an HTTP library: construct the URL, set the authentication header, serialize the payload, send it, parse the response. It works, and it's about twenty lines of boilerplate that every user of that API would otherwise write identically.

**Layer 2 — the SDK.** A package the provider publishes so you don't write that plumbing:

```python
import anthropic
client = anthropic.Anthropic()          # picks up the key from the environment
response = client.messages.create(...)   # constructs, sends, parses for you
```

Underneath, it does exactly what the manual version did. **The API is the contract; the SDK is a convenience layer in a specific language.** One API, many SDKs — Python, TypeScript, and so on. The API exists whether or not anyone writes an SDK for it.

And the reason it's called a *kit* rather than a library: it usually bundles type definitions so your editor can autocomplete responses, proper error classes instead of raw status codes, automatic retries on rate limits, and authentication helpers. It's the whole toolkit for one service rather than a bag of functions.

**Layer 3 — the CLI.** A command-line wrapper that uses the SDK internally and exposes it as terminal commands. So yes — the CLI *is* using the same API underneath. That was the thing I couldn't work out.

**Layer 4 — the GUI.** The web or desktop app. Also, ultimately, the same API.

And the rule that makes the stack make sense:

> **Each layer adds convenience and removes flexibility. The API stays the same underneath all of them.**

The GUI is the easiest to use and can only do what its designers put buttons on. Raw HTTP can do anything the API permits and makes you do all the work. Every layer is that trade, made once more.

---

## 6. What I took away

**Choose your layer deliberately.** For a one-off, use the GUI. For a repeatable task, the CLI. For something inside a program, the SDK. Drop to raw HTTP only when the SDK doesn't expose what you need — which does happen, and knowing that raw HTTP is *always* available underneath means being blocked by an SDK is never actually being blocked.

**A version number is a promise about breakage.** Not decoration, and not internal bookkeeping — it's the provider telling you which changes will and won't be forced on you, and when.

**"Is the CLI using the API underneath?" turned out to be the right question.** It sounds like a naive plumbing question and it's actually the question that organizes the whole category. Everything is the API; the rest is ergonomics.
