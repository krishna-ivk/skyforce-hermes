import logging
import uuid
from typing import Dict, Any, Optional
from .events import HermesEventBus, HermesDLQ, HermesHeartbeat
from .provider import WorkspaceProvider
from .tools import HermesToolset
from .agent import HermesAgent

logger = logging.getLogger(__name__)

class HermesWorker:
    """
    Orchestrates the lifecycle of an Agentic Task within the Hermes cluster.
    """
    def __init__(self, event_bus: HermesEventBus, dlq: HermesDLQ, provider: WorkspaceProvider):
        self.bus = event_bus
        self.dlq = dlq
        self.provider = provider
        self.tools = HermesToolset(provider)
        self.agent = HermesAgent()
        self.worker_id = f"hermes-worker-{uuid.uuid4().hex[:8]}"
        logger.info(f"Worker {self.worker_id} initialized.")

    def run_task(self, event_envelope: Dict[str, Any]):
        """
        Executes a task with full Crucible Layer protection.
        """
        task_payload = event_envelope.get("data", event_envelope)
        task_id = task_payload.get("task_id", "unknown")
        logger.info(f"[{self.worker_id}] Starting task {task_id}")

        # 1. Start Heartbeat
        lock_key = f"lock:task:{task_id}"
        heartbeat = HermesHeartbeat(self.worker_id, lock_key)
        heartbeat.start()

        try:
            # 2. Execute Logic
            results = self._execute_logic(task_payload)

            # 3. Publish Success
            completion_data = {
                "task_id": task_id,
                "results": results
            }
            self.bus.publish("task_completions", "TASK_FINISHED", completion_data, sender=self.worker_id)
            logger.info(f"[{self.worker_id}] Task {task_id} completed successfully.")

        except Exception as e:
            # 4. Route to DLQ
            logger.error(f"[{self.worker_id}] Task {task_id} FAILED: {e}")
            self.dlq.route_to_dlq(task_payload, e)

        finally:
            # 5. Cleanup
            heartbeat.stop()

    def _execute_logic(self, payload: Dict[str, Any]):
        """
        Executes a sequence of tool calls or engages the Reasoning Engine.
        """
        tool_calls = payload.get("tool_calls", [])
        
        # Autonomous Planning Phase
        if not tool_calls and "description" in payload:
            logger.info(f"[{self.worker_id}] No explicit tool calls. Engaging Reasoning Engine...")
            tool_calls = self.agent.plan(payload["description"])

        results = []
        if not tool_calls:
            raise ValueError("No plan formulated. Agent reached an impasse.")

        # Execution Phase
        for call in tool_calls:
            try:
                result = self.tools.execute_tool(call["name"], call["params"])
                results.append({"tool": call["name"], "status": "success", "output": result})
            except Exception as e:
                logger.error(f"[{self.worker_id}] Tool {call['name']} failed: {e}")
                results.append({"tool": call["name"], "status": "error", "message": str(e)})
                raise

        return results
