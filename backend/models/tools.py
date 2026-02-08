from pydantic import BaseModel
from typing import Any, Dict, Optional

class ToolRequest(BaseModel):
    name: str
    # description: str
    args: Dict[str, Any]

class ToolResult(BaseModel):
    message: str  # e.g., "Tool executed successfully"
    value: Optional[Any] = None  # The actual returned data / parameters
