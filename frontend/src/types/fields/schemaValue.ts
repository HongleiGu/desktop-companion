// schemaValue.ts
import {
  JSONSchema,
  StringSchema,
  NumberSchema,
  BooleanSchema,
  ArraySchema,
  ObjectSchema,
} from "@/types/fields";

export type SchemaValue<S extends JSONSchema> =
  S extends StringSchema ? string :
  S extends NumberSchema ? number :
  S extends BooleanSchema ? boolean :
  S extends ArraySchema ? SchemaValue<S["items"]>[] :
  S extends ObjectSchema ? Record<string, unknown> :
  never;
