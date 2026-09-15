# SPDX-License-Identifier: GPL-3.0-or-later

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

from rigged_anatomy import role_registry
from rigged_anatomy.role_registry import load_role_registry


AXIAL_ROLES = ("root", "hips", "spine", "chest", "upper_chest", "neck", "head")
BILATERAL_ROLES = (
    "clavicle",
    "scapula",
    "upper_arm",
    "forearm",
    "hand",
    "thigh",
    "shin",
    "foot",
    "toe",
)
FINGER_CHAINS = {
    "thumb": ("metacarpal", "proximal", "distal"),
    "index": ("proximal", "intermediate", "distal"),
    "middle": ("proximal", "intermediate", "distal"),
    "ring": ("proximal", "intermediate", "distal"),
    "little": ("proximal", "intermediate", "distal"),
}


def expected_roles():
    roles = set(AXIAL_ROLES)
    for side in ("L", "R"):
        roles.update(f"{stem}.{side}" for stem in BILATERAL_ROLES)
        for finger, segments in FINGER_CHAINS.items():
            roles.update(f"{finger}_{segment}.{side}" for segment in segments)
    return roles


def expected_parents():
    parents = {
        "root": None,
        "hips": "root",
        "spine": "hips",
        "chest": "spine",
        "upper_chest": "chest",
        "neck": "upper_chest",
        "head": "neck",
    }
    for side in ("L", "R"):
        parents.update(
            {
                f"clavicle.{side}": "upper_chest",
                f"scapula.{side}": f"clavicle.{side}",
                f"upper_arm.{side}": f"scapula.{side}",
                f"forearm.{side}": f"upper_arm.{side}",
                f"hand.{side}": f"forearm.{side}",
                f"thigh.{side}": "hips",
                f"shin.{side}": f"thigh.{side}",
                f"foot.{side}": f"shin.{side}",
                f"toe.{side}": f"foot.{side}",
            }
        )
        for finger, segments in FINGER_CHAINS.items():
            parent = f"hand.{side}"
            for segment in segments:
                role = f"{finger}_{segment}.{side}"
                parents[role] = parent
                parent = role
    return parents


class RoleRegistryTests(unittest.TestCase):
    def assert_registry_rejected(self, payload, message):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "role-registry.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with patch.object(role_registry, "REGISTRY_PATH", path):
                with self.assertRaisesRegex(ValueError, message):
                    load_role_registry()

    def registry_payload(self):
        return json.loads(role_registry.REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_has_exact_roles_and_required_metadata(self):
        registry = load_role_registry()
        roles = {role.id: role for role in registry.roles}

        self.assertEqual(registry.schema_version, 1)
        self.assertEqual(set(roles), expected_roles())
        self.assertEqual(len(roles), len(registry.roles))
        self.assertEqual(
            {role.id: role.parent for role in registry.roles}, expected_parents()
        )
        self.assertEqual(len({role.generated_name for role in registry.roles}), len(roles))

        for role in registry.roles:
            expected_side = role.id.rpartition(".")[2]
            if expected_side not in {"L", "R"}:
                expected_side = None
            self.assertEqual(role.side, expected_side)
            self.assertEqual(
                role.generated_name,
                "root" if role.id == "root" else f"DEF-{role.id}",
            )
            self.assertEqual(role.deform, role.id != "root")

        self.assertEqual(registry.require("upper_arm.L").generated_name, "DEF-upper_arm.L")
        with self.assertRaisesRegex(KeyError, "Unknown canonical role"):
            registry.require("source:humerus")

    def test_registry_rejects_unsupported_schema(self):
        payload = self.registry_payload()
        payload["schema_version"] = 2

        self.assert_registry_rejected(payload, "schema version must be 1")

    def test_registry_rejects_duplicate_role_ids(self):
        payload = self.registry_payload()
        payload["roles"].append(deepcopy(payload["roles"][-1]))

        self.assert_registry_rejected(payload, "role IDs must be unique")

    def test_registry_rejects_duplicate_generated_names(self):
        payload = self.registry_payload()
        payload["roles"][1]["generated_name"] = payload["roles"][0]["generated_name"]

        self.assert_registry_rejected(payload, "role names must be unique")

    def test_registry_rejects_missing_parent(self):
        payload = self.registry_payload()
        payload["roles"][1]["parent"] = "missing"

        self.assert_registry_rejected(payload, "Unknown parent role for hips: missing")

    def test_registry_rejects_hierarchy_cycle(self):
        payload = self.registry_payload()
        payload["roles"][1]["parent"] = "spine"

        self.assert_registry_rejected(payload, "hierarchy contains a cycle")

    def test_registry_rejects_side_and_id_mismatches(self):
        for role_id, side in (("upper_arm.L", "R"), ("hips", "L")):
            with self.subTest(role_id=role_id, side=side):
                payload = self.registry_payload()
                role = next(role for role in payload["roles"] if role["id"] == role_id)
                role["side"] = side

                self.assert_registry_rejected(payload, "side does not match its ID")


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
