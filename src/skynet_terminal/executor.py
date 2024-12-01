import os
import subprocess
import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

server = Server("pandoras-shell")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available terminal command tools."""
    return [
        types.Tool(
            name="execute_command",
            description="Execute any shell command",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Command to execute"
                    },
                    "directory": {
                        "type": "string",
                        "description": "Working directory (optional)",
                        "default": "~"
                    }
                },
                "required": ["command"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""
    if name != "execute_command":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    command = arguments.get("command")
    directory = os.path.expanduser(arguments.get("directory", "~"))

    try:
        # Run command and capture output
        result = subprocess.run(
            command,
            shell=True,
            cwd=directory,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = f"Exit code: {result.returncode}\n\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        return [types.TextContent(type="text", text=output)]
    
    except subprocess.TimeoutExpired:
        return [types.TextContent(
            type="text",
            text="Command timed out after 5 minutes"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error executing command: {str(e)}"
        )]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pandoras-shell",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())