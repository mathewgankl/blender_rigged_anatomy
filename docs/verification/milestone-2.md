# Milestone 2 Verification

**Status:** IN PROGRESS - NAMING AUTHORITY AND CATALOG SEED PASS COMPLETE
**Date:** 2026-09-15
**Environment:** Windows, Blender 5.2.1 LTS, embedded Python 3.13.13
**Scope:** Round 1, Milestone 2 only

## Current Result

The first Milestone 2 increment establishes a versioned, data-only canonical role
registry. It contains 55 stable root and deform role IDs covering the approved axial
chain, bilateral limb chains, scapula intermediates, and complete bilateral finger
chains. Each record declares its parent, side, generated name, and deform status.

The second increment adds versioned VRM 1.0 and HumanIK/FBX Character mapping
manifests. Each manifest has exactly the registry's 55 keys, unique supported target
names, and explicit unsupported values for `root` and both scapula roles. The data
uses VRM specification commit `821c11b250d8c70d5804ee13431e42bee56ea9c0` and
Autodesk's official FBX SDK 2020 `FbxCharacter::ENodeId` reference.

These increments contain no armature materialization, controls, constraints,
mechanism behavior, anatomy assets, or exporters.

The third increment adds a reproducible inventory of the pinned MuJoCo Menagerie
source. Starting from `MS-Human-700.xml`, it follows nested includes relative to
their declaring files and records SHA-256 values for 23 XML files and 190 referenced
resources. The manifest retains 186 anatomy meshes and explicitly ignores the
marble rendering texture and three water-bottle manipulation meshes.

The fourth increment extends that same manifest to 80 unique anatomical bodies, 700
unique tendon paths, 2,576 ordered attachment-site references, 252 ordered wrapping
references, and 700 muscle actuators. Each retained source entity has one stable
catalog key, and the generator rejects duplicate keys or a mismatch between the
tendon and actuator key sets.

The fifth increment adds one packaged schema-version-1 descriptor consumed by
dependency-free anatomy and relationship catalog validators. Anatomy entries require
stable anatomy and driver roles, template and topology metadata, generation defaults,
surface-region topology IDs, and pinned provenance. Relationship entries preserve
every source tendon element in order and validate actuator closure plus anatomy-role,
region, triangle, vertex, barycentric, and bone-local fallback references. This
increment defines and tests the catalog boundary without populating either catalog.

The sixth increment resolves every tendon reference to one source declaration while
preserving effective body ownership through nested XML includes. The manifest now
contains 2,756 unique attachment-site declarations: 2,536 are directly referenced
by path elements and 220 are wrap sidesites. Their occurrence counts are 2,576 and
240 respectively. It also contains 182 unique wrapping-geometry declarations that
cover all 252 wrap occurrences. Every record retains its declaring XML path, owning
body source key, original XML attributes, and reference counts.

The seventh increment adds a deterministic developer converter and one packaged
offline source-tier anatomy artifact for `mesh:humerus`. The converter verifies the
pinned source hash, reads binary STL without an external dependency, merges exact
duplicate coordinates in source order, and uses zero-based array positions as stable
vertex and triangle IDs. The artifact records meter units, complete provenance, an
Apache-2.0 modification notice, and reproducible topology diagnostics. The Extension
now distributes the upstream Apache-2.0 license alongside its GPL-3.0-or-later code.

The eighth increment preserves that source tier and adds a separate generation-ready
`base` humerus tier. Blender 5.2.1 LTS performs a 0.002-meter Voxel Remesh with zero
adaptivity, collapse-decimates to 600 triangles, recalculates winding, and assigns
canonical IDs by lexicographic vertex order and winding-preserving triangle order.
The result has 302 vertices, 600 triangles, one connected component, and no boundary,
over-connected, inconsistent-winding, or degenerate topology. Its bidirectional
vertex-to-surface samples measure 0.383 mm at p95 and 1.491 mm maximum against the
preserved source tier. Regression guards cap those sampled values at 0.5 mm and 1.6
mm respectively. These are provisional local regression bounds, not approved general
asset-conversion acceptance criteria.

The ninth increment makes the canonical role registry authoritative in application
plan construction. Registry loading now rejects unsupported schema versions,
duplicate role IDs or generated names, missing parents, hierarchy cycles, and side/ID
mismatches, and exposes one required-role lookup. The left-arm plan projects its
included hierarchy and derives Blender names and deform flags from injected registry
definitions instead of repeating `DEF-` literals.

The same increment adds the first packaged anatomy catalog entry. It maps
`mesh:humerus` to the right-side anatomical role `humerus.R`, canonical driver role
`upper_arm.R`, and packaged `base` artifact. Its `whole_surface` region resolves
vertex and triangle IDs through that artifact. The relationship fixture now uses the
matching right biceps source path rather than crossing source sides.

The tenth increment adds focused loader regressions for every role-registry
corruption branch: unsupported schema versions, duplicate role IDs, duplicate
generated names, missing parents, hierarchy cycles, and side/ID mismatches. Catalog
schema version 1 now declares `all` as its surface-region topology sentinel, and both
anatomy and relationship validation resolve that declaration only against a loaded
packaged artifact. Regressions reject an undeclared sentinel and reject `all` when
the referenced artifact tier cannot be loaded.

## Red-Green Evidence

The focused Blender-headless test first failed at the missing registry module:

```text
ModuleNotFoundError: No module named 'rigged_anatomy.role_registry'
```

After adding the immutable loader and packaged `role-registry-v1.json`, the focused
test passed. It checks schema version 1, exact role-key equality, unique role IDs and
generated names, the full parent map, `.L`/`.R` sidedness, `DEF-` naming, and the
non-deforming `root` exception.

The mapping test then failed at the next missing boundary:

```text
ModuleNotFoundError: No module named 'rigged_anatomy.semantic_mappings'
```

After adding both manifests and their validating loader, the mapping test passed. It
checks exact canonical keys, exact official target names, source versions, unique
supported targets, and the explicit unsupported set.

The source-manifest test then failed at the missing packaged loader:

```text
ModuleNotFoundError: No module named 'rigged_anatomy.source_manifest'
```

The first inventory run also exposed nested body includes when it failed to resolve
`Body_Arm_l.xml` from the model root. Resolving include paths relative to each
declaring XML produced the complete 23-file closure. The checked-in manifest now
matches a fresh inventory of the pinned temporary checkout exactly.

The entity-level regression first failed because the file-level manifest had no
`bodies` collection:

```text
KeyError: 'bodies'
```

After extending the generator, all entity counts, source-key uniqueness, ordered
path-element counts, catalog-key assignments, and one-to-one actuator/tendon
references pass.

The catalog test first failed at the missing validator module:

```text
ModuleNotFoundError: No module named 'rigged_anatomy.catalogs'
```

An initial generic surface-reference shape passed its narrow test but did not encode
the PRD's ordered source path or topology correspondence. The strengthened regression
failed on the obsolete required `surface_refs` field and missing path/surface issue
codes. Replacing that provisional shape with ordered `path_points` produced a green
test for valid fixtures and aggregated malformed-reference diagnostics.

The declaration-resolution regression first failed against the previous manifest:

```text
KeyError: 'attachment_sites'
```

The first generator implementation then exposed MuJoCo include semantics:

```text
ValueError: site:EO_R10_l-P1 must resolve to exactly one owned declaration; found 0.
```

`Body_Torso_Simple.xml` declares sites at its fragment root but is included from
inside the named pelvis body. Traversing includes in place from the root model
preserved that effective owner. The regenerated manifest then passed exact comparison
with the pinned checkout and complete site, sidesite, and wrap reference closure.

The anatomy conversion test first failed at the absent runtime asset boundary:

```text
ModuleNotFoundError: No module named 'rigged_anatomy.anatomy_assets'
```

After the initial exact-coordinate conversion, the assumed closed-manifold assertion
failed with 45 boundary edges. A weld-tolerance sweep through `1e-3` meters and a
Blender STL-import comparison reproduced the defects rather than removing them. The
pinned source contains 309 vertices and 588 triangles with 45 boundary edges, 3
over-connected edges, 2 inconsistent-winding edges, no degenerate triangles, and one
connected component. The test now locks those observed source-tier diagnostics and
explicitly rejects a closed-two-manifold claim. Deterministic regeneration matches
the packaged artifact exactly.

The base-tier regression first failed at the unimplemented preprocessing boundary:

```text
ImportError: cannot import name 'build_base_anatomy_asset'
```

After adding isolated temporary Blender materialization, Voxel Remesh, collapse
decimation, canonical ordering, topology rejection, and source-deviation reporting,
two independent builds produced exactly equal data and matched the packaged base
artifact.

The registry-authority regressions first failed at the absent lookup and injection
boundaries:

```text
AttributeError: 'RoleRegistry' object has no attribute 'require'
TypeError: run_generate() got an unexpected keyword argument 'role_registry'
```

The real-catalog regression then failed at the absent packaged loader:

```text
ImportError: cannot import name 'load_anatomy_catalog'
```

After the cleanup, a substituted registry changes generated plan names and deform
flags without application edits, and the packaged catalog validates its source,
driver, artifact tier, topology IDs, and provenance.

The new registry corruption tests passed immediately against the validator added in
the preceding increment, confirming that each existing fail-fast branch is now
covered. The catalog test failed at the missing versioned sentinel declaration:

```text
KeyError: 'surface_region_all_sentinel'
```

After declaring the sentinel in schema version 1 and consuming that declaration in
both catalog validators, all five focused catalog tests passed.

## Commands And Results

```powershell
& "tests\run_milestone2.ps1" -MsHumanSource "<pinned-ms_human_700-path>"
```

- All seven focused role-registry tests pass, including every corruption branch.
- The focused semantic-mapping test passes.
- All four source-manifest tests pass, including exact regeneration from the pinned
  source checkout.
- All five catalog-schema tests pass for valid fixtures, independent malformed
  references, ordered path/topology correspondence, and artifact-backed sentinel
  behavior.
- All four anatomy conversion tests pass for source and base topology, provenance,
  deviation bounds, and exact deterministic regeneration from the pinned source.
- All eight Milestone 1 Blender-headless behavior tests pass, including substituted
  registry authority over generated plan metadata.
- Extension source and ZIP validation pass.
- The isolated installed Extension loads the registry, semantic mappings, and the
  complete source/entity/declaration inventory, catalog schema, and validators.
- The isolated installed Extension loads both packaged humerus topology tiers.
- Install, enable, disable, re-enable, uninstall, and post-uninstall checks pass.

## Changed Files

- `src/rigged_anatomy/blender_manifest.toml`
- `src/rigged_anatomy/role_registry.py`
- `src/rigged_anatomy/semantic_mappings.py`
- `src/rigged_anatomy/data/role-registry-v1.json`
- `src/rigged_anatomy/data/vrm-1.0-mapping-v1.json`
- `src/rigged_anatomy/data/humanik-fbx-2020-mapping-v1.json`
- `src/rigged_anatomy/source_manifest.py`
- `src/rigged_anatomy/data/ms-human-700-source-v1.json`
- `src/rigged_anatomy/catalogs.py`
- `src/rigged_anatomy/data/catalog-schema-v1.json`
- `src/rigged_anatomy/data/anatomy-catalog-v1.json`
- `src/rigged_anatomy/anatomy_assets.py`
- `src/rigged_anatomy/data/anatomy/humerus-source-v1.json`
- `src/rigged_anatomy/data/anatomy/humerus-base-v1.json`
- `src/rigged_anatomy/licenses/Apache-2.0.txt`
- `src/rigged_anatomy/licenses/MS-Human-700-NOTICE.txt`
- `tools/convert_anatomy_asset.py`
- `tools/inventory_ms_human_700.py`
- `tests/headless/test_role_registry.py`
- `tests/headless/test_semantic_mappings.py`
- `tests/headless/test_installed_lifecycle.py`
- `tests/headless/test_source_manifest.py`
- `tests/headless/test_catalog_schemas.py`
- `tests/headless/test_anatomy_asset_conversion.py`
- `tests/run_milestone2.ps1`
- `docs/verification/milestone-2.md`
- `docs/research/rigging-standards-and-ms-human-700.md`
- `docs/decisions/round-1-planning-interview.md`
- `docs/project-state.md`
- `jumpstart.md`

## Remaining Scope

Further asset conversion, catalog population, fitting, containment, morphology,
scale behavior, and approved source-rest validation thresholds remain later
Milestone 2 work. Milestone 3 rig behavior remains unauthorized.
