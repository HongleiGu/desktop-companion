from typing import Iterator
from models.stream import StreamChunk
from models.route import Route


def tokens_to_stream_chunks(
    tokens: Iterator[str],
    *,
    protocol: Route,
    stage: str = "llm",
) -> Iterator[StreamChunk]:
    """
    Convert raw token stream into StreamChunks.
    Agent controls protocol & stage.
    """
    for token in tokens:
        yield StreamChunk(
            type="token",
            content=token,
            protocol=protocol,
            stage=stage,
        )

    yield StreamChunk(
        type="done",
        content=None,
        protocol=protocol,
        stage="terminated",
    )
