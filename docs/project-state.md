# Project State

**Status:** MILESTONE 2 AUTHORIZED - ROLE REGISTRY NOT IMPLEMENTED
**Round:** 1
**Updated:** 2026-09-14

## Current Result

Milestone 1 has a dependency-free Blender Extension skeleton and one left-arm
vertical slice. A shared application command validates inputs, produces canonical
JSON and a plan digest, and optionally materializes a staged Blender collection.
The UI operator uses the same command as headless callers.

The slice contains `DEF-upper_arm.L` and `DEF-forearm.L` plus deterministic closed
synthetic mesh islands for `humerus.L`, `radius.L`, and `ulna.L`. These meshes prove
the anatomy/armature materialization seam only; they are not the pinned anatomical
assets authorized for Milestone 2.

The source-rest amendment is implemented at the Milestone 1 boundary. Application
settings require no T/A category, the canonical rig plan stores no categorical
`source_pose`, and the Blender operator exposes no pose selector. The user approved
the refreshed Milestone 1 evidence and authorized Milestone 2 on 2026-09-14.

## Evidence

See `docs/verification/milestone-1.md`. The complete local gate is:

```powershell
& "tests\run_milestone1.ps1"
```

It passes seven headless behavior tests against the amended contract, validates and
builds the Extension ZIP in a temporary directory, validates the ZIP, and verifies
isolated install, enable, disable, re-enable, and uninstall behavior under Blender
5.2.1 LTS.

## Risks And Boundaries

- Only `shoulder.L` and `palm.L` are accepted by this vertical slice. The complete
  ten-landmark contract and fitting behavior remain Milestone 2 work.
- Numeric supported-source-rest rejection thresholds require approval before
  Milestone 2 validation is implemented; they do not block the role-registry
  increment.
- The data-only canonical role registry and mapping manifests now belong to
  Milestone 2 because its catalogs depend on them. Rig behavior remains Milestone 3
  scope.
- The repository root license is `GPL-3.0-or-later`. Future MS-Human-700-derived
  assets retain separate Apache-2.0 terms and provenance.
- The numeric pose oracle remains unapproved and blocks Milestone 3.
- Binding, Geometry Nodes clearance, private `Body_lowpoly` acceptance, and release
  automation remain in their approved later milestones.

## Next Action

Add the smallest failing test for a versioned data-only canonical role registry with
an exact closed role set and required metadata. Implement that registry without
materializing Milestone 3 rig behavior, run the focused and affected regression
checks, update evidence, and stop before the mapping-manifest increment.
