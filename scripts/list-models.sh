#!/bin/bash
set -e

if [ -z "$GEMINI_API_KEY" ]; then
  echo "Error: GEMINI_API_KEY environment variable is not set." >&2
  exit 1
fi

LOG_DIR="logs"
mkdir -p "$LOG_DIR"

OUTPUT_FILE="$LOG_DIR/models.log"

echo "Fetching models from Google AI..."
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" -o "$OUTPUT_FILE"

echo "Successfully fetched models and saved to $OUTPUT_FILE"