import { Message } from "../types/chat"
import { useStore } from "../store/store";

export const buildSystemPrompt = (prompt: string) => {
  return {
    id: crypto.randomUUID(),
    content: prompt,
    role: "system",
    timestamp: Date.now().toLocaleString()
  } as Message
}

/**
 * Simple function to format a system prompt template string
 * using the variables from handleSystemPromptTemplate.
 */
export const formatSystemPrompt = (template: string): string => {
  const characterProfile = useStore.getState().characterProfile;

  // Map variable placeholders to values (all strings)
  const varMap: Record<string, string> = {
    "{{character.name}}": characterProfile.ocName ?? "",
    "{{character.personality}}": characterProfile.personality ?? "",
    "{{character.speakingStyle}}": characterProfile.speakingStyle ?? "",
    "{{character.relation}}": characterProfile.relation ?? "",
    "{{character.birthday}}": characterProfile.birthday ?? "",
    "{{character.description}}": characterProfile.description ?? "",
    "{{env.time}}": new Date().toLocaleString(),
  };

  // Replace all placeholders in one pass
  return template.replace(/{{\s*[\w.]+\s*}}/g, (match) => varMap[match] ?? "");
};