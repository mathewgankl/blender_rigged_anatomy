---
name: matt-diagnosing-bugs
description: Diagnoses hard bugs and performance regressions with a reproducible feedback loop; use when behavior is broken, failing, throwing, flaky, or slow.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "diagnosing-bugs"
---

# Diagnosing Bugs

Redact secrets from commands, output, and artifacts. Read `jumpstart.md` and
relevant records under `docs/decisions/` before reasoning about the area.

## Workflow

1. Build one tight, deterministic, red-capable command that exercises the
   user's exact symptom. Prefer an existing test, request, CLI invocation,
   browser flow, replay, minimal harness, fuzz loop, or differential check.
2. Run it and minimize the reproducer one element at a time until every
   remaining element is load-bearing. If no loop is possible, report attempts
   and request access, a redacted artifact, or permission for instrumentation.
3. Produce three to five ranked, falsifiable hypotheses. State each prediction
   and show the list before testing, then continue unless asked to pause.
4. Test one variable at a time. Prefer debugger or REPL inspection, then
   targeted uniquely tagged logs. For performance, establish a measured
   baseline and use profiling or query plans.
5. At the correct seam, convert the minimal repro into a failing regression
   test before fixing. If no valid seam exists, report that design limitation.
6. Apply the smallest fix, run the regression test, and rerun the original
   unminimized loop.
7. Remove temporary instrumentation and verify no tagged logs remain.

Use project-native commands and files; this skill bundles no Bash or HITL
script. Ask before adding instrumentation or making any Git state change.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools before considering an agent. If delegation is necessary, use
one focused agent for one bounded question; never use broad fan-out.
