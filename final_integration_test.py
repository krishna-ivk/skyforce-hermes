import logging
import sys
import os

# Setup path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core import HermesEventBus, HermesDLQ, WorkspaceProvider, HermesWorker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

def run_final_verification():
    print("\n--- HERMES FINAL E2E VERIFICATION (PHASE III) ---\n")
    
    # 1. Initialize Infrastructure
    bus = HermesEventBus()
    dlq = HermesDLQ(bus)
    
    # Scope: Only allow access to 'skyforce-hermes/temp'
    # Use relative path for the sandbox root
    root_dir = os.path.dirname(os.path.abspath(__file__))
    provider = WorkspaceProvider(root_dir, ["temp"])
    
    worker = HermesWorker(bus, dlq, provider)
    
    # Ensure temp dir exists
    os.makedirs(os.path.join(root_dir, "temp"), exist_ok=True)

    # 2. Test Case A: Allowed Write
    print("\n[TEST A] Writing to Allowed Path (temp/manifest.json)")
    success_task = {
        "task_id": "verified_task_001",
        "type": "documentation",
        "description": "Create a manifest file in the temp directory."
    }
    
    # Simulate worker logic using the provider
    try:
        worker.provider.write_file("temp/manifest.json", '{"status": "verified"}')
        print("Success: File written to sandbox.")
    except Exception as e:
        print(f"Failure: {e}")

    # 3. Test Case B: Blocked Write (Sandbox Enforcement)
    print("\n[TEST B] Attempting to Write Out-of-Scope (README.md)")
    blocked_task = {
        "task_id": "malicious_task_002",
        "type": "exploit",
        "description": "Try to overwrite the project README."
    }
    
    try:
        worker.provider.write_file("README.md", "HACKED")
        print("Failure: Sandbox was bypassed!")
    except PermissionError as e:
        print(f"Success: Sandbox correctly blocked the write: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print("\n--- FINAL VERIFICATION COMPLETE ---\n")

if __name__ == "__main__":
    run_final_verification()
