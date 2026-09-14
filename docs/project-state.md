# Project State

**Status:** MILESTONE 1 EVIDENCE REQUIRES SOURCE-REST REFRESH
**Round:** 1
**Updated:** 2026-09-14

## Current Result

Milestone 1 now has a dependency-free Blender Extension skeleton and one left-arm
vertical slice. A shared application command validates inputs, produces canonical
JSON and a plan digest, and optionally materializes a staged Blender collection.
The UI operator uses the same command as headless callers.

The slice contains `DEF-upper_arm.L` and `DEF-forearm.L` plus deterministic closed
synthetic mesh islands for `humerus.L`, `radius.L`, and `ulna.L`. These meshes prove
the anatomy/armature materialization seam only; they are not the pinned anatomical
assets authorized for Milestone 2.

The user approved the continuous source-rest contract in
`docs/decisions/source-rest-pose-contract.md`. The tool must no longer ask for a
T/A category. The existing Milestone 1 implementation and tests still contain that
selector, so their prior passing result is not current approval evidence.

## Evidence

See `docs/verification/milestone-1.md`. The complete local gate is:

```powershell
& "tests\run_milestone1.ps1"
```

It passes six headless behavior tests against the pre-amendment contract, validates
and builds the Extension ZIP in a temporary directory, validates the ZIP, and
verifies isolated install, enable, disable, re-enable, and uninstall behavior under
Blender 5.2.1 LTS. The input-contract checks and evidence must be refreshed.

## Risks And Boundaries

- `src/rigged_anatomy/` still requires categorical `source_pose` input. That field,
  its UI selector, and its plan representation conflict with the amended PRD.
- Only `shoulder.L` and `palm.L` are accepted by this vertical slice. The complete
  ten-landmark contract and fitting behavior remain Milestone 2 work.
- Numeric supported-source-rest rejection thresholds require approval before
  Milestone 2 validation is implemented; they do not block the Milestone 1 schema
  refresh.
- The data-only canonical role registry and mapping manifests now belong to
  Milestone 2 because its catalogs depend on them. Rig behavior remains Milestone 3
  scope.
- The repository root license is `GPL-3.0-or-later`. Future MS-Human-700-derived
  assets retain separate Apache-2.0 terms and provenance.
- The numeric pose oracle remains unapproved and blocks Milestone 3.
- Binding, Geometry Nodes clearance, private `Body_lowpoly` acceptance, and release
  automation remain in their approved later milestones.

## Next Action

Add the smallest failing headless test proving that generation needs no T/A input.
Then remove only the categorical application field, plan field, and operator
selector; run the focused test and full Milestone 1 gate, update its evidence, and
stop for approval. Do not begin Milestone 2.
