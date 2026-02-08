import json
import logging
from typing import Iterator, List
from uuid import uuid4

from core.registry import UnifiedRegistry
from models.message import Message
from llm.base import LLM
from ...base import Agent
from models.route import Route

# Using a more "Ollama-friendly" prompt structure
ORCHESTRATOR_PROMPT = """
You are a routing system. Your job is to decide if the user's request needs a tool (REACT) or is just conversation (DIRECT_LLM).

AVAILABLE TOOL NAMESPACES:
{namespaces}

DECISION RULES:
1. Use 'REACT' if the request requires fetching specific data, performing actions, or using any tool from the namespaces above.
2. Use 'DIRECT_LLM' for greetings, general knowledge, or if no tools match.

OUTPUT FORMAT:
You must return ONLY a valid JSON object. Do not include markdown blocks or extra text.
{{
  "route": "DIRECT_LLM",
  "reason": "explanation"
}}
"""

class ReActOrchestrator(Agent):
    def __init__(self, llm: LLM, registry: UnifiedRegistry):
        self.llm = llm
        self.registry = registry

    def _format_messages(self, question: str, namespaces: List[str]) -> List[Message]:
        system_content = ORCHESTRATOR_PROMPT.format(namespaces=", ".join(namespaces))
        return [
            Message(
                id=str(uuid4()),
                role="system",
                content=system_content,
                timestamp=""
            ),
            Message(
                id=str(uuid4()),
                role="user",
                content=f"User Request: {question}",
                timestamp=""
            )
        ]

    def run(self, messages: List[Message]) -> Route:
        user_text = messages[-1].content
        
        # Get namespaces
        tools = self.registry.list_tools()
        namespaces = list(set([tool.name.split(':')[0] for tool in tools]))

        formatted_msgs = self._format_messages(user_text, namespaces)

        try:
            # Note: Ensure your LLM class returns the string content of the message
            raw = self.llm.generate(formatted_msgs)
            
            if not raw or not raw.strip():
                print("Warning: LLM returned empty content. Defaulting to DIRECT_LLM.")
                return Route.DIRECT_LLM

            # Clean up potential markdown backticks if the LLM ignores the "no markdown" rule
            clean_raw = raw.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_raw)
            
            route_str = data.get("route", "DIRECT_LLM")
            # Ensure we return a valid Route enum
            return Route(route_str)

        except Exception as e:
            print(f"Orchestrator error: {e} | Raw output: {raw}")
            return Route.DIRECT_LLM
        
    def stream(self, messages: List[Message]) -> Iterator:
        raise NotImplementedError("Orchestrator does not support streaming.")