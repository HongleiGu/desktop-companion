from typing import List
from models.message import Message
from llm.base import LLM
from ..base import Agent

class BaseAgent(Agent):
    def __init__(self, llm: LLM):
        self.llm = llm

    def run(self, messages: List[Message]) -> str:
        """
        Default behavior: single-pass generation
        Override if agent needs tools.
        """
        return self.llm.generate(messages)

    def stream(self, messages: List[Message]):
        """
        Default behavior: direct LLM streaming
        """
        return self.llm.stream(messages)
