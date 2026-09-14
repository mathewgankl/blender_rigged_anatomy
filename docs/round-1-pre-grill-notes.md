# Round 1 Pre-Grill Design Notes

**Status:** SUPERSEDED
**Replaced by:** `docs/prds/round-1.md`
**Target:** Blender 5.2 LTS on Windows
**Updated:** 2026-09-13

These notes predate the completed `matt-grill-with-docs` interview and approved
PRD. They preserve historical planning input but are not execution authority or a
normal continuation read. Read them only for provenance or a named historical
question.

## Outcome

Create a Blender add-on that turns a closed humanoid mesh in T-pose plus ten user
landmarks into a deterministic, scale-independent anatomical IK rig. The rig must
support stylized human proportions, keep its fitted anatomical envelopes inside
the mesh, expose independent shoulder mechanics and patella motion, and encode
representative biceps and hamstring relationships without generating muscle
volume or physics.

Round 1 ends when the generated rig passes automated fitting and IK checks on
`Body_lowpoly` in `roxanne_5.blend`, can be posed to match the supplied reference
image at a human-reviewed visual gate, and is packaged with reproducible local and
GitHub CI checks.

## Baseline

Verified with Blender 5.2.1 LTS, build `9e2066aef7ef`:

- Blender embeds Python 3.13.13; system Python 3.14.3 is also installed.
- `Body_lowpoly` is an unparented mesh with identity transform, no modifiers, no
  armature, 19,722 vertices, 19,720 quad faces, and no non-manifold or loose edges.
- Its world dimensions are approximately `1.040587 x 0.336944 x 1.619984` Blender
  units. The scene unit system is `METRIC` with scale length `1.0`.
- The standards and source-project decisions are recorded in
  `docs/research/rigging-standards-and-ms-human-700.md` and
  `docs/research/node-workflow-and-muskemo.md`.

## Scope

- Human-only meshes, including non-realistic humanoid proportions.
- One mesh target in a local-axis-aligned T-pose: `+Z` up, `-Y` forward, and `+X`
  character-left.
- Required landmarks at the head, neck base, left/right shoulder joint, palm
  center, hip joint, and ankle joint.
- Inferred and user-correctable elbows, wrists, knees, heels, balls, and toes.
- A Blender-native armature with deform, mechanism, and animator-control roles.
- IK legs and arms with stable poles and anatomical bend directions.
- Independent scapula controls with a bounded automatic shoulder contribution.
- Driven patellae and major limb twist distribution.
- Radial anatomical-envelope fitting and visualization.
- One biceps and one hamstring relation path per side for movement validation.
- VRM 1.0 and HumanIK semantic mapping data at export boundaries.
- Add-on install, uninstall, undo, reload, regeneration, headless tests, and
  GitHub CI.

## Exclusions

- Non-human skeletons, quadrupeds, wings, tails, or arbitrary limb counts.
- Muscle meshes, contraction shapes, skin deformation correctives, fat, breasts,
  soft bodies, XPBD, collisions, and all later-round physics.
- Automatic landmark detection from mesh shape or images.
- Anatomically exact bone meshes, medical measurements, or clinical use.
- Finger, facial, breast, cloth, hair, and genital rigs.
- Turnkey VRM/FBX export, retargeting, or a HumanIK control rig.
- A custom node editor or user-authored rig graph.
- Runtime or copied-code dependencies on Rigify, MuSkeMo, MuJoCo,
  MS-Human-700, Autodesk SDKs, VRM add-ons, or NumPy.

## User Workflow

1. Select one closed humanoid mesh in an axis-aligned T-pose.
2. Create or assign these tool-owned landmark roles: `head`, `neck_base`,
   `shoulder.L/R`, `palm.L/R`, `hip.L/R`, and `ankle.L/R`.
3. Run validation. Fix missing, duplicate, non-finite, wrongly sided, or clearly
   out-of-mesh landmarks before generation.
4. Generate a preview. The tool infers the remaining joints, poles, feet, frames,
   envelope radii, and relation paths.
5. Move optional correction handles where stylized proportions make the inference
   unsuitable, set Containment Balance, and regenerate.
6. Generate or update the rig. The add-on commits staged output only after all
   structural checks pass.
7. Pose with hand and foot IK controls. Adjust scapula controls independently when
   the automatic shoulder contribution is insufficient.
8. Run validation and save or export through a separately approved boundary.

## Fitting Semantics

User landmarks are authoritative joint-region anchors. Inferred correction points
are deterministic defaults and become authoritative only after the user moves
them. Landmark positions and the evaluated target mesh are transformed into a
common world space and divided by character height `H`; fitting tolerances and
anatomical ratios operate in these normalized units. Materialization multiplies
the plan by `H`, so scene units and positive target-object scale do not change the
normalized result.

The required mesh must be closed because inside/outside and clearance tests use a
triangulated evaluated mesh and a BVH. Zero or negative scale, zero height,
non-finite coordinates, missing roles, duplicate roles, invalid left/right order,
or an authoritative centerline outside the mesh is an error. Inferred points may
be clamped inward by a documented safety margin; user landmarks are never moved
silently.

Containment applies to a sampled radial envelope around each anatomical bone, not
to chain length, IK reach, deform influence, or the target mesh. Let `b_i > 0` be
a role's base radius at sample `i`, `d_i` its measured radial clearance, and `s`
the safety margin. The usable clearance is `c_i = max(0, d_i - s)`, the global
deflation factor is `g = min(1, min_i(c_i / b_i))`, and the locally deflated
profile is `l_i = min(b_i, c_i)`. For Containment Balance `a` in `[0, 1]`, the
displayed and validated radius is:

`r_i = a * g * b_i + (1 - a) * l_i`

`a = 1` uniformly scales the whole radial profile; `a = 0` preserves unaffected
areas and deflates only local intersections. Both endpoints remain contained.
The generated envelope is a fitting and visualization artifact; only `DEF-`
bones deform the character.

## Rig Model

The canonical role registry is the source of hierarchy, sidedness, bone role,
export mapping, and generated name. It uses `root`, `DEF-`, `MCH-`, unprefixed
controls, and `.L`/`.R` as specified in the standards report.

| Region | Minimum deform roles | Required behavior |
|---|---|---|
| Axial | `hips`, `spine`, `chest`, `upper_chest`, `neck`, `head` | Continuous core hierarchy and positive rest scale |
| Shoulder/arm | `clavicle`, `scapula`, `upper_arm`, `upper_arm_twist`, `forearm`, `forearm_twist`, `hand` | Scapula remains independently controllable; arm IK has explicit target and pole |
| Leg | `thigh`, `thigh_twist`, `shin`, `shin_twist`, `foot`, `toe`, `patella` | Leg IK has explicit target and pole; patella remains anterior and follows flexion |

The root does not deform. Controls and `MCH-` bones never deform. Twist bones
distribute axial roll without changing semantic export mappings. Scapulae,
patellae, twists, poles, and helpers stay in the authoring rig; export projections
omit unsupported helpers and bake their visible result when required.

Each biceps relation path spans the shoulder/upper-arm region and elbow to a
forearm attachment. Each hamstring relation path spans a pelvic attachment and
the posterior knee to a shin attachment. They are line/path evidence only. With
the other joint fixed, biceps length must decrease through elbow flexion and
hamstring length must decrease through knee flexion over the accepted test range.

## Architecture

Use one application command behind both the UI operator and headless harness:

`target + landmarks + settings -> validated rig plan -> staged Blender output`

The implementation has four boundaries:

| Boundary | Responsibility |
|---|---|
| Domain pipeline | Immutable landmark, frame, bone, constraint, envelope, relation-path, and mapping data; validation, normalization, inference, and fitting; no `bpy` import |
| Blender adapter | Read evaluated mesh/landmarks, build BVH data, materialize edit/pose bones and constraints, stage/commit output, inspect generated Blender data |
| Visualization adapter | Generate one versioned Geometry Nodes group from plan attributes for envelope and relation-path geometry; never drive rig state |
| UI/headless entry points | Collect inputs, call the application command, present the same structured result; contain no fitting rules |

Generated objects live in a dedicated collection and carry an ownership marker,
schema version, and plan digest. Regeneration may replace only matching
tool-owned output. It must stage a complete replacement, validate it, then commit;
failure leaves the previous rig and all user-owned data unchanged. If existing
tool output has an Action or unrecognized external dependency, update fails with
an actionable error rather than deleting user work.

No custom node tree is part of Round 1. The generated Geometry Nodes interface is
small and versioned; deleting the modifier affects visualization only.

## Failure Behavior

- Return all independently detectable input errors in one validation result.
- Name the object or landmark role and the failed invariant.
- Do not guess missing landmarks, swap left/right roles, alter user landmarks, or
  commit partial output.
- Reject an unsuitable open mesh instead of treating ray parity as reliable.
- On internal failure, remove staged artifacts and retain previous generated
  output.
- Repeated generation from identical inputs converges to the same plan and scene
  structure without duplicate collections, objects, bones, constraints, or node
  groups.

## Acceptance Criteria

1. A pure test suite passes under system Python 3.14.3; the same domain fixtures
   pass inside Blender 5.2.1's embedded Python 3.13.13.
2. A clean Blender 5.2.1 process installs, enables, disables, and removes the
   add-on without tracebacks or external packages.
3. Headless generation on `Body_lowpoly` creates every registry role exactly once,
   the approved hierarchy and names, and no deform-enabled control or `MCH-` bone.
4. Identical inputs, fresh generation, and repeated generation produce identical
   plan digests, names, hierarchy, normalized rest transforms, constraints,
   mappings, and node interfaces, with no duplicate generated data.
5. Uniform target-object scales `0.1`, `1`, and `10`, both applied and unapplied,
   produce normalized landmark endpoints and IK targets within `1e-5 * H` of the
   scale-1 result. Export-view rest scales remain positive and uniform.
6. Every sampled deform-bone centerline lies inside the evaluated target mesh.
   Every envelope sample satisfies its safety clearance within `1e-4 * H` at
   Containment Balance `0`, `0.5`, and `1`; endpoint settings implement the stated
   local and global formulas.
7. Elbow sweeps from `0` through `140` degrees and knee sweeps from `0` through
   `120` degrees keep a consistent signed bend plane, reach targets within
   `1e-5 * H`, and show no pole flip or discontinuous transform.
8. Patella centers remain anterior to their knee axes and move continuously during
   the knee sweep. Moving a scapula control changes its scapula transform without
   changing the clavicle or opposite scapula; automatic shoulder motion remains
   bounded and can be overridden.
9. With shoulder and hip controls fixed, each biceps and hamstring path respectively
   shortens monotonically during the accepted elbow and knee flexion sweeps, with
   no increase greater than `1e-5 * H` between samples.
10. Automatic weights run on `Body_lowpoly` without a Blender error. Expected
    `DEF-` vertex groups exist; no control or `MCH-` vertex group is created by the
    tool. Visual deformation remains a separate human-reviewed gate.
11. Disabling or deleting the Geometry Nodes visualization changes no plan digest,
    bone transform, constraint, IK result, or mapping result.
12. Missing landmarks, duplicate roles, wrong-sided pairs, non-finite positions,
    open meshes, zero height, and failed staged validation produce deterministic
    errors and no partial committed output.
13. Generate, undo, redo, save, reload, and regenerate preserve valid ownership
    metadata and do not alter unrelated scene objects.
14. A reviewer can pose `Body_lowpoly` from T-pose to the visible torso, head, arm,
    and leg directions in the supplied reference using generated controls, then
    approve a saved Blender pose fixture. The source image alone is not treated as
    a numeric 3D ground truth.
15. GitHub Actions uses least-privilege permissions and runs the Python 3.14 suite
    plus a pinned, checksum-verified Blender 5.2 headless suite on Windows. The
    same commands run locally.

## Delivery Milestones

1. **Harness and minimal rig:** add-on lifecycle, shared application command,
   pure test harness, headless Blender harness, ten-landmark validation, and one
   deterministic axial/leg vertical slice. Stop when its tests pass.
2. **Skeleton fitting:** complete inference, symmetry, normalized scale behavior,
   BVH containment, correction handles, envelope formula, and transactional
   regeneration. Stop when fitting and failure tests pass.
3. **Anatomical IK:** complete arm/leg IK, twists, scapula and patella mechanics,
   and biceps/hamstring relation paths. Stop when pose sweeps pass.
4. **Weighting and pose validation:** automatic-weight readiness, Geometry Nodes
   visualization, deformation review, and approved reference-pose fixture. Stop
   at the human visual gate.
5. **Packaging and CI:** clean installation/removal, documentation, local Windows
   checks, and GitHub Actions. Stop when release-candidate checks pass.

Each milestone requires explicit approval before the next begins.

## Approval Decisions

1. **Python compatibility.** Recommended: Blender's embedded Python 3.13 is the
   add-on runtime; dependency-free domain code is also tested on Python 3.14, and
   external tooling uses 3.14. Requiring the add-on itself to run under 3.14 is
   incompatible with the verified Blender 5.2.1 distribution.
2. **Containment meaning.** Recommended: approve the radial-envelope formula
   above. Scaling chain length would move landmark-defined joints and break IK;
   changing deform influence would not describe a visible bone intersection.
3. **Landmark correction.** Recommended: keep the ten named landmarks required,
   infer elbows/knees/wrists/feet deterministically, and expose those inferred
   points as optional correction handles. Requiring every joint as input would no
   longer meet the intended semi-automatic workflow.
4. **Axis convention.** Recommended: require local `+Z` up, `-Y` forward, and
   `+X` character-left for Round 1. Adding an orientation-calibration workflow
   increases UI and validation scope without improving the approved test asset.
5. **Reference pose gate.** Recommended: use the supplied 2D image for human
   visual approval and make the approved Blender pose a regression fixture. The
   occluded, perspective image cannot uniquely define numeric 3D joint targets.

Production implementation must not begin until grilling is complete and the
resulting `docs/prds/round-1.md` is approved.
