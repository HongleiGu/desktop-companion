from typing import Any, Dict, List
from ollama import Tool
from MCP.base import MCP
from tools.impl import GetTimeTool
from tools.impl import UpdateCharacterProfileTool
from tools.registry import ToolRegistry

class SimpleMCP(MCP):
    def __init__(self):
        self.name = "SimpleMCP"
        self.description = "A simple MCP implementation."
        self.tool_registry = ToolRegistry()
        self.init_tools()

    def init_tools(self):
        self.tool_registry.register(UpdateCharacterProfileTool())
        self.tool_registry.register(GetTimeTool())

    def get_tool_schemas(self) -> List[dict]:
        # We return the tool metadata in a format LLMs (like Ollama/OpenAI) expect
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.schema
            }
            for tool in self.tool_registry.list()
        ]

    def call_tool(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """
        Executes a tool safely and returns a result or a descriptive error.
        """
        # 1. Look up the tool safely
        tool = self.tool_registry.get(tool_name)
        if not tool:
            return {
                "is_error": True,
                "message": f"Tool '{tool_name}' not found in registry."
            }

        # 2. Execute with a broad try-except to prevent the whole app from crashing
        try:
            # We unpack the dictionary into keyword arguments
            result = tool.execute(**arguments)
            return {
                "is_error": False,
                "data": result
            }
        except TypeError as te:
            # Specifically catch argument mismatch errors
            return {
                "is_error": True,
                "message": f"Invalid arguments for {tool_name}: {str(te)}"
            }
        except Exception as e:
            # Catch all other runtime errors (API timeouts, DB errors, etc.)
            return {
                "is_error": True,
                "message": f"Execution error in {tool_name}: {str(e)}"
            }