"use strict";
// vscode-extension/src/mcp_helper.ts
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildDockerCommand = buildDockerCommand;
/**
 * Helper functions for MCP client infrastructure commands
 */
/**
 * Build docker exec command for MCP server with proper environment
 */
function buildDockerCommand(containerName) {
    // Ensure PYTHONPATH is set for container module imports
    // Use -u for unbuffered output to ensure "ready" signals are not delayed
    return [
        'docker', 'exec', '-i',
        '-e', 'PYTHONPATH=/deps/backend/src:/deps/backend',
        containerName,
        'python', '-u', '-m', 'agent.infrastructure.mcp.entrypoint'
    ];
}
//# sourceMappingURL=mcp_helper.js.map