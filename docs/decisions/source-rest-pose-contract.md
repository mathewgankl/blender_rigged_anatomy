# Continuous Source Rest Pose Contract

**Status:** APPROVED
**Date:** 2026-09-14
**Scope:** Round 1 input, fitting, persistence, interoperability mapping, and tests
**Evidence:** `docs/research/source-rest-pose-contract.md`

## Context

The approved Round 1 PRD required the user to classify the source mesh as T- or
A-pose. The user observed that humanoid meshes can lie between those categories,
that the geometric difference is not fundamental to generation, and that fitting
should account for the actual mesh pose.

The investigation confirmed that Blender does not require the category. The binary
label was primarily a shortcut for canonical T mapping and deterministic fixtures.
Unrestricted arbitrary source rest poses would create material ambiguity with the
approved ten-landmark contract, so removing the label must not remove the neutral
rest-pose boundary.

## Decision

- Do not ask the user to select T- or A-pose.
- Accept a **supported neutral source rest pose**: upright, forward-facing, and
  uncrossed, with substantially extended elbows and knees.
- Allow arm elevation to vary continuously and independently on each side,
  including conventional A-pose, T-pose, and poses between them.
- Preserve the exact supported source rest pose when authoring the mesh and rig.
- Derive the canonical T mapping from the actual fitted source rest transforms.
  A conforming T source maps identically; every non-T source stores deterministic
  role-local deltas without changing source geometry, joint centers, or bone
  lengths.
- Reject a source rest pose when crossed limbs, material joint flexion, torso
  articulation, or another ambiguity prevents deterministic fitting under the
  approved landmarks and correction workflow. Report actionable diagnostics rather
  than guessing.

## Consequences

- The `T`/`A` selector and categorical `source_pose` field are removed from the
  application contract and canonical rig plan.
- Durable state records source rest transforms, their digest, and the computed
  canonical T mapping instead of a pose-class label.
- Public fixtures cover conforming T, conventional A, intermediate symmetric, and
  intermediate asymmetric arm elevations. Unsupported bent or crossed poses fail.
- Exact rejection thresholds must be proposed and approved before Milestone 2
  source-rest validation is implemented. Exact fixture deltas remain part of the
  approved pose-oracle gate. Neither may be invented merely to preserve the former
  category.
- Existing Milestone 1 evidence predates this decision. Its architecture remains
  valid, but its input schema, operator, tests, and evidence must be refreshed before
  Milestone 1 can be approved.
