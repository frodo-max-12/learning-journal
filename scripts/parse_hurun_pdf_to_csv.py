#!/usr/bin/env python3
"""Parse a Hurun India Rich List text dump into CSV.

Input is the flattened text of the PDF (e.g. produced by `pdftotext -layout`),
where each record occupies fixed-width columns and long names wrap onto
neighbouring lines.

Usage:
    python3 parse_hurun_pdf_to_csv.py Hurun-India-Rich-List-Oct-2025.txt
    python3 parse_hurun_pdf_to_csv.py input.txt -o out.csv
"""

import argparse
import csv
import re
from pathlib import Path

# Column boundaries observed in the text dump.
# RANK starts ~col 3, NAME ~col 15, WEALTH ~col 44, COMPANY ~col 64,
# INDUSTRY ~col 95, CITY ~col 125
COL_NAME_START = 15
COL_NAME_END = 43
COL_WEALTH_START = 43
COL_WEALTH_END = 63
COL_COMPANY_START = 63
COL_COMPANY_END = 94
COL_INDUSTRY_START = 94
COL_INDUSTRY_END = 124
COL_CITY_START = 124

# A "data line" starts with whitespace then a rank number, followed by
# a comma-separated wealth value somewhere on the same line.
DATA_LINE_RE = re.compile(
    r"^\s{2,5}(\d{1,4})\s{2,}.*?(\d{1,3}(?:,\d{2,3})+)"
)

# Lines to skip (page headers/footers).
SKIP_PATTERNS = [
    re.compile(r"^\s*\d+/\d+/\d+,\s+\d+:\d+\s+(AM|PM)"),  # date stamp
    re.compile(r"^https?://"),
    re.compile(r"^\s*RANK\s+NAME"),
    re.compile(r"^\s*2025\s*\(INR"),
    re.compile(r"^\s*CR\)"),
    re.compile(r"^\s*Hurun\s*$"),
    re.compile(r"^\s*RESIDENCE\s*$"),
    re.compile(r"^\s*M3M\s*$"),
    re.compile(r"^\s*HURUN\s*$"),
    re.compile(r"^\s*INDIA RICH LIST"),
    re.compile(r"^\s*2025\s*$"),
    re.compile(r"^\s*Celebrating"),
    re.compile(r"^\s*Change in wealth"),
    re.compile(r"^\s*Rank moved"),
    re.compile(r"^\s*Search\s*$"),
    re.compile(r"^\s*Show \d+ rows"),
    re.compile(r"^\s*Page\s+\d+"),
    re.compile(r"^\s*Stay updated"),
    re.compile(r"^\s*Subscribe"),
    re.compile(r"^\s*E-mail"),
    re.compile(r"^\s*PILLARS"),
    re.compile(r"^\s*FROM HURUN"),
    re.compile(r"^\s*ABOUT US"),
    re.compile(r"^\s*Wealth Creation"),
    re.compile(r"^\s*Value creation"),
    re.compile(r"^\s*Start-ups"),
    re.compile(r"^\s*Philanthropy"),
    re.compile(r"^\s*Culture"),
    re.compile(r"^\s*Hurun Lists"),
    re.compile(r"^\s*Reports"),
    re.compile(r"^\s*Media Release"),
    re.compile(r"^\s*Research Notes"),
    re.compile(r"^\s*Events"),
    re.compile(r"^\s*Our Story"),
    re.compile(r"^\s*Contact Us"),
    re.compile(r"^\s*Careers"),
    re.compile(r"^\s*Privacy Policy"),
    re.compile(r"^\s*Terms"),
]


def is_skip_line(line: str) -> bool:
    return any(p.search(line) for p in SKIP_PATTERNS)


def slice_col(line: str, start: int, end: int | None = None) -> str:
    """Return the slice of line between start and end columns (strip)."""
    if end is None:
        return line[start:].strip()
    return line[start:end].strip()


def parse_data_line(line: str) -> dict:
    """Pull rank, name-frag, wealth, company-frag, industry-frag, city from a data line."""
    # Rank is the first number on the line.
    rank_m = re.match(r"^\s*(\d{1,4})\s+", line)
    rank = rank_m.group(1) if rank_m else ""

    return {
        "rank": rank,
        "name_frag": slice_col(line, COL_NAME_START, COL_NAME_END),
        "wealth": slice_col(line, COL_WEALTH_START, COL_WEALTH_END),
        "company_frag": slice_col(line, COL_COMPANY_START, COL_COMPANY_END),
        "industry_frag": slice_col(line, COL_INDUSTRY_START, COL_INDUSTRY_END),
        "city": slice_col(line, COL_CITY_START),
    }


def parse_aux_line(line: str) -> dict:
    """Pull only the column fragments from a non-data (continuation) line."""
    return {
        "name_frag": slice_col(line, COL_NAME_START, COL_NAME_END),
        "company_frag": slice_col(line, COL_COMPANY_START, COL_COMPANY_END),
        "industry_frag": slice_col(line, COL_INDUSTRY_START, COL_INDUSTRY_END),
    }


def normalize_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main(src: Path, dst: Path):
    lines = src.read_text(encoding="utf-8").splitlines()

    # Filter out obvious junk lines (page headers/footers) but keep line
    # indices intact by replacing them with empty strings.
    clean_lines = []
    for line in lines:
        if is_skip_line(line):
            clean_lines.append("")
        else:
            clean_lines.append(line)

    # Identify data line indices.
    data_indices = []
    for i, line in enumerate(clean_lines):
        m = DATA_LINE_RE.match(line)
        if m:
            data_indices.append(i)

    print(f"Found {len(data_indices)} data lines")

    entries = []
    for idx, i in enumerate(data_indices):
        data = parse_data_line(clean_lines[i])

        # Look at up to 2 lines above and 2 lines below for continuations.
        # Stop expanding upward at the previous data line, and downward at
        # the next data line.
        prev_data = data_indices[idx - 1] if idx > 0 else -1
        next_data = data_indices[idx + 1] if idx + 1 < len(data_indices) else len(clean_lines)

        above = []
        for offset in (2, 1):
            j = i - offset
            if j > prev_data and j >= 0 and clean_lines[j].strip():
                above.append(parse_aux_line(clean_lines[j]))
            else:
                above.append({"name_frag": "", "company_frag": "", "industry_frag": ""})

        below = []
        for offset in (1, 2):
            j = i + offset
            if j < next_data and j < len(clean_lines) and clean_lines[j].strip():
                below.append(parse_aux_line(clean_lines[j]))
            else:
                below.append({"name_frag": "", "company_frag": "", "industry_frag": ""})

        # Stitch: above[0] = i-2, above[1] = i-1, data = i, below[0] = i+1, below[1] = i+2
        name = " ".join(
            x for x in [above[0]["name_frag"], above[1]["name_frag"], data["name_frag"], below[0]["name_frag"], below[1]["name_frag"]] if x
        )
        company = " ".join(
            x for x in [above[0]["company_frag"], above[1]["company_frag"], data["company_frag"], below[0]["company_frag"], below[1]["company_frag"]] if x
        )
        industry = " ".join(
            x for x in [above[0]["industry_frag"], above[1]["industry_frag"], data["industry_frag"], below[0]["industry_frag"], below[1]["industry_frag"]] if x
        )

        entries.append({
            "Rank": data["rank"],
            "Name": normalize_spaces(name),
            "Wealth_2025_INR_Cr": data["wealth"],
            "Company": normalize_spaces(company),
            "Industry": normalize_spaces(industry),
            "City_of_Residence": data["city"],
        })

    # Write to CSV.
    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Rank", "Name", "Wealth_2025_INR_Cr", "Company", "Industry", "City_of_Residence"],
        )
        writer.writeheader()
        writer.writerows(entries)

    print(f"Wrote {len(entries)} entries to {dst}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("txt", type=Path, help="flattened text dump of the PDF")
    parser.add_argument("-o", "--output", type=Path,
                        help="CSV to write (default: same name as the input, .csv extension)")
    args = parser.parse_args()
    main(args.txt, args.output or args.txt.with_suffix(".csv"))
