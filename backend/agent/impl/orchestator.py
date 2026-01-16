# this is the orchestrator, it decides what agent we should use and what tools to call
# since in our design, the agent is fully stateless, so we must call this before every Agent call

import json
from typing import List
from uuid import uuid4

from models.intent import Intent
from models.message import Message
from llm.base import LLM
from ..base import Agent
from models.route import Route

# this seems a bit tricky here, will have a second thought when I have time
ORCHESTRATOR_PROMPT = """
Analyze the user's request and classify its primary intent. Choose ONE main intent from:

1. CONVERSATIONAL: Casual chat, questions, explanations, creative writing
2. INFORMATIONAL: Asking for facts, knowledge, explanations without action
3. ACTION: Requires performing an action (update, create, delete, modify)
4. UPDATE: Specifically about updating/changing existing data
5. RETRIEVAL: Fetching or retrieving information
6. SYSTEM: Technical/system-level requests

Critical decision rule: If the request involves ANY action that changes state (data, UI, files, profiles), 
classify as ACTION or UPDATE regardless of other factors.

Return JSON:
{{
  "intent": "CONVERSATIONAL|INFORMATIONAL|ACTION|UPDATE|RETRIEVAL|SYSTEM",
}}

User request:
---
{question}
---
"""



class Orchestrator(Agent):
    """
    Stateless routing agent.
    Decides execution strategy for every user request.
    """

    # Intent to route mapping
    INTENT_TO_ROUTE = {
        Intent.CONVERSATIONAL: Route.DIRECT_LLM,
        Intent.INFORMATIONAL: Route.DIRECT_LLM,
        Intent.ACTION: Route.REACT,
        Intent.UPDATE: Route.REACT,
        Intent.RETRIEVAL: Route.REACT,  # Might need tools for retrieval
        Intent.SYSTEM: Route.REACT,
    }

    def __init__(self, llm: LLM):
        self.llm = llm

    def _format_messages(self, question: str) -> List[Message]:
        print(question)
        return [
            Message(
                id=str(uuid4()),
                role="system",
                content=ORCHESTRATOR_PROMPT.format(question=question),
                name=None,
                timestamp=""
            )
        ]

    def run(self, messages: List[Message]) -> Route:
        """
        Decide whether to route to DIRECT_LLM or REACT.

        Fail-closed behavior:
        - Any parsing error
        - Any unexpected output
        → DIRECT_LLM
        """
        user_text = messages[-1].content

        raw = self.llm.generate(self._format_messages(user_text))
        print(raw + "\n\n")
        try:
            intent = json.loads(raw).get("intent")

            decision = self.INTENT_TO_ROUTE.get(Intent(intent))
            return decision

        except Exception as e:
            print(f"Orchestrator parsing error: {e}")
            return Route.DIRECT_LLM
        
    def stream(self, messages):
        raise NotImplementedError("Orchestrator should not enable stream")
