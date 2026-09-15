---
name: pstack-blast-radius
description: "Finds indirect breakage risks and tests the safety assumptions behind a change; use when assessing blast radius, hidden callers, or a suspicious diff."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "blast-radius"
---

# PStack blast radius

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize boundary discipline, root-cause analysis, idempotence, and proof against
the real behavior.

## Workflow

1. Establish the authorized change set from supplied files, context, or an already
   available diff. Do not fetch branches, inspect remotes, or widen the scope.
2. Describe the behavioral change, including altered timing, state, serialization,
   cleanup, and error behavior that a line-by-line diff can hide.
3. Search direct callers, then follow contracts that symbol search misses: public
   types, configuration, database fields, wire formats, feature flags, lifecycle
   hooks, generated output, and consumers in other modules or languages.
4. Find the facts on which safety depends. Prefer direct
   source evidence, a failure-path trace, an existing focused test, or execution of
   the real path. Mark assumptions that cannot be executed as unproven.
5. Use bounded read-only agents only when independent investigation adds value, and
   verify their findings.
6. Rank confirmed risks by likelihood and impact. Separate risks from cases checked
   and cleared. Do not pad the result with generic possibilities.

## Output

Put actionable findings first, cite concrete evidence, distinguish observation from
inference, and identify the cheapest useful check for unresolved risk.
