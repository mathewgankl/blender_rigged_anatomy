# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .role_registry import load_role_registry


DATA_PATH = Path(__file__).with_name("data")


@dataclass(frozen=True)
class SemanticMappingManifest:
    schema_version: int
    target: str
    source_url: str
    source_version: str
    mappings: Mapping[str, str | None]


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate semantic mapping key: {key}")
        result[key] = value
    return result


def _load_manifest(filename: str) -> SemanticMappingManifest:
    payload = json.loads(
        (DATA_PATH / filename).read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
    )
    mappings = payload["mappings"]
    role_ids = {role.id for role in load_role_registry().roles}
    if set(mappings) != role_ids:
        raise ValueError("Semantic mapping keys must exactly match the role registry.")
    targets = [target for target in mappings.values() if target is not None]
    if len(targets) != len(set(targets)):
        raise ValueError("Supported semantic mapping targets must be unique.")
    return SemanticMappingManifest(
        schema_version=payload["schema_version"],
        target=payload["target"],
        source_url=payload["source_url"],
        source_version=payload["source_version"],
        mappings=MappingProxyType(mappings),
    )


def load_vrm_mapping() -> SemanticMappingManifest:
    return _load_manifest("vrm-1.0-mapping-v1.json")


def load_humanik_mapping() -> SemanticMappingManifest:
    return _load_manifest("humanik-fbx-2020-mapping-v1.json")
