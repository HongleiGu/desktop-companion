from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationConfig:
    temperature: float = 0.2
    top_p: float = 1.0
    max_tokens: Optional[int] = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0