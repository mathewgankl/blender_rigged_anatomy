# PStack principles

These principles guide decisions. They do not grant permission to use Git, write
files, expand scope, install dependencies, contact remotes, or take destructive
actions. Project and user instructions always take precedence.

## Laziness

Prefer deletion and the smallest change that solves the problem. Avoid speculative
layers, one-caller wrappers, duplicated decisions, and signals threaded through
many layers when a direct path exists.

## Foundational thinking

Choose core types and data structures before writing logic. Trace access patterns,
identify shared state, and establish only the scaffolding that benefits later work.
Keep each increment coherent and explicit.

## Model the domain

Encode repeated rules and valid states in one fitting structure, such as a state
machine, typed model, registry, reducer, or index. Do not add abstraction unless it
removes branches, duplicated rules, invalid states, or lifecycle risk.

## Boundary discipline

Validate and narrow untrusted input at system boundaries. Keep framework and
transport details at the edge, pass domain concepts inward, trust established
internal types, and keep business logic pure where practical.

## Minimize reader load

Reduce both indirection and hidden state. Collapse pass-through layers, keep state
in the narrowest scope, derive values instead of synchronizing copies, and make
each boundary hide enough complexity to justify itself.

## Idempotence

Make mutating operations converge on the same result after retries or partial
failure. Detect existing and stale state, reconcile before acting, and ask what
happens when an operation runs twice or stops at every intermediate point.

## Prove it works

Check the real artifact and actual execution path, not a proxy or self-report.
Build when useful, then exercise the behavior, inspect input-to-output flow, and
state clearly when direct proof is unavailable.

## Fix root causes

Reproduce before changing code. Trace the symptom through actual state and data,
instrument when uncertain, fix the earliest incorrect assumption, and search for
other instances of the same pattern instead of masking the observed failure.

## Sequence verifiable units

Split work into the smallest coherent units that end with a meaningful check.
Verify each unit before building on it, and order the sequence so a reviewer can
follow the evidence from baseline or failure to the corrected result.
