# Project Jumpstart

**Status:** MILESTONE 2 AUTHORIZED - ROLE REGISTRY NOT IMPLEMENTED
**Phase:** Round 1 Milestone 2 canonical data foundations
**Updated:** 2026-09-14

## Read

1. `read_first.md`
2. `prompts_transferable/generic_engineering_execution_protocol.md`
3. `prompts_transferable/milestone_continuation_prompt.md`
4. `prompts_project/rigged_anamtomy_execution_prompt.md`
5. `docs/prds/round-1.md`
6. `docs/decisions/source-rest-pose-contract.md`
7. `docs/project-state.md`

The source brief and pre-grill notes are superseded. Read them only for provenance
or a named unresolved requirement. Read a research report only when an active
question links it. `docs/agent-operations-log.md` is non-authoritative and is not a
normal continuation read.

## Authority

- `docs/prds/round-1.md` is the approved Round 1 execution authority.
- The user completed `matt-grill-with-docs` and separately authorized PRD drafting
  on 2026-09-14. Volunteered user reasoning and attribution boundaries are retained
  in `docs/decisions/round-1-planning-interview.md`; read it only when rationale is
  material to a current decision.
- The user approved the PRD and explicitly authorized Milestone 1 on 2026-09-14.
- The user approved the continuous source-rest amendment on 2026-09-14. It removes
  the T/A selector while retaining a supported neutral rest-pose boundary and a
  computed canonical T mapping. The decision is recorded in
  `docs/decisions/source-rest-pose-contract.md`.
- The user approved moving the data-only canonical role registry and mapping
  manifests into Milestone 2 so its catalogs have stable role references. Milestone
  3 retains rig behavior materialization. See
  `docs/decisions/role-registry-milestone-order.md`.
- The user approved the refreshed Milestone 1 evidence and explicitly authorized
  Milestone 2 on 2026-09-14. Milestone 3 and later remain unauthorized.
- The versioned numeric pose oracle remains a separate decision required before
  Milestone 3; it does not block PRD review or Milestones 1-2.

## Verified State

- Blender 5.2.1 LTS is installed at
  `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`; it embeds Python
  3.13.13. The add-on targets Blender's embedded runtime only.
- `roxanne_5.blend` opens headlessly. `Body_lowpoly` has identity transforms, no
  armature or modifiers, 19,722 vertices, 19,720 quad faces, and no non-manifold or
  loose edges. The scene uses metric units with scale length `1.0`. A fresh
  Blender 5.2.1 headless handoff smoke test passed on 2026-09-14.
- `roxanne_5.blend` and the supplied reference image are private local acceptance
  fixtures unless redistribution rights are documented.
- `src/rigged_anatomy/` contains the Blender Extension skeleton, canonical
  serializable rig plan, shared application command, Blender operator, and staged
  left-arm materializer. The vertical slice creates two deform bones and synthetic
  humerus/radius/ulna proof meshes; pinned anatomy assets remain Milestone 2 work.
- `tests/run_milestone1.ps1` passes seven Blender-headless behavior tests, validates
  and builds the Extension ZIP, and passes isolated install/enable/disable/uninstall
  lifecycle checks under Blender 5.2.1 LTS. The refreshed tests prove direct and
  operator generation need no T/A category and that neither the canonical plan nor
  operator RNA contains `source_pose`. Detailed status is in
  `docs/verification/milestone-1.md`.
- Git tracks `origin/main` at
  `https://github.com/mathewgankl/blender_rigged_anatomy.git`.
- Round 1 research is complete under `docs/research/`: standards/MS-Human-700,
  node workflow/MuSkeMo, Mantis, geometry density, skin clearance, and the
  source-rest contract.
- `opencode.json` configures the read-only `research` subagent as
  `openai/gpt-5.6-terra` with `reasoningEffort: medium`. Apply the generic research
  allocation and route-fit preflight before any new research batch.
- Documentation whitespace checks pass; Git reports only LF-to-CRLF conversion
  warnings.

## Active Decisions

- Round 1 delivers a Blender Extension containing a full fitted anatomical skeleton,
  a smaller animator/deform rig, transactional Automatic Weights binding, and a
  post-armature Geometry Nodes local bone-clearance corrector.
- Muscle/fat generation, soft-tissue wrapping, body self-collision, and physics stay
  in later rounds.
- Independently written code is `GPL-3.0-or-later`; MS-Human-700-derived assets
  retain Apache-2.0 terms and provenance.
- The root `LICENSE` is aligned with `GPL-3.0-or-later`.
- Input uses a supported neutral source rest pose, not a categorical T/A selection.
  Arm elevation may vary continuously and independently; canonical T deltas are
  computed from actual fitted rest transforms.
- Public CI uses redistributable fixtures. Private `Body_lowpoly` and image-based
  acceptance remain local release gates.

## Blockers And Risks

- Numeric supported-source-rest rejection thresholds require a proposal and user
  approval before Milestone 2 validation implementation. They do not block
  the role-registry increment.
- Milestone 3 is additionally blocked until targeted anatomy evidence supports a
  numeric `tests/fixtures/pose-suite-v1.json` proposal and the user approves it.
- Geometry Nodes signed clearance, full source conversion, Automatic Weights on
  `Body_lowpoly`, and the reclining pose remain implementation proof obligations
  recorded in the PRD.

## Next Action

Add the smallest failing test for a versioned data-only canonical role registry with
an exact closed role set and required metadata. Implement that registry without
materializing Milestone 3 rig behavior, run the focused and affected regression
checks, update evidence, and stop before the mapping-manifest increment.
