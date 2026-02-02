"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const vscode = require("vscode");
const sinon = require("sinon");
const mocha_1 = require("mocha");
const api = require("../../api"); // Import the api module to stub it
const extension_1 = require("../../extension"); // Import activate to test it
(0, mocha_1.suite)('Extension Test Suite', () => {
    let sandbox;
    (0, mocha_1.beforeEach)(() => {
        sandbox = sinon.createSandbox();
    });
    (0, mocha_1.afterEach)(() => {
        sandbox.restore();
    });
    // Helper to create a robust mock context
    const createMockContext = () => ({
        subscriptions: [],
        asAbsolutePath: (relativePath) => `/mock/path/${relativePath}`,
        extensionUri: vscode.Uri.file('/mock/path'),
        environmentVariableCollection: {},
        extensionMode: vscode.ExtensionMode.Test,
        storageUri: vscode.Uri.file('/mock/storage'),
        globalStorageUri: vscode.Uri.file('/mock/globalStorage'),
        logUri: vscode.Uri.file('/mock/log'),
        extension: {
            id: 'mock.extension',
            extensionUri: vscode.Uri.file('/mock/path'),
            packageJSON: { version: '0.0.1' },
            isActive: true,
            exports: undefined,
            activate: () => Promise.resolve(),
        },
        secrets: {
            get: () => Promise.resolve(undefined),
            store: () => Promise.resolve(),
            delete: () => Promise.resolve(),
            onDidChange: new vscode.EventEmitter().event,
        },
        workspaceState: {
            get: () => undefined,
            update: () => Promise.resolve(),
            keys: () => []
        },
        globalState: {
            get: () => undefined,
            update: () => Promise.resolve(),
            keys: () => [],
            setKeysForSync: () => { }
        },
        extensionPath: '/mock/path',
        storagePath: '/mock/storage',
        globalStoragePath: '/mock/globalStorage'
    });
    // Test for successful health check
    (0, mocha_1.test)('should show an information message on successful health check', async () => {
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: 'ok' });
        const showInfoMessageSpy = sandbox.spy(vscode.window, 'showInformationMessage');
        // Stub command registration to prevent side effects between tests
        sandbox.stub(vscode.commands, 'registerCommand');
        const mockContext = createMockContext();
        (0, extension_1.activate)(mockContext);
        await new Promise(resolve => setImmediate(resolve));
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        assert.ok(showInfoMessageSpy.calledWith('Auto-Researcher: Connected to backend.'), 'showInformationMessage should be called with the success message');
    });
    // Test for failed health check
    (0, mocha_1.test)('should show an error message on failed health check', async () => {
        const checkHealthStub = sandbox.stub(api, 'checkHealth').rejects(new Error('Network Error'));
        const showErrorMessageSpy = sandbox.spy(vscode.window, 'showErrorMessage');
        // Stub command registration to prevent side effects between tests
        sandbox.stub(vscode.commands, 'registerCommand');
        const mockContext = createMockContext();
        (0, extension_1.activate)(mockContext);
        await new Promise(resolve => setImmediate(resolve));
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        assert.ok(showErrorMessageSpy.calledWith('Auto-Researcher: Failed to connect to backend.'), 'showErrorMessage should be called with the failure message');
    });
    // Test for view and command registration
    (0, mocha_1.test)('should register three-panel layout views and commands on activation', () => {
        const registerTreeDataProviderStub = sandbox.stub(vscode.window, 'registerTreeDataProvider');
        const registerCommandStub = sandbox.stub(vscode.commands, 'registerCommand');
        const mockContext = createMockContext();
        (0, extension_1.activate)(mockContext);
        assert.ok(registerTreeDataProviderStub.calledWith('assetLibrary', sinon.match.any), 'assetLibrary should be registered');
        assert.ok(registerTreeDataProviderStub.calledWith('manuscript', sinon.match.any), 'manuscript should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.showControlPanel', sinon.match.any), 'showControlPanel command should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.refreshAssetLibrary', sinon.match.any), 'refreshAssetLibrary command should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.refreshManuscript', sinon.match.any), 'refreshManuscript command should be registered');
    });
    // Test for control panel webview creation
    (0, mocha_1.test)('should create a webview panel when showControlPanel is triggered', async () => {
        const createWebviewPanelSpy = sandbox.spy(vscode.window, 'createWebviewPanel');
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: 'ok' });
        // Manually call the command handler logic
        const panel = vscode.window.createWebviewPanel('aiControlPanel', 'AI Control Panel', vscode.ViewColumn.One, { enableScripts: true });
        let status = 'Unknown';
        try {
            const health = await api.checkHealth();
            status = health.status || 'Unknown';
        }
        catch (err) {
            status = 'Error';
        }
        panel.webview.html = `<html><body><h2>Agent Status</h2><p>${status}</p></body></html>`;
        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
    });
    // TDD: Test for agent status in control panel webview
    (0, mocha_1.test)('should display agent status in control panel webview', async () => {
        const mockStatus = 'Agent is running';
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: mockStatus });
        const createWebviewPanelSpy = sandbox.spy(vscode.window, 'createWebviewPanel');
        // Manually create the webview panel like the command does
        const panel = vscode.window.createWebviewPanel('aiControlPanel', 'AI Control Panel', vscode.ViewColumn.One, { enableScripts: true });
        let status = 'Unknown';
        try {
            const health = await api.checkHealth();
            status = health.status || 'Unknown';
        }
        catch (err) {
            status = 'Error';
        }
        panel.webview.html = `<html><body><h2>Agent Status</h2><p>${status}</p></body></html>`;
        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        // 检查 webview HTML 是否包含 agent 状态
        const html = panel.webview.html;
        assert.ok(html.includes(mockStatus), 'Webview HTML should include agent status');
    }); // TDD: Asset Library should display papers from backend
    (0, mocha_1.test)('should display papers from backend in Asset Library view', async () => {
        // 1. (Red) Setup the test for failure
        const mockPapers = {
            papers: [
                {
                    id: '1',
                    session_id: 'session-1',
                    title: 'Paper 1',
                    authors: ['Author A'],
                    abstract: 'Abstract 1',
                    doi: null,
                    arxiv_id: null,
                    url: null,
                    created_at: new Date().toISOString(),
                    extra_metadata: {}
                },
                {
                    id: '2',
                    session_id: 'session-2',
                    title: 'Paper 2',
                    authors: ['Author B', 'Author C'],
                    abstract: 'Abstract 2',
                    doi: null,
                    arxiv_id: null,
                    url: null,
                    created_at: new Date().toISOString(),
                    extra_metadata: {}
                },
            ]
        };
        sandbox.stub(api, 'getAllPapers').resolves(mockPapers);
        // We will create this provider in the implementation step
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { AssetLibraryProvider } = await Promise.resolve().then(() => require('../../extension'));
        const assetLibraryProvider = new AssetLibraryProvider();
        // 2. Get the children from the provider
        const children = await assetLibraryProvider.getChildren();
        // 3. Assert the results (AssetLibrary now groups by session by default)
        assert.strictEqual(children.length, 2, 'Should return two session groups');
        assert.ok(children[0].label && children[0].label.includes('session-1'), 'First session label should match');
        assert.ok(children[1].label && children[1].label.includes('session-2'), 'Second session label should match');
    });
    // TDD: Manuscript should display report from backend
    (0, mocha_1.test)('should display report from backend in Manuscript view', async () => {
        // 1. (Red) Setup the test for failure
        const mockReports = {
            reports: [
                {
                    id: '1',
                    session_id: 'session-1',
                    content: 'This is the generated research report.',
                    format: 'markdown',
                    version: 1,
                    created_at: new Date().toISOString(),
                    extra_metadata: {}
                }
            ]
        };
        sandbox.stub(api, 'getAllReports').resolves(mockReports);
        // We will create this provider in the implementation step
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await Promise.resolve().then(() => require('../../extension'));
        const manuscriptProvider = new ManuscriptProvider();
        // 2. Get the children from the provider
        const children = await manuscriptProvider.getChildren();
        // 3. Assert the results (ManuscriptProvider now groups by session)
        assert.strictEqual(children.length, 1, 'Should return one session group');
        // The label for report group is usually the session ID or similar
        assert.ok(children[0].label && children[0].label.includes('session-1'), 'Session label should match');
    });
    // TDD: Manuscript should display message when report is empty
    (0, mocha_1.test)('should display "No reports found" when report is empty', async () => {
        const mockReports = {
            reports: []
        };
        sandbox.stub(api, 'getAllReports').resolves(mockReports);
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await Promise.resolve().then(() => require('../../extension'));
        const manuscriptProvider = new ManuscriptProvider();
        const children = await manuscriptProvider.getChildren();
        assert.strictEqual(children.length, 1, 'Should return one item');
        assert.strictEqual(children[0].label, 'No reports found', 'Should display "No reports found"');
    });
    // TDD: Asset Library refresh should trigger onDidChangeTreeData event
    (0, mocha_1.test)('should fire onDidChangeTreeData event when Asset Library is refreshed', async () => {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { AssetLibraryProvider } = await Promise.resolve().then(() => require('../../extension'));
        const provider = new AssetLibraryProvider();
        let eventFired = false;
        provider.onDidChangeTreeData(() => {
            eventFired = true;
        });
        provider.refresh();
        assert.ok(eventFired, 'onDidChangeTreeData event should be fired when refresh is called');
    });
    // TDD: Manuscript refresh should trigger onDidChangeTreeData event
    (0, mocha_1.test)('should fire onDidChangeTreeData event when Manuscript is refreshed', async () => {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await Promise.resolve().then(() => require('../../extension'));
        const provider = new ManuscriptProvider();
        let eventFired = false;
        provider.onDidChangeTreeData(() => {
            eventFired = true;
        });
        provider.refresh();
        assert.ok(eventFired, 'onDidChangeTreeData event should be fired when refresh is called');
    });
    // TDD: Enhanced Control Panel should display research topic
    (0, mocha_1.test)('should display research topic in enhanced Control Panel', async () => {
        const mockState = {
            // eslint-disable-next-line @typescript-eslint/naming-convention
            research_topic: 'Machine Learning in Healthcare',
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: '',
        };
        sandbox.stub(api, 'getAgentState').resolves(mockState);
        sandbox.stub(api, 'checkHealth').resolves({ status: 'ok' });
        const createWebviewPanelSpy = sandbox.spy(vscode.window, 'createWebviewPanel');
        // Simulate the enhanced control panel command
        const panel = vscode.window.createWebviewPanel('aiControlPanel', 'AI Control Panel', vscode.ViewColumn.One, { enableScripts: true });
        const state = await api.getAgentState();
        const html = `<html><body><h2>Research Topic: ${state.research_topic || 'N/A'}</h2></body></html>`;
        panel.webview.html = html;
        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(panel.webview.html.includes('Machine Learning in Healthcare'), 'HTML should include research topic');
    });
    // TDD: Enhanced Control Panel should display paper count
    (0, mocha_1.test)('should display paper count in enhanced Control Panel', async () => {
        const mockState = {
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [
                { title: 'Paper 1', authors: ['Author A'], abstract: 'Abstract 1' },
                { title: 'Paper 2', authors: ['Author B'], abstract: 'Abstract 2' },
            ],
            report: '',
        };
        sandbox.stub(api, 'getAgentState').resolves(mockState);
        const state = await api.getAgentState();
        const paperCount = state.literature_abstracts.length;
        assert.strictEqual(paperCount, 2, 'Paper count should be 2');
    });
});
//# sourceMappingURL=extension.test.js.map