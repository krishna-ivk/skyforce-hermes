import logging
import sys
import os
import time
from typing import Dict, Any
from .events import HermesEventBus, HermesDLQ
from .worker import HermesWorker
from .provider import WorkspaceProvider
from .evaluator import HermesEvaluator

logger = logging.getLogger(__name__)

class HermesDaemon:
    """
    The persistent runtime for a Hermes Node.
    Listens to the Event Bus and spawns workers for incoming tasks.
    """
    def __init__(self, root_dir: str, allowed_scope: list, role: str = "worker"):
        self.bus = HermesEventBus()
        self.dlq = HermesDLQ(self.bus)
        self.provider = WorkspaceProvider(root_dir, allowed_scope)
        self.role = role
        if role == "evaluator":
            self.evaluator = HermesEvaluator(self.bus)
        self.running = False

    def start(self):
        """Initializes the daemon and starts the listening loop."""
        logger.info(f"Hermes Daemon ({self.role}) starting...")
        
        if self.role == "worker":
            logger.info("Subscribing to 'system_tasks'")
            self.bus.subscribe("system_tasks", self._on_task_received)
        elif self.role == "evaluator":
            logger.info("Subscribing to 'task_completions'")
            self.bus.subscribe("task_completions", self._on_completion_received)

        self.running = True
        logger.info("Daemon is IDLE. Awaiting events...")

    def _on_task_received(self, event: Dict[Any, Any]):
        """Callback for new tasks on the Event Bus."""
        logger.info(f"Task received: {event['type']} from {event['sender']}")
        worker = HermesWorker(self.bus, self.dlq, self.provider)
        worker.run_task(event)

    def _on_completion_received(self, event: Dict[Any, Any]):
        """Callback for completed tasks on the Event Bus (Evaluator Role)."""
        logger.info(f"Completion report received: {event['type']}")
        self.evaluator.evaluate_completion(event)
        
    def stop(self):
        self.running = False
        logger.info("Hermes Daemon shutting down.")
