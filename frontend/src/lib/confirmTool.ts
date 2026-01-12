import { useToolApprovalStore } from "../store/toolApprovalStore";

export async function confirmTool(tool: string, args: unknown): Promise<boolean> {
  const { requestApproval } = useToolApprovalStore.getState();
  return await requestApproval(tool, args);
}