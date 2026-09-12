# Read This File First

**Status:** ACTIVE  
**Purpose:** Universal repository entry point and operating policy  
**Applies to:** All projects unless a higher-authority instruction overrides it  
**Last verified:** 2026-09-13

Read this file at the start of every session. On project start, read the active
`proj_*.txt` user brief, execute the applicable `ACTIVE` instructions in
`prompts/`, and create `jumpstart.md`. Use `jumpstart.md` as the control center
thereafter. Load only files required by it or the current task.

## 1. Start

1. Confirm the project root, files, and version-control state.
2. Read the active `proj_*.txt` brief.
3. Read and execute applicable `ACTIVE` files in `prompts/`; honor each file's
   scope and authority.
4. Create `jumpstart.md` if absent. Record project-specific instructions, current
   milestone and status, key decisions, verified build/test progress, blockers,
   and one next action. Update it after each material decision or build checkpoint.
5. On continuation, read `jumpstart.md` and its minimum required file set.
6. Before treating a named skill as unavailable, check
   `.opencode/skills/<name>/SKILL.md` when present. Read and apply its shared
   project policy even if the skill is absent from the session's advertised list.
7. Identify the active requirements, milestone, project state, and protocol.
8. Check for unrelated or uncommitted work and preserve it.
9. Verify relevant tools, dependencies, and environment facts instead of trusting
   old summaries.
10. Select one bounded objective with acceptance criteria and a stop condition.

Use the smallest authoritative reading set:

- **Planning:** `jumpstart.md`, the active brief or user requirements, then its
  listed planning instructions. Clarify material ambiguity and obtain approval
  before execution.
- **Execution:** Approved requirements, active project state, project-specific
  protocol, and only the decisions or evidence linked by the control center.
- **Continuation:** `jumpstart.md`, active project state, then their minimum
  referenced files; verify critical claims and the smallest relevant smoke test.
- **History:** Read deprecated or archived material only when historical evidence
  is required.

## 2. Authority

Apply instructions within their stated scope, in this order:

1. Platform and system instructions.
2. The user's latest explicit instruction.
3. Approved current requirements.
4. Repository- and project-specific instructions.
5. Approved decision records.
6. `jumpstart.md` for current routing, status, and the next bounded action.
7. Active detailed project state and milestone instructions.
8. This generic policy.
9. Templates and deprecated records, as non-authoritative context only.

Newer text overrides older text only when it has equal or greater authority.
Never silently resolve a material conflict: identify its impact, recommend a
resolution, and ask when the choice is material or irreversible.

## 3. Execution

- Inspect before editing; do not assume repository structure or technology.
- Follow established conventions and make the smallest correct change.
- Work only within the authorized milestone or request.
- Prefer direct tools for known files, searches, builds, tests, and facts.
- Delegate only bounded, independent, verifiable work; assign one writer per file
  or tightly coupled module and verify all delegated output.
- Distinguish facts, assumptions, hypotheses, decisions, and unresolved questions.
- Test cheap assumptions. Ask before material architecture, public behavior,
  persistent data, security, privacy, licensing, compatibility, migration, cost,
  or irreversible decisions.
- Do not add speculative abstractions, options, dependencies, compatibility code,
  fallbacks, or future scaffolding without a demonstrated requirement.
- Preserve unrelated changes. Never revert or delete work you did not create
  unless explicitly authorized.
- Stop and report a concrete blocker when acceptance criteria cannot be met.

## 4. Research

Research only a question that affects the current decision or milestone. Define
the question, impact, minimum credible source, and stop condition first.

Prefer local code and tests, primary implementation sources, official
documentation or specifications, focused experiments, then secondary sources.
Avoid broad crawls, surveys, videos when text suffices, duplicate research, and
future-milestone investigation. Stop when primary evidence adequately answers the
question. Record reusable conclusions and exact sources, not browsing logs.

## 5. Repository and Tools

- Use existing structure. Create directories and documents only with their first
  real use; do not generate empty scaffolding.
- Verify installed tools through PATH, standard locations, package managers, or
  vendor discovery; never scan the entire disk by default.
- Ask before initializing version control, installing software, changing system
  settings, adding machine-wide dependencies, or incurring external cost.
- Prefer isolated project-local dependencies and lockfiles or exact revisions.
- Add only demonstrated dependencies; record versions, licenses, attribution, and
  relevant source revisions.
- Keep generated output, caches, downloads, credentials, and local settings out of
  source control unless they are intentional release assets or approved evidence.

## 6. Git, Remotes, and Secrets

- Check repository state before Git operations. If uninitialized, get approval
  before `git init`.
- Before committing, inspect status and diffs and stage only intended files.
- Commit, amend, tag, push, publish, create remotes or pull requests, release, or
  change remote settings only when explicitly requested.
- Never use destructive history or worktree commands on unreviewed work.
- Do not change Git identity or authentication automatically.
- Give CI and automation least privilege; keep their commands locally reproducible.
- Never expose credentials, tokens, private keys, personal data, or confidential
  information in prompts, source, documentation, logs, artifacts, or Git history.
  If exposure is suspected, remove and rotate the secret immediately.

## 7. Documentation and State

Follow existing conventions. When no convention exists, use these only as needed:

- `docs/project-state.md`: Concise current milestone, evidence, blockers, tests,
  changed files, and one bounded next action.
- `jumpstart.md`: Project control center, current phase, minimum read set, status,
  and next action. Keep detailed execution evidence in project state.
- `docs/prds/`: Approved requirements.
- `docs/decisions/`: Material decisions and evaluated credible alternatives.
- `docs/research/`: Reusable verified findings and sources.
- `docs/verification/`: Durable milestone or release evidence.
- `prompts/`: Active reusable or project-specific prompts.

Keep one active authority per subject and link shared policy instead of copying it.
Update documentation with behavior; never present plans as implemented. Support
material claims with paths, symbols, revisions, commands, tests, or primary URLs.
Keep raw logs and large generated reports temporary or in managed artifacts.

Before a context reset or milestone stop, reconcile `jumpstart.md` and detailed
project state with the workspace. Record the objective, status, acceptance
criteria, verified facts, active decisions, changed files, commands and results,
risks or blockers, and minimum next reads and action. Replace stale state instead
of appending a diary; retain history in decisions, verification, and Git.

## 8. Testing and Performance

- Define acceptance criteria before implementation.
- Reproduce defects and add the smallest useful failing test where practical.
- Run narrow tests while iterating, then affected integration and regression tests.
- Use deterministic fixtures and fixed seeds where possible; test failures,
  cleanup, repeated runs, and supported environments.
- Record commands, environment, dependency versions, results, and known gaps.
- Do not optimize before a correct baseline. Define representative workloads and
  correctness invariants, profile measured bottlenecks, change one variable at a
  time, repeat measurements, and reject changes without meaningful improvement.

Implementation alone does not complete a milestone; acceptance tests and durable
verification are required.

## 9. Document Lifecycle

- **DRAFT:** Incomplete and non-authoritative.
- **ACTIVE:** Current authority within its scope.
- **DEPRECATED:** Transitional; identify its replacement or explain its absence.
- **SUPERSEDED:** Replaced by a named newer record.
- **ARCHIVED:** Inactive and retained for a documented historical need.

Before deprecating or removing behavior, files, APIs, formats, configuration, or
dependencies, identify consumers and persisted data, define replacement and
migration needs, update references and tests, and obtain approval for material or
external effects. Do not add compatibility code without concrete consumers.

Use version-control history as the default archive. Archive only for a specific
audit, contractual, release, migration, or reproducibility need; record provenance,
reason, replacement, and retention condition. Never archive secrets, caches,
builds, dependencies, or large raw logs in the repository.

Ask before deleting untracked or uncommitted user files without reliable recovery.
Remove reproducible disposable artifacts instead of archiving them.

## 10. Completion

Before reporting completion:

1. Verify acceptance criteria and review the final diff.
2. Run the smallest relevant tests plus affected regressions.
3. Confirm no unrelated work, secrets, generated artifacts, or stale references
   were introduced.
4. Update `jumpstart.md`, durable state, and documentation when status, behavior,
   routing, or handoff changed.
5. Report changed files, commands, results, remaining risks or blockers, and the
   next required decision.
6. Stop at the authorized boundary; do not begin the next milestone automatically.
