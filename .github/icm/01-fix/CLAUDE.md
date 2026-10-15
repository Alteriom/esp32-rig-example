# 01-fix — fix a defect

One run is one defect in the firmware, the bundle, the suite or a workflow: reproduced, fixed at its cause in the smallest readable way (people copy this), and proposed as a pull request. Every rig that ships the "Rig example" follows `main` here, so a merge reaches them at their next run.

Stages, in order; inputs, outputs and checks for each are in [CONTEXT.md](CONTEXT.md):

1. [Reproduce](stages/01_reproduce/CONTEXT.md) — make it fail on purpose.
2. [Fix](stages/02_fix/CONTEXT.md) — change the cause, watch the reproduction pass.
3. [Verify](stages/03_verify/CONTEXT.md) — both workflows' checks, the pull request.
