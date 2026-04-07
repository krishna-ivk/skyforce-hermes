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

def run_mission_004():
    print("\n--- HERMES SELF-HEALING MISSION 004 (EVALUATOR) ---\n")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Start Two Daemons: One Worker, One Evaluator
    print("[SYSTEM] Starting Worker Node (NODE_EXEC)...")
    worker_node = HermesDaemon(root_dir, ["temp"], role="worker")
    worker_node.start()

    print("[SYSTEM] Starting Evaluator Node (NODE_QC)...")
    eval_node = HermesDaemon(root_dir, ["temp"], role="evaluator")
    eval_node.start()

    time.sleep(1)

    # 2. Submit a Task that will FAIL validation (Deliberate ERROR in content)
    print("\n[CLI] Submitting Malicious Task (intentional bad syntax)...")
    task_payload = {
        "task_id": "mission_004_target",
        "description": "Ensure temp/critical.cfg has PORT=ERROR_MARKER",
        "retries": 0
    }
    
    worker_node.bus.publish("system_tasks", "NEW_TASK", task_payload, sender="hermes-ctl")
    
    # Sequence: 
    # 1. Worker picks it up -> reasoning -> write 'PORT=ERROR_MARKER' -> publish completion.
    # 2. Evaluator picks up completion -> sees 'ERROR' -> publishes 'correction_mission_004_target'.
    # 3. Worker picks up correction -> Reasoning engine (Iteration 023) fixes it.
    
    print("\n[MONITOR] Awaiting feedback loop (Worker -> Evaluator -> Worker)...")
    time.sleep(3)
    
    print("\n--- MISSION 004 COMPLETE ---\n")

if __name__ == "__main__":
    run_mission_004()
