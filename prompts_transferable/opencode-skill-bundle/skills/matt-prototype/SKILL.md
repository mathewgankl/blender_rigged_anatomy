---
name: matt-prototype
description: Use ONLY when explicitly requested to build throwaway evidence that answers a specific logic, state-model, or UI design question.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "prototype"
---

# Prototype

A prototype is throwaway code that answers one explicit question. Clarify the
question first and choose the branch that produces evidence for it.

## Branches

- **Logic or state model:** make the smallest runnable harness that exercises
  difficult transitions and displays complete relevant state after actions.
- **UI:** make several materially different variants at one project-native
  route or entry point, with a simple in-page or URL-based variant switch.

## Rules

1. Place the artifact near the target code, follow existing conventions, and
   mark its path and UI clearly as a prototype.
2. Make it runnable through the existing toolchain with one obvious command,
   or as a self-contained HTML file when that answers the question.
3. Keep state in memory unless persistence is the question; then use explicitly
   disposable local storage or data.
4. Skip production abstractions, comprehensive tests, and polish. Add only the
   error handling needed to obtain trustworthy evidence.
5. Run the prototype, capture observations, and state the answer, limits, and
   unresolved questions.
6. Stop after producing evidence. Leave integration and cleanup choices to the
   user under a separate request.

Never auto-commit, create or switch branches, publish, integrate into production
code, or delete the prototype.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.
