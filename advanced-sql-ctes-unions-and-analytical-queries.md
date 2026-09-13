# Advanced SQL — CTEs, UNIONs, and analytical queries

*Learned in February 2026. I was trying to understand a production SQL query from Google's SA360 (Search Ads 360) bidding dashboard. My earlier learning covered basic SQL — SELECT, WHERE, JOIN, GROUP BY. This was the moment I realized that "knowing SQL" and "reading real SQL in the wild" are two very different things. The query was 80+ lines long, and I could not follow any of it. So I went line by line.*

---

## The context — why this query exists

Google's SA360 is a platform for managing search advertising bids. The team I was looking at tracked three bidding features — Value-Based Bidding (VBB), AI Bidding, and Enterprise Bidding — and needed to know: what percentage of advertisers have adopted each one? That is the entire question. But turning that question into SQL requires combining data from multiple sources, handling missing values, protecting against division by zero, and producing both a summary view and a detailed breakdown. That complexity is where the learning happened.

## What is a CTE, and why does it exist?

The first thing I encountered was this pattern:

```sql
WITH _0 AS (
    -- a whole query here
),
_1 AS (
    -- another query that uses _0
)
SELECT * FROM _1
```

This is a **CTE — Common Table Expression**. The `WITH` keyword lets you define temporary named result sets that you can reference later in the query, almost like naming intermediate variables.

The analogy that clicked for me: imagine you are doing a complex calculation on paper. Instead of writing one enormous expression, you would say "let X = this intermediate result" and "let Y = that intermediate result" and then your final answer is some function of X and Y. A CTE is that "let X = ..." step for SQL.

Without CTEs, you would have to either nest subqueries inside subqueries (which becomes unreadable fast) or create actual temporary tables in the database (which requires extra permissions and cleanup). CTEs give you the readability of named steps without the overhead of creating real tables.

In this query, `_0` combined two data sources into one unified dataset. `_1` then computed all the percentage metrics from that unified dataset. And the final `SELECT * FROM _1` just returned the results. Three clean steps instead of one monstrous nested query.

> CTEs are named intermediate results. They make SQL readable the same way variables make code readable — by giving names to things so you can think about them one at a time.

## UNION ALL — merging two tables with different data

The `_0` CTE contained a `UNION ALL`, which was the second concept I had to unpack. The dashboard tracked bidding metrics in two separate tables:

- `AutomatedBiddingActivationDash_DSF` — had VBB and AI Bidding numbers
- `EnterpriseBidding_DSF` — had Enterprise Bidding numbers

These tables had different columns and tracked different things, but the query needed to combine them into a single dataset for analysis. That is what UNION ALL does — it stacks the results of two queries on top of each other, row by row.

But here is the subtle part. Since the two tables had different columns, each side of the UNION had to produce the same column structure. The VBB side set all Enterprise Bidding columns to `NULL`:

```sql
SELECT 'VBB' AS Source,
       vbb_numerator, vbb_denominator,
       ai_bidding_numerator, ai_bidding_denominator,
       NULL AS EB_numerator, NULL AS EB_denominator,
       NULL AS multi_channels, NULL AS multi_engines
FROM AutomatedBiddingActivationDash_DSF
GROUP BY ALL
```

And the Enterprise Bidding side did the reverse — real values for EB columns, NULLs for VBB columns. A `Source` column tagged each row so you could tell where it came from later.

This is like having two spreadsheets with different columns and merging them into one master sheet. Where one sheet does not have a column, you fill in blanks. Now every row lives in the same table and you can analyze everything together.

I also learned the difference between `UNION` and `UNION ALL`. Plain `UNION` removes duplicate rows (which requires sorting and comparing every row — expensive). `UNION ALL` keeps everything, duplicates included. Since the two tables here contain fundamentally different data, there cannot be duplicates, so `UNION ALL` is both correct and faster.

## NULLIF — the division-by-zero bodyguard

The percentage calculations all followed this pattern:

```sql
SUM(IF(source = 'VBB', ai_bidding_numerator, 0))
  / NULLIF(SUM(IF(source = 'VBB', ai_bidding_denominator, 0)), 0)
```

There are three things happening here, and each one taught me something.

**First, the conditional SUM.** The `IF(source = 'VBB', ai_bidding_numerator, 0)` says: "only include this row's numerator if it came from the VBB source; otherwise treat it as zero." This prevents Enterprise Bidding rows from accidentally polluting the VBB calculation. Because the UNION ALL mixed everything into one table, you need these source filters to separate them back out for the right calculations.

**Second, the division.** Numerator divided by denominator gives you the adoption percentage. Simple enough.

**Third, and this was the real insight: `NULLIF`.** In SQL, dividing by zero does not just give you infinity or an error — it can crash the query or produce undefined results depending on the database. `NULLIF(x, 0)` says: "if x equals zero, return NULL instead." And dividing by NULL in SQL produces NULL (not an error). So the whole expression gracefully returns NULL when there is no denominator data, instead of blowing up.

This is a defensive programming pattern. The real-world scenario: what if some region has zero advertisers eligible for VBB? The denominator would be zero. Without NULLIF, the query fails. With it, that region just shows up as NULL (no data) rather than crashing the entire dashboard.

| Expression | When denominator = 100 | When denominator = 0 |
|---|---|---|
| `num / denom` | 0.45 (normal result) | ERROR - division by zero |
| `num / NULLIF(denom, 0)` | 0.45 (normal result) | NULL (graceful) |

I started noticing NULLIF everywhere after learning this. It is one of those patterns that separates "SQL that works in a demo" from "SQL that works in production."

## GROUP BY ALL — a convenient shorthand

The query used `GROUP BY ALL`, which I had never seen before. In standard SQL, when you use aggregate functions like SUM or COUNT, you have to explicitly list every non-aggregated column in the GROUP BY clause. If your SELECT has ten columns and only two are aggregated, you write out the other eight in GROUP BY. It is tedious and error-prone.

`GROUP BY ALL` is a shorthand (available in some SQL dialects like Google's internal query engine and newer databases like DuckDB) that says: "group by every column in the SELECT that is not inside an aggregate function." It saves typing and reduces the chance of forgetting a column, which would cause an error.

This is not standard SQL — you would not find it in PostgreSQL or MySQL. But knowing it exists helped me understand that SQL is not one monolithic language. Every database has its own dialect, its own extensions, its own quirks. The core is standard, but the edges are vendor-specific.

## The subquery for date alignment

One detail that took me a while to appreciate:

```sql
WHERE _partition_date IN (
    SELECT max(date) FROM AutomatedBiddingActivationDash_DSF
)
```

The Enterprise Bidding table could have data for any date. But the query filters it to only the most recent date available in the VBB table. Why? Because if VBB data was last updated on February 20 and Enterprise Bidding data goes up to February 23, comparing their percentages would be misleading — you would be looking at different time periods. This subquery ensures both sources align on the same reporting date.

This is a pattern I now think of as "temporal alignment" — making sure you are comparing apples to apples when data sources update at different cadences. It is the kind of detail that does not show up in SQL tutorials but matters enormously in real dashboards.

## Two queries, one CTE — the summary vs. breakdown pattern

The thing that made this learning really click was discovering that there were actually two queries sharing the exact same `_0` CTE. The difference was entirely in how `_1` was written.

**Query 1 — Global summary.** No GROUP BY clause. Everything rolled up into a single row. One number for each adoption percentage across the entire portfolio. This answers: "what is our overall AI Bidding adoption rate?"

**Query 2 — Granular breakdown.** Same calculations, but with a GROUP BY on seven dimensions: date, region, engine, country, advertiser ID, customer ID, and a few more. This produces one row per combination, sorted by search spend descending (`ORDER BY search_cost_quarterly_fx DESC`). This answers: "what is the adoption rate for each advertiser in each region, with the biggest spenders first?"

Same data, same CTE, same math — but two completely different outputs. The summary feeds the executive scoreboard. The breakdown feeds the detail table where you can drill into specific accounts.

| Aspect | Query 1 (Summary) | Query 2 (Breakdown) |
|---|---|---|
| GROUP BY | None | 7 dimensions |
| Output rows | 1 | Potentially thousands |
| ORDER BY | None | By spend, descending |
| Use case | Dashboard scoreboard | Drill-down analysis |

This is when I understood why CTEs are so powerful. You define the data preparation once and then build multiple views on top of it. The CTE is the shared foundation; the final SELECTs are different lenses on the same data.

## The practical context — why this matters to me

This was not academic. The dashboard tracked bidding feature adoption for Google's advertising clients, organized by operating company (OpCo). Every few weeks, a stakeholder would ask: "which OpCos have high Enterprise Bidding adoption and which have low? Which top accounts should we prioritize?" The answer lived in this SQL — but getting it out required downloading a data dump, importing it into Google Sheets, and manually running XLOOKUP against a separate "book of business" file to map advertiser IDs to OpCo names.

The conversation led me to realize the most practical solution was not to automate the query (that would require getting the book-of-business mapping into the SQL layer, which was not feasible). It was to build a template Google Sheet with three tabs: one for the data dump, one for the book of business, and one with pre-built XLOOKUP formulas that auto-calculate when you paste fresh data. The insight was pragmatic: do the manual thing now since someone is waiting for the answer, but clean it up into a reusable template so next time takes ten minutes instead of forty-five.

> The most scalable solution is not always the most automated one. Sometimes a well-structured spreadsheet with good formulas beats a fully automated pipeline — especially when the request comes every two to four weeks, not every two minutes.

## What I actually learned about SQL

This query taught me more than any tutorial because it was real. Tutorials show you SELECT-FROM-WHERE on a toy dataset. Production SQL has CTEs that build on each other, UNION ALLs that merge heterogeneous sources, NULLIF guards against edge cases, conditional aggregation with IF statements inside SUMs, subqueries for temporal alignment, and the same foundation repurposed for both summary and detail views.

The gap between "I know SQL" and "I can read and write production SQL" is exactly this set of patterns. Basic SQL is vocabulary. Analytical SQL is prose.

---

*What I studied next: window functions (RANK, ROW_NUMBER, PARTITION BY) and how they differ from GROUP BY. These showed up in the OpCo ranking query and deserve their own entry. See also: [databases and SQL fundamentals](../databases-learning/README.md).*
