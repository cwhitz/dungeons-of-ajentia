import streamlit as st

def render_action_card(agent_name: str, action: str):
    with st.container():
        cols = st.columns([1, 6])

        # left spacer to align with thought cards
        with cols[0]:
            st.markdown("")

        with cols[1]:
            st.markdown(
                f"""
                <div style="
                    background-color: #111827;
                    padding: 0.75rem;
                    border-radius: 0.5rem;
                    border-left: 4px solid #10b981;
                ">
                    <strong>⚔️ {agent_name} acts</strong><br/>
                    <span>{action}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

