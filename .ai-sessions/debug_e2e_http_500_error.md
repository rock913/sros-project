# Debugging Snapshot Record: E2E HTTP 500 Error

This document logs the debugging process for fixing the `HTTP 500` error encountered during the enhanced E2E test. It follows the snapshot-driven methodology outlined in `GEMINI.md`.

---

**Debugging Theme:** Fix `HTTP 500` error in the enhanced E2E test.

**Snapshot #1**
*   **Trigger**: `bash backend/examples/e2e_test_enhanced.sh "The future of personalized medicine"`
*   **Observation**: Test fails at step "[2/6] Pre-flight /agent/invoke status check" with an `HTTP 500` error.
*   **Log Analysis (`docker logs langgraph-api`)**:
    ```
    litellm.exceptions.NotFoundError: GeminiException - {
      "error": { "code": 404, "message": "models/gemini-1.5-flash is not found for API version v1beta..." }
    }
    ```
*   **Root Cause Analysis**: `litellm` cannot find the model `gemini-1.5-flash`.
*   **Hypothesis #1**: The default `generation_model` in `configuration.py` (`gemini/gemini-1.5-flash`) contains an incorrect prefix `gemini/`.
*   **Fix Attempt #1**: Remove the prefix, changing the model name to `gemini-1.5-flash`.
*   **Result**: **FAIL**. The same `HTTP 500` error occurred.

**Snapshot #2**
*   **Trigger**: Re-running the E2E test after Fix Attempt #1.
*   **Observation**: Same `HTTP 500` error.
*   **Log Analysis**: The error message is identical to Snapshot #1.
*   **Conclusion**: Hypothesis #1 is incorrect. The issue is not just the prefix.
*   **Hypothesis #2**: The model `gemini-1.5-flash` is incompatible with the `v1beta` API used by `litellm` or is unavailable in the current region.
*   **Fix Attempt #2**: Change the model to a known stable model, `gemini-pro`, for testing.
*   **Result**: **Operation cancelled by user**.

**Snapshot #3**
*   **User-directed Action**: Try a hypothetical model name `gemini-2.5-flash`.
*   **Hypothesis #3**: `gemini-2.5-flash` is a valid and available model.
*   **Fix Attempt #3**: Change `generation_model` to `gemini-2.5-flash`.
*   **Expected Result**: High probability of failure, as `gemini-2.5-flash` is likely not a real model. This will confirm that the core issue is finding a *valid* model name.
*   **Actual Result**: *(Pending test execution)*
