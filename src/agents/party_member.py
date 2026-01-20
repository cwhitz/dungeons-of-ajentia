from abc import ABC

import dotenv
from langchain.agents import create_agent
from pathlib import Path

dotenv.load_dotenv()

class PartyMember(ABC):
    def __init__(self, prompt_path: Path, conversation_id: str, tools: list):
        super().__init__()
        self.conversation_id = conversation_id
        self.current_room = None
        self.messages = []

        with open(prompt_path, 'r') as f:
            agent_system_prompt = f.read()

        self.agent = create_agent(
            model="o3-mini",
            tools=tools,
            system_prompt=agent_system_prompt,
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