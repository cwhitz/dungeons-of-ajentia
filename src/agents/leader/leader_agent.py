
from src.agents.leader.leader_tools import (
    make_find_exit_passageways,
    make_use_passageway,
    make_announce_thought_tool
)

from src.agents.party_member import PartyMember

import dotenv
from langchain.agents import create_agent

dotenv.load_dotenv()

class LeaderAgent(PartyMember):
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.current_room = None
        self.messages = []

        self.find_exit_tool = make_find_exit_passageways(self)
        self.use_passageway_tool = make_use_passageway(self)
        self.announce_thought_tool = make_announce_thought_tool(self)

        with open("src/agents/leader/leader_prompt.txt", "r") as f:
            leader_system_prompt = f.read()

        self.agent = create_agent(
            model="o3-mini",
            tools=[self.find_exit_tool, self.use_passageway_tool, self.announce_thought_tool],
            system_prompt=leader_system_prompt,
        )

    def journey(self, starting_room):
        """
        """

        self.current_room = starting_room
        # append the user's message to the chat history
        self.messages.append({"role": "user", "content": "You enter the dungeon."})

        print(self.messages)
        try:
            messages_with_response = self.agent.invoke(
                input={
                    "messages": [
                        {"role": m["role"], "content": m["content"]}
                        for m in self.messages
                    ]
                },
                config={
                    "metadata": {"conversation_id": self.conversation_id},
                    "tags": [f"conversation:{self.conversation_id}"],
                },
            )
        except Exception as e:
            raise e

        # extract the last message from the bot in the chain
        response = messages_with_response["messages"][-1]

        # add the message from the LLM to the chat history
        self.messages.append(
            {
                "role": "assistant",
                "content": response.content,
                "tokens_used": response.usage_metadata["total_tokens"],
            }
        )

        return response.content