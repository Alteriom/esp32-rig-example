# 02-rig-release — move the suite to a newer rig release

One run is one move of `RIG_RELEASE` in `.github/workflows/suite.yml`: the new rig release checked against this suite, then one pull request that says why (history: "suite: run against rig release 1.0.179"). The README's line naming the release that first shipped this project is a fact, not a pin, and moves only if that fact does.

Stages, in order; inputs, outputs and checks for each are in [CONTEXT.md](CONTEXT.md):

1. [Check](stages/01_check/CONTEXT.md) — the suite against the new release's simulator.
2. [Move](stages/02_move/CONTEXT.md) — the one-line pull request, with the reason.
