export type Role = "system" | "user" | "assistant" | "tool";
export type AgentProtocol = "DIRECT_LLM" | "REACT" | null; // null for user input and tool output, need here for unity

export interface Message {
  id: string;
  role: Role;
  content: string;
  name?: string;
  timestamp: string;
  protocol?: AgentProtocol
}

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, unknown>;
}

export interface ChatConfig {
  provider: string;
  model: string;
  temperature: number;
  tools?: ToolDefinition[];
  metadata?: Record<string, unknown>;
}

export interface ChatRequest extends ChatConfig {
  messages: Message[];
  stream: boolean;
  files?: File[];
}

export interface StreamChunk {
  type: "token" | "done" | "error";
  content?: string;
  protocol?: AgentProtocol;
  stage?: string;
}
