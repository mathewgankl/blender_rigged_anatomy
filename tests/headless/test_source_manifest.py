# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

from rigged_anatomy.source_manifest import load_source_manifest
from tools.inventory_ms_human_700 import build_manifest


EXPECTED_XML_PATHS = {
    "MS-Human-700.xml",
    "assets/asset/Asset_Lowerbody.xml",
    "assets/asset/Asset_Others.xml",
    "assets/asset/Asset_Torso.xml",
    "assets/asset/Asset_Upperbody.xml",
    "assets/body_primary/Body_Leg_Foot_l.xml",
    "assets/body_primary/Body_Leg_Foot_r.xml",
    "assets/body_primary/Body_Arm_l.xml",
    "assets/body_primary/Body_Arm_r.xml",
    "assets/body_primary/Body_Torso_Simple.xml",
    "assets/contact/Contact_Lowerbody.xml",
    "assets/equality/Equality_Lowerbody.xml",
    "assets/equality/Equality_Upperbody.xml",
    "assets/muscle/Muscle_Arm_l.xml",
    "assets/muscle/Muscle_Arm_r.xml",
    "assets/muscle/Muscle_Leg_l.xml",
    "assets/muscle/Muscle_Leg_r.xml",
    "assets/muscle/Muscle_Torso.xml",
    "assets/tendon/Tendon_Arm_l.xml",
    "assets/tendon/Tendon_Arm_r.xml",
    "assets/tendon/Tendon_Leg_l.xml",
    "assets/tendon/Tendon_Leg_r.xml",
    "assets/tendon/Tendon_Torso.xml",
}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class SourceManifestTests(unittest.TestCase):
    def test_manifest_has_closed_source_inventory(self):
        manifest = load_source_manifest()

        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(
            manifest["source_revision"],
            "8161bba264d7fa7c99ca301e91e7fb44737676ad",
        )
        self.assertEqual(manifest["source_license"], "Apache-2.0")
        self.assertEqual(manifest["root_model"], "MS-Human-700.xml")
        self.assertEqual(
            {entry["path"] for entry in manifest["xml_files"]}, EXPECTED_XML_PATHS
        )
        self.assertEqual(
            len({entry["source_key"] for entry in manifest["resources"]}),
            len(manifest["resources"]),
        )
        for entry in (*manifest["xml_files"], *manifest["resources"]):
            self.assertRegex(entry["sha256"], SHA256_PATTERN)
        self.assertEqual(
            {
                entry["source_key"]
                for entry in manifest["resources"]
                if entry["disposition"] == "ignored"
            },
            {
                "texture:marblecube",
                "mesh:waterbottle",
                "mesh:waterbottle_contact0",
                "mesh:waterbottle_contact1",
            },
        )

    def test_manifest_matches_pinned_source_when_available(self):
        source_root = os.environ.get("RA_MS_HUMAN_700_SOURCE")
        if source_root is None:
            self.skipTest("Pinned ms_human_700 source is not available.")

        self.assertEqual(build_manifest(Path(source_root)), load_source_manifest())

    def test_domain_entities_have_exact_catalog_mappings(self):
        manifest = load_source_manifest()
        bodies = manifest["bodies"]
        paths = manifest["tendon_paths"]
        muscles = manifest["muscle_actuators"]

        self.assertEqual(len(bodies), 80)
        self.assertEqual(len(paths), 700)
        self.assertEqual(len(muscles), 700)
        for entries in (bodies, paths, muscles):
            self.assertEqual(
                len({entry["source_key"] for entry in entries}), len(entries)
            )
            self.assertTrue(
                all(entry["catalog_key"] == entry["source_key"] for entry in entries)
            )

        elements = [element for path in paths for element in path["elements"]]
        self.assertEqual(sum(element["kind"] == "site" for element in elements), 2576)
        self.assertEqual(sum(element["kind"] == "wrap" for element in elements), 252)
        self.assertEqual(
            {muscle["tendon"] for muscle in muscles},
            {path["name"] for path in paths},
        )

        for resource in manifest["resources"]:
            if resource["disposition"] == "retain":
                self.assertEqual(resource["catalog_key"], resource["source_key"])
            else:
                self.assertIsNone(resource["catalog_key"])

    def test_tendon_references_resolve_to_owned_source_declarations(self):
        manifest = load_source_manifest()
        sites = manifest["attachment_sites"]
        wraps = manifest["wrapping_geometries"]
        paths = manifest["tendon_paths"]
        body_keys = {body["source_key"] for body in manifest["bodies"]}
        xml_paths = {entry["path"] for entry in manifest["xml_files"]}

        direct_site_refs = Counter(
            f"site:{element['ref']}"
            for path in paths
            for element in path["elements"]
            if element["kind"] == "site"
        )
        sidesite_refs = Counter(
            f"site:{element['sidesite']}"
            for path in paths
            for element in path["elements"]
            if element["kind"] == "wrap" and "sidesite" in element
        )
        wrap_refs = Counter(
            f"wrap:{element['ref']}"
            for path in paths
            for element in path["elements"]
            if element["kind"] == "wrap"
        )

        self.assertEqual(len(sites), 2756)
        self.assertEqual(len(wraps), 182)
        self.assertEqual(sum(direct_site_refs.values()), 2576)
        self.assertEqual(sum(sidesite_refs.values()), 240)
        self.assertEqual(sum(wrap_refs.values()), 252)
        self.assertEqual(
            {site["source_key"] for site in sites},
            set(direct_site_refs) | set(sidesite_refs),
        )
        self.assertEqual({wrap["source_key"] for wrap in wraps}, set(wrap_refs))
        self.assertEqual(len(sites), len({site["source_key"] for site in sites}))
        self.assertEqual(len(wraps), len({wrap["source_key"] for wrap in wraps}))

        for site in sites:
            self.assertIn("pos", site["attributes"])
            self.assertEqual(site["path_reference_count"], direct_site_refs[site["source_key"]])
            self.assertEqual(
                site["sidesite_reference_count"], sidesite_refs[site["source_key"]]
            )
        for wrap in wraps:
            self.assertEqual(wrap["attributes"]["class"], "wrap")
            self.assertIn("pos", wrap["attributes"])
            self.assertIn("size", wrap["attributes"])
            self.assertEqual(wrap["path_reference_count"], wrap_refs[wrap["source_key"]])

        for declaration in (*sites, *wraps):
            self.assertIn(declaration["owning_body_source_key"], body_keys)
            self.assertIn(declaration["declaration_path"], xml_paths)
            self.assertIsInstance(declaration["attributes"], dict)
            self.assertNotIn("name", declaration["attributes"])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
