import { spawn } from 'child_process';
import * as vscode from 'vscode';

/**
 * MCP Client for VS Code Extension
 * Connects to backend MCP server via stdio stream
 */
export class McpClient {
    private process: any;
    private outputChannel: vscode.OutputChannel;
    private onMessageCallbacks: Array<(message: any) => void> = [];
    private onErrorCallbacks: Array<(error: string) => void> = [];
    private messageIdCounter = 1;

    // @ts-ignore - intentionally unused parameter for future extension context access
    constructor(private _context: vscode.ExtensionContext) {
        this.outputChannel = vscode.window.createOutputChannel('Auto-Researcher MCP');
    }

    /**
     * Start MCP server process
     */
    async start(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
        // Find docker container name (use 'aider-agent' for MCP server based on docker-compose)
        const containerName = 'aider-agent';

                // Start MCP server via docker exec
                this.process = spawn('docker', ['exec', '-i', containerName,
                    'python', '-m', 'aider_mcp_launcher'], {
                    stdio: ['pipe', 'pipe', 'pipe']
                });

                this.setupEventHandlers();
                this.initializeMcpConnection();

                // Wait for ready message or timeout
                const timeout = setTimeout(() => {
                    this.outputChannel.appendLine('[ERROR] Timeout checking logs, but enforcing container check...');
                    // Try to inspect container to see if process is running despite no log match
                    const checkProcess = spawn('docker', ['exec', containerName, 'ps', 'aux']);
                    checkProcess.stdout.on('data', (psData) => {
                        if (psData.toString().includes('python -m agent.infrastructure.mcp.entrypoint')) {
                            this.outputChannel.appendLine('✓ Server process found active in container. Assuming ready.');
                            clearTimeout(timeout);
                            resolve(); // Force resolve if process exists
                        } else {
                            reject(new Error('MCP server startup timeout - process not found in container'));
                        }
                    });
                }, 30000); // Increase timeout to 30s for slow Docker environments

                // Listen for ready indication (more flexible detection)
                const readyListener = (data: Buffer) => {
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

            } catch (error) {
                reject(new Error(`Failed to start MCP server: ${error}`));
            }
        });
    }

    /**
     * Stop MCP server process
     */
    async stop(): Promise<void> {
        if (this.process) {
            this.process.kill();
            this.process = null;
        }
    }

    /**
     * Send MCP request and return response
     */
    async sendRequest(method: string, params?: any): Promise<any> {
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
            this.process.stdin.write(requestJson, (err: any) => {
                if (err) {
                    reject(new Error(`Failed to send request: ${err}`));
                }
            });

            // Listen for response
            const responseListener = (data: Buffer) => {
                try {
                    const response = JSON.parse(data.toString());
                    if (response.id === id) {
                        this.process.stdout.removeListener('data', responseListener);
                        if (response.error) {
                            reject(new Error(response.error.message));
                        } else {
                            resolve(response.result);
                        }
                    }
                } catch (e) {
                    // Not a valid JSON response, continue listening
                }
            };

            this.process.stdout.on('data', responseListener);
        });
    }

    /**
     * Register callback for messages from MCP server
     */
    onMessage(callback: (message: any) => void): void {
        this.onMessageCallbacks.push(callback);
    }

    /**
     * Register callback for errors from MCP server
     */
    onError(callback: (error: string) => void): void {
        this.onErrorCallbacks.push(callback);
    }

    /**
     * Call MCP tool
     */
    async callTool(toolName: string, args: any): Promise<any> {
        const response = await this.sendRequest('tools/call', {
            name: toolName,
            arguments: args
        });

        return response;
    }

    /**
     * Start research session (convenience method)
     */
    async startResearch(topic: string): Promise<void> {
        this.outputChannel.appendLine(`🚀 Starting research on: ${topic}`);

        try {
            // @ts-ignore - intentionally unused for future streaming event handling (Phase 5.2)
            const _events: any[] = [];

            // Use streaming version when available
            // For now, use tool call
            // @ts-ignore - intentionally unused result for now, will use in future streaming
            const _result = await this.callTool('orchestrator', { topic });

            // Handle streaming events if available
            // This will be enhanced in Phase 5.2 when we integrate real LangGraph streaming

            vscode.window.showInformationMessage(`Research started: ${topic}`);
            this.outputChannel.appendLine(`✓ Research orchestration initiated`);

        } catch (error) {
            const errorMsg = `Failed to start research: ${error}`;
            vscode.window.showErrorMessage(errorMsg);
            this.outputChannel.appendLine(`✗ ${errorMsg}`);
        }
    }

    private setupEventHandlers(): void {
        if (!this.process) return;

        this.process.stdout.on('data', (data: Buffer) => {
            const output = data.toString().trim();
            if (output) {
                this.outputChannel.appendLine(`← MCP: ${output}`);

                try {
                    const message = JSON.parse(output);
                    // Notify subscribers
                    this.onMessageCallbacks.forEach(callback => callback(message));
                } catch (e) {
                    // Not JSON, just log
                    this.outputChannel.appendLine(`Raw output: ${output}`);
                }
            }
        });

        this.process.stderr.on('data', (data: Buffer) => {
            const errorOutput = data.toString().trim();
            if (errorOutput) {
                this.outputChannel.appendLine(`✗ MCP Error: ${errorOutput}`);
                this.onErrorCallbacks.forEach(callback => callback(errorOutput));
            }
        });

        this.process.on('exit', (code: number) => {
            this.outputChannel.appendLine(`Process exited with code ${code}`);
            vscode.window.showInformationMessage('MCP server stopped');
        });
    }

    private async initializeMcpConnection(): Promise<void> {
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

        } catch (error) {
            this.outputChannel.appendLine(`✗ MCP initialization failed: ${error}`);
            vscode.window.showErrorMessage('Failed to connect to MCP server');
        }
    }
}

/**
 * Singleton MCP client instance
 */
let mcpClient: McpClient | null = null;

/**
 * Get or create MCP client instance
 */
export function getMcpClient(context: vscode.ExtensionContext): McpClient {
    if (!mcpClient) {
        mcpClient = new McpClient(context);
    }
    return mcpClient;
}

/**
 * Stop MCP client
 */
export async function stopMcpClient(): Promise<void> {
    if (mcpClient) {
        await mcpClient.stop();
        mcpClient = null;
    }
}