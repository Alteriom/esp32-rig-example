# Shared reference

What every job on this repository draws on. Each file points at the repository file that owns a fact; follow the pointer for the detail, and when the two disagree the owning file is right.

| File | Answers |
|---|---|
| [architecture.md](architecture.md) | the map: the four repositories, the firmware, the bundle, the suite, the two workflows |
| [build-and-test.md](build-and-test.md) | how to build a bundle and run the suite against the simulator, the pinned rig release, what CI runs, what counts as evidence |
| [rules.md](rules.md) | the defaults the rig reads, the revision key, families, the pinned rig release, keeping it minimal, conventions |
| [documents.md](documents.md) | the documents a person reads here and who owns their facts |

Each stage's contract names the files it loads.
