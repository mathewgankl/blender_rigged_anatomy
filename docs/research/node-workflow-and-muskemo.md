# Node-Oriented Workflow and MuSkeMo

**Status:** ACTIVE EVIDENCE
**Scope:** Milestone 0, Round 1 fitting and rig generation only
**Researched:** 2026-09-13

This report was produced by a bounded research subagent. On 2026-09-13, the user
accepted it as Round 1 planning-interview evidence without a model-routing rerun or
additional primary-agent verification. Future research still follows the configured
model and effort requirements.

## Recommendation

Use a deterministic Python pipeline to validate landmarks, fit the skeleton,
build the armature, and configure constraints. Use one generated Geometry Nodes
group only to visualize fitted bone envelopes and the biceps/hamstring relation
paths. Do not create a custom node editor in Round 1, and do not make node output
authoritative rig state.

This boundary keeps the numerical and anatomical rules testable outside Blender
while using Blender's native data model where edit bones, pose bones, and
constraints must be materialized. It also leaves a narrow node-oriented seam:
the visualization group consumes points, radii, paths, and role attributes from
the fitted plan without owning landmark inference or armature mutation.

## Blender Workflow

The pipeline is a sequence of data transformations:

1. Read the target mesh and named landmark objects through a Blender adapter.
2. Validate topology, transforms, required roles, sidedness, and finite values.
3. Transform evaluated mesh and landmark positions into character-height-normalized
   coordinates.
4. Infer correction points, anatomical frames, joint axes, poles, envelope
   profiles, and relation paths into a complete rig plan.
5. Validate the plan without changing the scene.
6. Materialize a staged armature, controls, constraints, metadata, and optional
   visualization; replace prior tool-owned output only after staged validation.
7. Validate the created Blender data through the same headless entry point used
   by the UI operator.

The domain stages must not call `bpy`. Blender panels and operators collect input,
invoke the same application command, and report structured validation errors.
This avoids embedding fitting rules in UI callbacks or requiring a 3D View
context for headless tests. Blender RNA data access is preferred over
context-sensitive `bpy.ops` where the API permits it.

Geometry Nodes is appropriate for derived geometry, not Round 1 control flow.
Blender 5.2 exposes `NodeTree` data blocks, a `NodesModifier`, group interface
sockets, and geometry operations suited to curves and radial previews. The
installed Blender 5.2.1 type registry exposes one bone-specific geometry node,
`GeometryNodeBoneInfo`; its sockets read an armature and bone name and return
pose/rest matrices and rest length. It does not create bones or constraints.
`EditBone`, `PoseBone`, and `KinematicConstraint` remain the direct APIs for the
authoritative rig.

The visualization node group should be generated from code with a stable name,
schema version, and explicit interface. Deleting or disabling it must not change
the armature, IK result, validation result, or export mappings. Round 1 does not
need a custom `NodeTree`: that would add registration, serialization, UI, and
migration obligations before users have more than one useful composable graph.

## MuSkeMo Viability

**Facts.** At revision `5e47be6b944e2bd491b5b5e08f3017722f894405`,
MuSkeMo identifies itself as add-on version `0.9.84`. Its README reports testing
with Blender 4.1 through 4.5 and 5.0, not 5.2. Its add-on registers many 3D View
panels and operators, stores settings on `Scene.muskemo`, uses NumPy, and creates
or loads Geometry Nodes groups for muscle visualization.

MuSkeMo landmarks are objects placed at the 3D cursor and parented to rigid body
objects. Its frame panel constructs an orthonormal frame from landmark vectors
and cross products. Its reflection operators apply explicit reflection matrices
and side-name substitutions. Assigning a local frame recomputes dependent joint,
contact, inertia, and path-point values in that frame. The joint tools can fit
geometric primitives, and the mesh tools include point-to-plane ICP.

The inspected README and source do not provide a landmark-to-humanoid-armature
autofit operation. MuSkeMo models rigid bodies, joints, frames, contacts, and
muscle paths for biomechanical interchange; it does not generate this project's
Blender deform/control/mechanism bone hierarchy. Its ICP aligns one mesh to
another using random subsampling and is neither skeleton inference nor
deterministic under its default implementation.

**Reusable concepts.** Independently implement only the general ideas that match
Round 1: named landmarks, landmark-defined orthonormal frames, explicit symmetry,
primitive or clearance fitting, and recomputation of derived values from source
inputs. Do not copy MuSkeMo's object schema, panels, operators, algorithms, node
assets, or source structure. Avoid a NumPy runtime dependency; Round 1 can use
small vector operations plus Blender's `mathutils` and `BVHTree` at the adapter
boundary.

**License.** The pinned repository tree has no root `LICENSE`, and GitHub's
repository license endpoint returned `404`. Therefore there is no verified
repository-wide permission to copy or adapt the add-on. Some files state separate
terms: `scripts/icp_point_to_plane.py` says CC-BY-NC, while
`scripts/fit_cylinder_eberly.py` references CC BY 4.0 and an upstream pseudocode
source. The safe Round 1 decision is clean implementation from requirements and
general mathematical principles, with MuSkeMo cited only as design evidence.
Any future source reuse requires a file-level provenance and license review.
This is an engineering recommendation, not legal advice.

## Objective Checks

1. UI and headless execution call the same application command and produce the
   same rig-plan digest for identical inputs.
2. Identical normalized inputs produce identical names, coordinates, hierarchy,
   constraints, mappings, and visualization attributes.
3. No domain module imports `bpy`, requires a UI context, or depends on NumPy,
   MuSkeMo, Rigify, MuJoCo, Autodesk, or a VRM add-on.
4. Disabling or deleting the generated Geometry Nodes visualization leaves all
   armature and IK checks unchanged.
5. A failed staged validation leaves prior tool-owned output and all user-owned
   scene objects unchanged.
6. Pure fitting tests pass under system Python 3.14; Blender integration tests
   pass under the Python version embedded in Blender 5.2.

## Sources

- [Blender 5.2 `NodeTree`](https://docs.blender.org/api/5.2/bpy.types.NodeTree.html),
  [`GeometryNodeTree`](https://docs.blender.org/api/5.2/bpy.types.GeometryNodeTree.html),
  and [`NodesModifier`](https://docs.blender.org/api/5.2/bpy.types.NodesModifier.html).
- [Blender 5.2 `EditBone`](https://docs.blender.org/api/5.2/bpy.types.EditBone.html),
  [`PoseBone`](https://docs.blender.org/api/5.2/bpy.types.PoseBone.html),
  [`KinematicConstraint`](https://docs.blender.org/api/5.2/bpy.types.KinematicConstraint.html),
  and [`BVHTree`](https://docs.blender.org/api/5.2/mathutils.bvhtree.html).
- [MuSkeMo README](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/README.md)
  and [add-on registration](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/__init__.py).
- MuSkeMo [landmark panel](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/landmark_marker_panel.py),
  [frame panel](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/frame_panel.py),
  [reflection operators](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/reflection_panel.py),
  and [simple muscle node generator](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/simple_muscle_viz_node.py).
- MuSkeMo [`icp_point_to_plane.py`](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/icp_point_to_plane.py)
  and [`fit_cylinder_eberly.py`](https://github.com/PashavanBijlert/MuSkeMo/blob/5e47be6b944e2bd491b5b5e08f3017722f894405/scripts/fit_cylinder_eberly.py).
- [Pinned MuSkeMo repository tree](https://github.com/PashavanBijlert/MuSkeMo/tree/5e47be6b944e2bd491b5b5e08f3017722f894405).
