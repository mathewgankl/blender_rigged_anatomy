---
name: matt-grill-with-docs
description: Use ONLY when explicitly requested to stress-test a plan or design through an interview while recording domain terms and durable decisions.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "grill-with-docs"
---

# Grill With Docs

Combine `matt-grilling` with `matt-domain-modeling`. Load both skills before
starting, then follow their workflows together rather than inventing a third
interview process.

## Workflow

1. Read `jumpstart.md` and relevant files under `docs/decisions/` if present.
2. Use the design-tree rounds from `matt-grilling` to expose every unsettled
   decision and wait for the user's answers between rounds.
3. Apply `matt-domain-modeling` during each round: challenge ambiguous terms,
   test concrete edge cases, and compare claims with the code.
4. Update `jumpstart.md` when domain vocabulary becomes settled.
5. Offer a decision record under `docs/decisions/` only for a durable,
   surprising, hard-to-reverse trade-off.
6. Finish only when the interview frontier is empty and the user confirms the
   shared understanding. Do not implement the resulting plan automatically.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools before considering an agent. If delegation is necessary, use
one focused agent for one bounded question; never use broad fan-out.
