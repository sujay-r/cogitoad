from mcp import StdioServerParameters

MODEL_NAME = "cogito:8b"
READER_MCP_SERVER_PARAMS = StdioServerParameters(
    command="python",
    args=["-m", "src.serve.mcp"],
    cwd="/home/sujay/Code/cogitoad/services/reader/",
    env=None,
)
