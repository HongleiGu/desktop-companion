import { Card } from "antd";
import { useState } from "react";
import { ToolSpec } from "@/types/registry";
import { SchemaField } from "@/components/Panels/GenericPanel";
import { SchemaValue } from "@/types/fields/schemaValue";

export function ToolPanel<S extends ToolSpec>({
  tool,
}: {
  tool: S;
}) {
  const [args, setArgs] = useState<SchemaValue<S["schema"]>>(
    {} as SchemaValue<S["schema"]>
  );

  return (
    <Card size="small" title={tool.name} className="space-y-4">
      <p className="text-gray-500 text-sm">
        {tool.description}
      </p>

      <SchemaField
        schema={tool.schema}
        value={args}
        onChange={(e: unknown) => setArgs(e as SchemaValue<S["schema"]>)}
      />
    </Card>
  );
}
