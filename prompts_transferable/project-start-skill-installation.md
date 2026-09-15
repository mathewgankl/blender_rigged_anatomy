# Reusable Skill Installation

**Status:** ACTIVE
**Purpose:** Install the maintained OpenCode skill bundle
**Applies to:** Explicit skill-setup sessions
**Last verified:** 2026-09-15
**Primary evidence:** `read_first.md`

Skill setup does not authorize project implementation.

## Method

1. Inspect project policy and existing `.opencode/skills/`; ask before the first
   download or installation.
2. Use `prompts_transferable/opencode-skill-bundle/`. Its `skills-lock.json` is the
   source inventory and pins revisions, hashes, licenses, and destinations.
3. Run the bundle installer for the project root. It must validate its lock, preserve
   notices, reject unsafe paths or local overwrites, and remain idempotent.
4. If the installation method is no longer valid, verify the current primary source
   before updating the canonical bundle and lock. Do not add compatibility behavior
   without a real consumer.
5. Restart OpenCode after installation and stop before project work.

Install only skills relevant to the project. Their descriptions define activation;
project and user policy still control scope, permissions, external changes, and
publishing. When `matt-grill-with-docs` is selected, planning follows
`prompts_transferable/planning-interview-and-prd-gate.md`.
