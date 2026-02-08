from typing import Any, Dict, Optional
from pydantic import BaseModel


class MCPInstanceConfig(BaseModel):
    enabled: bool = True
    type: Optional[str] = "remote"  # "remote" or "local"
    config: Dict[str, Any]           # runtime config (command, path, args)
    # configSchema: 
    env: Optional[Dict[str, str]] = None  # secrets/env vars

class ToolInstanceConfig(BaseModel):
    enabled: bool = True
    config: Dict[str, Any] = {}  # tool-specific runtime params

class UnifiedRegistrySpec(BaseModel):
    mcps: Dict[str, MCPInstanceConfig] = {}
    tools: Dict[str, ToolInstanceConfig] = {}