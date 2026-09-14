# Milestone Continuation Prompt

**Status:** ACTIVE
**Purpose:** Resume one approved milestone from durable state after a context reset
**Applies to:** Fresh-session milestone continuation
**Last verified:** 2026-09-14
**Supersedes:** NONE
**Superseded by:** NONE
**Primary evidence:** `read_first.md` and the active project execution prompt

Use after a completed checkpoint in a fresh session. Read `read_first.md`, then
`prompts_transferable/generic_engineering_execution_protocol.md`, before any project
prompt; all generic policies apply unless an approved scoped project override says
otherwise.

## Required Continuation Protocol

1. Inspect the workspace and version-control state; preserve unrelated changes.
2. Treat the handoff as evidence: verify referenced revisions, relevant tool
   versions, subagent model/effort routing, and critical claims. A requested route
   is not proof that the task interface applied it.
3. Run the checkpoint's smallest listed smoke test when feasible.
4. Confirm the next action remains applicable; flag stale, contradictory,
   missing, or unverified state.
5. When an approved PRD exists, exclude superseded briefs, pre-grill notes, and
   draft requirements from normal context. Read one only when the active handoff
   names the unresolved question or provenance need it answers.
6. During Milestone 0, enforce
   `prompts_transferable/planning-interview-and-prd-gate.md` and any stricter
   project protocol. Verify that the user selected when to run
   `matt-grill-with-docs`, that only the named bounded evidence was gathered, and
   that no PRD predates the completed interview and separate drafting authorization.
7. Follow every scope, research, assumption, testing, model/subagent, and stop
   rule in the project protocol.
8. Do not repeat research, broaden scope, consume videos or broad documentation,
   enumerate speculative options, or delegate unless a concrete current blocker
   meets that protocol's criteria. For any new research batch or delegation, apply
   the allocation preflight and route-fit rules in
   `prompts_transferable/generic_engineering_execution_protocol.md`; brief the user
   only when that policy requires it.
9. Test cheap reversible assumptions; ask about material, high-risk, expensive,
   or irreversible decisions.
10. Before stopping, update durable state and report as required. Never begin the
   next milestone.

## Generic Project Version

Follow the `read_first.md` sequence: after the generic execution baseline, read the
control center, other applicable generic prompts, the active project prompt,
approved requirements, and only linked records. Read the source brief only while it
is active or for a question explicitly linked by the control center.

Execute only:

- Milestone: `<MILESTONE NUMBER AND NAME>`
- Bounded next action: `<NEXT ACTION>`
- Acceptance criteria: `<ACCEPTANCE CRITERIA OR PATH TO THEIR DEFINITION>`

## Rigged Anatomy Project Version

Read these files in order:

1. `read_first.md`
2. `prompts_transferable/generic_engineering_execution_protocol.md`
3. `jumpstart.md`
4. The latest user requirements
5. Any other generic prompt active for the current work
6. `prompts_project/rigged_anamtomy_execution_prompt.md`
7. The approved PRD referenced by `jumpstart.md`, when one exists
8. During pre-PRD planning, the active brief and pre-grill evidence named by
   `jumpstart.md`
9. Only other active records required by the current state

Execute only `<ROUND AND MILESTONE>` under
`prompts_project/rigged_anamtomy_execution_prompt.md`. Confirm Blender, Python,
assets, dependencies, milestone prerequisites, and acceptance criteria. Verify
critical claims against source, local files, tool versions, and tests.

Research only a specific current blocker unanswered by local source, project
records, a focused experiment, or targeted primary documentation. Do not repeat
broad rigging, anatomy, or Blender research. Run narrow tests while implementing
and the applicable regression suite before completion.
