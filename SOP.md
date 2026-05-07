# ️ THE POLICY PROWLER: STANDARD OPERATING PROCEDURE

## 1.0 THE CITATION PROTOCOL (Open Ledger)
- **Zero-Trust Rule:** Every fact, dollar amount, and vote count must be followed by a source.
- **Source Map:**
    - CBO Data: https://www.cbo.gov (reports mirrored locally in `data/cbo_reports/`)
    - Legislative Text: https://www.congress.gov
    - House Vote Records: https://clerk.house.gov
    - Senate Vote Records: https://www.senate.gov/legislative/votes_new.htm
    - Daily Treasury Statement: https://fiscaldata.treasury.gov/datasets/daily-treasury-statement
- **Verification:** Any audit must cross-reference the local file (e.g., 260211_CBO_Budget_Outlook.md) against the Airtable source ID in the Legislative_Base.

## 2.0 FORENSIC WORKFLOW
- **Step 1: Ingest.** Move raw bills/reports into /data.
- **Step 2: Scan.** Identify "Bugs" (Midnight Riders, Arithmetic Leaks).
- **Step 3: Diff.** Compare House vs. Senate versions of text.
- **Step 4: Audit.** Generate the 'Bug Report' in research/audits.
- **Step 5: Sync.** Push the audit to institutional memory via nlm source add.

## 3.0 DATA VISUALIZATION
- **LaTeX Tables:** Use for all budget comparisons to ensure 3-decimal precision and Substack compatibility.
