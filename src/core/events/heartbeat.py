import time
import threading
import logging
from typing import Optional

import redis

logger = logging.getLogger(__name__)


class HermesHeartbeat:
    """
    Active Heartbeat daemon for Hermes Agents.
    Renews Redis TTL leases while long-running tasks execute.
    Falls back to no-op when Redis is unavailable.
    """

    def __init__(
        self,
        agent_id: str,
        lock_key: str,
        ttl: float = 30.0,
        redis_url: Optional[str] = None,
    ):
        self.agent_id = agent_id
        self.lock_key = lock_key
        self.ttl = ttl
        self.stop_event = threading.Event()
        self.thread: Optional[threading.Thread] = None
        self._redis: Optional[redis.Redis] = None

        redis_url = redis_url or "redis://localhost:6379/0"

        try:
            self._redis = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            self._redis.ping()
            self._mode = "redis"
            logger.info(f"Heartbeat connected to Redis at {redis_url}")
        except (redis.ConnectionError, redis.TimeoutError, OSError) as exc:
            logger.warning(
                f"Redis unavailable for heartbeat ({exc}), operating in no-op mode"
            )
            self._redis = None
            self._mode = "noop"

    def start(self):
        if self._mode == "noop":
            return
        logger.info(
            f"Starting heartbeat for agent {self.agent_id} on lock {self.lock_key}"
        )
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        if self._mode == "noop":
            return
        if self.thread:
            self.stop_event.set()
            self.thread.join()
            logger.info(f"Stopped heartbeat for agent {self.agent_id}")

    def _run(self):
        while not self.stop_event.is_set():
            try:
                self._redis.expire(self.lock_key, int(self.ttl))
                logger.debug(f"Renewed TTL for {self.lock_key} (ID: {self.agent_id})")
            except (redis.ConnectionError, redis.TimeoutError) as exc:
                logger.warning(f"Heartbeat renewal failed for {self.lock_key}: {exc}")
            time.sleep(self.ttl / 3.0)
