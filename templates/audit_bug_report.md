---
audit_id: AUD-YYMMDD-[SUBJECT-SLUG]
date: "YYMMDD"
subject: "[one-line description]"
bill: "[H.R. X / Public Law XXX-XX (SHORT NAME)] or null"
severity: "[LOW / MEDIUM / HIGH / CRITICAL / TERMINAL]"
status: "[CLEAN / COMPROMISED / MALICIOUS CODE INJECTED / INSOLVENT / TERMINAL SYSTEM FAILURE / PAYLOAD DEPLOYED / SOLVENCY THRESHOLD BREACHED / SEVERE SYSTEMIC FAILURE / INSOLVENCY ACCELERATING]"
key_figures:
  - {label: "[Label]", value: "[Dollar amount or ratio]"}
actors:
  - "[Actor name]"
affected_programs:
  - "[Program name]"
vote_counts:
  house: "[NNN-NNN (Date)]"
  senate: "[Result or null]"
related_audits:
  - AUD-YYMMDD-[RELATED-SLUG]
tags:
  - [tag]
---

# [EMOJI] BUG REPORT: [SUBJECT — ALL CAPS]
**Audit ID:** AUD-YYMMDD-[SUBJECT-SLUG]
**Subject:** [Full bill name, provision, or topic]
**Severity:** [LOW / MEDIUM / HIGH / CRITICAL / TERMINAL]
**Status:** [CLEAN / COMPROMISED / MALICIOUS CODE INJECTED / INSOLVENT / TERMINAL SYSTEM FAILURE]

---

## [EMOJI] Summary: [One-line hook]
[2-3 sentence executive summary. State the exploit, name the arithmetic, name the actors.
No narrative throat-clearing — open on the wound.]

---

## [EMOJI] Vector 1: [Name of the first exploit or mechanism]
**Target:** [Specific bill section, fund, vote, or actor]
**The UI:** [What the official narrative claims]
**The Kernel:** [What the arithmetic actually shows]

[Supporting detail. Cross-reference local data files where possible.]

- **Key Figure 1:** $X.XXX [B/T] — [what it is]
- **Key Figure 2:** X.XX% — [what it measures]

---

## [EMOJI] Vector 2: [Name]
[Same structure as Vector 1.]

---

## [EMOJI] Vector 3: [Name — add/remove vectors as needed]
[Same structure.]

---

## Payload Metrics (LaTeX Table — if applicable)

$$
\small
\begin{array}{|l|r|r|r|}
\hline
\textbf{Component} & \textbf{Value} & \textbf{Delta} & \textbf{Status} \\[0.5ex]
\hline
\text{Row 1} & \$X.XXX\text{B} & +X.X\% & \text{STATUS} \\
\hline
\textbf{TOTAL} & \textbf{\$X.XXX\text{T}} & & \textbf{SYSTEM STATUS} \\
\hline
\end{array}
$$

---

## ⚖️ Forensic Conclusion
[2-4 sentences. Restate the core arithmetic finding. Name the systemic implication.
End on the immutable fact, not an opinion.]

**Sources:**
- [Source 1 — local file or URL]
- [Source 2]
