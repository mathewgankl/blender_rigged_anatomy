# Milestone Continuation Prompt

**Status:** ACTIVE
**Purpose:** Resume an approved milestone from durable state after a context reset
**Applies to:** Fresh-session milestone continuation
**Last verified:** 2026-09-15
**Supersedes:** NONE
**Superseded by:** NONE
**Primary evidence:** `read_first.md` and the active project prompt

Follow `read_first.md` and `jumpstart.md`. Read only the generic and project-prompt
sections, authority, state, and evidence needed for the current increment; do not
reconstruct status from logs or inactive planning records.

## Continuation

1. Inspect the workspace and preserve unrelated changes.
2. Verify critical handoff claims against current source, tools, or tests.
3. Confirm the routed next action is still authorized and applicable, then run the
   smallest useful smoke test when feasible.
4. Apply the planning gate during Milestone 0. Otherwise avoid new research or
   delegation unless a current blocker justifies it.
5. Ask about material or hard-to-reverse decisions. Apply documentation update
   triggers only when durable content changed.
6. Stop at the milestone boundary.

Execute only the milestone and next action routed through project state. If the
handoff is stale, contradictory, or unverifiable, resolve that before implementation.
Do not pull downstream work into the session until the user explicitly promotes it.
