# Planning Interview and PRD Gate

**Status:** ACTIVE
**Purpose:** Standardize research timing, `matt-grill-with-docs`, PRD creation, and
planning closure
**Applies to:** Milestone 0 planning for all projects
**Last verified:** 2026-09-14
**Primary evidence:** `read_first.md` and the installed `matt-grill-with-docs` skill

Read `read_first.md` and
`prompts_transferable/generic_engineering_execution_protocol.md` first. A stricter
approved project requirement may add scope, but it may not silently bypass this
gate.

## 1. Choose Interview Timing

Inspect the local workspace, brief, assets, toolchain, and existing decisions before
asking the user anything. Do not ask the user for facts available from local tools.

Before external research or PRD drafting, ask the user to choose only when no valid
selection is recorded for the current planning scope:

1. **Grill before external research.** Recommend this when intended users,
   workflows, outcomes, vocabulary, priorities, scope, or success criteria remain
   unclear. The interview should first determine which research is actually needed.
2. **Grill after a specified bounded research set.** Recommend this when meaningful
   choices depend on external facts. Name the proposed research before asking for
   the choice; never offer an undefined "research first" phase.

The timing question is also the request for explicit permission to invoke the
opt-in skill. Record the user's selection in `jumpstart.md`. If
`matt-grill-with-docs` is unavailable, report the blocker and ask how to proceed;
do not silently substitute an ordinary planning conversation.

## 2. Recommend Only Useful Context

For every proposed research item, state the exact question, decision affected,
minimum credible primary source, and stop condition. Recommend only context that
can change the current design tree, normally drawn from:

- Governing standards, protocols, laws, or official platform/API behavior.
- Required dependency, license, security, privacy, and compatibility facts.
- Target-environment constraints verified from the actual toolchain or assets.
- Existing code, persisted data, integrations, and externally consumed interfaces.
- One relevant primary implementation when feasibility or interoperability is
  otherwise uncertain.
- One focused experiment when documentation cannot settle a material assumption.

Do not recommend broad competitor surveys, general tutorials, videos when text
suffices, duplicate research, speculative future-milestone work, or evidence that
cannot change a current decision. Research agents are read-only: they return facts,
sources, limits, and uncertainties, not integrated plans, decisions, or PRDs.

Route every research batch through Section 3 of
`prompts_transferable/generic_engineering_execution_protocol.md`. This document
governs what research is useful; the generic protocol governs allocation, user
briefing, model/effort fit, and invocation.

## 3. Run The Interview

When the selected point is reached:

1. Load `matt-grill-with-docs`; follow its requirement to load and combine
   `matt-grilling` and `matt-domain-modeling` rather than inventing another process.
2. Give the interview only the active brief, verified local state, approved prior
   decisions, and the bounded evidence selected by the user. Label unverified
   research, assumptions, and unverified model-routing claims explicitly.
3. Build a dependency-ordered design tree. Ask one complete numbered frontier per
   round, with a concise recommendation and material trade-off for each question.
   Do not place dependent questions in the same round.
4. Wait for the user's answers after every round. Recompute the frontier and
   continue until no material prerequisite, edge case, failure behavior, boundary,
   or acceptance decision for the current scope remains silent.
5. Preserve the user's decision and any reasoning they volunteer: constraints,
   examples, trade-offs, caveats, uncertainty, and rejected alternatives. Summarize
   faithfully rather than requesting private chain-of-thought. Label agent
   interpretation separately and confirm any materially consequential paraphrase.
6. Challenge ambiguous domain terms with concrete scenarios. Whenever the user
   supplies reasoning, preserve a faithful summary with the decision in
   `docs/decisions/<scope>-planning-interview.md` or the project's named equivalent.
   Include volunteered constraints, examples, trade-offs, caveats, uncertainty, and
   rejected alternatives; label agent rationale separately. Keep only a link and
   decisions needed for current routing in `jumpstart.md`.
7. Finish only when the frontier is empty and the user confirms the shared
   understanding. Do not implement the result.

If research performed after an early interview contradicts or materially expands a
settled answer, stop and ask the user to reopen only the affected design-tree
branches with `matt-grill-with-docs`. The interview is not complete while those
branches remain unresolved.

## 4. Write The PRD Last

Ask for explicit authorization to draft the PRD after the user confirms the
interview result. Only then create `docs/prds/<scope>.md` from settled decisions,
verified evidence, explicit exclusions, acceptance criteria, and remaining
non-blocking questions.

Before that authorization:

- Store research under `docs/research/` and mark its verification status.
- Store synthesis only as non-authoritative pre-grill planning material outside
  `docs/prds/`.
- Do not label requirements approved, present recommendations as decisions, or
  begin production implementation.

After drafting, stop for PRD approval. PRD creation does not authorize Milestone 1.

## 5. Close Planning After Approval

After the user approves the PRD:

1. Make the approved PRD the sole execution authority for its scope. Record later
   approved amendments in the PRD and a decision record when the trade-off needs
   durable rationale.
2. Deactivate the source brief, pre-grill synthesis, draft requirements, and other
   superseded planning files. Add a lifecycle status and replacement pointer without
   rewriting the user's original content. Archive a file only when the repository
   has a defined archive convention and a concrete retention reason; otherwise mark
   it `SUPERSEDED` in place.
3. Remove deactivated files from `jumpstart.md`, continuation prompts, agent context,
   and normal read lists. Read them later only for provenance, attribution, or a
   named unresolved question.
4. Sweep the approved PRD, active decisions, project state, verification records,
   and `jumpstart.md` for inconsistent terms, duplicated rules, stale status,
   broken pointers, hidden prerequisites, and illogical milestone ordering. Apply
   `pstack-unslop` when available. Fix non-material defects directly and ask the user
   before changing approved meaning, scope, authority, licensing, or order.
5. Treat milestones as approval and evidence gates, not implementation batches.
   Put only the next smallest coherent vertical increment in active project state,
   with one observable outcome, the cheapest decisive test, prerequisites, and a
   stop condition. Order later increments by dependency and risk; do not create
   future scaffolding merely to make the plan look complete.

Planning is closed only when inactive inputs are out of normal routing, active
documents agree, and the next authorized increment is small enough to fail and pass
independently.
