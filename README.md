# 🧠 Dungeons of Ajentia (v0.1)
## 🧩 Overview

Dungeons of Ajentia is a web-based multi-agent coordination engine that explores how large language models (LLMs) can reason and collaborate through a graph-based dungeon environment.

It supports:

- Autonomous mode, where AI agents make decisions and coordinate

- Player mode, where a human acts as the party leader

A graph-native world, where all entities (rooms, characters, items) are first-class nodes connected by edges

A transparent, extensible backend powered by LangGraph, Memgraph, and Streamlit

🗺️ World Modeling: Fully Graph-Based
🌐 Graph Schema (Memgraph)

In Ajentia, everything is a node:

Rooms

Characters (player + NPCs)

Items

Enemies

Puzzles

And everything is connected by labeled edges:

"CONTAINS" (room → item/enemy/puzzle)

"CONNECTED" (room ↔ room, with direction/condition)

"HAS_ROLE" (player → character agents)

"CARRIES" or "DEFEATED" (character → item/enemy)

"LEADS" (player → team)

✅ Example Nodes
(:Room {id: "room_1", label: "Dusty Hall"})
(:Item {id: "key_silver", type: "key"})
(:Enemy {id: "skeleton_archer", health: 30})
(:Puzzle {id: "riddle_door", challenge: "speak the password"})
(:Character {id: "ranger", role: "scout", health: 70})

✅ Example Edges
(:Room {id: "room_1"})-[:CONTAINS]->(:Enemy {id: "skeleton_archer"})
(:Room {id: "room_1"})-[:CONNECTED {direction: "north", locked: true}]->(:Room {id: "room_2"})
(:Character {id: "leader"})-[:LEADS]->(:Character {id: "wizard"})

🧠 Agent-Based Characters

Each character is an LLM agent node in LangGraph, with its own memory, persona, and decision function.

🧙 Party of Five
Character	Role	Personality/Skills
Leader	Tactician	Coordinates team actions, player-controlled in player mode
Ranger	Scout	Identifies paths, avoids traps
Wizard	Solver	Deciphers puzzles, casts spells
Healer	Support	Restores health, removes curses
Barbarian	Bruiser	Engages enemies head-on

In Autonomous mode, the Leader is also an LLM agent.
In Player mode, the Leader is the human player, who guides and queries the rest of the party.

🎮 Game Modes
⚔️ Autonomous Mode

LangGraph coordinates all agents

Characters independently:

Perceive environment (via graph query)

Propose actions

Discuss plans

Vote/consensus on next move

All interactions are recorded and visualized in Streamlit

🧑‍✈️ Player Mode (Human-as-Leader)

The player assumes the Leader role via UI

Other characters act as AI agents

Streamlit provides:

Chat interface with party

Dungeon map view

Action menu (e.g. "Ask Wizard to solve puzzle", "Move north")

Player may override or delegate decisions

🧱 Tech Stack
Component	Technology	Purpose
Frontend	Streamlit	UI for player mode and visualization
Backend	LangGraph	Multi-agent coordination graph
Storage	Memgraph	Live dungeon graph DB
LLMs	OpenAI, Gemini, Claude, etc.	Agent reasoning models
