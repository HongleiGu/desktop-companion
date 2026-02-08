import { JSONSchema } from ".";

// Recursive function to infer your JSONSchema from a value
export function inferJSONSchema(value: unknown): JSONSchema {
  if (Array.isArray(value)) {
    return {
      type: "array",
      items: value.length > 0 ? inferJSONSchema(value[0]) : { type: "string" },
    };
  }

  if (value !== null && typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const properties: Record<string, JSONSchema> = {};
    for (const [k, v] of Object.entries(obj)) {
      properties[k] = inferJSONSchema(v);
    }
    return {
      type: "object",
      properties,
      required: Object.keys(properties),
      additionalProperties: false,
    };
  }

  switch (typeof value) {
    case "string":
      return { type: "string" };
    case "number":
      return { type: "number" };
    case "boolean":
      return { type: "boolean" };
    default:
      return { type: "string" };
  }
}
