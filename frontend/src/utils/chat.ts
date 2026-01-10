import { Message } from "../types/chat"

export const buildSystemPrompt = (prompt: string) => {
  return {
    id: crypto.randomUUID(),
    content: prompt,
    role: "system",
    timestamp: Date.now().toLocaleString()
  } as Message
}