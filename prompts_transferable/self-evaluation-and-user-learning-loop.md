# Self-Evaluation And User Learning Loop

**Status:** ACTIVE
**Activation:** OPT-IN
**Purpose:** Improve user instructions, model routing, context quality, and work efficiency through concise feedback
**Applies to:** Projects that explicitly reference this prompt or sessions where the user explicitly requests it
**Last verified:** 2026-09-14
**Primary evidence:** `read_first.md` and the actual instruction, work, and verification being evaluated

Do not run this loop automatically. An active project prompt may request it at named
planning or milestone checkpoints; otherwise the user must explicitly invoke it.
Activation permits evaluation and feedback, not unrequested research,
implementation, model changes, delegation, or scope expansion.

Read `read_first.md` and
`prompts_transferable/generic_engineering_execution_protocol.md` before applying
this prompt. Apply project prompts afterward; record and honor only approved scoped
overrides.

## Evaluation Loop

Evaluate the smallest complete unit that can produce useful feedback: one material
instruction, planning round, milestone, failed attempt, or context handoff.

1. **User instruction:** Identify what made the instruction effective and only the
   ambiguities, conflicts, missing constraints, undefined terms, acceptance gaps, or
   unnecessary detail that materially affected execution. Propose a tighter example
   instruction when wording can improve. Do not grade the user or demand hidden
   reasoning.
2. **Exploration:** Suggest missing areas the user may want to include or explore.
   Separate required blockers from optional opportunities and explain what decision
   each would affect. Do not perform the exploration without authorization.
3. **Context health:** Assess whether the current context is sufficient, stale,
   duplicated, or overloaded. Recommend the minimum additional read, durable record,
   cleanup, or context reset needed. Keep `jumpstart.md` limited to fresh-context
   routing under `read_first.md`.
4. **Route suitability:** Apply the route-fit rules in
   `prompts_transferable/generic_engineering_execution_protocol.md`. State the
   current model and effort only when exposed. Recommend upgrade, downgrade, direct
   work, or a bounded subagent only when it materially changes quality, cost, or
   context use; ask before a user-controlled route change.
5. **Usage efficiency:** Evaluate duplicated reading/research, agent allocation,
   avoidable context transfer, tool choice, verification depth, and likely rework.
   Base criticism on observable actions and outcomes, not token-count guesses or
   hidden chain-of-thought.
6. **Learning update:** End with at most three reusable changes to the user's next
   instruction or the project's prompt/state documents. Ask whether durable prompt
   changes are wanted; never rewrite standing instructions merely because the loop
   ran.

When evaluating a prompt set, map each behavior to one authoritative document.
Flag contradictory rules, duplicated behavior, excessive minimum-read sets, and
project prompts that repeat generic policy instead of pointing to it. Check that
generic prompts are read first and that every project-level conflict has an
explicitly approved scoped override.

## Output Contract

Use only sections with actionable content:

- **Instruction Feedback:** precise strengths and improvements, with a revised
  example when useful.
- **Missing Or Optional Exploration:** blockers first, then clearly optional ideas.
- **Context And Routing:** context health plus model/effort/delegation suitability.
- **Efficiency:** concrete waste or a concise statement that routing was efficient.
- **Next Input:** up to three changes the user can include next time.

Keep the response brief and candid. Separate defects in the user's instruction from
defects in model execution. Do not manufacture criticism, repeat ordinary status
reporting, restate the full task, provide private chain-of-thought, or turn every
completion into a retrospective. If no material improvement is found, say so in one
sentence.
