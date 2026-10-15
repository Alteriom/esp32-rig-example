# 01-fix — the pipeline

Make it fail, make it pass for the right reason, keep it small enough to copy.

| Stage | Job | Input | Output | Human check |
|---|---|---|---|---|
| [`01_reproduce`](stages/01_reproduce/CONTEXT.md) | reproduce the reported defect | the report | `output/reproduction.md` | A person runs the command, or reads the evidence, and confirms it fails for the reported reason and that the cause is in this repository. |
| [`02_fix`](stages/02_fix/CONTEXT.md) | change the cause, not the symptom | 01_reproduce's `reproduction.md` | `output/change.md` | A person reads the diff beside the reproduction: it removes the cause, stays small enough to copy, and leaves the rig's defaults alone. |
| [`03_verify`](stages/03_verify/CONTEXT.md) | both workflows' checks, the pull request | 02_fix's `change.md` | `output/pull-request.md` | A person reads `pull-request.md` and the `HIL` and `Suite` results and says whether to open it; the reviewer merges, knowing every rig's built-in example follows `main`. |
