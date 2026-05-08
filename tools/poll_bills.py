#!/usr/bin/env python3
"""
Poll Congress.gov for recently updated bills, apply keyword pre-filter,
then triage survivors with Claude Haiku to score Prowler relevance.

Usage:
    python3 tools/poll_bills.py [--dry-run] [--hours N] [--min-score N]

Output (stdout):
    JSON list of objects:
    [{"bill_id": "119hr8007", "score": 4, "reason": "...", "vectors": [...], "title": "..."}, ...]

Exit codes:
    0 — completed (check stdout for results)
    1 — fatal error (bad credentials, API down)

Requirements:
    pip install anthropic requests
    CONGRESS_API_KEY in .env or environment
    ANTHROPIC_API_KEY in .env or environment
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── bootstrap .env ────────────────────────────────────────────────────────────

def load_dotenv():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())

load_dotenv()

import requests
import anthropic

# ── Congress.gov API ──────────────────────────────────────────────────────────

CONGRESS_API_BASE = "https://api.congress.gov/v3"
CONGRESS_API_KEY  = os.environ.get("CONGRESS_API_KEY", "")

# Current congress; bump when 120th convenes
ACTIVE_CONGRESS = 119

# Polling parameters
DEFAULT_HOURS  = 26   # slightly more than 24h to avoid edge gaps on daily cron
DEFAULT_LIMIT  = 250  # max per page; congress.gov caps at 250

# ── Keyword pre-filter ────────────────────────────────────────────────────────
# Bills must mention at least one of these (case-insensitive, in title or summary)
# before Claude sees them. Keeps triage cost low.

KEYWORDS = [
    # Fiscal / debt
    "deficit", "debt ceiling", "debt limit", "reconciliation", "continuing resolution",
    "appropriation", "supplemental appropriation", "sequestration", "rescission",
    "budget resolution", "omnibus",
    # Revenue / tax
    "tax cut", "revenue act", "excise tax", "tariff", "customs duty", "trade remedy",
    # Entitlements / Medicaid
    "medicaid", "medicare", "snap", "supplemental nutrition", "chip", "affordable care",
    "social security", "disability insurance",
    # Financial markets / commodities
    "commodity exchange", "derivatives", "futures", "clearing organization", "depository",
    "precious metals", "gold", "silver", "vault", "cftc", "sec oversight",
    "systemic risk", "too big to fail", "resolution authority",
    # Regulatory capture / carve-outs
    "exemption", "carve-out", "waiver", "safe harbor", "preemption",
    "deregulation", "regulatory relief", "streamline",
    # Defense / DHS smokescreen patterns
    "emergency supplemental", "border security supplemental", "national emergency",
    # Lobbying / campaign finance
    "campaign finance", "dark money", "lobbyist disclosure", "revolving door",
    # Geographic / industry markers from OBBBA/SILVER audit threads
    "idaho", "silver valley", "union pacific", "coeur d'alene",
    "treasury general account", "tga", "interest on the national debt",
]

_KEYWORD_PATTERN = re.compile(
    "|".join(re.escape(kw) for kw in KEYWORDS),
    re.IGNORECASE,
)


def keyword_match(title: str, summary: str | None) -> bool:
    text = title + " " + (summary or "")
    return bool(_KEYWORD_PATTERN.search(text))


# ── Congress.gov polling ──────────────────────────────────────────────────────

def fetch_recent_bills(hours: int) -> list[dict]:
    """Return bills updated within the last `hours` hours."""
    if not CONGRESS_API_KEY:
        sys.exit("Error: CONGRESS_API_KEY not set. Add it to .env:\n  CONGRESS_API_KEY=your_key")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    from_dt = cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {
        "api_key":     CONGRESS_API_KEY,
        "congress":    ACTIVE_CONGRESS,
        "sort":        "updateDate+desc",
        "limit":       DEFAULT_LIMIT,
        "fromDateTime": from_dt,
        "format":      "json",
    }

    url = f"{CONGRESS_API_BASE}/bill"
    resp = requests.get(url, params=params, timeout=30)

    if resp.status_code != 200:
        sys.exit(f"Congress.gov API error {resp.status_code}: {resp.text[:500]}")

    data = resp.json()
    bills = data.get("bills", [])

    print(f"[poll] {len(bills)} bills updated since {from_dt}", file=sys.stderr)
    return bills


def normalize_bill_id(bill: dict) -> str:
    """Convert Congress.gov bill object to canonical ID like '119hr8007'."""
    congress  = bill.get("congress", ACTIVE_CONGRESS)
    bill_type = bill.get("type", "").lower().replace(".", "")
    number    = bill.get("number", "")
    return f"{congress}{bill_type}{number}"


# ── Claude triage ─────────────────────────────────────────────────────────────

# System prompt is stable → cache it to minimize cost across batch calls
SYSTEM_PROMPT = """\
You are the triage engine for The Policy Prowler, a forensic journalism project \
that audits US legislation using cyberpunk-noir methodology: every bill has a \
"UI" (the official narrative) and a "Kernel" (the actual commercial or fiscal payload). \

Your job: given a bill title and summary, score its relevance to The Policy Prowler's \
investigative priorities on a scale of 1–5:

5 — CRITICAL. Clear fiscal damage, market-access exploit, regulatory capture, or \
    lobbyist-ROI pattern. Requires immediate full audit.
4 — HIGH. Strong Prowler-lens signals. Likely contains hidden vectors worth a \
    targeted investigation.
3 — MEDIUM. Possible angle. Flag for human review.
2 — LOW. Weak signal. Routine legislation with no obvious exploit.
1 — NOISE. No Prowler-relevant signal.

Prowler priority lenses (in order):
1. Fiscal bleed: bills that expand deficits, redirect TGA flows, or game debt-limit mechanics
2. Regulatory capture: carve-outs, exemptions, safe harbors that protect specific actors at systemic cost
3. Market-access exploits: bills that force open controlled markets for positioned insiders \
   (cf. SILVER Act H.R.8007 — vault mandate wrapped in systemic risk language)
4. Entitlement erosion: Medicaid, SNAP, CHIP, Social Security cuts hidden in reconciliation riders
5. Defense/DHS smokescreens: emergency supplementals that obscure fiscal damage
6. Geographic tells: bills whose findings language describes specific constituencies without naming them

Respond ONLY with valid JSON, no markdown, no explanation outside the JSON:
{"score": <1-5>, "reason": "<1-2 sentence forensic read>", "vectors": ["<vector1>", "<vector2>"]}\
"""


def triage_bills(candidates: list[dict], dry_run: bool = False) -> list[dict]:
    """Send candidates to Claude Haiku for scoring. Returns enriched list."""
    if not candidates:
        return []

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        sys.exit("Error: ANTHROPIC_API_KEY not set. Add it to .env.")

    client = anthropic.Anthropic(api_key=api_key)
    results = []

    for bill in candidates:
        bill_id = normalize_bill_id(bill)
        title   = bill.get("title", "(no title)")
        summary = bill.get("summary", {})
        summary_text = summary.get("text", "") if isinstance(summary, dict) else ""

        if dry_run:
            print(f"[dry-run] would triage: {bill_id} — {title[:80]}", file=sys.stderr)
            results.append({
                "bill_id": bill_id,
                "score":   0,
                "reason":  "dry-run",
                "vectors": [],
                "title":   title,
            })
            continue

        user_msg = f"Bill ID: {bill_id}\nTitle: {title}\nSummary: {summary_text[:1200] or '(none provided)'}"

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=256,
                system=[
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},  # cache stable system prompt
                    }
                ],
                messages=[{"role": "user", "content": user_msg}],
            )

            raw = response.content[0].text.strip()
            parsed = json.loads(raw)

            results.append({
                "bill_id": bill_id,
                "score":   parsed.get("score", 0),
                "reason":  parsed.get("reason", ""),
                "vectors": parsed.get("vectors", []),
                "title":   title,
                "url":     f"https://www.congress.gov/bill/{ACTIVE_CONGRESS}th-congress/"
                           f"{bill.get('type','').lower().replace('.','')}-bill/{bill.get('number','')}",
            })

            print(
                f"[triage] {bill_id} → score {parsed.get('score')} | {parsed.get('reason','')[:80]}",
                file=sys.stderr,
            )

        except (json.JSONDecodeError, KeyError, anthropic.APIError) as exc:
            print(f"[warn] triage failed for {bill_id}: {exc}", file=sys.stderr)
            results.append({
                "bill_id": bill_id,
                "score":   -1,
                "reason":  f"triage error: {exc}",
                "vectors": [],
                "title":   title,
            })

    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Poll Congress.gov and triage bills with Claude")
    parser.add_argument("--dry-run",   action="store_true", help="Skip Claude calls; print keyword matches only")
    parser.add_argument("--hours",     type=int, default=DEFAULT_HOURS, help="Look-back window in hours (default: 26)")
    parser.add_argument("--min-score", type=int, default=3, help="Minimum score to include in output (default: 3)")
    args = parser.parse_args()

    # 1. Fetch recent bills
    bills = fetch_recent_bills(args.hours)

    # 2. Keyword pre-filter
    candidates = [b for b in bills if keyword_match(b.get("title", ""), None)]
    print(
        f"[filter] {len(candidates)}/{len(bills)} bills passed keyword filter",
        file=sys.stderr,
    )

    if not candidates:
        print("[]")
        return

    # 3. Claude triage
    scored = triage_bills(candidates, dry_run=args.dry_run)

    # 4. Filter by min score and sort descending
    output = sorted(
        [r for r in scored if r["score"] >= args.min_score],
        key=lambda r: r["score"],
        reverse=True,
    )

    print(f"[result] {len(output)} bills at score ≥{args.min_score}", file=sys.stderr)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
