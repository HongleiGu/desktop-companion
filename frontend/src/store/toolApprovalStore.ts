import { create } from "zustand";

type ToolApprovalState = {
  pending: null | {
    tool: string;
    args: unknown;
    resolve: (approved: boolean) => void;
  };

  requestApproval: (tool: string, args: unknown) => Promise<boolean>;
  approve: () => void;
  reject: () => void;
};

export const useToolApprovalStore = create<ToolApprovalState>((set, get) => ({
  pending: null,

  requestApproval: (tool, args) =>
    new Promise<boolean>((resolve) => {
      set({
        pending: { tool, args, resolve }
      });
    }),

  approve: () => {
    const p = get().pending;
    if (!p) return;
    p.resolve(true);
    set({ pending: null });
  },

  reject: () => {
    const p = get().pending;
    if (!p) return;
    p.resolve(false);
    set({ pending: null });
  }
}));
