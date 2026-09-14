---
name: pstack-unslop
description: "Edits prose to remove vague, repetitive, or machine-like writing while preserving intent; use when asked to tighten, humanize, or unslop text."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/main/pstack"
  revision: "889ec4b68fa5aab0e867dad71ec3fdf386ae48f3"
  upstream-skill: "unslop"
---

# PStack unslop

Project and user policies override this skill. Invoking it does not authorize
dependency installs, Git or remote operations, scope expansion, destructive
actions, or unrelated writes.

Apply the relevant guidance in `../../PSTACK_PRINCIPLES.md`, which is the
`../PSTACK_PRINCIPLES.md` reference from the bundle's `skills/` directory.
Prioritize reader load, domain precision, minimal edits, and verifiable claims.

## Workflow

1. Determine the audience, purpose, intended tone, and applicable project style.
2. Preserve meaning, tone, technical precision, factual qualifications, and useful
   emphasis. Do not flatten an author's voice or turn nuanced claims into absolutes.
3. Replace vague attribution with a named source or retain uncertainty honestly.
   Replace generic claims with concrete facts only when evidence exists.
4. Cut filler, canned chatbot framing, forced transitions, repeated conclusions,
   empty praise, inflated vocabulary, and decorative formatting that adds no signal.
5. Prefer active and concrete phrasing when it is clearer, but retain passive voice,
   specialist terms, long sentences, headings, punctuation, or rhetorical devices
   when they serve the audience or project style.
6. Remove accidental repetition and synonym cycling. Keep one stable name for each
   technical concept, and use exact symbols, flags, paths, and measured values.
7. Split sentences that require rereading, but preserve deliberate cadence. Avoid
   categorical style bans; judge every edit by clarity, fidelity, and context.
8. Compare the revision with the source and restore any lost constraint, caveat,
   relationship, or implication.

Use direct editing and inspection tools first. An agent is rarely justified; for a
large document set, use at most one bounded read-only consistency pass.

## Output

Return the revised text in the requested format. When reviewing rather than editing,
lead with specific problems and offer minimal revisions that preserve the author's
intent.
