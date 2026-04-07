import logging
import sys
import os

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.daemon import HermesDaemon

# Configure logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

def run_mission_simulation():
    print("\n--- HERMES LIVE MISSION 001 (AGENT DISPATCH) ---\n")
    
    # 1. Start Daemon (Persistent Node)
    # Root: skyforce-hermes. Scope: ['temp', 'AGENTS.md']
    root_dir = os.path.dirname(os.path.abspath(__file__))
    daemon = HermesDaemon(root_dir, ["temp", "AGENTS.md"])
    daemon.start()
    
    # 2. Simulate CLI Submit (hermes-ctl submit --task 'Update Agent context')
    print("\n[CLI] hermes-ctl submit --task 'Update Agent context' --id 'mission_001'")
    task_payload = {
        "task_id": "mission_001",
        "description": "Update Agent context to include Crucible Iterations.",
        "retries": 0
    }
    
    # Publishing to the bus (The daemon callback is synchronous in this mock)
    daemon.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    print("\n--- MISSION 001 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_simulation()
