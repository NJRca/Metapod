import { spawn } from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';

interface MetapodTask {
    id: string;
    description: string;
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    notes?: string;
}

interface MetapodSession {
    id: string;
    workspaceFolder: string;
    request: string;
    status: 'active' | 'completed' | 'failed';
    tasks: MetapodTask[];
    startTime: Date;
}

export class MetapodAgent {
    private outputChannel: vscode.OutputChannel;
    private statusBarItem: vscode.StatusBarItem;
    private progressProvider: MetapodProgressProvider;
    private currentSession: MetapodSession | null = null;
    private context: vscode.ExtensionContext;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.outputChannel = vscode.window.createOutputChannel('Metapod Agent');
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.progressProvider = new MetapodProgressProvider();
        
        this.setupStatusBar();
        this.registerCommands();
        this.registerViews();
    }

    private setupStatusBar() {
        this.statusBarItem.text = "$(robot) Metapod: Ready";
        this.statusBarItem.command = 'metapod.showProgress';
        this.statusBarItem.tooltip = 'Metapod Autonomous Refactoring Agent';
        this.statusBarItem.show();
    }

    private registerCommands() {
        const commands = [
            vscode.commands.registerCommand('metapod.activate', () => this.activate()),
            vscode.commands.registerCommand('metapod.refactor', (uri?) => this.startRefactoring(uri)),
            vscode.commands.registerCommand('metapod.research', () => this.research()),
            vscode.commands.registerCommand('metapod.status', () => this.showStatus()),
            vscode.commands.registerCommand('metapod.configure', () => this.configure()),
            vscode.commands.registerCommand('metapod.showProgress', () => this.showProgress())
        ];

        commands.forEach(cmd => this.context.subscriptions.push(cmd));
    }

    private registerViews() {
        vscode.window.registerTreeDataProvider('metapodProgress', this.progressProvider);
    }

    async activate() {
        const config = vscode.workspace.getConfiguration('metapod');
        
        // Check if Metapod is installed
        const agentPath = config.get<string>('agentPath') || await this.findMetapodInstallation();
        
        if (!agentPath) {
            const install = await vscode.window.showWarningMessage(
                'Metapod agent not found. Would you like to install it?',
                'Install', 'Configure Path', 'Cancel'
            );
            
            if (install === 'Install') {
                await this.installMetapod();
            } else if (install === 'Configure Path') {
                await this.configure();
            }
            return;
        }

        // Set context to show Metapod UI elements
        vscode.commands.executeCommand('setContext', 'metapod.active', true);
        
        this.statusBarItem.text = "$(robot) Metapod: Active";
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.prominentBackground');
        
        this.outputChannel.appendLine('Metapod agent activated');
        this.outputChannel.show();
        
        vscode.window.showInformationMessage('Metapod autonomous refactoring agent is now active!');
    }

    async startRefactoring(uri?: vscode.Uri) {
        const workspaceFolder = this.getWorkspaceFolder(uri);
        if (!workspaceFolder) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }

        // Get refactoring request from user
        const request = await vscode.window.showInputBox({
            prompt: 'Enter your refactoring request',
            placeholder: 'e.g., "Implement hexagonal architecture", "Add error handling", "Harden for production"',
            value: 'Begin autonomous refactoring'
        });

        if (!request) {
            return;
        }

        // Show autonomy level options
        const autonomyLevel = await vscode.window.showQuickPick([
            {
                label: '🤖 Full Autonomy',
                description: 'Let Metapod make all decisions and implement changes',
                detail: 'Recommended for experienced teams',
                value: 'full'
            },
            {
                label: '🤝 Interactive Mode',
                description: 'Metapod asks for approval before major changes',
                detail: 'Recommended for most projects',
                value: 'interactive'
            },
            {
                label: '👁️ Guided Mode',
                description: 'Metapod shows plans but requires manual execution',
                detail: 'Recommended for learning',
                value: 'guided'
            }
        ], {
            placeHolder: 'Select autonomy level'
        });

        if (!autonomyLevel) {
            return;
        }

        // Create new session
        this.currentSession = {
            id: Date.now().toString(),
            workspaceFolder: workspaceFolder.fsPath,
            request,
            status: 'active',
            tasks: this.getDefaultTasks(),
            startTime: new Date()
        };

        // Update UI
        this.statusBarItem.text = "$(loading~spin) Metapod: Refactoring...";
        this.progressProvider.refresh(this.currentSession);

        // Start refactoring process
        await this.executeMetapod(workspaceFolder.fsPath, request, autonomyLevel.value);
    }

    private async executeMetapod(projectPath: string, request: string, autonomyLevel: string) {
        const config = vscode.workspace.getConfiguration('metapod');
        const pythonPath = config.get<string>('pythonPath', 'python3');
        const agentPath = config.get<string>('agentPath') || await this.findMetapodInstallation();

        if (!agentPath) {
            vscode.window.showErrorMessage('Metapod installation not found');
            return;
        }

        const cliPath = path.join(agentPath, 'cli.py');
        const args = [cliPath, projectPath];

        if (autonomyLevel === 'interactive') {
            args.push('--interactive');
        } else if (autonomyLevel === 'guided') {
            args.push('--dry-run');
        } else {
            args.push(request);
        }

        this.outputChannel.appendLine(`Executing: ${pythonPath} ${args.join(' ')}`);
        
        const process = spawn(pythonPath, args, {
            cwd: agentPath,
            stdio: ['pipe', 'pipe', 'pipe']
        });

        process.stdout?.on('data', (data) => {
            const output = data.toString();
            this.outputChannel.append(output);
            this.parseMetapodOutput(output);
        });

        process.stderr?.on('data', (data) => {
            this.outputChannel.append(`Error: ${data.toString()}`);
        });

        process.on('close', (code) => {
            if (code === 0) {
                this.onRefactoringComplete();
            } else {
                this.onRefactoringFailed(code);
            }
        });

        // Show progress with ability to cancel
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Metapod is refactoring your project...",
            cancellable: true
        }, async (progress, token) => {
            token.onCancellationRequested(() => {
                process.kill();
                this.outputChannel.appendLine('Refactoring cancelled by user');
            });

            return new Promise<void>((resolve) => {
                process.on('close', () => resolve());
            });
        });
    }

    private parseMetapodOutput(output: string) {
        // Parse Metapod output to update progress
        if (output.includes('✅') && this.currentSession) {
            // Find completed tasks and update status
            const lines = output.split('\n');
            lines.forEach(line => {
                if (line.includes('✅')) {
                    const taskDesc = line.replace('✅', '').trim();
                    const task = this.currentSession!.tasks.find(t => t.description.includes(taskDesc));
                    if (task) {
                        task.status = 'completed';
                    }
                }
            });
            this.progressProvider.refresh(this.currentSession);
        }

        // Update status bar with current phase
        if (output.includes('Phase')) {
            const phaseMatch = output.match(/Phase \d+: (.*)/);
            if (phaseMatch) {
                this.statusBarItem.text = `$(loading~spin) Metapod: ${phaseMatch[1]}`;
            }
        }
    }

    private onRefactoringComplete() {
        if (this.currentSession) {
            this.currentSession.status = 'completed';
            this.progressProvider.refresh(this.currentSession);
        }

        this.statusBarItem.text = "$(check) Metapod: Complete";
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.prominentBackground');

        vscode.window.showInformationMessage(
            'Metapod refactoring completed successfully!',
            'View Output', 'Show Changes'
        ).then(action => {
            if (action === 'View Output') {
                this.outputChannel.show();
            } else if (action === 'Show Changes') {
                vscode.commands.executeCommand('workbench.view.scm');
            }
        });
    }

    private onRefactoringFailed(exitCode: number | null) {
        if (this.currentSession) {
            this.currentSession.status = 'failed';
            this.progressProvider.refresh(this.currentSession);
        }

        this.statusBarItem.text = "$(error) Metapod: Failed";
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');

        vscode.window.showErrorMessage(
            `Metapod refactoring failed (exit code: ${exitCode})`,
            'View Output', 'Retry'
        ).then(action => {
            if (action === 'View Output') {
                this.outputChannel.show();
            } else if (action === 'Retry') {
                this.startRefactoring();
            }
        });
    }

    async research() {
        const topic = await vscode.window.showInputBox({
            prompt: 'What topic would you like Metapod to research?',
            placeholder: 'e.g., "latest fastapi patterns", "error handling best practices"'
        });

        if (!topic) {
            return;
        }

        this.outputChannel.appendLine(`Researching: ${topic}`);
        this.outputChannel.show();

        // Execute research command
        const config = vscode.workspace.getConfiguration('metapod');
        const pythonPath = config.get<string>('pythonPath', 'python3');
        const agentPath = config.get<string>('agentPath') || await this.findMetapodInstallation();

        if (agentPath) {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (workspaceFolder) {
                const cliPath = path.join(agentPath, 'cli.py');
                const process = spawn(pythonPath, [cliPath, workspaceFolder.uri.fsPath, '--interactive'], {
                    cwd: agentPath
                });

                // Send research command
                process.stdin?.write(`research ${topic}\n`);
                process.stdin?.write('exit\n');

                process.stdout?.on('data', (data) => {
                    this.outputChannel.append(data.toString());
                });
            }
        }
    }

    showStatus() {
        if (this.currentSession) {
            const completedTasks = this.currentSession.tasks.filter(t => t.status === 'completed').length;
            const totalTasks = this.currentSession.tasks.length;
            const progress = Math.round((completedTasks / totalTasks) * 100);

            vscode.window.showInformationMessage(
                `Metapod Progress: ${progress}% (${completedTasks}/${totalTasks} tasks completed)`,
                'View Details'
            ).then(action => {
                if (action === 'View Details') {
                    this.showProgress();
                }
            });
        } else {
            vscode.window.showInformationMessage('No active Metapod session');
        }
    }

    showProgress() {
        vscode.commands.executeCommand('workbench.view.explorer');
        vscode.commands.executeCommand('metapodProgress.focus');
    }

    async configure() {
        const action = await vscode.window.showQuickPick([
            'Set Python Path',
            'Set Metapod Installation Path',
            'Configure Autonomy Level',
            'Configure Stack Preference',
            'Open Settings'
        ], {
            placeHolder: 'What would you like to configure?'
        });

        const config = vscode.workspace.getConfiguration('metapod');

        switch (action) {
            case 'Set Python Path':
                const pythonPath = await vscode.window.showInputBox({
                    prompt: 'Enter path to Python executable',
                    value: config.get<string>('pythonPath', 'python3')
                });
                if (pythonPath) {
                    await config.update('pythonPath', pythonPath, vscode.ConfigurationTarget.Global);
                }
                break;

            case 'Set Metapod Installation Path':
                const agentPath = await vscode.window.showInputBox({
                    prompt: 'Enter path to Metapod installation directory',
                    value: config.get<string>('agentPath', '')
                });
                if (agentPath) {
                    await config.update('agentPath', agentPath, vscode.ConfigurationTarget.Global);
                }
                break;

            case 'Open Settings':
                vscode.commands.executeCommand('workbench.action.openSettings', 'metapod');
                break;
        }
    }

    private async findMetapodInstallation(): Promise<string | null> {
        // Try to find Metapod in common locations
        const possiblePaths = [
            path.join(__dirname, '..', '..'),  // Relative to extension
            path.join(require.os.homedir(), 'metapod'),
            '/usr/local/metapod',
            '/opt/metapod'
        ];

        for (const metapodPath of possiblePaths) {
            try {
                const cliPath = path.join(metapodPath, 'cli.py');
                if (require.fs.existsSync(cliPath)) {
                    return metapodPath;
                }
            } catch (error) {
                // Continue searching
            }
        }

        return null;
    }

    private async installMetapod() {
        const installPath = await vscode.window.showInputBox({
            prompt: 'Enter installation directory for Metapod',
            value: path.join(require.os.homedir(), 'metapod')
        });

        if (!installPath) {
            return;
        }

        vscode.window.showInformationMessage(
            'Installing Metapod... This may take a few minutes.',
            'View Progress'
        ).then(action => {
            if (action === 'View Progress') {
                this.outputChannel.show();
            }
        });

        // Clone and setup Metapod
        const terminal = vscode.window.createTerminal('Metapod Installation');
        terminal.sendText(`git clone https://github.com/NJRca/Metapod.git "${installPath}"`);
        terminal.sendText(`cd "${installPath}" && bash setup.sh`);
        terminal.show();

        // Update configuration
        const config = vscode.workspace.getConfiguration('metapod');
        await config.update('agentPath', installPath, vscode.ConfigurationTarget.Global);
    }

    private getWorkspaceFolder(uri?: vscode.Uri): vscode.WorkspaceFolder | undefined {
        if (uri) {
            return vscode.workspace.getWorkspaceFolder(uri);
        }
        return vscode.workspace.workspaceFolders?.[0];
    }

    private getDefaultTasks(): MetapodTask[] {
        return [
            { id: 'scope', description: 'Scope & acceptance criteria confirmed', status: 'pending' },
            { id: 'baseline', description: 'Baseline tests/telemetry in place', status: 'pending' },
            { id: 'plan', description: 'Plan approved (small reversible cuts)', status: 'pending' },
            { id: 'implement', description: 'Implement step 1 (inputs validated, errors standardized)', status: 'pending' },
            { id: 'test', description: 'Tests green (unit/contract/property)', status: 'pending' },
            { id: 'observability', description: 'Observability updated (logs/metrics/traces)', status: 'pending' },
            { id: 'pr', description: 'PR opened with checklist & research notes', status: 'pending' },
            { id: 'rollout', description: 'Rollout plan & rollback documented', status: 'pending' }
        ];
    }

    dispose() {
        this.outputChannel.dispose();
        this.statusBarItem.dispose();
    }
}

class MetapodProgressProvider implements vscode.TreeDataProvider<MetapodTask> {
    private _onDidChangeTreeData: vscode.EventEmitter<MetapodTask | undefined | null | void> = new vscode.EventEmitter<MetapodTask | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<MetapodTask | undefined | null | void> = this._onDidChangeTreeData.event;

    private session: MetapodSession | null = null;

    refresh(session?: MetapodSession): void {
        if (session) {
            this.session = session;
        }
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: MetapodTask): vscode.TreeItem {
        const item = new vscode.TreeItem(element.description, vscode.TreeItemCollapsibleState.None);
        
        switch (element.status) {
            case 'completed':
                item.iconPath = new vscode.ThemeIcon('check', new vscode.ThemeColor('charts.green'));
                break;
            case 'in_progress':
                item.iconPath = new vscode.ThemeIcon('loading~spin', new vscode.ThemeColor('charts.yellow'));
                break;
            case 'failed':
                item.iconPath = new vscode.ThemeIcon('error', new vscode.ThemeColor('charts.red'));
                break;
            default:
                item.iconPath = new vscode.ThemeIcon('circle-outline');
        }

        item.tooltip = element.notes || element.description;
        
        return item;
    }

    getChildren(element?: MetapodTask): Thenable<MetapodTask[]> {
        if (!this.session) {
            return Promise.resolve([]);
        }

        return Promise.resolve(this.session.tasks);
    }
}

export function activate(context: vscode.ExtensionContext) {
    const agent = new MetapodAgent(context);
    context.subscriptions.push(agent);
}

export function deactivate() {}
