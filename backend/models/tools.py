from pydantic import BaseModel
from typing import Any, Dict, Optional

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

class ToolResult(BaseModel):
    message: str  # e.g., "Tool executed successfully"
    value: Optional[Any] = None  # The actual returned data / parameters
