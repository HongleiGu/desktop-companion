import { Input, Select } from "antd";
import { StringSchema } from "@/types/fields";
import { FieldProps } from "@/types/fields/fieldProps";

export function StringField({
  schema,
  value,
  onChange,
}: FieldProps<StringSchema>) {
  if (schema.enum) {
    return (
      <Select
        className="w-full"
        value={value}
        placeholder={schema.description}
        options={schema.enum.map(v => ({ label: v, value: v }))}
        onChange={onChange}
      />
    );
  }

  return (
    <Input
      value={value}
      placeholder={schema.description}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}
