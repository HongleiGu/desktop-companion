from agent import Agent
from tools import remember, get_time
from memory import Memory
from tools import Tool, ToolRegistry
from memory import AgentState
from llm import create_llm
from prompts import build_prompt
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

tools = ToolRegistry()
tools.register(Tool("time", "Get current time", lambda _: get_time(None)))
tools.register(Tool("remember", "Store a memory", remember))

agent = Agent(
    llm=create_llm("ollama"),
    memory=Memory(),
    tools=tools,
    state=AgentState()
)

if __name__ == "__main__":
    print("Desktop Companion Online ✨")
    while True:
        user = input("You: ")
        if user.lower() in {"exit", "quit"}:
            break
        response = agent.step(user)
        print("Companion:", response)
