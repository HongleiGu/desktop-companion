import os
from abc import ABC
from dataclasses import dataclass, asdict
from typing import List, Iterator, Optional, Dict, Any

from openai import OpenAI
from dotenv import load_dotenv

from models.message import Message

# Load environment variables from .env
load_dotenv()


# -----------------------------
# Generation configuration
# -----------------------------

@dataclass
class GenerationConfig:
    """
    Provider-agnostic generation parameters.
    Safe defaults for agent-style reasoning.
    """
    temperature: float = 0.2
    top_p: float = 1.0
    max_tokens: Optional[int] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


# -----------------------------
# Base LLM abstraction
# -----------------------------

class LLM(ABC):
    def __init__(
        self,
        model: Optional[str] = None,
        apiKey: Optional[str] = None,
        baseUrl: Optional[str] = None,
        timeout: Optional[int] = None,
        generation_config: Optional[GenerationConfig] = None,
    ):
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("Missing required LLM environment variables")

        self.client = OpenAI(
            api_key=apiKey,
            base_url=baseUrl,
            timeout=timeout,
        )

        self.generation_config = generation_config or GenerationConfig()

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _build_params(self, **overrides: Any) -> Dict[str, Any]:
        """
        Merge default generation config with per-call overrides.
        """
        params = asdict(self.generation_config)
        for k, v in overrides.items():
            if v is not None:
                params[k] = v
        return params

    def _format_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        return [{"role": m.role, "content": m.content} for m in messages]

    # -----------------------------
    # Public API
    # -----------------------------

    def generate(self, messages: List[Message], **kwargs) -> str:
        """
        Synchronous completion.
        kwargs may override generation parameters.
        """
        chat_messages = self._format_messages(messages)
        params = self._build_params(**kwargs)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                stream=False,
                **params,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"❌ Failed to generate response: {e}")
            return ""

    def stream(self, messages: List[Message], **kwargs) -> Iterator[str]:
        """
        Streaming completion (token-by-token).
        """
        chat_messages = self._format_messages(messages)
        params = self._build_params(**kwargs)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                stream=True,
                **params,
            )
            for chunk in response:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except Exception as e:
            print(f"❌ Failed to stream response: {e}")
            return
