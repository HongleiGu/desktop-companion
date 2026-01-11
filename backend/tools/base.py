from abc import ABC, abstractmethod
from typing import Dict, Any, Literal

class Tool(ABC):
    """
    Base interface for all tools.
    Tools are deterministic capabilities callable by agents.
    """

    name: str
    description: str

    # the execution is used to determine whether the tool
    # should be executed on the frontend or backend
    # for example, some UI changes need frontend involvement
    execution: Literal["backend", "frontend"]

    @abstractmethod
    def args_schema(self) -> Dict[str, Any]:
        """
        Returns a JSON Schema describing expected arguments.
        Must be valid JSON Schema draft-07 compatible.
        """
        pass

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> Any:
        """
        Execute the tool with validated arguments.
        """
        pass
