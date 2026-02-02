"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
const vscodeBridge_1 = require("./lib/vscodeBridge");
const vscode = window.acquireVsCodeApi();
const App = () => {
    const [message, setMessage] = (0, react_1.useState)('Loading Auto Researcher Webview...');
    (0, react_1.useEffect)(() => {
        // Initialize VS Code bridge
        const bridge = new vscodeBridge_1.VSCodeBridge(vscode);
        // Listen for messages from extension
        const messageHandler = (event) => {
            const message = event.data;
            console.log('[Webview] Received message:', message);
            switch (message.type) {
                case 'init':
                    setMessage('Webview initialized successfully!');
                    break;
                case 'update-data':
                    setMessage(`Data updated: ${JSON.stringify(message.data)}`);
                    break;
                default:
                    console.log('[Webview] Unknown message type:', message.type);
            }
        };
        window.addEventListener('message', messageHandler);
        // Send ready message to extension
        bridge.postMessage({ type: 'webview-ready' });
        return () => {
            window.removeEventListener('message', messageHandler);
        };
    }, []);
    return (<div className="min-h-screen bg-background text-foreground p-4">
      <div className="max-w-4xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-primary">
            🤖 Auto Researcher Webview
          </h1>
          <p className="text-muted-foreground mt-2">
            React-based Collaboration UI for MCP-powered Research
          </p>
        </header>

        <main className="space-y-6">
          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Status</h2>
            <p className="text-sm text-muted-foreground">{message}</p>
          </div>

          <div className="bg-card p-6 rounded-lg border">
            <h2 className="text-xl font-semibold mb-4">Components to be Implemented</h2>
            <ul className="space-y-2 text-sm">
              <li className="flex items-center">
                <span className="w-2 h-2 bg-primary rounded-full mr-3"></span>
                Activity Timeline (Chain of Thought)
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-muted rounded-full mr-3"></span>
                HITL Decision Cards
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-muted rounded-full mr-3"></span>
                Session Management
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-muted rounded-full mr-3"></span>
                MCP Data Integration
              </li>
            </ul>
          </div>
        </main>
      </div>
    </div>);
};
exports.default = App;
//# sourceMappingURL=App.js.map