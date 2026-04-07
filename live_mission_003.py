import logging
import sys
import os

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.daemon import HermesDaemon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    stream=sys.stdout
)

def run_mission_003():
    print("\n--- HERMES AUTONOMOUS MISSION 003 (REASONING) ---\n")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    daemon = HermesDaemon(root_dir, ["temp"])
    daemon.start()
    
    # MISSION: Use only Natural Language. No explicit tool calls provided.
    print("\n[CLI] Submitting Intent-only Task 'mission_003'...")
    task_payload = {
        "task_id": "mission_003",
        "description": "Ensure temp/runtime.lock exists and has STATE=ACTIVE",
        "retries": 0
    }
    
    daemon.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    import time
    time.sleep(2)
    
    print("\n--- MISSION 003 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_003()
