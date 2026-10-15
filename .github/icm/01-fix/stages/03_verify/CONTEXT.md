# 03_verify — both workflows' checks, the pull request

One job: the pull request a reviewer can merge, with what `HIL` and `Suite` will run already green.

## Inputs
- Working (this run): `.github/icm/01-fix/stages/02_fix/output/change.md`
- Reference (every run): `.github/icm/_shared/build-and-test.md`
- Reference (only when the fix changes what a reader of the README would do): `.github/icm/_shared/documents.md`

Do NOT load: the other pipelines, other runs' output.

## Process
1. Run the suite against the simulator at the pinned rig release, and build the bundle for the families the change touches, or say that `hil.yml` builds all four and read its result after pushing ([build-and-test.md](../../../_shared/build-and-test.md)).
2. Update `README.md` if the change made a line there wrong.
3. Write the pull request: what was wrong, how you know, what the change does, the checks and results, what only a rig run can prove. The subject says what changed for someone forking the example.
4. After the human check, open it against `main` (`gh pr create --base main --body-file <this stage's output/pull-request.md>`). The agent never merges.

## Outputs
- pull-request.md → output/ — the title and body; the checks run with results; any rig run, or why none.

## Human check
A person reads `pull-request.md` and the `HIL` and `Suite` results and says whether to open it; the reviewer merges, knowing every rig's built-in example follows `main`.
