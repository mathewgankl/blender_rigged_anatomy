# Read This File First

**Status:** ACTIVE
**Purpose:** Universal repository entry point and operating policy
**Applies to:** All projects unless a higher-authority instruction overrides it
**Last verified:** 2026-09-14

Read this file at the start of every session. Transferable generic prompts establish
the baseline and must always be read before project prompts. Project prompts may
then specialize or explicitly override that baseline within their project scope.
Use `jumpstart.md` as the compact control center after initialization.

## 1. Start

1. Confirm the project root, repository structure, and version-control state. This
   inspection is the first project action; preserve unrelated work.
2. Read `prompts_transferable/generic_engineering_execution_protocol.md` as the
   generic execution baseline before any project prompt.
3. Read an existing `jumpstart.md` for routing and the latest user requirements.
   Read the `proj_*.txt` brief only before PRD approval or when `jumpstart.md` links
   it for an unresolved requirement. In a new project without `jumpstart.md`, read
   the brief and immediately create the compact stub defined below.
4. Identify and read every other applicable `ACTIVE` prompt in
   `prompts_transferable/`. Read optional prompts only when their activation
   condition is met.
5. Only after the generic prompts, read and execute applicable `ACTIVE` files in
   `prompts_project/`; honor each file's scope and approved overrides.
6. Create or update `jumpstart.md`. Keep only the information a fresh context needs
   to act correctly: phase/status, minimum read set, current authority, concise
   verified state, active decisions that affect routing, current blockers/risks,
   and one bounded next action. Link detailed records instead of copying them.
7. Before treating a named skill as unavailable, check
   `.opencode/skills/<name>/SKILL.md` when present. Read and apply its shared
   project policy even if the skill is absent from the session's advertised list.
8. Identify the active requirements, milestone, project state, and protocol.
9. Check for unrelated or uncommitted work and preserve it.
10. Verify relevant tools, dependencies, and environment facts instead of trusting
   old summaries.
11. Select one bounded objective with acceptance criteria and a stop condition.

Use this compact `jumpstart.md` shape unless the project already has a stricter
convention:

```markdown
# Project Jumpstart
**Status:** <current status>
**Phase:** <current phase or milestone>
**Updated:** <date>

## Read
<minimum ordered file set>

## Authority
<current approved requirement and active protocol links>

## Verified State
<facts needed for the next action>

## Active Decisions
<only decisions that affect current or next work>

## Blockers And Risks
<current items only>

## Next Action
<one bounded action and stop condition>
```

Do not use `jumpstart.md` as a diary, interview transcript, command log, research
report, or archive. Replace stale state rather than appending history.

Use the smallest authoritative reading set:

- **Planning:** Follow the Section 1 order, then use the active requirements and
  only the evidence linked by the control center. Clarify material ambiguity and
  obtain approval before execution.
- **Execution:** Follow the Section 1 order, then read approved requirements and
  only linked evidence.
- **Continuation:** Follow the Section 1 order, verify critical claims from the
  minimum referenced state, and run the smallest relevant smoke test.
- **History:** Read deprecated or archived material only when historical evidence
  is required.

## 2. Read Order And Authority

Read order does not set authority. Generic prompts are read first so the shared
baseline is visible; an approved project prompt has higher authority only within its
stated project scope.

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

Use project-prompt overrides sparingly:

- Point to generic policy for unchanged behavior instead of copying it.
- Specialize generic placeholders without calling that an override when no rule
  conflicts.
- Before writing or editing a project prompt that contradicts a generic prompt,
  show the user the generic clause, proposed replacement, project-only scope,
  reason, and consequences. Obtain explicit approval before writing the conflict.
- Record an approved conflict in the project prompt as `Overrides: <generic file
  and section - scoped replacement and reason>`. Use `Overrides: NONE` otherwise.
- If an existing project/generic conflict has no recorded approval, stop and ask the
  user before applying, normalizing, or expanding it.

## 3. Execution

- Inspect before editing; do not assume repository structure or technology.
- Follow established conventions and make the smallest correct change.
- Work only within the authorized milestone or request.
- Split authorized work into the smallest coherent increment that proves one
  observable behavior with the cheapest decisive test. Order increments by actual
  dependency and risk: resolve blockers first, prefer pure/local/reversible work
  before framework mutation or external integration, and defer expensive checks
  until their cheaper prerequisites pass. If no safe testable order exists, ask the
  user before execution.
- Prefer direct tools for known files, searches, builds, tests, and facts.
- Delegate only bounded, independent, verifiable work; assign one writer per file
  or tightly coupled module and verify all delegated output.
- Before any research batch or model/subagent route change, apply the allocation
  preflight and route-fit check in
  `prompts_transferable/generic_engineering_execution_protocol.md`.
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

Delegated research follows the allocation and route-fit rules in the generic
execution protocol.

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
- `jumpstart.md`: Compact project control center defined in Section 1. Keep detailed
  execution evidence in project state.
- `docs/prds/`: Approved requirements.
- `docs/decisions/`: Material decisions and evaluated credible alternatives.
- `docs/research/`: Reusable verified findings and sources.
- `docs/verification/`: Durable milestone or release evidence.
- `docs/agent-operations-log.md`: Non-authoritative administrative/debug reference.
  Create it only after a real issue such as routing mismatch, invocation failure,
  quota failure, configuration troubleshooting, or retry diagnosis. Record the
  event, impact, evidence, resolution, and current consequence. Keep only an active
  consequence and a pointer in `jumpstart.md`; omit the log from minimum reads once
  the issue no longer affects work.
- `prompts_project/`: Active project-specific prompts.
- `prompts_transferable/`: Reusable prompts and protocols.
- `prompts_transferable/self-evaluation-and-user-learning-loop.md`: Optional,
  explicitly activated feedback on instruction quality, context, routing, and work
  efficiency.

Keep one active authority per subject and link shared policy instead of copying it.
Update documentation with behavior; never present plans as implemented. Support
material claims with paths, symbols, revisions, commands, tests, or primary URLs.
For substantive prompt, requirements, decision, state, and handoff edits, apply
`pstack-unslop` when available. Preserve constraints and attribution while removing
stale wording, repetition, vague claims, and synonym drift.
Keep raw logs and large generated reports temporary or in managed artifacts. The
operations log contains concise diagnosis and outcome, not raw command output.

Before a context reset, restart, or milestone stop, sweep the active documentation
and its direct pointers. Correct stale status, conflicting authority, repeated or
contradictory requirements, broken links, inconsistent terms, illogical ordering,
oversized execution blocks, and claims that do not match source or tests. Apply
`pstack-unslop` when available. Fix mechanical issues directly; ask the user about
any issue whose resolution changes approved meaning, scope, authority, licensing,
or milestone order. Then reconcile `jumpstart.md` and detailed project state with
the workspace. Keep only fresh-context routing in `jumpstart.md`; put commands and
results in verification records and administrative incidents in the operations log.
Retain durable history in decisions, research, verification, and Git.

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

After a PRD is approved, follow
`prompts_transferable/planning-interview-and-prd-gate.md` to deactivate its source
brief, pre-grill synthesis, and superseded planning files. Preserve user-supplied
reasoning and provenance, but remove inactive files from normal continuation reads.

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

Run `prompts_transferable/self-evaluation-and-user-learning-loop.md` only when the
user explicitly requests it or an active project prompt opts in. Do not add an
unsolicited evaluation to ordinary completion reports.
