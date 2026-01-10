import json
import requests
from typing import List, Iterator
from .base import LLM
from models.message import Message
from models.stream import StreamChunk

class OllamaLLM(LLM):
    def __init__(
        self,
        model: str,
        host: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        self.model = model
        self.host = host
        self.temperature = temperature

    def generate(self, messages: List[Message]) -> str:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "options": {
                "temperature": self.temperature,
                "num_ctx": 4096,
            },
            "stream": False,
        }

        r = requests.post(f"{self.host}/api/chat", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        payload = {
            "model": self.model,
            "messages": [m.model_dump() for m in messages],
            "options": {
                "temperature": self.temperature,
                "num_ctx": 4096,
            },
            "stream": True,
        }

        try:
            with requests.post(
                f"{self.host}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    event = json.loads(line)
                    text = event.get("message", {}).get("content")
                    if text:
                        yield StreamChunk(type="token", content=text)

            yield StreamChunk(type="done", content=None)

        except Exception as e:
            yield StreamChunk(type="error", content=str(e))
