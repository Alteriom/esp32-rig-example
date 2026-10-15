---
verified_at: 2026-10-15
verified_commit: b2bbfc6d683b7aa0763ed8110670c6c81c523d37
---

# Build, test, and what counts as evidence

What CI runs is `.github/workflows/hil.yml` and `.github/workflows/suite.yml`; read their steps rather than copying them anywhere. The person's version is `README.md` "Building it yourself".

## Build a bundle, run the suite

```bash
python -m pip install platformio esptool
python scripts/build_bundle.py --out hil-artifacts --target esp32     # one family; omit --target for all four
# The suite against the rig's simulator, with the rig's wheels from the release suite.yml pins:
RIG_RELEASE=1.0.179
base=https://github.com/Alteriom/esp32-rig/releases/download/v$RIG_RELEASE
python -m pip install "$base/alteriom_hil_core-$RIG_RELEASE-py3-none-any.whl" "$base/alteriom_hil-$RIG_RELEASE-py3-none-any.whl"
ALTERIOM_HIL_MODE=sim ALTERIOM_HIL_SIM_BOARDS=2 python -m pytest tests -q -p no:cacheprovider
```

Take `RIG_RELEASE` from the `env` of `suite.yml`, never from memory: it is the release CI installs (1.0.179 at the verified commit). Both wheels go on one command line, which is what satisfies the rig package's dependency on the core without an index. The suite needs `alteriom_hil` importable (`tests/conftest.py` imports its simulator); without the wheels nothing collects.

## What CI runs, and when

| Workflow | Runs | On |
|---|---|---|
| `hil.yml` `bundle` | `scripts/build_bundle.py --out hil-artifacts` for every family, uploads `hil-artifacts`; hands it to a rig only when the variable `HAND_OVER_TO_RIG` is `true` and the secrets `RIG_URL` and `RIG_KEY` are set, never on a pull request | every pull request and push to `main` |
| `suite.yml` `sim` | the suite against the rig's simulator with two simulated boards, at `RIG_RELEASE` | every pull request and push to `main` |
| `icm-check.yml` | the workspace files compile to the ICM standard | changes to the entry files or `.github/icm/`; weekly with `--strict` |

## Evidence

- A simulated pass is evidence about the suite, never about a board: the tests carry `hil_only` (`tests/test_it_answers.py`, the docstring of `tests/conftest.py`).
- A board's behaviour is proven by a run on a rig: the project's page, Get firmware from GitHub, then a run, three green rows per board (`README.md` "On a rig").
- A bundle is proven by `hil.yml` building every family and printing the manifest's `git_sha` and targets ("Say what was built").
