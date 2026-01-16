import os
from abc import ABC
from typing import List, Iterator
from openai import OpenAI
from dotenv import load_dotenv

from models.message import Message
from models.stream import StreamChunk

# Load environment variables from .env
load_dotenv()

class LLM(ABC):

    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("env vars are missing")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def generate(self, messages: List[Message]) -> str:
        chat_messages = [{"role": m.role, "content": m.content} for m in messages]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ failed te generate the response: {e}")
            return ""
        
    def stream(self, messages: List[Message]) -> Iterator[str]:
        chat_messages = [{"role": m.role, "content": m.content} for m in messages]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                stream=True,
            )
            for chunk in response:
                yield chunk.choices[0].delta.content or ""
            # the wrapping to StreamChunk should be done in the agent layer
        except Exception as e:
            print(f"❌ failed to stream the LLM: {e}")
            return

    # def stream(self, messages: List[Message], **kwargs) -> Iterator[StreamChunk]:
    #     chat_messages = [{"role": m.role, "content": m.content} for m in messages]
    #     try:
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=chat_messages,
    #             stream=True,
    #         )
    #         for chunk in response:
    #             content = chunk.choices[0].delta.content or ""
    #             yield StreamChunk(type="token",content=content)
    #     except Exception as e:
    #         print(f"❌ failed to stream the LLM: {e}")
    #         return
