import os
import json
from db.session import db


from service.level import load_level, build_level
from agents.leader.leader_agent import LeaderAgent

if __name__ == "__main__":
    data = load_level.load_level_from_json("./levels/data")

    entry_point = build_level.build_level_in_memgraph(db=db, data=data)

    

