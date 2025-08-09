"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const cp = require("child_process");
const axios_1 = require("axios");
class VibeTrackProvider {
    constructor() {
        this.outputChannel = vscode.window.createOutputChannel('VibeTrack');
        this.updateConfig();
    }
    updateConfig() {
        const config = vscode.workspace.getConfiguration('vibetrack');
        this.config = {
            aiEndpoint: config.get('aiEndpoint', 'http://localhost:1234/v1/chat/completions'),
            aiModel: config.get('aiModel', 'mistralai/mathstral-7b-v0.1'),
            englishMode: config.get('englishMode', true),
            autoSave: config.get('autoSave', true),
            exportFormat: config.get('exportFormat', 'markdown')
        };
    }
    async executeGitCommand(command, workspaceRoot) {
        return new Promise((resolve, reject) => {
            cp.exec(command, { cwd: workspaceRoot }, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                }
                else {
                    resolve(stdout);
                }
            });
        });
    }
    async analyzeWithAI(diff, analysisType = 'diff') {
        try {
            const systemPrompt = "You are a senior code reviewer and mentor. Analyze code diffs and explain them clearly for developers who might be confused about what changed.";
            const userPrompt = `The following code was changed:\n\n${diff}\n\nPlease explain clearly:\n1. What exactly changed?\n2. Why was it likely changed? (What was the probable reason?)\n3. What's the difference in behavior?\n4. How would you explain this to someone who asks about it?\n\nMake your explanation narrative and easy to understand, not overly technical.`;
            const response = await axios_1.default.post(this.config.aiEndpoint, {
                model: this.config.aiModel,
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: userPrompt }
                ],
                temperature: 0.7,
                max_tokens: 1024
            });
            return response.data.choices[0].message.content.trim();
        }
        catch (error) {
            return `❌ Error connecting to AI: ${error}\n\n💡 The AI server might not be available. Please check your configuration.`;
        }
    }
    async showAnalysisResult(title, diff, analysis) {
        const panel = vscode.window.createWebviewPanel('vibetrackAnalysis', title, vscode.ViewColumn.Two, {
            enableScripts: true,
            retainContextWhenHidden: true
        });
        const htmlContent = this.generateWebviewContent(title, diff, analysis);
        panel.webview.html = htmlContent;
        // Handle messages from webview
        panel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'export':
                    this.exportReport(message.format, diff, analysis, title);
                    break;
                case 'copy':
                    vscode.env.clipboard.writeText(message.text);
                    vscode.window.showInformationMessage('Copied to clipboard!');
                    break;
            }
        }, undefined);
    }
    generateWebviewContent(title, diff, analysis) {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${title}</title>
            <style>
                body {
                    font-family: var(--vscode-font-family);
                    font-size: var(--vscode-font-size);
                    color: var(--vscode-foreground);
                    background-color: var(--vscode-editor-background);
                    padding: 20px;
                    line-height: 1.6;
                }
                .header {
                    border-bottom: 2px solid var(--vscode-panel-border);
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }
                .section {
                    margin-bottom: 30px;
                    padding: 15px;
                    border: 1px solid var(--vscode-panel-border);
                    border-radius: 8px;
                    background-color: var(--vscode-editor-inactiveSelectionBackground);
                }
                .diff-container {
                    background-color: var(--vscode-textCodeBlock-background);
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-family: var(--vscode-editor-font-family);
                    font-size: var(--vscode-editor-font-size);
                }
                .analysis {
                    white-space: pre-wrap;
                    background-color: var(--vscode-textBlockQuote-background);
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid var(--vscode-textLink-foreground);
                }
                .button-group {
                    margin-top: 20px;
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                .btn {
                    background-color: var(--vscode-button-background);
                    color: var(--vscode-button-foreground);
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
                .btn:hover {
                    background-color: var(--vscode-button-hoverBackground);
                }
                .btn-secondary {
                    background-color: var(--vscode-button-secondaryBackground);
                    color: var(--vscode-button-secondaryForeground);
                }
                .emoji { font-size: 1.2em; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1><span class="emoji">🎯</span> ${title}</h1>
                <p>VibeTrack Analysis - AI-powered Git change analyzer</p>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🔍</span> Detected Changes</h2>
                <div class="diff-container">
                    <pre>${diff}</pre>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🧠</span> AI Analysis</h2>
                <div class="analysis">${analysis}</div>
            </div>
            
            <div class="button-group">
                <button class="btn" onclick="exportReport('markdown')">
                    <span class="emoji">📄</span> Export Markdown
                </button>
                <button class="btn" onclick="exportReport('json')">
                    <span class="emoji">📊</span> Export JSON
                </button>
                <button class="btn" onclick="exportReport('html')">
                    <span class="emoji">🌐</span> Export HTML
                </button>
                <button class="btn btn-secondary" onclick="copyAnalysis()">
                    <span class="emoji">📋</span> Copy Analysis
                </button>
            </div>
            
            <script>
                const vscode = acquireVsCodeApi();
                
                function exportReport(format) {
                    vscode.postMessage({
                        command: 'export',
                        format: format
                    });
                }
                
                function copyAnalysis() {
                    vscode.postMessage({
                        command: 'copy',
                        text: \`${analysis}\`
                    });
                }
            </script>
        </body>
        </html>`;
    }
    async exportReport(format, diff, analysis, title) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return;
        try {
            // Call the Python CLI for export
            const command = `vibetrack check --no-save`;
            await this.executeGitCommand(command, workspaceRoot);
            vscode.window.showInformationMessage(`Report exported as ${format}!`);
        }
        catch (error) {
            vscode.window.showErrorMessage(`Export error: ${error}`);
        }
    }
    async analyzeCurrentChanges() {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) {
            vscode.window.showErrorMessage('No workspace folder found!');
            return;
        }
        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: '🔍 Analyzing changes...',
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                const diff = await this.executeGitCommand('git diff HEAD', workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage('✅ No changes found!');
                    return;
                }
                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'current-changes');
                progress.report({ increment: 40 });
                const title = '🔍 Current Changes Analysis';
                await this.showAnalysisResult(title, diff, analysis);
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }
    async analyzeStagedChanges() {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return;
        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: '🎭 Analyzing staged changes...',
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                const diff = await this.executeGitCommand('git diff --cached', workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage('ℹ️ No staged files found!');
                    return;
                }
                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'staged-changes');
                progress.report({ increment: 40 });
                const title = '🎭 Staged Files Analysis';
                await this.showAnalysisResult(title, diff, analysis);
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }
    async compareCommits() {
        const commit1 = await vscode.window.showInputBox({
            prompt: 'First commit (e.g., HEAD~1):',
            value: 'HEAD~1'
        });
        if (!commit1)
            return;
        const commit2 = await vscode.window.showInputBox({
            prompt: 'Second commit (e.g., HEAD):',
            value: 'HEAD'
        });
        if (!commit2)
            return;
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return;
        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: `📖 Comparing ${commit1} and ${commit2}...`,
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                const diff = await this.executeGitCommand(`git diff ${commit1} ${commit2}`, workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage('ℹ️ No differences found!');
                    return;
                }
                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'commit-comparison');
                progress.report({ increment: 40 });
                const title = `📖 Compare ${commit1} and ${commit2}`;
                await this.showAnalysisResult(title, diff, analysis);
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }
    async analyzeCommitMessage() {
        const commitHash = await vscode.window.showInputBox({
            prompt: 'Commit hash (default: HEAD):',
            value: 'HEAD'
        });
        if (!commitHash)
            return;
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return;
        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: '📝 Analyzing commit message...',
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 25 });
                // Get commit message
                const commitMessage = await this.executeGitCommand(`git log --format=%B -n 1 ${commitHash}`, workspaceRoot);
                progress.report({ increment: 25 });
                // Get commit changes
                const diff = await this.executeGitCommand(`git show ${commitHash} --format=""`, workspaceRoot);
                progress.report({ increment: 25 });
                // Analyze consistency
                const prompt = `Commit message:\n${commitMessage}\n\nActual changes:\n${diff}\n\nDoes the commit message match the changes? Analyze the consistency and suggest improvements if needed.`;
                const analysis = await this.analyzeWithAI(prompt, 'commit-message-analysis');
                progress.report({ increment: 25 });
                const title = '📝 Commit Message Analysis';
                await this.showAnalysisResult(title, `Commit: ${commitHash}\nMessage: ${commitMessage}\n\n${diff}`, analysis);
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }
}
function activate(context) {
    const provider = new VibeTrackProvider();
    // Register commands
    const commands = [
        vscode.commands.registerCommand('vibetrack.analyzeChanges', () => provider.analyzeCurrentChanges()),
        vscode.commands.registerCommand('vibetrack.analyzeStaged', () => provider.analyzeStagedChanges()),
        vscode.commands.registerCommand('vibetrack.compareCommits', () => provider.compareCommits()),
        vscode.commands.registerCommand('vibetrack.analyzeCommitMessage', () => provider.analyzeCommitMessage()),
        vscode.commands.registerCommand('vibetrack.openSettings', () => {
            vscode.commands.executeCommand('workbench.action.openSettings', 'vibetrack');
        })
    ];
    commands.forEach(command => context.subscriptions.push(command));
    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = "$(git-branch) VibeTrack";
    statusBarItem.tooltip = "VibeTrack - AI-powered Git change analyzer";
    statusBarItem.command = 'vibetrack.analyzeChanges';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map