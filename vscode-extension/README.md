# Metapod VSCode Extension

This directory contains the VSCode extension for integrating Metapod as a selectable agent mode within VSCode.

## Features

- **Agent Mode Integration**: Metapod appears as a selectable agent in VSCode
- **Autonomous Refactoring**: Start refactoring with a simple command
- **Progress Tracking**: Real-time progress visualization
- **Interactive Mode**: Choose between full autonomy, interactive, or guided modes
- **Research Integration**: Research best practices directly from VSCode
- **Status Monitoring**: Visual progress indicators and status updates

## Installation

### Option 1: Install from VSCode Marketplace (Coming Soon)

1. Open VSCode
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Metapod Agent"
4. Click Install

### Option 2: Install from Source

1. Clone the Metapod repository
2. Navigate to the `vscode-extension` directory
3. Run `npm install`
4. Run `npm run compile`
5. Press F5 to open a new VSCode window with the extension loaded

## Setup

1. **Install Metapod Core**: The extension requires the Metapod Python agent

   ```bash
   git clone https://github.com/NJRca/Metapod.git
   cd Metapod
   bash setup.sh
   ```

2. **Configure Extension**: Open VSCode settings and configure:
   - `metapod.pythonPath`: Path to Python executable
   - `metapod.agentPath`: Path to Metapod installation
   - `metapod.autonomyLevel`: Preferred autonomy level
   - `metapod.stackPreference`: Your technology stack

## Usage

### Activating Metapod

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Metapod: Activate"
3. The Metapod icon will appear in your status bar

### Starting Refactoring

1. Right-click on a project folder or file
2. Select "Metapod: Start Autonomous Refactoring"
3. Choose your autonomy level:
   - **🤖 Full Autonomy**: Metapod makes all decisions
   - **🤝 Interactive Mode**: Metapod asks for approval
   - **👁️ Guided Mode**: Metapod shows plans only

### Monitoring Progress

- Check the status bar for current phase
- Open the Metapod Progress panel in Explorer
- View detailed output in the Metapod output channel

## Commands

| Command                                 | Description                           |
| --------------------------------------- | ------------------------------------- |
| `Metapod: Activate`                     | Activate the Metapod agent            |
| `Metapod: Start Autonomous Refactoring` | Begin refactoring the current project |
| `Metapod: Research Best Practices`      | Research topics for best practices    |
| `Metapod: Show Refactoring Status`      | Display current progress              |
| `Metapod: Configure Agent Settings`     | Open configuration options            |

## Configuration

```json
{
  "metapod.pythonPath": "python3",
  "metapod.agentPath": "/path/to/metapod",
  "metapod.autonomyLevel": "interactive",
  "metapod.riskTolerance": "medium",
  "metapod.stackPreference": "auto-detect",
  "metapod.enableResearch": true,
  "metapod.showProgressNotifications": true
}
```

## Development

### Building

```bash
npm install
npm run compile
```

### Testing

```bash
npm test
```

### Packaging

```bash
npm install -g vsce
vsce package
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the extension
5. Submit a pull request

## License

MIT License - see [LICENSE](../LICENSE) file for details.
