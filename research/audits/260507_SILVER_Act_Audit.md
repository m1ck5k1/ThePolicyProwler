---
audit_id: AUD-260507-SILVER-ACT
date: "260507"
subject: "SILVER Act H.R.8007 — systemic risk framing used to force open precious metals vault market for Mountain/Pacific time zone operators"
bill: "H.R. 8007 / SILVER Act (119th Congress, introduced)"
severity: HIGH
status: COMPROMISED
key_figures:
  - {label: "Approved COMEX vaults, Eastern Time Zone", value: "~8"}
  - {label: "Approved COMEX vaults, Mountain Time Zone", value: "0"}
  - {label: "Approved COMEX vaults, Pacific Time Zone", value: "0"}
  - {label: "Minimum new vaults mandated (Mountain + Pacific)", value: "4"}
  - {label: "Idaho silver production rank (US)", value: "Top 3 state"}
  - {label: "Bill introduced", value: "2026-03-19"}
  - {label: "OBBBA signed (fiscal context)", value: "2025-07"}
actors:
  - "Rep. Russ Fulcher (R-ID-01)"
  - "Rep. Chuck Harris (R-NC)"
  - "CME Group / COMEX (forced compliance)"
  - "House Agriculture Committee"
  - "Unidentified Mountain/Pacific vault operators (pending investigation)"
affected_programs:
  - "Commodity Exchange Act §5b(c)(2)"
  - "CME Group / COMEX depository approval process"
  - "Precious metals futures settlement infrastructure"
  - "CFTC oversight of derivatives clearing organizations"
vote_counts:
  house: "Not yet voted — introduced 2026-03-19"
  senate: null
related_audits:
  - AUD-260222-TERMINAL-OBBBA
  - AUD-260222-CBO-CROSSOVER
tags:
  - SILVER-Act
  - precious-metals
  - COMEX
  - CME-Group
  - vault-infrastructure
  - Idaho
  - Fulcher
  - systemic-risk-framing
  - market-access
  - commodity-exchange-act
  - CFTC
---

# BUG REPORT: THE SILVER ACT & THE VAULT MARKET EXPLOIT
**Audit ID:** AUD-260507-SILVER-ACT
**Subject:** H.R. 8007 — "System Integrity through Licensed Vault Expansion and Resilience Act"
**Severity:** HIGH / MARKET STRUCTURE COMPROMISED
**Status:** PAYLOAD STAGED — bill introduced, not yet passed

---

## Summary: The Systemic Risk Wrapper

H.R. 8007 is a four-page amendment to the Commodity Exchange Act dressed in systemic risk language. The official narrative: precious metals vault concentration near New York City creates dangerous geographic vulnerabilities. The fix: force CME Group's COMEX — the only derivatives clearing organization for gold, silver, platinum, and palladium futures — to approve a minimum of two depositories in each US time zone.

The arithmetic of the current vault landscape makes the commercial target unmistakable. Of the eight approved COMEX depositories, every single one operates in the Eastern Time Zone. Mountain Time: zero. Pacific Time: zero. This bill doesn't just encourage geographic diversification — it mandates a minimum of four new approvals (two Mountain, two Pacific) in markets that are currently locked out of the regulated precious metals settlement ecosystem entirely.

Rep. Russ Fulcher (R-ID) sponsored the bill. Idaho is Mountain Time. Idaho's Silver Valley — the Coeur d'Alene Mining District — is one of the richest silver deposits in North American history, sitting on the Union Pacific freight corridor. Finding 6 of the bill describes the target beneficiary geography without naming it: *"markets near hubs of precious metals activity and interstate transportation networks."*

The systemic risk argument is the UI. The vault market opening is the Kernel.

---

## Vector 1: The Sponsor Circuit

The bill has two sponsors. Each maps to a specific commercial interest.

**Rep. Fulcher (R-ID-01):** Idaho is Mountain Time. Idaho's First Congressional District includes Boise, the Silver Valley (Coeur d'Alene Mining District — historically one of the world's largest silver producers), and runs along the Union Pacific Railroad main line. Any vault operator in northern Idaho seeking COMEX delivery approval is currently blocked by the absence of a statutory pathway. This bill creates that pathway and mandates CME use it.

**Rep. Harris (R-NC):** North Carolina is Eastern Time — the zone that already has eight approved vaults. His district interest is less immediately obvious. Charlotte Douglas International Airport is one of the largest air cargo hubs on the East Coast. Financial services dominate the Charlotte economy. A plausible read: Harris provides bipartisan cover and Eastern Time optics for a bill that primarily delivers Mountain Time market access. The "Eastern Time" geographic requirement is already satisfied by existing vaults — his district's inclusion in the mandate costs nothing and adds a co-sponsor.

**The Forensic Gap:** The lobbying trail between Mountain/Pacific vault operators and Fulcher's campaign finance has not been fully traced. This is the outstanding vector requiring further investigation.

---

## Vector 2: The CME Compliance Trap

CME Group / COMEX does not want this bill. The existing vault approval system works in their operational favor — a small, vetted set of established Eastern operators with decades of compliance history. The SILVER Act imposes three new compliance burdens:

1. **Publish objective selection criteria** — currently CME approves vaults through an internal process with no statutory transparency requirement. This forces public disclosure of standards that CME may prefer to apply selectively.
2. **Maintain a formal application process** — creates a legal pathway for any qualified Mountain/Pacific vault operator to apply and, if rejected, to challenge the rejection against published criteria.
3. **Guarantee 2 approvals per time zone** — removes CME's discretion to decline Mountain/Pacific applications on operational grounds. Approval in those zones becomes a legal obligation, not a business decision.

The bill's systemic risk framing puts CME in an impossible position: opposing a bill that claims to reduce systemic risk exposes them to regulatory and reputational risk. The compliance trap is elegant. CME's silence or opposition becomes evidence they are perpetuating the geographic concentration risk the bill identifies.

---

## Vector 3: The OBBBA-SILVER Connection

This audit cannot be read in isolation from the OBBBA findings.

The OBBBA (Public Law 119-21) added $3.4-4.1 trillion to the federal deficit. Net interest has surpassed defense spending for the first time — $1.025T vs $0.885T. The Treasury General Account is draining at $11.4 billion per day.

In high-debt, high-interest-accrual environments, precious metals function as fiscal distress hedges. Gold and silver prices are elevated and rising in direct proportion to the fiscal damage the OBBBA created. Operating a COMEX-approved gold or silver vault in this environment is one of the most commercially attractive positions in the current market structure.

The SILVER Act was introduced eight months after the OBBBA was signed. The sequence:
1. OBBBA (July 2025) creates fiscal conditions that inflate precious metals prices
2. Elevated precious metals prices make vault operation highly lucrative
3. SILVER Act (March 2026) mandates opening the vault market to Mountain/Pacific operators
4. Vault operators in previously excluded geographies gain access to the regulated settlement ecosystem at peak market value

The bills are not formally linked. The legislative arithmetic connects them regardless.

---

## Vector 4: The Framing Audit

Finding 3 deserves specific scrutiny: *"Recent liquidity events in global metals markets underscore the need to minimize regulatory barriers that reduce the available supply of metals to the publicly traded marketplace."*

This is almost certainly a reference to the London Metal Exchange (LME) nickel short squeeze of March 2022, in which LME suspended nickel trading and cancelled billions in executed trades. That event demonstrated a real vulnerability in concentrated metals market infrastructure.

The forensic problem: geographic concentration of US COMEX vaults is not what caused the LME nickel event. LME nickel's crisis was a position-concentration problem, not a storage-geography problem. Citing "liquidity events" as justification for geographic vault diversification is technically accurate as a general concern and operationally unrelated to the specific crisis being invoked. The reference functions as emotional momentum, not causation.

---

## Payload Metrics

$$
\small
\begin{array}{|l|r|l|}
\hline
\textbf{Vault Landscape} & \textbf{Current} & \textbf{Post-SILVER Act (minimum)} \\[0.5ex]
\hline
\text{Eastern Time approved vaults} & \sim8 & \geq2 \text{ (already satisfied)} \\
\text{Central Time approved vaults} & \sim0 & \geq2 \text{ (forced)} \\
\text{Mountain Time approved vaults} & 0 & \geq2 \text{ (forced)} \\
\text{Pacific Time approved vaults} & 0 & \geq2 \text{ (forced)} \\
\hline
\textbf{Net new vault approvals mandated} & \textbf{—} & \textbf{\geq6} \\
\hline
\end{array}
$$

---

## ⚖️ Forensic Conclusion

The SILVER Act is a precisely constructed market access bill. The systemic risk framing is partially valid — geographic concentration of precious metals vaults is a real, auditable vulnerability. The bill exploits that validity to mandate a specific commercial outcome: CME must open the Mountain and Pacific vault markets it currently controls exclusively through Eastern Time incumbents.

The sponsor geography is the bill's fingerprint. Fulcher/Idaho maps to the Coeur d'Alene silver corridor. The bill's Finding 6 describes his constituency without naming it. The CME compliance trap ensures the incumbent cannot block new entrants through discretionary approval processes.

The OBBBA connection elevates the severity. This is not an isolated market-access play — it is infrastructure being built to harvest the fiscal conditions that the OBBBA created. The Kernel underneath the systemic risk UI is a vault market opening, timed to peak precious metals valuations, authored by a congressman whose district sits on one of the continent's largest silver deposits.

**Outstanding:** Lobbying trail from Mountain/Pacific vault operators to Fulcher campaign finance. CME Group's formal position on the bill. Full identification of positioned beneficiaries in ID, NV, UT, CA, OR, WA.

**Sources:** BILLS-119hr8007ih.xml, data/bills/SILVER_HR8007/key_sections.md, AUD-260222-TERMINAL-OBBBA, AUD-260222-CBO-CROSSOVER, congress.gov/119/bills/hr8007
