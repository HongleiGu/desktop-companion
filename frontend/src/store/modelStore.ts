import { create } from "zustand";
import { ChatConfig } from "../types/chat";

interface ModelConfigState {
  config: ChatConfig;
  setConfig: (cfg: Partial<ChatConfig>) => void;
}

export const useModelConfigStore = create<ModelConfigState>((set) => ({
  config: {
    provider: "ollama",
    model: "llama3.1",
    temperature: 0.7,
  },
  setConfig: (cfg) =>
    set((state) => ({ config: { ...state.config, ...cfg } })),
}));
