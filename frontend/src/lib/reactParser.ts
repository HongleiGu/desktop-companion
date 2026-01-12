export type ParsedResult =
  | { type: "finish"; answer: string }
  | { type: "action"; tool: string; args: unknown }
  | { type: "error"; message: string };

export function parseReAct(text: string): ParsedResult {
  const lines = text.split("\n").map(l => l.trim());

  for (const line of lines) {
    if (line.startsWith("Finish")) {
      const match = line.slice("Finish[".length, -1).trim();
      return {
        type: "finish",
        answer: match?.[1] ?? ""
      };
    }

    if (line.includes("Action:")) {
      const raw = line.split("Action:")[1]!.trim();
      const name = raw.split("[")[0];
      const argStr = raw.slice(name.length + 1, -1);

      let args = {};
      try {
        args = argStr ? JSON.parse(argStr) : {};
      } catch {
        args = { input: argStr };
      }

      return {
        type: "action",
        tool: name,
        args
      };
    }
  }

  return { type: "error", message: "No Action or Finish found" };
}
