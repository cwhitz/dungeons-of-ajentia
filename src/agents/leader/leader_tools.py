from langchain_core.tools import Tool
from pydantic import BaseModel
from src.db.session import db
import random

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

def make_search_for_objects(agent):
    def run(x, **kwargs):
        query = """
        MATCH (r:Room {name: $room_name})-[:CONTAINS]->(o:Object)
        RETURN o.name as object, o.description as description
        """
        objects = db.execute_and_fetch(query, {'room_name': agent.current_room})
        if objects:
            return f"You find: {[o['object'] + ': ' + o['description'] for o in objects]}"
        return "No objects found here."
    
    return Tool(name="search_for_objects", func=run, description="Search for objects in the current room. No arguements.", args_schema=None)

class RetrieveObjectInputSchema(BaseModel):
    object_name: str

def make_retrieve_object(agent):
    def run(object_name: str):
        """Retrieve an object if it has no alive creature protecting it."""
        # Check if object exists in the current room
        query = """
        MATCH (r:Room {name: $room_name})-[:CONTAINS]->(o:Object {name: $object_name})
        RETURN o.name as object
        """
        result = list(db.execute_and_fetch(query, {
            'room_name': agent.current_room,
            'object_name': object_name
        }))
        
        if not result:
            return f"No object named '{object_name}' found in the current room."

        # Check if any alive creature protects the object
        protection_query = """
        MATCH (c:Creature)-[:PROTECTS]->(o:Object {name: $object_name})
        WHERE c.health > 0
        RETURN c.name as creature
        """
        protection_result = list(db.execute_and_fetch(protection_query, {
            'object_name': object_name
        }))

        if protection_result:
            print("PLACEHOLDER: Object is protected by:", [p['creature'] for p in protection_result])
            return f"You cannot retrieve '{object_name}' because it is protected by: {[p['creature'] for p in protection_result]}."

        return f"You successfully retrieve '{object_name}'."
    
    return Tool(name="retrieve_object", func=run, description="Retrieve an object from the current room.", args_schema=RetrieveObjectInputSchema)

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

class MeleeBattleInputSchema(BaseModel):
    creature: str

def make_melee_battle_tool(agent):
    def run(creature: str):
        # get creature details from db
        query = """
        MATCH (c:Creature {name: $creature_name})
        RETURN c.name as name, c.description as description, c.health as health, c.attack as attack, c.strikes_first as strikes_first, c.attack_damage_chance as attack_damage_chance
        """
        result = list(db.execute_and_fetch(query, {'creature_name': creature}))
        if not result:
            return f"No creature named '{creature}' found."
        creature = result[0]
        print("Creature stats:", creature)

        if creature['strikes_first']:
            agent.health -= creature['attack']
            print("PLACEHOLDER: Creature strikes first! Agent health after attack:", agent.health)
        # Simulate the melee battle

        print(f"PLACEHOLDER: Melee battle begins between Leader {agent.health} HP and {creature['name']} {creature['health']} HP")
        while agent.health > 0 and creature['health'] > 0:
            # Agent attacks
            if random.random() < agent.attack_damage_chance:  # 80% chance to hit
                creature['health'] -= agent.attack  # Agent's attack damage
                print("PLACEHOLDER: Leader hits! Creature health after attack:", creature['health'])
            else:
                print("PLACEHOLDER: Leader misses!")

            if creature['health'] <= 0:
                #update db to reflect creature's defeat
                query = """
                MATCH (c:Creature {name: $creature_name})
                SET c.health = 0
                """
                db.execute(query, {'creature_name': creature['name']})
                print("PLACEHOLDER: Creature croaks, Leader wins the melee battle!")
                return "You have defeated the creature in melee combat! You can now safely retrieve any objects it was protecting."

            # Creature attacks
            if random.random() < creature['attack_damage_chance']:
                agent.health -= creature['attack']
                print("PLACEHOLDER: Creature hits! Leader health after attack:", agent.health)
            else:
                print("PLACEHOLDER: Creature misses!")

        if agent.health <= 0:
            print("PLACEHOLDER: Leader has been defeated in melee combat.")
            return "You have been defeated in melee combat. Game over."
    
    return Tool(name="melee_battle", func=run, description="Engage in melee combat with a creature.", args_schema=MeleeBattleInputSchema)