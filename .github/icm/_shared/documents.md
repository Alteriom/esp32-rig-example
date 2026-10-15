---
verified_at: 2026-10-15
verified_commit: b2bbfc6d683b7aa0763ed8110670c6c81c523d37
---

# Documents — what a person reads here, and who owns its facts

The agent-facing files are `AGENTS.md` (the entry) and this folder. The document below restates facts that code or a workflow owns; the owner is right when they disagree. It is pinned in the workspace, so an agent can be given it by path.

| Document | What it answers | Owner of the facts |
|---|---|---|
| [README.md](../../../README.md) | what the example is, the files, using it on a rig, what a rig expects of a firmware and a bundle, building it | `src/main.cpp`, `scripts/build_bundle.py`, `tests/conftest.py`, `.github/workflows/hil.yml`, `.github/workflows/suite.yml` |

The rig's guide explains projects in general (the "Projects and your CI" page published from `Alteriom/esp32-rig`) and links here as the project to copy.

## Known drift

None in `README.md` at the verified commit. One question is open for a person, recorded here because no file answers it: the optional hand-over in `hil.yml` posts with `profile=esp32-rig-example`, the name a project added from this URL gets, while the rig's built-in copy is named `rig-example`. Whether the hand-over reaches the built-in project was not checked against a rig.
