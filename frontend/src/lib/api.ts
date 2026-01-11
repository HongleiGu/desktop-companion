import { ChatConfig, ChatRequest, Message } from "../types/chat";
import { buildSystemPrompt } from "../utils/chat";

export const sendMessage = async (
  messages: Message[],
  systemPrompt: string,
  config: ChatConfig,
  files?: File[],
  stream: boolean = false
): Promise<string> => {
  const formData = tidyChatRequest(messages, systemPrompt, config, stream, files)
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  return data.content;
};

export const sendMessageStream = async (
  messages: Message[],
  systemPrompt: string,
  config: ChatConfig,
  files?: File[],
  stream: boolean = false
): Promise<ReadableStreamDefaultReader<Uint8Array>> => {
  const formData = tidyChatRequest(messages, systemPrompt, config, stream, files)
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    body: formData,
  });

  if (!res.body) throw new Error("No stream body");

  return res.body.getReader(); // caller can read chunks incrementally
};


export const tidyChatRequest = (messages: Message[], systemPrompt: string, config: ChatConfig, stream: boolean, files?: File[]) => {
  // Build logical object
  const req: ChatRequest = {
    ...config,
    messages: [buildSystemPrompt(systemPrompt), ...messages],
    stream,
  };

  // Build FormData
  const formData = new FormData();
  formData.append("payload", JSON.stringify(req));
  if (files) files.forEach((f) => formData.append("files", f));
  return formData
}

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
