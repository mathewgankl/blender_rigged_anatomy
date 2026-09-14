# Reusable Skill Installation

**Status:** ACTIVE
**Purpose:** Install a maintained OpenCode skill bundle with minimal per-project work
**Applies to:** Explicit skill-setup sessions
**Last verified:** 2026-09-14
**Primary evidence:** `read_first.md`

> Skill setup only. Do not begin project implementation.

Read `read_first.md` and
`prompts_transferable/generic_engineering_execution_protocol.md` before this setup
prompt. Read project prompts afterward and apply only approved scoped overrides.

## Method

1. Read project policy and inspect existing `.opencode/skills/`. Ask before the
   first download or installation.
2. Use the adapted bundle in
   `prompts_transferable/opencode-skill-bundle/`. Its `skills-lock.json` pins
   sources, revisions, hashes, licenses, and paths.
3. Run `install.ps1 -ProjectRoot <path>` from the bundle directory. Do not
   re-research, re-adapt, or fetch upstream when the locked bundle validates.
4. The installer must copy only selected skill directories, preserve references
   and notices, reject hash or path mismatches, avoid overwriting local changes,
   and produce the same files on repeated runs.
5. Validate folder/name agreement, frontmatter, descriptions, relative links,
   attribution, and absence of scripts, plugins, hooks, MCPs, dependencies, or
   permissions not approved by project policy.
6. If installation fails, check the primary source for the current supported
   method. Update the canonical bundle, lock, installer, and this prompt only when
   the method changed. Remove a deprecated skill from the bundle and list; do not
   add a compatibility shim without a real consumer.
7. Record the bundle revision and validation result, then restart OpenCode. Stop
   before project work.

## Recommended Skills

Treat this as a recommendation, not a mandatory install set. Select only skills
that serve the project.

**Matt Pocock:** `grill-with-docs`, `grilling`, `grill-me`, `domain-modeling`,
`codebase-design`, `diagnosing-bugs`, `code-review`, `prototype`,
`writing-for-agents`.

**PStack:** `how`, `blast-radius`, `tdd`, `interrogate`, `technical-writing`,
`unslop`.

Preserve applicable PStack principles for laziness, foundational thinking, domain
modeling, boundary discipline, reader load, idempotence, proof, root cause, and
verifiable units without installing redundant skills.

All adapted names use `matt-` or `pstack-`. Interviews, prototypes, and broad or
adversarial reviews require explicit invocation. Skills must defer to project
scope and must not install software, create remote state, commit, push, merge,
publish, or broaden work without explicit authorization.

When `matt-grill-with-docs` is selected, project planning follows
`prompts_transferable/planning-interview-and-prd-gate.md`; installation alone does
not authorize an interview or PRD drafting.
