import { Button, Card } from "antd";
import { PlusOutlined, DeleteOutlined } from "@ant-design/icons";
import { ArraySchema } from "@/types/fields";
import { FieldProps } from "@/types/fields/fieldProps";
import { SchemaField } from "..";
import { SchemaValue } from "@/types/fields/schemaValue";

export function ArrayField({
  schema,
  value,
  onChange,
}: FieldProps<ArraySchema>) {
  return (
    <div className="space-y-2">
      {value.map((item, idx) => (
        <Card
          key={idx}
          size="small"
          className="flex gap-2 items-start"
        >
          <div className="flex-1">
            <SchemaField
              schema={schema.items}
              value={item}
              onChange={(v: unknown) => {
                const copy = [...value] as SchemaValue<typeof schema.items>[];
                copy[idx] = v as SchemaValue<typeof schema.items>;
                onChange(copy as SchemaValue<ArraySchema>);
              }}
            />
          </div>

          <Button
            danger
            type="text"
            icon={<DeleteOutlined />}
            onClick={() =>
              onChange(value.filter((_, i) => i !== idx) as SchemaValue<ArraySchema>)
            }
          />
        </Card>
      ))}

      <Button
        type="dashed"
        icon={<PlusOutlined />}
        onClick={() => {
          // Use schema.default or provide empty default based on type
          const defaultValue = schema.items.default ?? 
            (schema.items.type === "string" ? "" :
             schema.items.type === "number" ? 0 :
             schema.items.type === "boolean" ? false :
             schema.items.type === "array" ? [] :
             schema.items.type === "object" ? {} : undefined);
          
          onChange([...value, defaultValue] as SchemaValue<ArraySchema>);
        }}
        block
      >
        Add item
      </Button>
    </div>
  );
}