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

def run_mission_006():
    print("\n--- HERMES LIVE SERVICE MAINTENANCE: MISSION 006 ---\n")
    
    root_dir = "/home/vashista/skyforce"
    allowed_scope = ["skyforce-hermes/temp", "openclaw"]
    
    daemon = HermesDaemon(root_dir, allowed_scope)
    daemon.start()
    
    # MISSION: Patch the live operational log of OpenClaw
    print("\n[CLI] Submitting Live Maintenance Task 'mission_006'...")
    task_payload = {
        "task_id": "mission_006_live",
        "description": "Update openclaw/openclaw.mjs and add a Hermes-Handshake comment",
        "retries": 0
    }
    
    daemon.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    print("\n[MONITOR] Awaiting Autonomous Patching on LIVE service file...")
    time.sleep(5)
    
    print("\n[VERIFY] Checking the patch in openclaw.mjs...")
    verify_path = "/home/vashista/skyforce/openclaw/openclaw.mjs"
    if os.path.exists(verify_path):
        with open(verify_path, 'r') as f:
            lines = f.readlines()
            print(f"Top 5 lines: {lines[:5]}")
    
    print("\n--- MISSION 006 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_006()
