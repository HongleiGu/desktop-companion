export type Role = "system" | "user" | "assistant" | "tool";

export interface Message {
  id: string;
  role: Role;
  content: string;
  name?: string;
  timestamp: string
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
}

export interface StreamChunk {
  type: "token" | "done" | "error";
  content?: string;
}
