# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rigged_anatomy.source_manifest import load_source_manifest


BASE_VOXEL_SIZE_METERS = 0.002
BASE_TARGET_TRIANGLE_COUNT = 600


def _read_binary_stl(path: Path) -> tuple[list[list[float]], list[list[int]]]:
    data = path.read_bytes()
    if len(data) < 84:
        raise ValueError("Binary STL is shorter than its header.")
    triangle_count = struct.unpack_from("<I", data, 80)[0]
    if len(data) != 84 + triangle_count * 50:
        raise ValueError("Binary STL length does not match its triangle count.")

    vertices = []
    triangles = []
    vertex_ids = {}
    for triangle_index in range(triangle_count):
        offset = 84 + triangle_index * 50 + 12
        triangle = []
        for vertex_index in range(3):
            coordinate = struct.unpack_from("<3f", data, offset + vertex_index * 12)
            if not all(math.isfinite(component) for component in coordinate):
                raise ValueError("Binary STL contains a non-finite coordinate.")
            coordinate = tuple(0.0 if component == 0.0 else component for component in coordinate)
            if coordinate not in vertex_ids:
                vertex_ids[coordinate] = len(vertices)
                vertices.append(list(coordinate))
            triangle.append(vertex_ids[coordinate])
        triangles.append(triangle)
    return vertices, triangles


def _topology(
    vertices: list[list[float]], triangles: list[list[int]]
) -> dict[str, int | bool]:
    edge_counts = Counter()
    edge_directions: dict[tuple[int, int], list[bool]] = {}
    parent = list(range(len(vertices)))

    def find(vertex_id: int) -> int:
        while parent[vertex_id] != vertex_id:
            parent[vertex_id] = parent[parent[vertex_id]]
            vertex_id = parent[vertex_id]
        return vertex_id

    def union(first: int, second: int) -> None:
        first_root = find(first)
        second_root = find(second)
        if first_root != second_root:
            parent[second_root] = first_root

    degenerate_count = 0
    for triangle in triangles:
        if len(set(triangle)) != 3:
            degenerate_count += 1
        for first, second in zip(triangle, (*triangle[1:], triangle[0])):
            edge = (min(first, second), max(first, second))
            edge_counts[edge] += 1
            edge_directions.setdefault(edge, []).append(first < second)
            union(first, second)

    used_vertices = {vertex_id for triangle in triangles for vertex_id in triangle}
    topology = {
        "vertex_count": len(vertices),
        "triangle_count": len(triangles),
        "boundary_edge_count": sum(count == 1 for count in edge_counts.values()),
        "non_manifold_edge_count": sum(count > 2 for count in edge_counts.values()),
        "inconsistent_winding_edge_count": sum(
            len(directions) == 2 and directions[0] == directions[1]
            for directions in edge_directions.values()
        ),
        "degenerate_triangle_count": degenerate_count,
        "connected_component_count": len({find(vertex_id) for vertex_id in used_vertices}),
    }
    topology["is_closed_two_manifold"] = all(
        topology[key] == 0
        for key in (
            "boundary_edge_count",
            "non_manifold_edge_count",
            "inconsistent_winding_edge_count",
            "degenerate_triangle_count",
        )
    ) and topology["connected_component_count"] == 1
    return topology


def _source_data(
    source_root: Path, source_key: str
) -> tuple[dict[str, object], dict[str, object], str, list[list[float]], list[list[int]]]:
    manifest = load_source_manifest()
    try:
        source = next(
            entry
            for entry in manifest["resources"]
            if entry["source_key"] == source_key and entry["disposition"] == "retain"
        )
    except StopIteration as error:
        raise KeyError(f"Unknown retained anatomy source: {source_key}") from error

    source_path = source_root / source["path"]
    digest = sha256(source_path.read_bytes()).hexdigest()
    if digest != source["sha256"]:
        raise ValueError(f"Pinned source hash mismatch: {source_key}")
    vertices, triangles = _read_binary_stl(source_path)
    return manifest, source, digest, vertices, triangles


def _provenance(
    manifest: dict[str, object], source: dict[str, object], source_key: str, digest: str
) -> dict[str, object]:
    return {
        "repository": manifest["source_repository"],
        "revision": manifest["source_revision"],
        "license": manifest["source_license"],
        "source_key": source_key,
        "source_path": source["path"],
        "sha256": digest,
    }


def build_anatomy_asset(source_root: Path, source_key: str) -> dict[str, object]:
    manifest, source, digest, vertices, triangles = _source_data(source_root, source_key)
    return {
        "schema_version": 1,
        "asset_id": source_key,
        "topology_tier": "source",
        "units": "meter",
        "id_convention": "zero_based_array_index",
        "provenance": _provenance(manifest, source, source_key, digest),
        "conversion": {
            "format": "indexed-triangle-mesh-v1",
            "source_format": "binary_stl",
            "operation": "Exact-coordinate vertex deduplication; source triangle order preserved.",
        },
        "modification_notice": (
            "Converted from binary STL to indexed JSON; exact duplicate vertex "
            "coordinates were merged and source triangle order was preserved."
        ),
        "topology": _topology(vertices, triangles),
        "vertices": vertices,
        "triangles": triangles,
    }


def _canonical_blender_mesh(mesh) -> tuple[list[list[float]], list[list[int]]]:
    import bmesh

    editable = bmesh.new()
    editable.from_mesh(mesh)
    bmesh.ops.triangulate(editable, faces=list(editable.faces))
    bmesh.ops.recalc_face_normals(editable, faces=list(editable.faces))
    coordinates = [tuple(float(component) for component in vertex.co) for vertex in editable.verts]
    order = sorted(range(len(coordinates)), key=lambda vertex_id: coordinates[vertex_id])
    canonical_ids = {old_id: new_id for new_id, old_id in enumerate(order)}
    vertices = [list(coordinates[old_id]) for old_id in order]
    editable_ids = {vertex: index for index, vertex in enumerate(editable.verts)}
    triangles = []
    for face in editable.faces:
        triangle = [canonical_ids[editable_ids[vertex]] for vertex in face.verts]
        first = triangle.index(min(triangle))
        triangles.append(triangle[first:] + triangle[:first])
    triangles.sort()
    editable.free()
    return vertices, triangles


def _source_deviation(
    source_vertices: list[list[float]],
    source_triangles: list[list[int]],
    result_vertices: list[list[float]],
    result_triangles: list[list[int]],
) -> dict[str, int | float | str]:
    from mathutils.bvhtree import BVHTree

    source_tree = BVHTree.FromPolygons(source_vertices, source_triangles, all_triangles=True)
    result_tree = BVHTree.FromPolygons(result_vertices, result_triangles, all_triangles=True)
    distances = [source_tree.find_nearest(vertex)[3] for vertex in result_vertices]
    distances.extend(result_tree.find_nearest(vertex)[3] for vertex in source_vertices)
    distances.sort()
    return {
        "method": "bidirectional_vertex_to_surface",
        "sample_count": len(distances),
        "p95_meters": distances[int(0.95 * (len(distances) - 1))],
        "max_meters": distances[-1],
    }


def build_base_anatomy_asset(source_root: Path, source_key: str) -> dict[str, object]:
    import bpy

    manifest, source, digest, source_vertices, source_triangles = _source_data(
        source_root, source_key
    )
    mesh = bpy.data.meshes.new("RA_TEMP_base_asset")
    object_ = bpy.data.objects.new("RA_TEMP_base_asset", mesh)
    bpy.context.scene.collection.objects.link(object_)
    try:
        mesh.from_pydata(source_vertices, [], source_triangles)
        mesh.update()
        bpy.ops.object.select_all(action="DESELECT")
        object_.select_set(True)
        bpy.context.view_layer.objects.active = object_
        mesh.remesh_voxel_size = BASE_VOXEL_SIZE_METERS
        mesh.remesh_voxel_adaptivity = 0.0
        bpy.ops.object.voxel_remesh()

        _, remeshed_triangles = _canonical_blender_mesh(mesh)
        modifier = object_.modifiers.new("RA Deterministic Decimate", "DECIMATE")
        modifier.decimate_type = "COLLAPSE"
        modifier.ratio = BASE_TARGET_TRIANGLE_COUNT / len(remeshed_triangles)
        modifier.use_collapse_triangulate = True
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        vertices, triangles = _canonical_blender_mesh(mesh)
    finally:
        bpy.data.objects.remove(object_, do_unlink=True)
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)

    topology = _topology(vertices, triangles)
    if topology["triangle_count"] != BASE_TARGET_TRIANGLE_COUNT:
        raise ValueError("Base-tier decimation did not reach its triangle target.")
    if not topology["is_closed_two_manifold"]:
        raise ValueError("Base-tier preprocessing did not produce a closed two-manifold.")
    return {
        "schema_version": 1,
        "asset_id": source_key,
        "topology_tier": "base",
        "units": "meter",
        "id_convention": "zero_based_array_index",
        "provenance": _provenance(manifest, source, source_key, digest),
        "processing": {
            "blender_version": bpy.app.version_string,
            "voxel_size_meters": BASE_VOXEL_SIZE_METERS,
            "voxel_adaptivity": 0.0,
            "target_triangle_count": BASE_TARGET_TRIANGLE_COUNT,
            "canonicalization": "Lexicographic vertices and cyclic winding-preserving triangles.",
        },
        "modification_notice": (
            "Derived from the source tier using Blender Voxel Remesh and collapse "
            "decimation; topology and vertex positions were replaced."
        ),
        "source_topology": _topology(source_vertices, source_triangles),
        "source_deviation": _source_deviation(
            source_vertices, source_triangles, vertices, triangles
        ),
        "topology": topology,
        "vertices": vertices,
        "triangles": triangles,
    }


def main() -> None:
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--source-key", required=True)
    parser.add_argument("--topology-tier", choices=("source", "base"), default="source")
    parser.add_argument("--output", required=True, type=Path)
    options = parser.parse_args(arguments)
    if options.topology_tier == "base":
        asset = build_base_anatomy_asset(options.source_root, options.source_key)
    else:
        asset = build_anatomy_asset(options.source_root, options.source_key)
    options.output.write_text(
        json.dumps(asset, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
