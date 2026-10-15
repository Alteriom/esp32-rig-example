# AGENTS.md — esp32-rig-example

The smallest project an [Alteriom HIL rig](https://github.com/Alteriom/esp32-rig) can run, and the **Rig example** every rig ships as a built-in project: a firmware that answers the rig, a suite of three tests, and the workflow that builds the bundle the rig flashes. People copy it to start their own project, so it must stay small, readable and working. Public, Apache-2.0. Humans: start with `README.md`. For Claude Code, Copilot, Codex and Cursor alike (`CLAUDE.md` and `.github/copilot-instructions.md` point here). Keep this file short and true; update it in the pull request that makes it wrong.

## Where things live

| Path | What it holds |
|---|---|
| `src/main.cpp`, `platformio.ini` | the firmware (newline JSON over serial: `info`, `echo`, `sum`, `reset`), one PlatformIO env per family |
| `scripts/build_bundle.py` | the bundle a rig flashes: one merged image per family and `manifest.json` (schema 2) |
| `tests/` | the suite: pytest with the rig's `bank` fixture, one row per board, and the simulator's `sum` |
| `.github/workflows/` | `hil.yml` (builds the bundle, uploads `hil-artifacts`, optional hand-over), `suite.yml` (the suite against the rig's simulator at a pinned rig release), `icm-check.yml` |
| [`.github/icm/_shared/`](.github/icm/_shared/CONTEXT.md) | what every job below draws on, one file per question |
| [`.github/icm/01-fix/`](.github/icm/01-fix/CLAUDE.md) | fix a defect in the firmware, the bundle, the suite or a workflow |
| [`.github/icm/02-rig-release/`](.github/icm/02-rig-release/CLAUDE.md) | move the suite to a newer rig release |

## Route by what just happened

| Route | If | Go to | Then stop at |
|---|---|---|---|
| triage | an issue or report arrives and its kind is unclear | read it whole, then take the row below that fits | the row chosen, said to the person |
| fix | a defect is reported: a bundle a rig refuses, a test that fails on a good board, a family that does not build | [01_reproduce](.github/icm/01-fix/stages/01_reproduce/CONTEXT.md) | a person has seen the reproduction fail |
| ci-red | `HIL` or `Suite` is red on `main` | [01_reproduce](.github/icm/01-fix/stages/01_reproduce/CONTEXT.md), with the run log as the report | a person has seen the reproduction fail |
| rig-release | a newer rig release is out, or the suite should run against one | [01_check](.github/icm/02-rig-release/stages/01_check/CONTEXT.md) | a person approves the release to move to |
| defaults | the suite path, the workflow, the artifact name or the revision key is to change | [rules.md](.github/icm/_shared/rules.md) "The rig reads these defaults" | a person agrees the matching `Alteriom/esp32-rig` change before any edit |
| feature | something new is asked of the example | [rules.md](.github/icm/_shared/rules.md) "Keep it minimal" | a person decides whether it belongs here or in the rig |
| next | a stage's output was approved | the next numbered stage of the same job | a person reads that stage's output |
| status | asked for status | scan `.github/icm/*/stages/*/output/` | report what exists |

## Agents connecting remotely

This repository becomes the ICM workspace `esp32-rig-example` on MemoryRelay, created by a person from this repository's `main`; the Alteriom hub `portfolio` then delegates to it. Until the workspace exists, an agent on a clone reads these files directly: this file is the entry and the table above is the route. Once it exists, an agent that is not on a clone reaches the same files over MCP at `https://api.memoryrelay.net/mcp` with a key in `MEMORYRELAY_API_KEY`; none of it holds a secret.

- Start with `icm_context_build` for the route that fits (`{kind: "route", id: "fix"}`), not with the whole repository.
- Report what you read with `icm_report_reads` when a stage ends, and what the task came to with `icm_report_outcome`.
- Never write through MCP: a change is a branch and a pull request here, read and merged by a person.

## Rules

- Nothing moves to the next stage until a person has read the output of the last one.
- A stage writes to its own `output/`, which is not committed: one run per worktree or branch; clear that job's `stages/*/output/` when its pull request merges or is abandoned.
- `.github/icm/` points at the files that own each fact. When they disagree, the owning file is right: correct `.github/icm/` in the same pull request and bump its `verified_commit`.
- Public repository: no internal host name, address, token or private repository name, in code or in these files ([rules.md](.github/icm/_shared/rules.md)).
