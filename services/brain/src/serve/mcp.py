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

    async def _connect_to_server(self):
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        self.read_stdio, self.write_stdio = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read_stdio, self.write_stdio)
        )

        await self.session.initialize()
        logger.info(f"Connected to MCP server.")

    async def _cleanup_resources(self):
        await self.exit_stack.aclose()

    async def __aenter__(self) -> "MCPClient":
        await self._connect_to_server()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self._cleanup_resources()

    async def get_all_tools(self) -> list:
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        logger.info(f"Calling tool {tool_name} with arguments: {kwargs}")
        result = await self.session.call_tool(tool_name, kwargs)
        logger.info(f"Tool response: {result.content}")
        return result.content


async def test():
    async with MCPClient(READER_MCP_SERVER_PARAMS) as mcp_client:
        tool_result = await mcp_client.call_tool(
            tool_name="get_contents_from_document_link",
            url="https://arxiv.org/pdf/1810.08575",
        )
        print(tool_result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test())
