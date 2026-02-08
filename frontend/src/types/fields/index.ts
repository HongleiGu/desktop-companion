// schema.ts
export type JSONSchemaType =
  | "string"
  | "number"
  | "integer"
  | "boolean"
  | "object"
  | "array";

export interface BaseSchema {
  type: JSONSchemaType;
  description?: string;
  enum?: readonly string[];
  default?: unknown;
  // required: boolean;
}

export interface StringSchema extends BaseSchema {
  type: "string";
}

export interface NumberSchema extends BaseSchema {
  type: "number" | "integer";
}

export interface BooleanSchema extends BaseSchema {
  type: "boolean";
}

export interface ArraySchema extends BaseSchema {
  type: "array";
  items: JSONSchema;
}

export interface ObjectSchema extends BaseSchema {
  type: "object";
  properties?: Record<string, JSONSchema>;
  required?: readonly string[];
  additionalProperties?: boolean;
}

export type JSONSchema =
  | StringSchema
  | NumberSchema
  | BooleanSchema
  | ArraySchema
  | ObjectSchema;

export interface FieldProps<Type, Schema> {
  schema: Schema;
  value: Type;
  onChange: (value: Type) => void;
}
