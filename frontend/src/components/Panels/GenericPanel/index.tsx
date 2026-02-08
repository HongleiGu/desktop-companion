import {
  JSONSchema,
  StringSchema,
  NumberSchema,
  ArraySchema,
  ObjectSchema,
  FieldProps,
  BooleanSchema
} from "@/types/fields"
import { StringField } from "./components/StringComponent";
import { ArrayField } from "./components/ArrayComponent";
import { BooleanField } from "./components/BooleanComponent";
import { NumberField } from "./components/NumberComponent";
import { ObjectField } from "./components/ObjectComponent";
import { SchemaValue } from "@/types/fields/schemaValue";
import { getSchemaDefaultValue } from "@/types/fields/defaults";
import { inferJSONSchema } from "@/types/fields/inferSchema";

export function SchemaField({ schema, value, onChange }: FieldProps<unknown, JSONSchema>) {
  console.log(schema, value)
  if (!schema) {
    schema = inferJSONSchema(value)
  }
  switch (schema.type) {
    case "string":
      return (
        <StringField
          schema={schema as StringSchema}
          value={value as SchemaValue<StringSchema> ?? getSchemaDefaultValue(schema)}
          onChange={onChange}
        />
      );

    case "number":
    case "integer":
      return (
        <NumberField
          schema={schema as NumberSchema}
          value={value as SchemaValue<NumberSchema> ?? getSchemaDefaultValue(schema)}
          onChange={onChange}
        />
      );

    case "boolean":
      return (
        <BooleanField
          schema={schema as BooleanSchema}
          value={value as SchemaValue<BooleanSchema> ?? getSchemaDefaultValue(schema)}
          onChange={onChange}
        />
      );

    case "array":
      return (
        <ArrayField
          schema={schema as ArraySchema}
          value={value as SchemaValue<ArraySchema> ?? getSchemaDefaultValue(schema)}
          onChange={onChange}
        />
      );

    case "object":
      return (
        <ObjectField
          schema={schema as ObjectSchema}
          value={value as SchemaValue<ObjectSchema> ?? getSchemaDefaultValue(schema)}
          onChange={onChange}
        />
      );
  }
}
