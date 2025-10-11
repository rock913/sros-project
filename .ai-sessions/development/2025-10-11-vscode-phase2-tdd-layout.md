# VS Code Extension Phase 2 (TDD): UI Layout & Testing - 2025-10-11

## Session Summary

This session adopts a Test-Driven Development (TDD) approach for building the Phase 2 UI skeleton. Instead of implementing features directly, we will first enhance the testing infrastructure with `sinon` for mocking and stubbing. Each feature will be developed by first writing a failing test that defines the desired behavior, and then writing the implementation code to make the test pass.

## Previous Session
- See `.ai-sessions/development/2025-10-11-vscode-extension-setup.md`

## User Directives for this Session
1.  Re-evaluate the development plan to incorporate enhanced testing with `sinon`.
2.  Adopt a strict Test-Driven Development (TDD) workflow.
3.  Implement the three-panel layout, but with a test-first approach.

## Development Plan

### Step 1: Create New Session File [DONE]
- Create this session file to track the TDD-based development of the Phase 2 UI layout.

### Step 2: Enhance Test Infrastructure with `sinon` [DONE]
- **Goal:** Set up `sinon` to enable mocking of VS Code APIs and our internal API client.
- **Summary of Actions:**
    1.  Installed `sinon` and `@types/sinon`.
    2.  Refactored `src/test/suite/extension.test.ts` to use `sinon` stubs for API calls (`api.checkHealth`) and spies for VS Code notifications (`vscode.window.showInformationMessage`).
    3.  Added explicit `mocha` imports (`beforeEach`, `afterEach`, etc.) to fix a `ReferenceError` in the test runner.
    4.  Successfully ran the new test suite, confirming the TDD environment is now robust and ready.

### Step 3: Implement Three-Panel Layout (Test-Driven)
- **Goal:** Create the three-panel layout.
- **Test First [DONE]:** Added a new test case in `extension.test.ts` that asserts the view and command registration calls are made upon activation. Confirmed that this test fails as expected (`AssertionError: assetLibrary should be registered`), completing the "Red" phase of the TDD cycle.
- **Implementation:** Modify `package.json` and `extension.ts` to make the test pass.

### Step 4: Populate Views with Static Content (Test-Driven)
- **Goal:** Verify the layout by filling views with placeholder content.
- **Test First:**
    - Write unit tests for the `TreeDataProvider` to ensure it returns the correct mock data.
    - Write a test to assert that the `WebviewPanel`'s `html` property is set to the expected placeholder HTML.
- **Implementation:** Implement the `TreeDataProvider` and the webview content generation to make the tests pass.

### Step 5: Connect Control Panel to Backend API (Test-Driven)
- **Goal:** Fetch and display agent status from the backend in the AI Control Panel.
- **Test First:** Write a test that uses `sinon` to stub the `api.ts` module. Assert that the `WebviewPanel`'s HTML is correctly updated based on mocked API responses (both success and error cases).
- **Implementation:** Write the necessary API calling and view update logic to make the tests pass.
