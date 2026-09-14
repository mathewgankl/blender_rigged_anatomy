# Rigging Standards and MS-Human-700

**Status:** ACTIVE EVIDENCE
**Scope:** Milestone 0, Round 1 skeleton and anatomical IK only
**Researched:** 2026-09-13

This report was produced by a bounded research subagent. On 2026-09-13, the user
accepted it as Round 1 planning-interview evidence without a model-routing rerun or
additional primary-agent verification. Future research still follows the configured
model and effort requirements.

## Findings

**Facts.** The three relevant targets solve different problems. Rigify is a
Blender rig generator and authoring convention. Autodesk HumanIK, represented in
FBX by `FbxCharacter`, is a proprietary characterization and retargeting schema.
VRM 1.0 is a versioned humanoid interchange specification on glTF. None defines
the detailed patella, scapula, tendon-path, or muscle-relation model required by
this project.

Rigify separates original, mechanism, and deformation bones with `ORG-`, `MCH-`,
and `DEF-`; unprefixed bones are controls, lateral names use suffixes such as
`.L` and `.R`, and the root is `root`. Its metarig is fitted before generation.
These are useful native-Blender conventions, but Rigify is not a cross-vendor
skeleton standard.

HumanIK assigns arbitrary skeleton objects to semantic character nodes. The
official FBX SDK exposes `FbxCharacter::ENodeId` values such as hips, knee,
ankle, chest, collar, shoulder, elbow, wrist, neck, head, roll, spine, and finger
nodes; `SetCharacterLink` associates a skeleton node with an ID. Therefore,
interoperability requires an explicit mapping, not HumanIK-shaped source bone
names. The SDK evidence does not identify the current MotionBuilder UI's minimum
required slot subset; the relevant current help page was inaccessible.

VRM 1.0 provides the strongest public semantic contract. It defines required
bones, uniqueness, parent-child rules, positive scale, and a numerical and visual
T-pose. It expressly permits non-humanoid nodes between humanoid nodes. This lets
the production rig retain scapulae, patellae, twist bones, and helpers while an
export projection remains conformant.

## Three-Way Comparison

| Target | Contract and strengths | Round 1 alignment | Limits |
|---|---|---|---|
| Blender Rigify | Blender-native metarig-to-rig workflow; clear control/mechanism/deform roles and side naming | Reuse role prefixes, `.L`/`.R`, `root`, and control/deform separation | Add-on implementation, not interchange standard; do not require Rigify at runtime |
| Autodesk HumanIK / FBX Character | Semantic node IDs, explicit skeleton-to-character links, control rig and retargeting support | Maintain a deterministic adapter from canonical deform roles to FBX character node IDs | Proprietary ecosystem; current UI required-slot documentation remains unverified; detailed anatomy is outside its character schema |
| VRM 1.0 Humanoid | Open, versioned humanoid names, required set, hierarchy constraints, positive uniform scale, defined T-pose | Use as the canonical interoperability vocabulary and hierarchy projection | Export skeleton is deliberately simpler than the authoring rig; no anatomical mechanics model |

## `ms_human_700` Viability

**Facts.** MuJoCo Menagerie revision
`8161bba264d7fa7c99ca301e91e7fb44737676ad` packages full-body, locomotion, and
manipulation MJCF variants and requires MuJoCo 3.2.6 or later to run. The full
model includes XML body trees and defaults, STL/OBJ bone geometry, constraints,
spatial tendons, wrapping geometry, and muscle actuators. Its main file includes
separate body, asset, tendon, and muscle XML files. Upstream revision
`2d686957aefd5739cf4d2859a6acfd94c8f84400` reports 90 bodies optimized to 80,
206 joints constrained to 85, and 700 actuators.

The tendon files are high-value evidence because ordered sites and wrapping
objects encode attachment paths across joints. The muscle files connect those
paths to actuators. Bone assets include independent structures such as pelvis,
patella, tibia/fibula, clavicle, and detailed spine and hand geometry.

**Assessment.** It is viable as a relationship reference, not as a Blender rig
foundation. MJCF bodies and multiple scalar joint degrees of freedom do not map
directly to Blender edit/pose bones, its fixed anthropometry conflicts with
stylized meshes, and 700 actuators exceed Round 1's major-visible-mechanics scope.
Running or importing it would add an unnecessary MuJoCo dependency.

**License.** `ms_human_700/LICENSE` is Apache-2.0, as is the upstream model
license. Copying and modification are permitted, but distribution of copied or
derived files must include the license, retain applicable notices, and mark
modified files. No `NOTICE` file exists at the inspected model root. The README
also requests the MS-Human-700 paper citation for academic use. The minimal-risk
choice is to cite the model and encode independently selected relationships and
tests; do not ship its XML or meshes. If exact XML, parameters, or geometry are
later copied, track provenance per file and satisfy Apache-2.0 redistribution
terms. This is an engineering recommendation, not legal advice.

## Recommendation

Use a native Blender authoring rig with a small canonical semantic registry and
dependency-free export mappings.

1. Name role-bearing bones with Rigify-compatible conventions: `root`,
   `DEF-<stem>`, `MCH-<stem>`, unprefixed animator controls, and `.L`/`.R`.
2. Use stable stems such as `hips`, `spine`, `chest`, `upper_chest`, `neck`,
   `head`, `thigh`, `shin`, `foot`, `toe`, `clavicle`, `scapula`, `upper_arm`,
   `forearm`, and `hand`. Treat the stem's canonical role, not its display name,
   as the mapping key.
3. Project the core hierarchy to VRM: `root -> hips -> spine -> chest ->
   upper_chest -> neck -> head`; each leg is `hips -> thigh -> shin -> foot ->
   toe`; each arm leaves `upper_chest` through clavicle to upper arm, forearm,
   and hand.
4. Keep `DEF-scapula.L/R` between clavicle and upper arm. VRM permits this
   non-humanoid intermediate. Keep patella and twist bones as driven anatomical
   branches. Omit helpers from VRM/HumanIK projections and bake their result into
   mapped deform bones when exporting.
5. Implement VRM and HumanIK as data mappings at the boundary. Do not import
   Rigify, a VRM add-on, FBX SDK, MuJoCo, or MS-Human-700 at runtime.

## Objective Checks

1. Every required VRM 1.0 role maps to exactly one deform bone; no bone fulfills
   two VRM roles, and every mapped parent path obeys the VRM hierarchy.
2. Every selected HumanIK/FBX `ENodeId` maps deterministically to one canonical
   role; unmapped anatomical helpers never enter the characterization projection.
3. Only `DEF-` bones deform `Body_lowpoly`; controls and `MCH-` bones have
   deformation disabled. Left/right pairs use `.L`/`.R` consistently.
4. Regeneration produces identical names, hierarchy, role mappings, and rest
   transforms from identical landmarks.
5. The same normalized landmarks at object scales `0.1`, `1`, and `10` produce
   endpoint and IK-target errors no greater than `1e-5` of character height after
   normalization, with no negative or non-uniform rest scale in the export view.
6. Knee and elbow sweeps retain their configured bend direction without flips;
   patellae remain anterior to the knee axis and scapulae move independently of
   the upper arms.
7. Representative biceps and hamstring relation paths span the correct joint and
   shorten monotonically over the tested flexion interval. Round 1 creates no
   muscle volume, actuator, or physics object.
8. A clean Blender 5.2.1 process can generate and validate the rig with no
   installed Rigify, VRM, Autodesk, MuJoCo, or MS-Human-700 package.

## Sources

- [Blender 5.0 Rigify basic usage](https://docs.blender.org/manual/en/5.0/addons/rigging/rigify/basics.html) and [bone positioning](https://docs.blender.org/manual/en/5.0/addons/rigging/rigify/bone_positioning.html). The available manual evidence is 5.0; the target API is [Blender 5.2](https://docs.blender.org/api/5.2/).
- [Rigify naming source at `f39ed89170ba2f7948417021ac8f3f2eba56e730`](https://github.com/blender/blender-addons/blob/f39ed89170ba2f7948417021ac8f3f2eba56e730/rigify/utils/naming.py). This archived mirror predates Blender 5.2; the current extension source returned `403` during inspection.
- [Autodesk FBX SDK `FbxCharacter`](https://help.autodesk.com/cloudhelp/2020/ENU/FBX-Developer-Help/files/cpp_ref/FBX_Developer_Help_cpp_ref_class_fbx_character_html.html) and [MotionBuilder SDK `FBCharacter`](https://help.autodesk.com/cloudhelp/2022/ENU/MotionBuilder-SDK/cpp_ref/class_f_b_character.html).
- [VRM 1.0 humanoid](https://github.com/vrm-c/vrm-specification/blob/821c11b250d8c70d5804ee13431e42bee56ea9c0/specification/VRMC_vrm-1.0/humanoid.md) and [T-pose](https://github.com/vrm-c/vrm-specification/blob/821c11b250d8c70d5804ee13431e42bee56ea9c0/specification/VRMC_vrm-1.0/tpose.md), revision `821c11b250d8c70d5804ee13431e42bee56ea9c0`.
- [Menagerie `ms_human_700` README](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/README.md), [main MJCF](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/MS-Human-700.xml), and [model license](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/LICENSE).
- [Menagerie arm tendon example](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/assets/tendon/Tendon_Arm_r.xml), [leg tendon example](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/assets/tendon/Tendon_Leg_r.xml), and [arm muscle example](https://github.com/google-deepmind/mujoco_menagerie/blob/8161bba264d7fa7c99ca301e91e7fb44737676ad/ms_human_700/assets/muscle/Muscle_Arm_r.xml).
- [Official MS-Human-700 repository at `2d686957aefd5739cf4d2859a6acfd94c8f84400`](https://github.com/LNSGroup/MS-Human-700/tree/2d686957aefd5739cf4d2859a6acfd94c8f84400).
