from mcp.server.fastmcp import FastMCP

from ..core.ocr import OCR

mcp = FastMCP("reader")

ocr = OCR()


@mcp.tool()
async def get_contents_from_document_link(url: str):
    """Retrieve contents of a document provided the URL to that document.

    Args:
        url (str): URL of the document.

    Returns:
        str: Markdown contents of the document.
    """
    return ocr.get_markdown_from_url(url)


if __name__ == "__main__":
    mcp.run(transport="stdio")
