import { InputNumber } from "antd";
import { NumberSchema } from "@/types/fields";
import { FieldProps } from "@/types/fields/fieldProps";

export function NumberField({
  schema,
  value,
  onChange,
}: FieldProps<NumberSchema>) {
  return (
    <InputNumber
      className="w-full"
      value={value}
      placeholder={schema.description}
      onChange={(v) => onChange(v ?? 0)}
    />
  );
}
