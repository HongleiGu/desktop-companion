from pydantic import BaseModel
from typing import Any, Dict

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
