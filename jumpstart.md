# Project Jumpstart

**Status:** ACTIVE
**Phase:** Milestone 0 - discovery and planning
**Updated:** 2026-09-13

## Read

1. `read_first.md`
2. `proj_003 blender rigging physics sim tool.txt`
3. `prompts/rigged_anamtomy_execution_prompt.md`
4. The approved Round 1 PRD when it exists

Other prompts apply only to their stated setup or continuation scope.

## Project Instructions

- Target Blender 5.2 LTS and Python 3.14 on Windows; use GitHub for CI/CD.
- Complete Round 1 before muscle deformation or later-round physics work.
- Round 1 covers a human-only anatomical IK rig, major visible muscle-group bone
  relationships, scale-safe semi-automatic skeleton fitting, and non-realistic
  humanoid proportions.
- Use targeted written sources. Avoid videos unless a transcript or selected
  frames uniquely answer a blocking question.
- Research the top three compatible rigging standards, node-oriented workflows,
  and the viability and licensing of MuJoCo Menagerie and MuSkeMo.
- Use `roxanne_5.blend` and the supplied reference image for acceptance testing.
- Prefer the smallest testable vertical slice; stop for approval before production
  implementation.

## Current State

- Blender 5.2.1 LTS and Python 3.14.3 verified.
- `roxanne_5.blend` opens headlessly.
- Expected object `body` is absent; mesh objects are `Body_lowpoly` and `Cube`.
- Git tracks `origin/main` at
  `https://github.com/mathewgankl/blender_rigged_anatomy.git`.
- No source, tests, approved PRD, build, or CI exists.
- No project decisions are approved yet.

## Next Action

Resolve whether `Body_lowpoly` is the intended test body, then define and obtain
approval for the Round 1 architecture, milestones, exclusions, and acceptance
tests.
