# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bpy
from mathutils import Vector

from .application import AnatomyDriverPlan, BonePlan, RigPlan


COLLECTION_NAME = "RA_Generated"
ARMATURE_NAME = "RA_LeftArm"


def _materialize_anatomy(
    collection: bpy.types.Collection,
    anatomy_plan: AnatomyDriverPlan,
    driver_plan: BonePlan,
    target_height: float,
) -> bpy.types.Object:
    head = Vector(driver_plan.head) * target_height
    tail = Vector(driver_plan.tail) * target_height
    direction = (tail - head).normalized()
    reference = Vector((0.0, 0.0, 1.0))
    if abs(direction.dot(reference)) > 0.9:
        reference = Vector((1.0, 0.0, 0.0))
    side = direction.cross(reference).normalized()
    normal = direction.cross(side).normalized()
    offset_sign = {"radius.L": 1.0, "ulna.L": -1.0}.get(anatomy_plan.role, 0.0)
    offset = side * target_height * 0.015 * offset_sign
    radius = target_height * 0.0125
    head += offset
    tail += offset
    center = (head + tail) / 2
    vertices = (
        head,
        tail,
        center + side * radius,
        center + normal * radius,
        center - side * radius,
        center - normal * radius,
    )
    faces = (
        (0, 2, 3),
        (0, 3, 4),
        (0, 4, 5),
        (0, 5, 2),
        (1, 3, 2),
        (1, 4, 3),
        (1, 5, 4),
        (1, 2, 5),
    )
    name = f"RA_Anatomy_{anatomy_plan.role}"
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, (), faces)
    mesh.update()
    anatomy = bpy.data.objects.new(name, mesh)
    anatomy["ra_owner"] = "rigged_anatomy"
    anatomy["ra_anatomy_role"] = anatomy_plan.role
    anatomy["ra_driver_role"] = anatomy_plan.driver
    collection.objects.link(anatomy)
    return anatomy


class BlenderMaterializer:
    def materialize(self, plan: RigPlan, target_height: float) -> None:
        existing = bpy.data.collections.get(COLLECTION_NAME)
        if existing is not None:
            armature = existing.objects.get(ARMATURE_NAME)
            if armature is not None and armature.get("ra_plan_digest") == plan.digest():
                return
            raise ValueError("Existing generated output does not match this plan.")

        staged = bpy.data.collections.new(f"{COLLECTION_NAME}.__staging__")
        bpy.context.scene.collection.children.link(staged)
        try:
            armature_data = bpy.data.armatures.new(ARMATURE_NAME)
            armature_object = bpy.data.objects.new(ARMATURE_NAME, armature_data)
            staged.objects.link(armature_object)
            bpy.context.view_layer.objects.active = armature_object
            armature_object.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")

            edit_bones = {}
            for bone_plan in plan.bones:
                bone = armature_data.edit_bones.new(bone_plan.name)
                bone.head = tuple(component * target_height for component in bone_plan.head)
                bone.tail = tuple(component * target_height for component in bone_plan.tail)
                bone.use_deform = bone_plan.deform
                if bone_plan.parent is not None:
                    bone.parent = edit_bones[bone_plan.parent]
                    bone.use_connect = True
                edit_bones[bone_plan.role] = bone

            bpy.ops.object.mode_set(mode="OBJECT")
            armature_object["ra_owner"] = "rigged_anatomy"
            armature_object["ra_schema_version"] = plan.schema_version
            armature_object["ra_plan_digest"] = plan.digest()
            if len(armature_data.bones) != len(plan.bones):
                raise RuntimeError("Staged armature did not contain every planned bone.")

            drivers = {bone.role: bone for bone in plan.bones}
            for anatomy_plan in plan.anatomy_drivers:
                anatomy = _materialize_anatomy(
                    staged,
                    anatomy_plan,
                    drivers[anatomy_plan.driver],
                    target_height,
                )
                anatomy["ra_schema_version"] = plan.schema_version
                anatomy["ra_plan_digest"] = plan.digest()
            staged.name = COLLECTION_NAME
        except Exception:
            if bpy.context.object is not None and bpy.context.object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            created_data = [obj.data for obj in staged.objects if obj.data is not None]
            for obj in list(staged.objects):
                bpy.data.objects.remove(obj, do_unlink=True)
            for data in created_data:
                if data.users == 0:
                    if isinstance(data, bpy.types.Armature):
                        bpy.data.armatures.remove(data)
                    elif isinstance(data, bpy.types.Mesh):
                        bpy.data.meshes.remove(data)
            bpy.data.collections.remove(staged)
            raise
