import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class WorkspaceProvider:
    """
    Handles real-world file-system interaction for Hermes Agents.
    Architectured from Iteration 001 and 004 Scoped Sandbox findings.
    """
    def __init__(self, root_dir: str, allowed_scope: List[str]):
        self.root_dir = os.path.abspath(root_dir)
        self.allowed_scope = [os.path.join(self.root_dir, s) for s in allowed_scope]
        logger.info(f"WorkspaceProvider initialized at {self.root_dir} with scope: {allowed_scope}")

    def read_file(self, relative_path: str) -> str:
        """Reads a file if it is within the allowed scope."""
        full_path = os.path.abspath(os.path.join(self.root_dir, relative_path))
        
        if not self._is_allowed(full_path):
            logger.error(f"Permission Denied: {relative_path} is out of scope.")
            raise PermissionError(f"Access to {relative_path} is restricted by the Hermes Sandbox.")

        with open(full_path, "r") as f:
            return f.read()

    def write_file(self, relative_path: str, content: str):
        """Writes a file ONLY if it is within the allowed scope."""
        full_path = os.path.abspath(os.path.join(self.root_dir, relative_path))
        
        if not self._is_allowed(full_path):
            logger.error(f"Permission Denied: Writing to {relative_path} is restricted.")
            raise PermissionError(f"Modification of {relative_path} is restricted by the Hermes Sandbox.")

        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        logger.info(f"Successfully modified: {relative_path}")

    def _is_allowed(self, target_path: str) -> bool:
        """Helper to check if path is within allowed substrings."""
        return any(target_path.startswith(scope) for scope in self.allowed_scope)
