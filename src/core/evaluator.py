import logging
import json
from typing import Dict, Any
from .events import HermesEventBus

logger = logging.getLogger(__name__)

class HermesEvaluator:
    """
    Quality Control Agent for the Hermes Cluster.
    """
    def __init__(self, event_bus: HermesEventBus):
        self.bus = event_bus

    def evaluate_completion(self, completion_event: Dict[str, Any]):
        """
        Inspects a completed task. 
        """
        task_data = completion_event.get("data", {})
        task_id = task_data.get("task_id", "unknown")
        results = task_data.get("results", [])
        
        logger.info(f"Evaluating completion of task: {task_id}")

        triggered_retry = False
        for res in results:
            output = str(res.get("output", ""))
            if "ERROR" in output or "FAIL" in output:
                logger.warning(f"Validation FAILED for {task_id}. Triggering auto-correction.")
                self._trigger_correction(task_data)
                triggered_retry = True
                break

        if not triggered_retry:
            logger.info(f"Validation PASSED for {task_id}.")

    def _trigger_correction(self, original_data: Dict[str, Any]):
        """Publishes a new task to correct the detected failure."""
        task_id = original_data.get("task_id", "unknown")
        correction_task = {
            "task_id": f"correction_{task_id}",
            "description": f"FIX: Previous task {task_id} failed validation. Remove 'ERROR/FAIL' markers.",
            "retries": (original_data.get("retries", 0) + 1)
        }
        self.bus.publish("system_tasks", "NEW_TASK", correction_task, sender="hermes-evaluator")
