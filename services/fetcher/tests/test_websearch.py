import pytest
from dotenv import load_dotenv
from src.core.websearch import WebSearch

load_dotenv()


@pytest.fixture
def search_client():
    return WebSearch()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search(search_client):
    query = "Who is Leo Messi?"
    result = await search_client.search(query, 1)
    expected_output = {
        "title": "Lionel Messi - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Lionel_Messi",
        "content": 'Lionel Andrés "Leo" Messi [note 1] (Spanish pronunciation: [ljoˈnel anˈdɾes ˈmesi] ⓘ; born 24 June 1987) is an Argentine professional footballer who plays as a forward for and captains both Major League Soccer club Inter Miami and the Argentina national team.',
        "score": 0.9442644,
        "raw_content": None,
    }
    assert result["results"][0] == expected_output
