import logging
import sys
import os
import time

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.events import HermesEventBus

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_redis_persistence():
    print("\n--- HERMES REDIS PERSISTENCE TEST ---")
    
    # 1. Connect to Real Redis
    try:
        bus = HermesEventBus()
    except Exception as e:
        print(f"FAILED to connect to Redis: {e}")
        return

    # 2. Publish Task
    task_id = "persistence_test_001"
    print(f"Publishing task: {task_id}")
    bus.publish("system_tasks", "NEW_TASK", {"task_id": task_id}, sender="test-script")

    # 3. Read it back
    print("Reading back from stream...")
    def callback(event):
        print(f"RECOVERY SUCCESS: Received {event['type']} from {event['sender']} (Data: {event['data']})")

    bus.subscribe("system_tasks", callback)
    print("--- TEST COMPLETE ---\n")

if __name__ == "__main__":
    test_redis_persistence()
