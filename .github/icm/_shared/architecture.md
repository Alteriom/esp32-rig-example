---
verified_at: 2026-10-15
verified_commit: b2bbfc6d683b7aa0763ed8110670c6c81c523d37
---

# Architecture — where to look

A map for finding the file that owns a fact. What the example is for and how a rig uses it: `README.md` "On a rig".

## Four repositories, kept consistent

| Repository | Role |
|---|---|
| `Alteriom/esp32-rig-example` (this) | the example firmware, its suite and the workflow that builds its bundle |
| `Alteriom/esp32-rig` | the rig software: ships this repository as its built-in "Rig example" project (`profiles/rig-example.yaml` there) and publishes the releases whose packages this suite installs |
| `Alteriom/esp32-hil-firmware` | the Rig Health Check firmware a rig pins; unrelated to this project's firmware |
| the farm portal (a private repository) | consumes rig releases |

## Where to look

| Question | Where |
|---|---|
| the protocol the firmware answers (newline JSON: `info`, `echo`, `sum`, `reset`; a `boot` event per start) | the header comment and dispatch of `src/main.cpp` |
| which families build, and how | `platformio.ini`, one `[env:<family>]` each (esp32, esp32-c3, esp32-s3, esp8266) |
| how the bundle is made: merged images, `manifest.json` schema 2, the commit under `git_sha` | `scripts/build_bundle.py` (`TARGETS`, `REVISION_KEY`) |
| one test row per board, and the simulator taught `sum` | `tests/conftest.py` |
| the three tests | `tests/test_it_answers.py` |
| the bundle a rig fetches, and the optional hand-over to a rig | `.github/workflows/hil.yml` (artifact `hil-artifacts`) |
| the suite against the rig's simulator, at a pinned rig release | `.github/workflows/suite.yml` (`RIG_RELEASE`) |
| what a rig expects of a firmware and of a bundle | `README.md` "What the rig expects of a firmware", "What the rig expects of a bundle" |
