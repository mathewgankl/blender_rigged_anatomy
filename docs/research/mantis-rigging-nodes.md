# Mantis Rigging Nodes

**Status:** ACTIVE EVIDENCE
**Scope:** Milestone 0, Round 1 node-ownership decision
**Researched:** 2026-09-14
**Model:** `openai/gpt-5.6-terra`
**Effort:** `medium`

## Question

Should Round 1 adopt Mantis as its rigging framework, integrate it optionally, use
its concepts only, or retain a project-owned Python rig plan with generated standard
Geometry Nodes for anatomical bone geometry?

## Findings

Mantis is Joseph Brandenburg/Nodespaghetti's active Blender rigging-nodes toolkit.
This report inspects revision `f6e69242cabaac7260a5693f7c28f0f833eb3db5`,
committed 2026-08-16. The extension manifest identifies version `0.13.4`, Blender
`4.2.0` minimum, Windows x64/macOS ARM/Linux x64 support, maintainer
`Nodespaghetti <josephbburg@protonmail.com>`, and bundled
`grandalf-0.8-py3-none-any.whl`. It sets no maximum Blender version.

Mantis uses custom `MantisTree` and `SchemaTree` graphs interpreted by Python into
Blender data. It is not a Geometry Nodes armature writer. Its Python implementation
can create armatures and edit bones, set parentage and transforms, configure deform,
IK, B-Bone, driver, and constraint properties, and provide many constraint node
types. Its Geometry Nodes support is auxiliary object-instancing functionality.

The project is capable and active, including recent Blender 5.2 fixes, but Round 1
adoption would make the Mantis graph and execution lifecycle authoritative. Its
implementation uses Blender context, operators, selection/active-object state,
depsgraph/load/undo handlers, and destructive reset paths. The inspected tree has no
published deterministic headless test suite, stable tagged data-format
specification, or benchmark proving a performance advantage for this workload.
Mantis also persists custom node trees and implementation-specific JSON and carries
version-migration behavior, creating a compatibility obligation beyond this
project's core rigging problem.

The manifest and `LICENSE.txt` license Mantis under GPL-3.0-or-later. Copying,
modifying, or tightly incorporating covered code into a distributed combined work
would create GPL source and licensing obligations. This is an engineering risk
summary, not legal advice.

## Recommendation

Do not adopt Mantis as a Round 1 framework or optional runtime dependency. Keep the
project-owned boundary:

1. Python validates landmarks and produces the authoritative rig plan.
2. Python materializes armatures, bones, controls, IK, and constraints.
3. Python generates a standard, versioned Geometry Nodes group that derives
   anatomical bone meshes from rig-plan data.
4. Deleting or disabling the generated Geometry Nodes modifier cannot change rig
   semantics.

Independently reuse only general ideas such as explicit transform graphs,
relationship ordering, repeated schemas, and named inputs. Do not copy Mantis code,
node trees, JSON formats, or bundled dependencies.

## Adoption Risks

- Custom Mantis graphs would become a second public and persisted rig definition.
- Context-sensitive and destructive generation conflicts with transactional,
  user-data-preserving regeneration.
- Headless determinism and Blender 5.2.1 behavior are not established by an
  upstream suite.
- Pinning Mantis would require install, migration, graph-format, and compatibility
  tests.
- GPL-3.0-or-later obligations would become relevant to copied or combined work.
- No measured performance evidence supports adoption for this project's workload.

## Objective Checks

- Identical input produces the same rig-plan digest, armature, constraints, node
  interface, and anatomical geometry attributes.
- Removing generated node visualization changes no bone, IK, mapping, or digest.
- Headless Blender 5.2.1 generation needs no viewport context and confines any
  required edit-mode operator transition to one adapter.
- Shipped source imports no Mantis or `grandalf` module and copies no Mantis code or
  node assets.

## Sources

- [Official project site](https://nodes.tools)
- [Official GitLab repository](https://gitlab.com/josephbburg/mantis)
- [Pinned revision](https://gitlab.com/josephbburg/mantis/-/commit/f6e69242cabaac7260a5693f7c28f0f833eb3db5)
- [Extension manifest](https://gitlab.com/josephbburg/mantis/-/blob/f6e69242cabaac7260a5693f7c28f0f833eb3db5/blender_manifest.toml)
- [GPL-3.0 license](https://gitlab.com/josephbburg/mantis/-/blob/f6e69242cabaac7260a5693f7c28f0f833eb3db5/LICENSE.txt)
- [Registration and lifecycle](https://gitlab.com/josephbburg/mantis/-/blob/f6e69242cabaac7260a5693f7c28f0f833eb3db5/__init__.py)
- [Armature and bone nodes](https://gitlab.com/josephbburg/mantis/-/blob/f6e69242cabaac7260a5693f7c28f0f833eb3db5/xForm_nodes.py)
- [Blender 5.2 compatibility fix](https://gitlab.com/josephbburg/mantis/-/merge_requests/7)
