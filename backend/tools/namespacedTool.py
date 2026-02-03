from typing import Dict, Any, Literal
from .base import Tool

class NamespacedTool(Tool):
    """
    A tool wrapper that enforces a namespace prefix.
    It satisfies the Tool interface by delegating execution to the inner tool.
    """
    def __init__(self, name: str, tool: Tool):
        self.tool = tool
        
        # Mirror the metadata from the inner tool
        self.name = name  # This is the "new" name (e.g., "mcp:tool")
        self.description = tool.description
        self.execution = tool.execution

    @property
    def schema(self) -> Dict[str, Any]:
        """
        Returns the original schema but with the 'name' field 
        updated to the namespaced fullname.
        """
        # Note: We access self.inner_tool.schema (the property)
        s = self.tool.schema.copy()
        s["name"] = self.name
        return s

    def execute(self, args: Dict[str, Any]) -> Any:
        """
        Delegates execution to the underlying tool logic.
        """
        return self.inner_tool.execute(args)