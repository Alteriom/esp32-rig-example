---
verified_at: 2026-10-15
verified_commit: b2bbfc6d683b7aa0763ed8110670c6c81c523d37
---

# Rules that are easy to break, and the conventions

Each rule names the file that holds it.

## The rig reads these defaults

Suite path `tests`, workflow `.github/workflows/hil.yml`, artifact `hil-artifacts`, revision key `git_sha` (`README.md` "On a rig", step 2). The rig's built-in "Rig example" project is written against them (`profiles/rig-example.yaml` in `Alteriom/esp32-rig`, which follows `main` of this repository), and a project added from this URL gets them as its defaults. Changing one needs the same change in the rig's profile, in the rig release that ships it; agree that change before editing here.

## The revision key holds the commit

`manifest.json` records the commit the bundle was built from under `git_sha` (`REVISION_KEY` in `scripts/build_bundle.py`; `hil.yml` prints it). The rig refuses a bundle whose revision does not match the commit it asked for, so the key and its value are not decoration.

## Whatever boards the user chose

A run is scoped to the families the user chose; the suite must pass whatever boards it is given, and never assume a family is present. One row per board comes from `tests/conftest.py` (`pytest_generate_tests`, `board`); the tests ask a board what it is rather than expecting one (`tests/test_it_answers.py`).

## The pinned rig release

`RIG_RELEASE` in `.github/workflows/suite.yml` is moved deliberately, to a published rig release, with the reason in the pull request (pipeline `02-rig-release`). `README.md` names the release that first shipped this project ("On a rig", step 2); that line changes only if the fact does.

## Keep it minimal

This is a template people fork: small, readable, working. A new capability belongs in the rig, not here; the example shows the shape (`src/main.cpp` says to replace `sum` and keep `info` and the framing; `scripts/build_bundle.py` is about a hundred lines and "yours to change").

## Conventions

- Small pull requests, squash-merged; the subject says what changed for someone forking the example.
- Public repository: no internal host name, address, token or private repository name in code, workflows or these files. A rig's address and key reach `hil.yml` only as the repository secrets `RIG_URL` and `RIG_KEY`.
