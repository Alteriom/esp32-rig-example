# 02_fix — change the cause, not the symptom

One job: the smallest readable change at the cause that turns the reproduction green, with the defaults the rig reads left as they are.

## Inputs
- Working (this run): `.github/icm/01-fix/stages/01_reproduce/output/reproduction.md`
- Reference (every run): `.github/icm/_shared/rules.md`
- Reference (only when the change touches a workflow or the suite's install): `.github/icm/_shared/build-and-test.md`

Do NOT load: the other pipelines, other runs' output.

## Process
1. Confirm the cause in the code before changing anything.
2. Change it the way someone copying the example would want to read it: short, commented with the *why*, no new dependency.
3. Check [rules.md](../../../_shared/rules.md): the suite path, workflow, artifact name and revision key stay as the rig reads them; `git_sha` still holds the commit built; the suite still passes whatever families a run is given.
4. Run the reproduction (green now) and the suite against the simulator at the pinned rig release.

## Outputs
- change.md → output/ — the cause in one paragraph; each file changed and why; the passing output; what only a rig run can prove.

## Human check
A person reads the diff beside the reproduction: it removes the cause, stays small enough to copy, and leaves the rig's defaults alone.
