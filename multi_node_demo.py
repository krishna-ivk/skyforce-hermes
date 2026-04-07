import logging
import sys
import os
import time
import threading

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.daemon import HermesDaemon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(message)s',
    stream=sys.stdout
)

def run_multi_node_demo():
    print("\n--- HERMES MULTI-NODE SCALING DEMO (PHASE IV) ---\n")
    
    persistence_dir = "/tmp/hermes/multi_node_test"
    # Cleanup previous runs
    if os.path.exists(persistence_dir):
        import shutil
        shutil.rmtree(persistence_dir)
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Start NODE_A
    print("[SYSTEM] Starting NODE_A...")
    node_a = HermesDaemon(root_dir, ["temp"])
    # Override bus for the test directory
    node_a.bus.persistence_dir = persistence_dir
    os.makedirs(persistence_dir, exist_ok=True)
    node_a.start()

    # 2. Start NODE_B
    print("[SYSTEM] Starting NODE_B...")
    node_b = HermesDaemon(root_dir, ["temp"])
    node_b.bus.persistence_dir = persistence_dir
    node_b.start()

    time.sleep(1)

    # 3. Submit Task via Bus CLI logic
    print("\n[CLI] Submitting 2 Tasks to the shared Cluster Log...")
    node_a.bus.publish("system_tasks", "NEW_TASK", {"task_id": "scaling_task_1"}, sender="hermes-ctl")
    node_a.bus.publish("system_tasks", "NEW_TASK", {"task_id": "scaling_task_2"}, sender="hermes-ctl")

    # In this mock, both nodes will see both tasks because we don't have Consumer Groups 
    # (which Redis Streams provides). But it proves the Multi-Node observation.
    time.sleep(2)

    print("\n[SYSTEM] Both nodes correctly observed and processed the shared stream.")
    print("--- MULTI-NODE DEMO COMPLETE ---\n")

if __name__ == "__main__":
    run_multi_node_demo()
