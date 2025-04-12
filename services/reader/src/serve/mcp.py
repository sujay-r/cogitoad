from mcp.server.fastmcp import FastMCP

mcp = FastMCP("reader")


@mcp.tool()
def hello(name: str):
    """Greets the user by name.
    Args:
        name (str): Name of the user.
    """
    return f"Hello, {name}!"


@mcp.tool()
def bye(name: str):
    """Says goodbye to the user by name.
    Args:
        name (str): Name of the user.
    """
    return f"Bye bye, {name}!"


if __name__ == "__main__":
    mcp.run(transport="stdio")
