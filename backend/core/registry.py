from typing import Dict, List, Optional, Tuple, Any
from MCP.base import MCP
from MCP.remoteMCPProxy import RemoteMCPProxy
from models.spec import *
from tools.namespacedTool import NamespacedTool
from tools.base import Tool

from typing import Dict, List, Optional, Any
from MCP.base import MCP

# -------------------
# Local Authority
# -------------------

# Example: local tools and local MCPs mappings
# These are static and authoritative
LOCAL_TOOLS: Dict[str, type[Tool]] = {}  # key = namespaced id, value = Tool class
LOCAL_MCPS: Dict[str, type[MCP]] = {}    # key = MCP name, value = MCP class

class UnifiedRegistry:
    def __init__(self, spec: UnifiedRegistrySpec | None = None):
        # Maps name "ns:name" to the NamespacedTool wrapper
        self._tools: Dict[str, NamespacedTool] = {}
        # Maps namespace to MCP instance for management
        self._providers: Dict[str, MCP] = {}
        if spec != None:
            self.register_from_spec(spec)

    def register_from_spec(self, spec: UnifiedRegistrySpec):
        self._register_mcps_from_spec(spec.mcps)
        self._register_standalone_tools_from_spec(spec.tools)

    def _register_mcps_from_spec(self, mcps_spec: MCPInstanceConfig):
        for mcp_name, spec in mcps_spec.items():
            if not spec.enabled:
                continue

            # --- Remote MCP ---
            if spec.type == "remote":
                mcp = RemoteMCPProxy(
                    name=mcp_name,
                    command=spec.config["command"],
                    args=spec.config.get("args", []),
                    env=spec.env
                )
            # --- Local MCP ---
            elif spec.type == "local":
                if mcp_name not in LOCAL_MCPS:
                    raise ValueError(f"Unknown local MCP: {mcp_name}")
                mcp_cls = LOCAL_MCPS[mcp_name]
                mcp = mcp_cls(**spec.config)
            else:
                raise ValueError(f"Unknown MCP type for {mcp_name}: {spec.type}")

            self._providers[mcp_name] = mcp

            # --- Auto-register tools from MCP ---
            for tool in mcp.list_tools():
                tool_name = f"{mcp_name}:{tool.name}"
                self._tools[tool_name] = NamespacedTool(
                    name=tool_name,
                    tool=tool
                )


    def _register_standalone_tools_from_spec(self, tools_spec: ToolInstanceConfig):
        for tool_id, spec in tools_spec.items():
            if not spec.enabled:
                continue

            if tool_id not in LOCAL_TOOLS:
                raise ValueError(f"Unknown local tool: {tool_id}")

            tool_cls = LOCAL_TOOLS[tool_id]
            tool = tool_cls(**spec.config)

            self._tools[tool_id] = NamespacedTool(
                name=tool_id,
                tool=tool
            )

    def runtime_view(self) -> Dict[str, Any]:
        """
        Returns a fully resolved view of the registry for the frontend.
        Includes MCP configs, tool configs, and discovered tools with schemas.
        """
        mcps_view = {}
        tools_view = {}

        # MCPs
        for mcp_name, mcp in self._providers.items():
            mcps_view[mcp_name] = {
                "enabled": True,
                "type": getattr(mcp, "type", "remote"),
                "config": getattr(mcp, "config", {}),
                "tools": [
                    {
                        "id": f"{mcp_name}:{tool.name}",
                        "name": tool.name,
                        "description": getattr(tool, "description", ""),
                        "execution": getattr(tool, "execution", "backend"),
                        "schema": getattr(tool, "schema", {}),
                    }
                    for tool in mcp.list_tools()
                ],
            }

        # Standalone / local tools
        for tool_id, entry in self._tools.items():
            # skip tools already included in MCPs
            if ":" in tool_id:
                # if not global
                if tool_id.split(":")[0] != "global":
                    continue
            tool = entry.tool
            tools_view[tool_id] = {
                "enabled": True,
                "id": tool_id,
                "name": tool.name,
                "description": getattr(tool, "description", ""),
                "execution": getattr(tool, "execution", "backend"),
                "schema": getattr(tool, "schema", {}),
            }

        return {
            "mcps": mcps_view,
            "tools": tools_view,
        }


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
    
    def shutdown(self):
        """Clean up all remote providers."""
        print("\nShutting down MCP providers...")
        for name, provider in self._providers.items():
            if hasattr(provider, 'shutdown'):
                provider.shutdown()