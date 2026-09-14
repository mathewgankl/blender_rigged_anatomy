---
name: matt-grilling
description: Use ONLY when explicitly requested to interview the user relentlessly and stress-test a plan, decision, or idea.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills"
  revision: "3cca18b368ae95cdbdebbff572ccafa662551015"
  upstream-skill: "grilling"
---

# Grilling

Interview until both sides share a precise understanding. Model the topic as a
design tree: each decision branches into decisions that depend on it.

## Rounds

1. Identify the frontier: all unsettled decisions whose prerequisites are
   already settled.
2. Investigate available facts directly with repository and environment tools.
   Do not ask the user for facts that can be looked up.
3. Ask the entire frontier in one numbered round. For each question, provide a
   concise recommended answer and its trade-off.
4. Wait for the user's answers. Do not ask a question whose answer depends on
   another open question in the same round.
5. Recompute the tree from those answers and repeat.

Use this shape:

```text
Q1 - <title>: <question and choices>
Recommendation: <answer and reason>
```

The interview is complete only when the frontier is empty, no assumption is
silent, and the user confirms shared understanding. Do not act on the result
without a separate request.

## Authority

Project and user policy overrides this skill. Invocation does not authorize
dependency installation, Git or remote operations, scope expansion,
destructive actions, or unrelated writes.

Use direct tools first. If one fact cannot be obtained directly, use at most
one focused agent for that bounded lookup; never use broad fan-out.
