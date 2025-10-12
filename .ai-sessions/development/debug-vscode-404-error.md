# Debug Session: VS Code Extension 404 Error

**Date:** 2025-10-12

**Goal:** Debug and fix the issue where the "Asset Library" and "Manuscript" views in the VS Code extension are empty.

## 1. Initial Observation

The user reported that after activating the `auto-researcher` extension, the UI panels for the asset library and manuscript remain empty.

The VS Code developer console shows the following critical error:

```
Error fetching agent state: AxiosError {message: 'Request failed with status code 404', name: 'AxiosError', code: 'ERR_BAD_REQUEST', ...}
```

This `404 Not Found` error indicates the extension is making an API call to an incorrect or non-existent endpoint.

## 2. Code Analysis

To diagnose this, I analyzed the relevant files from the frontend (VS Code extension) and backend (FastAPI server).

*   **VS Code Extension (`vscode-extension/src/api.ts`):** The `getAgentState` function is responsible for fetching data. It was making a `POST` request to `http://langgraph-api:8000/agent`.
*   **Backend (`backend/src/agent/app.py`):** The backend uses `langserve` to expose the agent graph. The `add_routes` function creates the API endpoints. The standard endpoint for invoking a graph is `/agent/invoke`, not `/agent`.

**Conclusion:** The root cause is a mismatch between the API endpoint called by the extension and the actual endpoint exposed by the backend.

## 3. Planned Fix

I will modify `vscode-extension/src/api.ts` to correct the endpoint URL.

*   **Change:** In the `getAgentState` function, update the `axios.post` call.
*   **From:** `${API_BASE_URL}/agent`
*   **To:** `${API_BASE_URL}/agent/invoke`

Additionally, the `langserve` endpoint expects the payload to be wrapped in an `input` object, and its response is wrapped in an `output` object. I will adjust the request payload and response handling accordingly.

## 4. Applying the Fix

**Status:** The fix has been applied to `vscode-extension/src/api.ts`.

## 5. Manual Verification

**Next Step:** The user will now manually test the fix.

1.  Reload the VS Code window running the `auto-researcher` extension.
2.  Check if the "Asset Library" and "Manuscript" views now populate with data.
3.  Confirm that the `404` error is no longer present in the developer console.