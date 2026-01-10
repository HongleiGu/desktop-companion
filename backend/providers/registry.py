from llm.ollama import OllamaLLM
from llm.base import LLM
from models.chat import ChatRequest

def get_llm(request: ChatRequest) -> LLM:
    if request.provider == "ollama":
        return OllamaLLM(
            model=request.model,
            temperature=request.temperature,
        )

    raise ValueError(f"Unknown provider: {request.provider}")
