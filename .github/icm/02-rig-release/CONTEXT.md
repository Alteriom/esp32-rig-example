# 02-rig-release — the pipeline

Check the new rig release against the suite, then move the pin deliberately.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| [`01_check`](stages/01_check/CONTEXT.md) | the suite against the new rig release | the candidate release | `output/check.md` | A person approves the release to move to, or decides not to move. |
| [`02_move`](stages/02_move/CONTEXT.md) | the one-line pull request, with the reason | 01_check's `check.md` | `output/move.md` | A person reads `move.md` and the `Suite` result and merges, or says why not. |
