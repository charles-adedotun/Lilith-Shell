# Lilith Shell

Experimental MCP server that exposes local shell command execution to an AI assistant.

## Current Status

This repository should be treated as a prototype, not as a secure shell server.

The current implementation exposes one MCP tool, `execute_command`, that runs a caller-provided command string through `subprocess.run(..., shell=True)`. It has a fixed five-minute timeout, captures stdout and stderr, and accepts an optional working directory. It does not currently implement the security controls previously described in this README.

Recommended profile action: archive or unpin this repository until the security model is rebuilt and tested.

## Security Warning

Do not run this against a host, account, or directory that contains credentials, production data, private source code, SSH keys, cloud tokens, or other sensitive material.

Known gaps in the current code:

- No command allowlist or denylist enforcement
- No strict, permissive, or lockdown modes
- No working-directory boundary enforcement
- No environment filtering
- No output sanitization
- No audit log
- No shell selection via configuration
- No streaming output
- No Windows-specific execution path
- `shell=True` is used with untrusted tool input

These gaps make the project unsuitable for production use and risky even in a normal developer workstation.

## What Works Today

The MCP server registers one tool:

- `execute_command`
  - input: `command` string
  - optional input: `directory` string, defaulting to `~`
  - behavior: executes the command in the requested directory and returns exit code, stdout, and stderr

## What Was De-Scoped

The previous README claimed support for command allowlisting, dangerous command detection, configurable modes, output sanitization, audit logging, working-directory confinement, cross-platform shell selection, and streaming output. Those capabilities are not present in the current source tree.

## Minimal Patch Plan Before Re-Publishing

Before this should be presented as a security-oriented MCP server:

1. Replace `shell=True` string execution with argv-based execution.
2. Add a required strict mode by default, with explicit command allowlists.
3. Canonicalize and enforce a configured workspace root before every command.
4. Build tests for command parsing, blocked commands, path traversal, symlink escapes, timeout behavior, and output limits.
5. Redact common secret patterns from returned output.
6. Add bounded output handling so large commands cannot exhaust memory or flood MCP responses.
7. Add auditable command logs with timestamps, cwd, exit code, and block reason.
8. Document exactly which shells, platforms, and threat boundaries are supported.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
