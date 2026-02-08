// utils/schemaDefaults.ts
import { JSONSchema } from "."

export function getSchemaDefaultValue(schema: JSONSchema) {
  if (schema.default !== undefined) return schema.default;
  
  switch (schema.type) {
    case "string": return "";
    case "number": 
    case "integer": return 0;
    case "boolean": return false;
    case "array": return [];
    case "object": return {};
    default: return undefined;
  }
}