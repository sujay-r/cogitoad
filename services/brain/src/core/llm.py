from typing import AsyncGenerator, Optional

from ollama import AsyncClient

from ..config import MODEL_TEMPERATURE


class LLM:
    def __init__(self, model: str) -> None:
        self.client = AsyncClient()
        self.model = model

    async def call_standalone(self, prompt: str) -> str:
        client_response = await self.client.generate(model=self.model, prompt=prompt)
        return client_response.response

    async def chat(self, messages: list, tools: Optional[list] = None):
        client_response = await self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options={"temperature": MODEL_TEMPERATURE},
        )
        return client_response.message

    async def stream_chat(
        self, messages: list, tools: Optional[list] = None
    ) -> AsyncGenerator[str | None, None]:
        client_response = await self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            stream=True,
            options={"temperature": MODEL_TEMPERATURE},
        )
        async for part in client_response:
            yield part.message.content
