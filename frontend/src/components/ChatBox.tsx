"use client";

import { useState } from "react";
import { Button, Input, Space } from "antd";
import { useStore } from "../store/store";
import { useModelConfigStore } from "../store/modelStore";
import { sendMessageStream } from "../lib/api";
import { Message } from "../types/chat";
import { formatSystemPrompt } from "../utils/chat";

export default function ChatBox() {
  const [msg, setMsg] = useState("");
  const addChat = useStore((s) => s.addChat);
  const setStreamText = useStore((s) => s.setStreamText);
  const clearStream = useStore((s) => s.clearStream);
  const setCharacterState = useStore((s) => s.setCharacterState);
  // const chatHistory = useStore((s) => s.chatHistory);
  const systemPrompt = useStore((s) => s.systemPrompt);
  const modelConfig = useModelConfigStore((s) => s.config);

  const handleSend = async () => {
    if (!msg.trim()) return;

    setCharacterState("thinking-eyes-open");
    // Clear previous typewriter stream
    clearStream();

    // Add user message
    addChat({
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      content: msg,
      role: "user"
    });

    setMsg("");

    try {
      // the update of chatHistory requires a re-render, so we had to do this runtime workaround
      const reader = await sendMessageStream(useStore.getState().chatHistory, formatSystemPrompt(systemPrompt), modelConfig); // fetch reader
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

      // Store final assistant message
      addChat({
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        content: fullReply,
        role: "assistant"
      } as Message);
      setCharacterState("idle");

      // Clear the temporary stream text
      // clearStream();
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
  );
}
