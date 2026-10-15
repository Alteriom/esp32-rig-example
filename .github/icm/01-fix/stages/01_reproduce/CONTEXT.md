# 01_reproduce — reproduce the reported defect

One job: turn the report into something that fails on demand, for the reason reported, and say whether it is this repository's.

## Inputs
- Working (this run): the report — read whole with what it links: an issue (`gh issue view <n> --comments`), a red run (`gh run view <run-id> --log-failed`), a rig's run report and serial capture, a bundle a rig refused.
- Reference (every run): `.github/icm/_shared/architecture.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`

Do NOT load: the other pipelines, other runs' output.

## Process
1. Restate the report as observed versus expected: which family, which test or command, what the board said, which rig release.
2. Decide whose it is. A refused bundle, a wrong `git_sha` or a family that does not build is this repository's; a fixture, the simulator or the board client misbehaving at the pinned rig release is the rig's (`Alteriom/esp32-rig`): stop with the reproduction for that repository.
3. Find the code with [architecture.md](../../../_shared/architecture.md) and name the suspected cause as `path:line`.
4. Reproduce it the cheapest way that shows the cause: the suite against the simulator at the pinned rig release, a bundle built for one family, or a rig run's evidence ([build-and-test.md](../../../_shared/build-and-test.md)).
5. Run it and keep the failing output.

## Outputs
- reproduction.md → output/ — the restated report; whose it is and why; suspected cause (`path:line`); the command; the failing output; what only a rig can show.

## Human check
A person runs the command, or reads the evidence, and confirms it fails for the reported reason and that the cause is in this repository.
