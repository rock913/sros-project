# Standardized Prompt Snippets

This file contains a collection of standardized prompt snippets to ensure consistent and effective collaboration with the AI assistant. Using these templates helps the AI understand the context and adhere to our project's workflow.

## General

### Constitutional Opening

*Always start a new development session with this prompt.*

> "Hello Gemini. In this session, we will strictly follow the development workflow defined in `.ai-conventions/01_workflow.md`. Please ensure all your suggestions and code generations adhere to this document."

## New Feature Development (DTDD Workflow)

### Step 1: Create the Code Contract

> "Based on our DTDD workflow, I need to start a new module named `[Module Name]`. Its core responsibility is `[Module Description]`. Please start by creating its code contract file. Use a [TypeScript interface / Python abstract base class] and provide detailed documentation for each method, including parameters, return values, and all possible error scenarios."

### Step 2: Write the Test Suite

> "Based on the `[Contract File Name]` we just created, please write a complete unit test suite using `[Jest/Pytest]`. The tests should cover all success and failure cases documented in the contract. The test suite should fail initially."

### Step 3: Implement the Code

> "Now, please implement the `[Interface/Protocol Name]` in `[Implementation File Name]`. Your only goal is to make all tests in `[Test File Name]` pass."

## Refactoring Legacy Code

### Step 1: Generate Documentation (Archaeology)

> "(Select the legacy code) @selection Please analyze this code and generate detailed `[JSDoc/PyDoc]` comments for all public functions and classes to clarify their current functionality."

### Step 2: Create Characterization Tests

> "Based on the documentation you just generated for `[File Name]`, write a comprehensive suite of characterization tests. The goal is to lock down the current behavior, including any quirks or potential bugs, to create a reliable safety net."

### Step 3: Perform the Refactor

> "With the test safety net in place for `[File Name]`, please refactor the code to `[Describe the desired change, e.g., use async/await instead of callbacks]`. You must ensure that all tests pass throughout the refactoring process."
