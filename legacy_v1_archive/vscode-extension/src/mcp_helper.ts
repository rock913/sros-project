// vscode-extension/src/mcp_helper.ts

/**
 * Helper functions for MCP client infrastructure commands
 */

/**
 * Build docker exec command for MCP server with proper environment
 */
export function buildDockerCommand(containerName: string): string[] {
    // Ensure PYTHONPATH is set for container module imports
    // Use -u for unbuffered output to ensure "ready" signals are not delayed
    return [
        'docker', 'exec', '-i',
        '-e', 'PYTHONPATH=/deps/backend/src:/deps/backend',
        containerName,
        'python', '-u', '-m', 'agent.infrastructure.mcp.entrypoint'
    ];
}
