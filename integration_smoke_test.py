import logging
import sys
import time
import os

# Ensure the parent directory is in the path so we can import src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.events import HermesEventBus, HermesDLQ
from src.core.worker import HermesWorker
from src.core.provider import WorkspaceProvider

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def run_integration_test():
    print("\n--- STARTING HERMES INTEGRATION SMOKE TEST ---\n")

    # 1. Initialize Infrastructure
    bus = HermesEventBus()
    dlq = HermesDLQ(bus)
    provider = WorkspaceProvider(os.path.dirname(os.path.abspath(__file__)), ["temp"])
    worker = HermesWorker(bus, dlq, provider)

    # 2. Test Case A: Clean Success
    print("\n[TEST A] Sequential Success Task")
    success_task = {
        "task_id": "hermes_task_001",
        "type": "code_repair",
        "description": "Clean repair of utils/parser.py",
        "retries": 0,
    }
    worker.run_task(success_task)

    # 3. Test Case B: DLQ & Alert Routing
    print("\n[TEST B] Poison Pill Task (Triggering DLQ -> Discard -> Alert)")
    fail_task = {
        "task_id": "hermes_task_fatal",
        "type": "orchestration",
        "description": "Poison pill that crashes the worker loop.",
        "force_fail": True,
        "retries": 3,  # Start at max retries to force discard binary logic
    }
    worker.run_task(fail_task)

    print("\n--- SMOKE TEST COMPLETE ---\n")


if __name__ == "__main__":
    run_integration_test()
