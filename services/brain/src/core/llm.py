from typing import AsyncGenerator

from ollama import AsyncClient


class LLM:
    def __init__(self, model: str) -> None:
        self.client = AsyncClient()
        self.model = model

    async def call_standalone(self, prompt: str) -> str:
        client_response = await self.client.generate(model=self.model, prompt=prompt)
        return client_response.response

    async def chat(self, messages: list) -> str:
        client_response = await self.client.chat(model=self.model, messages=messages)
        response_content = client_response.message.content
        assert (
            response_content is not None
        ), f"LLM chat response is None. Input messages: {messages}"

        return response_content

    async def stream_chat(self, messages: list) -> AsyncGenerator[str | None, None]:
        client_response = await self.client.chat(
            model=self.model, messages=messages, stream=True
        )
        async for part in client_response:
            yield part.message.content
