# Collision-Aware Anatomical Mesh Density

**Status:** ACTIVE EVIDENCE
**Scope:** Milestone 0, Round 1 geometry contract only
**Researched:** 2026-09-14
**Model:** `openai/gpt-5.6-terra`
**Effort:** `medium`

## Question

Does Blender 5.2 impose a defensible polygon-size upper bound for generated
anatomical bone meshes intended as future rigid collision and attachment geometry?

## Findings

Blender 5.2 defines no universal anatomy-specific maximum edge length or
triangles-per-joint rule. Absolute edge length alone cannot guarantee reliable
collision. Relevant cloth collision behavior depends on evaluated triangles,
vertex-to-face and edge-to-edge contact, collision distance, relative motion per
step, simulation and collision iterations, triangle quality, curvature
approximation, clearance, thin gaps, normals, and the selected collision
representation.

Blender's cloth RNA exposes `distance_min`, `self_distance_min`,
`collision_quality`, and simulation `quality` steps per frame. The collision source
builds BVHs from mesh triangles and computes triangle intersection,
vertex-to-triangle closest points, and edge-to-edge closest points. Blender also
exposes a separate `voxel_cell_size` for interaction effects. These controls show
that mesh resolution is only one input to collision behavior.

The requested 2 cm to 10 cm scale is therefore a generation policy and future-
compatibility proxy, not a Blender collision guarantee. A coarse target near 10 cm
is suitable only on tagged long, low-curvature, non-contact surfaces; it is not a
minimum edge length. Small, curved, joint, intended contact, attachment, narrow-gap,
and near-skin regions need finer representation.

## Recommendation

Use height-normalized adaptive density and preserve measurements needed for later
solver-specific validation:

- Let `H` be character height. In critical regions, target maximum edge length
  `0.02 m * H / 1.70 m` or finer.
- Permit targets near or above `0.10 m * H / 1.70 m` only on explicitly tagged
  low-curvature, non-contact regions whose shape and clearance remain represented.
- Record edge-length statistics by region, including minimum, median, 95th
  percentile, and maximum.
- Record local curvature radius `R`, opposing-surface clearance `g`, and intended
  future contact thickness `t`, or mark unknown. Preserve `h/R`, `h/g`, and `h/t`
  so a later selected solver can establish actual thresholds.
- Preserve region and attachment IDs through evaluation and triangulation.

Round 1 should not claim collision readiness. It should claim only that generated
geometry is measurable, well-formed, adaptively resolved, and retains the metadata
needed for a later solver-specific test.

## Objective Checks

- Evaluated geometry is triangulable, outward oriented, manifold where intended,
  and free of zero-area triangles, degenerate edges, and unintended
  self-intersections.
- Critical regions satisfy the normalized 2 cm reference-height cap.
- Coarse regions are explicitly tagged and pass curvature, clearance, and intended-
  contact exclusions before using the coarse target.
- Every generated region reports edge statistics and the available `R`, `g`, and
  `t` measures.
- Uniform object scaling preserves normalized topology, region IDs, attachment
  metadata, and normalized edge statistics.

## Uncertainty

The proposed critical-region cap is a conservative project policy, not a value
required by Blender. Its adequacy remains unproven until a later round selects a
collision representation, solver settings, contact thickness, expected motion, and
representative deformation test.

## Sources

- [Blender 5.2 cloth collision settings](https://docs.blender.org/manual/en/5.2/physics/cloth/settings/collisions.html)
- [Blender 5.2 cloth RNA at revision `fbe6228777e7d9afefcd61a413844e790ae75db7`](https://github.com/blender/blender/blob/fbe6228777e7d9afefcd61a413844e790ae75db7/source/blender/makesrna/intern/rna_cloth.cc)
- [Blender collision implementation](https://github.com/blender/blender/blob/fbe6228777e7d9afefcd61a413844e790ae75db7/source/blender/blenkernel/intern/collision.cc)
- [Blender 5.2 rigid-body collision representations](https://docs.blender.org/manual/en/5.2/physics/rigid_body/properties/collisions.html)
- [Bridson, Fedkiw, and Anderson, Robust Treatment of Collisions, Contact and Friction for Cloth Animation](https://graphics.stanford.edu/papers/cloth-sig02/cloth.pdf)
