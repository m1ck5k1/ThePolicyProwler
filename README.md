# The Policy Prowler

> *Contrarian legislative auditor and cyberpunk-noir fiscal forensicist.*
> *Auditing the Legislative Stack. Identifying systemic debt bugs, fiscal malware, and the arithmetic of insolvency.*

---

## What This Is

The Policy Prowler is a structured research and publication system for forensic fiscal journalism. It treats legislation the way a security researcher treats source code — scanning for hidden riders, arithmetic leaks, and lobby-funded exploits — and publishes findings as noir dispatches.

**Core framing:**
- Official bill summaries = **User Interface**. The arithmetic = **the Kernel**.
- CBO baseline projections = **Optimistic Simulation**. Cross-referenced against real-world interest rate friction.
- Every "bipartisan" bill is a suspected fiscal trap until the math proves otherwise (**Zero-Trust policy**).

---

## Repository Layout

```
data/
  bills/          — Raw legislative source code (bill text, amendments, diffs)
  cbo_reports/    — CBO "Optimistic Simulation" logs
  archive/        — Superseded or historical data

research/
  audits/         — Verified bug reports and forensic breakdowns

articles/
  published/      — Immutable noir dispatches (never edited post-publish)

templates/        — Audit and article scaffolding
tools/            — Ingestion, triage, formatting, and sync pipeline scripts
logs/             — Operational session logs
```

---

## Forensic Workflow

1. **Ingest** — Drop raw bills/CBO reports into `data/`
2. **Scan** — Identify bugs: Midnight Riders, Arithmetic Leaks, Localized Bribes
3. **Diff** — Compare House vs. Senate versions; track delta between cost estimates
4. **Audit** — Generate a Bug Report in `research/audits/` using `templates/audit_bug_report.md`
5. **Dispatch** — Write the published article using `templates/article_dispatch.md`
6. **Sync** — Push audit record to Airtable institutional memory

---

## Tools

| Script | Purpose |
|---|---|
| `tools/ingest_bill.sh` | Download and stage bill text from congress.gov |
| `tools/diff_bills.sh` | Diff two bill versions to surface delta |
| `tools/poll_bills.py` | Poll Congress.gov for new bills; Claude Haiku triage for Prowler relevance |
| `tools/format_table.py` | Render LaTeX budget comparison tables (3-decimal, Substack-compatible) |
| `tools/sync_audit.py` | Sync completed audit YAML front-matter to Airtable institutional memory |
| `tools/publish.py` | Finalize and stamp a dispatch for `articles/published/` |

### Automated Bill Monitor

`tools/poll_bills.py` runs on a schedule, pulling recently updated legislation from the Congress.gov API, applying keyword pre-filters, then scoring survivors with Claude Haiku for fiscal exploit vectors. High-scoring bills are auto-staged for triage.

```bash
python3 tools/poll_bills.py [--dry-run] [--hours N] [--min-score N]
```

Output is a JSON list of scored bills, ready to feed directly into an audit.

---

## Setup

```bash
cp .env.example .env
# Fill in the three keys:
#   CONGRESS_API_KEY   — free at api.congress.gov/sign-up
#   ANTHROPIC_API_KEY  — Anthropic console
#   AIRTABLE_API_KEY   — Airtable personal access token (data.records:write scope)

pip install anthropic requests pyaml
```

---

## Citation Protocol

Every published fact requires a source. Canonical sources:

- **Bill text:** congress.gov
- **CBO data:** cbo.gov
- **House votes:** clerk.house.gov
- **Senate votes:** senate.gov/legislative/votes_new.htm
- **Treasury data:** fiscaldata.treasury.gov

All audit records are registered in [`RESEARCH_INDEX.md`](RESEARCH_INDEX.md).

---

## File Naming

`YYMMDD_Short_Title.md` — e.g., `260222_Lobbyist_ROI_Audit.md`

Audit IDs: `AUD-YYMMDD-SUBJECT` (embedded in each audit's YAML front-matter)

---

## License

MIT — see [LICENSE](LICENSE).
