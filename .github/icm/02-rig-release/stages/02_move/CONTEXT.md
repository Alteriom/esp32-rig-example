# 02_move — the one-line pull request, with the reason

One job: the pull request that moves `RIG_RELEASE` to the approved release and says why.

## Inputs
- Working (this run): `.github/icm/02-rig-release/stages/01_check/output/check.md`
- Reference (every run): `.github/icm/_shared/rules.md`

Do NOT load: the other pipelines, other runs' output.

## Process
1. Change `RIG_RELEASE` in `.github/workflows/suite.yml` to the approved release; nothing else in that file.
2. Leave `README.md` "On a rig" alone unless the release that first shipped this project is wrong; the release numbers there are facts about the rig, not pins ([rules.md](../../../_shared/rules.md) "The pinned rig release").
3. Write the pull request: subject `suite: run against rig release <version>`, the reason from `check.md`, and the suite's output against it.
4. After the human check, open it against `main` (`gh pr create --base main --body-file <this stage's output/move.md>`), then read the `Suite` result on it. The agent never merges.

## Outputs
- move.md → output/ — the title and body; the one-line diff; the `Suite` result on the pull request.

## Human check
A person reads `move.md` and the `Suite` result and merges, or says why not.
