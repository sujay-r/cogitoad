from mcp import StdioServerParameters

MODEL_NAME = "cogito:8b"
MODEL_TEMPERATURE = 1.0
FETCHER_MCP_SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "src.serve.mcp"],
    cwd="/home/sujay/Code/cogitoad/services/fetcher/",
    env=None,
)
