"use client";
import { useState } from "react";
import { Input, Button, Space } from "antd";
import { useStore } from "../store/store";

export default function PromptEditor() {
  const systemPrompt = useStore((s) => s.systemPrompt);
  const setPrompt = useStore((s) => s.setPrompt);
  const [value, setValue] = useState(systemPrompt);

  return (
    <Space orientation="vertical" style={{ width: "100%" }}>
      <Input.TextArea
        rows={4}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="在这里编辑系统提示词（人设、语气、称呼等）"
      />
      <Button
        size="small"
        type="primary"
        onClick={() => setPrompt(value)}
      >
        保存提示词
      </Button>
    </Space>
  );
}
