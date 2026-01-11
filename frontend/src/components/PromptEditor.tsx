"use client";

import { useRef } from "react";
import { List, Typography, Space, Button, Input, Divider } from "antd";
import { CopyOutlined } from "@ant-design/icons";
import { useStore } from "../store/store";

const { Text } = Typography;
const { TextArea } = Input;

export default function SystemPromptPanel() {
  const systemPrompt = useStore((s) => s.systemPrompt);
  const setSystemPrompt = useStore((s) => s.setSystemPrompt);

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const variables = [
    {
      title: "角色",
      vars: [
        "{{character.name}}",
        "{{character.personality}}",
        "{{character.speakingStyle}}",
        "{{character.relation}}",
        "{{character.birthday}}",
        "{{character.description}}",
      ],
    },
    {
      title: "环境",
      vars: ["{{env.time}}"],
    },
  ];

  /**
   * Insert variable at cursor position
   */
  const insertVar = (v: string) => {
    const el = textareaRef.current;
    if (!el) return;

    const start = el.selectionStart ?? 0;
    const end = el.selectionEnd ?? 0;

    const next =
      systemPrompt.slice(0, start) +
      v +
      systemPrompt.slice(end);

    setSystemPrompt(next);

    // restore cursor
    requestAnimationFrame(() => {
      el.focus();
      el.selectionStart = el.selectionEnd = start + v.length;
    });
  };

  return (
    <div className="flex gap-3">
      {/* Left: variables */}
      <div className="w-48 shrink-0">
        <List
          size="small"
          header={<Text strong>可用变量</Text>}
        >
          {variables.map((section) => (
            <List.Item key={section.title}>
              <Space direction="vertical" size={4}>
                <Text type="secondary" style={{ fontSize: 11 }}>
                  {section.title}
                </Text>

                {section.vars.map((v) => (
                  <Button
                    key={v}
                    type="text"
                    size="small"
                    icon={<CopyOutlined />}
                    onClick={() => insertVar(v)}
                    style={{ padding: 0, textAlign: "left" }}
                  >
                    <Text code style={{ fontSize: 12 }}>
                      {v}
                    </Text>
                  </Button>
                ))}
              </Space>
            </List.Item>
          ))}
        </List>
      </div>

      <Divider orientation="vertical" style={{ height: "auto" }} />

      {/* Right: editor */}
      <div className="flex-1">
        <Text strong>系统提示词</Text>

        <TextArea
          ref={textareaRef}
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          placeholder="在这里编写系统提示词，可使用左侧变量…"
          autoSize={{ minRows: 6, maxRows: 12 }}
          className="mt-1"
        />

        <Text type="secondary" style={{ fontSize: 11 }}>
          提示：系统提示词会在每次对话时自动注入,修改后自动保存
        </Text>
      </div>
    </div>
  );
}
