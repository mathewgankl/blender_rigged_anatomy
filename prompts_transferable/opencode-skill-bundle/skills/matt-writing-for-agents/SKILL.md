---
name: matt-writing-for-agents
description: Guides concise OpenCode agent documentation; use when creating or editing SKILL.md, AGENTS.md, instructions, or documents reached by agent pointers.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "writing-for-agents"
---

# Writing For Agents

Write a process that produces predictable behavior, not prose that demands a
fixed output. Treat each pointer and document as part of an information ladder.

## OpenCode Skill Semantics

An OpenCode skill lives at `<skill-name>/SKILL.md`. Its YAML frontmatter needs
`name` matching the folder and a third-person `description` that says both what
the skill does and when it should load. Optional supported fields include
`license`, `compatibility`, and a string-to-string `metadata` map. The Markdown
body is loaded as instructions when OpenCode invokes the skill. Use an explicit
phrase such as `Use ONLY when explicitly requested` to gate opt-in workflows.
Do not add Claude- or Cursor-specific invocation fields.

## Writing Method

1. Write a context pointer that front-loads concrete triggers and names each
   genuinely distinct branch once.
2. Put ordered actions in the main file. End each step with a checkable,
   demanding completion criterion.
3. Keep definitions, rules, and caveats together. Move branch-only reference
   behind a precise pointer only when progressive disclosure improves focus.
4. Use stable leading words for recurring concepts so one compact term carries
   the behavior consistently.
5. Prune duplicated meaning, environment facts that tools can discover, stale
   sediment, and instructions that do not change model behavior.
6. Split by sequence only when visible later steps cause premature completion;
   split by invocation only when trigger conditions are genuinely different.
7. Re-read the result as an agent: every trigger, branch, authority boundary,
   step, and completion condition must be unambiguous.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.
