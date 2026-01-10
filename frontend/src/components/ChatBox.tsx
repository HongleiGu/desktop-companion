"use client";

import { useState } from "react";
import { Button, Input, Space } from "antd";
import { useStore } from "../store/store";
import { sendMessageStream } from "../lib/api";

export default function ChatBox() {
  const [msg, setMsg] = useState("");
  const addChat = useStore((s) => s.addChat);
  const setStreamText = useStore((s) => s.setStreamText);
  const clearStream = useStore((s) => s.clearStream);

  const handleSend = async () => {
    if (!msg.trim()) return;

    // Clear previous typewriter stream
    clearStream();

    // Add user message
    addChat({
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      message: msg,
    });

    setMsg("");

    try {
      const reader = await sendMessageStream(msg); // fetch reader
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
        id: (Date.now() + 1).toString(),
        timestamp: new Date().toISOString(),
        message: fullReply,
      });

      // Clear the temporary stream text
      // clearStream();
    } catch (err) {
      console.error(err);
      addChat({
        id: (Date.now() + 2).toString(),
        timestamp: new Date().toISOString(),
        message: "（她好像没有回应…）",
      });
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
