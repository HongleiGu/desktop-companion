from typing import Dict, List, Optional, Tuple, Any
from MCP.base import MCP
from tools import NamespacedTool
from tools.base import Tool

from typing import Dict, List, Optional, Any
from MCP.base import MCP

class UnifiedRegistry:
    def __init__(self):
        # Maps name "ns:name" to the NamespacedTool wrapper
        self._tools: Dict[str, NamespacedTool] = {}
        # Maps namespace to MCP instance for management
        self._providers: Dict[str, MCP] = {}

    def register_standalone(self, tool: Tool, namespace: str = "global"):
        """Registers a local tool under a default or specific namespace."""
        name = f"{namespace}:{tool.name}"
        self._tools[name] = NamespacedTool(name=name, tool=tool)

    def register_mcp(self, mcp: MCP):
        """Imports tools from an MCP and namespaces them."""
        self._providers[mcp.name] = mcp
        for tool in mcp.list_tools():
            name = f"{mcp.name}:{tool.name}"
            self._tools[name] = NamespacedTool(name=name, tool=tool)

    def get(self, name: str) -> Optional[Tool]:
        """Returns the raw Tool instance for execution."""
        entry = self._tools.get(name)
        return entry.tool if entry else None

    def list_tools(self) -> List[NamespacedTool]:
        """Returns all wrapped tools."""
        return list(self._tools.values())

    @property
    def schemas(self) -> List[Dict[str, Any]]:
        """Returns all namespaced schemas for the Agent."""
        return [nt.schema for nt in self._tools.values()]

    def get_relevant_tools(self, query: str):
        """Future home for Tool-RAG and Dynamic Installation."""
        raise NotImplementedError("Dynamic provisioning via RAG not implemented.")