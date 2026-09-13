"""Approach 3: Extract the Hurun list directly from the PDF using pdfplumber.

Usage:
    python3 parse_hurun_pdf_with_pdfplumber.py Hurun-India-Rich-List-Oct-2025.pdf
    python3 parse_hurun_pdf_with_pdfplumber.py input.pdf -o out.csv
"""
import argparse
import csv
from pathlib import Path

import pdfplumber

HEADERS = ["Rank", "Name", "Wealth_2025_INR_Cr", "Company", "Industry", "City_of_Residence"]

parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
parser.add_argument("pdf", type=Path, help="source PDF")
parser.add_argument("-o", "--output", type=Path,
                    help="CSV to write (default: same name as the PDF, .csv extension)")
args = parser.parse_args()

PDF = args.pdf
OUT = args.output or PDF.with_suffix(".csv")


def clean_cell(cell):
    """Replace internal newlines with a single space; collapse whitespace."""
    if cell is None:
        return ""
    return " ".join(cell.split())


def is_data_row(row):
    """A data row has a numeric value in the first cell (the rank)."""
    if not row or not row[0]:
        return False
    first = clean_cell(row[0])
    return first.isdigit()


entries = []
with pdfplumber.open(PDF) as pdf:
    for page in pdf.pages:
        for table in page.extract_tables():
            for row in table:
                if is_data_row(row):
                    entries.append([clean_cell(c) for c in row])

print(f"Extracted {len(entries)} entries")

# Quick sanity: first and last 3
print("\nFirst 3:")
for r in entries[:3]:
    print(" ", r)
print("\nLast 3:")
for r in entries[-3:]:
    print(" ", r)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(entries)

print(f"\nWrote to {OUT}")
