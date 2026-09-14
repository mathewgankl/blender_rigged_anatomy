# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bpy

from .application import GenerateRequest, GenerateSettings, run_generate
from .blender_adapter import BlenderMaterializer


class RIGGED_ANATOMY_OT_generate_vertical_slice(bpy.types.Operator):
    bl_idname = "rigged_anatomy.generate_vertical_slice"
    bl_label = "Generate Anatomy Rig"
    bl_description = "Generate the current anatomical rig plan"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        target = context.active_object
        target_name = target.name if target is not None else ""
        target_height = target.dimensions.z if target is not None else 0.0
        landmarks = {}
        for obj in context.scene.objects:
            role = obj.get("ra_landmark_role")
            if role in {"shoulder.L", "palm.L"}:
                location = obj.matrix_world.translation
                landmarks[role] = tuple(location)

        request = GenerateRequest(
            target_name=target_name,
            target_height=target_height,
            landmarks=landmarks,
            settings=GenerateSettings(),
        )
        result = run_generate(request, BlenderMaterializer())
        context.scene["ra_last_result"] = result.to_json()
        if not result.ok:
            for error in result.errors:
                self.report({"ERROR"}, f"{error.code}: {error.message}")
            return {"CANCELLED"}
        return {"FINISHED"}


CLASSES = (RIGGED_ANATOMY_OT_generate_vertical_slice,)
_registered = False


def register():
    global _registered
    if _registered:
        return
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    _registered = True


def unregister():
    global _registered
    if not _registered:
        return
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    _registered = False
