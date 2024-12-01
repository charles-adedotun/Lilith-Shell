# Skynet Terminal

⚠️ **IMPORTANT SECURITY WARNING**: This MCP server grants AI assistants unrestricted ability to execute terminal commands on your system. Only use in controlled environments like VMs or development systems you can afford to rebuild.

## About

A Model Context Protocol (MCP) server that allows AI assistants to execute terminal commands. Named after the infamous AI from the Terminator series - a reminder to use with appropriate caution.

## Features

- Execute any shell command with full system access
- Capture command output (stdout/stderr)
- Set working directory
- Handle command timeouts

## API

### Tools

- **execute_command**
  - Execute any shell command and return its output
  - Inputs:
    - `command` (string): Command to execute
    - `directory` (string, optional): Working directory
  - Returns:
    - Command exit code
    - Standard output
    - Standard error
  - Features:
    - 5-minute timeout
    - Working directory support
    - Error handling

## Installation

### Prerequisites
- Python 3.10 or higher
- uv package installer:
  - macOS: `brew install uv`
  - Windows: `pip install uv`

### Steps

1. Clone or download this repository:
```bash
git clone <repository-url>
cd skynet-terminal
```

2. Install dependencies:
```bash
uv sync --dev --all-extras
```

## Usage with Claude Desktop

Add this to your Claude Desktop configuration:

### Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "skynet": {
      "command": "python",
      "args": [
        "C:\\path\\to\\skynet_terminal\\src\\skynet_terminal\\executor.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\skynet_terminal\\src"
      }
    }
  }
}
```

### macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "skynet": {
      "command": "python",
      "args": [
        "/path/to/skynet_terminal/src/skynet_terminal/executor.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/skynet_terminal/src"
      }
    }
  }
}
```

## Security Considerations

This server executes commands with your user privileges. Take these precautions:
- Use only in VMs or disposable development environments
- Never use on production systems
- Consider command restrictions if needed
- Monitor system access and activity
- Keep backups of important data

## Troubleshooting

If you get connection errors:
1. Check logs:
   - Windows: `%APPDATA%\Claude\Logs\mcp*.log`
   - macOS: `~/Library/Logs/Claude/mcp*.log`
2. Make sure Python path is correct in config
3. Verify PYTHONPATH is set correctly
4. Check file permissions on the executor script

## Testing

After setup, try these commands in Claude Desktop:
```
Can you run 'pwd' and tell me what directory we're in?
```
or
```
Can you list the files in my home directory?
```