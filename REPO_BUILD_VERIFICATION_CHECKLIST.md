# Skyforce Hermes Repo Build Verification Checklist

## Purpose

This checklist verifies `skyforce-hermes` as the Hermes-oriented setup and integration surface.

## Repo Role

This repo should own:

- Hermes setup and bootstrap
- workspace context for Hermes
- integration notes for linking Hermes into Skyforce
- Hermes-oriented local demo and smoke scripts

It should not become:

- the primary code-build runtime
- the main orchestration runtime
- the main operator surface

## Required Local Prerequisites

- Python 3
- shell access for `setup-hermes.sh`
- Hermes upstream prerequisites where applicable

## Setup Verification

- [ ] setup script is present and readable
- [ ] AGENTS context file is present
- [ ] integration notes are present

Suggested commands:

```bash
cd /home/vashista/skyforce/skyforce-hermes
ls -1 setup-hermes.sh AGENTS.md LINKING_ACTIONS.md README.md
```

## Build And Runtime Verification

Because this repo is primarily an integration surface, verification is lighter and focused on setup health.

- [ ] setup script can be invoked
- [ ] local Hermes control entrypoint exists

Suggested commands:

```bash
cd /home/vashista/skyforce/skyforce-hermes
bash setup-hermes.sh
ls -1 bin/hermes-ctl
```

## Test Verification

The repo currently exposes Python test and demo scripts rather than a single packaged test harness.

Suggested verification commands:

```bash
cd /home/vashista/skyforce/skyforce-hermes
python3 integration_smoke_test.py
python3 cli_verification_test.py
python3 final_integration_test.py
```

Optional additional spot checks:

```bash
cd /home/vashista/skyforce/skyforce-hermes
python3 bus_persistence_test.py
python3 redis_test.py
```

## Repo-Specific Verification Checklist

- [ ] Hermes remains documented as the preferred setup path, not the primary build runtime
- [ ] the split-node posture described in the README still matches reality
- [ ] setup and integration notes still point at current Skyforce repos and boundaries

## Pass Condition

Treat `skyforce-hermes` as repo-healthy when:

- setup artifacts are present
- Hermes bootstrap path is intact
- smoke and verification scripts run cleanly
- the repo still behaves as an integration surface rather than a second runtime
