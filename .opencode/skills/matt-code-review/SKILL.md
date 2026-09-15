---
name: matt-code-review
description: Use ONLY when explicitly requested to perform a broad findings-first review of a branch, pull request, worktree, or diff against local requirements.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "code-review"
---

# Code Review

Review read-only along two separate axes: **Standards** and **Spec**. Findings
are the primary output, ordered by severity within each axis and supported by
file and line references.

## Workflow

1. Establish the review range from the user's fixed point. If none is given,
   ask. Validate the ref and inspect the three-dot diff against its merge base.
2. Find the originating local requirement from a user-provided path, commit
   references, `docs/`, `specs/`, or project instructions. Do not fetch an
   issue or use a remote without permission. If no spec exists, say so.
3. Read local standards such as `AGENTS.md`, `CONTRIBUTING.md`, style guides,
   linters, tests, and requirements. Local documented policy overrides generic
   review heuristics.
4. Inspect the diff and nearby code directly. Do not use parallel review agents
   or broad fan-out.
5. Report **Standards** findings: documented-rule violations first, then clearly
   labeled judgment calls such as duplication, unclear names, data clumps,
   primitive obsession, repeated switches, shotgun surgery, divergent change,
   speculative generality, message chains, middle men, or feature envy.
6. Report **Spec** findings: missing or partial requirements, incorrect
   behavior, and unrequested scope. Quote or cite the local requirement.
7. State explicitly when an axis has no findings, then note residual risks and
   unrun tests. Keep the axes separate rather than reranking them together.

Do not edit files, install dependencies, or change repository state during the
review.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.
