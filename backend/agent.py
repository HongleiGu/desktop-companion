import re
from typing import Iterator, Dict
from llm import LLM, StreamChunk, Message
from prompts import build_prompt


class Agent:
    def __init__(self, llm: LLM, memory, tools, state):
        self.llm = llm
        self.memory = memory
        self.tools = tools
        self.state = state

    def _build_messages(self, user_input: str) -> list[Message]:
        """
        Construct the message history for the LLM based on memory and state.
        """
        system_message = {
            "role": "system",
            "content": build_prompt(self.memory, self.tools, self.state.describe())
        }
        user_message = {"role": "user", "content": user_input}

        return [system_message, *self.memory.context(), user_message]

    def step(self, user_input: str) -> str:
        """
        Non-streaming agent step: returns the full assistant reply.
        """
        self.memory.add_short("user", user_input)
        self.state.update_from_text(user_input)

        messages = self._build_messages(user_input)
        reply = self.llm.generate(messages)

        # Tool call pattern: [TOOL:name args]
        match = re.search(r"\[TOOL:(\w+)\s*(.*?)\]", reply)
        if match:
            tool_name, args = match.groups()
            tool_result = self.tools.run(tool_name, args)
            self.memory.add_short("assistant", tool_result)
            return tool_result

        self.memory.add_short("assistant", reply)
        return reply

    def step_stream(self, user_input: str) -> Iterator[StreamChunk]:
        """
        Streaming agent step: yields incremental assistant tokens/events.
        """
        self.memory.add_short("user", user_input)
        self.state.update_from_text(user_input)

        messages = self._build_messages(user_input)

        # Stream the LLM output
        for chunk in self.llm.stream(messages):
            # Optionally handle tool call detection on the fly
            if chunk["type"] == "token":
                # Simple incremental tool detection (optional)
                match = re.search(r"\[TOOL:(\w+)\s*(.*?)\]", chunk["content"] or "")
                if match:
                    tool_name, args = match.groups()
                    tool_result = self.tools.run(tool_name, args)
                    self.memory.add_short("assistant", tool_result)
                    yield {"type": "token", "content": tool_result}
                    continue

            # Pass the LLM token along
            yield chunk

        # Ensure final done event
        yield {"type": "done", "content": None}
