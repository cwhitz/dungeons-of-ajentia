from langgraph.graph import StateGraph, END

from src.agents.leader.leader_agent import LeaderAgent


def build_party_graph(party_selection):
    """
    Build a party graph based on the selected party members.

    Args:
        party_selection (dict): A dictionary where keys are character names and values are dictionaries
                                with 'display' and 'active' status.

    Returns:
        dict: A representation of the party graph.
    """

    leader_agent = LeaderAgent(conversation_id="leader_1")

    def leader_node(state):
        msg = leader_agent.journey(starting_room='Collapsed Entrance Tunnel')
        return {"messages": state["messages"] + [msg]}

    graph = StateGraph(dict)

    graph.add_node("leader", leader_node)

    graph.set_entry_point("leader")
    graph.add_edge("leader", END)

    return graph.compile()
