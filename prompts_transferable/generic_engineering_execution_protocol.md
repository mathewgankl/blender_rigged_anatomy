# Generic Engineering Execution Protocol

**Status:** ACTIVE
**Purpose:** Reusable engineering, research, verification, and delegation policy
**Applies to:** Engineering sessions before project-specific instructions
**Last verified:** 2026-09-15
**Supersedes:** NONE
**Superseded by:** NONE
**Primary evidence:** `read_first.md`

Follow `read_first.md` for authority, repository safety, documentation, and lifecycle
policy. Use active briefs for planning, approved PRDs for execution, and project
prompts only for scoped specialization or approved overrides.

If no milestone is authorized, perform discovery and planning only. Do not start
production implementation or advance beyond the authorized milestone.

## 1. Execution And Decisions

- Inspect the relevant workspace, requirements, source, tests, dependencies, and
  toolchain before changing them.
- Prefer the smallest correct, verifiable change and avoid speculative behavior.
- Treat milestones as approval and evidence gates. Work through coherent increments
  without beginning later scope.
- Test cheap assumptions. Ask before material decisions involving security, privacy,
  licensing, persistent or public interfaces, migration, substantial cost, or
  irreversible action.
- Preserve unrelated work and obtain authorization for remote, destructive, costly,
  or publishing actions.
- Completion requires approved acceptance and verification, not implementation alone.

Track facts, assumptions, decisions, and open questions clearly enough to avoid
silently treating one as another. Persist them only when the documentation policy in
`read_first.md` requires a durable record.

Before starting newly ordered or planned work, apply the context-fit and deferral rule
in `docs/documentation-map.md`.

## 2. Research And Planning

Research just in time and only when it can change the current decision. Prefer local
and primary evidence, official sources, and focused experiments. Avoid broad or
duplicate research and stop when the decision has adequate support.

Milestone 0 planning follows
`prompts_transferable/planning-interview-and-prd-gate.md`. Do not draft a PRD before
the required interview is complete and the user separately authorizes drafting.

## 3. Models, Tools, And Agents

Use direct tools when they can complete the work efficiently. Delegate when work is
independent, bounded, objectively checkable, and likely to save more context or time
than dispatch and reconciliation cost.

Choose models, effort, tools, and permissions according to task difficulty and error
cost. Ask before a material user-controlled change in route or cost. Do not claim a
model or effort setting was applied unless the interface exposes or verifies it, and
do not use an unapproved fallback when the user or project requires a specific route.

Give agents only relevant context and no credentials. Avoid duplicated or dependent
parallel work and conflicting ownership. The primary agent must verify claims, inspect
written changes, and run relevant integration checks. Agent agreement is not proof.

## 4. Milestones

The active PRD owns project milestones. Each milestone needs clear scope, acceptance,
verification, and a stop boundary. Detail only the next useful increment and order
work by real dependencies and risk rather than a generic phase template.

## 5. Implementation And Verification

Confirm expected behavior, implement minimally, run the most relevant checks, and
inspect the resulting diff. Add regression tests for reproduced defects and cover
important failure or cleanup behavior where applicable. Prefer deterministic tests
and cheaper evidence before expensive end-to-end checks.

At a milestone gate, run the approved acceptance checks, report material gaps or
risks, preserve durable evidence under `read_first.md`, and stop unless further work
is already authorized.

## 6. Performance

Optimize only measured bottlenecks against representative workloads. Preserve
correctness, compare reproducible results, and reject changes without meaningful
improvement.
