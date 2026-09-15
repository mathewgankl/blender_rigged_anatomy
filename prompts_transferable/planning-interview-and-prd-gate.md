# Planning Interview And PRD Gate

**Status:** ACTIVE
**Purpose:** Control interview timing and PRD authorization
**Applies to:** Milestone 0 planning
**Last verified:** 2026-09-15
**Primary evidence:** `read_first.md` and the installed `matt-grill-with-docs` skill

Follow `read_first.md` and the generic execution protocol. A project may add stricter
requirements but may not silently bypass this gate.

## Interview Timing

Inspect available local facts before asking the user. Before external research or PRD
drafting, obtain permission to invoke `matt-grill-with-docs` and agree whether it runs
before research or after a named bounded research set. Recommend research first only
when external facts materially affect the interview choices. Preserve the selection
in the planning-interview record.

## Evidence And Interview

Research only decision-changing questions under the generic protocol. Prefer primary
sources for material platform, dependency, licensing, security, privacy, and
compatibility claims.

At the selected point, load `matt-grill-with-docs` and give it only the active brief,
relevant verified state, prior approved decisions, and agreed evidence. Preserve a
faithful summary of settled decisions and user-supplied rationale in
`docs/decisions/<scope>-planning-interview.md` or the project equivalent. Distinguish
agent interpretation and unverified claims. Finish only when the user confirms the
shared understanding; do not implement the plan.

If the required skill is unavailable, stop and ask rather than silently substituting
another interview process.

Reopen only decisions materially affected by later contradictory evidence.

## PRD Gate

After the interview, ask for separate authorization to draft the PRD. Build it from
settled decisions, verified evidence, exclusions, acceptance criteria, and open
questions. Do not present recommendations as approved requirements or begin
production implementation before approval. Stop after drafting for PRD approval.

After approval, the PRD becomes execution authority for its scope. Remove superseded
planning inputs from normal routing without rewriting their historical content, keep
active documents consistent, and place only the next authorized increment in project
state. Milestones remain approval and evidence gates.
