---
name: pstack-interrogate
description: "Performs an adversarial, findings-first review of supplied code or changes; Use ONLY when explicitly requested for interrogation, challenge, stress testing, or blind-spot review."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "interrogate"
---

# PStack interrogate

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

This workflow is read-only. It never auto-applies fixes, edits files, creates
commits, pushes changes, opens pull requests, or changes review scope.

Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize boundary discipline, reader load, root causes, and proof.

## Workflow

1. Determine scope only from material supplied by the user or already present in
   the authorized workspace. State the intended behavior in one concise paragraph.
2. Inspect the code directly first. Review correctness, security, data integrity,
   concurrency, lifecycle, error handling, compatibility, maintainability, and
   missing behavior-level tests where relevant.
3. Use bounded read-only agents only when independent review adds clear value. Keep
   their scope and rubric aligned; do not depend on a specific model.
4. Verify every candidate finding against source and context. Deduplicate overlaps,
   note agreement only as supporting signal, and reject claims that lack evidence.
5. Rank findings by real impact and likelihood, not reviewer count.

## Output

Lead with actionable findings ordered by severity and supported by concrete evidence.
Include relevant open questions and testing gaps. If there are no findings, say so
and state residual risks.
