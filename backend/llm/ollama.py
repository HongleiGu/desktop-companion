import json
import requests
from typing import List, Iterator
from .llm import LLM, StreamChunk, Message


class OllamaLLM(LLM):
    def __init__(
        self,
        model: str = "llama3.1",
        host: str = "http://localhost:11434",
        temperature: float = 0.8,
    ):
        self.model = model
        self.host = host
        self.temperature = temperature

    def generate(self, messages: List[Message]) -> str:
        """
        Non-streaming completion.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {
                "temperature": self.temperature,
                "num_ctx": 4096,
            },
            "stream": False,
        }

        response = requests.post(
            f"{self.host}/api/chat",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        payload = {
            "model": self.model,
            "messages": messages,
            "options": {"temperature": self.temperature, "num_ctx": 4096},
            "stream": True,
        }

        try:
            with requests.post(
                f"{self.host}/api/chat",
                json=payload,
                stream=True,
                timeout=120,
            ) as response:
                response.raise_for_status()
                # Each line is a JSON object representing a token
                for line in response.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        text = event.get("message", {}).get("content")
                        if text:
                            # Yield each incremental token
                            yield {"type": "token", "content": text}
                    except Exception as e:
                        yield {"type": "error", "content": str(e)}

            # Done signal
            yield {"type": "done", "content": None}

        except Exception as e:
            yield {"type": "error", "content": str(e)}