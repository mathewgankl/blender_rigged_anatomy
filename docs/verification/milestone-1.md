# Milestone 1 Verification

**Status:** REQUIRES REFRESH - SOURCE-REST CONTRACT AMENDED
**Date:** 2026-09-14
**Environment:** Windows, Blender 5.2.1 LTS, embedded Python 3.13.13
**Scope:** Round 1, Milestone 1 only

## Result

The recorded Harness and Vertical Slice checks passed for one unilateral left-arm
chain under the former categorical T/A input contract. The approved continuous
source-rest amendment invalidates that part of the evidence. No Milestone 2 asset
conversion, full fitting, or later rig behavior has started.

## Amendment Impact

On 2026-09-14, the user approved
`docs/decisions/source-rest-pose-contract.md`. Milestone 1 must remove the T/A
selector and categorical `source_pose` field, preserve the actual supported source
rest pose, and produce the same deterministic plan without requiring a category.
The lifecycle, materialization, and idempotence evidence remains useful, but this
record cannot support Milestone 1 approval until the implementation and tests are
refreshed and the complete gate passes again.

## Red-Green Evidence

The first headless run failed at the intended missing production boundary:

```text
ModuleNotFoundError: No module named 'rigged_anatomy'
```

After the minimal implementation, the focused suite passed. A tightened
materialization check then failed because only the armature existed; adding the
three synthetic anatomy islands made that check pass. An operator/headless
equivalence check also exposed Blender float32 coordinate storage. Canonical
normalized coordinates are now quantized to seven decimal places, safely inside
the approved `1e-4 H` tolerance, and both paths produce identical JSON.

## Pre-Amendment Evidence

| Criterion | Evidence |
|---|---|
| Extension ZIP lifecycle | Source and ZIP manifests validate; isolated install, enable, disable, re-enable, and uninstall checks pass. |
| Malformed input | Missing `palm.L` plus non-finite target height returns ordered structured errors and creates no generated collection. |
| Normalized plan | Canonical JSON contains normalized transforms; inputs scaled by `100` produce the same plan JSON and SHA-256 digest. |
| Shared command seam | The Blender operator and direct headless call return byte-identical structured JSON for equivalent inputs. |
| Materialization | A staged `RA_Generated` collection receives a two-bone deform armature and closed synthetic humerus, radius, and ulna meshes with role/driver metadata. |
| Idempotence | Running the same plan twice leaves one collection, one armature, two bones, and one mesh per anatomy role. |
| Deterministic fixture | The checked-in synthetic target and left shoulder/palm fixture drive all vertical-slice checks without external packages or private assets. |
| Amended source-rest contract | Not yet met. The current operator and rig plan still require and store `T` or `A`. |

## Final Command

```powershell
& "tests\run_milestone1.ps1"
```

Pre-amendment observed result:

- Six Blender-headless tests pass.
- Source manifest validation passes.
- Extension ZIP build and ZIP validation pass.
- `EXTENSION_LIFECYCLE_OK` is printed.
- `EXTENSION_UNINSTALL_OK` is printed.
- Temporary package and isolated Blender user resources are removed by the harness.

## Changed Files

- `.gitignore`
- `src/rigged_anatomy/blender_manifest.toml`
- `src/rigged_anatomy/__init__.py`
- `src/rigged_anatomy/application.py`
- `src/rigged_anatomy/blender_adapter.py`
- `tests/headless/test_vertical_slice.py`
- `tests/headless/test_installed_lifecycle.py`
- `tests/run_milestone1.ps1`
- `docs/project-state.md`
- `docs/verification/milestone-1.md`
- `jumpstart.md`

## Remaining Scope

Before this milestone can return to the approval gate, refresh the input schema,
operator, deterministic fixture, and structured validation tests for the continuous
source-rest contract and rerun this command.

The full ten-landmark contract, pinned anatomy assets, complete catalogs, fitting,
containment, morphology, and scale matrix belong to Milestone 2. Milestone 2 remains
unauthorized pending explicit approval of this evidence.
