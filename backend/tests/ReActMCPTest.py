import json
from uuid import uuid4
from typing import List

# Final structure imports
from core.registry import UnifiedRegistry
from MCP.impl import SimpleMCP
from tools.impl import GetTimeTool 
from llm import LLM
from agent import ReActAgent
from models import Message, ToolResult

# ---------------- 1. Setup Unified Architecture ---------------- #
# 1. Create the Registry (The brain)
registry = UnifiedRegistry()

# 2. Setup the MCP and add the tool
mcp = SimpleMCP() # name: "sample_mcp"
mcp.tool_registry.register(GetTimeTool()) # name: "get_time"

# 3. Register MCP to the Unified Registry
registry.register_mcp(mcp)

llm = LLM()
# Agent now gets the NAMESPACED schemas (e.g., 'sample_mcp:get_time')
agent = ReActAgent(llm, tool_registry=registry)

messages: List[Message] = []

user_input = (
    "Tell me the time now and calculate how many hours it is "
    "from now to tomorrow 2 am."
)

messages.append(Message(
    id=str(uuid4()),
    role="user",
    content=user_input,
    timestamp="2026-02-03T02:27:00"
))

print(f"--- Starting ReAct Loop ---\nUser: {user_input}\n")

# ---------------- 2. ReAct Execution Loop ---------------- #
MAX_STEPS = 5
step_count = 0

while step_count < MAX_STEPS:
    step_count += 1
    
    # STEP 1: Agent Step (Uses schemas from registry)
    stream = agent.stream(messages)
    # print([chunk for chunk in stream])
    assistant_text = "".join([chunk.content for chunk in stream if (chunk.content is not None)])
    print(assistant_text)

    messages.append(Message(
        id=str(uuid4()),
        role="assistant",
        content=assistant_text,
        timestamp=""
    ))

    # STEP 2: Parse Action
    result = agent.parse_result(assistant_text)
    
    if result["type"] == "finish":
        print(f"\n✅ FINAL ANSWER:\n{result['answer']}")
        break

    elif result["type"] == "action":
        full_tool_name = result["tool"] # Will be "sample_mcp:get_time"
        tool_args = result["args"]

        print(f"Step {step_count}: Agent calls '{full_tool_name}'")

        # STEP 3: Unified Execution
        # We find the tool by its namespaced name
        tool = registry.get(full_tool_name)
        
        if not tool:
            status = "Error"
            val = None
            msg = f"Tool '{full_tool_name}' not found."
        else:
            try:
                # We execute the tool logic
                output = tool.execute(**tool_args)
                status = "Success"
                val = output
                msg = "Execution successful"
            except Exception as e:
                status = "Error"
                val = None
                msg = str(e)

        tool_result = ToolResult(message=msg, value=val)

        # STEP 4: Provide Observation
        observation_content = (
            f"Observation: Status: {status}, "
            f"Result: {json.dumps(tool_result.value)}, "
            f"Message: {tool_result.message}"
        )
        
        messages.append(Message(
            id=str(uuid4()),
            role="tool", 
            content=observation_content,
            timestamp=""
        ))
        
        print(f"↳ Observation: {observation_content}\n")
        continue

# ---------------- 3. Persistence ---------------- #
output_file = "./ReAct_Unified_Test.json"
with open(output_file, "w") as f:
    json.dump([m.model_dump() for m in messages], f, indent=4)

print(f"\n--- Test Complete ---\nConversation saved to {output_file}")