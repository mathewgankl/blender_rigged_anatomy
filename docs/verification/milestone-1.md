# Milestone 1 Verification

**Status:** APPROVED
**Date:** 2026-09-14
**Environment:** Windows, Blender 5.2.1 LTS, embedded Python 3.13.13
**Scope:** Round 1, Milestone 1 only

## Result

The Harness and Vertical Slice checks pass for one unilateral left-arm chain under
the approved continuous source-rest contract. Generation requires no T/A category,
the canonical plan stores no categorical `source_pose`, and the Blender operator
exposes no pose selector. No Milestone 2 asset conversion, full fitting, or later
rig behavior has started.

## Amendment Result

On 2026-09-14, the user approved
`docs/decisions/source-rest-pose-contract.md`. The refreshed application contract,
plan, operator, and fixtures no longer require or store a T/A category. Actual
source-rest transforms and canonical T mapping remain Milestone 2 and Milestone 3
work under their approved ordering and gates.

## Red-Green Evidence

The source-rest regression first failed at the intended obsolete application
boundary:

```text
TypeError: GenerateSettings.__init__() missing 1 required positional argument: 'source_pose'
```

After removing the categorical field, validation branch, plan value, and operator
enum, the focused `test_generation_requires_no_source_pose_category` check passed.
The operator/headless test now invokes the operator without arguments and verifies
that its RNA properties contain no `source_pose` selector.

The original vertical-slice red-green work remains represented by the materialized
two-bone armature and three synthetic anatomy islands. Canonical normalized
coordinates remain quantized to seven decimal places, safely inside the approved
`1e-4 H` tolerance, and the operator and direct paths produce identical JSON.

## Current Evidence

| Criterion | Evidence |
|---|---|
| Extension ZIP lifecycle | Source and ZIP manifests validate; isolated install, enable, disable, re-enable, and uninstall checks pass. |
| Malformed input | Missing `palm.L` plus non-finite target height returns ordered structured errors and creates no generated collection. |
| Normalized plan | Canonical JSON contains normalized transforms; inputs scaled by `100` produce the same plan JSON and SHA-256 digest. |
| Shared command seam | The Blender operator and direct headless call return byte-identical structured JSON for equivalent inputs. |
| Materialization | A staged `RA_Generated` collection receives a two-bone deform armature and closed synthetic humerus, radius, and ulna meshes with role/driver metadata. |
| Idempotence | Running the same plan twice leaves one collection, one armature, two bones, and one mesh per anatomy role. |
| Deterministic fixture | The checked-in synthetic target and left shoulder/palm fixture drive all vertical-slice checks without external packages or private assets. |
| Amended source-rest contract | Direct and operator generation require no T/A input; the plan and operator RNA contain no `source_pose` field. |

## Final Command

```powershell
& "tests\run_milestone1.ps1"
```

Observed result on 2026-09-14:

- Seven Blender-headless tests pass.
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

The user approved this evidence and authorized Milestone 2 on 2026-09-14. The full
ten-landmark contract, source-rest validation thresholds, pinned anatomy assets,
role registry, complete catalogs, fitting, containment, morphology, and scale matrix
belong to Milestone 2.
