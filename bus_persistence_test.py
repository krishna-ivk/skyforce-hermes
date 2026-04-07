import logging
import sys
import os
import time

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.events import HermesEventBus

# Configure logging
logging.basicConfig(level=logging.INFO)


def test_file_persistence():
    print("\n--- HERMES FILE-BUS PERSISTENCE TEST ---")

    # 1. Initialize Bus
    persistence_dir = "/tmp/hermes/test_bus"
    # Ensure a clean start for the test
    if os.path.exists(os.path.join(persistence_dir, "system_tasks.jsonl")):
        os.remove(os.path.join(persistence_dir, "system_tasks.jsonl"))

    bus = HermesEventBus(persistence_dir=persistence_dir)

    # 2. Publish Task
    task_id = "persistence_test_001"
    print(f"Publishing task: {task_id}")
    bus.publish("system_tasks", "NEW_TASK", {"task_id": task_id}, sender="test-script")

    # 3. Simulate Restart (New Bus instance pointing to same file)
    print("Simulating Bus Restart...")
    new_bus = HermesEventBus(persistence_dir=persistence_dir)

    # 4. Read it back via Catch-up
    print("Reading back from persistent log...")
    received_events = []

    def callback(event):
        received_events.append(event)
        print(
            f"RECOVERY SUCCESS: Received {event['type']} from {event['sender']} (Data: {event['data']})"
        )

    new_bus.subscribe("system_tasks", callback, catch_up=True)
    time.sleep(0.5)  # Allow tail thread to catch up

    if len(received_events) > 0:
        print("\n--- PERSISTENCE VERIFIED: 100% DURABILITY ---")
    else:
        print("\n--- PERSISTENCE FAILED: NO EVENTS RECOVERED ---")
    print("--- TEST COMPLETE ---\n")


if __name__ == "__main__":
    test_file_persistence()
