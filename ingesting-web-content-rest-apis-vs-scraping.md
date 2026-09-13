# Ingesting Web Content — REST APIs vs Scraping

*After indexing seven David Burns books into [my local semantic search system](building-a-local-notebooklm-semantic-search-from-scratch.md), I wanted his web writing too — feelinggood.com, a blog archive of over a thousand posts, plus his "Feeling Good" column on Psychology Today. Fetching ~1,100 posts cleanly, politely, and re-runnably turned out to be its own education. The lesson that stuck: before writing a scraper, check whether the site will simply hand you the data.*

---

## Check for an API first

My instinct was "blog → scraper": fetch each page's HTML, fight through the markup, extract the article. For feelinggood.com that would have been entirely wasted effort, because the site runs on WordPress — and **every WordPress site ships a public JSON API by default**. Roughly 40% of the web runs WordPress, so this one fact eliminates scraping for a huge fraction of content sites.

The endpoint:

```
/wp-json/wp/v2/posts?per_page=100&page=N&_fields=link,date,title,content
```

That returns clean, structured JSON — title, date, URL, and the *full post body* — with no HTML-soup archaeology. Three details I now reuse everywhere:

- `per_page=100` is the maximum page size, so a thousand posts is just eleven requests.
- `_fields=` trims the response to only the fields you need, shrinking the payload dramatically.
- Pagination termination is quirky: when you request a page past the end, WordPress returns **HTTP 400**. The fetcher treats that specific response as the natural stop condition of the loop, not as an error.

The deeper habit: when you want data from any site, spend five minutes probing for a structured interface first — `/wp-json/` on WordPress, RSS/Atom feeds, sitemap.xml, a JSON API behind the page's own JavaScript (visible in the browser's network tab). Rendered HTML is the *worst* interface a site offers; it's just the default one.

## Scraping as the fallback

Psychology Today has no public API, so that source genuinely needed scraping. The approach that worked:

1. **Walk the paginated index** and collect article URLs with a regex — the links followed a stable shape (`/blog/feeling-good/` followed by a six-digit `YYYYMM` segment and a slug), so a pattern match on the index pages yielded the full article list.
2. **Fetch each article and keep only `<p>` blocks of ≥12 words.** This crude-sounding filter is remarkably effective: navigation labels, bylines, cookie banners, and link lists are short; sentences of actual prose are long. One threshold separates content from boilerplate.
3. **Recover metadata from the URL itself.** The publish date was baked into that `YYYYMM` URL segment — no need to parse it out of the page at all.

Scraping is brittle by nature (a redesign breaks your selectors), which is exactly why it's the fallback rather than the default. But when the URL structure carries metadata and a simple length filter isolates prose, a scraper can stay small and survive most cosmetic redesigns.

## What makes a fetcher production-grade

The whole fetch script is ~130 lines, but a handful of details separate it from a homework script:

- **Retries with backoff** — three attempts per request, sleeping `2·(attempt+1)` seconds between them, so transient network failures don't kill a long run.
- **A browser User-Agent and politeness delays** — 0.4s between API pages, a slower 1.0s between scraped pages. Hammering a site is both rude and a fast way to get blocked.
- **Quality gates** — posts under 50 words are dropped before they ever pollute the index.
- **Idempotency by design** — on startup the script loads every URL already in the corpus into a `seen` set, so re-running it only appends *new* posts. Combined with append-only **JSONL** output (one self-contained JSON object per line), a killed run loses nothing and a re-run never duplicates. I can run it again next month and it picks up exactly the new episodes.

That idempotency-plus-append-only pairing has become my default shape for any data-collection script: crash-safe, resumable, and re-runnable with no bookkeeping.

The haul: **1,102 posts, ~944k words** — 1,086 from feelinggood.com (including podcast show notes and live-session transcripts) and 16 from Psychology Today. That roughly *doubled* the knowledge base, since the seven books themselves total about the same word count.

## Merging into the index without breaking the experiment

The subtle part wasn't fetching — it was adding the web corpus to the existing index *without disturbing it*, because I run the books-only and books-plus-web versions side by side as an A/B test.

The ingest script never re-processes the books. It **copies** the books-only SQLite database and **stacks** the new blog vectors below the existing book matrix (`np.vstack`), assigning new rows ids starting at `MAX(id)+1` in exactly the order the vectors were stacked. Book retrieval in the expanded system is therefore *byte-identical* to the original — any behavioural difference between the two versions is attributable to exactly one variable: the presence of the web corpus. Experimental control, applied to a data pipeline.

Two schema tricks made mixed content fit the existing shape: `ALTER TABLE` added `source` and `url` columns, and the existing citation columns got reused — for blog rows, the "book" field holds the post title and date, and the "chapter" field holds the site name. One schema, two citation styles.

The invariant that everything depends on — SQLite id N ↔ matrix row N — survives because inserts and stacking happen in the same order. It's the kind of correspondence that's trivial to maintain and catastrophic to break silently, which is why the aligned-insert step is the most carefully written code in the script.

## What carried over

Three habits I'm keeping from this build:

1. **Probe for structure before scraping.** APIs, feeds, and sitemaps are everywhere once you look; HTML is the interface of last resort.
2. **Make every collector idempotent and append-only.** A `seen` set plus JSONL costs ten lines and converts a fragile script into a re-runnable pipeline.
3. **When extending a system you're measuring, change one variable.** Copying the baseline index instead of rebuilding it turned "I added more data" into a controlled experiment.
