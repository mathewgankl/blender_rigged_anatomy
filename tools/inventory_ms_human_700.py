# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ElementTree


SOURCE_REPOSITORY = "https://github.com/google-deepmind/mujoco_menagerie.git"
SOURCE_REVISION = "8161bba264d7fa7c99ca301e91e7fb44737676ad"
ROOT_MODEL = "MS-Human-700.xml"


def _digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _xml_kind(path: str) -> str:
    if path == ROOT_MODEL:
        return "root_model"
    for folder, kind in (
        ("assets/body_primary/", "body"),
        ("assets/asset/", "asset_catalog"),
        ("assets/contact/", "contact"),
        ("assets/equality/", "equality"),
        ("assets/tendon/", "tendon_paths"),
        ("assets/muscle/", "muscle_actuators"),
    ):
        if path.startswith(folder):
            return kind
    raise ValueError(f"Unclassified XML source: {path}")


def _xml_closure(source_root: Path) -> list[Path]:
    pending = [source_root / ROOT_MODEL]
    found: dict[str, Path] = {}
    while pending:
        path = pending.pop()
        relative = _relative(path, source_root)
        if relative in found:
            continue
        found[relative] = path
        root = ElementTree.parse(path).getroot()
        for include in root.findall(".//include"):
            pending.append((path.parent / include.attrib["file"]).resolve())
    return [found[path] for path in sorted(found)]


def _resource_disposition(tag: str, name: str) -> tuple[str, str | None]:
    if tag == "texture":
        return "ignored", "Rendering texture outside anatomy conversion."
    if name.startswith("waterbottle"):
        return "ignored", "Manipulation prop outside human anatomy."
    return "retain", None


def _require_unique(records: list[dict[str, object]], label: str) -> None:
    keys = [record["source_key"] for record in records]
    if len(keys) != len(set(keys)):
        raise ValueError(f"Duplicate {label} source key.")


def _owned_declarations(
    source_root: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    sites = []
    geoms = []

    def visit(
        element: ElementTree.Element,
        owning_body: str | None,
        xml_path: Path,
    ) -> None:
        if element.tag == "include":
            included_path = (xml_path.parent / element.attrib["file"]).resolve()
            included_root = ElementTree.parse(included_path).getroot()
            for child in included_root:
                visit(child, owning_body, included_path)
            return
        if element.tag == "body" and "name" in element.attrib:
            owning_body = element.attrib["name"]
        if owning_body is not None and element.tag in {"site", "geom"}:
            name = element.attrib.get("name")
            if name is not None:
                record = {
                    "name": name,
                    "declaration_path": _relative(xml_path, source_root),
                    "owning_body_source_key": f"body:{owning_body}",
                    "attributes": {
                        key: value
                        for key, value in sorted(element.attrib.items())
                        if key != "name"
                    },
                }
                (sites if element.tag == "site" else geoms).append(record)
        for child in element:
            visit(child, owning_body, xml_path)

    root_path = source_root / ROOT_MODEL
    visit(ElementTree.parse(root_path).getroot(), None, root_path)
    return sites, geoms


def _resolve_declarations(
    candidates: list[dict[str, object]], references: Counter[str], prefix: str
) -> list[dict[str, object]]:
    by_key: dict[str, list[dict[str, object]]] = {}
    for candidate in candidates:
        source_key = f"{prefix}:{candidate['name']}"
        by_key.setdefault(source_key, []).append(candidate)
    resolved = []
    for source_key in sorted(references):
        matches = by_key.get(source_key, [])
        if len(matches) != 1:
            raise ValueError(
                f"{source_key} must resolve to exactly one owned declaration; "
                f"found {len(matches)}."
            )
        resolved.append({"source_key": source_key, **matches[0]})
    return resolved


def build_manifest(source_root: Path) -> dict[str, object]:
    source_root = source_root.resolve()
    xml_paths = _xml_closure(source_root)
    xml_files = []
    resources = []
    bodies = []
    tendon_paths = []
    muscle_actuators = []
    site_declarations, geom_declarations = _owned_declarations(source_root)
    for xml_path in xml_paths:
        relative_xml = _relative(xml_path, source_root)
        xml_files.append(
            {
                "path": relative_xml,
                "kind": _xml_kind(relative_xml),
                "sha256": _digest(xml_path),
            }
        )
        root = ElementTree.parse(xml_path).getroot()
        for body in root.findall(".//body[@name]"):
            name = body.attrib["name"]
            source_key = f"body:{name}"
            bodies.append(
                {
                    "source_key": source_key,
                    "name": name,
                    "declaration_path": relative_xml,
                    "mesh_refs": [
                        geom.attrib["mesh"] for geom in body.findall("./geom[@mesh]")
                    ],
                    "catalog_key": source_key,
                }
            )
        for spatial in root.findall(".//spatial[@name]"):
            name = spatial.attrib["name"]
            source_key = f"path:{name}"
            elements = []
            for element in spatial:
                if element.tag == "site":
                    elements.append({"kind": "site", "ref": element.attrib["site"]})
                elif element.tag == "geom":
                    wrap = {"kind": "wrap", "ref": element.attrib["geom"]}
                    if "sidesite" in element.attrib:
                        wrap["sidesite"] = element.attrib["sidesite"]
                    elements.append(wrap)
                else:
                    raise ValueError(
                        f"Unsupported tendon path element {element.tag} in {name}."
                    )
            tendon_paths.append(
                {
                    "source_key": source_key,
                    "name": name,
                    "declaration_path": relative_xml,
                    "elements": elements,
                    "catalog_key": source_key,
                }
            )
        for actuator in root.findall(".//actuator/*[@name][@tendon]"):
            name = actuator.attrib["name"]
            source_key = f"muscle:{name}"
            muscle_actuators.append(
                {
                    "source_key": source_key,
                    "name": name,
                    "declaration_path": relative_xml,
                    "tendon": actuator.attrib["tendon"],
                    "catalog_key": source_key,
                }
            )
        for tag in ("mesh", "texture"):
            for element in root.findall(f".//{tag}[@file]"):
                name = element.attrib["name"]
                resource_path = (xml_path.parent / element.attrib["file"]).resolve()
                disposition, reason = _resource_disposition(tag, name)
                record = {
                    "source_key": f"{tag}:{name}",
                    "declaration_path": relative_xml,
                    "path": _relative(resource_path, source_root),
                    "kind": "anatomy_mesh" if disposition == "retain" else "non_domain",
                    "sha256": _digest(resource_path),
                    "disposition": disposition,
                    "catalog_key": f"{tag}:{name}" if disposition == "retain" else None,
                }
                if reason is not None:
                    record["reason"] = reason
                resources.append(record)
    bodies.sort(key=lambda record: record["source_key"])
    tendon_paths.sort(key=lambda record: record["source_key"])
    muscle_actuators.sort(key=lambda record: record["source_key"])
    resources.sort(key=lambda record: record["source_key"])
    _require_unique(bodies, "body")
    _require_unique(tendon_paths, "tendon path")
    _require_unique(muscle_actuators, "muscle actuator")
    _require_unique(resources, "resource")
    tendon_names = {record["name"] for record in tendon_paths}
    actuator_tendons = {record["tendon"] for record in muscle_actuators}
    if tendon_names != actuator_tendons:
        raise ValueError("Muscle actuator references must exactly match tendon paths.")
    direct_site_refs = Counter(
        f"site:{element['ref']}"
        for path in tendon_paths
        for element in path["elements"]
        if element["kind"] == "site"
    )
    sidesite_refs = Counter(
        f"site:{element['sidesite']}"
        for path in tendon_paths
        for element in path["elements"]
        if element["kind"] == "wrap" and "sidesite" in element
    )
    wrap_refs = Counter(
        f"wrap:{element['ref']}"
        for path in tendon_paths
        for element in path["elements"]
        if element["kind"] == "wrap"
    )
    attachment_sites = _resolve_declarations(
        site_declarations, direct_site_refs + sidesite_refs, "site"
    )
    for site in attachment_sites:
        site["path_reference_count"] = direct_site_refs[site["source_key"]]
        site["sidesite_reference_count"] = sidesite_refs[site["source_key"]]
    wrapping_geometries = _resolve_declarations(geom_declarations, wrap_refs, "wrap")
    for wrap in wrapping_geometries:
        wrap["path_reference_count"] = wrap_refs[wrap["source_key"]]
    return {
        "schema_version": 1,
        "source_repository": SOURCE_REPOSITORY,
        "source_revision": SOURCE_REVISION,
        "source_license": "Apache-2.0",
        "root_model": ROOT_MODEL,
        "xml_files": xml_files,
        "resources": resources,
        "bodies": bodies,
        "attachment_sites": attachment_sites,
        "wrapping_geometries": wrapping_geometries,
        "tendon_paths": tendon_paths,
        "muscle_actuators": muscle_actuators,
    }


def main() -> None:
    arguments = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    options = parser.parse_args(arguments)
    manifest = build_manifest(options.source_root)
    options.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
