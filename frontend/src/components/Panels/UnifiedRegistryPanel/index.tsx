import { useState } from "react";
import { Button, Modal, Input, message } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { MCPPanel } from "./MCPPanel";
import { useUnifiedRegistryConfigStore } from "@/store/unifiedRegistryStore";
import { MCPSpec } from "@/types/registry";
import { inferJSONSchema } from "@/types/fields/inferSchema";
import { discoverTools } from "@/lib/api";

export function UnifiedRegistryPanel() {
  const store = useUnifiedRegistryConfigStore();
  const [modalVisible, setModalVisible] = useState(false);
  const [jsonInput, setJsonInput] = useState("");

  const handleAddMCP = async () => {
    try {
      const parsed = JSON.parse(jsonInput) as MCPSpec;
      if (!parsed.name) {
        message.error("MCP JSON must have a `name` field");
        return;
      }
      // parsed.configSchema = inferJSONSchema(parsed.config)

      // 1️⃣ Create updated config object
      // there is a timing issue with zustand, even if you await
      // the config that reaches discoverTools is not the updated version
      const newConfig = {
        ...store.config,
        mcps: {
          ...store.config.mcps,
          [parsed.name]: parsed,
        },
      };

      // 2️⃣ Update Zustand store
      store.setConfig(newConfig);

      // 3️⃣ Clear input and close modal
      setJsonInput("");
      setModalVisible(false);

      // 4️⃣ Call discoverTools with the updated config
      await discoverTools(newConfig, store.setConfig);
    } catch (err) {
      message.error("Invalid JSON");
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2 items-center">
        <Input.TextArea
          rows={6}
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          placeholder="Paste raw MCP JSON here (must include `name` field)"
        />
        <Button type="primary" onClick={handleAddMCP}>
          Add MCP
        </Button>
      </div>

      {Object.entries(store.config.mcps).map(([name, mcp]) => {
        console.log("mcp", mcp)
        return (
          <MCPPanel key={name} name={name} mcp={mcp} />
        )
      })}
    </div>

  );
}
