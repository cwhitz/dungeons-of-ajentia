from langchain_core.tools import Tool
from pydantic import BaseModel
from src.db.session import db

def make_find_exit_passageways(agent):
    def run(x, **kwargs):
        query = """
        MATCH (r:Room {name: $room_name})-[c:CONNECTS_TO]->(connected:Room)
        RETURN connected.name as room, c.passageway as passageway
        """
        exits = db.execute_and_fetch(query, {'room_name': agent.current_room})
        if exits:
            return f"You see exits: {[e['passageway'] for e in exits]}"
        return "No exits here."
    
    return Tool(name="find_exit_passageways", func=run, description="Find exits. No arguements.", args_schema=None)

class UsePassagewayInputSchema(BaseModel):
    passageway: str

def make_use_passageway(agent):
    def run(passageway: str):
        query = """
        MATCH (r:Room {name: $current_room})-[c:CONNECTS_TO]->(connected:Room)
        WHERE c.passageway = $passageway
        RETURN connected.name as room, connected.description as description
        """
        result = list(db.execute_and_fetch(query, {
            "current_room": agent.current_room,
            "passageway": passageway
        }))
        
        if result:
            agent.current_room = result[0]["room"]
            return f"Moved to {agent.current_room}: {result[0]['description']}"
        
        return f"No passageway '{passageway}' from '{agent.current_room}'."
    
    return Tool(name="use_passageway", func=run, description="Use a passageway.", args_schema=UsePassagewayInputSchema)


class ThoughtToolInputSchema(BaseModel):
    thought: str

def make_announce_thought_tool(agent):
    def run(thought: str):
        agent.messages.append({
            "role": "assistant",
            "content": thought
        })
        return "Thoughts announced."
    
    return Tool(name="announce_thought", func=run, description="Announce your thoughts to your party members.", args_schema=ThoughtToolInputSchema)
