import logging
import sys
import os
import time

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.daemon import HermesDaemon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    stream=sys.stdout
)

def run_mission_005():
    print("\n--- HERMES OPENCLAW INTEGRATION MISSION 005 ---\n")
    
    # The OpenClaw directory is at /home/vashista/skyforce/openclaw
    # We must allow the worker to scope into it.
    root_dir = "/home/vashista/skyforce"
    allowed_scope = ["skyforce-hermes/temp", "openclaw"]
    
    daemon = HermesDaemon(root_dir, allowed_scope)
    daemon.start()
    
    # MISSION: Use only Natural Language to fix the fake log issue.
    print("\n[CLI] Submitting Task 'mission_005_openclaw'...")
    task_payload = {
        "task_id": "mission_005_openclaw",
        "description": "Fix typo in openclaw/hermes_test.log",
        "retries": 0
    }
    
    daemon.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    print("\n[MONITOR] Awaiting Reasoning & Execution (Target: OpenClaw Workspace)...")
    time.sleep(3)
    
    # Verify the fix
    print("\n[VERIFY] Checking the result in OpenClaw...")
    verify_path = "/home/vashista/skyforce/openclaw/hermes_test.log"
    if os.path.exists(verify_path):
        with open(verify_path, 'r') as f:
            print(f"Content: {f.read().strip()}")
    
    print("\n--- MISSION 005 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_005()
