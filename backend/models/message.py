from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Message(BaseModel):
    text: str = Field(..., description="User input text")
    role: Literal["user", "assistant", "system"] = "user"
    timestamp: datetime = Field(default_factory=datetime.now())
