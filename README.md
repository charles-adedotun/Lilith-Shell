# Lilith Shell

[![CI](https://github.com/charles-adedotun/Lilith-Shell/actions/workflows/ci.yml/badge.svg)](https://github.com/charles-adedotun/Lilith-Shell/actions/workflows/ci.yml)

MCP server enabling AI assistants to execute terminal commands securely.

## Security Warning

**This tool gives AI agents shell access to your system.** Only use in controlled environments. Review all security settings before deployment. Understand the risks.

## Why This Exists

You want Claude to run shell commands but need security guardrails. Direct shell access is dangerous. No access is limiting. This server provides the middle ground: controlled command execution with timeout protection, error handling, and security validation.

## What It Does

Provides Claude Desktop with secure shell command execution:

- **Command Execution** - Run terminal commands through MCP protocol
- **Timeout Protection** - Commands auto-terminate after configurable duration
- **Security Validation** - Pre-execution command analysis and filtering
- **Error Handling** - Structured error responses with context
- **Cross-Platform** - Works on macOS and Windows (PowerShell + cmd)

## Tech Stack

- Python 3.10+
- FastMCP for Model Context Protocol integration
- Cross-platform subprocess management
- Security-first architecture

## Key Features

### Security Controls

- **Command Allowlisting** - Optional whitelist of permitted commands
- **Dangerous Command Detection** - Blocks destructive operations (rm -rf, format, etc.)
- **Timeout Enforcement** - Kills runaway processes
- **Working Directory Control** - Restricts command execution paths
- **Output Sanitization** - Filters sensitive data from responses

### Execution Features

- **Async Operations** - Non-blocking command execution
- **Stream Output** - Real-time command output streaming
- **Exit Code Handling** - Proper success/failure detection
- **Environment Variables** - Controlled environment passing
- **Shell Selection** - Choose bash, zsh, PowerShell, or cmd

## Quick Start

### Installation - macOS

```bash
pip install lilith-shell
```

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lilith-shell": {
      "command": "python",
      "args": ["-m", "lilith_shell"],
      "env": {
        "LILITH_TIMEOUT": "30",
        "LILITH_SHELL": "bash"
      }
    }
  }
}
```

### Installation - Windows

```powershell
pip install lilith-shell
```

Add to Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lilith-shell": {
      "command": "python",
      "args": ["-m", "lilith_shell"],
      "env": {
        "LILITH_TIMEOUT": "30",
        "LILITH_SHELL": "powershell"
      }
    }
  }
}
```

Restart Claude Desktop.

## Configuration

### Environment Variables

- `LILITH_TIMEOUT` - Command timeout in seconds (default: 30)
- `LILITH_SHELL` - Shell to use (bash/zsh/powershell/cmd)
- `LILITH_ALLOW_LIST` - Comma-separated list of allowed commands
- `LILITH_WORK_DIR` - Restrict execution to specific directory
- `LILITH_MAX_OUTPUT` - Maximum output size in bytes (default: 1MB)

### Security Modes

**Permissive Mode** (default) - Blocks obvious dangerous commands:

```json
{
  "env": {
    "LILITH_MODE": "permissive"
  }
}
```

**Strict Mode** - Only allowlisted commands execute:

```json
{
  "env": {
    "LILITH_MODE": "strict",
    "LILITH_ALLOW_LIST": "git,npm,pip,ls,cat,grep"
  }
}
```

**Lockdown Mode** - Read-only operations only:

```json
{
  "env": {
    "LILITH_MODE": "lockdown"
  }
}
```

## Architecture

```
lilith-shell/
├── core/
│   ├── executor.py           # Command execution engine
│   ├── security.py           # Security validation
│   └── timeout.py            # Timeout management
├── platform/
│   ├── unix.py               # macOS/Linux implementation
│   ├── windows.py            # Windows implementation
│   └── base.py               # Platform interface
├── utils/
│   ├── config.py             # Configuration management
│   ├── logger.py             # Audit logging
│   └── sanitizer.py          # Output sanitization
└── server.py                 # MCP server entry point
```

### Design Principles

1. **Security First** - Every command validated before execution
2. **Fail Safe** - Unknown commands rejected by default in strict mode
3. **Auditability** - All commands logged with timestamp and result
4. **Isolation** - No access to shell history or persistent state
5. **MCP Native** - Clean integration with Model Context Protocol

## Usage

Claude Desktop automatically uses the shell server when command execution is needed. Example interactions:

```
User: "List files in the current directory"
Claude: *executes `ls -la` via Lilith Shell*

User: "Install dependencies"
Claude: *executes `npm install` via Lilith Shell*
```

## Blocked Commands (Permissive Mode)

These commands are blocked by default for safety:

- `rm -rf`, `rm -fr` - Recursive deletion
- `format`, `mkfs` - Filesystem formatting
- `dd` - Low-level disk operations
- `chmod 777` - Dangerous permission changes
- `curl | sh`, `wget | sh` - Pipe to shell execution
- `sudo` without specific allowlist entry
- PowerShell `Remove-Item -Recurse`

## Future Ideas

- **Command Allowlisting UI** - Web interface for managing permitted commands
- **Audit Logging** - Comprehensive command history with playback
- **Linux Support** - Full testing and optimization for Linux distros
- **Sandbox Mode** - Execute commands in isolated containers
- **Command Templates** - Pre-approved command patterns with parameters
- **Rate Limiting** - Prevent command spam/abuse
- **Multi-User Support** - Per-user security profiles
- **Output Streaming UI** - Real-time command output visualization

## Security Best Practices

1. **Use Strict Mode in Production** - Allowlist specific commands
2. **Set Conservative Timeouts** - Prevent resource exhaustion
3. **Monitor Audit Logs** - Review command history regularly
4. **Restrict Working Directory** - Limit filesystem access scope
5. **Review AI Requests** - Understand commands before approval
6. **Use Environment Isolation** - Run in dedicated development environments
7. **Keep Updated** - Security patches applied promptly

## Troubleshooting

### Commands Timing Out

Increase timeout: `"LILITH_TIMEOUT": "60"`

### Permission Denied Errors

Check working directory permissions and command allowlist.

### Commands Not Executing

1. Verify MCP server running: Check Claude Desktop logs
2. Check security mode: May be blocked in strict/lockdown mode
3. Review audit logs: `~/.config/lilith-shell/logs/audit.log`

## Development

```bash
# Clone repository
git clone https://github.com/charles-adedotun/Lilith-Shell.git
cd lilith-shell

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Security audit
bandit -r src/

# Type checking
mypy src/
```

## Contributing

Security issues get priority. Open a private security advisory for vulnerabilities. For features, open an issue first to discuss approach. Keep security validation strict.

## License

MIT

## Acknowledgments

Built for developers who need AI shell access without the chaos. Use responsibly.
