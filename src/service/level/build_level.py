from gqlalchemy import Memgraph
from db.schema import Room, Object, Creature, ConnectsTo, Contains, Protects
from db.session import db


def drop_all_constraints(db: Memgraph) -> None:
    """Drop all existing constraints and indexes"""
    print("Dropping all constraints and indexes...")
    try:
        # Drop all constraints
        result = list(db.execute_and_fetch("SHOW CONSTRAINT INFO"))
        for row in result:
            constraint_name = row.get('constraint name')
            if constraint_name:
                try:
                    db.execute(f"DROP CONSTRAINT {constraint_name}")
                    print(f"  Dropped constraint: {constraint_name}")
                except Exception as e:
                    print(f"  Could not drop {constraint_name}: {e}")
        
        # Drop all indexes
        index_result = list(db.execute_and_fetch("SHOW INDEX INFO"))
        for row in index_result:
            index_name = row.get('index name')
            if index_name:
                try:
                    db.execute(f"DROP INDEX {index_name}")
                    print(f"  Dropped index: {index_name}")
                except Exception as e:
                    print(f"  Could not drop {index_name}: {e}")
                    
    except Exception as e:
        print(f"  Note: {e}")
    print("Constraints and indexes cleared.")


def clear_database(db: Memgraph) -> None:
    """Clear all nodes and relationships from the database"""
    print("Clearing database...")
    db.execute("MATCH (n) DETACH DELETE n")
    print("Database cleared.")


def build_level_from_json(level: dict):
    """
    Builds the level in memgraph.
    """

    data = level.get("data", {})
    nodes = data.get("nodes", {})
    relationships = data.get("relationships", {})

    # Dictionaries for easy lookup by name
    rooms_by_name = {}
    objects_by_name = {}
    creatures_by_name = {}

    print("\n=== Creating Rooms ===")
    for r in nodes.get("rooms", []):
        room = Room(
            name=r["name"],
            description=r["description"]
        )
        room.save(db)
        rooms_by_name[room.name] = room
        print(f"  Created Room: {room.name}")

    print("\n=== Creating Objects ===")
    for o in nodes.get("objects", []):
        obj = Object(
            name=o["name"],
            description=o["description"]
        )
        obj.save(db)
        objects_by_name[obj.name] = obj
        print(f"  Created Object: {obj.name}")

    print("\n=== Creating Creatures ===")
    for c in nodes.get("creatures", []):
        creature = Creature(
            name=c["name"],
            description=c["description"],
            health=c.get("health", 100),
            attack=c.get("attack", 10),
            strikes_first=c.get("strikes_first", False),
            attack_damage_chance=c.get("attack_damage_chance", 0.5)
        )
        creature.save(db)
        creatures_by_name[creature.name] = creature
        print(f"  Created Creature: {creature.name}")

    print("\n=== Creating CONNECTS_TO relationships ===")
    for rel in relationships.get("connects_to", []):
        from_room = rooms_by_name[rel["from_room"]]
        to_room = rooms_by_name[rel["to_room"]]

        conn = ConnectsTo(
            _start_node_id=from_room._id,
            _end_node_id=to_room._id,
            passageway=rel["passageway"],
            description=rel["description"]
        )
        conn.save(db)
        print(f"  {from_room.name} -> {to_room.name}")

    print("\n=== Creating CONTAINS relationships ===")
    for rel in relationships.get("contains", []):
        room = rooms_by_name[rel["room"]]

        # Determine whether it's an object or creature
        if rel.get("object"):
            target = objects_by_name[rel["object"]]
        elif rel.get("creature"):
            target = creatures_by_name[rel["creature"]]
        else:
            raise ValueError("CONTAINS must specify either object or creature")

        contains = Contains(
            _start_node_id=room._id,
            _end_node_id=target._id
        )
        contains.save(db)

        print(f"  {room.name} CONTAINS {target.name}")

    print("\n === Creating PROTECTS relationships ===")
    for rel in relationships.get("protects", []):
        creature = creatures_by_name[rel["creature"]]
        obj = objects_by_name[rel["object"]]

        protects = Protects(
            _start_node_id=creature._id,
            _end_node_id=obj._id,
            creature=creature.name,
            object=obj.name
        )
        protects.save(db)
        

    print("\n=== Level Loaded Successfully ===")


def build_level_in_memgraph(db: Memgraph, data: dict) -> None:
    """Main function to import all data from JSON into Memgraph"""
    
    # Drop constraints and clear existing data
    drop_all_constraints(db)
    clear_database(db)
    
    # Create nodes
    build_level_from_json(data)
    
    print("\n✓ Import completed successfully!")
