from agent import ReActAgent
from tools import ToolRegistry, UpdateCharacterProfileTool
from llm import LLM

if __name__ == "__main__":
  registry = ToolRegistry()
  registry.register(UpdateCharacterProfileTool())
  llm = LLM()
  agent = ReActAgent(llm, registry, 5)
  response = agent.run("Be a bit friendly, imagine you are a stargazer wandering in outer space, planets and civilizations flourish and vanish in front of you yet the space remains slient", [])
  print(response)