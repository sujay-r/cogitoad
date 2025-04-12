import pytest
from src.config import MODEL_NAME
from src.core.llm import LLM


@pytest.mark.integration
@pytest.mark.asyncio
async def test_llm_call_standalone_integration():
    """
    Integration test for LLM class that tests actual communication with Ollama.

    This test requires Ollama to be running with the specified model available.
    """
    # Create LLM instance
    llm = LLM(MODEL_NAME)

    # Call the method
    test_prompt = "Return only the word 'TEST'"
    response = await llm._call_standalone(test_prompt)

    # Verify we got some kind of response
    assert isinstance(response, str)
    assert len(response) > 0
