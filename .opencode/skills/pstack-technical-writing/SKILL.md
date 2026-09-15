---
name: pstack-technical-writing
description: "Writes and reviews clear technical prose for docs, RFCs, READMEs, change descriptions, and engineering messages; use when technical writing quality or structure matters."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "technical-writing"
---

# PStack technical writing

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

Project documentation, terminology, templates, and style guides take precedence.
Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize reader load, domain language, boundaries, and verifiable claims.

## Workflow

1. Identify the audience, task, and project conventions. Inspect nearby documents
   and source directly before choosing structure or terminology.
2. Choose one primary mode: a tutorial teaches by guided results; a how-to solves a
   task; reference supports lookup; explanation develops understanding and reasons.
   Split and link material when modes conflict.
3. Use the project's exact symbols, paths, commands, and domain terms. Never invent
   a synonym for a named concept or claim a count that was not checked.
4. Put conditions before instructions, common cases before exceptions, and one
   action per procedural step. Use commands for instructions and present tense for
   facts. Name the actor when that improves clarity.
5. Prefer plain, precise words. Cut filler, keep articles and verbs needed to avoid
   ambiguity, place modifiers next to what they modify, and make pronouns explicit.
6. Use headings that state the point, numbered lists for sequences, and bullets for
   non-sequential sets. Keep code and UI notation consistent with project style.
7. Read the result as a tired engineer. Check that each claim is sourced, each link
   says where it leads, terminology is stable, and sentence rhythm remains natural.

Use a bounded read-only consistency review only when it materially improves a large
document set.

## Output

Deliver the requested prose or findings in project style. Preserve established
voice unless the user explicitly asks to change it.
