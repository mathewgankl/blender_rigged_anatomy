---
name: pstack-how
description: "Explains how code, subsystems, ownership, and runtime flows work; use when answering architecture, walkthrough, placement, or onboarding questions."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "how"
---

# PStack how

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize foundational thinking, domain modeling, boundary discipline, and
minimizing reader load.

## Workflow

1. State a reasonable interpretation if the question is ambiguous. Ask only when
   different interpretations would materially change the answer.
2. Use direct read, search, symbol, and history-free inspection tools first. Start
   at entry points, then trace calls, state transitions, data shapes, and effects.
3. For a narrow question, inspect and explain in one pass. For a subsystem that
   genuinely spans independent areas, use at most two or three bounded read-only
   agents with distinct questions, then verify their claims against source files.
4. Identify ownership and boundaries: where input enters, where it is validated,
   where domain decisions live, and where output or side effects occur.
5. Cite concrete files and lines. Separate observed behavior from inference, and
   say what remains unknown rather than inventing a caller or contract.
6. Explain the mental model before details. Include only concepts needed to answer
   the question and surface consequential lifecycle, concurrency, or state traps.

## Output

Use applicable sections: Overview, Key concepts, Runtime flow, Where it lives, and
Gotchas. Keep the explanation architectural rather than annotating every line.
This workflow is explanatory and does not modify code unless separately requested.
