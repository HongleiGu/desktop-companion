"use client";

import { List, Space, Typography, Select, Slider, InputNumber } from "antd";
import { useModelConfigStore } from "../store/modelStore";

const { Text } = Typography;

export default function ModelConfigPanel() {
  const config = useModelConfigStore((s) => s.config);
  const setConfig = useModelConfigStore((s) => s.setConfig);

  return (
    <List
      size="small"
      bordered
      header={<Text strong>模型设置</Text>}
      style={{ width: "100%" }}
    >
      {/* Provider */}
      <List.Item>
        <Space direction="vertical" style={{ width: "100%" }} size={2}>
          <Text type="secondary" style={{ fontSize: 11 }}>
            Provider
          </Text>
          <Select
            size="small"
            value={config.provider}
            onChange={(provider) => setConfig({ provider })}
            options={[
              { label: "Ollama", value: "ollama" },
              // future providers
              // { label: "OpenAI", value: "openai" },
            ]}
          />
        </Space>
      </List.Item>

      {/* Model */}
      <List.Item>
        <Space direction="vertical" style={{ width: "100%" }} size={2}>
          <Text type="secondary" style={{ fontSize: 11 }}>
            Model
          </Text>
          <Select
            size="small"
            value={config.model}
            onChange={(model) => setConfig({ model })}
            options={[
              { label: "llama3.1", value: "llama3.1" },
              // { label: "llama3", value: "llama3" },
              { label: "qwen3:7b", value: "qwen3:7b"}
            ]}
          />
        </Space>
      </List.Item>

      {/* Temperature */}
      <List.Item>
        <Space direction="vertical" style={{ width: "100%" }} size={2}>
          <Text type="secondary" style={{ fontSize: 11 }}>
            Temperature
          </Text>
          <Space>
            <Slider
              min={0}
              max={1}
              step={0.05}
              value={config.temperature}
              onChange={(temperature) => setConfig({ temperature })}
              style={{ flex: 1 }}
            />
            <InputNumber
              size="small"
              min={0}
              max={1}
              step={0.05}
              value={config.temperature}
              onChange={(temperature) =>
                typeof temperature === "number" &&
                setConfig({ temperature })
              }
            />
          </Space>
        </Space>
      </List.Item>
    </List>
  );
}
