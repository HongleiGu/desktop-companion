import json
import re
from typing import List, Dict, Any, Optional, Tuple
from tools.registry import ToolRegistry
from models.message import Message
from llm.base import LLM

REACT_PROMPT_TEMPLATE = """
You are an AI assistant that can reason step-by-step and use tools.
Follow this format strictly. Do NOT add notes, filler, or explanations outside the format.

Available tools:
{tools}

Format example:
Thought: I need to check the weather.
Action: get_weather[{{"location": "London"}}]
Observation: Tool result: 20°C, Sunny.
Thought: I now know the weather.
Action: Finish[The weather in London is 20°C and sunny.]

Use the following rules:
- Always use Thought → Action → Observation for each step.
- Only call tools if necessary; do not repeat tools already used.
- Use Finish[...] when you have a complete answer.
- Do not include any extra text or commentary.

---
Current Conversation:
{history}
User question: {question}
"""

class ReActAgent:
    def __init__(
        self,
        llm: LLM,
        tool_registry: ToolRegistry,
        max_steps: int = 10,
        session_id: str = None,
    ):
        self.llm = llm
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.session_id = session_id or str(id(self))
        self.conversation_history: List[str] = []
        self.frontend_tool_calls: List[Dict[str, Any]] = []
        self.current_step = 0
        self.is_waiting_for_frontend = False
        self.last_thought: Optional[str] = None
        self.last_action: Optional[str] = None

    def run(
        self, 
        question: str, 
        messages: List[Message], 
        frontend_tool_results: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the ReAct agent.
        
        Args:
            question: The user's question
            messages: Previous conversation messages
            frontend_tool_results: Results from frontend tool execution to resume with
        
        Returns:
            Dict containing answer, frontend_tools, and state information
        """
        # Reset or initialize state
        if not self.conversation_history and not frontend_tool_results:
            # First call - initialize history from messages
            self._initialize_history(messages)
            self.frontend_tool_calls = []
            self.current_step = 0
            self.is_waiting_for_frontend = False
        elif frontend_tool_results:
            # Resuming after frontend tool execution
            return self._resume_after_frontend_tool(frontend_tool_results)

        # Main ReAct loop
        while self.current_step < self.max_steps:
            result = self._execute_step(question)
            
            if result.get("status") == "frontend_tool_required":
                # Save state for resumption
                self.is_waiting_for_frontend = True
                return result
            elif result.get("status") == "complete":
                # Reset state for next conversation
                self._reset_state()
                return result
            elif result.get("status") == "continue":
                self.current_step += 1
                continue
        
        # Max steps reached
        final_result = {
            "answer": "I've reached the maximum number of reasoning steps. Please try rephrasing your question or breaking it down into smaller parts.",
            "frontend_tools": [],
            "status": "max_steps_reached"
        }
        self._reset_state()
        return final_result

    def _execute_step(self, question: str) -> Dict[str, Any]:
        """Execute a single ReAct step."""
        # Prepare prompt
        tools_desc = self._format_tools()
        history_str = "\n".join(self.conversation_history)
        
        prompt = REACT_PROMPT_TEMPLATE.format(
            tools=tools_desc,
            history=history_str,
            question=question,
        )

        # Generate response from LLM
        response = self.llm.generate([
            Message(
                id=f"react-{self.current_step}", 
                role="user", 
                content=prompt, 
                timestamp=""
            )
        ])
        
        response_text = self._extract_response_text(response)
        
        # Parse the response
        thought, action = self._parse_output(response_text)
        
        if not action:
            return {
                "answer": f"I'm having trouble processing this request. My response was: {response_text[:200]}...",
                "frontend_tools": [],
                "status": "error"
            }

        # Store thought and action for potential resumption
        self.last_thought = thought
        self.last_action = action

        # Check for final answer
        if action.startswith("Finish["):
            final_answer = self._parse_final_answer(action)
            return {
                "answer": final_answer,
                "frontend_tools": self.frontend_tool_calls,
                "status": "complete"
            }

        # Handle tool execution
        try:
            tool_name, tool_args = self._parse_action(action)
            tool = self.tool_registry.get(tool_name)
            
            if not tool:
                observation = f"Error: Tool '{tool_name}' not found."
                self._update_history(thought, action, observation)
                return {"status": "continue"}
                
            elif tool.execution == "backend":
                # Execute backend tool immediately
                result = tool.execute(**tool_args) if tool_args else tool.execute()
                observation = f"Tool result: {result}"
                self._update_history(thought, action, observation)
                return {"status": "continue"}
                
            elif tool.execution == "frontend":
                # Frontend tool - pause execution and return tool call
                self._update_history(thought, action, "")
                
                self.frontend_tool_calls.append({
                    "name": tool.name,
                    "args": tool_args,
                    "execution": tool.execution,
                    "call_id": f"call_{len(self.frontend_tool_calls)}_{tool.name}"
                })
                
                return {
                    "answer": f"Please execute the '{tool.name}' tool in the UI.",
                    "frontend_tools": self.frontend_tool_calls,
                    "status": "frontend_tool_required",
                    "state": self._get_state(),  # Save state for resumption
                    "requires_ui_action": True,
                }
                
            else:
                observation = f"Error: Unknown execution type '{tool.execution}' for tool '{tool_name}'."
                self._update_history(thought, action, observation)
                return {"status": "continue"}
                
        except Exception as e:
            observation = f"Error executing tool: {str(e)}"
            self._update_history(thought, action, observation)
            return {"status": "continue"}

    def _resume_after_frontend_tool(self, tool_results: Dict[str, Any]) -> Dict[str, Any]:
        """Resume execution after frontend tool completion."""
        if not self.is_waiting_for_frontend:
            return {
                "answer": "No pending frontend tool execution.",
                "frontend_tools": [],
                "status": "error"
            }
        
        # Add the tool result as observation
        tool_name = tool_results.get("name", "unknown")
        result = tool_results.get("result", "No result returned")
        success = tool_results.get("success", True)
        
        observation = f"Tool '{tool_name}' result: {result}"
        if not success:
            observation = f"Tool '{tool_name}' failed: {result}"
        
        # Update history with observation
        self.conversation_history[-1] = f"Observation: {observation}"
        
        # Reset waiting flag and continue
        self.is_waiting_for_frontend = False
        
        # Continue with next step
        return {"status": "continue"}

    def _initialize_history(self, messages: List[Message]):
        """Initialize conversation history from messages."""
        self.conversation_history = []
        for msg in messages:
            if msg.role == "user":
                self.conversation_history.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        self.conversation_history.append(f"Action: {tool_call['name']}[{json.dumps(tool_call['args'])}]")
                self.conversation_history.append(f"Assistant: {msg.content}")
            elif msg.role == "tool":
                self.conversation_history.append(f"Observation: {msg.content}")

    def _update_history(self, thought: Optional[str], action: str, observation: str):
        """Update conversation history with new step."""
        if thought:
            self.conversation_history.append(f"Thought: {thought}")
        if action:
            self.conversation_history.append(f"Action: {action}")
        if observation:
            self.conversation_history.append(f"Observation: {observation}")

    def _get_state(self) -> Dict[str, Any]:
        """Get current agent state for resumption."""
        return {
            "conversation_history": self.conversation_history.copy(),
            "current_step": self.current_step,
            "frontend_tool_calls": self.frontend_tool_calls.copy(),
            "last_thought": self.last_thought,
            "last_action": self.last_action,
            "is_waiting_for_frontend": self.is_waiting_for_frontend,
            "session_id": self.session_id
        }

    def load_state(self, state: Dict[str, Any]):
        """Load agent state for resumption."""
        if state.get("session_id") != self.session_id:
            raise ValueError("Cannot load state from different session")
        
        self.conversation_history = state.get("conversation_history", [])
        self.current_step = state.get("current_step", 0)
        self.frontend_tool_calls = state.get("frontend_tool_calls", [])
        self.last_thought = state.get("last_thought")
        self.last_action = state.get("last_action")
        self.is_waiting_for_frontend = state.get("is_waiting_for_frontend", False)

    def _reset_state(self):
        """Reset agent state for new conversation."""
        self.conversation_history = []
        self.frontend_tool_calls = []
        self.current_step = 0
        self.last_thought = None
        self.last_action = None
        self.is_waiting_for_frontend = False
    
    def _extract_response_text(self, response) -> str:
        """Extract text from LLM response object."""
        if hasattr(response, 'content'):
            return response.content
        elif isinstance(response, str):
            return response
        elif hasattr(response, 'choices') and len(response.choices) > 0:
            # Handle OpenAI-style response
            return response.choices[0].message.content
        else:
            return str(response)

    def _format_tools(self) -> str:
        lines = []
        for tool in self.tool_registry.list():
            # Get the schema properly
            schema = tool.args_schema
            if callable(schema):
                schema = schema()
            
            # Format schema for display
            if isinstance(schema, dict):
                schema_str = json.dumps(schema, indent=2)
            else:
                schema_str = str(schema)
                
            lines.append(
                f"{tool.name}: {tool.description}\n"
                f"Args schema: {schema_str}\n"
                f"Execution: {tool.execution}"
            )
        return "\n\n".join(lines)

    def _parse_output(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        # Extract thought (can be multi-line)
        thought_match = re.search(r"Thought:\s*(.*?)(?=\s*(?:Action:|Finish\[|$))", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        
        # Extract action (either tool call or Finish)
        action_match = re.search(r"(?:Action|Finish)\[?\s*:?\s*(\w+\[.*?\]|Finish\[.*?\])", text, re.DOTALL)
        if not action_match:
            # Try alternative pattern
            action_match = re.search(r"(Action:\s*.+?\]|Finish\[.+?\])", text, re.DOTALL)
        
        action = action_match.group(1).strip() if action_match else None
        
        # Clean up the action string
        if action and action.startswith("Action: "):
            action = action[8:]  # Remove "Action: " prefix
        
        return thought, action

    def _parse_action(self, action_text: str) -> Tuple[str, Dict[str, Any]]:
        # Handle both tool[args] and tool[] formats
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if not match:
            raise ValueError(f"Invalid Action format: {action_text}")

        tool_name = match.group(1)
        raw_args = match.group(2).strip()
        
        # Parse JSON arguments
        if raw_args:
            try:
                # Clean up the JSON string
                args = json.loads(raw_args)
                if not isinstance(args, dict):
                    args = {"input": args}
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                try:
                    # Add quotes around unquoted keys
                    fixed_raw = re.sub(r'(\w+):', r'"\1":', raw_args)
                    args = json.loads(fixed_raw)
                except:
                    # Fallback to treating as a single string input
                    args = {"input": raw_args}
        else:
            args = {}
            
        return tool_name, args

    def _parse_final_answer(self, action_text: str) -> str:
        """Extract the final answer from a Finish[...] action."""
        match = re.search(r"Finish\[(.*?)\]", action_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # If no proper match, try to extract any text after Finish[
        if "Finish[" in action_text:
            return action_text.split("Finish[", 1)[1].rstrip("]")
        
        return action_text  # Fallback