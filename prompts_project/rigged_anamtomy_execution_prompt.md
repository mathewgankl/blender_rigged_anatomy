# Rigged Anatomy Execution Prompt

**Status:** ACTIVE
**Purpose:** Control staged design, implementation, and verification of the Blender rigged-anatomy tool
**Applies to:** This project, all rounds
**Last verified:** 2026-09-14
**Primary evidence:** The approved round PRD when available; otherwise the active
brief
**Generic baseline:** `prompts_transferable/generic_engineering_execution_protocol.md`
**Overrides:** NONE

Before this project prompt, follow the exact `read_first.md` order: read the generic
execution protocol, `jumpstart.md`, and every other applicable generic prompt. Read
the source brief only before PRD approval or for an unresolved requirement linked by
`jumpstart.md`. This prompt then specializes project scope, research, milestones,
testing, and handoff. Approved requirements override plans; stop for material
unresolved decisions.

## Goal

Build a Blender 5.2 LTS tool, running in Blender's embedded Python, that generates
a scale-independent, anatomically informed humanoid rig and later adds muscle,
fat, skin, and optional physics in separately approved rounds.

## Current Scope: Round 1

- Support human skeletons only, including non-realistic humanoid proportions.
- Generate a semi-automatic skeleton from user landmarks at the palms, shoulders,
  hips, ankles, neck base, and head.
- Keep bones inside the mesh with a user-controlled balance between uniform
  cross-sectional scaling and local surface deflation at mesh intersections;
  neither endpoint changes landmark-defined joints or bone lengths.
- Model major visible anatomical mechanics only, including knees, shoulders,
  biceps, and hamstrings. Preserve independently moving structures and future
  attachment topology. Anatomical mesh geometry is read-only diagnostic and local
  clearance input; it does not seed or modify Automatic Weights.
- Build and validate IK behavior from anatomical joint and bone relationships.
- Bind the selected skin transactionally to the deform armature with Blender
  Automatic Weights and apply the approved deterministic Geometry Nodes
  bone-clearance corrector after the Armature modifier. This is a narrow exception
  needed to validate bone-driven deformation and non-penetration in Round 1.
- Work consistently after object and scene scaling.
- Test `Body_lowpoly` in `roxanne_5.blend` and reproduce the supplied reference
  pose.
- Design workflows with node-based composition in mind.

Do not implement muscle-shape deformation, soft-body simulation, fat, breasts,
muscle/fat-driven Surface Deform or Mesh Deform skin wrapping, VeeDynamics, or
other future-round features until Round 1 passes and the next round is approved.
Round 1 skin work is limited to native armature binding and the nonphysical local
bone-clearance corrector above; it does not model soft tissue or contact between
unrelated body regions.

## Evidence Priority

1. Local brief, assets, source, and tests.
2. Official Blender 5.2 LTS API and the documentation for Blender's embedded Python
   version. Python 3.14 is not a controlling runtime target.
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

Use the project-local `research` subagent configured in `opencode.json` with model
`openai/gpt-5.6-terra` and `reasoningEffort: medium`. Delegate only bounded,
independent questions with exact sources, outputs, and stop conditions. Verify the
merged configuration before dispatch and verify all research claims locally or
against primary sources. Route each batch through Section 3 of the generic execution
protocol. Terra Medium is the project-specific default, not an exemption from the
generic allocation, user-briefing, route-fit, or approval rules. Do not research
later rounds.

For each new round or planning scope, apply
`prompts_transferable/planning-interview-and-prd-gate.md`. Ask when to invoke
`matt-grill-with-docs` only when `jumpstart.md` does not already record a valid
selection for that scope. Preserve user-supplied reasoning as required by that
prompt. Round 1 selected bounded research before grilling and has completed its
interview and PRD-drafting gates; do not repeat them.

## Decisions

Ask before material choices involving architecture, public behavior, persistent
data, licensing, compatibility, migration, cost, or irreversible work. Test cheap
assumptions. Apply only minimal reversible defaults. Do not add speculative
abstractions, settings, dependencies, fallbacks, or compatibility layers.

## Milestone 0: Discovery and Round 1 Design

1. Verify Blender, Python, Git, assets, object names, dimensions, transforms, and
   existing armatures or modifiers.
2. If no valid Round 1 timing selection is recorded, ask whether
   `matt-grill-with-docs` should run before research or after the bounded research
   in steps 4 and 5; recommend a timing and explain why.
3. If the user selects before research, complete the planning interview now.
4. Complete the two required research tracks.
5. Evaluate `ms_human_700` and MuSkeMo viability, revisions, dependencies, and
   licenses without importing code prematurely.
6. Verify the research reports against primary sources. If the user selected after
   research, explicitly invoke and complete `matt-grill-with-docs` using only the
   verified bounded evidence.
7. Define the minimum anatomical bone and major muscle-relation model needed for
   Round 1.
8. Specify landmarks, fitting behavior, scale invariants, slider semantics, joint
   placement, IK behavior, and failure handling.
9. Define one minimal architecture and objective automated and Blender-headless
   acceptance tests.
10. Only after the selected interview is complete, write `docs/prds/round-1.md` as
    `DRAFT`, list open decisions, and stop for
   approval before production implementation.

Do not create the PRD before grilling. Do not create the production add-on during
Milestone 0.

## Planned Round 1 Milestones

### Milestone 1: Harness And Vertical Slice

Create the Extension skeleton, shared UI/headless application command, serializable
rig plan, deterministic harness, and one unilateral limb-chain vertical slice.

### Milestone 2: Assets And Anatomical Fitting

Build the pinned offline anatomy assets and catalogs, complete skeleton, required
landmarks and corrections, morphology, topology tiers, containment, provenance,
scale behavior, and repeatable regeneration.

### Milestone 3: Animator And Deform Rig

After separately approving the versioned numeric pose oracle, implement and test
the full animator/deform rig, mappings, and approved spine, limb, shoulder, patella,
forearm, foot, digit, and relationship-path mechanics.

### Milestone 4: Binding, Clearance, And Pose Approval

Implement transactional Automatic Weights binding, binding freshness, read-only
weight diagnostics, the Geometry Nodes bone-clearance corrector, full pose suite,
and private `Body_lowpoly` visual approval.

### Milestone 5: Lifecycle And Release Candidate

Complete ownership and breaking-schema behavior, undo/save/reload hardening,
documentation, reproducible Extension packaging, GitHub CI, and draft-release
automation without replacing required local Blender tests.

Each milestone needs approved scope, exclusions, acceptance tests, verification,
and a stop condition. Do not begin the next milestone without approval.

## Implementation and Testing

For each increment:

1. Define observable behavior and the smallest useful failing test.
2. Make the smallest correct change.
3. Run narrow tests, then affected headless and regression tests.
4. Test malformed landmarks, unsuitable meshes, cleanup, repeated generation,
   undo/reload where applicable, multiple scales, and deterministic output.
5. Review the diff and record state according to `read_first.md`: keep
   `jumpstart.md` concise and route detailed verification or operations evidence to
   its proper record.

Implementation alone does not complete a milestone. Before stopping, reconcile
the compact `jumpstart.md` fields with the workspace and put detailed changed-file,
command, and verification evidence in the records defined by `read_first.md`.
