import streamlit as st
from src.party.build_party import build_party_graph
from src.party.invoke_party import stream_party_graph
from src.party.stream_party import stream_party_graph_to_streamlit

st.set_page_config(page_title="Dungeons of Ajentia", layout="wide")

# -------------------------
# Session state init
# -------------------------
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "party_selection" not in st.session_state:
    st.session_state.party_selection = {
        "ranger": {'display': 'Ranger 🏹', 'active': True},
        "wizard": {'display': 'Wizard 🔮', 'active': True},
        "healer": {'display': 'Healer 💊', 'active': True},
        "barbarian": {'display': 'Barbarian 🪓', 'active': True},
    }

# ============================================================
# SETUP SCREEN
# ============================================================
if not st.session_state.game_started:
    st.title("🏰 Dungeons of Ajentia")
    st.header("🎮 Game Setup")

    # Mode selection
    mode = st.radio(
        "Select Game Mode:",
        options=[
            "Player-led (You are the Leader)",
            "Autonomous (LLMs control all agents)"
        ],
        horizontal=True,
    )

        # Mode selection
    level = st.radio(
        "Select Level:",
        options=[
            "Dwarven Depths",
            "Vampiric Vaults",
            "Great Goblin Grotto",
            "Wild Western Woodland"
        ],
        horizontal=True,
    )

    st.markdown("---")

    # Party selection
    st.subheader("🧙 Select Your Party")

    cols = st.columns(5)
    for i, (char_key, char_info) in enumerate(st.session_state.party_selection.items()):
        with cols[i]:
            st.session_state.party_selection[char_key]['active'] = st.toggle(
                char_info['display'],
                value=char_info['active'],
                disabled=True)

    st.markdown("---")

    # Start game
    if st.button("🚀 Start Game"):
        st.session_state.game_started = True
        st.session_state.mode = mode
        st.session_state.level = level
        st.session_state.messages.append({
            "role": "system",
            "content": "The party enters the dungeon. The air is cold and damp..."
        })
        st.rerun()

# ============================================================
# GAME / CHAT SCREEN
# ============================================================
else:
    # run party initialization
    party_graph = build_party_graph(
        st.session_state.party_selection
    )

    st.title("🗡️ Dungeons of Ajentia")

    # Sidebar (optional, easy to expand later)
    with st.sidebar:
        st.header("🧙 Party")
        for char, active in st.session_state.party_selection.items():
            if active:
                st.write(f"• {char}")

        st.markdown("---")
        st.write(f"**Mode:** {st.session_state.mode}")
        st.markdown("---")
        st.write(f"**Dungeon:** {st.session_state.level}")
        st.write("Entry hall")

        if st.button("🔄 Restart Game"):
            st.session_state.clear()
            st.rerun()

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if st.session_state.mode == "Autonomous (LLMs control all agents)":
        if st.button("▶️ Start the Adventure!"):
            result = stream_party_graph_to_streamlit(
                party_graph,
                st.session_state.messages
            )

            st.session_state.messages = result["messages"]
            st.rerun()
    elif prompt := st.chat_input("Issue a command or speak to your party..."):
        # Player message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        result = party_graph.invoke({
            "messages": st.session_state.messages, "config": {'recursion_limit': 60}
        })

        st.session_state.messages = result["messages"]
        st.rerun()
    else:
        st.info("Type a message and press Enter to continue your adventure!")
