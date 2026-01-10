import { create } from "zustand";

export interface ChatRecord {
  id: string;
  timestamp: string;
  message: string;
}

export interface UserProfile {
  nickname: string;
  birthday: string;
  ocName: string;
  relation: string;
}

export type ModalType = "history" | "profile" | "settings" | null;
export type CharacterState = "idle" | "blink" | "drag" | "smile" | "thinking-eyes-open" | "thinking-eyes-closed"

interface Store {
  chatHistory: ChatRecord[];
  systemPrompt: string;
  userProfile: UserProfile;
  affinity: number;
  characterState: CharacterState;

  // --- streaming state ---
  currentStreamText: string;
  setStreamText: (text: string) => void;
  clearStream: () => void;

  // --- chat actions ---
  addChat: (chat: ChatRecord) => void;
  deleteChat: (id: string) => void;
  setPrompt: (prompt: string) => void;
  setUserProfile: (profile: UserProfile) => void;
  incrementAffinity: (amount: number) => void;
  setCharacterState: (state: CharacterState) => void;

  openModal: ModalType;
  setOpenModal: (m: ModalType) => void;
}

export const useStore = create<Store>((set) => ({
  chatHistory: [],
  systemPrompt: "",
  userProfile: { nickname: "", birthday: "", ocName: "", relation: "" },
  affinity: 0,
  characterState: "idle",

  // --- streaming state ---
  currentStreamText: "",
  setStreamText: (text) => {
    console.log(text)
    set({ currentStreamText: text })
  },
  clearStream: () => set({ currentStreamText: "" }),

  // --- chat actions ---
  addChat: (chat) =>
    set((state) => ({ chatHistory: [...state.chatHistory, chat] })),
  deleteChat: (id) =>
    set((state) => ({ chatHistory: state.chatHistory.filter((c) => c.id !== id) })),
  setPrompt: (prompt) => set({ systemPrompt: prompt }),
  setUserProfile: (profile) => set({ userProfile: profile }),
  incrementAffinity: (amount) => set((state) => ({ affinity: state.affinity + amount })),
  setCharacterState: (stateVal) => set({ characterState: stateVal }),

  openModal: null,
  setOpenModal: (m) => set({ openModal: m }),
}));
