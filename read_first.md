# Read This File First

**Status:** ACTIVE
**Purpose:** Universal repository entry point and operating policy
**Applies to:** All projects unless a higher-authority instruction overrides it
**Last verified:** 2026-09-15

Use `jumpstart.md` only to route a fresh context. Read the generic protocol before
applicable project instructions, but open supporting records and source only when the
current task needs them.

## Start

1. Inspect the project root and version-control state; preserve unrelated work.
2. Read the generic protocol's metadata, preamble, execution core, and any section
   relevant to the current work.
3. Follow `jumpstart.md` when present. Before PRD approval, use the active brief;
   afterward, read it only for a named unresolved question or provenance need.
4. Read the metadata, preamble, and relevant sections of the routed project prompt,
   current state, approved requirements, and decisions.
5. Verify relevant environment facts and select one authorized objective with clear
   acceptance and a stop boundary.

Keep `jumpstart.md` to minimum-read, authority, and current-state pointers. It is not
a status record, glossary, transcript, log, or archive. Update it only when routing
changes.

## Authority

Read order does not determine authority. Apply instructions within their scope in
this order:

1. Platform and system instructions.
2. The user's latest explicit instruction.
3. Approved requirements.
4. Approved project instructions.
5. Approved decisions.
6. Generic policy.
7. Current project state and evidence.
8. Templates and inactive records as context only.

Do not silently resolve a material conflict. Ask before changing approved meaning,
scope, authority, licensing, milestone order, or another hard-to-reverse commitment.
A project prompt may override generic policy only through an approved, scoped entry
under `Overrides`; otherwise it should point to generic policy rather than repeat it.

## Execution

Follow the generic execution protocol. Work only within authorized scope, preserve
unrelated changes, and ask before material or hard-to-reverse decisions.

## Research

Follow the generic research policy. Preserve durable conclusions and sources, not
browsing history.

## Repository Safety

- Use existing structure and add dependencies only for demonstrated needs.
- Ask before initializing version control, installing software, changing machine or
  remote settings, or incurring external cost.
- Do not change Git identity or authentication without authorization.
- Inspect status and diffs before commits. Commit, amend, tag, push, publish, create
  remotes or pull requests, and release only when explicitly requested.
- Do not use destructive Git or filesystem operations on unreviewed work.
- Keep credentials, personal data, confidential information, caches, downloads, and
  local settings out of source control and distributable artifacts.
- If a secret may have been exposed, remove it from further exposure and tell the
  user it must be rotated.
- Preserve required dependency versions, licenses, attribution, and provenance.

## Documentation

`docs/documentation-map.md` defines document roles, access conditions, hierarchy, and
downstream deferral. Open the narrowest authoritative source that can answer the
current question; do not preload linked history, research, verification, logs,
artifacts, or broad source trees.

Files are not session ledgers. Update only the document whose durable content changed,
and use pointers instead of copied detail. Do not store routine activity, transient
observations, command history, or checkpoint summaries.

Inactive documents must identify their lifecycle and replacement when one exists.
Remove superseded inputs from normal routing, retain them only for a concrete
historical need, and use version-control history as the default archive. Ask before
deleting user files that lack reliable recovery.

Before removing behavior, APIs, formats, configuration, or dependencies, inspect
their consumers and persisted data and account for material migration effects.

## Verification And Completion

Follow the generic verification policy and use tests that materially increase
confidence in the changed behavior.

Before reporting completion, verify acceptance, inspect the diff, run relevant tests,
update only documentation whose trigger fired, report material results or gaps, and
stop at the authorized boundary. Implementation alone does not complete a milestone;
its approved acceptance and verification must pass or have a concrete blocker.

Run `prompts_transferable/self-evaluation-and-user-learning-loop.md` only when the
user or an active project prompt explicitly requests it.
