# Project State

**Status:** MILESTONE 2 IN PROGRESS - NAMING AUTHORITY AND CATALOG SEED PASS COMPLETE
**Round:** 1
**Updated:** 2026-09-15

Milestone 2 is authorized. Milestone 3 and later remain unauthorized.

## Current Result

Milestone 1 provides the dependency-free Blender Extension skeleton, shared
UI/headless generation command, canonical rig plan, and staged left-arm vertical
slice. The slice creates registry-named upper-arm and forearm bones plus synthetic
humerus, radius, and ulna proof meshes. Input uses continuous source-rest transforms;
there is no categorical T/A selector or `source_pose` field.

Milestone 2 provides the 55-role canonical registry, exact VRM 1.0 and HumanIK/FBX
mapping manifests, and a pinned MS-Human-700 source inventory. The inventory closes
the XML/resource/body/tendon/actuator graph and resolves every path site, sidesite,
and wrapping geometry to one owned declaration. See
`docs/verification/milestone-2.md` for checked counts and hashes.

Versioned anatomy and relationship catalog schemas validate source provenance,
canonical roles, packaged artifact tiers, ordered paths, and surface/topology
references. The first catalog entry establishes
`mesh:humerus -> humerus.R -> upper_arm.R -> DEF-upper_arm.R`.

The first offline anatomy conversion preserves a diagnostic humerus `source` tier
and produces a separate closed `base` tier through pinned Blender remeshing,
decimation, and canonical ID ordering. Apache-2.0 terms and modification notices are
packaged with derived assets. Detailed topology and deviation evidence remains in
`docs/verification/milestone-2.md`.

Every role-registry fail-fast branch now has a focused malformed-input regression.
Catalog schema version 1 formally declares the artifact-backed `all` surface-region
sentinel, which anatomy and relationship validators consume instead of duplicating a
literal rule.

## Evidence

The current Milestone 1 and Milestone 2 gates pass, including exact source and asset
regeneration against the pinned checkout. Reproducible commands and detailed results
are in `docs/verification/milestone-1.md` and
`docs/verification/milestone-2.md`.

## Risks And Boundaries

- Only `shoulder.L` and `palm.L` are accepted by this vertical slice. The complete
  ten-landmark contract and fitting behavior remain Milestone 2 work.
- Numeric supported-source-rest rejection thresholds require approval before
  Milestone 2 validation is implemented; they do not block the next asset/catalog
  increment.
- The canonical role registry, interoperability manifests, and catalog schemas are
  established, but catalog content and anatomy-driver mappings remain Milestone 2
  work. Rig behavior remains Milestone 3 scope.
- The repository root license is `GPL-3.0-or-later`. Future MS-Human-700-derived
  assets retain separate Apache-2.0 terms and provenance; the first converted asset
  now packages those terms and a modification notice.
- The pinned humerus source mesh is not closed or consistently two-manifold. It is a
  preserved diagnostic source tier; the separate base tier satisfies the current
  topology gate.
- Current deviation evidence samples vertices against the opposing triangle surface;
  it is not a continuous Hausdorff bound. The `0.5 mm` p95 and `1.6 mm` maximum test
  guards are provisional local regression bounds, not approved general acceptance
  criteria. Humerus parameters are not proven for other anatomy.
- The Milestone 1 left-arm vertical slice still uses synthetic humerus, radius, and
  ulna proof geometry. Its bone naming is registry-backed, but its three temporary
  anatomy-driver records are not yet sourced from complete anatomy catalog content.
- The numeric pose oracle remains unapproved and blocks Milestone 3.
- Binding, Geometry Nodes clearance, private `Body_lowpoly` acceptance, and release
  automation remain in their approved later milestones.

## Next Action

Stop before further asset conversion. On the next explicit continuation, select the
smallest dependency-ordered anatomy asset and catalog expansion from the closed
source manifest, define its decisive topology/provenance checks, and record that
bounded increment here before implementation.
