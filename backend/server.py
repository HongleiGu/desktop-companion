import time
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Iterator
import json
from dotenv import load_dotenv, find_dotenv

from agent import Agent
from tools import remember, get_time, Tool, ToolRegistry
from memory import Memory, AgentState
from llm import create_llm

load_dotenv(find_dotenv())

# --- Initialize tools ---
tools = ToolRegistry()
tools.register(Tool("time", "Get current time", lambda _: get_time(None)))
tools.register(Tool("remember", "Store a memory", remember))

# --- Initialize agent ---
agent = Agent(
    llm=create_llm("ollama"),
    memory=Memory(),
    tools=tools,
    state=AgentState()
)

# --- FastAPI setup ---
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic model ---
class Message(BaseModel):
    text: str

# --- Sync endpoint ---
@app.post("/chat")
def chat(msg: Message):
    """
    Non-streaming chat endpoint.
    Returns full assistant response.
    """
    reply = agent.step(msg.text)
    return {"reply": reply}

# --- Streaming endpoint ---
@app.post("/chat/stream")
def chat_stream(msg: Message):
    """
    Streaming chat endpoint using SSE.
    Yields incremental assistant tokens as JSON events.
    """

    def event_generator() -> Iterator[str]:
        for chunk in agent.step_stream(msg.text):
            # Convert chunk to JSON and SSE format
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# @app.post("/chat/stream")
# def chat_stream(msg: Message):
#     def event_generator():
#         # simulate streaming tokens
#         for token in ["Hello", " ", "world", "!"]:
#             yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
#             time.sleep(0.1)  # simulate delay
#         # send done signal
#         yield f"data: {json.dumps({'type': 'done', 'content': None})}\n\n"

#     return StreamingResponse(event_generator(), media_type="text/event-stream")