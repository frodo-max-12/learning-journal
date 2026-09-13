# How search engines work — from crawling to ranking

*Learned in April 2026. I wanted to understand what actually happens when I type a query into Google. Not the hand-wavy "algorithms" answer, but the real machinery underneath. I started with a simple question: what are all the search engines in the world? That question opened a rabbit hole that changed how I think about the internet itself.*

---

## The question that started it all

I type "STM32F103C8T6 price" into Google and get results in 0.3 seconds. That has always felt like magic to me. But I have been learning to ask "how does this actually work?" about everything now, so I decided to pull this apart. What I found was that a search engine is really four separate systems bolted together, and understanding each one individually makes the whole thing demystifiable.

## Step one — somebody has to go fetch all the web pages

Before you can search anything, someone has to actually visit every page on the internet and save a copy. This is what a **web crawler** does. It is conceptually simple — almost embarrassingly so.

A crawler starts with a list of seed URLs. It visits the first one, downloads the HTML, extracts every link on that page, and adds those links to the queue. Then it visits the next URL in the queue, downloads it, extracts links, adds them. Repeat forever.

```python
queue = ["https://seed-url.com"]
while queue:
    url = queue.pop()
    html = fetch(url)
    store(url, html)
    for link in extract_links(html):
        if not already_seen(link):
            queue.append(link)
```

That is the entire idea. In maybe ten lines of pseudocode, you have a web crawler. Google's original crawler was called Googlebot. There is an open-source one called Apache Nutch if you want to see real code.

But of course, the simplicity is deceptive. At real scale, you need politeness rules — respecting `robots.txt` files where websites say "don't crawl me" and rate-limiting so you do not accidentally DDoS someone's server. You need deduplication so you do not store the same page a thousand times. You need URL normalization so `example.com/page` and `example.com/page/` and `EXAMPLE.COM/page` all resolve to the same thing. And you need to distribute this across thousands of machines because the web has hundreds of billions of pages.

This was my first "oh" moment. The hard part of search is not being clever about ranking. The hard part is the brute infrastructure of fetching and storing a meaningful fraction of the entire web.

## Step two — the inverted index

Once you have raw HTML, you need to make it searchable. You parse out the text from each page and build something called an **inverted index**. This is the single most important data structure in search.

Think of the index at the back of a textbook. You look up "semiconductor" and it says "pages 42, 87, 155." The inverted index works exactly the same way, but for every word across every document:

```
"semiconductor" → [doc_42, doc_1307, doc_98234]
"trading"       → [doc_42, doc_555, doc_98234]
```

Now when someone searches "semiconductor trading," the system just intersects the two lists: which documents appear in both? Answer: `doc_42` and `doc_98234`. That intersection operation is extremely fast — much faster than scanning through every page looking for both words.

Real inverted indexes go further. They store positional information (where in the document does the word appear), term frequencies (how many times), and they use compression because the posting lists get enormous. But the concept is that simple: a mapping from every word to every document containing it.

I realized this is why searching feels instant. You are not scanning the web in real time. You are looking up precomputed lists and intersecting them. The work happened days or weeks ago when the crawler visited those pages.

## Step three — ranking, or why the first result is not random

Finding pages that contain your query words is the easy part. The hard part is deciding which of those thousands or millions of matching pages to show you first. This is where the actual intelligence of a search engine lives.

**TF-IDF** is the foundation. The idea: a word is more important in a document if it appears frequently in that document (term frequency) but is rare across all documents (inverse document frequency). The word "the" appears in every document, so it is basically useless for ranking. The word "semiconductor" is much rarer, so a document that mentions it many times is probably genuinely about semiconductors. The math gives higher scores to documents where your query terms are unusually concentrated.

**BM25** is the refined version of TF-IDF that handles a subtle problem: document length. A 10,000-word page might mention "semiconductor" twenty times just because it is long, not because it is more relevant than a focused 500-word page that mentions it five times. BM25 normalizes for this. Remarkably, BM25 — an algorithm from the 1990s — is still the backbone of most search engines today.

**PageRank** was Google's original breakthrough. The insight: a page linked to by many other pages is probably more important. If a hundred different websites all link to the Wikipedia article on semiconductors, that article is probably authoritative. PageRank treats the entire web as a directed graph (pages are nodes, links are edges) and computes a "prestige" score for each node using an iterative random walk simulation. Imagine a person clicking random links forever — PageRank is essentially the probability that this random surfer lands on any given page.

**Neural re-ranking** is the modern layer. Transformer-based models like BERT can understand semantic meaning — they know that "affordable MCU" and "cheap microcontroller" mean similar things even though the words do not overlap. But running a neural model over billions of documents is computationally impossible. So search engines use a two-stage approach: BM25 quickly narrows billions of documents down to maybe a thousand candidates, then the neural model carefully re-ranks just those candidates. Speed for breadth, intelligence for depth.

> The full pipeline is: crawl the web, build an inverted index, use BM25 to find candidates fast, then re-rank with neural models for quality. Every search you have ever done flows through some version of this pipeline.

## Step four — the query processing pipeline

When you actually type a query, there is a whole processing step before the index is even touched. The system tokenizes your query (breaks it into words), corrects spelling, expands synonyms, and sometimes rewrites the query entirely. "Cheap MCU India" might become "affordable microcontroller India" internally. Then it hits the inverted index, scores results, merges them from shards distributed across thousands of machines, and returns them — all in under 200 milliseconds.

At Google's scale, the index is too large for any single machine. It is sharded across thousands of servers, each holding a slice. Your query runs against every shard in parallel, each returns its top results, and a coordinator merges them. This is distributed systems engineering at an extreme level.

## The revelation — there are only two real search engines

This is what genuinely surprised me. I had assumed there were dozens of independent search engines. The reality is starkly different.

| Search Engine | Has own index? | Estimated index size | What it actually does |
|---|---|---|---|
| **Google** | Yes | ~400 billion documents | Full independent crawl and index |
| **Bing** | Yes | ~8-14 billion pages | Full independent crawl and index |
| **Yandex** | Yes | ~10-20 billion pages | Independent, strongest on Russian web |
| **Baidu** | Yes | ~10+ billion pages | Independent, primarily Chinese web |
| **Brave Search** | Partial | ~30 billion pages | Own index with Bing fallback |
| **Mojeek** | Yes | ~8 billion pages | Fully independent but tiny |
| **DuckDuckGo** | No | Uses Bing's index | Privacy layer on top of Bing |
| **Startpage** | No | Uses Google's index | Privacy layer on top of Google |
| **Ecosia** | No | Uses Bing's index | Plants trees, but it is Bing underneath |
| **Yahoo** | No | Uses Bing's index | Has been Bing since 2009 |

DuckDuckGo is Bing underneath. They have always been open about this. Their value proposition was never "we built a better index" — it was "we do not track you." The actual web results come from Bing's API.

Google does not sell wholesale API access to its index. Microsoft does, through the Bing Web Search API. So almost every "alternative" search engine is secretly a Bing skin. When someone launches a "new search engine," the first question to ask is: whose index are you actually querying?

There are really only **two comprehensive maps of the web** — Google's and Microsoft's. That is a remarkable concentration of power. Two American companies essentially decide what is findable on the internet.

## The documents vs. pages distinction

One detail that caught my attention: Google's VP of Search testified in the US antitrust trial that their index contained about 400 billion "documents." Bing's estimate is 8-14 billion "pages." Those are different units.

Google's 400 billion figure includes web pages plus PDFs, images, books, news articles, patents, and other file types. "Documents" is broader than "pages." If you stripped it down to just web pages, Google's number would be lower — but nobody outside Google knows how much lower. Even conservatively, the gap is enormous. Google's index is roughly 30-50x larger than Bing's. That is the real moat. Not the algorithm, but the sheer scale of what they have crawled and stored.

Google also discovered that it encounters trillions of URLs but deliberately indexes only the "useful parts of the web." The crawler finds everything; the indexer is selective about what it keeps. That curation is itself an algorithmic decision — and one of the most consequential, because if a page is not in the index, it effectively does not exist for search purposes.

## What I took away

Search engines are not magic. They are four engineering systems — crawler, indexer, ranker, query processor — layered on top of each other. The concepts are old (inverted indexes date back to the 1960s, TF-IDF to the 1970s, BM25 to the 1990s). What makes Google dominant is not algorithmic genius but infrastructure scale: the willingness to crawl and store 400 billion documents and serve results from them in milliseconds.

The thing that sticks with me most is the two-index reality. The entire visible internet, for practical purposes, runs through two companies' crawlers. Everything else is a skin on top. That is not a technology insight so much as a power-structure insight, and it is the kind of thing you only see when you understand what is actually under the hood.

---

*What I studied next: how inverted indexes connect to database indexing more broadly, and how the same concept shows up in PostgreSQL B-trees and Elasticsearch. See also: [databases and SQL fundamentals](../databases-learning/README.md).*
