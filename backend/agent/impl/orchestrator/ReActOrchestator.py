# this is the orchestrator, it decides what agent we should use and what tools to call
# since in our design, the agent is fully stateless, so we must call this before every Agent call

import json
from typing import List
from uuid import uuid4

from core.registry import UnifiedRegistry
from models.intent import Intent
from models.message import Message
from llm.base import LLM
from ...base import Agent
from models.route import Route

ORCHESTRATOR_PROMPT = """
You are a routing agent. Determine if the user's request requires external tools or just a conversation.

Available Tool Namespaces:
{namespaces}

Intents:
- DIRECT_LLM: Casual chat, general knowledge, greeting, or the request cannot be fulfilled by available tools.
- REACT: Use this if the user wants to perform an action, update data, or fetch specific information that matches an available tool namespace.

Return JSON:
{{
  "route": "DIRECT_LLM | REACT",
  "reason": "short explanation"
}}

User request: {question}
"""

class ReActOrchestrator(Agent):
    def __init__(self, llm: LLM, registry: UnifiedRegistry):
        self.llm = llm
        self.registry = registry

    def run(self, messages: List[Message]) -> Route:
        user_text = messages[-1].content
        
        # Get a simple list of namespaces/tools for context
        # e.g., "system, weather_mcp, character_mcp"
        namespaces = list(set([name.split(':')[0] for name, _ in self.registry.list_all()]))

        formatted_prompt = ORCHESTRATOR_PROMPT.format(
            question=user_text,
            namespaces=", ".join(namespaces)
        )

        try:
            raw = self.llm.generate([Message(role="system", content=formatted_prompt)])
            data = json.loads(raw)
            
            # Map the route directly from the LLM's decision
            route_str = data.get("route")
            return Route(route_str) if route_str else Route.DIRECT_LLM

        except Exception as e:
            print(f"Orchestrator error: {e}")
            return Route.DIRECT_LLM