import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class HermesAgent:
    """
    The Reasoning Engine for Hermes Workers.
    Simulates LLM-based autonomous planning.
    Architected from Iteration 023.
    """
    def __init__(self):
        logger.info("Hermes Reasoning Engine initialized.")

    def plan(self, description: str) -> List[Dict[str, Any]]:
        """
        Translates natural language intent into a sequence of tool calls.
        """
        logger.info(f"Reasoning about task: '{description}'")
        plan = []

        # 1. Pattern: "Ensure <path> exists and has <content>"
        # Using a more flexible regex for 'has'
        match_ensure = re.search(r"Ensure\s+([\w/\.-]+)\s+.*has\s+(.*)", description, re.IGNORECASE)
        if match_ensure:
            path = match_ensure.group(1).strip()
            content = match_ensure.group(2).strip()
            logger.info(f"Plan Formulation: Enforcing content in {path}")
            plan.append({"name": "write_file", "params": {"path": path, "content": content}})
            plan.append({"name": "read_file", "params": {"path": path}})
            return plan

        # 2. Pattern: "Fix typo in <path>" or "Update <path>"
        if "fix" in description.lower() or "update" in description.lower():
            path_match = re.search(r"in ([\w/\.-]+)", description)
            if path_match:
                path = path_match.group(1)
                logger.info(f"Plan Formulation: Patching {path}")
                plan.append({"name": "read_file", "params": {"path": path}})
                plan.append({"name": "write_file", "params": {"path": path, "content": "# Updated by Hermes Agent\n"}})
                return plan

        logger.warning("No specific pattern matched. Aborting plan.")
        return []
