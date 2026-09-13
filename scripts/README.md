# Scripts

Small, runnable code samples that go with specific journal entries. Each one is a real working script I wrote while learning — not pseudocode.

## What's here

### `parse_hurun_pdf_to_csv.py`

The regex-on-text-dump approach to parsing the Hurun India Rich List 2025 PDF into a CSV. ~200 lines. Reads a pre-flattened text dump, identifies "anchor lines" with a rank+wealth regex, stitches multi-line names and companies together using a look-above/look-below pass over fixed-width columns, and writes 1,688 rows to CSV.

**Companion entry:** [Parsing a PDF into CSV — Regex vs pdfplumber](../parsing-a-pdf-into-csv-regex-vs-pdfplumber.md)

### `parse_hurun_pdf_with_pdfplumber.py`

The same job done with the `pdfplumber` library. ~25 lines. Reads the PDF directly (no text-dump step), uses `extract_tables()` to get back already-merged rows, filters out header rows by checking if the first cell is a digit, writes 1,688 rows to CSV.

Produces an output identical to the regex version, in roughly 1/8th the code.

**Companion entry:** [Parsing a PDF into CSV — Regex vs pdfplumber](../parsing-a-pdf-into-csv-regex-vs-pdfplumber.md)

## Getting the input

Both scripts take the input file as an argument — nothing is hard-coded, and no data is committed here. The Hurun India Rich List is published each year as a free, sponsor-branded press release PDF; download the year you want and point the script at it.

The regex version works on a *flattened text dump* rather than the PDF, which is the whole reason it needs 200 lines instead of 25. To produce one:

```bash
pdftotext -layout Hurun-India-Rich-List-Oct-2025.pdf Hurun-India-Rich-List-Oct-2025.txt
```

The `-layout` flag is load-bearing — it preserves the column positions the script slices on.

## Running them

The regex version uses only Python's standard library:

```bash
python3 parse_hurun_pdf_to_csv.py Hurun-India-Rich-List-Oct-2025.txt
```

The pdfplumber version reads the PDF directly, and needs `pdfplumber` installed. On macOS with the system Python you'll likely need a virtualenv (PEP 668):

```bash
python3 -m venv ~/pdfvenv
~/pdfvenv/bin/pip install pdfplumber
~/pdfvenv/bin/python parse_hurun_pdf_with_pdfplumber.py Hurun-India-Rich-List-Oct-2025.pdf
```

Both default to writing a `.csv` next to the input. Pass `-o` to choose a different destination, and `--help` for the full usage.

**A note on the column constants.** The regex script hard-codes the character offsets where each column starts and ends, because I counted them by hand from one specific text dump. That is exactly the brittleness the companion entry is about — a different year, or a different flattening tool, will shift them and the script will need re-measuring. The pdfplumber version has no equivalent constants, which is the point of the comparison.
