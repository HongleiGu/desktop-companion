import json
from core.registry import UnifiedRegistry
from models.spec import UnifiedRegistrySpec

DATA: UnifiedRegistrySpec = UnifiedRegistrySpec.model_validate_json("""
{
  "mcps": {
    "github": {
      "enabled": true,
      "type": "remote",
      "config": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"]
      },
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "GITHUB_SECRET"
      }
    }
  },
  "tools": {}
}
""")


if __name__ == '__main__':
  registry = UnifiedRegistry(spec=DATA)
  # registry.register_from_spec(spec=DATA)
  with open('./UnifiedRegistryInit.json', 'w') as f:
    json.dump(registry.runtime_view(), f, indent=4)
    f.write('\n\n')
