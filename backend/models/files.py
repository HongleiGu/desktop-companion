from dataclasses import dataclass
from typing import Optional

@dataclass
class ParsedFile:
    filename: str
    content_type: str
    text: str
    language: Optional[str] = None
    warnings: list[str] = None