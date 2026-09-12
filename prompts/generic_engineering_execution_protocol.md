# Generic Engineering Execution Protocol

**Status:** ACTIVE  
**Purpose:** Reusable staged engineering, research, testing, and agent-routing policy  
**Applies to:** New project execution prompts and protocol reviews  
**Last verified:** 2026-09-04  
**Supersedes:** NONE  
**Superseded by:** NONE  
**Primary evidence:** `read_first.md`

Read `read_first.md` first and obey its authority, repository, Git/remote, CI,
secrets, dependency, documentation, handoff, deprecation, archival, and removal
policies. Use the active brief for planning, approved PRDs for execution, and the
project protocol over this generic fallback.

If no current milestone is explicit, execute only **Milestone 0**. Do not start
production implementation until Milestone 0 is reviewed or its acceptance
criteria explicitly authorize continuation. Stop after the authorized milestone.

## 1. Execution And Decisions

1. Inspect the relevant workspace, requirements, source, tests, dependencies,
   toolchain, and version-control state before proposing changes.
2. Label verified facts, assumptions, decisions, hypotheses, and open questions.
3. Prefer the smallest correct, verifiable change; avoid speculative abstractions,
   options, compatibility layers, and fallbacks.
4. Work in independently verifiable vertical increments with observable behavior,
   tests, and concise documentation. Execute only the current milestone.
5. Preserve unrelated changes. Never revert, overwrite, delete unrecoverable user
   work, commit, push, publish, install system software, change system/remote/Git
   settings, expose secrets, or incur external cost without authorization.
6. Stop for user decision before destructive or irreversible action, substantial
   rework or cost, security/privacy/licensing risk, persistent/public format or API
   commitment, migration, or material architecture/compatibility choice.
7. Completion requires the milestone's acceptance criteria, verification, and
   documentation, not implementation alone.

Maintain an assumption/decision register. Handle assumptions as follows:

- **Material/blocking:** ask before implementation when architecture, public
  behavior, security, licensing, persisted data, external cost, compatibility, or
  irreversible choices may change.
- **Cheaply testable:** inspect source, run a focused experiment, or test rather
  than asking the user to speculate.
- **Low-risk/reversible:** apply and record the conventional minimal default
  without interrupting progress.

Batch related decisions. State the required decision, current impact, recommended
option, credible alternatives, relative cost/benefit/risk/reversibility, and the
effect of deferral. Raise only assumptions material to the current or next
milestone. Never silently resolve a material authority conflict; follow
`read_first.md` and ask when the resolution is material or irreversible.

## 2. Research

Research just in time. First state the exact unanswered question, current impact,
decision it changes, minimum credible source, and stop condition. Prefer:

1. Local code, tests, configuration, and documentation.
2. Primary implementation source.
3. Official API, language, framework, or vendor documentation.
4. Specifications, standards, and primary papers.
5. Focused experiments or minimal prototypes.
6. Secondary sources only when primary evidence is insufficient.

Do not broadly crawl, consume full overviews or videos when targeted text/source
suffices, survey literature/competitors without request, analyze multiple large
references without need, research future milestones, or collect beyond adequate
support. Optimize for the next verified decision, not exhaustive knowledge.

Expand only for an unexplained reproducible failure, conflicting primary
evidence, a blocking undocumented API/format, required licensing/security/privacy/
compatibility/destructive-change confirmation, a measured algorithm-specific
bottleneck, or explicit user request. Reproduce and isolate failures and form a
specific hypothesis first. Prefer a safe, cheap, deterministic, conclusive
experiment over extended research.

## 3. Models, Tools, And Agents

Minimize total cost: model/tool/research usage, duplicated context, reconciliation,
verification, and likely rework. Use the cheapest model likely to produce a
verifiably correct result; a stronger single model can cost less than several
cheap agents. Map capability tiers to available models in configuration, never to
vendor names:

| Tier | Use |
|---|---|
| `FAST_MODEL` | Retrieval, indexing, classification, formatting, and easily checked mechanical transforms |
| `BALANCED_MODEL` | Localized implementation, ordinary debugging/tests/integration, and moderate analysis |
| `DEEP_MODEL` | Architecture, numerical/concurrent/security work, destructive migration, persistent/public formats/APIs, and difficult root cause or high-risk review |
| `MULTIMODAL_MODEL` | Necessary visual evidence such as screenshots, diagrams, or PDFs |

If model routing is unavailable, constrain agent type, scope, thoroughness,
context, permissions, tools, and output. An agent name does not prove cost; inspect
configuration when cost matters.

Use direct tools for known file/symbol/string searches, one to three known files,
known builds/tests/formatters/benchmarks, bounded status/diff review, one known URL,
or a simple environment fact. Long commands still use execution tools.

Delegate only when exploration is multistep or work is genuinely independent,
bounded by exact questions/sources, objectively checkable, and saves more time or
context than dispatch/reconciliation costs. Defaults: no subagent for initial
discovery, integrated planning, or localized implementation; at most one for
focused exploration; at most two for two independent implementation areas; one
post-implementation reviewer for high risk. More than two concurrent agents needs
explicit justification or user approval.

Do not parallelize dependent tasks, shared files/interfaces, a shared unresolved
decision, duplicate discovery, unverifiable output, or work under a constrained
budget. Do not solicit competing full plans; use one analysis plus one focused
independent review only when error cost warrants it.

Assign one writer per file/tightly coupled module. Research/review is read-only
unless writing is explicit. For parallel implementation, define interfaces and
non-overlapping ownership first; keep shared config/dependencies with one owner;
require changed-file reports; then inspect the combined diff and run integration
tests.

### Scenario Routing

| Scenario | Execution | Tier/effort | Permission |
|---|---|---|---|
| Exact lookup; read a few known files | Direct tools | None | Read-only |
| Map small repository | Primary or 1 explorer | Fast/low | Read-only |
| Map large unfamiliar repository | 1 explorer | Fast-balanced/low-medium | Read-only |
| Initial planning | Primary | Balanced-deep/medium-high | Read-only until accepted |
| Material architecture | Primary | Deep/high | Read-only or docs-only |
| Targeted documentation | Primary or 1 researcher | Fast/low | Restricted web |
| Conflicting specifications | 1 researcher, then primary decision | Balanced-deep/medium-high | Read-only |
| Numerical/scientific algorithm | Primary or 1 specialist | Deep/high | Read-only before implementation |
| Routine localized feature | Primary | Balanced/medium | Assigned files |
| Repetitive stable-interface work | 1 implementer | Fast-balanced/low-medium | Assigned files |
| Cross-cutting refactor | Primary | Deep/high | Repository write |
| Straightforward test generation | Test agent only if worthwhile | Fast-balanced/low-medium | Tests only |
| Difficult bug | Primary; optionally 1 independent hypothesis agent | Deep/high | Initially read-only |
| Security/destructive migration review | Independent reviewer after proposal | Deep/high | Read-only |
| Ordinary review | Primary or 1 reviewer | Balanced/medium | Read-only |
| High-risk review | Independent reviewer | Deep/high | Read-only |
| Documentation formatting | Agent only if volume warrants | Fast/low | Docs only |
| Benchmark execution | Direct tools | None | Build/run only |
| Benchmark interpretation | Primary | Balanced-deep/medium | Read-only |
| UI screenshot comparison | Visual reviewer | Multimodal/medium | Read-only |
| Video research | Avoid; prefer source/text/transcript | Multimodal only if unavoidable/focused | Read-only |

For OpenCode-style tools, use Glob/Grep/Read for exact work; `explore` quick for
basic mapping, medium for cross-module discovery, and very thorough only after
recording why medium failed. Use `general` only for genuinely multistep work that
direct tools and focused exploration cannot handle.

### Settings And Escalation

- Retrieval: fast/low, deterministic, concise (about 300-700 words), local
  read/search unless targeted web is required.
- Routine implementation: balanced/medium, deterministic, with only assigned
  files, interfaces, tests, current state, and scoped write access.
- Algorithms/architecture: deep/high, concise evidence/tradeoffs/uncertainties,
  material constraints only, read-only until approach selection.
- Debugging: balanced after reproducing conventional failures; deep for
  nondeterminism, concurrency, numerical instability, memory corruption, or
  cross-system failures; increase effort only after narrowing.
- Review: balanced ordinarily; deep for security, concurrency, persistence,
  numerical correctness, public APIs, or destructive operations; findings first,
  severity ordered, read-only.
- Brainstorming: balanced/deep, medium effort and moderate diversity, bounded
  materially different options; no implementation unless separately requested.

Use low diversity for implementation/verification and higher diversity only for
ideation when supported. Request concise conclusions, assumptions, evidence,
tradeoffs, uncertainty, and reproducible checks, not verbosity or hidden
chain-of-thought.

For low-risk work, escalate direct tools -> fast retrieval/mechanical work ->
balanced interpretation/implementation -> deep only for justified complexity,
ambiguity, or error cost. Start deep for security boundaries, data loss/destructive
migration, public/persistent interfaces, numerical correctness, concurrency,
distribution-affecting licensing, or irreversible infrastructure/deployment.
Escalate for a failed criterion, conflicting primary evidence, material ambiguity,
repeated reproduction failure, or capability mismatch. Do not rerun the same broad
prompt across models; narrow the question/evidence/experiment. Reassess delegation
after one failed or quota-limited attempt.

### Subagent Contract And Review

Give each agent only the minimum complete context; never credentials, unrelated
history/documents, avoidable raw logs, all future milestones, or speculative
alternatives.

```text
Task/Purpose: <concrete result and current decision or milestone>
Inputs: <exact paths, URLs, revisions, interfaces, and state>
Questions: <short exact list>
Scope: <in scope; out of scope>
Model/Effort: <fast|balanced|deep|multimodal; low|medium|high>
Tools/Permissions: <read-only, web limits, write paths, commands>
Evidence: <paths/symbols/lines/commands/tests/citations>
Deliverable: <format and maximum size>
Verification/Stop: <checks; completion and blocker conditions>
```

Subagent output is evidence, not authority. The primary agent checks citations and
commands, separates findings from recommendations, rejects irreproducible claims,
inspects every produced diff, independently runs relevant tests, resolves conflicts
against requirements/primary evidence, and updates durable state only with verified
conclusions. Give independent reviewers requirements, criteria, and actual diff,
not the implementer's persuasive narrative. Agent agreement is not proof.

## 4. Milestones

Derive and adapt project milestones after discovery; remove inapplicable stages
rather than creating empty future scaffolding.

### Milestone 0: Discovery And Planning
Inspect requirements, workspace, toolchain, dependencies, tests, constraints,
licenses, and material ambiguities. Define the smallest useful implementation
milestone and objective acceptance criteria.

### Milestone 1: Harness And Minimal Vertical Slice
Establish build/test workflow and the smallest end-to-end behavior proving the
architecture without optional features.

### Milestone 2: Correctness And Failure Handling
Cover normal, boundary, malformed, and failure inputs; add deterministic errors,
regressions, cleanup, recovery, and repeated-run behavior.

### Milestone 3: External Integration
Integrate the required application/service/platform/workflow; test lifecycle,
state synchronization, installation, and removal.

### Milestone 4: Feature Expansion
Add one independently testable capability at a time and rerun regressions.

### Milestone 5: Performance
Baseline representative workloads, profile measured bottlenecks, optimize supported
hypotheses, and reverify correctness.

### Milestone 6: Compatibility And Release
Exercise the supported matrix, packaging, install/upgrade/rollback, documentation,
and release automation.

For each milestone define purpose; inputs/outputs/dependencies; explicit scope;
objective criteria; required tests; applicable failure/rollback strategy;
documentation; stop condition; and decisions required before the next milestone.

## 5. Implementation And Verification

For each increment:

1. Confirm behavior and acceptance criteria; reproduce defects.
2. Add or identify the smallest useful failing test where practical.
3. Make the smallest correct change.
4. Run the narrow test; diagnose locally before external research.
5. Run affected integration/regression tests.
6. Review the diff for unintended changes.
7. Record verified results and update project state before proceeding.

Before implementation and at major gates, confirm every material requirement maps
to a milestone/test; ordering matches dependencies; no unresolved decision/API/
format/tool blocks work; interfaces, ownership, lifecycle, errors, and cleanup are
defined; correctness and local tests precede optimization and remote automation;
applicable security/privacy/licensing/migration/packaging/rollback/compatibility are
covered; unsupported/deferred scope is explicit; the next milestone is independently
verifiable; and no circular dependency, hidden prerequisite, or curiosity-only
research remains. Perform this bounded review directly, not with a broad planner.

At the milestone gate, report outcome; changed files; commands/tests; pass/fail/
skip/benchmark results; assumptions/risks/blockers; scope deviations; and next
decision/milestone. Do not continue unless already authorized. If criteria fail,
record the concrete blocker; never declare completion from implementation alone.

## 6. Testing

Plan tests during discovery and add applicable layers incrementally: static/
format/type checks, unit, contract, integration, critical end-to-end, regression
for every reproduced defect, supported compatibility, and performance benchmarks
separate from correctness tests.

Use deterministic fixtures/fixed seeds; record environment and dependency
versions; assert observable behavior; cover expected failure, cleanup,
cancellation, and repeated runs. Run narrow tests while iterating and the relevant
full suite at milestone gates. Coverage is not a substitute for meaningful
assertions; do not normalize flakes. Reserve expensive end-to-end tests for
behavior cheaper layers cannot prove. A milestone passes only when acceptance
tests pass or a concrete blocker is documented.

## 7. Benchmarking

Do not optimize before a valid baseline. Define measured behavior; representative
small/medium/large workloads; invariant correctness checks; hardware, OS, runtime,
build mode, and dependencies; warm-up; repetitions; reported statistics (for
example median/percentiles); and expected variance.

Then measure the correct unoptimized implementation, profile instead of guessing,
set targets from user needs/baseline/hardware, estimate credible options, and
change one variable at a time. Repeat identical benchmarks, reject changes without
meaningful improvement, and rerun behavioral/numerical correctness checks. Keep
noisy thresholds non-blocking until stable. Record baseline and optimized results
with source revision; follow `read_first.md` for durable records and artifacts.
