# Project Start Skill Installation

**Status:** ACTIVE
**Purpose:** Install curated Matt Pocock and PStack skills for OpenCode
**Applies to:** Explicit skill-setup sessions
**Last verified:** 2026-09-04
**Supersedes:** NONE
**Superseded by:** NONE
**Primary evidence:** `read_first.md`

> **Scope:** Skill setup only. Do not begin project implementation.

1. Read project instructions first; they override every skill.
2. Confirm the project root, version-control state, existing skills, and OpenCode
   config. Ask before Git initialization, downloading, or installation.
3. Fetch exact pinned revisions from
   <https://github.com/mattpocock/skills> and
   <https://github.com/cursor/plugins/tree/main/pstack>.
4. Install project-locally in `.opencode/skills/`, preserving required reference
   files, MIT notices, source URLs, and revisions. Prefix names with `matt-` or
   `pstack-` and update internal references.
5. Install these adapted Matt skills: `grill-with-docs`, `grilling`, `grill-me`,
   `domain-modeling`, `codebase-design`, `diagnosing-bugs`, `code-review`,
   `prototype`, and `writing-for-agents`.
6. Install these adapted PStack skills: `how`, `blast-radius`, `tdd`, `interrogate`,
   `technical-writing`, and `unslop`; also preserve the laziness,
   foundational-thinking, domain-modeling, boundary-discipline, reader-load,
   idempotence, proof, root-cause, and verifiable-unit principles.
7. Adapt skills so project policy controls scope, documentation, tools, agents,
   permissions, and completion; use established documentation paths.
8. Require explicit invocation for interviews, prototypes, and broad or
   adversarial reviews; OpenCode ignores `disable-model-invocation`.
9. Without explicit authorization, skills must not install software, broaden
   scope, create remote state, commit, push, merge, publish, or implement. Exclude
   setup skills, top-level routers, issue trackers, autonomous orchestration,
   multi-agent swarms, and shipping workflows.
10. Validate frontmatter, unique names, relative links, permissions, attribution,
    and absence of unapproved scripts, plugins, hooks, MCPs, or dependencies.
11. Restart OpenCode, verify discovery, and report files, revisions, adaptations,
    checks, and risks. Stop before project work.
