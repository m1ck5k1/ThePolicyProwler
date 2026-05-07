#!/usr/bin/env bash
# Downloads a bill from congress.gov and places it in the correct versioned directory.
# Usage: ./tools/ingest_bill.sh <congress_bill_url> <bill_slug> <version_label>
# Example: ./tools/ingest_bill.sh https://www.congress.gov/... OBBBA_HR1 senate_amendments

set -euo pipefail

BILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)/data/bills"

URL="${1:-}"
BILL_SLUG="${2:-}"
VERSION_LABEL="${3:-}"

if [[ -z "$URL" || -z "$BILL_SLUG" || -z "$VERSION_LABEL" ]]; then
  echo "Usage: $0 <congress_bill_url> <bill_slug> <version_label>"
  echo "  bill_slug:     directory name under data/bills/ (e.g. OBBBA_HR1)"
  echo "  version_label: file name without extension (e.g. house_v1_excerpt, senate_amendments, final_enrolled)"
  exit 1
fi

TARGET_DIR="$BILLS_DIR/$BILL_SLUG"
TARGET_FILE="$TARGET_DIR/${VERSION_LABEL}.md"

mkdir -p "$TARGET_DIR"

echo "Fetching: $URL"
RAW=$(curl -fsSL "$URL")

# Strip HTML if response is HTML (congress.gov text endpoint returns HTML)
if echo "$RAW" | grep -q "<html"; then
  if command -v lynx &>/dev/null; then
    TEXT=$(echo "$RAW" | lynx -stdin -dump -nolist 2>/dev/null)
  elif command -v w3m &>/dev/null; then
    TEXT=$(echo "$RAW" | w3m -T text/html -dump 2>/dev/null)
  else
    echo "Warning: HTML detected but no text browser (lynx/w3m) found. Saving raw HTML."
    TEXT="$RAW"
  fi
else
  TEXT="$RAW"
fi

# Write with metadata header
DATESTAMP=$(date +%y%m%d)
cat > "$TARGET_FILE" << HEADER
# $BILL_SLUG — $VERSION_LABEL
**Ingested:** $DATESTAMP
**Source:** $URL

---

$TEXT
HEADER

echo "Saved: $TARGET_FILE"
echo "Next: review the file, trim to relevant sections, and update data/bills/$BILL_SLUG/README.md"
