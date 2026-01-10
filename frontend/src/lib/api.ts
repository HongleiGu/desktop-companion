import axios from "axios";
import { ChatConfig, ChatRequest, Message } from "../types/chat";
import { buildSystemPrompt } from "../utils/chat";

export const sendMessage = async (messages: Message[], systemPrompt: string, config: ChatConfig): Promise<string> => {

  const req: ChatRequest = {
    ...config,
    messages: [buildSystemPrompt(systemPrompt), ...messages],
    stream: false,
  };

  const res = await axios.post("http://localhost:8000/chat", req);
  return res.data.content;
};

// of course we can directly fetch from the central store, but for flexibility, we add the params
export const sendMessageStream = async (messages: Message[], systemPrompt: string, config: ChatConfig) => {

  const req: ChatRequest = {
    ...config,
    messages: [buildSystemPrompt(systemPrompt), ...messages],
    stream: true,
  };

  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!res.body) throw new Error("No stream body");
  return res.body.getReader();
};


/**
 * Example helper function to read chunks from the reader
 * (can be used elsewhere in your code)
 */
export const readStreamChunks = async (
  reader: ReadableStreamDefaultReader<Uint8Array>,
  onChunk: (chunk: string, prev: string) => void
) => {
  const decoder = new TextDecoder();
  let buffer = "";
  let accumulated = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      if (!part.startsWith("data:")) continue;
      const json = part.replace(/^data:/, "");
      const chunk = JSON.parse(json);

      if (chunk.type === "token") {
        accumulated += chunk.content;
        onChunk(chunk.content, accumulated);
      }
    }
  }
};
