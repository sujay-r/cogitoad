from contextlib import AsyncExitStack

from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from ..config import READER_MCP_SERVER_PARAMS


class MCPClient:
    def __init__(self, server_params: StdioServerParameters) -> None:
        self.server_params = server_params
        self.exit_stack = AsyncExitStack()

    async def _connect_to_server(self, debug: bool = False):
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        self.read_stdio, self.write_stdio = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read_stdio, self.write_stdio)
        )

        await self.session.initialize()

        response = await self.session.list_tools()
        logger.info(f"Connected to MCP server.")
        logger.info(f"List of available tools: {response.tools}")

        if debug:
            await self._close_connection()

    async def _close_connection(self):
        await self.exit_stack.aclose()


if __name__ == "__main__":
    import asyncio

    mcp_client = MCPClient(READER_MCP_SERVER_PARAMS)
    asyncio.run(mcp_client._connect_to_server(debug=True))
