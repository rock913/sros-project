#!/bin/bash

# End-to-End test script for the Auto-Researcher agent using curl.
#
# This script sends a research topic to the agent's streaming API endpoint,
# prints the event stream, and saves the full output to a log file.

# --- Configuration ---
HOST="localhost"
PORT=8121 # Default port from docker-compose-dev.yml
ENDPOINT="/agent/stream"
URL="http://${HOST}:${PORT}${ENDPOINT}"

# --- Log File Setup ---
# The script is in backend/examples, so logs should go ../../logs
LOG_DIR="../../logs"
# Create logs directory if it doesn't exist
mkdir -p $LOG_DIR
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${LOG_DIR}/e2e_test_${TIMESTAMP}.log"


# --- Input Validation ---
if [ -z "$1" ]; then
  echo "Usage: $0 \"<research_topic>\""
  echo "Example: $0 \"The impact of AI on climate change\""
  exit 1
fi

# --- Main execution block ---
# Redirect all output from this block to both console and the log file using tee.
{

  RESEARCH_TOPIC="$1"

  # --- Request Body ---
  # The input to the graph is a dictionary with a "messages" key.
  JSON_PAYLOAD=$(cat <<EOF
{
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "${RESEARCH_TOPIC}"
      }
    ]
  }
}
EOF
)

  # --- Execution ---

  echo "================================================="
  echo "  Auto-Researcher E2E Test (curl version)"
  echo "================================================="
  echo
  echo "[1/4] Preparing to send request..."
  echo "  > URL: ${URL}"
  echo "  > Topic: ${RESEARCH_TOPIC}"
  echo

  echo "[2/4] Checking for dependencies (jq)..."
  # Check if jq is installed for pretty-printing
  if ! command -v jq &> /dev/null; then
      echo "  > [INFO] 'jq' command not found. JSON output will not be pretty-printed."
      echo "         To install jq, run: sudo apt-get install jq (or equivalent for your OS)"
      JQ_CMD="cat"
  else
      echo "  > [OK] 'jq' is installed."
      JQ_CMD="jq ."
  fi
  echo

  echo "[3/4] Sending request and streaming response..."
  echo "-------------------------------------------------"
  
  START_TIME=$(date +%s)
  echo "  > Agent process started at: $(date)"

  # Use curl to send the request and process the stream.
  # -X POST: Specifies a POST request.
  # -H "Content-Type: application/json": Sets the content type header.
  # -H "Accept: text/event-stream": Indicates we want a streaming response.
  # -d "$JSON_PAYLOAD": Provides the JSON data as the request body.
  # --no-buffer: Disables buffering of the output stream, so we see events as they arrive.
  # The output is piped to a while loop to process each line of the stream.
  curl -s -X POST \
       -H "Content-Type: application/json" \
       -H "Accept: text/event-stream" \
       -d "$JSON_PAYLOAD" \
       --no-buffer \
       "$URL" | while IFS= read -r line; do
    # LangServe SSE streams prefix data chunks with "data: ".
    # We check for this prefix, remove it, and then parse the JSON.
    if [[ $line == data:* ]]; then
      # Remove "data: " prefix
      json_data=${line#data: }
      echo "--- Agent Chunk Received ---"
      echo "$json_data" | $JQ_CMD
    fi
  done
  
  END_TIME=$(date +%s)
  DURATION=$((END_TIME - START_TIME))

  echo
  echo "-------------------------------------------------"
  echo "[4/4] Stream finished. Test complete."
  echo "  > Agent process finished at: $(date)"
  echo "  > Total execution time: ${DURATION} seconds."
  echo "================================================="
  echo
  echo "Log file saved to: $(realpath $LOG_FILE)"

} | tee "${LOG_FILE}"