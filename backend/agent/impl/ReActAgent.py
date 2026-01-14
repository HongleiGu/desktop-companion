import json
import re
from typing import Iterator, List, Dict, Any, Optional, Tuple
from models.stream import StreamChunk
from tools.registry import ToolRegistry
from models.message import Message
from llm.base import LLM

"""
some thoughts: to allow streaming in the agent, we assume all tools need some time so we need to "await" them

then the flow is like this:

1. stream output as a text, retrieve the response type at the end, may need to tell the frontend to stop streaming two response as one
2. if a tool is needed, then we wait for the tool to execute completely (we treat frontend tools )
3. stream next one

the the agent requires such functions

1. generate_response: this only do the streaming
2. (maybe optional), wait_for_stream: get the whole content of the stream and parse all the tool related stuff
3. execute_after_response: this is to await for the tool output, still may need to pass the tool output to the frontend for a non-interrupted history

"""

REACT_PROMPT_TEMPLATE = """
Please note, you are an intelligent assistant capable of using external tools.

Available tools:
{tools}

You must respond strictly in the following format:

Thought: Your thought process for analyzing the problem, breaking down tasks, and planning the next step.
Action: The action you decide to take, which must be one of the following formats:
- `{{tool_name}}[{{tool_input}}]`: Call an available tool.
- `Finish[final answer]`: Use this when you believe you have obtained the final answer.
- Once you have gathered enough information to answer the user’s question, you must use `Finish[...]` in the `Action:` field to output the final answer.

You must provide only ONE Thought and ONE Action at a time. After specifying an Action, you must STOP and wait for the Observation. Do not output multiple Thoughts or try to guess the outcome of your actions.

When calling tools:
- You MUST output arguments as STRICT, VALID JSON.
- Use double quotes for all strings.
- Do NOT include any text outside the JSON object.
- You MUST fill in EVERY JSON field

Now, please start helping the user with their question:

History: {history}
"""


class ReActStepAgent:
    def __init__(self, llm: LLM, tool_registry: ToolRegistry):
        self.llm = llm
        self.tool_registry = tool_registry

    def step(
        self,
        messages: list[Message],
    ) -> Iterator[StreamChunk]:
        """
        Streams exactly ONE assistant turn.
        Frontend is responsible for:
        - maintaining history
        - executing tools
        - calling step() again if needed
        """

        prompt = REACT_PROMPT_TEMPLATE.format(
            tools=self._format_tools(),
            history=self._format_history(messages),
        )

        return self.llm.stream([
            Message(
                id="react-step",
                role="user",
                content=prompt,
                timestamp=""
            )
        ])

    def parse_result(self, text: str) -> Dict[str, Any]:
        """
        Called AFTER streaming completes.
        """
        action = None

        for line in text.splitlines():
            line = line.strip()
            if line.startswith("Action:"):
                action = line[len("Action:"):].strip()

        if not action:
            return {
                "type": "error",
                "message": "No Action or Finish found"
            }
        
        if action.startswith("Finish["):
            return {
                "type": "finish",
                "answer": self._parse_finish(action)
            }

        tool, args = self._parse_action(action)
        return {
            "type": "action",
            "tool": tool,
            "args": args
        }

    # ---------------- helpers ---------------- #

    def _parse_action(self, text: str) -> Tuple[str, Dict[str, Any]]:
        name, raw = text.split("[", 1)
        raw = raw.rstrip("]")

        if not raw:
            return name, {}

        try:
            args = json.loads(raw)
        except Exception:
            args = {"input": raw}

        return name, args

    def _parse_finish(self, text: str) -> str:
        return text[len("Finish["):-1].strip()

    def _format_history(self, messages: list[Message]) -> str:
        lines = []
        for m in messages:
            lines.append(f"{m.role.capitalize()}: {m.content}")
        return "\n".join(lines)

    def _format_tools(self) -> str:
        lines = []
        for tool in self.tool_registry.list():
            schema = tool.args_schema
            if callable(schema):
                schema = schema()

            schema_str = json.dumps(schema, indent=2)
            lines.append(
                f"{tool.name}: {tool.description}\n"
                f"Args schema:\n{schema_str}\n"
                f"Execution: {tool.execution}"
            )
        return "\n\n".join(lines)