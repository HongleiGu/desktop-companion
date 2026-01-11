from abc import ABC, abstractmethod
from typing import List, Iterator
from models.message import Message
from models.stream import StreamChunk

class Agent(ABC):

    @abstractmethod
    def run(self, messages: List[Message]) -> str:
        """Run agent synchronously, return final text"""
        pass

    @abstractmethod
    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        """Run agent and stream final output"""
        pass