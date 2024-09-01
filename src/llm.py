import asyncio
import enum
import openai
from openai.types.chat.chat_completion import ChatCompletion
from pydantic import BaseModel

from src.settings import DEEP_INFRA_API_KEY


class Role(str, enum.Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    role: Role = Role.user
    content: str


class LanguageModel:
    def __init__(
        self, system_prompt: str, model: str = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    ) -> None:
        self.client = openai.AsyncOpenAI(
            api_key=DEEP_INFRA_API_KEY,
            base_url="https://api.deepinfra.com/v1/openai",
        )

        self.model = model

        self.messages: list[Message] = []
        self.messages.append(Message(role=Role.system, content=system_prompt))

    async def chat(self, message: str) -> Message:
        self.messages.append(Message(role=Role.user, content=message))

        chat_completion: ChatCompletion = await self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,  # type:ignore
        )

        if not chat_completion.choices[0].message.content:
            raise Exception("Failed completing chat!")

        bot_message = Message(
            role=Role.assistant, content=chat_completion.choices[0].message.content
        )

        self.messages.append(bot_message)

        return bot_message


if __name__ == "__main__":

    async def main():
        model = "meta-llama/Meta-Llama-3.1-8B-Instruct"
        system_prompt = "You are rimbot, a chatbot assistant to help new player and veteran player about the game Rimworld made by Ludeon Studios"

        rimbot = LanguageModel(model=model, system_prompt=system_prompt)

        result = await rimbot.chat("What is the best gun DPS-wise?")

        print("result:\n", result)
        print("rimbot:\n", rimbot)
        print("rimbot.messages:\n", rimbot.messages)

    asyncio.run(main())
