# Parsing a PDF into CSV — regex vs pdfplumber

---

## The starting problem

I had the M3M Hurun India Rich List 2025 as a PDF: 105 pages, 2.1 MB, 1,688 billionaires. I wanted it as a CSV so I could sort, filter, and pivot in a spreadsheet. The obvious first move was to convert the PDF to plain text and parse the text file.

The text file looked like this:

```
               Mukesh Ambani &
   1                                         9,55,410             Reliance Industries           Energy                      Mumbai
               family

               Gautam Adani &
   2                                         8,14,720             Adani                         Energy                      Ahmedabad
               family
```

Fixed-width columns, except:

- Names like "Mukesh Ambani & family" split across multiple lines.
- Companies sometimes wrapped across three lines (rank 40, "Samvardhana / Motherson / International").
- Every page had headers and footers polluting the text (date stamps, URLs, column titles, "Subscribe", "Privacy Policy").
- All 1,688 of these awkward little blocks across 9,000 lines.

Two approaches ended up working. The first leaned heavily on regex. The second skipped regex entirely. The contrast taught me more than I expected.

## Approach 1 — regex on the text dump

The strategy:

1. Find "anchor lines" — lines that contain a rank number and a wealth number.
2. For each anchor, look 2 lines above and 2 lines below for continuations of the name, company, or industry.
3. Use the column positions (name starts at character 15, wealth at 44, company at 64, etc.) to slice fragments out of each line.
4. Stitch the fragments together in document order, then write CSV.

The script ended up ~200 lines of Python. Worth walking through how it's organised, because the structure shows both what regex is and what working with it actually feels like.

### What regex is (introduced via the script)

A **regular expression** ("regex") is a tiny language for describing patterns in text. Instead of writing code to check each character, you write a pattern, and a regex engine matches it against your string.

The script's central pattern looked like this:

```python
DATA_LINE_RE = re.compile(
    r"^\s{2,5}(\d{1,4})\s{2,}.*?(\d{1,3}(?:,\d{2,3})+)"
)
```

Decoded piece by piece:

| Piece | Meaning |
|---|---|
| `^` | Start of line |
| `\s{2,5}` | 2 to 5 whitespace characters (the indent before a rank) |
| `(\d{1,4})` | 1–4 digits — the rank. Parentheses capture this for later extraction |
| `\s{2,}` | At least 2 whitespace characters |
| `.*?` | Any characters (non-greedy — match as few as possible) |
| `(\d{1,3}(?:,\d{2,3})+)` | The wealth value like `9,55,410` — 1–3 digits, then one or more groups of comma + 2–3 digits |

The `r"..."` prefix is a **raw string** — don't interpret backslashes, important because `\s` and `\d` are regex syntax. `re.compile(...)` precompiles the pattern so it's faster on repeated use.

That's regex in concentrated form: a few characters expressing what would otherwise be a paragraph of nested if-statements.

### How the script was organised

Six blocks, each doing one job:

```python
# Block 1: imports and inputs
import argparse, csv, re
from pathlib import Path
# input path comes in as a CLI argument; output defaults to the same name + .csv

# Block 2: column positions (counted manually from the text file)
COL_NAME_START, COL_NAME_END = 15, 43
COL_WEALTH_START, COL_WEALTH_END = 43, 63
COL_COMPANY_START, COL_COMPANY_END = 63, 94
COL_INDUSTRY_START, COL_INDUSTRY_END = 94, 124
COL_CITY_START = 124

# Block 3: regex patterns
DATA_LINE_RE = re.compile(r"^\s{2,5}(\d{1,4})\s{2,}.*?(\d{1,3}(?:,\d{2,3})+)")
SKIP_PATTERNS = [
    re.compile(r"^\s*\d+/\d+/\d+,\s+\d+:\d+\s+(AM|PM)"),   # date stamps
    re.compile(r"^https?://"),                              # URLs
    re.compile(r"^\s*RANK\s+NAME"),                         # column header
    # ... 30+ more patterns for "Subscribe", "Privacy Policy", "Page 5 of 17" etc.
]

# Block 4: small helper functions
def is_skip_line(line):
    return any(p.search(line) for p in SKIP_PATTERNS)

def slice_col(line, start, end=None):
    return line[start:end].strip() if end else line[start:].strip()

def parse_data_line(line):
    return {
        "rank": re.match(r"^\s*(\d{1,4})", line).group(1),
        "name_frag": slice_col(line, COL_NAME_START, COL_NAME_END),
        "wealth": slice_col(line, COL_WEALTH_START, COL_WEALTH_END),
        # ... etc
    }

# Block 5: main pipeline
def main():
    lines = SRC.read_text().splitlines()
    # Replace junk lines with empty strings (keep indices stable)
    clean = ["" if is_skip_line(l) else l for l in lines]
    # Find all data-line indices
    data_indices = [i for i, l in enumerate(clean) if DATA_LINE_RE.match(l)]
    # For each anchor, look 2 above and 2 below for continuation fragments
    entries = []
    for idx, i in enumerate(data_indices):
        data = parse_data_line(clean[i])
        # ... stitching logic (~30 lines)
        entries.append({...})
    # Write CSV
    with DST.open("w") as f:
        csv.DictWriter(f, fieldnames=[...]).writerows(entries)

# Block 6: entry point
if __name__ == "__main__":
    main()
```

The `if __name__ == "__main__":` guard at the bottom is a standard Python idiom — it means "only run `main()` if this file is executed directly, not if someone imports it as a module." Small thing, but it's the difference between a one-off script and something reusable.

### What the script taught me about Python

Walking through it block-by-block, I picked up patterns that show up everywhere:

- **`pathlib.Path`** for file paths instead of string-mashing with `os.path`.
- **Generator expressions with `any()` / `all()`** for short-circuiting checks: `any(p.search(line) for p in SKIP_PATTERNS)` stops at the first match.
- **`enumerate()`** for `(index, value)` pairs when looping.
- **Dictionaries** as the natural shape for "one record with named fields."
- **List comprehensions** like `[i for i, l in enumerate(clean) if DATA_LINE_RE.match(l)]`.
- **Context managers** with `with ... as f:` for safe file I/O.
- **Decomposing logic into small helper functions** — the main loop reads almost like English because the helpers absorbed the messy details.

These are the patterns I keep seeing in real Python code. The script was a real-world way to meet them.

### The cost of the regex approach

It worked — produced exactly 1,688 rows. But:

- ~200 lines for what felt like a simple table extraction.
- A 30+ pattern skip-list, each pattern manually crafted.
- Hard-coded column positions painstakingly counted from the text file.
- Multi-line stitching logic that needed careful handling for the edge cases (3-line entries, where company *also* wrapped).
- Fragile: if the PDF-to-text converter changed its output even slightly, the parser would silently start producing garbage.

The whole approach was working *one layer too late*. The text file was already the output of a flattening step (PDF → text) that had thrown away structure. My regex code was heroically reconstructing what was discarded.

## Approach 2 — pdfplumber direct on the PDF

Then I tried a Python library called `pdfplumber` that reads PDFs natively — skipping the text-dump step entirely. The whole working script:

```python
import csv
import pdfplumber

with pdfplumber.open("Hurunn-India-Rich-List-Oct-2025.pdf") as pdf:
    entries = []
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                if row and row[0] and " ".join(row[0].split()).isdigit():
                    entries.append([" ".join((c or "").split()) for c in row])

with open("out.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Rank", "Name", "Wealth", "Company", "Industry", "City"])
    w.writerows(entries)
```

25 lines. Same 1,688 entries. Every field matched the regex version exactly.

The only meaningful logic: "skip rows where the first cell isn't a number." That filters out the column-header rows. No skip-pattern list. No column positions. No multi-line stitching.

The reason it works: `extract_tables()` returns multi-line cells already merged. "Mukesh Ambani &\nfamily" comes back as one string with an internal newline. I just collapse the newline into a space and I'm done.

## Side by side

| Step | Regex on text dump | pdfplumber on PDF |
|---|---|---|
| What it sees | Lines of text with spaces | Characters with (x, y) coordinates on the page |
| How it finds rows | Regex for rank + wealth | Layout analysis finds table boundaries |
| How it finds columns | Hard-coded character positions | Whitespace clustering in 2D coordinates |
| How it merges multi-line cells | Custom look-above/below logic | Automatic — characters in the same cell rectangle group together |
| Junk-line filtering | 30+ regex patterns | One check: is the first cell a number? |
| Lines of code | ~200 | ~25 |

pdfplumber works at a different layer. It reads the PDF's binary format directly, gets back characters with their pixel coordinates, and does layout analysis to reconstruct the table. The text-dump approach was working with characters whose coordinates had already been approximated into whitespace. Different inputs → different difficulty.

## When regex actually earned its keep

Looking back at my own script, only one of the four regex uses was a clean win:

| Where I used regex | Could a string method have done it? |
|---|---|
| Indian-format wealth like `9,55,410` | Awkward with string methods — needs alternation + repetition. **Regex was right.** |
| Extracting the rank from a line | `line.strip().split()[0].isdigit()` — simpler |
| The 30+ skip patterns (URLs, "Page", etc.) | Mostly `line.strip().startswith(...)` |
| Collapsing whitespace `re.sub(r"\s+", " ", s)` | `" ".join(s.split())` does the same thing |

A rule of thumb that's served me: **if you can describe the check in one short English sentence using "starts with," "contains," "is all digits," or "ends with," reach for a string method first.** If you need "optionally," "one or more of," "any of," or "matched groups," that's when regex earns its keep.

Regex is a power tool. Used where it isn't needed, it makes code harder to read, harder to debug, and slower for anyone (including future-me) to modify safely.

## The deeper lesson — choose the right layer

The thing this exercise taught me, beyond regex specifically: **whenever I'm writing a lot of code to extract structure from a derived format, I should ask whether an upstream tool exists that works with the original format directly.**

```
PDF binary  →  text-dump tool  →  flattened .txt  →  my regex code  →  table structure
                                                                       (200 lines)

PDF binary  →  pdfplumber                                          →  table structure
                                                                       (25 lines)
```

Every conversion step loses information. Working from a derived format and reconstructing lost structure is harder than working from the original. The same pattern shows up everywhere:

- Scraping `.docx` files by converting them to text first, when `python-docx` reads the structured XML inside.
- Parsing API responses by string-matching on the printed output, when the underlying JSON is already structured.
- Reading log files with regex when the application could write structured JSON logs.

When you genuinely can't move upstream (a vendor only sends you the PDF, a regulator only publishes the printable version), then regex + string methods on the flattened format are your only option. But it should be the fallback, not the default.

The pdfplumber probe takes 30 seconds: open the PDF, call `extract_tables()` on a few sample pages, look at what comes back. If you see clean structured rows, you're done. If you see garbage, fall back to the text-dump approach with full awareness of what you're paying for.

---

*What I studied next: [Why PDFs are binary, not text](why-pdfs-are-binary-not-text.md) — the design choice that makes PDF text extraction hard in the first place, and why pdfplumber works the way it does.*
