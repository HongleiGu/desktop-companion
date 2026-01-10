from abc import ABC, abstractmethod
from typing import List, Iterator
from models.message import Message
from models.stream import StreamChunk

class LLM(ABC):

    @abstractmethod
    def generate(self, messages: List[Message]) -> str:
        pass

    @abstractmethod
    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        pass
