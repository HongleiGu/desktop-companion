export interface CharacterProfile {
  birthday: string;
  ocName: string;
  relation: string;
  speakingStyle: string;
  personality: string;
  description: string;
}

export type MenuType = "history" | "profile" | "system prompt" | "modelConfig" | "exit" | null;
export type CharacterState = "idle" | "blink" | "drag" | "smile" | "thinking-eyes-open" | "thinking-eyes-closed"