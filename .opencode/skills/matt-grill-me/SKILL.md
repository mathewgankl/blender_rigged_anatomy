---
name: matt-grill-me
description: Use ONLY when explicitly requested to sharpen a plan or design through a relentless structured interview.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "grill-me"
---

# Grill Me

This is the explicit router for the interview workflow.

## Workflow

1. Load `matt-grilling`.
2. State the plan, design, decision, or idea being tested in one sentence.
3. Follow `matt-grilling` exactly: construct the design tree, ask one complete
   frontier per numbered round, recommend an answer for every question, and
   wait between rounds.
4. Look up repository and environment facts directly instead of asking the
   user to retrieve them.
5. Stop when the frontier is empty and the user confirms shared understanding.
6. Do not implement or document the result unless separately requested. If the
   user wants domain documentation during the interview, load
   `matt-grill-with-docs` instead.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools before considering an agent. If delegation is necessary, use
one focused agent for one bounded question; never use broad fan-out.
