---
name: pstack-tdd
description: "Runs a focused red-green regression workflow; use when TDD or a failing test is requested, or when a bug has an obvious cheap local test target."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "tdd"
---

# PStack TDD

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize root causes, behavior-level proof, minimal changes, and verifiable units.

## Workflow

1. Identify intended behavior, current behavior, the affected path, and the smallest
   observable reproduction. Reproduce before proposing a fix.
2. Respect the current scope. In read-only work, describe the test and evidence but
   do not create or edit it. A request for analysis does not imply write permission.
3. Use the nearest existing test style and harness. Do not install packages, add a
   test framework, or introduce new test dependencies for this workflow.
4. Write the smallest behavior-focused regression test that would catch the bug.
   Avoid implementation assertions, broad fixtures, timing dependence, and mocks
   that replace the behavior under test.
5. Run the new test before the production fix. Confirm that it fails for the expected
   reason; repair a false-positive or unrelated failure before proceeding.
6. Make the smallest root-cause fix, rerun the focused test, then run nearby existing
   checks justified by the affected boundary.
7. If a practical failing test is unavailable, say why before the fix and use the
   closest existing executable check. Prefer no new test to a misleading one.

Use direct tools first. A bounded agent is justified only for an independently
inspectable area, and its report is not test evidence.

## Output

Name the red check and failure, the green check, nearby validation, and any evidence
that could not be obtained. Never claim red-green evidence that was not observed.
