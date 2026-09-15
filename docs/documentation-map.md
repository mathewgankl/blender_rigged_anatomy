# Documentation Map

**Status:** ACTIVE
**Purpose:** Prevent authority overlap and unnecessary context loading

Read this map when choosing which document to open or update.

| File | Owns | Access |
|---|---|---|
| `read_first.md` | Repository policy and authority rules | Start of session |
| `jumpstart.md` | Fresh-context routes only | Fresh continuation |
| `prompts_transferable/` | Reusable workflows | Only when applicable to current work |
| `prompts_project/` | Project-specific execution constraints | Relevant sections for current work |
| `docs/prds/` | Approved scope, requirements, order, and acceptance | Relevant sections before execution |
| `docs/decisions/` | Approved durable choices and rationale | Only when the current question touches one |
| `docs/project-state.md` | Current status, evidence pointers, risks, next action, and a small downstream queue | Continuation or material checkpoint |
| `docs/verification/` | Reproducible evidence | When validating or claiming results |
| `docs/research/` | Sourced findings, not execution authority | Only for a named open question |
| `docs/agent-operations-log.md` | Non-authoritative incident history | Only for a related diagnosis or audit |
| Superseded files | Provenance only | Only for a named historical need |

For the same subject, use this order: approved PRD or amendment, approved project
instruction, approved decision, generic policy, current project state, verification,
research, then operational history. Link to the owner instead of copying its content.

## Context Fit

If planned work is poorly aligned with the active objective or available context,
inform the user before starting and recommend deferring it to a fresh context. With
agreement, place a concise item in the PRD's later scope or the project-state
downstream queue; do not add it to `jumpstart.md` or active work until promoted.
