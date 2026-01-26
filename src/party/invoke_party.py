from typing import Any

from langchain.messages import AIMessage, AnyMessage, AIMessageChunk, ToolMessage

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")

def stream_party_graph(party_graph, messages: list[dict[str, Any]]):
    current_agent = None
    for _, stream_mode, data in party_graph.stream(
        {"messages": messages},
        stream_mode=["messages", "updates"],
        subgraphs=True,  
    ):
        if stream_mode == "messages":
            token, metadata = data
            if agent_name := metadata.get("lc_agent_name"):  
                if agent_name != current_agent:  
                    print(f"🤖 {agent_name}: ")  
                    current_agent = agent_name  
            if isinstance(token, AIMessage):
                _render_message_chunk(token)
        if stream_mode == "updates":
            for source, update in data.items():
                if source in ("model", "tools"):
                    _render_completed_message(update["messages"][-1])