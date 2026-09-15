# Rigged Anatomy Execution Prompt

**Status:** ACTIVE
**Purpose:** Apply project-specific constraints to the Blender rigged-anatomy tool
**Applies to:** This project, all rounds
**Last verified:** 2026-09-15
**Primary evidence:** The approved round PRD
**Generic baseline:** `prompts_transferable/generic_engineering_execution_protocol.md`
**Overrides:** NONE

Follow `read_first.md` and the generic protocol. The approved PRD owns project scope,
milestones, exclusions, and acceptance; `docs/project-state.md` owns current
authorization and next work. Read the source brief only before PRD approval or for a
named unresolved requirement or provenance need.

## Goal

Build a Blender 5.2 LTS Extension, running in Blender's embedded Python, that produces
a scale-independent anatomically informed humanoid rig. Muscle, fat, skin, and physics
work require their separately approved rounds.

## Project Evidence

Prefer local assets, source, tests, the approved PRD, official Blender documentation,
and the pinned primary anatomy or rigging sources named by project records. Research
only a current blocker or decision and preserve durable source and license evidence
under `read_first.md`. Do not repeat completed Round 1 planning or research unless new
evidence materially reopens it.

New planning scopes follow
`prompts_transferable/planning-interview-and-prd-gate.md`.

## Decision Guards

Treat measured geometry, fitting, pose, and performance values as evidence until the
user approves them as acceptance criteria. Approval to implement an algorithm does not
approve provisional numeric limits or an unstated persistent-format change. Ask before
a cleanup expands a public interface or versioned schema beyond the named defect.

## Verification

Use Blender-headless and dependency-free tests where they provide useful confidence.
Verify scale behavior, deterministic output, malformed or unsuitable inputs, cleanup,
repeated generation, and undo or reload when relevant to the changed behavior. Every
claimed fail-fast data invariant needs a focused malformed-input regression.

Run the complete milestone gate after a stable increment and again only when later
changes can affect it. Preserve durable evidence under `read_first.md` and do not
advance beyond the authorization in project state.
