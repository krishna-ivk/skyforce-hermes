# Hermes Linking Actions & Integration Points

This document outlines the specific actions to integrate Hermes Agent into the Skyforce ecosystem.

## 1. Symphony: Hermes as the Communications Runtime
**Context**: Symphony routes communication-oriented and support tasks to Hermes while keeping implementation and build execution on the local build node.
**Action**: 
- Register Hermes as the communications/support agent on the EC2 comms node.
- Route implementation, code build, and validation work to the local build node instead of Hermes.

## 2. Harness: MCP Tool Integration
**Context**: Harness provides execution adapters and supports the Model Context Protocol (MCP).
**Action**:
- Keep MCP-backed execution/build tools attached to the local build node.
- Expose only the bounded communication/support tool surface to Hermes on EC2.

## 3. morphOS: Hermes Agent Archetype
**Context**: morphOS defines the "Agent Archetypes" and workflows.
**Action**:
- Create `morphOS/agents/hermes.md` defining the Hermes persona and its specific capabilities.
- Add Hermes-optimized prompt templates to `morphOS/workflows/`.

## 4. Skyforce-Core: Hermes Skills System
**Context**: Hermes has a built-in skills system.
**Action**:
- Create Hermes-facing skills that support communication, drafting, and triage flows.
- Keep implementation/build-oriented `sky` operations on the local execution node unless explicitly bridged.

## 5. Command Centre: Telemetry Alignment
**Context**: Command Centre displays execution receipts and receipts from Symphony.
**Action**:
- Ensure Hermes communication sessions and local build-node execution both report progress in a format Symphony can normalize into shared artifacts.
