import json
from typing import List
from uuid import uuid4

from fastapi import Body, FastAPI, Form, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from models.tools import ToolRequest, ToolResult
from models.spec import UnifiedRegistrySpec
from llm import LLM
from agent import ReActAgent, Message, BaseAgent, ReActOrchestrator
from files.inject import inject_file_context
from files.parser import parse_uploaded_file
from models.files import ParsedFile
from models.chat import ChatRequest
from models import StreamChunk, Route
from core.registry import UnifiedRegistry

# ---------------- Setup ---------------- #
app = FastAPI(title="Desktop Companion AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LLM + Agent ---------------- #
llm_client = LLM()
# ---------------- UnifiedRegistry ---------------- #
registry = UnifiedRegistry()
agent_map = {
    Route.REACT: ReActAgent(llm_client, registry),
    Route.DIRECT_LLM: BaseAgent(llm_client)
}
orchestrator = ReActOrchestrator(llm_client, registry)

# ---------------- Helper ---------------- #
def parse_messages(req: ChatRequest, files: List[UploadFile]) -> List[Message]:
    messages = req.messages.copy()
    file_contexts: List[ParsedFile] = []

    for file in files:
        raw_bytes = file.file.read()
        parsed = parse_uploaded_file(
            filename=file.filename,
            content_type=file.content_type,
            raw_bytes=raw_bytes,
        )
        file_contexts.append(parsed)

    messages = inject_file_context(messages, file_contexts)

    pydantic_messages = []
    for m in messages:
        if not hasattr(m, "id") or not m.id:
            m["id"] = str(uuid4())
        pydantic_messages.append(Message.model_validate(m))

    return pydantic_messages

# ---------------- Endpoints ---------------- #
@app.post("/chat")
async def chat(payload: str = Form(...), files: List[UploadFile] = File([])):
    # Parse payload
    try:
        chat_data = ChatRequest.model_validate_json(payload)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON format: {str(e)}")

    messages = parse_messages(chat_data, files)
    stream = chat_data.stream

    agent_route = orchestrator.run(messages)
    agent = agent_map.get(agent_route)
    if not agent:
        raise HTTPException(status_code=400, detail=f"No agent found for route {agent_route}")

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

    messages.append(
        Message(
            id=str(uuid4()),
            role="assistant",
            content=assistant_text,
            timestamp="",
            protocol=agent_route
        )
    )

    result = agent.parse_result(assistant_text)

    return {
        "assistant_text": assistant_text,
        "result": result,
        "messages": [m.model_dump() for m in messages],
    }

@app.post("/discover-tools")
async def discover_tools(spec: UnifiedRegistrySpec):
    """
    Update the UnifiedRegistry from frontend spec and return
    the full runtime_view (MCPs + tool schemas).
    """
    registry.register_from_spec(spec)
    # Return the fully resolved runtime view
    rtrn = registry.runtime_view()
    return rtrn



@app.post("/call-tool")
async def call_tool(request: ToolRequest) -> ToolResult:
    try:
        # 1. Check if tool exists in registry
        tool = registry.get(request.name)
        if not tool:
            raise HTTPException(
                status_code=404, 
                detail=f"Tool '{request.name}' not found in registry."
            )

        # 2. Execute the tool
        # We use await if your tool's execute method is async
        result = tool.execute(request.args)
        
        return ToolResult(
            message=f"Tool {request.name} executed successfully",
            value=result
        )

    except TypeError as e:
        # print(e)
        # This catches cases where the 'args' don't match the function signature
        raise HTTPException(status_code=400, detail=f"Invalid arguments: {str(e)}")
    except Exception as e:
        # General catch for tool-side logic errors
        # print(e)
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")