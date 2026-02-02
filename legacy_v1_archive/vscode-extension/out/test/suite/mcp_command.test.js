"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// vscode-extension/src/test/suite/mcp_command.test.ts
const assert = require("assert");
const mcp_helper_1 = require("../../mcp_helper");
suite('MCP Infrastructure Test Suite', () => {
    test('Docker command includes PYTHONPATH', () => {
        const cmdArgs = (0, mcp_helper_1.buildDockerCommand)('langgraph-api');
        const cmd = cmdArgs.join(' ');
        // Assertion (The Contract)
        assert.ok(cmd.includes('PYTHONPATH=/deps/backend/src:/deps/backend'), 'Must inject PYTHONPATH for container modules');
        assert.ok(cmd.includes('python -m agent.infrastructure.mcp.entrypoint'), 'Must target correct entrypoint');
    });
});
//# sourceMappingURL=mcp_command.test.js.map