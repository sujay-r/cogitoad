from typing import Optional, TypedDict

import gradio as gr
from loguru import logger

from ..config import FETCHER_MCP_SERVER_PARAMS, MODEL_NAME
from ..core.llm import LLM
from .mcp import MCPClient


class State(TypedDict):
    document_content: Optional[str]
    document_name: Optional[str]
    parsed_document: Optional[str]
    all_tools: Optional[list]


state: State = {
    "document_content": None,
    "document_name": None,
    "parsed_document": None,
    "all_tools": None,
}
llm = LLM(MODEL_NAME)
mcp_client = MCPClient(FETCHER_MCP_SERVER_PARAMS)


async def setup_mcp_client():
    await mcp_client._connect_to_server()
    all_tools = await mcp_client.get_all_tools()
    state["all_tools"] = [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in all_tools
    ]
    logger.info("Loaded tools from MCP server")


async def cleanup_mcp_client():
    await mcp_client._cleanup_resources()


def user(message, chat_history):
    return "", chat_history + [{"role": "user", "content": message}]


async def handle_tool_calls(chat_history, tool_calls):
    logger.info(f"LLM called following tools: {tool_calls}")
    for tool_call in tool_calls:
        tool_response = await mcp_client.call_tool(
            tool_call.function.name, **tool_call.function.arguments
        )
        chat_history.append({"role": "tool", "content": tool_response[0].text})

    logger.info("Calling LLM again with tool outputs..")
    ai_response_to_tool_outputs = await llm.chat(chat_history)
    chat_history.append(
        {"role": "assistant", "content": ai_response_to_tool_outputs.content}
    )
    return chat_history


async def bot(chat_history):
    logger.info("Calling LLM")
    ai_response = await llm.chat(chat_history, state["all_tools"])
    if ai_response.tool_calls:
        chat_history = await handle_tool_calls(chat_history, ai_response.tool_calls)
    else:
        chat_history.append({"role": "assistant", "content": ai_response.content})

    return chat_history


async def stream_bot(chat_history):
    chat_history.append({"role": "assistant", "content": ""})
    async for chunk in llm.stream_chat(chat_history, state["all_tools"]):
        chat_history[-1]["content"] += chunk
        yield chat_history


with gr.Blocks(title="Cogitoad") as gradio_app:
    gradio_app.load(setup_mcp_client)
    gr.Markdown("# Cogitoad")

    chatbot = gr.Chatbot(
        value=[{"role": "system", "content": "Enable deep thinking subroutine"}],
        type="messages",
    )
    msg = gr.Textbox(
        label="Ask a question",
        placeholder="Type your question here...",
        lines=1,
    )

    # Handle chat submission
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )


if __name__ == "__main__":
    gradio_app.launch()
