from tools.base import Tool

class GetTimeTool(Tool):
    name = "get_time"
    description = "Get the current system time"
    execution = "backend"

    def args_schema(self):
        return {"type": "object", "properties": {}}

    def execute(self):
        from datetime import datetime
        return datetime.now().isoformat()