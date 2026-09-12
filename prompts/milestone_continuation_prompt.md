# Milestone Continuation Prompt

**Status:** ACTIVE
**Purpose:** Resume one approved milestone from durable state after a context reset
**Applies to:** Fresh-session milestone continuation
**Last verified:** 2026-09-04
**Supersedes:** NONE
**Superseded by:** NONE
**Primary evidence:** `read_first.md` and the active project execution prompt

Use after a completed checkpoint in a fresh session. Read `read_first.md` first;
all its policies apply.

## Required Continuation Protocol

1. Inspect the workspace and version-control state; preserve unrelated changes.
2. Treat the handoff as evidence: verify referenced revisions, relevant tool
   versions, and critical claims.
3. Run the checkpoint's smallest listed smoke test when feasible.
4. Confirm the next action remains applicable; flag stale, contradictory,
   missing, or unverified state.
5. Follow every scope, research, assumption, testing, model/subagent, and stop
   rule in the project protocol.
6. Do not repeat research, broaden scope, consume videos or broad documentation,
   enumerate speculative options, or delegate unless a concrete current blocker
   meets that protocol's criteria.
7. Test cheap reversible assumptions; ask about material, high-risk, expensive,
   or irreversible decisions.
8. Before stopping, update durable state and report as required. Never begin the
   next milestone.

## Generic Project Version

After `read_first.md`, read in order: project state, its referenced approved PRDs,
the active execution prompt, and only records referenced by project state. Read
an active `proj_*.txt` brief only during planning.

Execute only:

- Milestone: `<MILESTONE NUMBER AND NAME>`
- Bounded next action: `<NEXT ACTION>`
- Acceptance criteria: `<ACCEPTANCE CRITERIA OR PATH TO THEIR DEFINITION>`

## Rigged Anatomy Project Version

Read these files in order:

1. `read_first.md`
2. `jumpstart.md`
3. The approved PRD referenced by `jumpstart.md`
4. `prompts/rigged_anamtomy_execution_prompt.md`
5. Only records required by the current state

Execute only `<ROUND AND MILESTONE>` under
`prompts/rigged_anamtomy_execution_prompt.md`. Confirm Blender, Python, assets,
dependencies, milestone prerequisites, and acceptance criteria. Verify critical
claims against source, local files, tool versions, and tests.

Research only a specific current blocker unanswered by local source, project
records, a focused experiment, or targeted primary documentation. Do not repeat
broad rigging, anatomy, or Blender research. Run narrow tests while implementing
and the applicable regression suite before completion.
