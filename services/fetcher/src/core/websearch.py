import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from tavily import AsyncTavilyClient

load_dotenv()


class WebSearch:
    def __init__(self, api_key: Optional[str] = None) -> None:
        api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("Tavily API key not provided and not found in environment")
        self.client = AsyncTavilyClient(api_key=api_key)

    async def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search the web using Tavily API.

        Args:
            query (str): The search query.
            num_results (int): The number of results to return.

        Returns:
            dict: Dictionary contating the search results.
        """
        client = AsyncTavilyClient()
        results = await client.search(query, num_results=num_results)
        return results
