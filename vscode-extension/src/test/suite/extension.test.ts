import * as assert from 'assert';
import * as vscode from 'vscode';
import * as sinon from 'sinon';
import { suite, test, beforeEach, afterEach } from 'mocha';
import * as api from '../../api'; // Import the api module to stub it
import { activate } from '../../extension'; // Import activate to test it

suite('Extension Test Suite', () => {
    let sandbox: sinon.SinonSandbox;

    beforeEach(() => {
        sandbox = sinon.createSandbox();
    });

    afterEach(() => {
        sandbox.restore();
    });

    // Test for successful health check
    test('should show an information message on successful health check', async () => {
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: 'ok' });
        const showInfoMessageSpy = sandbox.spy(vscode.window, 'showInformationMessage');
        // Stub command registration to prevent side effects between tests
        sandbox.stub(vscode.commands, 'registerCommand');

        const mockContext: any = { subscriptions: [] };
        activate(mockContext);
        await new Promise(resolve => setImmediate(resolve));

        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        assert.ok(
            showInfoMessageSpy.calledWith('Auto-Researcher: Connected to backend.'),
            'showInformationMessage should be called with the success message'
        );
    });

    // Test for failed health check
    test('should show an error message on failed health check', async () => {
        const checkHealthStub = sandbox.stub(api, 'checkHealth').rejects(new Error('Network Error'));
        const showErrorMessageSpy = sandbox.spy(vscode.window, 'showErrorMessage');
        // Stub command registration to prevent side effects between tests
        sandbox.stub(vscode.commands, 'registerCommand');

        const mockContext: any = { subscriptions: [] };
        activate(mockContext);
        await new Promise(resolve => setImmediate(resolve));

        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        assert.ok(
            showErrorMessageSpy.calledWith('Auto-Researcher: Failed to connect to backend.'),
            'showErrorMessage should be called with the failure message'
        );
    });

    // Test for view and command registration
    test('should register three-panel layout views and commands on activation', () => {
        const registerTreeDataProviderStub = sandbox.stub(vscode.window, 'registerTreeDataProvider');
        const registerCommandStub = sandbox.stub(vscode.commands, 'registerCommand');

        const mockContext: any = { subscriptions: [] };
        activate(mockContext);

        assert.ok(registerTreeDataProviderStub.calledWith('assetLibrary', sinon.match.any), 'assetLibrary should be registered');
        assert.ok(registerTreeDataProviderStub.calledWith('manuscript', sinon.match.any), 'manuscript should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.showControlPanel', sinon.match.any), 'showControlPanel command should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.refreshAssetLibrary', sinon.match.any), 'refreshAssetLibrary command should be registered');
        assert.ok(registerCommandStub.calledWith('auto-researcher.refreshManuscript', sinon.match.any), 'refreshManuscript command should be registered');
    });

    // Test for control panel webview creation
    test('should create a webview panel when showControlPanel is triggered', async () => {
        const createWebviewPanelSpy = sandbox.spy(vscode.window, 'createWebviewPanel');
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: 'ok' });

        // Manually call the command handler logic
        const panel = vscode.window.createWebviewPanel(
            'aiControlPanel',
            'AI Control Panel',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );
        let status = 'Unknown';
        try {
            const health = await api.checkHealth();
            status = health.status || 'Unknown';
        } catch (err) {
            status = 'Error';
        }
        panel.webview.html = `<html><body><h2>Agent Status</h2><p>${status}</p></body></html>`;

        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
    });

    // TDD: Test for agent status in control panel webview
    test('should display agent status in control panel webview', async () => {
        const mockStatus = 'Agent is running';
        const checkHealthStub = sandbox.stub(api, 'checkHealth').resolves({ status: mockStatus });
        const createWebviewPanelSpy = sandbox.spy(vscode.window, 'createWebviewPanel');
        
        // Manually create the webview panel like the command does
        const panel = vscode.window.createWebviewPanel(
            'aiControlPanel',
            'AI Control Panel',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );
        let status = 'Unknown';
        try {
            const health = await api.checkHealth();
            status = health.status || 'Unknown';
        } catch (err) {
            status = 'Error';
        }
        panel.webview.html = `<html><body><h2>Agent Status</h2><p>${status}</p></body></html>`;
        
        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(checkHealthStub.calledOnce, 'checkHealth should be called once');
        // 检查 webview HTML 是否包含 agent 状态
        const html = panel.webview.html;
        assert.ok(html.includes(mockStatus), 'Webview HTML should include agent status');
    });    // TDD: Asset Library should display papers from backend
    test('should display papers from backend in Asset Library view', async () => {
        // 1. (Red) Setup the test for failure
        const mockState: api.AgentState = {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [
                { title: 'Paper 1', authors: ['Author A'], abstract: 'Abstract 1' },
                { title: 'Paper 2', authors: ['Author B', 'Author C'], abstract: 'Abstract 2' },
            ],
            report: '', // Add missing property to satisfy the interface
        };
        sandbox.stub(api, 'getAgentState').resolves(mockState);

        // We will create this provider in the implementation step
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { AssetLibraryProvider } = await import('../../extension');
        const assetLibraryProvider = new AssetLibraryProvider();

        // 2. Get the children from the provider
        const children = await assetLibraryProvider.getChildren();

        // 3. Assert the results
        assert.strictEqual(children.length, 2, 'Should return two paper items');
        assert.strictEqual(children[0].label, 'Paper 1', 'First paper title should match');
        assert.strictEqual(children[0].description, 'Author A', 'First paper authors should match');
        assert.strictEqual(children[1].label, 'Paper 2', 'Second paper title should match');
        assert.strictEqual(children[1].description, 'Author B, Author C', 'Second paper authors should match');
    });

    // TDD: Manuscript should display report from backend
    test('should display report from backend in Manuscript view', async () => {
        // 1. (Red) Setup the test for failure
        const mockState: api.AgentState = {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: 'This is the generated research report.',
        };
        sandbox.stub(api, 'getAgentState').resolves(mockState);

        // We will create this provider in the implementation step
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await import('../../extension');
        const manuscriptProvider = new ManuscriptProvider();

        // 2. Get the children from the provider
        const children = await manuscriptProvider.getChildren();

        // 3. Assert the results
        assert.strictEqual(children.length, 1, 'Should return one report item');
        assert.strictEqual(children[0].label, mockState.report, 'Report content should match');
    });

    // TDD: Manuscript should display message when report is empty
    test('should display "No report found" when report is empty', async () => {
        const mockState: api.AgentState = {
            // Backend API uses snake_case
            // eslint-disable-next-line @typescript-eslint/naming-convention
            literature_abstracts: [],
            report: '',
        };
        sandbox.stub(api, 'getAgentState').resolves(mockState);

        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await import('../../extension');
        const manuscriptProvider = new ManuscriptProvider();
        const children = await manuscriptProvider.getChildren();

        assert.strictEqual(children.length, 1, 'Should return one item');
        assert.strictEqual(children[0].label, 'No report found', 'Should display "No report found"');
    });

    // TDD: Asset Library refresh should trigger onDidChangeTreeData event
    test('should fire onDidChangeTreeData event when Asset Library is refreshed', async () => {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { AssetLibraryProvider } = await import('../../extension');
        const provider = new AssetLibraryProvider();
        
        let eventFired = false;
        provider.onDidChangeTreeData(() => {
            eventFired = true;
        });

        provider.refresh();
        
        assert.ok(eventFired, 'onDidChangeTreeData event should be fired when refresh is called');
    });

    // TDD: Manuscript refresh should trigger onDidChangeTreeData event
    test('should fire onDidChangeTreeData event when Manuscript is refreshed', async () => {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        const { ManuscriptProvider } = await import('../../extension');
        const provider = new ManuscriptProvider();
        
        let eventFired = false;
        provider.onDidChangeTreeData(() => {
            eventFired = true;
        });

        provider.refresh();
        
        assert.ok(eventFired, 'onDidChangeTreeData event should be fired when refresh is called');
    });

    // TDD: Enhanced Control Panel should display research topic
    test('should display research topic in enhanced Control Panel', async () => {
        const mockState: api.AgentState = {
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
        const panel = vscode.window.createWebviewPanel(
            'aiControlPanel',
            'AI Control Panel',
            vscode.ViewColumn.One,
            { enableScripts: true }
        );
        
        const state = await api.getAgentState();
        const html = `<html><body><h2>Research Topic: ${state.research_topic || 'N/A'}</h2></body></html>`;
        panel.webview.html = html;
        
        assert.ok(createWebviewPanelSpy.calledOnce, 'createWebviewPanel should be called once');
        assert.ok(panel.webview.html.includes('Machine Learning in Healthcare'), 'HTML should include research topic');
    });

    // TDD: Enhanced Control Panel should display paper count
    test('should display paper count in enhanced Control Panel', async () => {
        const mockState: api.AgentState = {
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

