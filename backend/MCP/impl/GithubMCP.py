import subprocess
import json
import os

from MCP.remoteMCPProxy import RemoteMCPProxy

class GitHubMCP(RemoteMCPProxy):
    def __init__(self, github_token: str):
        # We pass the Token via environment variables, which is standard for MCP
        env = os.environ.copy()
        env["GITHUB_PERSONAL_ACCESS_TOKEN"] = github_token
        
        super().__init__(
            name="github",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env=env # Pass the token to the subprocess
        )

    def search_repo(self, query: str):
        """
        Example of a helper method. 
        In reality, the ReAct Agent will call 'call_tool' directly.
        """
        return self.call_tool("search_repositories", {"query": query})