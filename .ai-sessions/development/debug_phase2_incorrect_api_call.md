# Debugging Phase 2: Incorrect API Call

## Problem

The VSCode extension is triggering a new research task upon activation, instead of displaying existing data. The goal of phase 2 is to only display previously generated data.

## Analysis

This section will document the analysis of the backend API and the VSCode extension code to identify the cause of the issue.

### Backend API Analysis

The backend's main endpoint `/agent/invoke` (exposed via `langserve.add_routes`) is designed to trigger a new research task when called. There was no dedicated read-only endpoint to fetch the state of a previous or existing research task.

### VSCode Extension Analysis

The `getAgentState` function in `vscode-extension/src/api.ts` was making a POST request to `/agent/invoke` with an empty payload. This action incorrectly initiated a new research process instead of just fetching existing data.

## Solution

1.  **Backend Modification (`database.py`):**
    *   Added a new function `get_all_documents()` to `backend/src/agent/database.py`.
    *   This function queries the database and returns all stored document records.

2.  **Backend Modification (`app.py`):**
    *   Added a new GET endpoint `/agent/state` to `backend/src/agent/app.py`.
    *   This endpoint uses `get_all_documents()` to retrieve all documents from the database.
    *   It then formats this data into a structure consistent with the `AgentOutput` model (specifically populating `literature_abstracts`) and returns it. This provides a read-only way to access existing research data.

3.  **Frontend Modification (`api.ts`):**
    *   Modified the `getAgentState` function in `vscode-extension/src/api.ts`.
    *   Changed the request from a `POST` to `/agent/invoke` to a `GET` request to the new `/agent/state` endpoint.
    *   Adjusted the response handling to process the data from the new endpoint correctly.
