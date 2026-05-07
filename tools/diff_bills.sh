#!/usr/bin/env bash
# Diff two bill version files and produce a readable change report.
# Highlights added sections (Senate riders, cost changes) vs. the base version.
#
# Usage: ./tools/diff_bills.sh <base_file> <revised_file> [--output <report_file>]
# Example: ./tools/diff_bills.sh \
#            data/bills/OBBBA_HR1/house_v1_excerpt.md \
#            data/bills/OBBBA_HR1/senate_amendments.md \
#            --output research/audits/OBBBA_House_Senate_Diff.md

set -euo pipefail

BASE="${1:-}"
REVISED="${2:-}"
OUTPUT=""

# Parse --output flag
shift 2 || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

if [[ -z "$BASE" || -z "$REVISED" ]]; then
  echo "Usage: $0 <base_file> <revised_file> [--output <report_file>]"
  exit 1
fi

if [[ ! -f "$BASE" ]]; then
  echo "Error: base file not found: $BASE"
  exit 1
fi

if [[ ! -f "$REVISED" ]]; then
  echo "Error: revised file not found: $REVISED"
  exit 1
fi

DATESTAMP=$(date +%y%m%d)
BASE_NAME=$(basename "$BASE")
REVISED_NAME=$(basename "$REVISED")

REPORT=$(cat << HEADER
# BILL DIFF REPORT: $BASE_NAME → $REVISED_NAME
**Generated:** $DATESTAMP
**Base:** $BASE
**Revised:** $REVISED

---

## Summary of Changes

\`\`\`diff
HEADER
)

DIFF_OUTPUT=$(diff --unified=3 "$BASE" "$REVISED" || true)

ADDED=$(echo "$DIFF_OUTPUT" | grep -c "^+" || true)
REMOVED=$(echo "$DIFF_OUTPUT" | grep -c "^-" || true)

FULL_REPORT="${REPORT}
${DIFF_OUTPUT}
\`\`\`

---

## Change Metrics
- Lines added:   $ADDED
- Lines removed: $REMOVED

## Forensic Notes
[Add analysis here: identify midnight riders, cost changes, new actors]
- [ ] Review all '+' sections for non-fiscal riders
- [ ] Cross-reference added dollar figures against CBO estimate delta
- [ ] Flag any section numbers not present in base version
"

if [[ -n "$OUTPUT" ]]; then
  mkdir -p "$(dirname "$OUTPUT")"
  echo "$FULL_REPORT" > "$OUTPUT"
  echo "Diff report saved: $OUTPUT"
else
  echo "$FULL_REPORT"
fi
