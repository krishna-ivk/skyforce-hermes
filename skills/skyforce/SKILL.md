# Skill: Skyforce CLI Integration

## Description
This skill enables Hermes to interact with the Skyforce platform using the `sky` operator CLI. It allows the agent to check system status, search across repos, and inspect issues.

## Usage
When you need to understand the state of the Skyforce workspace, use the `sky` command.

### Commands
- `sky status`: Get a high-level summary of the fleet, nodes, and workflows.
- `sky search <query>`: Search for text across all repositories.
- `sky inspect <issue>`: View detailed information about a specific issue/ticket.
- `sky nodes`: List all active and known nodes in the system.
- `sky workflows`: View currently active orchestration workflows in Symphony.

## Implementation Detail
The `sky` command is located in `skyforce-core/scripts/sky.mjs`. It is typically aliased or run via `node`.

## Examples
- "Check the status of the workspace" -> `sky status`
- "Find where 'NodeRegistry' is defined" -> `sky search --code "NodeRegistry"`
- "What is the current state of ticker BUILD-12?" -> `sky inspect BUILD-12`
