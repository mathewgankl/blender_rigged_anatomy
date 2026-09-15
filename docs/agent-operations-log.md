# Agent Operations Log

**Status:** REFERENCE - NON-AUTHORITATIVE
**Purpose:** Optional reference for administrative and debugging incidents with reusable diagnostic value
**Updated:** 2026-09-15

Do not read this file during normal project continuation or use it to recover project
status. Consult a named entry only when diagnosing a related setup, routing, quota,
or invocation problem. Project requirements, decisions, research findings, and
verification evidence belong in their dedicated records. Do not add routine session
activity, command history, or checkpoint summaries.

## 2026-09-13: Invalid Research CLI Invocation

- `opencode run --agent research` rejected the subagent as non-primary, fell back
  to the default `build` primary agent on `gpt-5.6-sol`, and reached a usage limit.
- The attempt produced no accepted Mantis or collision-density evidence.
- Diagnosis confirmed that `opencode.json` defined a read-only `research` subagent
  using `openai/gpt-5.6-terra` with `reasoningEffort: medium`, but the CLI command
  accepts primary agents rather than Task subagents.
- After configuration validation and restart, the Task tool correctly invoked the
  configured subagent for both bounded tracks.
- Outcome: the failed route was abandoned; current invocation rules live in the
  generic execution protocol.

## 2026-09-13: Early Research Routing Waiver

- The first rigging-standards and node-workflow reports predated the finalized
  subagent-routing checks and included direct document writes.
- The user explicitly accepted those two reports for Round 1 without rerun or
  additional routing verification.
- Outcome: the waiver applies only to those reports; current routing requirements
  live in the active prompt set.
