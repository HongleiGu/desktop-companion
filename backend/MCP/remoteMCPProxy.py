import subprocess
import json
import threading
from typing import List, Dict, Any
from MCP.base import MCP
from tools.base import Tool

class RemoteMCPProxy(MCP):
    def __init__(self, name: str, command: str, args: List[str]):
        self.name = name
        # Start the official MCP server (e.g., 'npx', '-y', '@modelcontextprotocol/server-github')
        self.process = subprocess.Popen(
            [command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self._id_counter = 1
        self.tool_registry = {} # Local cache of remote tool schemas

    def _send_rpc(self, method: str, params: Dict = None) -> Dict:
        """Standard JSON-RPC 2.0 implementation over stdio."""
        request = {
            "jsonrpc": "2.0",
            "id": self._id_counter,
            "method": method,
            "params": params or {}
        }
        self._id_counter += 1
        
        # Write to process stdin
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        # Read from process stdout
        response_line = self.process.stdout.readline()
        return json.loads(response_line)

    def list_tools(self) -> List[Any]:
        """Fetch tools from the remote server and wrap them."""
        # Official MCP method: 'tools/list'
        response = self._send_rpc("tools/list")
        tools_data = response.get("result", {}).get("tools", [])
        
        # We store these to return when UnifiedRegistry asks
        return tools_data 

    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Route the call to the remote process."""
        # Official MCP method: 'tools/call'
        response = self._send_rpc("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        return response.get("result")
    

### Example usage
# # ---------------- Core Setup ---------------- #
# registry = UnifiedRegistry()

# # 1. Register local/standalone tools
# registry.register_standalone(GetTimeTool())

# # 2. Provision and register the Remote GitHub MCP
# # This assumes the environment has Node/NPM installed
# github_mcp = RemoteMCPProxy(
#     name="github",
#     command="npx",
#     args=["-y", "@modelcontextprotocol/server-github"]
# )

# registry.register_mcp(github_mcp)

# # ---------------- Usage ---------------- #
# # The LLM will see "github:create_issue" or "github:search_repositories"
# schemas = registry.schemas
# print(f"Loaded {len(schemas)} tools into the registry.")