// fieldProps.ts
import { JSONSchema } from ".";
import { SchemaValue } from "./schemaValue";

export interface FieldProps<S extends JSONSchema> {
  schema: S;
  value: SchemaValue<S>;
  onChange: (value: SchemaValue<S>) => void;
}
