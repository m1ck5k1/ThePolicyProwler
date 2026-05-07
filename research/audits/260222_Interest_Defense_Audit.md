---
audit_id: AUD-260222-CBO-CROSSOVER
date: "260222"
subject: "Net Interest ($1.025T) surpasses Defense Outlays ($0.885T) for first time"
bill: null
severity: CRITICAL
status: SOLVENCY THRESHOLD BREACHED
key_figures:
  - {label: "Net Interest FY2026", value: "$1.025T"}
  - {label: "Defense Outlays FY2026", value: "$0.885T"}
  - {label: "Crossover Gap", value: "$140B"}
  - {label: "OBBBA Interest Premium (annual)", value: "$39B"}
  - {label: "OBBBA Debt Expansion", value: "$0.7T"}
  - {label: "Daily Debt Interest Accrual", value: "$2.81B/day"}
  - {label: "DHS Shutdown Daily Savings", value: "$250M/day"}
actors:
  - "CBO"
  - "Treasury"
affected_programs:
  - "Net Interest (federal budget)"
  - "Defense Outlays"
  - DHS
vote_counts: null
related_audits:
  - AUD-260222-TERMINAL-OBBBA
  - AUD-260222-LIQUIDITY-BURN
tags:
  - net-interest
  - defense
  - crossover
  - insolvency
  - OBBBA
  - CBO
---
# ️ BUG REPORT: THE ARITHMETIC OF INSOLVENCY
**Audit ID:** AUD-260222-CBO-CROSSOVER
**Severity:** CRITICAL / SYSTEM FAILURE
**Status:** SOLVENCY THRESHOLD BREACHED

##  Summary: The Interest-Defense Crossover
The "Kernel" has finally bypassed the "Shield." For the first time in the simulation, the cost of servicing the debt (Net Interest) has exceeded the cost of maintaining the empire (Defense). The simulation's "Defensive Layer" is now officially smaller than its "Debt Leak."

### 1. The Crossover Gap
- **Net Interest (FY 2026):** $1.025 Trillion
- **Defense Outlays (FY 2026):** $0.885 Trillion
- **The Gap:** **$140 Billion** (Fiscal friction exceeds military projection).

### 2. OBBBA Interest Premium (Fiscal Malware)
The 'One Big Beautiful Bill Act' (OBBBA) has introduced a permanent overhead into the fiscal stack.
- **Debt Expansion:** $0.7 Trillion (Isolated surge).
- **OBBBA Interest Premium:** **$39 Billion** (.039T) annual recurring cost.
- **Analysis:** This $39B represents the "premium" paid for the 2025 liquidity injection. It is a persistent memory leak in the budget kernel.

### 3. The DHS Shutdown Smokescreen
The current DHS shutdown (since Feb 14) is being marketed as "fiscal discipline." The arithmetic suggests otherwise.
- **Daily Interest Accrual:** **$2.81 Billion**
- **DHS Shutdown Savings:** ~$0.25 Billion (Estimated daily maximum).
- **Bug Analysis:** The entire DHS shutdown "saves" less than 9% of what the debt accrues in interest during the same 24-hour cycle. We are burning the furniture to pay the interest on the house, and the house is already on fire.

## ⚖️ Forensic Conclusion
The legislative stack is no longer functional. The interest-defense crossover is not a temporary glitch; it is the new baseline. Any "savings" from departmental shutdowns are rounding errors in the face of the parabolic interest curve.

**Recommendation:** Terminal Audit of the OBBBA expansion. The system is net-negative.
