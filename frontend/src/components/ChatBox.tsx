"use client";

import { useState } from "react";
import { Button, Input, List, Space, Tag } from "antd";
import { useStore } from "../store/store";
import { useModelConfigStore } from "../store/modelStore";
import { sendMessageStream } from "../lib/api";
// import { Message } from "../types/chat";
import { formatSystemPrompt } from "../utils/chat";
import { parseReAct } from "../lib/reactParser";
import { TOOL_MAP } from "../types/tools";
import { confirmTool } from "../lib/confirmTool";

export default function ChatBox() {
  const [msg, setMsg] = useState("");
  const addChat = useStore((s) => s.addChat);
  const setStreamText = useStore((s) => s.setStreamText);
  const clearStream = useStore((s) => s.clearStream);
  const setCharacterState = useStore((s) => s.setCharacterState);
  // const chatHistory = useStore((s) => s.chatHistory);
  const systemPrompt = useStore((s) => s.systemPrompt);
  const files = useStore((s) => s.files);
  const setFiles = useStore((s) => s.setFiles);
  const modelConfig = useModelConfigStore((s) => s.config);

  const handleSend = async () => {
    if (!msg.trim()) return;

    setCharacterState("thinking-eyes-open");
    // Clear previous typewriter stream
    clearStream();

    // Add user message
    addChat({
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      content: msg,
      role: "user"
    });

    setMsg("");

    try {
      // the update of chatHistory requires a re-render, so we had to do this runtime workaround
      const reader = await sendMessageStream(useStore.getState().chatHistory, formatSystemPrompt(systemPrompt), modelConfig, files, true); // fetch reader
      let fullReply = "";
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });

        // split lines (SSE format: data: {...}\n\n)
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (!line.startsWith("data:")) continue;
          const data = JSON.parse(line.replace(/^data:\s*/, ""));
          if (data.type === "token" && data.content) {
            fullReply += data.content;
            setStreamText(fullReply);
            console.log("token:", data.content);
          }
        }
      }
      console.log("final:", fullReply);

      // Store assistant message
      addChat({
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        content: fullReply,
        role: "assistant"
      });

      // 🔍 Parse result
      const parsed = parseReAct(fullReply);
      console.log(parsed)

      if (parsed.type === "action") {
        const { tool, args } = parsed;

        if (!TOOL_MAP[tool]) {
          console.error("Unknown tool:", tool);
          setCharacterState("idle");
          return;
        }

        const confirmed = await confirmTool(tool, args);
        if (!confirmed) {
          setCharacterState("idle");
          return;
        }

        // Execute tool
        const result: Record<string, unknown> = await TOOL_MAP[tool](args as unknown);

        // Append tool message
        addChat({
          id: crypto.randomUUID(),
          timestamp: new Date().toISOString(),
          role: "tool",
          content: JSON.stringify({
            tool_name: tool,
            value: result.value,
            message: result.message
          })
        });

        // 🔁 Send SECOND request
        await handleSend();
        return;
      }

      setCharacterState("idle");
    } catch (err) {
      console.error(err);
      addChat({
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        content: "（ta好像没有回应…）",
        role: "assistant"
      });
      setCharacterState("idle");
    }
  };

    return (
    <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: 8 }}>
      {/* Input + Send button */}
      <Space.Compact style={{ width: "100%" }}>
        <Input
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          placeholder="说点什么…"
          onPressEnter={handleSend}
          className="interactive"
        />
        <Button type="primary" onClick={handleSend}>
          发送
        </Button>
      </Space.Compact>

      {/* Uploaded files list */}
      {files.length > 0 && (
        <div
          style={{
            maxHeight: 120,
            overflowY: "auto",
            padding: 4,
            border: "1px solid #f0f0f0",
            borderRadius: 4,
            backgroundColor: "#fafafa",
          }}
        >
          <List
            size="small"
            dataSource={files}
            renderItem={(file, idx) => (
              <List.Item
                style={{ display: "flex", justifyContent: "space-between", padding: "4px 8px" }}
              >
                <Tag
                  closable
                  onClose={(e) => {
                    e.preventDefault(); // prevent default tag close behavior
                    setFiles(files.filter((_, i) => idx != i));
                  }}
                  style={{ margin: 0 }}
                >
                  {file.name}
                </Tag>
                
              </List.Item>
            )}
          />
        </div>
      )}
    </div>
  );
}
