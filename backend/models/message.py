from pydantic import BaseModel
from typing import Literal, Optional
from .route import Route

class Message(BaseModel):
    id: str # the frontend needs this to delete messages
    role: Literal["system", "user", "assistant", "tool", "orchestator"]
    content: str
    name: Optional[str] = None # useless, will maybe delete this
    timestamp: str
    protocol: Optional[Route] = None # for format parsing,  