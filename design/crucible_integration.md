# MorphOS Sandbox to Hermes Integration Blueprint

## 1. The PANOPTICON FORGE Proven Patterns
Throughout 12 experimental iterations inside `morphOS/forge`, the agentic framework generated critical self-healing requirements. These concepts, proven locally via threading, will now form the fundamental cluster architecture of **Skyforce Hermes**.

## 2. Hermes Node Architecture
Hermes Agents will be deployed as completely isolated, single-tenant, RAG-enabled microservices based directly on the Crucible Loop iterations:

### A. Semantic Memory Base (Iteration 002 & 005)
* **Gap**: 450MB raw context caused OOM/Context Bloat.
* **Hermes Implementation**: Hermes Agents will NOT load raw `README` or document files directly. Hermes must use a Vector DB (e.g., pgvector/Pinecone) to execute Top-K semantic chunk retrievals before passing context to LLM planning APIs.

### B. Sandbox Boundaries (Iteration 001 & 004)
* **Gap**: Agents modified unauthorized test suites trying to be "smart", crashing pipelines.
* **Hermes Implementation**: Hermes containers must run with explicit UNIX user permissions bound to `Workspace.ALLOWED_SCOPE` arrays. Write calls to paths outside this string array will raise strict Kernel-level rejections.

### C. A2A Synchronization (Iteration 003, 006, 007, 008)
* **Gap**: Race conditions & DB deadlocks when multiple sub-agents hit the same file simultaneously.
* **Hermes Implementation**: 
  - Central Redis-backed Distributed Locks.
  - Strict 30-second TTL Leases on locks.
  - Every active Hermes instance spawns a lightweight `HeartbeatDaemon` thread which connects to Redis and renews the TTL every 10 seconds.
  - If a Hermes node fails its health check or crashes, TTL expires, and the locked file is released to the event queue.

### D. Event Bus & DLQ (Iteration 009, 010, 011, 012)
* **Gap**: Synchronous polling blocked threads. Bad inputs poisoned the entire loop. Dropped payloads were lost silently.
* **Hermes Implementation**:
  - Implementation of **Hermes Bus** (e.g., Apache Kafka / Redis Streams).
  - All tasks are PubSub broadcasts.
  - `MAX_RETRIES = 3` header embedded into the Hermes Node specification.
  - Failed messages are sent to a dedicated Dead-Letter Queue (DLQ).
  - Hermes Alerter Daemon streams the Discard Bin directly into a #skyforce-alerts webhook.

## 3. Deployment Strategy
To execute this blueprint, `skyforce-hermes` will phase out standard API calls and become a pure Event-Sourced Agent cluster based on these 4 architectural pillars.
