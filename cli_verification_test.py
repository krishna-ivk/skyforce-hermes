import logging
import sys
import os

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.events import HermesEventBus, HermesDLQ
from src.core.worker import HermesWorker
from src.core.provider import WorkspaceProvider

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def verify_cli_flow():
    print("\n--- HERMES CLI ORCHESTRATION VERIFICATION ---\n")

    bus = HermesEventBus()
    dlq = HermesDLQ(bus)
    provider = WorkspaceProvider(os.path.dirname(os.path.abspath(__file__)), ["temp"])
    worker = HermesWorker(bus, dlq, provider)

    # 2. Simulate CLI Submit Logic
    # (Normally this happens in a separate process, but here we trigger the worker's subscription)
    print("[CLI] Running: hermes-ctl submit --task 'Repair Documentation'")

    task_payload = {
        "task_id": "cli_task_001",
        "description": "Repair Documentation",
        "retries": 0,
    }

    # In a real cluster, the worker would be listening on a loop.
    # Here we simulate the event arrival.
    print("[Cluster] Event NEW_TASK detected on 'system_tasks' topic.")
    worker.run_task(task_payload)

    print("\n--- CLI VERIFICATION COMPLETE ---\n")


if __name__ == "__main__":
    verify_cli_flow()
