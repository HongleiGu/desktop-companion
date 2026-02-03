from tools import ToolRegistry, GetTimeTool
from llm import LLM
import json
from agent import ReActAgent  # stateless version
from models import Message, StreamChunk, ToolResult
from uuid import uuid4

# ---------------- Setup ---------------- #
registry = ToolRegistry()
tool = GetTimeTool()
registry.register(tool)
llm = LLM()
agent = ReActAgent(llm, registry)

# Conversation history: frontend owns this
messages = []

user_input = (
    "Tell me the time now"
    "and calculate how many hours is it from now to tommorrow 2 am, downcast if necessary"
)

messages.append(Message(
    id=str(uuid4()),
    role="user",
    content=user_input,
    timestamp=""
))

# ---------------- Frontend loop ---------------- #
while True:
    # Step 1: agent generates a turn
    stream: StreamChunk = agent.run(messages)

    # Collect full streamed text
    assistant_text = ""
    for chunk in stream:
        assistant_text += chunk.content

    # Add assistant turn to conversation
    messages.append(
        Message(
            id=str(uuid4()),
            role="assistant",
            content=assistant_text,
            timestamp=""
        )
    )


    # Step 2: parse Action or Finish
    result = agent.parse_result(assistant_text)
    print("Agent Result:", result)

    if result["type"] == "finish":
        print("Final Story:\n", result["answer"])
        break

    elif result["type"] == "action":
        tool_name = result["tool"]
        tool_args = result["args"]

        print(f"Agent requested frontend tool '{tool_name}' with params:")
        print(json.dumps(tool_args, indent=2))

        # Step 3: Frontend executes the tool (simulated)
        # This tool updates the character profile using agent-provided args
        if tool_name == "get_time":
            # Simulate execution: just echoing back for observation
            tool_result = ToolResult(message=f"get_time executed successfully", value=tool.execute())
        else:
            tool_result = ToolResult(message="Error: Tool not found", value=None)

        # Step 4: append tool result as Observation
        messages.append(
            Message(
                id=str(uuid4()),
                role="tool",
                content=f"{tool_name} result: {json.dumps(tool_result.value)}, message: {tool_result.message}",
                timestamp=""
            )
        )

        # Next iteration: agent sees Observation and continues
        continue

    else:
        print("Error parsing agent output:", result)
        break

# ---------------- Save conversation ---------------- #
with open("./ReActTestBackend.json", "w") as f:
    json.dump([m.model_dump() for m in messages], f, indent=4)
    f.write("\n\n")