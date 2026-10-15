# 01_check — the suite against the new rig release

One job: say whether this suite passes against a newer rig release's simulator, and what changed in the rig that a project would notice.

## Inputs
- Working (this run): the candidate release — `gh release list --repo Alteriom/esp32-rig --limit 5`, and the current `RIG_RELEASE` in `.github/workflows/suite.yml`.
- Reference (every run): `.github/icm/_shared/build-and-test.md`
- Reference (every run): `.github/icm/_shared/rules.md`

Do NOT load: the other pipelines, other runs' output.

## Process
1. Name the candidate: a published rig release newer than `RIG_RELEASE`, with both wheels attached (`gh release view v<version> --repo Alteriom/esp32-rig`).
2. Read its release notes and the rig's changes since the current pin for anything a project notices: the `bank` fixture or board client, the simulator, the bundle manifest a rig accepts, the defaults the rig reads ([rules.md](../../../_shared/rules.md)).
3. Install that release's two wheels in a clean venv and run the suite against the simulator ([build-and-test.md](../../../_shared/build-and-test.md)). Keep the output.
4. If it fails, decide whose it is: this suite (a fix here, through `01-fix`) or the rig (an issue there). Do not move the pin past a failing suite.

## Outputs
- check.md → output/ — the candidate release; what changed for a project; the suite's output against it; the recommendation (move, or not and why).

## Human check
A person approves the release to move to, or decides not to move.
