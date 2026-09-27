# AGENTS.md — esp32-rig-example

Instructions for AI coding agents (Claude Code, Copilot, Codex, Cursor). Humans: start with README.md.

## What this repo is

The smallest project an [Alteriom HIL rig](https://github.com/Alteriom/esp32-rig) can run, and the
**Rig example** every rig ships as a built-in project. It is copied by people starting their own
project, so it must stay small, readable and working. Public, Apache-2.0.

One of four repositories that must stay consistent:

| Repo | Role |
|---|---|
| `Alteriom/esp32-rig` (public) | The rig software; pins this repo's suite behaviour and ships it as "Rig example" |
| `Alteriom/esp32-hil-firmware` (public) | The Rig Health Check firmware, pinned by the rig |
| `Alteriom/esp32-rig-example` (this) | Example firmware + suite + bundle workflow |
| The Alteriom farm portal (a private repository) | Consumes rig releases |

## Where to look

| Question | File |
|---|---|
| The firmware protocol (newline JSON over serial: `info`, `echo`, `sum`, `reset`) | `src/main.cpp` |
| Which families build, and how | `platformio.ini` (one env per family) |
| How the bundle the rig flashes is made | `scripts/build_bundle.py` (manifest schema 2, one merged image per family) |
| The suite | `tests/` (pytest, the rig's `bank` fixture, one row per board) |
| Build + hand-over workflow the rig fetches from | `.github/workflows/hil.yml` (artifact name `hil-artifacts`) |
| CI against the rig's simulator | `.github/workflows/suite.yml` (`RIG_RELEASE` pins the rig release it installs) |

## Commands

```bash
python -m pip install platformio esptool
python scripts/build_bundle.py --out hil-artifacts --target esp32     # one family
# The suite against the rig's simulator, with the rig's wheels from a release:
base=https://github.com/Alteriom/esp32-rig/releases/download/v1.0.179
python -m pip install "$base/alteriom_hil_core-1.0.179-py3-none-any.whl" "$base/alteriom_hil-1.0.179-py3-none-any.whl" pytest
ALTERIOM_HIL_MODE=sim python -m pytest tests -q -p no:cacheprovider
```

## Rules

- **The rig reads these defaults.** Suite path `tests`, workflow `.github/workflows/hil.yml`, artifact
  `hil-artifacts`, revision key `git_sha`. The rig's built-in "Rig example" project assumes them;
  changing one needs the same change in `esp32-rig` (`profiles/rig-example.yaml`) in the same release.
- **The manifest's revision key is `git_sha`** and must hold the commit the bundle was built from;
  the rig refuses a bundle whose revision does not match the commit it asked for.
- **Tests must pass whatever boards the user selected.** A run is scoped to the families the user
  chose; never assume a family (e.g. esp32-c5) is present.
- **Move `RIG_RELEASE` in `suite.yml` deliberately**, to a published rig release, and say why in the PR.
- Keep it minimal: this is a template. New features belong in the rig, not here.
- Public repo: no internal hostnames, IPs, tokens or private repo names.

## Conventions

Small PRs, squash-merged. Commit subject says what changed for someone forking the example.
