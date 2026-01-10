from pydantic import BaseModel
from typing import Literal, Optional

class StreamChunk(BaseModel):
    type: Literal["token", "done", "error"]
    content: Optional[str]
