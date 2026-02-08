import { create } from "zustand";
import { UnifiedRegistrySpec, MCPSpec, ToolSpec } from "@/types/registry";

export interface UnifiedRegistryConfigState {
  config: UnifiedRegistrySpec;
  setConfig: (cfg: UnifiedRegistrySpec) => void;

  // Generic add/update/delete
  addMCP: (name: string, mcp: MCPSpec) => void;
  updateMCP: (name: string, patch: Partial<MCPSpec>) => void;
  deleteMCP: (name: string) => void;

  addTool: (id: string, tool: ToolSpec) => void;
  updateTool: (id: string, patch: Partial<ToolSpec>) => void;
  deleteTool: (id: string) => void;
}

export const useUnifiedRegistryConfigStore = create<UnifiedRegistryConfigState>((set) => ({
  config: { mcps: {}, tools: {} },

  setConfig: (cfg) => set(() => ({ config: cfg })),

  addMCP: (name, mcp) =>
    set((state) => ({ config: { ...state.config, mcps: { ...state.config.mcps, [name]: mcp } } })),

  updateMCP: (name, patch) =>
    set((state) => ({
      config: {
        ...state.config,
        mcps: {
          ...state.config.mcps,
          [name]: { ...state.config.mcps[name], ...patch },
        },
      },
    })),

  deleteMCP: (name) =>
    set((state) => {
      const { [name]: _, ...rest } = state.config.mcps;
      return { config: { ...state.config, mcps: rest } };
    }),

  addTool: (id, tool) =>
    set((state) => ({ config: { ...state.config, tools: { ...state.config.tools, [id]: tool } } })),

  updateTool: (id, patch) =>
    set((state) => ({
      config: {
        ...state.config,
        tools: {
          ...state.config.tools,
          [id]: { ...state.config.tools[id], ...patch },
        },
      },
    })),

  deleteTool: (id) =>
    set((state) => {
      const { [id]: _, ...rest } = state.config.tools;
      return { config: { ...state.config, tools: rest } };
    }),
}));
