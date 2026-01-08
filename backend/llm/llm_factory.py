def create_llm(backend="ollama"):
    if backend == "ollama":
        from .ollama import OllamaLLM
        return OllamaLLM(model="llama3.1")
    if backend == "groq":
        from .groq import GroqLLM
        return GroqLLM(api_key="YOUR_KEY")
    raise ValueError("Unknown LLM backend")
