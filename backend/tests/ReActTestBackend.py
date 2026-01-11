from agent import ReActAgent
from tools import ToolRegistry, GetTimeTool
from llm import LLM

if __name__ == "__main__":
  registry = ToolRegistry()
  registry.register(GetTimeTool())
  llm = LLM()
  agent = ReActAgent(llm, registry, 5)
  response = agent.run("What is the time now, how many hours is it from now to tomorrow 2:00 am", [])
  print(response)