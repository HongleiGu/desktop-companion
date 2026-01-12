import json
from typing import List, Dict
from uuid import uuid4
from fastapi import Body, FastAPI, Form, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from llm import LLM
from agent import ReActStepAgent, Message
from tools import ToolRegistry, UpdateCharacterProfileTool
from files.inject import inject_file_context
from files.parser import parse_uploaded_file
from models.files import ParsedFile
from models.chat import ChatRequest
from models import ToolResult, StreamChunk

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
agent = ReActStepAgent(llm_client, tool_registry)


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
    # CHANGE THIS: Accept payload as a raw string from the Form
    payload: str = Form(...), 
    files: List[UploadFile] = File([]),
):
    
    # NOW your manual validation logic will actually run
    try:
        # We parse the string into your Pydantic model here
        chat_data = ChatRequest.model_validate_json(payload)
    except Exception as e:
        # This catches bad JSON formatting
        raise HTTPException(status_code=422, detail=f"Invalid JSON format: {str(e)}")

    # IMPORTANT: Use 'chat_data' instead of 'payload' for the rest of your logic
    messages = parse_messages(chat_data, files)
    stream = chat_data.stream

    # ---------------- Streaming ---------------- #
    if stream:
        async def generator():
            llm_stream: List[StreamChunk] = agent.step(messages)
            for chunk in llm_stream:
                yield f"data: {chunk.model_dump_json()}\n\n"

        return StreamingResponse(generator(), media_type="text/event-stream")

    # ---------------- Non-streaming ---------------- #
    llm_stream: List[StreamChunk] = agent.step(messages)
    assistant_text = "".join([chunk.content for chunk in llm_stream])

    # Append assistant message
    messages.append(
        Message(
            id=str(uuid4()),
            role="assistant",
            content=assistant_text,
            timestamp=""
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
