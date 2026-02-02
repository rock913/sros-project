#!/usr/bin/env bash
# Enhanced End-to-End streaming test for the Auto-Researcher agent.
# Adds: health check, HTTP status validation, retry, timeout, structured summary, basic assertions.
# Usage:
#   bash backend/examples/e2e_test_enhanced.sh "<research topic>" [--host localhost] [--port 8121] [--timeout 900]
# Examples:
#   bash backend/examples/e2e_test_enhanced.sh "recent development on neuro ai"
#   bash backend/examples/e2e_test_enhanced.sh "ai in climate change" --timeout 600
#
# Exit codes:
#   0 success (report field observed)
#   2 invalid usage
#   3 health check failed / server not ready
#   4 HTTP request failed / non-200
#   5 stream ended without expected keys
#   6 timeout
#
set -euo pipefail

TOPIC=""
HOST="localhost"
PORT=8121
TIMEOUT=900   # seconds overall budget
RETRY=30       # max health retries
SLEEP=2
EXPECTED_KEYS=(run_id generate_initial_queries execute_searches reflection_and_refinement retrieve_and_synthesize_report)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) HOST="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    -h|--help) sed -n '1,60p' "$0"; exit 0;;
    *) if [[ -z "$TOPIC" ]]; then TOPIC="$1"; shift; else echo "[ERR] Unexpected arg: $1"; exit 2; fi;;
  esac
done

if [[ -z "$TOPIC" ]]; then
  echo "Usage: $0 \"<research topic>\" [--host HOST] [--port PORT] [--timeout SEC]" >&2
  exit 2
fi

BASE="http://${HOST}:${PORT}"
STREAM_URL="${BASE}/agent/stream"
INVOKE_URL="${BASE}/agent/invoke"
HEALTH_URL="${BASE}/ok"
START_TS=$(date +%s)

LOG_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo .)/logs"
mkdir -p "$LOG_DIR"
STAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${LOG_DIR}/e2e_test_enhanced_${STAMP}.log"
TMP_RAW="$(mktemp)"
trap 'rm -f "$TMP_RAW"' EXIT

# --- Functions ---
log(){ echo -e "$*" | tee -a "$LOG_FILE"; }
now(){ date '+%Y-%m-%d %H:%M:%S'; }
remaining(){ local now_ts=$(date +%s); echo $(( TIMEOUT - (now_ts - START_TS) )); }

log "================================================="
log " Enhanced Auto-Researcher E2E Test"
log "================================================="
log "Start: $(now)"
log "Topic: $TOPIC"
log "Host : $HOST  Port: $PORT" 
log "Timeout (s): $TIMEOUT"
log "Log file: $LOG_FILE"

# --- Step 1: Health check with retry ---
log "[1/6] Health check ${HEALTH_URL} (up to $RETRY retries) ..."
ATTEMPT=0
until curl -fsS "${HEALTH_URL}" >/dev/null 2>&1; do
  ATTEMPT=$((ATTEMPT+1))
  if (( ATTEMPT >= RETRY )); then
    log "[FAIL] Health check failed after $ATTEMPT attempts."
    exit 3
  fi
  if (( $(remaining) <= 0 )); then
    log "[FAIL] Timeout waiting for health endpoint."; exit 6
  fi
  sleep "$SLEEP"
  log "  retry $ATTEMPT ..."
done
log "  Health OK"

# --- Step 2: Pre-flight invoke (non-stream) to detect immediate 4xx/5xx quickly ---
log "[2/6] Pre-flight /agent/invoke status check ..."
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' \
  -d '{"input":{"messages":[{"role":"user","content":"ping"}]}}' "$INVOKE_URL")
if [[ "$HTTP_CODE" != "200" ]]; then
  log "[FAIL] /agent/invoke returned HTTP $HTTP_CODE"; exit 4
fi
log "  Invoke OK (200)"

# --- Step 3: Streaming test ---
log "[3/6] Streaming from $STREAM_URL ..."
JSON_PAYLOAD=$(cat <<EOF
{"input":{"messages":[{"role":"user","content":"${TOPIC}"}]}}
EOF
)

# We'll capture all SSE lines; parse keys; enforce total timeout using (timeout) utility if present
CURL_BIN="curl"
TIMEOUT_CMD=""
if command -v timeout >/dev/null 2>&1; then TIMEOUT_CMD="timeout $(remaining)"; fi

$TIMEOUT_CMD $CURL_BIN -s -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: text/event-stream' \
  --no-buffer -d "$JSON_PAYLOAD" "$STREAM_URL" | tee "$TMP_RAW" | while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    if [[ $line == data:* ]]; then
      payload=${line#data: }
      # print truncated for readability
      show=$(echo "$payload" | sed 's/\\n/ /g' | head -c 220)
      log "  [CHUNK] ${show}"
    fi
  done
STREAM_RC=${PIPESTATUS[0]}
if (( STREAM_RC != 0 )); then
  log "[FAIL] curl stream exited with code $STREAM_RC"; exit 4
fi

# --- Step 4: Post-process captured stream to extract JSON objects & keys ---
log "[4/6] Parsing stream for expected keys ..."
FOUND_KEYS=()
if command -v jq >/dev/null 2>&1; then
  # Extract lines beginning with data:, strip prefix, attempt to parse and collect top-level keys
  while IFS= read -r obj; do
    klist=$(echo "$obj" | jq -r 'keys_unsorted[]' 2>/dev/null || true)
    while IFS= read -r k; do
      [[ -z "$k" ]] && continue
      FOUND_KEYS+=("$k")
    done <<< "$klist"
  done < <(grep '^data:' "$TMP_RAW" | sed 's/^data: //')
else
  log "  jq not installed; skipping deep key parse"
  # Fallback: simple grep of keywords
  for k in "${EXPECTED_KEYS[@]}"; do
    if grep -q "$k" "$TMP_RAW"; then FOUND_KEYS+=("$k"); fi
  done
fi

unique_keys=$(printf '%s\n' "${FOUND_KEYS[@]}" | sort -u)
log "  Keys observed (unique):\n$(printf '   - %s\n' $unique_keys)" || true

# --- Step 5: Assertions ---
log "[5/6] Validating expectations ..."
MISSING=()
for k in "${EXPECTED_KEYS[@]}"; do
  if ! printf '%s\n' "$unique_keys" | grep -Fxq "$k"; then
    MISSING+=("$k")
  fi
done
if (( ${#MISSING[@]} )); then
  log "  [WARN] Missing expected keys: ${MISSING[*]}"
  # Only fatal if final 'report' missing
  if printf '%s\n' "${MISSING[@]}" | grep -q '^report$'; then
    log "  [FAIL] Final report not produced."; exit 5
  fi
else
  log "  All expected keys present." 
fi

# Extract final report (best-effort)
REPORT_FILE="${LOG_FILE%.log}_report.txt"
if command -v jq >/dev/null 2>&1; then
  grep '^data:' "$TMP_RAW" | sed 's/^data: //' | jq -r 'select(.retrieve_and_synthesize_report.report!=null) | .retrieve_and_synthesize_report.report' | tail -n1 > "$REPORT_FILE" || true
else
  grep -o '"report": *"[^"]\{1,400\}' "$TMP_RAW" | sed 's/^.*"report": *"//' | tail -n1 > "$REPORT_FILE" || true
fi
if [[ -s "$REPORT_FILE" ]]; then
  log "  Saved final report to: $REPORT_FILE"
else
  log "  (No report extracted)"
fi

# --- Step 6: Summary ---
END_TS=$(date +%s)
DUR=$((END_TS-START_TS))
log "[6/6] Done. Duration: ${DUR}s"
log "================================================="

# Success criterion: have a report file with some content
if [[ -s "$REPORT_FILE" ]]; then
  exit 0
else
  exit 5
fi
