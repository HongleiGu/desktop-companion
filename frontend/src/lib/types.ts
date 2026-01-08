export interface Message {
  text: string;
  role: "user" | "assistant" | "system";
  timestamp: string;
}