// this is the single global instance registry that handles the config of all the tools and config

import { JSONSchema } from "@/types/fields";

export interface ToolSpec {
  id: string;                 // "github:create_issue"
  name: string;               // "create_issue"
  description: string;
  execution: "backend" | "frontend";
  schema: JSONSchema;
}

// registry types
export interface MCPSpec {
  name: string;
  enabled: boolean;
  type: "remote" | "local";
  // configSchema: JSONSchema;   // 👈 editable
  config: Record<string, unknown>;
  env?: Record<string, string>;
  tools: ToolSpec[];
}


export interface UnifiedRegistrySpec {
  mcps: Record<string, MCPSpec>;
  tools: Record<string, ToolSpec>; // standalone tools
}
