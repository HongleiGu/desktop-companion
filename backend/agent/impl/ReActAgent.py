import json
import re
from typing import Iterator, List, Dict, Any, Optional, Tuple
from core.registry import UnifiedRegistry
from models.stream import StreamChunk
from tools.registry import ToolRegistry
from models.message import Message
from models import Route
from llm.base import LLM
from ..utils import tokens_to_stream_chunks

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
You are an intelligent assistant that can reason step-by-step and use tools.

TOOLS (tool names may include namespaces):
{tools}

IMPORTANT:
- Some tool names include a namespace and colon, for example: github:search_repositories
- A namespaced tool name MUST be treated as ONE complete tool name
- Do NOT split, shorten, or modify tool names

You MUST follow this output format exactly:

Thought: Brief reasoning about what to do next.
Action: One of the following (and only one):
- tool_name[tool_input]
- Finish[final answer]

Rules:
- Output exactly ONE Thought and ONE Action.
- After an Action, STOP. Wait for the Observation.
- Do NOT output multiple Thoughts or Actions.
- Do NOT explain or predict tool results.
- Use Finish[...] ONLY when the final answer is ready.

Tool usage rules:
- tool_input MUST be valid JSON.
- Use double quotes for all strings.
- Include ALL required JSON fields.
- Do NOT include any text outside the JSON.

EXAMPLE (format must be followed exactly):

    Thought: I need to use a tool to get the required information.
    Action: example_namespace:example_tool[{{"input":"example value"}}]

    Observation: Tool returns the requested data.

    Thought: I have enough information to answer the question.
    Action: Finish[final answer]

Begin solving the user’s request.

Conversation history:
{history}
"""


class ReActAgent:
    def __init__(self, llm: LLM, tool_registry: UnifiedRegistry):
        self.llm = llm
        self.tool_registry = tool_registry

    # will fix this later, frontend never use this
    def run(
        self,
        messages: list[Message],
    ) -> str:
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

        if self.is_last_message_tool_call(messages):
            stage = "using_tool"

        return self.llm.generate([
            Message(
                id="react-step",
                role="user",
                content=prompt,
                timestamp="",
                protocol=Route.REACT
            )
        ])
    
    def is_last_message_tool_call(self, messages: List[Message]) -> bool:
        """
        Check if the last message from the frontend is a tool call.
        """
        if not messages:
            return False
        
        last_message = messages[-1]
        if last_message.role != "tool":
            return False
        
        # action_pattern = r"Action:\s*(\w+)\[.*\]"
        # match = re.search(action_pattern, last_message.content)
        # if match:
        #     action = match.group(1)
            # tools never finish
            # if action != "Finish":
            #     return True
        
        return False
    
    def stream(
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

        if self.is_last_message_tool_call(messages):
            stage = "using_tool"
        else:
            # believe the orchestrator for tool needs
            stage = "tool_finding"

        return tokens_to_stream_chunks(
            self.llm.stream([
                Message(
                    id="react-step",
                    role="user",
                    content=prompt,
                    timestamp="",
                    protocol=Route.REACT
                )
            ]),
            protocol=Route.REACT,
            stage=stage
        )

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
        for tool in self.tool_registry.list_tools():
            schema = tool.schema
            if callable(schema):
                schema = schema()

            schema_str = json.dumps(schema, indent=2)
            lines.append(
                f"{tool.name}: {tool.description}\n"
                f"Args schema:\n{schema_str}\n"
                f"Execution: {tool.execution}"
            )
        return "\n\n".join(lines)