# When the Official API Can't Do It — Reverse-Engineering an Internal Endpoint

**Context:** I'd asked for a transcript of a video, got one, and then asked the question I've learned to ask: *which tool actually did that?* The answer was an open-source library — and the interesting part was that it **doesn't use the platform's official API at all.** It can't. Pulling that thread produced the clearest example I've seen of the difference between a documented public API and the internal endpoints a product's own client uses, and why the second is sometimes the only option.

---

## 1. Why the official API is a dead end here

This surprised me, because "use the official API" is the advice I'd internalized.

The platform's public API does have a captions resource. It lets you **list** the caption tracks for a video. But to **download** the actual caption text you must authenticate as the *video's owner*.

**You cannot download captions for someone else's video through the official API.** So for any video you didn't upload — which is essentially every video anyone sends you — the official route simply doesn't do the thing.

Two smaller obstacles on top: it requires a cloud project, an API key, and a quota; and auto-generated captions are often filtered out of what it exposes even for owners — and auto-generated captions are what most videos have.

That reframed something for me. **An official API is not a complete interface to a product. It's the subset the company chose to support**, shaped by their business and legal constraints. The gap between "what the product can do" and "what the API exposes" is a real gap, and it's where this whole category of tooling lives.

---

## 2. The alternative: the endpoint the product's own client uses

The library instead hits the same internal endpoint the web player uses to render captions in your browser. The principle:

> **If your browser can render it, something can fetch it.**

The player is a client. It gets the captions somehow. That "somehow" is an endpoint, and endpoints can be called by other programs.

---

## 3. How it actually works — four steps

Reading the source, the flow is short enough to hold in your head, and each step taught me something.

**Step 1 — GET the ordinary watch page.** Just the HTML a browser would receive. There's a wrinkle handled here: if the response contains a consent-gate form, the library scrapes the consent token out, sets a cookie, and retries — the same dance a browser does in certain regions.

**Step 2 — regex the API key out of the HTML.** Buried in a JavaScript blob in the page is `"INNERTUBE_API_KEY":"..."`, and the library pulls it out with a pattern match.

**This is the detail worth pausing on: there is no API key in the library.** The platform ships one in the page and rotates it, so the library scrapes a fresh one at runtime. It doesn't hold a credential — it *borrows the one the page was going to use anyway.*

And the failure branch is elegant: if the regex doesn't match **and** the page contains a CAPTCHA element, it raises "IP blocked." The absence of the key plus the presence of a challenge is a diagnosis.

**Step 3 — POST to the internal player endpoint**, with a body declaring the client as the **Android app**, not the web client:

```json
{"context": {"client": {"clientName": "ANDROID", "clientVersion": "..."}},
 "videoId": "..."}
```

The mobile client endpoint is more permissive about returning caption data than the web one. So the library **impersonates a different first-party client** to get a more useful response. Same service, different door.

**Step 4 — classify the response.** The returned JSON carries a playability status, and this is where soft failures get sorted:

| status and reason | meaning |
|---|---|
| login required + "confirm you're not a bot" | request blocked — bot detection |
| login required + "may be inappropriate" | age restricted |
| error + "video is unavailable" | video gone |
| anything else non-OK | unplayable |

That's a genuinely good pattern independent of the domain: **one ambiguous failure surface, decomposed into named, distinguishable causes.** Without it, every one of those cases is "it didn't work."

---

## 4. What you give up

This approach is fragile in three specific ways, and it's worth being precise about them rather than saying "it might break":

**IP-based rate limiting and blocking.** Hammer it from one address and you get blocked. Datacenter address ranges are blocked aggressively, because that's where scrapers run — so the same code is markedly more reliable from a residential connection than from a cloud server. That's a fact I'd never have predicted and it explains why such libraries document proxy support prominently.

**The endpoint can change without notice.** It's internal. Nobody promised it would stay. It has changed a handful of times historically, breaking the library until maintainers shipped a fix.

**No contract, so no versioning.** Which is precisely the thing a public API's `/v1/` is *for* — a promise about when breakage may happen. Internal endpoints make no such promise, and that's the whole trade.

---

## 5. The trade, stated plainly

| | official API | internal endpoint |
|---|---|---|
| stability | versioned, deprecation notices | can change any day |
| access | requires keys, quotas, sometimes ownership | none needed |
| capability | the subset the company chose to expose | whatever the product's own client can do |
| legitimacy | sanctioned | tolerated at best |
| failure mode | documented error codes | ambiguous, needs classification |

**You trade stability and sanction for capability and access.** For a one-off interactive use that's almost always the right trade. For a production pipeline pulling thousands of items a day, you'd need proxy rotation and an acceptance that it will break — or a paid third-party service that has absorbed the fragility on your behalf, which is what those services are actually selling.

---

## 6. What I took away

**"Use the official API" is advice with a precondition** — that the official API can do the thing. Checking whether it actually can, before assuming, would have saved me the confusion I started with.

**Reading the source settled every question at once.** Three files, under 1,600 lines. Rather than guessing why it might be rate-limited or how it authenticates, I could see: it doesn't authenticate, it borrows a rotating key, it impersonates a mobile client, and here are the exact four things that make it fail. That's the argument for reading small libraries rather than reasoning about them.

**And "if the browser can do it, something can fetch it" is a genuinely useful heuristic** — with the honest caveat attached. It tells you a path exists; it doesn't tell you the path is stable, permitted, or wise. Knowing precisely which of those you're giving up is the difference between a considered choice and an accident.
