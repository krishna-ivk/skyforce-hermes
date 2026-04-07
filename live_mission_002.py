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

def run_mission_002():
    print("\n--- HERMES LIVE MISSION 002 (TOOL EXECUTION) ---\n")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # Scope: Allow access to 'temp'
    daemon = HermesDaemon(root_dir, ["temp"])
    daemon.start()
    
    # 1. Mission: Write a file and then Read it back
    print("\n[CLI] Submitting Multi-Tool Task 'mission_002'...")
    task_payload = {
        "task_id": "mission_002",
        "description": "Write a config file and verify its contents.",
        "tool_calls": [
            {
                "name": "write_file",
                "params": {"path": "temp/config.env", "content": "NODE_ENV=production\nHERMES_PORT=8080"}
            },
            {
                "name": "read_file",
                "params": {"path": "temp/config.env"}
            }
        ],
        "retries": 0
    }
    
    daemon.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    # Let the daemon process the sequence
    import time
    time.sleep(1.5)
    
    print("\n--- MISSION 002 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_002()
