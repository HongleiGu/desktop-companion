from typing import List, Iterator
from .llm import LLM, StreamChunk, Message
from openai import OpenAI

class OpenAILLM(LLM):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def generate(self, messages: List[Message]) -> str:
        """
        Non-streaming OpenAI completion.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        """
        Streaming OpenAI completion.
        """
        try:
            stream = self.client.chat.completions.stream(
                model=self.model,
                messages=messages,
            )
            for event in stream:
                delta = event.choices[0].delta
                text = getattr(delta, "content", None)
                if text:
                    yield {"type": "token", "content": text}

            yield {"type": "done", "content": None}

        except Exception as e:
            yield {"type": "error", "content": str(e)}