from pydantic import BaseModel
from typing import Literal, Optional

class Message(BaseModel):
    id: str # the frontend needs this to delete messages
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None # if tool is needed
    timestamp: str
