---
name: matt-domain-modeling
description: Builds and sharpens a project's domain vocabulary and durable decisions; use when terms, relationships, or decision records are being resolved.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "domain-modeling"
---

# Domain Modeling

Treat `jumpstart.md` as the project's living domain glossary and
`docs/decisions/` as the home for durable decision records. Create or update
them lazily, only when there is settled information to record.

## Workflow

1. Read relevant vocabulary in `jumpstart.md`, decision records, and code.
2. Challenge conflicts immediately. Ask whether the established term or the
   new meaning is authoritative.
3. Replace vague or overloaded language with a precise canonical term.
4. Stress-test relationships with concrete scenarios, especially edge cases
   that expose unclear concept boundaries.
5. Compare claims with implementation. Surface contradictions for the user to
   resolve rather than silently choosing one source.
6. Record a resolved term in `jumpstart.md` as soon as it crystallizes. Keep
   glossary entries about domain meaning, not implementation or plans.

Create a record in `docs/decisions/` only when the decision is hard to reverse,
surprising without context, and the result of a genuine trade-off. Record the
context, considered options, decision, consequences, and status. Skip routine
or easily reversible choices.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools before considering an agent. If delegation is necessary, use
one focused agent for one bounded question; never use broad fan-out.
