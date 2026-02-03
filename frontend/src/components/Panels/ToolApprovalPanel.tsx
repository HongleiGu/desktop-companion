import { Button, Card } from "antd";
import { useToolApprovalStore } from "@/store/toolApprovalStore";

export function ToolApprovalPanel() {
  const pending = useToolApprovalStore(s => s.pending);
  const approve = useToolApprovalStore(s => s.approve);
  const reject = useToolApprovalStore(s => s.reject);

  if (!pending) return null;

  return (
    <Card
      title={`Tool Request: ${pending.tool}`}
      style={{ marginTop: 8, maxWidth: 800 }}
    >
      <pre style={{ maxHeight: 200, overflow: "auto" }}>
        {JSON.stringify(pending.args, null, 2)}
      </pre>

      <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
        <Button danger onClick={reject}>Reject</Button>
        <Button type="primary" onClick={approve}>Approve</Button>
      </div>
    </Card>
  );
}
