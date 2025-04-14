import pytest
from src.config import MODEL_NAME
from src.core.llm import LLM


@pytest.fixture
def llm():
    return LLM(MODEL_NAME)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_llm_call_standalone(llm):
    """
    Integration test for LLM class that tests actual communication with Ollama.

    This test requires Ollama to be running with the specified model available.
    """

    # Call the method
    test_prompt = "Return only the word 'TEST'"
    response = await llm.call_standalone(test_prompt)

    # Verify we got some kind of response
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_llm_call_chat(llm):
    """
    Integration test for LLM class that tests actual communication with Ollama.

    This test requires Ollama to be running with the specified model available.
    """

    # Call the method
    test_messages = [{"role": "user", "content": 'Response with "TEST"'}]
    response = await llm.chat(test_messages)

    # Verify we got some kind of response
    assert isinstance(response, str)
    assert len(response) > 0
