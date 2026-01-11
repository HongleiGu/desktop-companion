import json
from typing import List
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import StreamingResponse
from files.inject import inject_file_context
from files.parser import parse_uploaded_file
from models.files import ParsedFile
from models.chat import ChatRequest
from providers.registry import get_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Desktop Companion AI API")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow Content-Type, Authorization, etc.
)

@app.post("/chat")
async def chat(
    payload: str = Form(...),
    files: List[UploadFile] = File([]),  # notice the list
):
    # Parse JSON payload
    req: ChatRequest = ChatRequest.model_validate(json.loads(payload))

    print(req)

    messages = req.messages

    print(messages)
    print(type(messages[0]))
    file_contexts = []

    # Parse all uploaded files
    for file in files:
        raw_bytes = await file.read()
        parsed: ParsedFile = parse_uploaded_file(
            filename=file.filename,
            content_type=file.content_type,
            raw_bytes=raw_bytes,
        )
        file_contexts.append(parsed)

    # Inject all file contexts as system messages
    messages = inject_file_context(messages, file_contexts)
    req.messages = messages

    llm = get_llm(req)

    if req.stream:
        def generator():
            for chunk in llm.stream(messages):
                yield f"data:{chunk.model_dump_json()}\n\n"

        return StreamingResponse(generator(), media_type="text/event-stream")

    text = llm.generate(messages)
    return {"content": text}
