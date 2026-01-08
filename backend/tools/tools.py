from typing import Callable, Dict

class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def run(self, args: str):
        return self.func(args)


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def describe(self):
        return "\n".join(
            f"{name}: {tool.description}"
            for name, tool in self.tools.items()
        )

    def run(self, name: str, args: str):
        return self.tools[name].run(args)
