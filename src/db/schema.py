from gqlalchemy import Node, Relationship, Field
from typing import Optional
from db.session import db
import uuid

# ==================== NODE CLASSES ====================

class Room(Node):
    """Base class for all rooms in the lair"""
    name: str = Field(unique=True, db=db)
    description: str

class Object(Node):
    """Items and objects that can be found in rooms"""
    name: str
    description: str

class Creature(Node):
    """Base class for all creatures (hostile or neutral)"""
    name: str = Field(index=True, db=db)
    description: str
    health: int = 100
    attack: int = 10
    strikes_first: bool = False
    attack_damage_chance: float = 0.5


# ==================== RELATIONSHIP CLASSES ====================

class ConnectsTo(Relationship, type="CONNECTS_TO"):
    """Links rooms together"""
    passageway: str
    description: str

class Contains(Relationship, type="CONTAINS"):
    """Room contains an object or creature"""

class Protects(Relationship, type="PROTECTS"):
    """A creature protects an object"""
    creature: str
    object: str