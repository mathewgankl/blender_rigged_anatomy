# SPDX-License-Identifier: GPL-3.0-or-later

import importlib
import importlib.util
import sys

import addon_utils
import bpy


MODULE = "bl_ext.user_default.rigged_anatomy"


def test_lifecycle():
    assert addon_utils.check(MODULE)[1]
    assert hasattr(bpy.types, "RIGGED_ANATOMY_OT_generate_vertical_slice")
    registry = importlib.import_module(f"{MODULE}.role_registry").load_role_registry()
    assert registry.schema_version == 1
    assert len(registry.roles) == 55
    mappings = importlib.import_module(f"{MODULE}.semantic_mappings")
    assert len(mappings.load_vrm_mapping().mappings) == 55
    assert len(mappings.load_humanik_mapping().mappings) == 55
    source_manifest = importlib.import_module(f"{MODULE}.source_manifest")
    source_inventory = source_manifest.load_source_manifest()
    assert len(source_inventory["xml_files"]) == 23
    assert len(source_inventory["resources"]) == 190
    assert len(source_inventory["bodies"]) == 80
    assert len(source_inventory["attachment_sites"]) == 2756
    assert len(source_inventory["wrapping_geometries"]) == 182
    assert len(source_inventory["tendon_paths"]) == 700
    assert len(source_inventory["muscle_actuators"]) == 700
    catalogs = importlib.import_module(f"{MODULE}.catalogs")
    assert catalogs.load_catalog_schema()["schema_version"] == 1
    empty_catalog = {"schema_version": 1, "entries": []}
    assert catalogs.validate_anatomy_catalog(empty_catalog) == ()
    assert catalogs.validate_relationship_catalog(empty_catalog, empty_catalog) == ()
    anatomy_catalog = catalogs.load_anatomy_catalog()
    assert catalogs.validate_anatomy_catalog(anatomy_catalog) == ()
    assert anatomy_catalog["entries"][0]["driver_role"] == "upper_arm.R"
    anatomy_assets = importlib.import_module(f"{MODULE}.anatomy_assets")
    humerus_source = anatomy_assets.load_anatomy_asset("mesh:humerus", "source")
    assert humerus_source["topology"]["vertex_count"] == 309
    assert humerus_source["topology"]["triangle_count"] == 588
    humerus_base = anatomy_assets.load_anatomy_asset("mesh:humerus", "base")
    assert humerus_base["topology"]["is_closed_two_manifold"]
    assert humerus_base["topology"]["triangle_count"] == 600
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
