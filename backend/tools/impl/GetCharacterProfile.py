from tools.base import Tool

class GetCharacterProfileTool(Tool):
    name = "get_character_profile"
    description = "Get the frontend character profile"
    execution = "frontend"

    @property
    def schema(self):
        return {
            "type": "object",
            "properties": "None",
            "return": {
                "birthday": {"type": "string"},
                "ocName": {"type": "string"},
                "relation": {"type": "string"},
                "speakingStyle": {"type": "string"},
                "personality": {"type": "string"},
                "description": {"type": "string"}
            },
            "additionalProperties": False
        }

    def execute(self):
        raise NotImplementedError("Client-side tool")
