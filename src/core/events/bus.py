import json
import logging
import os
import time
import threading
from typing import Callable, Any, Dict, Optional

import redis

logger = logging.getLogger(__name__)


class HermesEventBus:
    """
    Redis-backed Event Bus with File-based Fallback.

    Primary mode uses Redis pub/sub for multi-container coordination.
    Falls back to file-backed JSONL tailing when Redis is unavailable.
    """

    def __init__(
        self,
        redis_url: Optional[str] = None,
        persistence_dir: str = "/tmp/hermes/bus",
    ):
        self.persistence_dir = persistence_dir
        os.makedirs(self.persistence_dir, exist_ok=True)
        self.stop_events: Dict[str, threading.Event] = {}
        self._redis: Optional[redis.Redis] = None
        self._pubsub: Optional[redis.client.PubSub] = None
        self._listener_threads: Dict[str, threading.Thread] = {}

        redis_url = redis_url or os.getenv(
            "HERMES_REDIS_URL", "redis://localhost:6379/0"
        )

        try:
            self._redis = redis.from_url(
                redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            self._redis.ping()
            self._mode = "redis"
            logger.info(f"Initialized Hermes Redis Event Bus at {redis_url}")
        except (redis.ConnectionError, redis.TimeoutError, OSError) as exc:
            logger.warning(
                f"Redis unavailable ({exc}), falling back to file-backed bus at {self.persistence_dir}"
            )
            self._redis = None
            self._mode = "file"

    # -- Public API ----------------------------------------------------------

    @property
    def mode(self) -> str:
        return self._mode

    def publish(self, topic: str, event_type: str, data: Any, sender: str = "Unknown"):
        payload = {
            "timestamp": time.time(),
            "type": event_type,
            "sender": sender,
            "data": data,
        }

        if self._mode == "redis":
            self._publish_redis(topic, payload)
        else:
            self._publish_file(topic, payload)

    def subscribe(
        self,
        topic: str,
        callback: Callable[[Dict[str, Any]], None],
        catch_up: bool = True,
    ):
        if self._mode == "redis":
            self._subscribe_redis(topic, callback, catch_up)
        else:
            self._subscribe_file(topic, callback, catch_up)

    def close(self):
        for stop_event in self.stop_events.values():
            stop_event.set()
        for thread in self._listener_threads.values():
            thread.join(timeout=2)
        if self._pubsub:
            self._pubsub.close()
        if self._redis:
            self._redis.close()
        logger.info("HermesEventBus closed")

    # -- Redis mode ----------------------------------------------------------

    def _publish_redis(self, topic: str, payload: Dict):
        channel = f"hermes:{topic}"
        self._redis.publish(channel, json.dumps(payload))
        self._redis.rpush(f"hermes:log:{topic}", json.dumps(payload))
        logger.info(f"Published {payload['type']} to {channel}")

    def _subscribe_redis(self, topic: str, callback: Callable, catch_up: bool):
        channel = f"hermes:{topic}"
        stop_event = threading.Event()
        self.stop_events[topic] = stop_event

        if catch_up:
            log_key = f"hermes:log:{topic}"
            try:
                messages = self._redis.lrange(log_key, 0, -1)
                for raw in messages:
                    callback(json.loads(raw))
            except (redis.ConnectionError, redis.TimeoutError):
                logger.warning(f"Could not catch up on {log_key}")

        thread = threading.Thread(
            target=self._redis_listener,
            args=(channel, callback, stop_event),
            daemon=True,
        )
        thread.start()
        self._listener_threads[topic] = thread
        logger.info(f"Subscribed to {channel} via Redis pub/sub")

    def _redis_listener(
        self, channel: str, callback: Callable, stop_event: threading.Event
    ):
        pubsub = self._redis.pubsub()
        pubsub.subscribe(channel)
        try:
            while not stop_event.is_set():
                message = pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=0.5
                )
                if message and message["type"] == "message":
                    try:
                        callback(json.loads(message["data"]))
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON on {channel}")
        finally:
            pubsub.unsubscribe(channel)
            pubsub.close()

    # -- File fallback mode --------------------------------------------------

    def _publish_file(self, topic: str, payload: Dict):
        log_path = os.path.join(self.persistence_dir, f"{topic}.jsonl")
        with open(log_path, "a", buffering=1) as f:
            f.write(json.dumps(payload) + "\n")
            os.fsync(f.fileno())
        logger.info(f"Published {payload['type']} to {topic} (file)")

    def _subscribe_file(self, topic: str, callback: Callable, catch_up: bool):
        stop_event = threading.Event()
        self.stop_events[topic] = stop_event

        thread = threading.Thread(
            target=self._tail_log,
            args=(topic, callback, catch_up, stop_event),
            daemon=True,
        )
        thread.start()
        logger.info(f"Subscribed to {topic} with file tailing")

    def _tail_log(
        self,
        topic: str,
        callback: Callable,
        catch_up: bool,
        stop_event: threading.Event,
    ):
        log_path = os.path.join(self.persistence_dir, f"{topic}.jsonl")

        if not os.path.exists(log_path):
            with open(log_path, "w"):
                pass

        with open(log_path, "r") as f:
            if catch_up:
                for line in f:
                    if line.strip():
                        callback(json.loads(line))
            else:
                f.seek(0, os.SEEK_END)

            while not stop_event.is_set():
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                if line.strip():
                    callback(json.loads(line))
