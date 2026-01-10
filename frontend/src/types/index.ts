export interface UserProfile {
  nickname: string;
  birthday: string;
  ocName: string;
  relation: string;
}

export type ModalType = "history" | "profile" | "settings" | null;
export type CharacterState = "idle" | "blink" | "drag" | "smile" | "thinking-eyes-open" | "thinking-eyes-closed"