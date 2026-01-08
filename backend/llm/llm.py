from typing import List, Dict, Iterator, TypedDict, Literal, Optional


Message = Dict[str, str]  # {"role": "user"|"assistant"|"system", "content": str}


class StreamChunk(TypedDict):
    type: Literal["token", "done", "error"]
    content: Optional[str]


class LLM:
    def generate(self, messages: List[Message]) -> str:
        """
        Non-streaming completion.
        Returns the full assistant response.
        """
        raise NotImplementedError

    def stream(self, messages: List[Message]) -> Iterator[StreamChunk]:
        """
        Streaming completion.
        Yields incremental events suitable for HTTP streaming.
        """
        raise NotImplementedError
