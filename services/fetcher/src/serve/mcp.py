from mcp.server.fastmcp import FastMCP

from ..config import NUM_WEB_SEARCH_RESULTS
from ..core.ocr import OCR
from ..core.websearch import WebSearch

mcp = FastMCP("reader")

ocr = OCR()
search_client = WebSearch()


@mcp.tool()
async def get_contents_from_document_link(url: str):
    """Retrieve contents of a document provided the URL to that document.

    Args:
        url (str): URL of the document.

    Returns:
        str: Markdown contents of the document.
    """
    return await ocr.get_markdown_from_url(url)


@mcp.tool()
async def get_contents_from_document_bytes(filename: str, file_bytes: bytes):
    """Retrieve contents of a document provided the bytes of that document.

    Args:
        filename (str): Name of the file.
        file_bytes (bytes): Bytes of the document.

    Returns:
        str: Markdown contents of the document.
    """
    return await ocr.get_markdown_from_file_bytes(filename, file_bytes)


@mcp.tool()
async def search_web(query: str):
    """Search the web.

    Args:
        query (str): The search query.

    Returns:
        dict: Dictionary containing the search results.
    """
    return await search_client.search(query, num_results=NUM_WEB_SEARCH_RESULTS)


if __name__ == "__main__":
    mcp.run(transport="stdio")
