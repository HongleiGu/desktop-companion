from tools.base import Tool

class UpdateCharacterProfileTool(Tool):
    name = "update_character_profile"
    description = "Update the character's profile information shown to the user."
    execution = "frontend"

    def args_schema(self):
        return {
            "type": "object",
            "properties": {
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
