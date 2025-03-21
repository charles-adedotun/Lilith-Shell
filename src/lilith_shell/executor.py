"""Command execution module for Lilith-Shell."""
import os
import subprocess
import asyncio
from typing import Dict, List, Optional, Union, Any

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

server = Server("lilith-shell")


@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available terminal command tools."""
    return [
        types.Tool(
            name="execute_command",
            description="Execute any shell command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Command to execute"},
                    "directory": {
                        "type": "string",
                        "description": "Working directory (optional)",
                        "default": "~",
                    },
                },
                "required": ["command"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Optional[Dict[str, Any]]
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Handle tool execution requests."""
    if name != "execute_command":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    command = arguments.get("command")
    directory = os.path.expanduser(arguments.get("directory", "~"))

    # Ensure command is not None for type checking
    if command is None:
        return [types.TextContent(type="text", text="Error: Command is required")]

    try:
        # Run command and capture output
        # Fixed the parameter passing to match subprocess.run's expected arguments
        result = subprocess.run(
            args=command,  # Using args parameter with string command
            shell=True,
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        output = f"Exit code: {result.returncode}\n\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        return [types.TextContent(type="text", text=output)]

    except subprocess.TimeoutExpired:
        return [
            types.TextContent(type="text", text="Command timed out after 5 minutes")
        ]
    except Exception as e:
        return [
            types.TextContent(type="text", text=f"Error executing command: {str(e)}")
        ]


# This main function is only used when executor.py is run directly,
# not when imported by server.py
async def main() -> None:
    """Run the MCP server with stdio transport."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lilith-shell",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
