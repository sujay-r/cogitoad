from ollama import AsyncClient


class LLM:
    def __init__(self, model: str) -> None:
        self.client = AsyncClient()
        self.model = model

    async def _call_standalone(self, prompt: str) -> str:
        client_response = await self.client.generate(model=self.model, prompt=prompt)
        return client_response.response


if __name__ == "__main__":
    import asyncio

    from ..config import MODEL_NAME

    llm = LLM(MODEL_NAME)

    print(asyncio.run(llm._call_standalone("What is your name?")))
