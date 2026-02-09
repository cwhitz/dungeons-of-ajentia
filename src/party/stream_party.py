from typing import Any
import streamlit as st
from langchain.messages import AIMessageChunk, AIMessage, ToolMessage
from src.display.thought_card import render_thought_card
from src.display.action_card import render_action_card


AGENT_IMAGES = {
    "leader": "images/leader.jpg",
    "wizard": "images/wizard.jpeg",
    "ranger": "images/ranger.jpeg",
    "healer": "images/healer.jpeg",
}


def stream_party_graph_to_streamlit(party_graph, messages):
    assistant_placeholder = None
    buffer = ""

    for _, stream_mode, data in party_graph.stream(
        {"messages": messages},
        stream_mode=["messages", "updates"],
        subgraphs=True,
        config={'recursion_limit': 100}
    ):
        if stream_mode == "messages":
            token, metadata = data

            # # Start a new chat bubble when agent changes
            # if agent_name != current_agent:
            #     current_agent = agent_name
            #     buffer = ""
            #     assistant_placeholder = st.chat_message("assistant")
            #     assistant_placeholder.markdown(f"**🤖 {agent_name}**")

            # if isinstance(token, AIMessageChunk) and token.text:
            #     buffer += token.text
            #     assistant_placeholder.markdown(buffer)

        elif stream_mode == "updates":
            for _, update in data.items():
                msg = update["messages"][-1]
                if isinstance(msg, AIMessage):
                    if msg.tool_calls is None:
                        continue
                    print(msg.tool_calls)
                    for tool_call in msg.tool_calls:
                        if tool_call['name'] == "announce_thought":
                            
                            thought_content = tool_call['args'].get("thought", "")

                            st.session_state.events.append({
                                "type": "thought",
                                "agent": "leader",
                                "thought": thought_content
                            })

                            render_thought_card(
                                agent_name="leader",
                                thought=thought_content,
                                image_path=AGENT_IMAGES["leader"]
                            )
                        elif tool_call['name'] == "use_passageway":
                            passageway = tool_call['args'].get("passageway", "")
                            render_action_card(
                                agent_name="leader",
                                action=f"👣 Leader uses the passageway: {passageway}"
                            )

                            st.session_state.events.append(
                                {"type": "action", "agent": "leader", "event": f"Used passageway: {passageway}"}
                            )


    return {
        "messages": messages + [{"role": "assistant", "content": buffer}]
    }
