from abc import ABC, abstractmethod
from typing import Dict, List

from tools.registry import ToolRegistry
from tools.base import Tool

class MCP(ABC):
    name: str
    description: str
    tool_registry: ToolRegistry

    @property
    @abstractmethod
    def config(self):
        # a config is required for all MCPs
        pass

    @abstractmethod
    def get_tool_schemas(self) -> List[dict]:
        """
        1. PROVIDE SCHEMAS: 
        Returns JSON-serializable definitions for the LLM to understand 
        what tools are available and how to call them.
        """
        raise NotImplementedError()

    @abstractmethod
    def call_tool(self, tool_name: str, arguments: dict) -> any:
        """
        2. FIND & EXECUTE:
        The entry point for the agent to actually trigger a tool. 
        This looks up the tool in the registry and runs it.
        """
        raise NotImplementedError()
        
    def list_tools(self) -> List[Tool]:
        # return all the tools
        return self.tool_registry.list_tools()
        