# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

from rigged_anatomy.role_registry import load_role_registry
from rigged_anatomy.semantic_mappings import load_humanik_mapping, load_vrm_mapping


FINGER_CHAINS = {
    "thumb": ("metacarpal", "proximal", "distal"),
    "index": ("proximal", "intermediate", "distal"),
    "middle": ("proximal", "intermediate", "distal"),
    "ring": ("proximal", "intermediate", "distal"),
    "little": ("proximal", "intermediate", "distal"),
}


def expected_vrm_mapping():
    mapping = {
        "root": None,
        "hips": "hips",
        "spine": "spine",
        "chest": "chest",
        "upper_chest": "upperChest",
        "neck": "neck",
        "head": "head",
    }
    targets = {
        "clavicle": "Shoulder",
        "scapula": None,
        "upper_arm": "UpperArm",
        "forearm": "LowerArm",
        "hand": "Hand",
        "thigh": "UpperLeg",
        "shin": "LowerLeg",
        "foot": "Foot",
        "toe": "Toes",
    }
    for side, prefix in (("L", "left"), ("R", "right")):
        for role, target in targets.items():
            mapping[f"{role}.{side}"] = None if target is None else f"{prefix}{target}"
        for finger, segments in FINGER_CHAINS.items():
            for segment in segments:
                mapping[f"{finger}_{segment}.{side}"] = (
                    f"{prefix}{finger.title()}{segment.title()}"
                )
    return mapping


def expected_humanik_mapping():
    mapping = {
        "root": None,
        "hips": "eHips",
        "spine": "eWaist",
        "chest": "eChest",
        "upper_chest": "eSpine2",
        "neck": "eNeck",
        "head": "eHead",
    }
    targets = {
        "clavicle": "Collar",
        "scapula": None,
        "upper_arm": "Shoulder",
        "forearm": "Elbow",
        "hand": "Wrist",
        "thigh": "Hip",
        "shin": "Knee",
        "foot": "Ankle",
        "toe": "Foot",
    }
    for side, prefix in (("L", "Left"), ("R", "Right")):
        for role, target in targets.items():
            mapping[f"{role}.{side}"] = None if target is None else f"e{prefix}{target}"
        for finger, segments in FINGER_CHAINS.items():
            target_finger = "Pinky" if finger == "little" else finger.title()
            for index, segment in enumerate(segments):
                mapping[f"{finger}_{segment}.{side}"] = (
                    f"e{prefix}{target_finger}{chr(ord('A') + index)}"
                )
    return mapping


class SemanticMappingTests(unittest.TestCase):
    def test_manifests_have_exact_keys_roles_and_official_names(self):
        role_ids = {role.id for role in load_role_registry().roles}
        vrm = load_vrm_mapping()
        humanik = load_humanik_mapping()

        self.assertEqual(vrm.schema_version, 1)
        self.assertEqual(vrm.target, "VRM 1.0")
        self.assertEqual(
            vrm.source_version, "821c11b250d8c70d5804ee13431e42bee56ea9c0"
        )
        self.assertEqual(
            vrm.source_url,
            "https://github.com/vrm-c/vrm-specification/blob/821c11b250d8c70d5804ee13431e42bee56ea9c0/specification/VRMC_vrm-1.0/humanoid.md",
        )
        self.assertEqual(dict(vrm.mappings), expected_vrm_mapping())

        self.assertEqual(humanik.schema_version, 1)
        self.assertEqual(humanik.target, "HumanIK/FBX Character")
        self.assertEqual(humanik.source_version, "FBX SDK 2020")
        self.assertEqual(
            humanik.source_url,
            "https://help.autodesk.com/cloudhelp/2020/ENU/FBX-API-Reference/cpp_ref/class_fbx_character.html",
        )
        self.assertEqual(dict(humanik.mappings), expected_humanik_mapping())

        for manifest in (vrm, humanik):
            self.assertEqual(set(manifest.mappings), role_ids)
            supported = [target for target in manifest.mappings.values() if target]
            self.assertEqual(len(supported), len(set(supported)))
            self.assertEqual(
                {role for role, target in manifest.mappings.items() if target is None},
                {"root", "scapula.L", "scapula.R"},
            )


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    if not result.wasSuccessful():
        raise SystemExit(1)
