from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from .message import Message
from .tools import ToolDefinition

class ChatRequest(BaseModel):
    provider: str = Field(..., example="ollama")
    model: str = Field(..., example="llama3.1")
    messages: List[Message]

    stream: bool = False
    temperature: float = 0.7

    tools: Optional[List[ToolDefinition]] = None
    metadata: Optional[Dict] = None
