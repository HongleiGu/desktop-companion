from pydantic import BaseModel
from typing import Literal, Optional

from models.route import Route

class StreamChunk(BaseModel):
    type: Literal["token", "done", "error"]
    content: Optional[str]
    protocol: Optional[Route] = None # DIRECT_LLM or REACT, for parsing
    stage: str # e.g. "tool_finding", "llm", and future "thinking", tool_execution is always handled in the frontend