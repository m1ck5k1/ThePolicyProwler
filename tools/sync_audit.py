#!/usr/bin/env python3
"""
Sync a completed audit to the Airtable institutional memory base.
Reads the YAML front-matter from the audit file and creates/updates a record
in the Audits table of The Policy Prowler — Institutional Memory base.

Usage:
    python3 tools/sync_audit.py <path_to_audit_file.md>

Example:
    python3 tools/sync_audit.py research/audits/260222_Terminal_Autopsy_OBBBA.md

Requirements:
    pip install pyaml requests
    Add AIRTABLE_API_KEY=<token> to a .env file in the project root
    (or export AIRTABLE_API_KEY=<token> in your shell)
"""

import os
import sys
import json
from pathlib import Path


def load_dotenv():
    """Load .env from project root if present, without requiring python-dotenv."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
import re
import requests

# ── Airtable config ──────────────────────────────────────────────────────────
BASE_ID   = "appA8bFOOAw72AZ24"
TABLE_ID  = "tbl92R4P97QrUZvFE"
API_URL   = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_ID}"

# Field IDs (Audits table)
FIELDS = {
    "audit_id":          "fldXINLbNEhK6YW4Z",
    "subject":           "fldr4Ip1j2GFpGNAC",
    "date":              "fldEJmnCfMI2ZaGxE",
    "bill":              "fldPH0If7a7mjQd9L",
    "severity":          "fldXd013qCD3xIO6i",
    "status":            "fldoualrUYCDFxE8e",
    "key_figures":       "fldUGtoTh9D8IaUQG",
    "actors":            "fldwSu6XWRZ6YtB4x",
    "affected_programs": "fldJaDqAO3OwzwuGh",
    "house_vote":        "fldcD9Uw47JWDXIb0",
    "senate_vote":       "fld4j07g7Q8NlJMb2",
    "tags":              "fldFFfsaUoa0YHzNz",
    "related_audits":    "flddySQ4VX1kytpAI",
    "file_path":         "fldxeuIrUn4oE6Ivb",
}


def extract_frontmatter(path: str) -> dict:
    """Parse YAML front-matter block from a markdown file."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        sys.exit(f"Error: no YAML front-matter found in {path}")

    try:
        import yaml
        return yaml.safe_load(match.group(1))
    except ImportError:
        # Minimal fallback parser for simple key: value lines
        fm = {}
        for line in match.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip().strip('"')
        return fm


def build_record(fm: dict, file_path: str) -> dict:
    """Map front-matter fields to Airtable field IDs."""

    def list_to_str(val) -> str:
        if isinstance(val, list):
            return "\n".join(str(v) for v in val)
        return str(val) if val else ""

    def kf_to_str(key_figures) -> str:
        if isinstance(key_figures, list):
            lines = []
            for item in key_figures:
                if isinstance(item, dict):
                    lines.append(f"{item.get('label', '')}: {item.get('value', '')}")
                else:
                    lines.append(str(item))
            return "\n".join(lines)
        return str(key_figures) if key_figures else ""

    record = {}

    if fm.get("audit_id"):
        record[FIELDS["audit_id"]] = fm["audit_id"]
    if fm.get("subject"):
        record[FIELDS["subject"]] = fm["subject"]
    if fm.get("date"):
        # Normalise YYMMDD → YYYY-MM-DD for Airtable
        d = str(fm["date"]).strip('"')
        if len(d) == 6 and d.isdigit():
            d = f"20{d[:2]}-{d[2:4]}-{d[4:]}"
        record[FIELDS["date"]] = d
    if fm.get("bill") and fm["bill"] != "null":
        record[FIELDS["bill"]] = fm["bill"]
    if fm.get("severity"):
        record[FIELDS["severity"]] = fm["severity"]
    if fm.get("status"):
        record[FIELDS["status"]] = fm["status"]
    if fm.get("key_figures"):
        record[FIELDS["key_figures"]] = kf_to_str(fm["key_figures"])
    if fm.get("actors"):
        record[FIELDS["actors"]] = list_to_str(fm["actors"])
    if fm.get("affected_programs"):
        record[FIELDS["affected_programs"]] = list_to_str(fm["affected_programs"])
    if fm.get("vote_counts"):
        vc = fm["vote_counts"]
        if isinstance(vc, dict):
            if vc.get("house"):
                record[FIELDS["house_vote"]] = vc["house"]
            if vc.get("senate"):
                record[FIELDS["senate_vote"]] = vc["senate"]
    if fm.get("tags"):
        record[FIELDS["tags"]] = fm["tags"] if isinstance(fm["tags"], list) else [fm["tags"]]
    if fm.get("related_audits"):
        record[FIELDS["related_audits"]] = list_to_str(fm["related_audits"])

    record[FIELDS["file_path"]] = file_path

    return record


def push_to_airtable(record: dict, api_key: str) -> str:
    """POST the record to Airtable. Returns the created record ID."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"records": [{"fields": record}], "typecast": True}
    resp = requests.post(API_URL, headers=headers, data=json.dumps(payload))

    if resp.status_code not in (200, 201):
        sys.exit(f"Airtable error {resp.status_code}: {resp.text}")

    created_id = resp.json()["records"][0]["id"]
    return created_id


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/sync_audit.py <audit_file.md>")
        sys.exit(1)

    audit_path = sys.argv[1]
    if not os.path.exists(audit_path):
        sys.exit(f"File not found: {audit_path}")

    load_dotenv()
    api_key = os.environ.get("AIRTABLE_API_KEY")
    if not api_key:
        sys.exit("Error: AIRTABLE_API_KEY not found.\n"
                 "Add it to .env in the project root:\n"
                 "  echo 'AIRTABLE_API_KEY=your_token' > .env")

    fm = extract_frontmatter(audit_path)
    record = build_record(fm, audit_path)

    print(f"Syncing: {fm.get('audit_id', audit_path)}")
    record_id = push_to_airtable(record, api_key)
    print(f"Created Airtable record: {record_id}")
    print(f"Base: https://airtable.com/{BASE_ID}/{TABLE_ID}")


if __name__ == "__main__":
    main()
