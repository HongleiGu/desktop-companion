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
      if (lines.includes("Action: Finish[")) {
        return {
          type: "finish",
          answer: line.split("Action:")[1]!.slice(0, -1).trim()
        } as ParsedResult
      }
      const raw = line.split("Action:")[1]!.trim();
      const name = raw.split("[")[0].trim();
      const argStr = raw.split("[")[1].slice(0, -1);
      console.log(name, argStr)

      let args = {};
      try {
        args = argStr ? JSON.parse(argStr) : {};
      } catch {
        try {
          // somtimmes the brackets are missing
          args = argStr ? JSON.parse('{'+argStr+'}') : {};

        } catch {
          args = { input: argStr };
        }
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
