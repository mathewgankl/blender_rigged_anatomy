# SPDX-License-Identifier: GPL-3.0-or-later

import json
import sys
import unittest
from pathlib import Path

import bmesh
import bpy


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.dont_write_bytecode = True

import rigged_anatomy
from rigged_anatomy.application import GenerateRequest, GenerateSettings, run_generate
from rigged_anatomy.blender_adapter import BlenderMaterializer


def valid_request():
    return GenerateRequest(
        target_name="SyntheticSkin",
        target_height=2.0,
        landmarks={
            "shoulder.L": (0.6, 0.0, 0.8),
            "palm.L": (0.9, 0.0, 0.2),
        },
        settings=GenerateSettings(),
    )


class ExtensionLifecycleTests(unittest.TestCase):
    def tearDown(self):
        rigged_anatomy.unregister()

    def test_register_and_unregister(self):
        rigged_anatomy.register()
        self.assertTrue(hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice"))

        rigged_anatomy.unregister()
        self.assertFalse(hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice"))


class VerticalSliceTests(unittest.TestCase):
    def tearDown(self):
        generated = bpy.data.collections.get("RA_Generated")
        if generated is not None:
            for obj in list(generated.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.collections.remove(generated)
        for name in ("SyntheticSkin", "ShoulderLandmark", "PalmLandmark"):
            obj = bpy.data.objects.get(name)
            if obj is not None:
                bpy.data.objects.remove(obj, do_unlink=True)
        for armature in list(bpy.data.armatures):
            if armature.users == 0:
                bpy.data.armatures.remove(armature)
        for mesh in list(bpy.data.meshes):
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        rigged_anatomy.unregister()

    def test_plan_is_canonical_json(self):
        first = run_generate(valid_request())
        second = run_generate(valid_request())

        self.assertTrue(first.ok, first.to_json())
        self.assertEqual(first.to_json(), second.to_json())
        payload = json.loads(first.to_json())
        self.assertEqual(payload["plan"]["schema_version"], 1)
        self.assertEqual(
            [bone["role"] for bone in payload["plan"]["bones"]],
            ["upper_arm.L", "forearm.L"],
        )
        self.assertEqual(payload["plan"]["bones"][1]["parent"], "upper_arm.L")
        self.assertEqual(payload["plan"]["bones"][0]["head"], [0.3, 0.0, 0.4])
        self.assertEqual(payload["plan"]["bones"][1]["tail"], [0.45, 0.0, 0.1])
        self.assertEqual(
            [driver["role"] for driver in payload["plan"]["anatomy_drivers"]],
            ["humerus.L", "radius.L", "ulna.L"],
        )

    def test_generation_requires_no_source_pose_category(self):
        request = valid_request()

        result = run_generate(request)

        self.assertTrue(result.ok, result.to_json())
        self.assertNotIn("source_pose", result.plan.to_dict())

    def test_plan_is_normalized_across_uniform_scale(self):
        baseline = run_generate(valid_request())
        scaled = valid_request()
        scaled.target_height *= 100
        scaled.landmarks = {
            role: tuple(component * 100 for component in location)
            for role, location in scaled.landmarks.items()
        }

        result = run_generate(scaled)

        self.assertTrue(result.ok, result.to_json())
        self.assertEqual(result.plan.to_json(), baseline.plan.to_json())
        self.assertEqual(result.plan.digest(), baseline.plan.digest())

    def test_malformed_input_returns_structured_errors(self):
        request = valid_request()
        request.landmarks.pop("palm.L")
        request.target_height = float("nan")

        result = run_generate(request)

        self.assertFalse(result.ok)
        self.assertIsNone(result.plan)
        self.assertEqual(
            [error.code for error in result.errors],
            ["invalid_target_height", "missing_landmark"],
        )
        self.assertIsNone(bpy.data.collections.get("RA_Generated"))

    def test_materialization_is_idempotent(self):
        materializer = BlenderMaterializer()

        first = run_generate(valid_request(), materializer)
        second = run_generate(valid_request(), materializer)

        self.assertTrue(first.ok, first.to_json())
        self.assertTrue(second.ok, second.to_json())
        generated = bpy.data.collections["RA_Generated"]
        self.assertEqual(
            sorted(obj.name for obj in generated.objects),
            [
                "RA_Anatomy_humerus.L",
                "RA_Anatomy_radius.L",
                "RA_Anatomy_ulna.L",
                "RA_LeftArm",
            ],
        )
        armature = generated.objects["RA_LeftArm"]
        self.assertEqual([bone.name for bone in armature.data.bones], ["DEF-upper_arm.L", "DEF-forearm.L"])
        self.assertEqual(armature["ra_plan_digest"], first.plan.digest())
        for role in ("humerus.L", "radius.L", "ulna.L"):
            anatomy = generated.objects[f"RA_Anatomy_{role}"]
            self.assertEqual(anatomy.type, "MESH")
            self.assertEqual(anatomy["ra_anatomy_role"], role)
            self.assertFalse(anatomy.data.validate(verbose=False, clean_customdata=False))
            mesh = bmesh.new()
            mesh.from_mesh(anatomy.data)
            self.assertTrue(all(edge.is_manifold for edge in mesh.edges))
            mesh.free()

    def test_operator_matches_headless_command(self):
        mesh = bpy.data.meshes.new("SyntheticSkin")
        mesh.from_pydata(
            [
                (-0.5, -0.5, -1.0),
                (0.5, -0.5, -1.0),
                (0.5, 0.5, -1.0),
                (-0.5, 0.5, -1.0),
                (-0.5, -0.5, 1.0),
                (0.5, -0.5, 1.0),
                (0.5, 0.5, 1.0),
                (-0.5, 0.5, 1.0),
            ],
            [],
            [
                (0, 1, 2, 3),
                (4, 7, 6, 5),
                (0, 4, 5, 1),
                (1, 5, 6, 2),
                (2, 6, 7, 3),
                (4, 0, 3, 7),
            ],
        )
        target = bpy.data.objects.new("SyntheticSkin", mesh)
        bpy.context.scene.collection.objects.link(target)
        for name, role, location in (
            ("ShoulderLandmark", "shoulder.L", (0.6, 0.0, 0.8)),
            ("PalmLandmark", "palm.L", (0.9, 0.0, 0.2)),
        ):
            landmark = bpy.data.objects.new(name, None)
            landmark["ra_landmark_role"] = role
            landmark.location = location
            bpy.context.scene.collection.objects.link(landmark)
        bpy.context.view_layer.objects.active = target
        target.select_set(True)
        rigged_anatomy.register()
        operator_type = bpy.types.RIGGED_ANATOMY_OT_generate_vertical_slice

        expected = run_generate(valid_request()).to_json()
        operator_result = bpy.ops.rigged_anatomy.generate_vertical_slice()

        self.assertEqual(operator_result, {"FINISHED"})
        self.assertNotIn("source_pose", operator_type.bl_rna.properties)
        self.assertEqual(bpy.context.scene["ra_last_result"], expected)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
