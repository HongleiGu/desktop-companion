import { Card, Collapse, Switch, Button, Popconfirm } from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import { MCPSpec } from "@/types/registry";
import { ToolPanel } from "./ToolPanel";
import { SchemaField } from "@/components/Panels/GenericPanel";
import { useUnifiedRegistryConfigStore } from "@/store/unifiedRegistryStore";

export function MCPPanel({
  name,
  mcp,
}: {
  name: string;
  mcp: MCPSpec;
}) {
  const { updateMCP, deleteMCP } =
    useUnifiedRegistryConfigStore();

  return (
    <Card
      title={name}
      extra={
        <div className="flex items-center gap-2">
          <Switch
            checked={mcp.enabled}
            onChange={(enabled) =>
              updateMCP(name, { enabled })
            }
          />

          <Popconfirm
            title="Delete MCP?"
            onConfirm={() => deleteMCP(name)}
          >
            <Button
              danger
              type="text"
              icon={<DeleteOutlined />}
            />
          </Popconfirm>
        </div>
      }
      className="space-y-4"
    >
      {/* MCP CONFIG */}
      <div>
        <h4 className="font-medium mb-2">
          MCP Configuration
        </h4>

        <SchemaField
          schema={mcp.configSchema}
          value={mcp.config}
          onChange={(config) =>
            updateMCP(name, { config: config as Record<string, unknown> | undefined })
          }
        />
      </div>

      {/* TOOLS (runtime only) */}
      <Collapse
        items={mcp.tools.map((tool) => ({
          key: tool.id,
          label: tool.name,
          children: <ToolPanel tool={tool} />,
        }))}
      />
    </Card>
  );
}
