# Role Registry Milestone Order

**Status:** APPROVED
**Date:** 2026-09-14
**Scope:** Round 1 Milestones 2 and 3

## Context

Milestone 2 requires complete anatomy and relationship catalogs with canonical role
references and driver mappings. The prior milestone summary deferred the full role
registry to Milestone 3, creating a hidden dependency and either a temporary role
list or later migration.

## Decision

Milestone 2 establishes the single data-only canonical role registry and mapping
manifests before catalog and asset generation. Milestone 3 consumes that registry to
materialize deform, mechanism, and control armatures and behavior.

## Consequences

- Catalog and asset validation use stable role IDs from their first implementation.
- Milestone 3 does not introduce a second registry or migrate Milestone 2 data.
- Rig behavior remains Milestone 3 scope; moving its data dependency does not
  authorize animator or mechanism implementation during Milestone 2.
