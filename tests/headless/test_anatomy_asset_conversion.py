# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

from rigged_anatomy.anatomy_assets import load_anatomy_asset
from rigged_anatomy.source_manifest import load_source_manifest
from tools.convert_anatomy_asset import build_anatomy_asset, build_base_anatomy_asset


class AnatomyAssetConversionTests(unittest.TestCase):
    def test_packaged_humerus_has_stable_topology_diagnostics_and_provenance(self):
        asset = load_anatomy_asset("mesh:humerus", "source")
        manifest = load_source_manifest()
        source = next(
            entry
            for entry in manifest["resources"]
            if entry["source_key"] == "mesh:humerus"
        )

        self.assertEqual(asset["schema_version"], 1)
        self.assertEqual(asset["asset_id"], "mesh:humerus")
        self.assertEqual(asset["topology_tier"], "source")
        self.assertEqual(asset["units"], "meter")
        self.assertEqual(asset["id_convention"], "zero_based_array_index")
        self.assertIn("Converted from binary STL", asset["modification_notice"])
        self.assertEqual(
            asset["provenance"],
            {
                "repository": manifest["source_repository"],
                "revision": manifest["source_revision"],
                "license": manifest["source_license"],
                "source_key": source["source_key"],
                "source_path": source["path"],
                "sha256": source["sha256"],
            },
        )

        vertices = asset["vertices"]
        triangles = asset["triangles"]
        topology = asset["topology"]
        self.assertEqual(topology["vertex_count"], len(vertices))
        self.assertEqual(topology["triangle_count"], len(triangles))
        self.assertTrue(
            all(
                len(triangle) == 3
                and all(0 <= vertex_id < len(vertices) for vertex_id in triangle)
                for triangle in triangles
            )
        )
        self.assertEqual(topology["vertex_count"], 309)
        self.assertEqual(topology["triangle_count"], 588)
        self.assertEqual(topology["boundary_edge_count"], 45)
        self.assertEqual(topology["non_manifold_edge_count"], 3)
        self.assertEqual(topology["inconsistent_winding_edge_count"], 2)
        self.assertEqual(topology["degenerate_triangle_count"], 0)
        self.assertEqual(topology["connected_component_count"], 1)
        self.assertFalse(topology["is_closed_two_manifold"])

    def test_packaged_humerus_matches_pinned_source_when_available(self):
        source_root = os.environ.get("RA_MS_HUMAN_700_SOURCE")
        if source_root is None:
            self.skipTest("Pinned ms_human_700 source is not available.")

        first = build_anatomy_asset(Path(source_root), "mesh:humerus")
        second = build_anatomy_asset(Path(source_root), "mesh:humerus")
        self.assertEqual(first, second)
        self.assertEqual(first, load_anatomy_asset("mesh:humerus", "source"))

    def test_packaged_base_humerus_is_generation_ready(self):
        asset = load_anatomy_asset("mesh:humerus", "base")
        topology = asset["topology"]

        self.assertEqual(asset["schema_version"], 1)
        self.assertEqual(asset["asset_id"], "mesh:humerus")
        self.assertEqual(asset["topology_tier"], "base")
        self.assertEqual(asset["processing"]["voxel_size_meters"], 0.002)
        self.assertEqual(asset["processing"]["target_triangle_count"], 600)
        self.assertEqual(topology["vertex_count"], 302)
        self.assertEqual(topology["triangle_count"], 600)
        self.assertTrue(topology["is_closed_two_manifold"])
        self.assertEqual(topology["boundary_edge_count"], 0)
        self.assertEqual(topology["non_manifold_edge_count"], 0)
        self.assertEqual(topology["inconsistent_winding_edge_count"], 0)
        self.assertEqual(topology["degenerate_triangle_count"], 0)
        self.assertEqual(topology["connected_component_count"], 1)
        self.assertLessEqual(asset["source_deviation"]["p95_meters"], 0.0005)
        self.assertLessEqual(asset["source_deviation"]["max_meters"], 0.0016)

    def test_packaged_base_humerus_matches_preprocessing_when_available(self):
        source_root = os.environ.get("RA_MS_HUMAN_700_SOURCE")
        if source_root is None:
            self.skipTest("Pinned ms_human_700 source is not available.")

        first = build_base_anatomy_asset(Path(source_root), "mesh:humerus")
        second = build_base_anatomy_asset(Path(source_root), "mesh:humerus")
        self.assertEqual(first, second)
        self.assertEqual(first, load_anatomy_asset("mesh:humerus", "base"))


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
