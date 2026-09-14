# Source Rest Pose Contract

**Status:** COMPLETE
**Question:** Does rig generation require the user to classify a mesh as T- or
A-pose?
**Date:** 2026-09-14

## Conclusion

Blender rig generation and Automatic Weights do not require a categorical T- or
A-pose declaration. The tool can preserve and fit a supported neutral source rest
pose while deriving bone transforms continuously from landmarks and geometry.

Removing the category does not remove pose constraints. The current ten-landmark
workflow cannot reliably recover anatomy from arbitrary crouched, crossed, twisted,
or materially flexed poses. A supported source must remain upright and uncrossed,
with substantially extended elbows and knees. Arm elevation may vary continuously
and independently, including conventional A-pose, T-pose, and poses between them.

## Evidence

- Blender defines the armature's Edit Mode configuration as its rest position and
  applies Pose Mode transforms as offsets from that position. The manual imposes no
  T- or A-pose classification.
- Blender Automatic Weights calculates influence from vertex-to-bone distance using
  its bone-heat algorithm. It does not consume a pose-class label.
- VRM 1.0 requires a specific visual and numerical T-pose. Removing the input label
  therefore does not remove the project's canonical T mapping. The mapping must be
  calculated from the actual source rest transforms instead of selected from a
  binary T/A branch.
- The Milestone 1 implementation currently validates and stores `source_pose`, but
  does not branch its generated geometry on the value. Replacing the category is a
  localized application-contract change rather than an architecture change.

## Sources

- Blender Manual,
  [Armature posing introduction](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/animation/armatures/posing/introduction.rst),
  accessed 2026-09-14.
- Blender Manual,
  [Armature Deform parenting and Automatic Weights](https://projects.blender.org/blender/blender-manual/raw/branch/main/manual/animation/armatures/skinning/parenting.rst),
  accessed 2026-09-14.
- VRM Consortium,
  [VRM 1.0 T-pose specification](https://github.com/vrm-c/vrm-specification/blob/821c11b250d8c70d5804ee13431e42bee56ea9c0/specification/VRMC_vrm-1.0/tpose.md),
  commit `821c11b250d8c70d5804ee13431e42bee56ea9c0`.
- Local implementation: `src/rigged_anatomy/application.py` and
  `src/rigged_anatomy/__init__.py` as inspected on 2026-09-14.
