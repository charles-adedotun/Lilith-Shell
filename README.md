# Skynet Terminal

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

- **Claude Desktop** with an active Claude Pro/Enterprise subscription (currently the only supported MCP client)
  - Download from: https://claude.ai/download
- **Python 3.10** or higher
- **Git** (required to clone the repository)
- **Optional**: Virtual environment tool (recommended for isolating dependencies)

### Steps

1. **Clone or download this repository:**

   ```bash
   git clone https://github.com/Zelaron/Skynet-Terminal.git
   cd Skynet-Terminal
   ```

2. **(Optional) Create and activate a virtual environment:**

   It's recommended to use a virtual environment to isolate the project's dependencies.

   **Windows:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the project and its dependencies:**

   The following command installs the project in "editable" mode, allowing you to modify the code without reinstalling:

   ```bash
   pip install -e .
   ```

   If you encounter any issues with the installation, ensure you have the latest version of `pip`:

   ```bash
   python -m pip install --upgrade pip
   ```

   Then try installing again:

   ```bash
   pip install -e .
   ```

4. **(Optional) Verify the installation:**

   ```bash
   pip show mcp
   ```

   You should see information about the `mcp` package installed.

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
        "C:\\path\\to\\Skynet-Terminal\\src\\skynet_terminal\\executor.py"
      ],
      "env": {
        "PYTHONPATH": "C:\\path\\to\\Skynet-Terminal\\src"
      }
    }
  }
}
```

- **Note:**
  - Replace `C:\\path\\to\\Skynet-Terminal` with the actual path to the `Skynet-Terminal` directory on your system.
  - Ensure you use double backslashes (`\\`) in Windows file paths.
  - If you **did not** create a virtual environment:
    - Ensure that `python` is available in your system's PATH.
    - The `command` is simply `"python"`.
  - If you **did** create a virtual environment:
    - Point `command` to the Python executable within your virtual environment:

      ```json
      "command": "C:\\path\\to\\Skynet-Terminal\\venv\\Scripts\\python.exe",
      ```

### macOS

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skynet": {
      "command": "python3",
      "args": [
        "/path/to/Skynet-Terminal/src/skynet_terminal/executor.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/Skynet-Terminal/src"
      }
    }
  }
}
```

- **Note:**
  - Replace `/path/to/Skynet-Terminal` with the actual path to the `Skynet-Terminal` directory on your system.
  - If you **did not** create a virtual environment:
    - Ensure that `python3` is available in your system's PATH.
    - The `command` is simply `"python3"`.
  - If you **did** create a virtual environment:
    - Point `command` to the Python executable within your virtual environment:

      ```json
      "command": "/path/to/Skynet-Terminal/venv/bin/python",
      ```

## Security Considerations

This server executes commands with your user privileges. **Take these precautions:**

- Use **only** in VMs or disposable development environments.
- **Never** use on production systems or machines with sensitive data.
- Consider implementing command restrictions if needed.
- Monitor system access and activity.
- Keep backups of important data.
- **Disclaimer**: The developers are not responsible for any damages or losses resulting from the use of this software. Use it at your own risk.

## Troubleshooting

If you get connection errors:

1. **Check logs:**

   - **Windows:** `%APPDATA%\Claude\Logs\mcp*.log`
   - **macOS:** `~/Library/Logs/Claude/mcp*.log`

2. **Ensure paths are correct in the configuration:**

   - Verify that the `command` and `args` paths in `claude_desktop_config.json` are accurate.
   - Ensure `PYTHONPATH` is set correctly.

3. **Verify Python and dependencies:**

   - Make sure you have Python 3.10 or higher installed.
   - Ensure all dependencies are installed in your environment.

4. **Check file permissions:**

   - Ensure that the `executor.py` script has execute permissions.

5. **Test the server manually:**

   - Run the server directly to check for errors:

     ```bash
     python src/skynet_terminal/executor.py
     ```

## Testing

After setup, try these commands in Claude Desktop:

```
Can you run 'pwd' and tell me what directory we're in?
```

or

```
Can you list the files in my home directory? Which of them are larger than 200 MB?
```
