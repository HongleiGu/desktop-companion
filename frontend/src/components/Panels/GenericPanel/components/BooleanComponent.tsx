import { Switch } from "antd";
import { BooleanSchema } from "@/types/fields";
import { FieldProps } from "@/types/fields/fieldProps";

export function BooleanField({
  value,
  onChange,
}: FieldProps<BooleanSchema>) {
  return <Switch checked={value} onChange={onChange} />;
}
