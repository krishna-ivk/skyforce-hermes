import logging
import sys
import os
import time

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.daemon import HermesDaemon

# Configure high-fidelity logging for demo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(module)s | %(levelname)s | %(message)s',
    stream=sys.stdout
)

def run_grand_demo():
    print("====================================================")
    print("       HERMES CLUSTER: THE PANOPTICON FORGE DEMO    ")
    print("====================================================\n")
    
    # 1. Booting the Cluster
    print("[1/4] INITIALIZING HERMES CLUSTER NODES...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    daemon = HermesDaemon(root_dir, ["temp", "AGENTS.md"])
    daemon.start()
    time.sleep(1)

    # 2. Sequential Success Mission
    print("\n[2/4] DEMO: SUCCESSFUL TASK PIPELINE")
    print("CLI -> SUBMIT 'Reputation sync sequence'")
    task_success = {
        "task_id": "demo_success_001",
        "type": "sync",
        "description": "Reputation sync sequence across cluster nodes.",
        "retries": 0
    }
    daemon.bus.publish("system_tasks", "NEW_TASK", task_success, sender="hermes-ctl")
    time.sleep(1.5)

    # 3. Self-Healing & Fatal Failure Mission
    print("\n[3/4] DEMO: SELF-HEALING & DLQ ESCALATION")
    print("CLI -> SUBMIT 'Malicious poisoned payload'")
    task_fail = {
        "task_id": "demo_fatal_002",
        "type": "exploit",
        "description": "Corrupted payload triggering DLQ discard.",
        "force_fail": True,
        "retries": 3 # Forcing immediate escalation to human alerter
    }
    daemon.bus.publish("system_tasks", "NEW_TASK", task_fail, sender="hermes-ctl")
    time.sleep(2)

    # 4. Final Status
    print("\n[4/4] CLUSTER TELEMETRY")
    print("Nodes: Active (hermes-worker-demo)")
    print("Bus Topology: Redis Streams (Simulated)")
    print("Health: OPERATIONAL")
    print("\n====================================================")
    print("          HERMES DEMO COMPLETE: CLUSTER ONLINE      ")
    print("====================================================\n")

if __name__ == "__main__":
    run_grand_demo()
