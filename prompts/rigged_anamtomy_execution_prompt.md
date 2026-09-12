# Rigged Anatomy Execution Prompt

**Status:** ACTIVE
**Purpose:** Control staged design, implementation, and verification of the Blender rigged-anatomy tool
**Applies to:** This project, all rounds
**Primary evidence:** `proj_003 blender rigging physics sim tool.txt`

Read `read_first.md`, the active brief, and `jumpstart.md`. This prompt governs
project scope, research, milestones, testing, and handoff. Approved requirements
override plans; stop for material unresolved decisions.

## Goal

Build a Blender 5.2 LTS and Python 3.14 tool that generates a scale-independent,
anatomically informed humanoid rig and later adds muscle, fat, skin, and optional
physics in separately approved rounds.

## Current Scope: Round 1

- Support human skeletons only, including non-realistic humanoid proportions.
- Generate a semi-automatic skeleton from user landmarks at the palms, shoulders,
  hips, ankles, neck base, and head.
- Keep bones inside the mesh with a user-controlled balance between whole-bone
  scaling and local deflation at mesh intersections.
- Model major visible anatomical mechanics only, including knees, shoulders,
  biceps, and hamstrings. Preserve independently moving structures and useful
  topology for automatic weights.
- Build and validate IK behavior from anatomical joint and bone relationships.
- Work consistently after object and scene scaling.
- Test with `roxanne_5.blend` and reproduce the supplied reference pose.
- Design workflows with node-based composition in mind.

Do not implement muscle-shape deformation, soft-body simulation, fat, breasts,
skin binding, VeeDynamics, or future-round features until Round 1 passes and the
next round is approved.

## Evidence Priority

1. Local brief, assets, source, and tests.
2. Official Blender 5.2 LTS and Python 3.14 documentation.
3. Primary rig-standard documentation and implementations.
4. MuJoCo Menagerie `ms_human_700` for bone-muscle relationships.
5. MuSkeMo for skeleton fitting concepts, subject to license and compatibility.
6. Targeted anatomy sources needed for a current design decision.
7. Houdini muscle documentation only for unresolved later-round decisions.

Use written sources. Do not parse videos; use a transcript or focused screenshots
only when they materially resolve a blocker. Record exact URLs, revisions,
licenses, facts, assumptions, and decisions. Stop research when the current
decision has adequate primary evidence.

## Research and Agents

Round 1 requires two bounded research tracks:

1. Compare the three most relevant rigging standards and recommend how this rig
   aligns with them.
2. Define a maintainable node-oriented Blender implementation workflow.

Use Terra medium for subagent research when available. Delegate only bounded,
independent questions with exact sources, outputs, and stop conditions. Verify all
claims locally or against primary sources. Do not research later rounds.

## Decisions

Ask before material choices involving architecture, public behavior, persistent
data, licensing, compatibility, migration, cost, or irreversible work. Test cheap
assumptions. Apply only minimal reversible defaults. Do not add speculative
abstractions, settings, dependencies, fallbacks, or compatibility layers.

## Milestone 0: Discovery and Round 1 Design

1. Verify Blender, Python, Git, assets, object names, dimensions, transforms, and
   existing armatures or modifiers.
2. Complete the two required research tracks.
3. Evaluate `ms_human_700` and MuSkeMo viability, revisions, dependencies, and
   licenses without importing code prematurely.
4. Define the minimum anatomical bone and major muscle-relation model needed for
   Round 1.
5. Specify landmarks, fitting behavior, scale invariants, slider semantics, joint
   placement, IK behavior, and failure handling.
6. Define one minimal architecture and objective automated and Blender-headless
   acceptance tests.
7. Write `docs/prds/round-1.md` as `DRAFT`, list open decisions, and stop for
   approval before production implementation.

Do not create the production add-on during Milestone 0.

## Planned Round 1 Milestones

### Milestone 1: Harness and Minimal Rig

Create the add-on skeleton, deterministic headless test harness, and smallest
landmark-to-armature vertical slice.

### Milestone 2: Skeleton Fitting

Implement required landmarks, proportion handling, mesh containment, the
scale-versus-deflation control, validation, and repeatable regeneration.

### Milestone 3: Anatomical IK

Implement and test the approved knee, shoulder, and other major joint mechanics,
including independent structures and predictable pole/constraint behavior.

### Milestone 4: Weighting and Pose Validation

Validate automatic-weight readiness, major visible deformation regions, scaling,
and the supplied reference pose on the approved test object.

### Milestone 5: Packaging and CI

Package clean installation and removal, document use, and run reproducible GitHub
CI checks that do not replace required local Blender tests.

Each milestone needs approved scope, exclusions, acceptance tests, verification,
and a stop condition. Do not begin the next milestone without approval.

## Implementation and Testing

For each increment:

1. Define observable behavior and the smallest useful failing test.
2. Make the smallest correct change.
3. Run narrow tests, then affected headless and regression tests.
4. Test malformed landmarks, unsuitable meshes, cleanup, repeated generation,
   undo/reload where applicable, multiple scales, and deterministic output.
5. Review the diff and record commands, versions, results, and gaps in
   `jumpstart.md`.

Implementation alone does not complete a milestone. Before stopping, reconcile
`jumpstart.md` with the workspace: status, decisions, changed files, verification,
blockers, and one bounded next action.
