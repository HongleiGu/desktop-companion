import axios from "axios";
import { useStore } from "../store/store";

export const sendMessage = async (message: string) => {
  const profile = useStore.getState().userProfile;
  const systemPrompt = useStore.getState().systemPrompt;

  const fullPrompt = `
昵称: ${profile.nickname}
生日: ${profile.birthday}
OC: ${profile.ocName}
关系: ${profile.relation}
---
系统提示词: ${systemPrompt}
---
用户: ${message}
`;

  const res = await axios.post("http://localhost:8000/chat", { text: fullPrompt });
  return res.data;
};

/**
 * Send a message to the FastAPI backend streaming endpoint.
 * Returns the fetch reader so the caller can read chunks manually.
 */
export const sendMessageStream = async (message: string): Promise<ReadableStreamDefaultReader<Uint8Array>> => {
  const profile = useStore.getState().userProfile;
  const systemPrompt = useStore.getState().systemPrompt;

  const fullPrompt = `
昵称: ${profile.nickname}
生日: ${profile.birthday}
OC: ${profile.ocName}
关系: ${profile.relation}
---
系统提示词: ${systemPrompt}
---
用户: ${message}
`;

  const response = await fetch("http://localhost:8000/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: fullPrompt }),
  });

  if (!response.body) {
    throw new Error("No response body from the streaming endpoint");
  }

  // Return the reader; caller handles streaming logic
  return response.body.getReader();
};

/**
 * Example helper function to read chunks from the reader
 * (can be used elsewhere in your code)
 */
export const readStreamChunks = async (
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onChunk: (chunk: string) => void
) => {
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? ""; // incomplete line

    for (const line of lines) {
      if (!line.startsWith("data:")) continue;
      const chunk = JSON.parse(line.replace(/^data:\s*/, ""));
      if (chunk.type === "token" && chunk.content) {
        onChunk(chunk.content);
      }
    }
  }
};
