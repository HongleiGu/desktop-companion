from typing import List, Iterator
from uuid import uuid4

from models.message import Message
from models.stream import StreamChunk
from models.route import Route
from llm.base import LLM
from ..base import Agent
from ..utils import tokens_to_stream_chunks


class BaseAgent(Agent):
    def __init__(self, llm: LLM):
        self.llm = llm

    def run(self, messages: List[Message]) -> str:
        """
        Single-pass, non-streaming generation.
        """
        return self.llm.generate(messages)

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        """
        Stream raw tokens from LLM and wrap them
        in protocol-aware StreamChunks.
        """
        return tokens_to_stream_chunks(
            self.llm.stream(messages),
            protocol=Route.DIRECT_LLM,
            stage="llm" # this is useless for BaseAgent
        )