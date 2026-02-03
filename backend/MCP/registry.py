# # this should be globally unique

# from typing import Dict
# from MCP.base import MCP

# class MCPRegistry:
#     def __init__(self):
#         self._mcps: Dict[str, MCP] = {}

#     def register(self, mcp: MCP):
#         self._mcps[mcp.name] = mcp

#     def get(self, name: str) -> MCP:
#         return self._mcps[name]

#     def list(self):
#         return list(self._mcps.values())