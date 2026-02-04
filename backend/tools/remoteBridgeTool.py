from typing import Any, Dict

from MCP.base import MCP
from tools.base import Tool


class RemoteBridgeTool(Tool):
    def __init__(self, name: str, description: str, schema: Dict, provider: "MCP"):
        self._name = name
        self._description = description
        self._schema = schema
        self.provider = provider
        self.execution = "backend"

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def schema(self) -> Dict[str, Any]:
        # This returns the JSON schema exactly as the remote server provided it
        return self._schema

    def execute(self, args: Dict[str, Any]) -> Any:
        # Pass the call back to the Proxy
        return self.provider.call_tool(self._name, args)