from typing import List

from dotenv import load_dotenv
from llm.base import GenerationConfig
from core.registry import UnifiedRegistry
from MCP.impl.GithubMCP import GitHubMCP
from agent import ReActAgent
from llm import LLM
from models.message import Message
from uuid import uuid4

import json
import os

load_dotenv()

# Initialize the "Brain"
registry = UnifiedRegistry()
github = GitHubMCP(github_token=os.getenv("GITHUB_KEY"))
registry.register_mcp(github)

config = GenerationConfig(
    temperature=0.2,
    top_p=0.9,
    max_tokens=4096,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

# Initialize the Agent with the namespaced schemas
agent = ReActAgent(LLM(generation_config=config), tool_registry=registry)

messages: List[Message] = []

user_input = (
    "Look up lambda-feedback/graph-eval. find how many open pull requests are there in the repo"
)

messages.append(Message(
    id=str(uuid4()),
    role="user",
    content=user_input,
    timestamp="2026-02-03T02:27:00"
))

# The ReAct Loop
for _ in range(3):  # Allow up to 3 steps
    # 1. Ask LLM for next step
    # print(messages)
    response = agent.run(messages) 
    # print(response)
    messages.append(
        Message(
            id=str(uuid4()),
            role="assistant", 
            content=response,
            timestamp=""
        )
    )
    # 2. Parse the Action (e.g., github:list_issues)
    action = agent.parse_result(response)
    print(action, response)

    # 3. EXECUTION: This is where our Registry shines
    try:
        tool = registry.get(action['tool'])
        print(f"DEBUG: Agent calling {action['tool']} with {action['args']}")
        result = tool.execute(action['args'])
        # print("tool and result", tool.name, result)
        
        # 4. Feed the real data back to the Agent
        messages.append(
            Message(
                id=str(uuid4()),
                role="tool",
                content=f"{action['tool']} result: {json.dumps(result)}",
                timestamp=""
            )
        )
    except:
        print(f"FINISH: Agent finishing with {action['answer']}")
        break
# ---------------- 3. Persistence ---------------- #
output_file = "./ReAct_Remote_MCP_Test.json"
with open(output_file, "w") as f:
    json.dump([m.model_dump() for m in messages], f, indent=4)
print("\n--- FINAL SUMMARY ---\n", messages[-1].content)