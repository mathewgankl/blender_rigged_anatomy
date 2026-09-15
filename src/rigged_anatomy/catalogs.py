# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping

from .anatomy_assets import load_anatomy_asset
from .role_registry import load_role_registry
from .source_manifest import load_source_manifest


SCHEMA_PATH = Path(__file__).with_name("data") / "catalog-schema-v1.json"
ANATOMY_CATALOG_PATH = Path(__file__).with_name("data") / "anatomy-catalog-v1.json"


@dataclass(frozen=True)
class CatalogIssue:
    code: str
    subject: str
    message: str


def load_catalog_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_anatomy_catalog() -> dict[str, object]:
    return json.loads(ANATOMY_CATALOG_PATH.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class _SourceIndex:
    all: dict[str, Mapping[str, object]]
    anatomy: set[str]
    paths: dict[str, Mapping[str, object]]
    muscles: dict[str, Mapping[str, object]]
    xml_hashes: dict[str, str]
    repository: str
    revision: str
    license: str

    def expected_provenance(self, source_key: object) -> dict[str, object] | None:
        if not isinstance(source_key, str) or source_key not in self.all:
            return None
        source = self.all[source_key]
        if "sha256" in source:
            source_path = source["path"]
            digest = source["sha256"]
        else:
            source_path = source["declaration_path"]
            digest = self.xml_hashes[source_path]
        return {
            "repository": self.repository,
            "revision": self.revision,
            "source_path": source_path,
            "sha256": digest,
            "license": self.license,
        }


def _source_index() -> _SourceIndex:
    manifest = load_source_manifest()
    resources = {
        entry["source_key"]: entry
        for entry in manifest["resources"]
        if entry["disposition"] == "retain"
    }
    bodies = {entry["source_key"]: entry for entry in manifest["bodies"]}
    paths = {entry["source_key"]: entry for entry in manifest["tendon_paths"]}
    muscles = {entry["source_key"]: entry for entry in manifest["muscle_actuators"]}
    return _SourceIndex(
        all=resources | bodies | paths | muscles,
        anatomy=set(resources) | set(bodies),
        paths=paths,
        muscles=muscles,
        xml_hashes={entry["path"]: entry["sha256"] for entry in manifest["xml_files"]},
        repository=manifest["source_repository"],
        revision=manifest["source_revision"],
        license=manifest["source_license"],
    )


def _catalog_entries(
    catalog: Mapping[str, object], kind: str, issues: list[CatalogIssue]
) -> list[Mapping[str, object]]:
    schema = load_catalog_schema()
    if catalog.get("schema_version") != schema["schema_version"]:
        issues.append(
            CatalogIssue("unsupported_schema", kind, "Catalog schema version must be 1.")
        )
    entries = catalog.get("entries")
    if not isinstance(entries, list):
        issues.append(CatalogIssue("invalid_entries", kind, "Catalog entries must be a list."))
        return []
    required = set(schema[kind]["required_entry_fields"])
    valid_entries = []
    for index, entry in enumerate(entries):
        subject = (
            str(entry.get("id", index)) if isinstance(entry, Mapping) else str(index)
        )
        if not isinstance(entry, Mapping):
            issues.append(CatalogIssue("invalid_entry", subject, "Catalog entry must be an object."))
            continue
        for field in sorted(required - set(entry)):
            issues.append(
                CatalogIssue("missing_field", subject, f"Missing required field {field}.")
            )
        valid_entries.append(entry)
    ids = [entry.get("id") for entry in valid_entries if isinstance(entry.get("id"), str)]
    if len(ids) != len(set(ids)):
        issues.append(CatalogIssue("duplicate_id", kind, "Catalog entry IDs must be unique."))
    return valid_entries


def _validate_driver_roles(
    roles: object, subject: str, role_ids: set[str], issues: list[CatalogIssue]
) -> None:
    values = roles if isinstance(roles, list) else [roles]
    for role in values:
        if role not in role_ids:
            issues.append(
                CatalogIssue(
                    "unknown_driver_role",
                    str(role),
                    f"{subject} references an unknown driver role.",
                )
            )


def _missing_fields(
    value: object, required: set[str], subject: str, issues: list[CatalogIssue]
) -> bool:
    if not isinstance(value, Mapping):
        issues.append(CatalogIssue("invalid_entry", subject, "Expected an object."))
        return True
    for field in sorted(required - set(value)):
        issues.append(CatalogIssue("missing_field", subject, f"Missing required field {field}."))
    return False


def _is_vector(value: object, length: int) -> bool:
    return (
        isinstance(value, list)
        and len(value) == length
        and all(isinstance(component, (int, float)) for component in value)
    )


def validate_anatomy_catalog(catalog: Mapping[str, object]) -> tuple[CatalogIssue, ...]:
    issues: list[CatalogIssue] = []
    entries = _catalog_entries(catalog, "anatomy", issues)
    sources = _source_index()
    role_ids = {role.id for role in load_role_registry().roles}
    anatomy_schema = load_catalog_schema()["anatomy"]
    region_required = set(anatomy_schema["required_surface_region_fields"])
    artifact_required = set(anatomy_schema["required_artifact_fields"])
    all_sentinel = anatomy_schema["surface_region_all_sentinel"]
    for entry in entries:
        subject = str(entry.get("id", ""))
        source_key = entry.get("source_key")
        if source_key not in sources.anatomy:
            issues.append(
                CatalogIssue(
                    "unknown_source_key",
                    str(source_key),
                    f"{subject} references an unknown anatomy source.",
                )
            )
        _validate_driver_roles(entry.get("driver_role"), subject, role_ids, issues)
        artifact_ref = entry.get("artifact")
        asset = None
        if not _missing_fields(artifact_ref, artifact_required, subject, issues):
            try:
                asset = load_anatomy_asset(
                    artifact_ref.get("asset_id"), artifact_ref.get("topology_tier")
                )
            except (KeyError, ValueError):
                issues.append(
                    CatalogIssue(
                        "unknown_artifact",
                        subject,
                        "Anatomy entry references an unknown packaged asset tier.",
                    )
                )
            else:
                if asset["asset_id"] != source_key:
                    issues.append(
                        CatalogIssue(
                            "artifact_source_mismatch",
                            subject,
                            "Packaged asset ID must match the anatomy source key.",
                        )
                    )
                if asset["topology_tier"] != entry.get("topology_tier"):
                    issues.append(
                        CatalogIssue(
                            "artifact_tier_mismatch",
                            subject,
                            "Packaged asset tier must match the catalog topology tier.",
                        )
                    )
        regions = entry.get("surface_regions", [])
        region_ids = []
        if not isinstance(regions, list):
            issues.append(
                CatalogIssue("invalid_surface_regions", subject, "Surface regions must be a list.")
            )
        else:
            for index, region in enumerate(regions):
                region_subject = f"{subject}.surface_regions[{index}]"
                if _missing_fields(region, region_required, region_subject, issues):
                    continue
                region_id = region.get("id")
                if isinstance(region_id, str):
                    region_ids.append(region_id)
                else:
                    issues.append(
                        CatalogIssue(
                            "invalid_surface_region_id",
                            region_subject,
                            "Surface region ID must be a string.",
                        )
                    )
                for field, count_field in (
                    ("vertex_ids", "vertex_count"),
                    ("triangle_ids", "triangle_count"),
                ):
                    references = region.get(field)
                    if references == all_sentinel and asset is not None:
                        continue
                    count = asset["topology"][count_field] if asset is not None else 0
                    if not (
                        isinstance(references, list)
                        and all(
                            isinstance(reference, int) and 0 <= reference < count
                            for reference in references
                        )
                        and len(references) == len(set(references))
                    ):
                        issues.append(
                            CatalogIssue(
                                "invalid_surface_topology_reference",
                                region_subject,
                                f"{field} must reference packaged artifact IDs.",
                            )
                        )
        if len(region_ids) != len(set(region_ids)):
            issues.append(
                CatalogIssue("duplicate_surface_region", subject, "Surface region IDs must be unique.")
            )
        if entry.get("provenance") != sources.expected_provenance(source_key):
            issues.append(
                CatalogIssue(
                    "provenance_mismatch",
                    subject,
                    "Provenance must match the pinned source manifest.",
                )
            )
    return tuple(issues)


def validate_relationship_catalog(
    catalog: Mapping[str, object], anatomy_catalog: Mapping[str, object]
) -> tuple[CatalogIssue, ...]:
    issues: list[CatalogIssue] = []
    entries = _catalog_entries(catalog, "relationship", issues)
    sources = _source_index()
    role_ids = {role.id for role in load_role_registry().roles}
    schema = load_catalog_schema()
    all_sentinel = schema["anatomy"]["surface_region_all_sentinel"]
    anatomy_entries = anatomy_catalog.get("entries", [])
    anatomy_by_id = {
        entry["id"]: entry
        for entry in anatomy_entries
        if isinstance(entry, Mapping) and isinstance(entry.get("id"), str)
    }
    anatomy_assets_by_id = {}
    for anatomy_id, anatomy_entry in anatomy_by_id.items():
        artifact = anatomy_entry.get("artifact", {})
        try:
            anatomy_assets_by_id[anatomy_id] = load_anatomy_asset(
                artifact.get("asset_id"), artifact.get("topology_tier")
            )
        except (AttributeError, KeyError, ValueError):
            pass
    point_required = set(schema["relationship"]["required_path_point_fields"])
    surface_required = set(schema["relationship"]["required_surface_ref_fields"])
    for entry in entries:
        subject = str(entry.get("id", ""))
        source_key = entry.get("source_key")
        if source_key not in sources.paths:
            issues.append(
                CatalogIssue(
                    "unknown_source_key",
                    str(source_key),
                    f"{subject} references an unknown tendon path.",
                )
            )
        muscles = entry.get("muscle_source_keys", [])
        muscles = muscles if isinstance(muscles, list) else []
        for muscle in muscles:
            if muscle not in sources.muscles:
                issues.append(
                    CatalogIssue(
                        "unknown_muscle_source",
                        str(muscle),
                        f"{subject} references an unknown muscle actuator.",
                    )
                )
            elif source_key != f"path:{sources.muscles[muscle]['tendon']}":
                issues.append(
                    CatalogIssue(
                        "muscle_path_mismatch",
                        str(muscle),
                        f"{subject} does not use the actuator's source tendon.",
                    )
                )
        _validate_driver_roles(entry.get("driver_roles", []), subject, role_ids, issues)
        if entry.get("impact_band") not in schema["impact_bands"]:
            issues.append(
                CatalogIssue("invalid_impact_band", subject, "Relationship impact band is not supported.")
            )
        points = entry.get("path_points", [])
        points = points if isinstance(points, list) else []
        if source_key in sources.paths and [
            point.get("source_element") if isinstance(point, Mapping) else None
            for point in points
        ] != sources.paths[source_key]["elements"]:
            issues.append(
                CatalogIssue(
                    "source_path_mismatch",
                    subject,
                    "Path points must preserve all source elements in order.",
                )
            )
        point_ids = []
        for index, point in enumerate(points):
            point_subject = f"{subject}.path_points[{index}]"
            if _missing_fields(point, point_required, point_subject, issues):
                continue
            point_id = point.get("id")
            if isinstance(point_id, str):
                point_ids.append(point_id)
            else:
                issues.append(
                    CatalogIssue(
                        "invalid_path_point_id",
                        point_subject,
                        "Path point ID must be a string.",
                    )
                )
            surface = point.get("surface_ref")
            if _missing_fields(surface, surface_required, point_subject, issues):
                continue
            anatomy_id = surface.get("anatomy_id")
            if anatomy_id not in anatomy_by_id:
                issues.append(
                    CatalogIssue(
                        "unknown_anatomy_reference",
                        str(anatomy_id),
                        f"{point_subject} references unknown anatomy.",
                    )
                )
                continue
            if surface.get("anatomy_role") != anatomy_by_id[anatomy_id].get(
                "anatomy_role"
            ):
                issues.append(
                    CatalogIssue(
                        "anatomy_role_mismatch",
                        str(surface.get("anatomy_role")),
                        f"{point_subject} does not match the referenced anatomy role.",
                    )
                )
            regions = {
                region.get("id"): region
                for region in anatomy_by_id[anatomy_id].get("surface_regions", [])
                if isinstance(region, Mapping)
            }
            region = regions.get(surface.get("region_id"))
            if region is None:
                issues.append(
                    CatalogIssue(
                        "unknown_surface_region",
                        str(surface.get("region_id")),
                        f"{point_subject} references an unknown surface region.",
                    )
                )
            anatomy_asset = anatomy_assets_by_id.get(anatomy_id)
            triangle_ids = region.get("triangle_ids", []) if region else []
            triangle_id = surface.get("triangle_id")
            triangle_known = (
                isinstance(triangle_id, int)
                and triangle_ids == all_sentinel
                and anatomy_asset is not None
                and 0 <= triangle_id < anatomy_asset["topology"]["triangle_count"]
            ) or triangle_id in (triangle_ids if isinstance(triangle_ids, list) else [])
            if not triangle_known:
                issues.append(
                    CatalogIssue(
                        "unknown_triangle_reference",
                        str(surface.get("triangle_id")),
                        f"{point_subject} references an unknown triangle.",
                    )
                )
            region_vertex_ids = region.get("vertex_ids", []) if region else []
            referenced_vertices = surface.get("vertex_ids", [])
            vertices_known = (
                isinstance(referenced_vertices, list)
                and len(referenced_vertices) == 3
                and all(isinstance(vertex_id, int) for vertex_id in referenced_vertices)
                and (
                    (
                        region_vertex_ids == all_sentinel
                        and anatomy_asset is not None
                        and all(
                            0 <= vertex_id < anatomy_asset["topology"]["vertex_count"]
                            for vertex_id in referenced_vertices
                        )
                    )
                    or (
                        isinstance(region_vertex_ids, list)
                        and set(referenced_vertices).issubset(region_vertex_ids)
                    )
                )
            )
            if not vertices_known:
                issues.append(
                    CatalogIssue(
                        "unknown_vertex_reference",
                        point_subject,
                        "Surface correspondence must reference three region vertices.",
                    )
                )
            barycentric = surface.get("barycentric")
            if not (
                _is_vector(barycentric, 3)
                and all(0.0 <= component <= 1.0 for component in barycentric)
                and abs(sum(barycentric) - 1.0) <= 1e-9
            ):
                issues.append(
                    CatalogIssue(
                        "invalid_barycentric",
                        point_subject,
                        "Barycentric coordinates must contain three weights summing to one.",
                    )
                )
            if not _is_vector(surface.get("bone_local_fallback"), 3):
                issues.append(
                    CatalogIssue(
                        "invalid_bone_local_fallback",
                        point_subject,
                        "Bone-local fallback must contain three numeric coordinates.",
                    )
                )
        if len(point_ids) != len(set(point_ids)):
            issues.append(CatalogIssue("duplicate_path_point", subject, "Path point IDs must be unique."))
        if entry.get("provenance") != sources.expected_provenance(source_key):
            issues.append(
                CatalogIssue(
                    "provenance_mismatch",
                    subject,
                    "Provenance must match the pinned source manifest.",
                )
            )
    return tuple(issues)
