# Pandora's Shell

⚠️ **IMPORTANT SECURITY WARNING**: This MCP server grants AI assistants unrestricted ability to execute terminal commands on your system. **Only use in controlled environments like virtual machines (VMs) or development systems you can afford to rebuild.**

## About

An MCP server that empowers AI assistants to execute terminal commands on your system. Due to the unrestricted access this provides, it's crucial to use this software responsibly and be fully aware of the security risks involved.

**Note**: This server is compatible with any AI assistant that supports the Model Context Protocol (MCP). The provided configuration and setup instructions are specifically tailored for Claude Desktop, which offers comprehensive support for all MCP features.

## Features

- Execute any shell command with full system access
- Capture command output (stdout/stderr)
- Set working directory
- Handle command timeouts

## API

### Tools

- **execute_command**
  - Execute any shell command and return its output
  - **Inputs**:
    - `command` (string): Command to execute
    - `directory` (string, optional): Working directory
  - **Returns**:
    - Command exit code
    - Standard output
    - Standard error
  - **Features**:
    - 5-minute timeout
    - Working directory support
    - Error handling

## Installation

### Prerequisites

- **Claude Desktop** with an active Claude Pro/Enterprise subscription
  - Download from: [Claude AI](https://claude.ai/download)
- **Python 3.10** or higher
- **Git**
- **uv** (required for package management)

### Windows Installation

1. Install Prerequisites:
   ```powershell
   # Using winget:
   winget install python git
   ```

2. Install uv (run PowerShell as administrator):
   ```powershell
   irm https://astral.sh/uv/install.ps1 | iex
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$HOME\.local\bin", "User")
   ```

3. Clone and set up the project:
   ```cmd
   git clone https://github.com/Zelaron/Pandoras-Shell.git
   cd Pandoras-Shell
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```cmd
   uv pip install mcp
   pip install -e .
   ```

### macOS Installation

1. Install Prerequisites:
   ```bash
   brew install python git uv
   ```

2. Clone and set up the project:
   ```bash
   git clone https://github.com/Zelaron/Pandoras-Shell.git
   cd Pandoras-Shell
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   uv pip install mcp
   pip install -e .
   ```

## Configuration

### Windows

Locate the correct configuration directory - try these paths in order:

1. `%APPDATA%\Claude\` (typically `C:\Users\[YourUsername]\AppData\Roaming\Claude\`)
2. `%LOCALAPPDATA%\AnthropicClaude\` (typically `C:\Users\[YourUsername]\AppData\Local\AnthropicClaude\`)

Create or edit `claude_desktop_config.json` in the correct directory:

```json
{
  "mcpServers": {
    "pandoras-shell": {
      "command": "python",
      "args": [
        "C:\\path\\to\\cloned\\Pandoras-Shell\\src\\pandoras_shell\\executor.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\cloned\\Pandoras-Shell\\src"
      }
    }
  }
}
```

#### Important Notes for Windows:

- Use forward slashes (`/`) in paths, not backslashes (`\`)
- Replace `[YourUsername]` with your actual Windows username
- File must be named exactly `claude_desktop_config.json`
- If both possible config locations exist, try each until successful

### macOS

Create or edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pandoras-shell": {
      "command": "python",
      "args": [
        "/path/to/cloned/Pandoras-Shell/src/pandoras_shell/executor.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/cloned/Pandoras-Shell/src"
      }
    }
  }
}
```

#### Important Notes for macOS:

- Replace `[YourUsername]` with your actual username
- You can use `$HOME` instead of `/Users/[YourUsername]` if preferred
- File must be named exactly `claude_desktop_config.json`

### After Configuration

1. Restart Claude Desktop completely (quit/exit, not just close the window).
2. Click the 🔌 icon to verify the server appears in the "Installed MCP Servers" list.
3. If the server doesn't appear, check Claude's logs:
   - **Windows**: `%APPDATA%\Claude\Logs\mcp*.log` or `%LOCALAPPDATA%\AnthropicClaude\Logs\mcp*.log`
   - **macOS**: `~/Library/Logs/Claude/mcp*.log`

## Security Considerations

This server executes commands with your user privileges. **Take these precautions:**

- Use **only** in VMs or disposable development environments.
- **Never** use on production systems or machines with sensitive data.
- Consider implementing command restrictions if needed.
- Monitor system access and activity.
- Keep backups of important data.

**Disclaimer**: The developers are not responsible for any damages or losses resulting from the use of this software. Use it at your own risk.

## Troubleshooting

If you encounter issues:

1. **Check logs:**
   - **Windows**: `%APPDATA%\Claude\Logs\mcp*.log` or `%LOCALAPPDATA%\AnthropicClaude\Logs\mcp*.log`
   - **macOS**: `~/Library/Logs/Claude/mcp*.log`

2. **Verify installation:**
   - Ensure `uv` is properly installed and in your PATH.
   - Check that `mcp` package is installed: `pip show mcp`.
   - Verify Python version is 3.10 or higher.

3. **Configuration issues:**
   - Double-check all paths in `claude_desktop_config.json`.
   - Verify JSON syntax is valid.
   - Ensure proper path separators for your OS.
   - Confirm config file is in the correct location.

4. **Environment issues:**
   - Make sure `virtualenv` is activated if using one.
   - Verify `PYTHONPATH` is set correctly.
   - Check file permissions.

5. **Test server manually:**
   ```bash
   python src/pandoras_shell/executor.py
   ```

## Testing

After setup, try these commands in Claude Desktop:

```text
Can you run 'pwd' and tell me what directory we're in?
```

or

```text
Can you list the files in my home directory? Which of them are larger than 200 MB?
```
