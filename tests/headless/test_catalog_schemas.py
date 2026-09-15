# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

from rigged_anatomy.catalogs import (
    load_anatomy_catalog,
    load_catalog_schema,
    validate_anatomy_catalog,
    validate_relationship_catalog,
)
from rigged_anatomy.source_manifest import load_source_manifest


def provenance_for(source_key):
    manifest = load_source_manifest()
    resources = {entry["source_key"]: entry for entry in manifest["resources"]}
    if source_key in resources:
        source = resources[source_key]
        source_path = source["path"]
        digest = source["sha256"]
    else:
        entities = {
            entry["source_key"]: entry
            for collection in ("bodies", "tendon_paths", "muscle_actuators")
            for entry in manifest[collection]
        }
        source_path = entities[source_key]["declaration_path"]
        digest = {
            entry["path"]: entry["sha256"] for entry in manifest["xml_files"]
        }[source_path]
    return {
        "repository": manifest["source_repository"],
        "revision": manifest["source_revision"],
        "source_path": source_path,
        "sha256": digest,
        "license": manifest["source_license"],
    }


def valid_anatomy_catalog():
    return deepcopy(load_anatomy_catalog())


def valid_relationship_catalog():
    source_path = next(
        entry
        for entry in load_source_manifest()["tendon_paths"]
        if entry["source_key"] == "path:BIClong_r_tendon"
    )
    return {
        "schema_version": 1,
        "entries": [
            {
                "id": "path:BIClong_r_tendon",
                "source_key": "path:BIClong_r_tendon",
                "muscle_source_keys": ["muscle:BIClong_r"],
                "driver_roles": ["upper_arm.R", "forearm.R"],
                "impact_band": "primary_visible",
                "path_points": [
                    {
                        "id": f"path:BIClong_r_tendon:{index:03d}",
                        "source_element": source_element,
                        "surface_ref": {
                            "anatomy_id": "mesh:humerus",
                            "anatomy_role": "humerus.R",
                            "region_id": "whole_surface",
                            "triangle_id": 0,
                            "vertex_ids": [0, 1, 2],
                            "barycentric": [0.2, 0.3, 0.5],
                            "bone_local_fallback": [0.0, 0.0, 0.0],
                        },
                    }
                    for index, source_element in enumerate(source_path["elements"])
                ],
                "provenance": provenance_for("path:BIClong_r_tendon"),
            }
        ],
    }


class CatalogSchemaTests(unittest.TestCase):
    def test_valid_catalogs_satisfy_versioned_schema(self):
        schema = load_catalog_schema()

        self.assertEqual(schema["schema_version"], 1)
        self.assertEqual(
            schema["impact_bands"],
            ["primary_visible", "secondary_visible", "deep_stabilizing"],
        )
        self.assertEqual(schema["anatomy"]["surface_region_all_sentinel"], "all")
        anatomy = valid_anatomy_catalog()
        self.assertEqual(validate_anatomy_catalog(anatomy), ())
        self.assertEqual(
            validate_relationship_catalog(valid_relationship_catalog(), anatomy), ()
        )

    def test_malformed_catalogs_report_independent_reference_errors(self):
        anatomy = valid_anatomy_catalog()
        anatomy["entries"][0]["source_key"] = "mesh:missing"
        anatomy["entries"][0]["driver_role"] = "missing_role.L"
        anatomy["entries"][0]["provenance"] = {}

        anatomy_issues = validate_anatomy_catalog(anatomy)

        self.assertEqual(
            {issue.code for issue in anatomy_issues},
            {
                "unknown_source_key",
                "unknown_driver_role",
                "artifact_source_mismatch",
                "provenance_mismatch",
            },
        )

        valid_anatomy = valid_anatomy_catalog()
        relationship = valid_relationship_catalog()
        entry = relationship["entries"][0]
        entry["source_key"] = "path:missing"
        entry["muscle_source_keys"] = ["muscle:missing"]
        entry["driver_roles"] = ["missing_role.L"]
        entry["impact_band"] = "unclassified"
        entry["path_points"][0]["surface_ref"]["anatomy_id"] = "mesh:missing"
        entry["provenance"] = {}

        relationship_issues = validate_relationship_catalog(relationship, valid_anatomy)

        self.assertEqual(
            {issue.code for issue in relationship_issues},
            {
                "unknown_source_key",
                "unknown_muscle_source",
                "unknown_driver_role",
                "invalid_impact_band",
                "unknown_anatomy_reference",
                "provenance_mismatch",
            },
        )

    def test_all_surface_region_sentinel_requires_a_packaged_artifact(self):
        anatomy = valid_anatomy_catalog()
        anatomy["entries"][0]["artifact"]["topology_tier"] = "missing"

        self.assertEqual(
            {issue.code for issue in validate_anatomy_catalog(anatomy)},
            {"unknown_artifact", "invalid_surface_topology_reference"},
        )
        self.assertEqual(
            {
                issue.code
                for issue in validate_relationship_catalog(
                    valid_relationship_catalog(), anatomy
                )
            },
            {"unknown_triangle_reference", "unknown_vertex_reference"},
        )

    def test_surface_region_rejects_an_undeclared_sentinel(self):
        anatomy = valid_anatomy_catalog()
        anatomy["entries"][0]["surface_regions"][0]["vertex_ids"] = "everything"

        self.assertEqual(
            {issue.code for issue in validate_anatomy_catalog(anatomy)},
            {"invalid_surface_topology_reference"},
        )

    def test_relationship_path_and_surface_correspondence_are_closed(self):
        anatomy = valid_anatomy_catalog()
        relationship = valid_relationship_catalog()
        entry = relationship["entries"][0]
        entry["muscle_source_keys"].append("muscle:APL_r")
        entry["path_points"][0]["source_element"] = {
            "kind": "site",
            "ref": "missing-site",
        }
        surface_ref = entry["path_points"][1]["surface_ref"]
        surface_ref["anatomy_role"] = "radius.L"
        surface_ref["region_id"] = "missing-region"
        surface_ref["triangle_id"] = 99
        surface_ref["vertex_ids"] = [0, 1, 99]
        surface_ref["barycentric"] = [0.2, 0.3, 0.4]

        issues = validate_relationship_catalog(relationship, anatomy)

        self.assertEqual(
            {issue.code for issue in issues},
            {
                "muscle_path_mismatch",
                "source_path_mismatch",
                "anatomy_role_mismatch",
                "unknown_surface_region",
                "unknown_triangle_reference",
                "unknown_vertex_reference",
                "invalid_barycentric",
            },
        )


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
