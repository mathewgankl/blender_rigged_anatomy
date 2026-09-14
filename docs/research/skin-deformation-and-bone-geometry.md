# Skin Deformation and Anatomical Bone Geometry

**Status:** ACTIVE EVIDENCE
**Scope:** Milestone 0, Round 1 weighting and future skin-binding seam
**Researched:** 2026-09-14
**Model:** `openai/gpt-5.6-terra`
**Effort:** `medium`

## Question

How should one skin mesh follow the animator armature and simplified anatomical
bone geometry, and can Blender 5.2 make skin reliably wrap around moving internal
bones without importing later muscle, fat, skin-binding, or physics work?

## Findings

Blender permits sequential mesh modifiers, but it does not provide a native coupled
solve that combines armature deformation with a skin shell wrapping around multiple
moving internal bone surfaces.

- An Armature modifier uses bone-name-matched vertex groups or bone envelopes.
  Vertex groups are the precise standard path. Preserve Volume changes armature
  interpolation but does not guarantee anatomical volume preservation.
- Automatic Weights is a supported armature-parent operation, but its bone-heat
  solve can fail on unsuitable geometry and is operator/context sensitive.
- Surface Deform transfers deformation from one target surface to the modified
  mesh after a bind. Sparse internal bone surfaces are not a matching enclosing
  skin target, and binding adds topology, transform, modifier-order, and
  regeneration lifecycle requirements.
- Mesh Deform requires a deliberate closed enclosing cage. Separate internal bones
  are not such a cage; binding can be expensive and large cage changes can artifact.
- Shrinkwrap moves skin vertices toward closest or projected target surfaces.
  Targeting internal bones would pull the outer skin inward, cause discontinuities
  between nearest bones, and risk collapse and intersections.
- Geometry Nodes proximity can measure bone-to-skin relationships but is not a
  contact, thickness, or wrapping solver.
- Cloth/collision is stateful physics and remains outside Round 1.

## Recommendation

Round 1 should use one runtime deformation owner for the skin:

`animator/deform armature -> skin mesh`

The same armature rigidly or conventionally drives the generated anatomical bone
meshes through their mapped drivers. Anatomical surfaces may provide read-only
containment, clearance, correspondence, and weight-quality diagnostics, but they do
not bind or deform the skin at runtime. The skin receives no Surface Deform, Mesh
Deform, Shrinkwrap, cloth, collision, or geometry-proximity runtime deformation from
anatomical meshes.

Use Blender Automatic Weights as the Round 1 usability path. Preserve editable
deform vertex groups and report a failed solve explicitly; do not silently replace
it with an unverified geometry-driven method. Regenerating anatomy must not modify
the skin modifier stack or retain stale geometry bindings.

Future skin wrapping should use an intermediate enclosing muscle/fat surface or
cage selected and tested in its approved round. It should not bind skin directly to
individual internal bones.

## Objective Checks

- The skin has one intended Armature modifier and no anatomical Surface Deform,
  Mesh Deform, Shrinkwrap, cloth, collision, or Geometry Nodes runtime deformer.
- Required deform bones have finite, non-negative skin vertex groups; tested skin
  vertices have a nonzero total deform influence unless explicitly excluded.
- Automatic-weight success is verified from resulting data; failure is deterministic
  and actionable.
- Rest and prescribed poses move skin and anatomy from the same armature and survive
  save/reload.
- Regenerating anatomical meshes changes neither skin weights nor its modifier
  stack; read-only diagnostics may be recomputed.
- Preserve Volume on/off causes no execution or geometric-validity failure, but
  Round 1 makes no soft-tissue realism claim.

## Sources

- [Blender 5.2 Armature Deform Parent](https://docs.blender.org/manual/en/5.2/animation/armatures/skinning/parenting.html)
- [Blender 5.2 Armature modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/armature.html)
- [Blender 5.2 Surface Deform modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/surface_deform.html)
- [Blender 5.2 Mesh Deform modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/mesh_deform.html)
- [Blender 5.2 Shrinkwrap modifier](https://docs.blender.org/manual/en/5.2/modeling/modifiers/deform/shrinkwrap.html)
- [Blender 5.2 Geometry Proximity node](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/geometry/sample/geometry_proximity.html)
- [Blender 5.2 source tag](https://projects.blender.org/blender/blender/src/tag/v5.2.0)
