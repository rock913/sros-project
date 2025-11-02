#!/bin/bash

# ==============================================================================
# Full End-to-End Test Script for the LangGraph Research Agent
#
# This script automates the process of testing the research agent by:
# 1.  Ensuring an assistant for the research graph exists (creating if not).
# 2.  Creating a new conversation thread.
# 3.  Starting a research run on a specified topic.
# 4.  Polling for the run's completion.
# 5.  Fetching and displaying the final report.
#
# Usage:
#   ./scripts/test_research_agent.sh
#
# ==============================================================================

# --- Configuration ---
# Use environment variables with defaults for flexibility
API_URL="${API_URL:-http://localhost:8121}"
# The ID of the graph as defined in langgraph.json
GRAPH_ID="${GRAPH_ID:-agent}"
# The research topic you want the agent to investigate
RESEARCH_TOPIC="${RESEARCH_TOPIC:-What are the latest advancements in Large Language Models for code generation?}"

# --- Script setup ---
# Exit immediately if a command exits with a non-zero status.
set -e
# Ensure required commands are available
command -v curl >/dev/null 2>&1 || { echo >&2 "I require curl but it's not installed. Aborting."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo >&2 "I require jq but it's not installed. Aborting."; exit 1; }

# --- Helper Functions ---

# A simple logging function to make output clear
log() {
    echo "--- $(date '+%Y-%m-%d %H:%M:%S') --- $1"
}

# --- Log File Setup ---
LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/test_run_$(date '+%Y%m%d_%H%M%S').log"

# --- Main Execution Block ---
# The output of this entire block will be piped to 'tee'
{
    log "🚀 Starting Research Agent Test"
    log "API Server URL: ${API_URL}"
    log "Research Topic: ${RESEARCH_TOPIC}"
    log "Full log will be saved to: ${LOG_FILE}"

    # --- Step 1: Find or Create the Assistant ---

    log "🔍 Step 1: Searching for an existing assistant for graph_id='${GRAPH_ID}'..."

    ASSISTANT_ID=$(curl -s -X POST "${API_URL}/assistants/search" \
        -H "Content-Type: application/json" \
        -d '{
          "graph_id": "'"${GRAPH_ID}"'"
        }' | jq -r '.[0].assistant_id // empty')

    if [ -z "$ASSISTANT_ID" ]; then
        log " Assistant not found. Creating a new one..."
        ASSISTANT_RESPONSE=$(curl -s -X POST "${API_URL}/assistants" \
            -H "Content-Type: application/json" \
            -d '{
              "graph_id": "'"${GRAPH_ID}"'",
              "config": { "metadata": { "name": "My Research Agent" } }
            }')
        ASSISTANT_ID=$(echo "$ASSISTANT_RESPONSE" | jq -r '.assistant_id')
        log "✅ Assistant created successfully."
    else
        log "✅ Found existing assistant."
    fi

    log "Assistant ID: ${ASSISTANT_ID}"

    # --- Step 2: Create a New Thread ---

    log "🧵 Step 2: Creating a new conversation thread..."
    THREAD_RESPONSE=$(curl -s -X POST "${API_URL}/threads" -H "Content-Type: application/json" -d '{}')
    THREAD_ID=$(echo "$THREAD_RESPONSE" | jq -r '.thread_id')
    log "✅ Thread created successfully."
    log "Thread ID: ${THREAD_ID}"

    # --- Step 3: Start the Run ---

    log "🏃 Step 3: Starting a new run in the thread..."
    RUN_RESPONSE=$(curl -s -X POST "${API_URL}/threads/${THREAD_ID}/runs" \
        -H "Content-Type: application/json" \
        -d '{
          "assistant_id": "'"${ASSISTANT_ID}"'",
          "input": {
            "messages": [
              {
                "role": "user",
                "content": "'"${RESEARCH_TOPIC}"'"
              }
            ]
          }
        }')
    RUN_ID=$(echo "$RUN_RESPONSE" | jq -r '.run_id')
    log "✅ Run started successfully."
    log "Run ID: ${RUN_ID}"

    # --- Step 4: Poll for Completion ---

    log "⏳ Step 4: Waiting for the run to complete. This may take a few minutes..."

    while true; do
        STATE_RESPONSE=$(curl -s "${API_URL}/threads/${THREAD_ID}/state")
        STATUS=$(echo "$STATE_RESPONSE" | jq -r '.status')
        NEXT_NODE=$(echo "$STATE_RESPONSE" | jq -r '.next[0] // "None"')
        
        log " Current Status: ${STATUS} | Next Node: ${NEXT_NODE}"
        
        if [ "$STATUS" != "busy" ]; then
            break
        fi
        sleep 5 # Wait for 5 seconds before checking again
    done

    log "🏁 Run finished with status: ${STATUS}"

    # --- Step 5: Fetch and Display the Final Report ---

    log "📄 Step 5: Fetching the final report..."
    FINAL_REPORT=$(curl -s "${API_URL}/threads/${THREAD_ID}/state" | jq -r '.values.report')

    echo -e "\n\n--- FINAL RESEARCH REPORT ---\n"
    echo "$FINAL_REPORT"
    echo -e "\n--- END OF REPORT ---\n"

    log "✅ Test script completed."

} | tee "$LOG_FILE"