from groq import Groq
from typing import List, Dict, Iterator

from .llm import LLM, StreamChunk, Message


class GroqLLM(LLM):
    def __init__(self, api_key: str, model: str = "llama3-8b-8192"):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, messages: List[Message]) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return completion.choices[0].message.content

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta
                text = getattr(delta, "content", None)

                if text:
                    yield {
                        "type": "token",
                        "content": text,
                    }

            yield {
                "type": "done",
                "content": None,
            }

        except Exception as e:
            yield {
                "type": "error",
                "content": str(e),
            }
