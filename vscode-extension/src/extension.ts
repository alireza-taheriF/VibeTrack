import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import axios from 'axios';

interface VibeTrackConfig {
    aiEndpoint: string;
    aiModel: string;
    persianMode: boolean;
    autoSave: boolean;
    exportFormat: string;
}

class VibeTrackProvider {
    private config: VibeTrackConfig;
    private outputChannel: vscode.OutputChannel;

    constructor() {
        this.outputChannel = vscode.window.createOutputChannel('VibeTrack');
        this.updateConfig();
    }

    private updateConfig() {
        const config = vscode.workspace.getConfiguration('vibetrack');
        this.config = {
            aiEndpoint: config.get('aiEndpoint', 'http://localhost:1234/v1/chat/completions'),
            aiModel: config.get('aiModel', 'mistralai/mathstral-7b-v0.1'),
            persianMode: config.get('persianMode', true),
            autoSave: config.get('autoSave', true),
            exportFormat: config.get('exportFormat', 'markdown')
        };
    }

    private async executeGitCommand(command: string, workspaceRoot: string): Promise<string> {
        return new Promise((resolve, reject) => {
            cp.exec(command, { cwd: workspaceRoot }, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(stdout);
                }
            });
        });
    }

    private async analyzeWithAI(diff: string, analysisType: string = 'diff'): Promise<string> {
        try {
            const systemPrompt = this.config.persianMode 
                ? "تو یک برنامه‌نویس باتجربه و مربی کدنویسی هستی. کارت اینه که تغییرات کد رو به زبان ساده و فارسی توضیح بدی."
                : "You are a senior code reviewer and mentor. Analyze code diffs and explain them clearly.";

            const userPrompt = this.config.persianMode
                ? `این کد تغییر کرده:\n\n${diff}\n\nلطفاً به زبان فارسی و ساده توضیح بده:\n1. دقیقاً چی عو�� شده؟\n2. چرا این تغییر انجام شده؟\n3. این تغییر چه تأثیری روی رفتار برنامه داره؟`
                : `The following code was changed:\n\n${diff}\n\nPlease explain:\n1. What exactly changed?\n2. Why was it likely changed?\n3. What's the difference in behavior?`;

            const response = await axios.post(this.config.aiEndpoint, {
                model: this.config.aiModel,
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: userPrompt }
                ],
                temperature: 0.7,
                max_tokens: 1024
            });

            return response.data.choices[0].message.content.trim();
        } catch (error) {
            const errorMsg = this.config.persianMode 
                ? `❌ خطا در اتصال به هوش مصنوعی: ${error}`
                : `❌ Error connecting to AI: ${error}`;
            return errorMsg;
        }
    }

    private async showAnalysisResult(title: string, diff: string, analysis: string) {
        const panel = vscode.window.createWebviewPanel(
            'vibetrackAnalysis',
            title,
            vscode.ViewColumn.Two,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        const htmlContent = this.generateWebviewContent(title, diff, analysis);
        panel.webview.html = htmlContent;

        // Handle messages from webview
        panel.webview.onDidReceiveMessage(
            message => {
                switch (message.command) {
                    case 'export':
                        this.exportReport(message.format, diff, analysis, title);
                        break;
                    case 'copy':
                        vscode.env.clipboard.writeText(message.text);
                        vscode.window.showInformationMessage(
                            this.config.persianMode ? 'کپی شد!' : 'Copied to clipboard!'
                        );
                        break;
                }
            },
            undefined
        );
    }

    private generateWebviewContent(title: string, diff: string, analysis: string): string {
        const isRTL = this.config.persianMode;
        return `<!DOCTYPE html>
        <html lang="${isRTL ? 'fa' : 'en'}" dir="${isRTL ? 'rtl' : 'ltr'}">
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
                <p>${isRTL ? 'تحلیل VibeTrack - دستیار شخصی برای Vibe Coders' : 'VibeTrack Analysis - Personal Assistant for Vibe Coders'}</p>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🔍</span> ${isRTL ? 'تغییرات شناسایی شده' : 'Detected Changes'}</h2>
                <div class="diff-container">
                    <pre>${diff}</pre>
                </div>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🧠</span> ${isRTL ? 'تحلیل هوش مصنوعی' : 'AI Analysis'}</h2>
                <div class="analysis">${analysis}</div>
            </div>
            
            <div class="button-group">
                <button class="btn" onclick="exportReport('markdown')">
                    <span class="emoji">📄</span> ${isRTL ? 'Export Markdown' : 'Export Markdown'}
                </button>
                <button class="btn" onclick="exportReport('json')">
                    <span class="emoji">📊</span> ${isRTL ? 'Export JSON' : 'Export JSON'}
                </button>
                <button class="btn" onclick="exportReport('html')">
                    <span class="emoji">🌐</span> ${isRTL ? 'Export HTML' : 'Export HTML'}
                </button>
                <button class="btn btn-secondary" onclick="copyAnalysis()">
                    <span class="emoji">📋</span> ${isRTL ? 'کپی تحلیل' : 'Copy Analysis'}
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

    private async exportReport(format: string, diff: string, analysis: string, title: string) {
        // This would integrate with the Python CLI to generate reports
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return;

        try {
            // Call the Python CLI for export
            const command = `python -m vibetrack.save_result --format ${format} --title "${title}"`;
            await this.executeGitCommand(command, workspaceRoot);
            
            vscode.window.showInformationMessage(
                this.config.persianMode 
                    ? `گزارش ${format} ذخیره شد!` 
                    : `Report exported as ${format}!`
            );
        } catch (error) {
            vscode.window.showErrorMessage(
                this.config.persianMode 
                    ? `خطا در export: ${error}` 
                    : `Export error: ${error}`
            );
        }
    }

    async analyzeCurrentChanges() {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) {
            vscode.window.showErrorMessage(
                this.config.persianMode ? 'پوشه پروژه پیدا نشد!' : 'No workspace folder found!'
            );
            return;
        }

        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: this.config.persianMode ? '🔍 دارم تغییرات رو چک میکنم...' : '🔍 Analyzing changes...',
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                
                const diff = await this.executeGitCommand('git diff HEAD', workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage(
                        this.config.persianMode ? '✅ هیچ تغییری پیدا نشد!' : '✅ No changes found!'
                    );
                    return;
                }

                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'current-changes');
                
                progress.report({ increment: 40 });
                const title = this.config.persianMode ? '😵 چی شده؟! - تحلیل تغییرات' : '😵 What happened?! - Changes Analysis';
                await this.showAnalysisResult(title, diff, analysis);
            });
        } catch (error) {
            vscode.window.showErrorMessage(
                this.config.persianMode ? `خطا: ${error}` : `Error: ${error}`
            );
        }
    }

    async analyzeStagedChanges() {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return;

        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: this.config.persianMode ? '🎵 دارم فایل‌های staged رو تحلیل میکنم...' : '🎵 Analyzing staged changes...',
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                
                const diff = await this.executeGitCommand('git diff --cached', workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage(
                        this.config.persianMode ? 'ℹ️ هیچ فایل staged پیدا نشد!' : 'ℹ️ No staged files found!'
                    );
                    return;
                }

                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'staged-changes');
                
                progress.report({ increment: 40 });
                const title = this.config.persianMode ? '🎵 تحلیل فایل‌های Staged' : '🎵 Staged Files Analysis';
                await this.showAnalysisResult(title, diff, analysis);
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }

    async compareCommits() {
        const commit1 = await vscode.window.showInputBox({
            prompt: this.config.persianMode ? 'کامیت اول (مثل HEAD~1):' : 'First commit (e.g., HEAD~1):',
            value: 'HEAD~1'
        });
        
        if (!commit1) return;

        const commit2 = await vscode.window.showInputBox({
            prompt: this.config.persianMode ? 'کامیت دوم (مثل HEAD):' : 'Second commit (e.g., HEAD):',
            value: 'HEAD'
        });
        
        if (!commit2) return;

        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return;

        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: this.config.persianMode ? `📖 دارم ${commit1} و ${commit2} رو مقایسه میکنم...` : `📖 Comparing ${commit1} and ${commit2}...`,
                cancellable: false
            }, async (progress) => {
                progress.report({ increment: 30 });
                
                const diff = await this.executeGitCommand(`git diff ${commit1} ${commit2}`, workspaceRoot);
                if (!diff.trim()) {
                    vscode.window.showInformationMessage(
                        this.config.persianMode ? 'ℹ️ هیچ تفاوتی پیدا نشد!' : 'ℹ️ No differences found!'
                    );
                    return;
                }

                progress.report({ increment: 30 });
                const analysis = await this.analyzeWithAI(diff, 'commit-comparison');
                
                progress.report({ increment: 40 });
                const title = this.config.persianMode ? `📖 مقایسه ${commit1} و ${commit2}` : `📖 Compare ${commit1} and ${commit2}`;
                await this.showAnalysisResult(title, diff, analysis);
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }

    async analyzeCommitMessage() {
        const commitHash = await vscode.window.showInputBox({
            prompt: this.config.persianMode ? 'کامیت hash (پیش‌فرض: HEAD):' : 'Commit hash (default: HEAD):',
            value: 'HEAD'
        });
        
        if (!commitHash) return;

        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot) return;

        try {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: this.config.persianMode ? '📝 دارم پیام کامیت رو تحلیل میکنم...' : '📝 Analyzing commit message...',
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
                const prompt = this.config.persianMode 
                    ? `پیام کامیت:\n${commitMessage}\n\nتغییرات واقعی:\n${diff}\n\nآیا پیام کامیت با تغییرات مطابقت داره؟ تحلیل کن.`
                    : `Commit message:\n${commitMessage}\n\nActual changes:\n${diff}\n\nDoes the commit message match the changes? Analyze.`;
                
                const analysis = await this.analyzeWithAI(prompt, 'commit-message-analysis');
                
                progress.report({ increment: 25 });
                
                const title = this.config.persianMode ? '📝 تحلیل پیام کامیت' : '📝 Commit Message Analysis';
                await this.showAnalysisResult(title, `Commit: ${commitHash}\nMessage: ${commitMessage}\n\n${diff}`, analysis);
            });
        } catch (error) {
            vscode.window.showErrorMessage(`Error: ${error}`);
        }
    }
}

export function activate(context: vscode.ExtensionContext) {
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
    statusBarItem.tooltip = "VibeTrack - دستیار شخصی برای Vibe Coders";
    statusBarItem.command = 'vibetrack.analyzeChanges';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

export function deactivate() {}