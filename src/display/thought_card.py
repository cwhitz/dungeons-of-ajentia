import streamlit as st

def render_thought_card(agent_name: str, thought: str, image_path: str):
    with st.container():
        cols = st.columns([1, 6])

        with cols[0]:
            st.image(image_path, width=140)

        with cols[1]:
            st.markdown(
                f"""
                <div style="
                    background-color: #1f2937;
                    padding: 0.75rem;
                    border-radius: 0.5rem;
                    border-left: 4px solid #8b5cf6;
                ">
                    <strong>💭 {agent_name}</strong><br/>
                    <em>{thought}</em>
                </div>
                """,
                unsafe_allow_html=True,
            )
