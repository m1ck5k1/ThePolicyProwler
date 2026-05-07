#!/usr/bin/env python3
"""
Format a published article for Substack.

Transforms a Prowler article from articles/published/ into a clean,
paste-ready Substack markdown file:
  - Converts LaTeX $$ ... $$ array tables → readable plain-text tables
  - Adds byline, datestamp, and estimated read time
  - Outputs to articles/substack_ready/ (created if needed)

Usage:
    python3 tools/publish.py <article_file.md> [--author "The Policy Prowler"]

Example:
    python3 tools/publish.py articles/published/260222_OBBBA_The_12000_ROI.md
"""

import os
import re
import sys
import math
import argparse
from pathlib import Path
from datetime import datetime


REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "articles" / "substack_ready"

WORDS_PER_MINUTE = 220


def estimate_read_time(text: str) -> int:
    words = len(re.findall(r"\w+", text))
    return max(1, math.ceil(words / WORDS_PER_MINUTE))


def parse_latex_array(block: str) -> str:
    """
    Convert a LaTeX \\begin{array} table block to a plain markdown table.
    Handles \\textbf{}, \\text{}, \\$, \\%, column alignment specs.
    """
    # Strip outer $$ and whitespace
    inner = re.sub(r"^\$\$\s*", "", block.strip())
    inner = re.sub(r"\s*\$\$$", "", inner)
    inner = re.sub(r"\\small\s*", "", inner)

    # Pull out rows between \hline markers
    # Remove \begin{array}{...} and \end{array}
    inner = re.sub(r"\\begin\{array\}\{[^}]*\}", "", inner)
    inner = re.sub(r"\\end\{array\}", "", inner)
    inner = re.sub(r"\\caption\{[^}]*\}", "", inner)

    # Split on \hline
    segments = re.split(r"\\hline", inner)
    rows = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        # Each row ends with \\ or \\[0.5ex]
        line_rows = re.split(r"\\\\(?:\[.*?\])?", seg)
        for row in line_rows:
            row = row.strip()
            if not row:
                continue
            rows.append(row)

    if not rows:
        return block  # fallback: return original if parsing fails

    def clean_cell(c: str) -> str:
        c = c.strip()
        c = re.sub(r"\{,\}", ",", c)             # LaTeX number grouping {,} → ,
        c = re.sub(r"\\\$", "$", c)
        c = re.sub(r"\\%", "%", c)
        # textbf/mathbf with possibly nested simple braces
        c = re.sub(r"\\(?:textbf|mathbf)\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"**\1**", c)
        c = re.sub(r"\\text\{([^}]*)\}", r"\1", c)
        c = re.sub(r"\{([^}]*)\}", r"\1", c)     # remove remaining braces
        c = re.sub(r"\s+", " ", c)
        return c.strip()

    md_rows = []
    for i, row in enumerate(rows):
        cells = [clean_cell(c) for c in row.split("&")]
        md_rows.append("| " + " | ".join(cells) + " |")
        if i == 0:
            md_rows.append("|" + "|".join(["---"] * len(cells)) + "|")

    return "\n".join(md_rows)


def convert_latex_tables(text: str) -> str:
    """Replace all $$ ... $$ LaTeX blocks containing array environments."""
    def replacer(m):
        block = m.group(0)
        if "\\begin{array}" in block or "\\begin{tabular}" in block:
            return parse_latex_array(block)
        # Non-table math — strip the $$ markers and leave inline
        return re.sub(r"^\$\$\s*|\s*\$\$$", "", block.strip())

    return re.sub(r"\$\$.*?\$\$", replacer, text, flags=re.DOTALL)


def format_datestamp(filename: str) -> str:
    """Extract YYMMDD from filename and return a readable date."""
    m = re.match(r"^(\d{6})", Path(filename).name)
    if m:
        try:
            return datetime.strptime(m.group(1), "%y%m%d").strftime("%B %d, %Y")
        except ValueError:
            pass
    return datetime.today().strftime("%B %d, %Y")


def build_substack_doc(content: str, filename: str, author: str) -> str:
    datestamp = format_datestamp(filename)
    read_time = estimate_read_time(content)

    # Strip existing italic metadata line if present (e.g. *The Policy Prowler | 260222 | ...*)
    content = re.sub(r"^\*The Policy Prowler.*?\*\s*\n+", "", content, flags=re.MULTILINE)

    converted = convert_latex_tables(content)

    byline = (
        f"*By {author} — {datestamp} · {read_time} min read*\n\n"
        "---\n\n"
    )

    footer = (
        "\n\n---\n\n"
        "*The Policy Prowler audits the legislative stack. "
        "Arithmetic over narrative. Zero-trust auditing.*"
    )

    return byline + converted.strip() + footer


def main():
    parser = argparse.ArgumentParser(description="Format Prowler article for Substack")
    parser.add_argument("article", help="Path to article in articles/published/")
    parser.add_argument("--author", default="The Policy Prowler",
                        help="Byline author name")
    args = parser.parse_args()

    src = Path(args.article)
    if not src.exists():
        sys.exit(f"File not found: {src}")

    content = src.read_text(encoding="utf-8")

    output = build_substack_doc(content, src.name, args.author)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dest = OUTPUT_DIR / src.name
    dest.write_text(output, encoding="utf-8")

    print(f"Published: {dest}")
    print(f"Read time: ~{estimate_read_time(content)} min")
    print("Next: copy contents of the output file and paste into Substack editor.")


if __name__ == "__main__":
    main()
