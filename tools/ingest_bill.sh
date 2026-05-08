#!/usr/bin/env bash
# Downloads a bill from congress.gov and places it in the correct versioned directory.
#
# Usage A — bill ID (preferred, used by poll_bills.py and bill_monitor.yml):
#   ./tools/ingest_bill.sh --id 119hr8007
#   ./tools/ingest_bill.sh --id 119hr8007 --version introduced
#
# Usage B — explicit URL (original behaviour, kept for manual ingestion):
#   ./tools/ingest_bill.sh <congress_bill_url> <bill_slug> <version_label>
#   ./tools/ingest_bill.sh https://www.congress.gov/... OBBBA_HR1 senate_amendments
#
# Bill ID format: <congress><type><number>  e.g. 119hr8007, 119s142, 119hjres1
#   congress: 3-digit or 2-digit number
#   type:     hr | s | hjres | sjres | hconres | sconres | hres | sres
#   number:   bill number (no leading zeros needed)
#
# The script constructs the congress.gov XML URL automatically from the bill ID.
# Downloaded XML is saved as-is; a README.md stub is created if one doesn't exist.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BILLS_DIR="$REPO_ROOT/data/bills"

# ── Parse arguments ───────────────────────────────────────────────────────────

BILL_ID=""
VERSION_LABEL="introduced"
URL=""
BILL_SLUG=""

if [[ "${1:-}" == "--id" ]]; then
  BILL_ID="${2:-}"
  if [[ -z "$BILL_ID" ]]; then
    echo "Error: --id requires a bill ID argument (e.g. 119hr8007)" >&2
    exit 1
  fi
  # Optional --version flag
  if [[ "${3:-}" == "--version" ]]; then
    VERSION_LABEL="${4:-introduced}"
  fi
else
  # Legacy positional mode
  URL="${1:-}"
  BILL_SLUG="${2:-}"
  VERSION_LABEL="${3:-introduced}"
  if [[ -z "$URL" || -z "$BILL_SLUG" ]]; then
    echo "Usage (bill ID):  $0 --id <congress><type><number> [--version <label>]"
    echo "Usage (URL):      $0 <congress_bill_url> <bill_slug> <version_label>"
    echo ""
    echo "Examples:"
    echo "  $0 --id 119hr8007"
    echo "  $0 --id 119hr8007 --version enrolled"
    echo "  $0 https://www.congress.gov/... OBBBA_HR1 senate_amendments"
    exit 1
  fi
fi

# ── Resolve bill ID → URL + slug ──────────────────────────────────────────────

if [[ -n "$BILL_ID" ]]; then
  # Parse: congress=digits, type=letters, number=digits
  if [[ "$BILL_ID" =~ ^([0-9]+)([a-zA-Z]+)([0-9]+)$ ]]; then
    CONGRESS="${BASH_REMATCH[1]}"
    TYPE_RAW="${BASH_REMATCH[2]}"    # hr, s, hjres, etc.
    NUMBER="${BASH_REMATCH[3]}"
  else
    echo "Error: cannot parse bill ID '$BILL_ID'. Expected format: 119hr8007" >&2
    exit 1
  fi

  # congress.gov XML URL pattern (introduced = "ih", enrolled = "enr", etc.)
  declare -A VERSION_SUFFIX=(
    ["introduced"]="ih"
    ["enrolled"]="enr"
    ["house_passed"]="eh"
    ["senate_passed"]="es"
    ["reported"]="rh"
  )
  SUFFIX="${VERSION_SUFFIX[$VERSION_LABEL]:-ih}"

  TYPE_LOWER="${TYPE_RAW,,}"  # lowercase
  URL="https://www.congress.gov/${CONGRESS}/bills/${TYPE_LOWER}${NUMBER}/BILLS-${CONGRESS}${TYPE_LOWER}${NUMBER}${SUFFIX}.xml"

  # Slug: UPPERCASE type + number (e.g. SILVER_HR8007, HR1)
  TYPE_UPPER="${TYPE_RAW^^}"
  # Friendly name: just type+number, no congress prefix
  BILL_SLUG="${TYPE_UPPER}${NUMBER}"
fi

# ── Ingest ────────────────────────────────────────────────────────────────────

TARGET_DIR="$BILLS_DIR/$BILL_SLUG"
TARGET_FILE="$TARGET_DIR/${VERSION_LABEL}.xml"

mkdir -p "$TARGET_DIR"

echo "Fetching: $URL" >&2
HTTP_CODE=$(curl -fsSL -w "%{http_code}" -o "$TARGET_FILE" "$URL" 2>&1 || true)

# curl exits non-zero on 404 etc. — check file size
if [[ ! -s "$TARGET_FILE" ]]; then
  echo "Error: download failed or empty response from $URL" >&2
  rm -f "$TARGET_FILE"
  exit 1
fi

DATESTAMP=$(date +%y%m%d)

# Create README stub if not present
README="$TARGET_DIR/README.md"
if [[ ! -f "$README" ]]; then
  cat > "$README" << EOF
# ${BILL_SLUG}
**Ingested:** $DATESTAMP
**Source:** $URL

## Version History
| File | Version | Date | Notes |
|---|---|---|---|
| \`${VERSION_LABEL}.xml\` | ${VERSION_LABEL} | $DATESTAMP | Auto-ingested |

## Related Audits
<!-- add audit IDs here after analysis -->
EOF
  echo "Created: $README" >&2
else
  # Append version entry to existing README version history
  sed -i "s/## Version History/## Version History\n| \`${VERSION_LABEL}.xml\` | ${VERSION_LABEL} | $DATESTAMP | Auto-ingested |/" "$README" 2>/dev/null || true
fi

echo "Saved: $TARGET_FILE"
echo "bill_slug=$BILL_SLUG"
echo "version=$VERSION_LABEL"
echo "source=$URL"
