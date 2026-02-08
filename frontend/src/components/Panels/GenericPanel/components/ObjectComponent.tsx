import { Card } from "antd";
import { ObjectSchema } from "@/types/fields";
import { FieldProps } from "@/types/fields/fieldProps";
import { SchemaField } from "..";

export function ObjectField({
  schema,
  value,
  onChange,
}: FieldProps<ObjectSchema>) {
  return (
    <Card size="small" className="space-y-4">
      {Object.entries(schema.properties ?? {}).map(([key, propSchema]) => (
        <div key={key} className="grid grid-cols-4 gap-4 items-start">
          <label className="col-span-1 text-sm font-medium text-gray-700">
            {key}
            {schema.required?.includes(key) && (
              <span className="text-red-500 ml-1">*</span>
            )}
          </label>

          <div className="col-span-3">
            <SchemaField
              schema={propSchema}
              value={value[key]}
              onChange={(v) =>
                onChange({ ...value, [key]: v })
              }
            />
          </div>
        </div>
      ))}
    </Card>
  );
}
