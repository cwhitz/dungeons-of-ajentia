import streamlit as st

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
        "Ranger 🏹": True,
        "Wizard 🔮": True,
        "Healer 💊": True,
        "Barbarian 🪓": True,
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
    for i, char in enumerate(st.session_state.party_selection.keys()):
        with cols[i]:
            st.session_state.party_selection[char] = st.toggle(
                char,
                value=st.session_state.party_selection[char]
            )

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
    if prompt := st.chat_input("Issue a command or speak to your party..."):
        # Player message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Placeholder response (later replaced by LangGraph)
        st.session_state.messages.append({
            "role": "assistant",
            "content": "The party acknowledges your command and prepares to act."
        })

        st.rerun()
