// vscode-extension/src/test/suite/mcp_command.test.ts
import * as assert from 'assert';
import { buildDockerCommand } from '../../mcp_helper';

suite('MCP Infrastructure Test Suite', () => {
    test('Docker command includes PYTHONPATH', () => {
        const cmdArgs = buildDockerCommand('langgraph-api');
        const cmd = cmdArgs.join(' ');

        // Assertion (The Contract)
        assert.ok(cmd.includes('PYTHONPATH=/deps/backend/src:/deps/backend'), 'Must inject PYTHONPATH for container modules');
        assert.ok(cmd.includes('python -m agent.infrastructure.mcp.entrypoint'), 'Must target correct entrypoint');
    });
});