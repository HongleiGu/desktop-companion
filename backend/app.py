import json
from typing import List, Dict
from uuid import uuid4
from fastapi import Body, FastAPI, Form, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from llm import LLM
from agent import ReActAgent, Message, BaseAgent, ReActOrchestrator
from tools import ToolRegistry, UpdateCharacterProfileTool
from files.inject import inject_file_context
from files.parser import parse_uploaded_file
from models.files import ParsedFile
from models.chat import ChatRequest
from models import ToolResult, StreamChunk, Route

# ---------------- Setup ---------------- #
app = FastAPI(title="Desktop Companion AI API")

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LLM + Agent ---------------- #
llm_client = LLM()
tool_registry = ToolRegistry()
tool_registry.register(UpdateCharacterProfileTool())
agent_map = {
    Route.REACT: ReActAgent(llm_client, tool_registry),
    Route.DIRECT_LLM: BaseAgent(llm_client)
}
orchestrator = ReActOrchestrator(llm_client)


# ---------------- Helper ---------------- #
def parse_messages(req: ChatRequest, files: List[UploadFile]) -> List[Message]:
    """
    Parse JSON payload into Message objects, inject file contexts,
    and ensure each message has a unique id.
    """
    messages = req.messages.copy()
    file_contexts: List[ParsedFile] = []

    # Parse all uploaded files
    for file in files:
        raw_bytes = file.file.read()
        parsed = parse_uploaded_file(
            filename=file.filename,
            content_type=file.content_type,
            raw_bytes=raw_bytes,
        )
        file_contexts.append(parsed)

    # Inject file context as system messages
    messages = inject_file_context(messages, file_contexts)

    # Ensure each message has a unique id and convert to Pydantic Message
    pydantic_messages = []
    for m in messages:
        if not hasattr(m, "id") or not m.id:
            m["id"] = str(uuid4())
        pydantic_messages.append(Message.model_validate(m))

    return pydantic_messages

@app.post("/chat")
async def chat(
    payload: str = Form(...), 
    files: List[UploadFile] = File([]),
):
    print("Received Raw:", payload)
    # NOW your manual validation logic will actually run
    try:
        # We parse the string into your Pydantic model here
        chat_data = ChatRequest.model_validate_json(payload)
    except Exception as e:
        # This catches bad JSON formatting
        print(f"Invalid JSON format: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Invalid JSON format: {str(e)}")

    # IMPORTANT: Use 'chat_data' instead of 'payload' for the rest of your logic
    messages = parse_messages(chat_data, files)
    stream = chat_data.stream

    # Step 1 let the Orchestrator determine which agent to use
    agent_route = orchestrator.run(messages)
    print(f" Using ${agent_route} Agent\n\n")
    agent = agent_map[agent_route]

    # ---------------- Streaming ---------------- #
    if stream:
        async def generator():
            llm_stream: List[StreamChunk] = agent.stream(messages)
            for chunk in llm_stream:
                yield f"data: {chunk.model_dump_json()}\n\n"

        return StreamingResponse(generator(), media_type="text/event-stream")

    # ---------------- Non-streaming ---------------- #
    llm_stream: List[StreamChunk] = agent.run(messages)
    assistant_text = "".join([chunk.content for chunk in llm_stream])
    # print(assistant_text)

    # the frontend always streams, thinking of this later
    # Append assistant message
    messages.append(
        Message(
            id=str(uuid4()),
            role="assistant",
            content=assistant_text,
            timestamp="",
            protocol=agent_route
        )
    )

    # Parse Action / Finish
    result = agent.parse_result(assistant_text)

    # ---------------- Prepare response ---------------- #
    return {
        "assistant_text": assistant_text,
        "result": result,
        "messages": [m.model_dump() for m in messages],
    }
