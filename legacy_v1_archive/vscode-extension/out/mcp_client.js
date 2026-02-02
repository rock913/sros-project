"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.McpClient = void 0;
exports.getMcpClient = getMcpClient;
exports.stopMcpClient = stopMcpClient;
const child_process_1 = require("child_process");
const vscode = require("vscode");
const mcp_helper_1 = require("./mcp_helper");
/**
 * MCP Client for VS Code Extension
 * Connects to backend MCP server via stdio stream
 */
class McpClient {
    // @ts-ignore - intentionally unused parameter for future extension context access
    constructor(_context) {
        this._context = _context;
        this.onMessageCallbacks = [];
        this.onErrorCallbacks = [];
        this.messageIdCounter = 1;
        this.outputChannel = vscode.window.createOutputChannel('Auto-Researcher MCP');
    }
    /**
     * Start MCP server process
     */
    async start() {
        return new Promise((resolve, reject) => {
            try {
                // Find docker container name (assume 'langgraph-api' based on docker-compose)
                const containerName = 'langgraph-api';
                // Start MCP server via docker exec with proper PYTHONPATH
                const dockerArgs = (0, mcp_helper_1.buildDockerCommand)(containerName);
                this.process = (0, child_process_1.spawn)(dockerArgs[0], dockerArgs.slice(1), {
                    stdio: ['pipe', 'pipe', 'pipe']
                });
                // Add error listener for immediate rejection on startup errors
                const errorListener = (errorData) => {
                    const errorOutput = errorData.toString().trim();
                    if (errorOutput) {
                        this.outputChannel.appendLine(`[STARTUP ERROR] ${errorOutput}`);
                        clearTimeout(timeout);
                        this.process.stderr.removeListener('data', errorListener);
                        reject(new Error(`MCP server startup failed: ${errorOutput}`));
                    }
                };
                this.process.stderr.on('data', errorListener);
                this.setupEventHandlers();
                this.initializeMcpConnection();
                // Wait for ready message or timeout
                const timeout = setTimeout(() => {
                    reject(new Error('MCP server startup timeout - check server logs for errors'));
                }, 15000); // Increased timeout
                // Listen for ready indication (more flexible detection)
                const readyListener = (data) => {
                    const output = data.toString().toLowerCase();
                    this.outputChannel.appendLine(`[STARTUP] ${output.trim()}`);
                    // More flexible detection - any of these indicate server is ready
                    if (output.includes('ready') ||
                        output.includes('listening') ||
                        output.includes('server started') ||
                        output.includes('mcp') && (output.includes('start') || output.includes('init'))) {
                        this.outputChannel.appendLine('✓ MCP server ready detected');
                        clearTimeout(timeout);
                        this.process.stdout.removeListener('data', readyListener);
                        resolve();
                    }
                };
                this.process.stdout.on('data', readyListener);
            }
            catch (error) {
                reject(new Error(`Failed to start MCP server: ${error}`));
            }
        });
    }
    /**
     * Stop MCP server process
     */
    async stop() {
        if (this.process) {
            this.process.kill();
            this.process = null;
        }
    }
    /**
     * Send MCP request and return response
     */
    async sendRequest(method, params) {
        return new Promise((resolve, reject) => {
            const id = this.messageIdCounter++;
            const request = {
                jsonrpc: '2.0',
                id,
                method,
                params: params || {}
            };
            const requestJson = JSON.stringify(request) + '\n';
            this.outputChannel.appendLine(`→ Sending: ${method} (${id})`);
            // Send request to stdin
            this.process.stdin.write(requestJson, (err) => {
                if (err) {
                    reject(new Error(`Failed to send request: ${err}`));
                }
            });
            // Listen for response
            const responseListener = (data) => {
                try {
                    const response = JSON.parse(data.toString());
                    if (response.id === id) {
                        this.process.stdout.removeListener('data', responseListener);
                        if (response.error) {
                            reject(new Error(response.error.message));
                        }
                        else {
                            resolve(response.result);
                        }
                    }
                }
                catch (e) {
                    // Not a valid JSON response, continue listening
                }
            };
            this.process.stdout.on('data', responseListener);
        });
    }
    /**
     * Register callback for messages from MCP server
     */
    onMessage(callback) {
        this.onMessageCallbacks.push(callback);
    }
    /**
     * Register callback for errors from MCP server
     */
    onError(callback) {
        this.onErrorCallbacks.push(callback);
    }
    /**
     * Call MCP tool
     */
    async callTool(toolName, args) {
        const response = await this.sendRequest('tools/call', {
            name: toolName,
            arguments: args
        });
        return response;
    }
    /**
     * Start research session (convenience method)
     */
    async startResearch(topic) {
        this.outputChannel.appendLine(`🚀 Starting research on: ${topic}`);
        try {
            // @ts-ignore - intentionally unused for future streaming event handling (Phase 5.2)
            const _events = [];
            // Use streaming version when available
            // For now, use tool call
            // @ts-ignore - intentionally unused result for now, will use in future streaming
            const _result = await this.callTool('orchestrator', { topic });
            // Handle streaming events if available
            // This will be enhanced in Phase 5.2 when we integrate real LangGraph streaming
            vscode.window.showInformationMessage(`Research started: ${topic}`);
            this.outputChannel.appendLine(`✓ Research orchestration initiated`);
        }
        catch (error) {
            const errorMsg = `Failed to start research: ${error}`;
            vscode.window.showErrorMessage(errorMsg);
            this.outputChannel.appendLine(`✗ ${errorMsg}`);
        }
    }
    setupEventHandlers() {
        if (!this.process)
            return;
        this.process.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                this.outputChannel.appendLine(`← MCP: ${output}`);
                try {
                    const message = JSON.parse(output);
                    // Notify subscribers
                    this.onMessageCallbacks.forEach(callback => callback(message));
                }
                catch (e) {
                    // Not JSON, just log
                    this.outputChannel.appendLine(`Raw output: ${output}`);
                }
            }
        });
        this.process.stderr.on('data', (data) => {
            const errorOutput = data.toString().trim();
            if (errorOutput) {
                this.outputChannel.appendLine(`✗ MCP Error: ${errorOutput}`);
                this.onErrorCallbacks.forEach(callback => callback(errorOutput));
            }
        });
        this.process.on('exit', (code) => {
            this.outputChannel.appendLine(`Process exited with code ${code}`);
            vscode.window.showInformationMessage('MCP server stopped');
        });
    }
    async initializeMcpConnection() {
        try {
            // Send initialization
            // @ts-ignore - intentionally unused initialization response for future capabilities
            const _initResponse = await this.sendRequest('initialize', {
                protocolVersion: '2024-11-05',
                capabilities: {},
                clientInfo: {
                    name: 'vscode-auto-researcher',
                    version: '0.1.0'
                }
            });
            this.outputChannel.appendLine('✓ MCP connection initialized');
            // Send initialized notification
            await this.sendRequest('notifications/initialized');
            this.outputChannel.appendLine('✓ MCP handshake complete');
            vscode.window.showInformationMessage('Connected to Auto-Researcher MCP server');
        }
        catch (error) {
            this.outputChannel.appendLine(`✗ MCP initialization failed: ${error}`);
            vscode.window.showErrorMessage('Failed to connect to MCP server');
        }
    }
}
exports.McpClient = McpClient;
/**
 * Singleton MCP client instance
 */
let mcpClient = null;
/**
 * Get or create MCP client instance
 */
function getMcpClient(context) {
    if (!mcpClient) {
        mcpClient = new McpClient(context);
    }
    return mcpClient;
}
/**
 * Stop MCP client
 */
async function stopMcpClient() {
    if (mcpClient) {
        await mcpClient.stop();
        mcpClient = null;
    }
}
//# sourceMappingURL=mcp_client.js.map