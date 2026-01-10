import json
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
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
async def chat(req: ChatRequest):
    print(req)
    llm = get_llm(req)

    if req.stream:
        def generator():
            for chunk in llm.stream(req.messages):
                yield f"data:{chunk.model_dump_json()}\n\n"

        return StreamingResponse(
            generator(),
            media_type="text/event-stream",
        )

    text = llm.generate(req.messages)
    return {"content": text}