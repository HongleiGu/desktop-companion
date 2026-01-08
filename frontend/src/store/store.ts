import { create } from "zustand";

interface ChatRecord {
  id: string;
  timestamp: string;
  message: string;
}

interface UserProfile {
  nickname: string;
  birthday: string;
  ocName: string;
  relation: string;
}

interface Store {
  chatHistory: ChatRecord[];
  systemPrompt: string;
  userProfile: UserProfile;
  affinity: number;
  characterState: "idle" | "talk" | "eat" | "sleep" | "alert";

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
  setCharacterState: (state: Store["characterState"]) => void;
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
}));
