"""Server module for Lilith-Shell."""
import asyncio

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
import mcp.server.stdio


# Re-export the server instance and handlers from executor.py
from lilith_shell.executor import server


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
