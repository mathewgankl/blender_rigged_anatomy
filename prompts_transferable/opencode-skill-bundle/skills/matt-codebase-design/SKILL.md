---
name: matt-codebase-design
description: Provides deep-module vocabulary and design checks; use when shaping interfaces, seams, adapters, testability, or module depth.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "codebase-design"
---

# Codebase Design

Design deep modules: substantial behavior behind a small interface at a clean,
testable seam. Optimize leverage for callers and locality for maintainers.

## Vocabulary

- **Module**: anything with an interface and implementation.
- **Interface**: everything callers must know, including invariants, errors,
  ordering, configuration, and performance constraints.
- **Implementation**: code hidden behind the interface.
- **Depth**: behavior available per unit of interface a caller must learn.
- **Seam**: a place where behavior can change without editing the caller.
- **Adapter**: a concrete implementation occupying a seam.
- **Leverage**: capability gained by callers from module depth.
- **Locality**: change, knowledge, bugs, and verification concentrated within
  the module.

## Design Checks

Reduce methods and parameters while hiding more complexity. Accept
dependencies rather than constructing them, return results where practical,
and test behavior through the same interface callers use.

Apply the deletion test: if deleting the module spreads its complexity across
callers, it is earning its place; if complexity disappears, it is likely a
pass-through. Distinguish internal seams from the external seam. Treat one
adapter as hypothetical and introduce a public seam when variation is real.
Explore materially different interface shapes before committing when trade-offs
are significant; do this directly and sequentially, not through agent fan-out.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools before considering an agent. If delegation is necessary, use
one focused agent for one bounded question; never use broad fan-out.
