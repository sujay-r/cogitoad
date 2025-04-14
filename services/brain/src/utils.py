from serve.mcp import MCPClient

from .config import FETCHER_MCP_SERVER_PARAMS


async def setup_mcp_client() -> MCPClient:
    client = MCPClient(FETCHER_MCP_SERVER_PARAMS)
    await client._connect_to_server()
    return client


async def cleanup_mcp_client(client: MCPClient) -> None:
    await client._cleanup_resources()
