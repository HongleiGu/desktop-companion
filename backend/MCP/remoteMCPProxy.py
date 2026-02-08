import os
import subprocess
import json
import threading
from typing import Dict, List, Any, Optional
from .base import MCP
from tools.remoteBridgeTool import RemoteBridgeTool

class RemoteMCPProxy(MCP):
    def __init__(self, name: str, command: str, args: List[str], env: Optional[Dict] = None):
        self.name = name
        self._id_counter = 1
        self._tools: List[RemoteBridgeTool] = []
        self._config = {
            "name": name,
            "args": args,
            "command": command,
            "env": env if env is not None else {}
        }
        
        # Merge provided env with system env (needed for PATH, etc.)
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        # Start the MCP server process
        self.process = subprocess.Popen(
            [command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=full_env,
            text=True,
            bufsize=1,  # Line buffered
            shell=True # for windows
        )

        # Start a thread to monitor stderr so it doesn't block and we see logs
        threading.Thread(target=self._log_stderr, daemon=True).start()

        # Phase 1: Auto-Discovery Handshake
        self._discover_tools()

    @property
    def config(self):
        return self._config

    def _log_stderr(self):
        """Pipes the remote server's logs to our console for debugging."""
        for line in self.process.stderr:
            print(f"[{self.name} LOG]: {line.strip()}")

    def _send_rpc(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Standard JSON-RPC 2.0 over stdio."""
        request = {
            "jsonrpc": "2.0",
            "id": self._id_counter,
            "method": method,
            "params": params or {}
        }
        self._id_counter += 1
        
        # Write to server
        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()
        
        # Read response
        line = self.process.stdout.readline()
        if not line:
            return {"error": "No response from MCP server"}
        return json.loads(line)

    def _discover_tools(self):
        """Initial handshake to populate our tool list."""
        response = self._send_rpc("tools/list")
        tools_data = response.get("result", {}).get("tools", [])
        
        self._tools = [
            RemoteBridgeTool(
                name=t["name"],
                description=t["description"],
                schema=t["inputSchema"],
                provider=self
            ) for t in tools_data
        ]

    def list_tools(self) -> List[RemoteBridgeTool]:
        return self._tools

    def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """The generic execution bridge."""
        response = self._send_rpc("tools/call", {
            "name": tool_name,
            "arguments": args
        })
        return response.get("result")
    
    def get_tool_schemas(self) -> List[dict]:
        """
        Implementation of the abstract method.
        Iterates through discovered tools and returns their JSON schemas.
        Note for remote MCPs, this is only valid after _discover_tools
        """
        # We use the list of RemoteBridgeTool objects we populated during discovery
        return [tool.schema for tool in self._tools]