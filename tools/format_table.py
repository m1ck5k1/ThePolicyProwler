#!/usr/bin/env python3
"""
Convert a CSV file of budget/fiscal data into a LaTeX array table
formatted for Prowler audits (Substack-compatible, 3-decimal precision).

Usage:
    python3 tools/format_table.py <input.csv> [--caption "Table title"] [--highlight-last]

Input CSV format (first row = headers):
    Component,Value (USD),Delta,Status
    Net TGA Cash Outflow,-11.400B,,CRITICAL DRAIN
    Debt Interest Accrual,-2.810B,,KERNEL LEAK

Output: LaTeX array block, printed to stdout. Paste into an audit .md file.
"""

import csv
import sys
import argparse
from pathlib import Path


def fmt_value(val: str) -> str:
    """Format a value string for LaTeX — escape $ and % signs."""
    val = val.strip()
    val = val.replace("$", r"\$").replace("%", r"\%").replace("&", r"\&")
    return val


def csv_to_latex(csv_path: str, caption: str = "", highlight_last: bool = False) -> str:
    rows = []
    headers = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            else:
                rows.append(row)

    if not headers:
        sys.exit("Error: CSV has no headers.")

    n_cols = len(headers)
    col_spec = "|" + "|".join(["l"] + ["r"] * (n_cols - 1)) + "|"

    lines = []
    lines.append("$$")
    lines.append(r"\small")
    lines.append(r"\begin{array}{" + col_spec + "}")
    lines.append(r"\hline")

    # Header row
    header_cells = " & ".join(r"\textbf{" + h.strip().replace("_", r"\_") + "}" for h in headers)
    lines.append(header_cells + r" \\[0.5ex]")
    lines.append(r"\hline")

    # Data rows
    for j, row in enumerate(rows):
        is_last = j == len(rows) - 1
        cells = " & ".join(fmt_value(c) for c in row)
        if highlight_last and is_last:
            cells = " & ".join(r"\textbf{" + fmt_value(c) + "}" for c in row)
        lines.append(cells + r" \\")
        if highlight_last and is_last:
            lines.append(r"\hline")

    lines.append(r"\hline")
    lines.append(r"\end{array}")
    if caption:
        lines.append(r"% Caption: " + caption)
    lines.append("$$")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CSV → LaTeX array for Prowler audits")
    parser.add_argument("csv_file", help="Path to input CSV")
    parser.add_argument("--caption", default="", help="Optional table caption comment")
    parser.add_argument("--highlight-last", action="store_true",
                        help="Bold the last row (use for TOTAL rows)")
    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        sys.exit(f"Error: file not found: {args.csv_file}")

    output = csv_to_latex(args.csv_file, caption=args.caption, highlight_last=args.highlight_last)
    print(output)


if __name__ == "__main__":
    main()
