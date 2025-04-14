from contextlib import AsyncExitStack
from typing import Any

from loguru import logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from ..config import READER_MCP_SERVER_PARAMS


class MCPClient:
    def __init__(self, server_params: StdioServerParameters) -> None:
        self.server_params = server_params
        self.exit_stack = AsyncExitStack()

    async def establish_connection(self, debug: bool = False) -> None:
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        self.read_stdio, self.write_stdio = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read_stdio, self.write_stdio)
        )

        await self.session.initialize()

        logger.info(f"Connected to MCP server.")

        if debug:
            await self.close_connection()

    async def close_connection(self):
        await self.exit_stack.aclose()

    async def get_all_tools(self) -> list:
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, *args) -> Any:
        logger.info(f"Calling tool {tool_name} with arguments: {args}")
        result = await self.session.call_tool(tool_name, *args)
        logger.info(f"Tool response: {result.content}")
        return result.content


async def test():
    mcp_client = MCPClient(READER_MCP_SERVER_PARAMS)
    await mcp_client.establish_connection()
    all_tools = await mcp_client.get_all_tools()
    print(all_tools)
    await mcp_client.close_connection()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
