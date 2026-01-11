import { create } from "zustand";
import { CharacterProfile, CharacterState, MenuType } from "../types";
import { Message } from "../types/chat";

interface Store {
  chatHistory: Message[];
  systemPrompt: string;
  characterProfile: CharacterProfile;
  affinity: number;
  characterState: CharacterState;

  // --- streaming state ---
  currentStreamText: string;
  setStreamText: (text: string) => void;
  clearStream: () => void;

  // --- chat actions ---
  addChat: (chat: Message) => void;
  deleteChat: (id: string) => void;
  setPrompt: (prompt: string) => void;
  setCharacterProfile: (profile: CharacterProfile) => void;
  incrementAffinity: (amount: number) => void;
  setCharacterState: (state: CharacterState) => void;

  openModal: MenuType;
  setOpenModal: (m: MenuType) => void;

  setSystemPrompt: (prompt: string) => void;
}

export const useStore = create<Store>((set) => ({
  chatHistory: [],
  systemPrompt: "",
  characterProfile: { birthday: "", ocName: "", relation: "", description: "", speakingStyle: "", personality: "" },
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
  setCharacterProfile: (profile) => set({ characterProfile: profile }),
  incrementAffinity: (amount) => set((state) => ({ affinity: state.affinity + amount })),
  setCharacterState: (stateVal) => set({ characterState: stateVal }),

  openModal: null,
  setOpenModal: (m) => set({ openModal: m }),

  setSystemPrompt: (prompt) => set({systemPrompt: prompt})
}));
