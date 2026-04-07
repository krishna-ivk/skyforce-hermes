import logging
import os
from typing import List, Dict, Any
from .provider import WorkspaceProvider

logger = logging.getLogger(__name__)

class HermesToolset:
    """
    A collection of safe developer tools for Hermes Workers.
    Encapsulates interactions with the WorkspaceProvider.
    """
    def __init__(self, provider: WorkspaceProvider):
        self.provider = provider

    def execute_tool(self, name: str, params: Dict[str, Any]) -> str:
        """Dispatches a tool call to the correct handler."""
        logger.info(f"Executing tool: {name} with params: {params}")
        
        if name == "read_file":
            return self.provider.read_file(params["path"])
        elif name == "write_file":
            self.provider.write_file(params["path"], params["content"])
            return f"Successfully wrote to {params['path']}"
        elif name == "list_dir":
            full_path = os.path.join(self.provider.root_dir, params.get("path", "."))
            if not self.provider._is_allowed(full_path):
                raise PermissionError(f"Access to {params.get('path')} is restricted.")
            return str(os.listdir(full_path))
        else:
            raise ValueError(f"Unknown tool: {name}")

class ToolResult:
    def __init__(self, tool_name: str, result: str, success: bool = True, error: str = None):
        self.tool_name = tool_name
        self.result = result
        self.success = success
        self.error = error

    def to_dict(self):
        return {
            "tool": self.tool_name,
            "result": self.result,
            "success": self.success,
            "error": self.error
        }
