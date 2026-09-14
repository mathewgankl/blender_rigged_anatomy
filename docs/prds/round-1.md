# Round 1 Anatomical Rig PRD

**Status:** APPROVED - MILESTONE 1 AMENDMENT AUTHORIZED
**Target:** Blender 5.2 LTS on Windows
**Runtime:** Blender's embedded Python
**Updated:** 2026-09-14

This document is the authoritative Round 1 product requirement produced from the
completed planning interview and approved by the user on 2026-09-14. It supersedes
`docs/round-1-pre-grill-notes.md` for Round 1 requirements. Approval establishes the
five gated milestones below; only Milestone 1 is currently authorized. It does not
authorize later-round muscle, fat, skin-wrapping, or physics work.

## Outcome

Deliver an installable Blender Extension that turns one selected closed humanoid
skin mesh in a supported neutral source rest pose and ten required landmark handles
into a deterministic anatomical rig. The output contains:

- A fitted low-poly anatomical skeleton with stable role and attachment metadata.
- A smaller Blender-native animator/deform armature mapped to the anatomy.
- Anatomically informed controls for the spine, shoulders, limbs, hands, patellae,
  forearm rotation, and feet.
- Transactional Automatic Weights binding.
- A deterministic post-armature Geometry Nodes corrector that prevents local mapped
  bones from penetrating the bound skin.
- VRM 1.0 and HumanIK semantic mappings without exporters or runtime dependencies.

Round 1 completes only after automated Blender tests pass, `Body_lowpoly` passes
the private local acceptance suite, a reviewer approves the saved reclining pose,
and the Blender Extension ZIP is reproducible through the approved release process.

## Users And Workflow

The primary user is a Blender rigger working with a human or stylized humanoid mesh.
The same application commands serve interactive operators and headless tests.

1. Select one eligible skin-surface mesh in a supported neutral source rest pose.
2. Create or assign the ten required landmark roles.
3. Validate the input and correct all reported errors.
4. Generate a preview with inferred editable correction handles.
5. Adjust correction handles, anatomical morphology controls, and Containment
   Balance where the inferred result is unsuitable.
6. Generate or regenerate the anatomical skeleton and rig transactionally.
7. Run the separate transactional `Bind Skin` operation.
8. Pose through animator controls and inspect fitting, weights, clearance, and
   correction-magnitude diagnostics.
9. Run structural and pose validation before saving or releasing the result.

## Domain Terms

- **Skin mesh:** The one selected user-owned, closed humanoid surface mesh. It is
  not clothing, hair, eyes, mouth parts, or an accessory.
- **Character height (`H`):** The finite positive character height after converting
  the evaluated input to a common space. Distances and tolerances are normalized by
  `H` and materialized at scene scale.
- **Supported neutral source rest pose:** The upright, forward-facing, uncrossed
  pose in which the skin and generated rest rig are authored. Elbows and knees are
  substantially extended. Arm elevation may vary continuously and independently,
  including conventional A-pose, T-pose, and poses between them.
- **Canonical T mapping:** Deterministic metadata that maps the preserved source
  rest pose to T-pose semantics for interoperability and tests. It does not mutate
  the source mesh or generated rest rig into a T-pose.
- **Anatomical skeleton:** The complete collection of named anatomical mesh islands,
  including islands that share a rigid driver.
- **Animator/deform rig:** The smaller armature containing animator controls,
  mechanism bones, and skin-deforming bones.
- **Rig plan:** The canonical serializable description of roles, rest transforms,
  hierarchy, constraints, mappings, anatomy drivers, settings, and generated node
  interfaces before Blender materialization.
- **Template family:** A stable-topology anatomical asset family with declared
  morphology controls and attachment correspondence.
- **Topology tier:** A deterministic density variant of a template family with its
  own stable IDs and attachment remaps.
- **Containment Balance:** A per-bone value in `[0, 1]`. `0` uses local surface
  deflation; `1` uses uniform cross-sectional scaling. Neither endpoint changes
  landmark-defined joint centers or bone length.
- **Binding:** The explicit operation that creates deform weights and the ordered
  skin modifier stack without modifying the generated rig plan.
- **Clearance corrector:** The generated Geometry Nodes modifier after the Armature
  modifier that enforces local mapped skin-to-bone non-penetration. It is not tissue
  wrapping, volume preservation, self-collision, or physics.

## Scope

### Input Contract

- Support one selected human or non-realistically proportioned humanoid skin mesh.
- Require a closed, finite, manifold mesh with nonzero height and local axes `+Z`
  up, `-Y` forward, and `+X` character-left.
- Accept translation, rotation, and positive uniform object scale, whether applied
  or unapplied.
- Reject zero scale, negative scale, non-uniform scale, shear, non-finite geometry,
  and multiple selected skin meshes with actionable errors.
- Do not require or infer a categorical T- or A-pose label.
- Accept continuous and independently different left/right arm elevations within
  the supported neutral source-rest boundary.
- Reject crossed limbs, material elbow or knee flexion, articulated torso poses, or
  another ambiguity that prevents deterministic fitting under the required
  landmarks and correction workflow. Report actionable diagnostics rather than
  guessing.
- Ignore clothing, hair, eyes, mouth parts, accessories, and unrelated scene
  objects.
- Preserve the exact user-owned mesh and landmarks unless the user explicitly runs
  `Bind Skin`; even binding changes must be transactional and undoable.

### Landmarks And Fitting

Require exactly one handle for each role:

- `head`
- `neck_base`
- `shoulder.L`
- `shoulder.R`
- `palm.L`
- `palm.R`
- `hip.L`
- `hip.R`
- `ankle.L`
- `ankle.R`

The tool must:

- Validate missing, duplicate, non-finite, wrongly sided, and out-of-mesh landmark
  data and return all independently detectable input errors together.
- Treat user-entered landmarks as authoritative handles; never move them silently.
- Infer deterministic secondary joint, pole, hand, digit, and foot landmarks.
- Expose editable elbow, wrist, knee, heel, ball, toe, per-digit base/tip, and
  thumb-plane correction handles.
- Fit left and right sides independently. Mirroring is an explicit editing helper,
  not an implicit symmetry constraint.
- Warn when detailed inferred hand and foot structures have not been reviewed.
- Preserve the selected source rest pose and store the canonical T mapping.

The canonical mapping covers every VRM/HumanIK role required below. A source that
already satisfies the canonical T definition maps identically. Every other supported
source rest pose stores deterministic role-local deltas that satisfy VRM 1.0 at
specification commit `821c11b250d8c70d5804ee13431e42bee56ea9c0` while leaving
source mesh coordinates, source armature rest transforms, bone lengths, and joint
centers unchanged. Synthetic conventional-A, intermediate symmetric, and
intermediate asymmetric fixtures provide exact expected deltas; an identity mapping
for a non-T source must fail.

### Anatomical Assets

- Generate a full human anatomical skeleton, not radial envelopes or a reduced
  visible-bones subset.
- Keep each anatomical bone as a named mesh island with a stable role ID, template
  family, topology tier, driver mapping, attachment metadata, and provenance.
- Allow multiple islands that do not move independently to share one rigid driver.
  Keep independently posing phalanges independently transformable.
- Default auditory ossicles and variable non-patellar sesamoids off, but retain
  opt-in generation. Keep the hyoid and structural hand and foot bones available by
  default.
- Do not disable another anatomical role by default without separate user approval.
- Use MuJoCo Menagerie `ms_human_700` at commit
  `8161bba264d7fa7c99ca301e91e7fb44737676ad` as the authoritative conversion
  source. Inventory its `ms_human_700` XML include tree and referenced bone, tendon,
  wrapping, and muscle assets in a checked-in conversion manifest containing source
  paths and SHA-256 values. Use upstream MS-Human-700 commit
  `2d686957aefd5739cf4d2859a6acfd94c8f84400` as provenance evidence, not as a
  second runtime or conversion source.
- Start from preprocessed project-owned assets derived from that manifest. The
  installed extension must work offline and must not download, parse, import, or
  execute MS-Human-700 or MuJoCo at runtime.
- Provide a reproducible developer asset build/import path pinned to those exact
  revisions.
- Declare independent anatomical morphology controls and a neutral starting preset.
  Do not encode deterministic gender categories.

Each topology tier must preserve stable vertex, triangle, region, and attachment
IDs. Attachment and wrapping sites must store:

- Anatomical bone role.
- Named surface region.
- Triangle and vertex correspondence.
- Barycentric coordinates.
- Bone-local fallback coordinates.

Every evaluated site must remain on its intended surface after fitting and
morphology changes.

The source conversion manifest is the closed-set oracle. Every source anatomical
body/mesh and every attachment/wrapping path in the pinned include tree must map to
exactly one retained catalog entry. Auditory ossicles and variable non-patellar
sesamoids use catalog generation-default metadata rather than conversion exclusion.
The manifest may mark non-domain source artifacts such as XML defaults or rendering
materials ignored with a reviewed reason. Tests compare all anatomical and path
source keys to generated catalog keys, not only entries that the converter happened
to emit.

### Geometry Density

Select topology tiers deterministically before materialization. Do not arbitrarily
remesh an existing generated rig.

- Cap evaluated edges at `H/80` in critical joint, attachment, and subcutaneous
  regions.
- Require the 95th-percentile evaluated edge length in each large simple region to
  be at most `H/16`.
- Permit coarser edges only in explicitly untagged flat regions whose fitted-surface
  deviation remains at or below `H/500`; report their minimum, median, 95th
  percentile, and maximum edge lengths separately.
- Select a denser tier and regenerate when the current tier cannot satisfy the
  applicable bound.
- Preserve region, curvature, clearance, thickness, and edge-statistic metadata for
  later solver-specific evaluation.

These are project geometry policies, not claims that the meshes are suitable for a
particular collision or physics solver.

### Containment

- Keep landmark-defined joints, centerlines, and bone lengths fixed.
- Blend local inward surface deflation with uniform cross-sectional scaling through
  Containment Balance.
- Reject an outside centerline, outside joint, or loss of an attachment-critical
  surface.
- Permit noncritical local thinning only with explicit degraded-region warnings and
  measurements.
- Produce manifold anatomical output with no triangle intersection against the
  closed rest-pose skin, subject only to the `1e-4 H` numerical tolerance for
  outside distance.

### Rig Roles And Interoperability

Use a canonical role registry as the source of hierarchy, sidedness, generated
names, deform status, anatomy-driver mapping, and interoperability mappings.
Milestone 2 establishes this data-only registry and its mapping manifests before
catalog and asset generation. Milestone 3 consumes the same registry to materialize
deform, mechanism, and control behavior; it does not create a second role authority.

- Use Rigify-compatible role conventions: `root`, `DEF-<stem>`, `MCH-<stem>`,
  unprefixed controls, and `.L`/`.R` suffixes.
- Deform only through `DEF-` bones. `root`, controls, and `MCH-` bones must not
  deform the skin.
- Map required VRM 1.0 humanoid roles to exactly one canonical deform role and
  preserve the required hierarchy projection.
- Map applicable HumanIK/FBX character node IDs deterministically from canonical
  roles.
- Keep anatomical helpers, twists, patellae, and unsupported details outside the
  interoperability projection while preserving their visible result at a future
  export boundary.
- Do not implement VRM, FBX, or HumanIK export, retargeting, or a HumanIK control
  rig in Round 1.
- Do not require Rigify, a VRM add-on, Autodesk software or SDKs, MuJoCo,
  MS-Human-700, MuSkeMo, Mantis, NumPy, or another external package at runtime.

The required mapping set is closed over these canonical roles: axial `hips`,
`spine`, `chest`, `upper_chest`, `neck`, and `head`; bilateral `clavicle`,
`upper_arm`, `forearm`, `hand`, `thigh`, `shin`, `foot`, and `toe`; and every
bilateral thumb, index, middle, ring, and little-finger phalanx for which the pinned
Autodesk FBX SDK 2020 `FbxCharacter::ENodeId` enum exposes a corresponding node. A
checked-in mapping manifest must name the exact official VRM role and HumanIK
`ENodeId` for each applicable canonical role and explicitly mark unsupported roles.
Tests compare exact key sets and reject missing, duplicate, or unexpected mappings.

### Animator And Mechanism Rig

The animator/deform rig must provide:

- Pose-preserving IK/FK switching and bidirectional snapping for both arms and both
  legs.
- Stable pole behavior and explicit anatomical bend directions.
- A spline-IK spine with pelvis, lower-spine, mid-spine, chest, and upper-chest
  controls, bounded twist and stretch, and separate FK neck and head controls.
- Independent clavicle and scapula controls.
- A default-on bounded automatic shoulder contribution driven by humerus elevation
  through a configurable curve. Manual shoulder controls add to it and may disable
  the automatic term.
- A patella mechanism that moves continuously along a calibrated bounded path on
  the anterior femoral groove during knee flexion.
- Separate radius and ulna anatomical islands. Hand axial rotation drives an
  approximate radius crossing/roll mechanism with ulna stability and distributed
  forearm deform twist.
- Ankle orientation, heel and ball pivots, toe roll, and simplified subtalar side
  tilt.
- Per-phalanx FK and fingertip IK for every digit, pose-preserving bidirectional
  switching, and additive aggregate curl, spread, and thumb-opposition controls.
- Default anatomical mechanism limits with explicit per-rig stylization overrides.
  Report out-of-range poses rather than permanently locking animator controls.

The complete anatomical skeleton remains distinct from the smaller control and
deform rig. Every anatomical island maps deterministically to a rigid, mechanism,
or deform driver.

### Muscle-Relationship Metadata

- Transfer every available attachment and wrapping-path entry from the pinned
  MS-Human-700 source into a versioned project catalog.
- Validate the schema, role references, provenance, and surface references of every
  catalog entry.
- Classify paths into `primary_visible`, `secondary_visible`, and
  `deep_stabilizing` impact bands. The band controls later defaults; it does not
  remove data.
- Instantiate and behavior-test only major visible Round 1 paths.
- Include representative bilateral biceps and hamstring paths and verify that they
  shorten monotonically through their accepted flexion sweeps with the other joint
  fixed.
- Do not create muscle volume, contraction shapes, actuators, or physics objects.

The minimum `primary_visible` groups are bilateral deltoid, pectoralis major,
latissimus dorsi, trapezius, biceps brachii, triceps brachii, forearm
flexor/extensor groups, rectus abdominis, abdominal obliques, erector spinae,
gluteus maximus/medius, iliopsoas, adductor group, quadriceps, hamstrings,
gastrocnemius, soleus, and tibialis anterior. The conversion manifest maps exact
source path IDs to these groups. Every mapped primary path is instantiated and
tested; biceps and hamstrings additionally have the monotonic flexion oracle.

### Materialization And Ownership

Use one application command behind the UI and headless entry points:

`target + landmarks + settings -> validated rig plan -> staged Blender output`

- Python owns validation, normalized fitting semantics, the canonical rig plan,
  armature and constraint materialization, ownership, and transactions.
- Python generates standard Blender Geometry Nodes groups for derived anatomical
  geometry and skin clearance where nodes are suitable.
- Do not add a custom node editor or user-authored rig graph.
- Retain Mantis's declarative transform-graph philosophy only through the
  project-owned serializable rig plan and a low-cost future adapter seam. Make no
  Mantis compatibility claim and copy no Mantis graph, format, or code.
- Store generated objects in a dedicated collection with ownership markers, schema
  version, template version, generator version, and plan digest.
- Store canonical post-materialization content digests for every protected
  armature, anatomical template/object, and generated node group. Regeneration
  compares current content to these digests; a mismatch is a user edit and triggers
  preservation in a new collection rather than replacement.
- Preview, stage complete materialization, run structural validation, and commit
  only after validation succeeds.
- Replace only matching unedited tool-owned output. If generated data was edited,
  preserve it and generate into a new collection. Support customization through
  declared inputs or an explicit user-owned fork, not arbitrary merge behavior.
- Preserve every user-owned datablock and prior valid generated result after any
  failure.

Reserve a versioned `collision_proxy` role/tag, source-anatomy reference, and
derivation-settings boundary in the rig plan for later physics. Round 1 does not
generate solver-ready proxy meshes, use the proxy in skin clearance, or claim
compatibility with a physics solver.

### Skin Binding

`Bind Skin` is a separate operation after successful rig generation.

- Use Blender Automatic Weights against the deform armature.
- Create the Armature modifier with Preserve Volume enabled by default and expose a
  user toggle.
- Use anatomical geometry only for read-only weight diagnostics. Do not seed or
  post-process Blender weights from anatomical distances in Round 1.
- If Automatic Weights fails, preserve all prior modifiers and vertex groups, keep
  the valid generated rig and anatomy, and report actionable diagnostics.
- Mark a binding stale after skin topology, source-rest geometry, armature-rest,
  anatomy-role mapping, or clearance-node schema changes.
- Do not mark a binding stale for translation, rotation, or accepted positive
  uniform object-scale changes alone.
- Never rebind silently. Rebuild stale weights and correction data only through the
  explicit transactional operation.

The ordered generated modifier stack is:

1. Armature deformation.
2. Bone-clearance correction.

This narrow Round 1 skin work exists to validate bone-driven deformation and local
non-penetration. It does not move muscle/fat-driven Surface Deform, Mesh Deform,
wrapping, tissue volume, unrelated-region body self-contact, or physics into Round
1.

### Bone-Clearance Corrector

- Generate a standard Geometry Nodes modifier after the Armature modifier.
- Evaluate fitted anatomical meshes through their mapped rig drivers.
- Correct only against anatomically mapped bones whose deform groups influence the
  skin region. A bone is a candidate for vertex `v` when its mapped deform group has
  weight greater than `1e-6` on `v` or on a vertex joined to `v` by one mesh edge.
  Expansion is exactly one topological ring and never crosses to another disconnected
  skin component.
- Ignore unrelated-region contact such as a hand bone approaching torso skin.
- Enforce minimum signed skin-to-bone clearance of `1e-4 H` by pushing only
  penetrating or under-clearance skin outward.
- Apply the full required correction. Do not clamp and leave known penetration.
- Fail pose validation when any correction exceeds `1% H`; report the pose,
  vertices, anatomical roles, and maximum displacement.
- Enable the corrector by default, expose a user toggle, and state that disabling it
  forfeits the non-penetration guarantee.
- Expose a correction-magnitude debug overlay. The overlay is disposable and may be
  rebuilt after reload.

When multiple candidate surfaces require correction, choose the correction that
produces the greatest remaining signed-clearance violation, reevaluate until all
candidates meet clearance or a versioned iteration limit fails validation, and
break equal-distance ties by canonical anatomical role ID. Synthetic fixtures must
store expected candidate masks and affected/unaffected vertex sets.

The future skin pipeline remains bone-driven muscle/fat layers followed by an
enclosing evaluated soft-tissue surface or cage that drives skin. Round 4 tests
Surface Deform first and Mesh Deform only as a fallback. Direct binding from
individual anatomical bone surfaces to skin is not the final architecture.

### Persistence And Breaking Changes

- Persist generated rig and anatomy, plan digest, ownership/schema/template
  versions, declared settings, source-rest transforms and canonical mapping,
  binding freshness, control behavior, and the approved reference pose across
  save/reload.
- Allow preview caches and debug overlays to rebuild after reload.
- Treat each successful `Generate/Regenerate` and `Bind Skin` as one Blender undo
  step that restores the exact previous tool-owned and target-binding state.
- Create no partial undo state after a failed operation.
- On an incompatible schema version, leave old output readable but stale and offer
  `Rebuild for Current Version`.
- Stage the rebuilt collection and binding, validate them, and preserve the old
  collection until the user confirms commit. Never migrate generated data silently
  during file load.

## Exclusions

- Non-human skeletons, arbitrary limb counts, quadrupeds, wings, or tails.
- Facial, cloth, hair, genital, breast, or non-anatomical accessory rigs.
- Automatic landmark detection from geometry or images.
- Clinical, diagnostic, or medically exact output.
- Muscle meshes, contraction shapes, soft tissue, fat, breasts, soft bodies, XPBD,
  cloth, collision simulation, or VeeDynamics.
- Skin wrapping from muscle/fat surfaces or cages.
- Unrelated-region body self-collision.
- Exporters, retargeting workflows, or external rig-standard runtimes.
- A custom node editor, Mantis runtime, or Mantis compatibility claim.
- Runtime network access, runtime source conversion, or external Python 3.14 tests.
- A performance gate. Investigate performance only after a user-observed slow
  preview or interaction produces a reproducible case.
- Legacy Blender-version compatibility.

## Failure Contract

- Return structured error and warning codes shared by UI and headless entry points.
- Report all independently detectable input errors in one validation result.
- Name the object, landmark, anatomical role, catalog entry, pose, or generated
  datablock associated with each failure.
- Never guess a missing required landmark, swap sided roles, silently change user
  landmarks, silently rebind, or silently migrate stale data.
- Remove staged artifacts after internal failure while retaining prior generated and
  user-owned data.
- Repeated generation from identical inputs must converge without duplicate
  collections, objects, bones, constraints, modifiers, node groups, or catalog
  entries.

## Acceptance

### Automated Blender Tests

1. A clean Blender 5.2 process installs, enables, disables, and uninstalls the
   built Extension ZIP without tracebacks, external packages, or residual handlers.
2. UI and headless entry points call the same application commands and return the
   same structured results for equivalent inputs.
3. Missing or duplicate landmarks, wrong-sided pairs, non-finite coordinates, open
   meshes, zero height, invalid transforms, unsupported or ambiguous source rest
   poses, and failed staged validation return deterministic errors and commit no
   partial output.
4. Entered landmark handles are reproduced within `1e-4 H`. Derived internal joint
   centers are reported but are not falsely compared directly to skin-surface
   landmarks.
5. Every default-enabled anatomical catalog role is generated exactly once as a
   named manifold island with valid IDs, topology tier, driver mapping, attachment
   metadata, and provenance. Default-off roles remain available by explicit option.
6. Anatomical and path source-manifest keys equal generated catalog keys, with no
   missing, unexpected, or duplicate entry. Ignored manifest entries are restricted
   to reviewed non-domain source artifacts. Every path entry passes schema,
   role-reference, source-reference, hash, and provenance validation. Every
   instantiated attachment evaluates on its intended surface.
7. Critical-region maximum edge length is at most `H/80`. Each large simple
   region's 95th percentile is at most `H/16`; every coarser edge is in an explicitly
   tagged flat exception region whose maximum fitted-surface deviation is at most
   `H/500`.
8. Every anatomical rest mesh has zero triangle intersections with the closed skin,
   and the maximum positive outside distance over all evaluated anatomical vertices
   and surface samples is no greater than `1e-4 H`.
9. Containment Balance values `0`, `0.5`, and `1` preserve joint centers and bone
   lengths, remain contained, and implement the declared local-to-uniform behavior.
10. Identical normalized inputs and pinned asset/schema versions produce the same
    rig-plan digest, names, hierarchy, normalized transforms, constraints, mappings,
    topology-family IDs, node interfaces, and validation results. Blender UUIDs,
    timestamps, and `.blend` byte order are excluded.
11. Applied and unapplied positive uniform object scales `0.01`, `1`, and `100`
    produce equivalent normalized plans and pose results within the applicable
    relative tolerances. Fixtures also cover nonzero translation, arbitrary proper
    rotation, combined translation/rotation/uniform scale, and scene unit scale
    lengths `0.01`, `1`, and `100`. Invalid scale and shear cases fail before
    staging.
12. Every required VRM role maps to one deform role with a valid hierarchy. Every
    applicable HumanIK node in the closed mapping set maps deterministically. Exact
    mapping-manifest key equality passes; missing, duplicate, and unexpected entries
    fail. No control, root, helper, or `MCH-` bone deforms skin.
13. IK targets and IK/FK snaps reproduce required bone endpoints within `1e-4 H`
    and orientations within `0.1` degrees. One hundred alternating switches return
    to those same tolerances without accumulating drift.
14. Single-joint sweeps use increments no larger than `5` degrees. IK/FK transitions
    run at sweep endpoints and midpoint. A named set of combined poses replaces an
    impractical joint-angle cross-product.
15. Source rest, canonical T mapping, reclining reference, bilateral arm-up,
    elbow-flex, hip-flex, knee-flex, spine bend/twist, foot-roll/subtalar, and
    representative finger-curl poses and transitions match the versioned pose
    manifest within the position and orientation tolerances. The conforming-T
    fixture mapping is identity. Conventional-A, intermediate symmetric, and
    intermediate asymmetric fixture mappings match their exact expected role-local
    deltas while source rest transforms remain unchanged. Adjacent rotation samples
    follow the expected quaternion shortest arc without a sign inversion.
16. Patellae remain anterior and move continuously; radius/ulna pronation mechanics
    and spine, foot, digit, and shoulder outputs stay within their numeric manifest
    bounds; shoulder automation remains manually overridable; independent scapula
    controls do not move the opposite scapula beyond `0.1` degrees or `1e-4 H`.
17. Representative biceps and hamstring paths shorten monotonically through their
    respective flexion sweeps with no increase greater than `1e-4 H` between
    samples.
18. Automatic Weights reports success; every deformable skin vertex has finite
    normalized influence from an allowed deform group; required bilateral groups
    exist; controls and mechanism groups do not influence skin.
19. Preserve Volume is enabled by default, both toggle states evaluate finite valid
    geometry, and no test claims realistic tissue-volume preservation.
20. With clearance enabled, mapped local bones have at least `1e-4 H` signed
    clearance throughout the pose suite. Any correction over `1% H` fails with the
    required diagnostics. Candidate masks equal the fixture masks, and unrelated-
    region contact changes no vertex outside those masks.
21. Topology, source-rest geometry or mapping, rest-rig, role-map, and
    correction-schema changes stale a binding. Accepted object transforms do not.
    No stale binding rebuilds silently.
22. Generate, regenerate, bind, undo, redo, save, reload, and explicit schema rebuild
    preserve ownership and durable state without changing unrelated scene data.
23. Mutating each protected armature, anatomy object/template, and node group causes
    its content digest to mismatch; regeneration preserves the edited output and
    stages a new collection.
24. Deleting or disabling disposable visualization and debug overlays changes no
    plan digest, rig transform, constraint, mapping, or binding weights.

The automated pose oracle is `tests/fixtures/pose-suite-v1.json`. Before Milestone
3 mechanism implementation begins, that versioned manifest must contain exact
numeric limits, expected bend signs, and expected endpoint transforms for every
required role and mechanism; all named single-joint and combined poses; and the
source citation or project rationale for each limit. Its required named poses are
the complete set listed in criterion 15. Elbow flexion spans `0` through `140`
degrees and knee flexion spans `0` through `120` degrees. The schema rejects a
missing required role, mechanism, endpoint, bound, or combined pose so the
implementation cannot shrink the suite to pass. Approval of Milestone 3's kickoff
locks version 1 before behavior code depends on it.

### Fixtures And Human Gate

- Use deterministic redistributable low-detail conforming-T, conventional-A,
  intermediate symmetric, and intermediate asymmetric neutral-rest mannequins for
  public CI branch coverage. Include unsupported bent and crossed fixtures.
- Keep `roxanne_5.blend`, `Body_lowpoly`, and the supplied reference image local and
  private unless redistribution rights are documented.
- Run the full local integration suite on `Body_lowpoly` as the private T-pose
  fixture declared by the project brief.
- Save a deterministic reclining pose, camera, and render fixture after numerical
  rig and clearance checks pass.
- Require documented human approval that the generated controls can reproduce the
  visible torso, head, arm, hand, and leg directions plausibly. Do not use pixel
  comparison against the illustration.

## Licensing And Provenance

- License independently written add-on code under `GPL-3.0-or-later`.
- Keep MS-Human-700-derived assets under Apache-2.0.
- Record the exact upstream revision and source path for every derived asset and
  catalog entry.
- Retain the Apache-2.0 license and applicable notices and mark every modified file.
- Include the requested MS-Human-700 citation where applicable.
- Copy no Mantis or MuSkeMo code, node trees, persisted formats, or bundled
  dependencies.
- Do not distribute the Roxanne model or reference image without documented rights.

## Delivery And CI/CD

The release artifact is one dependency-free Blender Extension ZIP containing:

- `blender_manifest.toml`.
- Semantically versioned add-on code.
- Independently versioned schemas and templates plus the versioned JSON
  semantic/path/provenance catalog.
- Offline derived assets.
- GPL and Apache licenses, notices, provenance, and modification records.
- User and validation documentation.

GitHub Actions must:

- Use least-privilege permissions.
- Run on Windows with a pinned Blender 5.2 distribution whose checksum is verified.
- Use only redistributable synthetic and packaged fixtures.
- Trigger on pull requests targeting `main` and pushes to `main`; semantic version
  tags additionally trigger the draft-release job.
- Run the headless acceptance subset and clean Extension ZIP lifecycle tests.
- Build the same Extension ZIP that local release checks consume.
- On a semantic version tag, create a draft GitHub Release with the ZIP, SHA-256,
  licenses/notices, and test evidence.
- Never publish the draft automatically. A person publishes only after the private
  `Body_lowpoly` suite and reclining-pose visual gate pass.

Two clean package builds from identical source must produce ZIPs with matching
SHA-256 values. The packager normalizes archive path order, relative paths,
permissions, compression settings, and timestamps before comparison.

## Implementation Milestones

Each milestone requires explicit user approval before work begins and explicit
approval of its evidence before the next milestone begins.

These milestones are approval gates, not implementation batches. During execution,
`docs/project-state.md` names only the next smallest dependency-ordered vertical
increment, its cheapest decisive test, and its stop condition. Complete and verify
that increment before detailing or starting another.

### Milestone 1: Harness And Vertical Slice

Build the Extension skeleton, shared UI/headless application command, canonical
serializable rig-plan model, structured validation result, deterministic test
fixtures, and one unilateral limb-chain anatomy/armature vertical slice.

Stop when the ZIP lifecycle, malformed-input, normalized-plan, materialization,
idempotence, and one-chain headless tests pass.

### Milestone 2: Assets And Anatomical Fitting

Build the data-only canonical role registry and mapping manifests first. Then build
the pinned reproducible asset-import path, offline anatomy assets, topology tiers,
complete path/provenance catalogs, morphology controls, all anatomical islands,
correction handles, containment, attachment evaluation, and scale tests.

Stop when all catalog, topology, density, provenance, fitting, containment, and
scale criteria pass on synthetic fixtures and the local `Body_lowpoly` rest fixture.

### Milestone 3: Animator And Deform Rig

Consume the Milestone 2 role registry and mappings to build deform/mechanism/control
armatures, spline spine, limb IK/FK and snaps, shoulders, patellae, radius/ulna,
feet, digits, anatomical limits, and major visible relationship paths.

Stop when hierarchy, mapping, mechanic, snap, monotonic-path, and five-degree pose
sweep tests pass.

### Milestone 4: Binding, Clearance, And Pose Approval

Build transactional Automatic Weights binding, Preserve Volume control, binding
freshness, read-only weight diagnostics, the generated Geometry Nodes clearance
corrector, correction overlay, and the complete pose suite.

Stop when structural weight checks, non-penetration checks, correction thresholds,
private `Body_lowpoly` integration, and documented reclining-pose human approval
pass.

### Milestone 5: Lifecycle And Release Candidate

Complete ownership conflict behavior, one-step undo, save/reload, staged breaking-
schema rebuild, documentation, final packaging, GitHub Actions, checksums, and draft
GitHub Release automation.

Stop when all public CI checks and private local release checks pass and a draft
release artifact is ready for separate publication approval.

## Risks And Proof Obligations

- A deterministic Geometry Nodes signed-clearance implementation that remains
  stable across all mapped anatomical regions is not yet proven. Milestone 1 or 2
  may build a disposable technical spike, but production clearance work remains in
  Milestone 4 and any material fallback requires approval.
- Blender Automatic Weights may fail or produce poor weights on `Body_lowpoly`.
  Round 1 must report failure rather than adding an unapproved custom weighting
  algorithm.
- Full MS-Human-700-derived topology and path conversion is substantial. The pinned
  build must prove completeness, stable IDs, and provenance before runtime assets
  are accepted.
- Stable topology, containment, and the density bounds may conflict for extreme
  stylized proportions. The approved response is deterministic tier selection,
  explicit degraded-region warnings, or rejection of critical failure, not silent
  remeshing or anatomical-length changes.
- The reclining illustration is not numeric 3D ground truth. Human approval remains
  an explicit local gate.

## Open Decision

Exact default anatomical limits, expected per-sample mechanism transforms,
canonical non-T-to-T fixture deltas, named combined-pose values, and numeric
continuity bounds require a versioned `tests/fixtures/pose-suite-v1.json` proposal
backed by targeted anatomy evidence. These values were not settled in the planning
interview and must not be invented during implementation. They do not block
Milestones 1 or 2. They must be reviewed and explicitly approved before Milestone 3
begins; until then, Milestone 3 and later milestones remain blocked.

The exact numeric boundary between a supported neutral source rest pose and rejected
joint flexion or articulation requires a separate proposal and user approval before
Milestone 2 source-rest validation is implemented. This does not block the
Milestone 1 removal of categorical pose input.

## Approval Gate

The user approved this PRD and authorized Milestone 1 on 2026-09-14. On the same
date, the user approved the continuous source-rest amendment recorded in
`docs/decisions/source-rest-pose-contract.md`. Milestone 1 remains authorized, but
its evidence must be refreshed against the amended contract. Milestone 2 and later
work remain unauthorized until each preceding milestone's evidence is approved. The
numeric pose oracle above requires its own approval before Milestone 3. Any other
change to public behavior, persistent data, licensing, compatibility, milestone
scope, or a fallback named in the risks above requires a new decision before
implementation.
