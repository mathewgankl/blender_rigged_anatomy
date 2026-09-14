# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.util
import sys

import addon_utils
import bpy


MODULE = "bl_ext.user_default.rigged_anatomy"


def test_lifecycle():
    assert addon_utils.check(MODULE)[1]
    assert hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice")
    bpy.ops.preferences.addon_disable(module=MODULE)
    assert not addon_utils.check(MODULE)[1]
    assert not hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice")
    bpy.ops.preferences.addon_enable(module=MODULE)
    assert addon_utils.check(MODULE)[1]
    print("EXTENSION_LIFECYCLE_OK")


def test_uninstalled():
    assert importlib.util.find_spec(MODULE) is None
    assert not hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice")
    print("EXTENSION_UNINSTALL_OK")


mode = sys.argv[sys.argv.index("--") + 1]
if mode == "lifecycle":
    test_lifecycle()
elif mode == "uninstalled":
    test_uninstalled()
else:
    raise ValueError(f"Unknown lifecycle test mode: {mode}")
