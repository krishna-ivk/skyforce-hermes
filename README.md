# Skyforce Hermes Integration

> [!WARNING]
> **Status**: Preferred setup path
> Use this repo as the current Hermes-oriented setup and integration surface for Skyforce agent work.

This directory contains the setup script, workspace context, and integration notes for the [Hermes Agent](https://github.com/NousResearch/hermes-agent) in the Skyforce workspace.

## Current Topology

Skyforce currently uses Hermes in a split-node posture:

- EC2 comms node: `3.235.173.182` (AWS Linux `t3.micro`)
- SSH key path from this workspace: `~/.ssh/hermes.pem`
- Hermes role on EC2: communication, support drafting, and triage support
- Local role on this device: execution, code build, and validation

Hermes should be treated as the comms/runtime edge, not the primary code-build surface.

## Setup

To get started with Hermes in this workspace:

1. **Run the setup script**:
   ```bash
   ./setup-hermes.sh
   ```
   This installs Hermes from the upstream project and prepares the local CLI.

2. **Reload your shell**:
   ```bash
   source ~/.bashrc
   ```

3. **Start Hermes with Skyforce Context**:
    ```bash
     hermes --workspace-target ./AGENTS.md
    ```

If you are operating Hermes on the EC2 comms node, connect first with your key:

```bash
ssh -i ~/.ssh/hermes.pem ec2-user@3.235.173.182
```

4. **Optional first-run bootstrap**:
   ```bash
   hermes setup
   ```
   Use the Hermes setup flow to import or initialize local configuration before connecting it to Symphony or other Skyforce tooling.

## Files in this Directory

- `setup-hermes.sh`: Automated installation script.
- `AGENTS.md`: Workspace context for Hermes to understand the Skyforce architecture.
- `LINKING_ACTIONS.md`: Current integration notes for Symphony, Harness, `morphOS`, and `skyforce-core`.
- `REPO_BUILD_VERIFICATION_CHECKLIST.md`: Repo-specific build, smoke, and verification checklist.
- `README.md`: This file.
