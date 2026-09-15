# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from pathlib import Path


_ASSET_PATHS = {
    ("mesh:humerus", "source"): Path(__file__).with_name("data")
    / "anatomy"
    / "humerus-source-v1.json",
    ("mesh:humerus", "base"): Path(__file__).with_name("data")
    / "anatomy"
    / "humerus-base-v1.json",
}


def load_anatomy_asset(asset_id: str, topology_tier: str) -> dict[str, object]:
    try:
        path = _ASSET_PATHS[(asset_id, topology_tier)]
    except KeyError as error:
        raise KeyError(f"Unknown anatomy asset tier: {asset_id} ({topology_tier})") from error
    asset = json.loads(path.read_text(encoding="utf-8"))
    if (
        asset.get("schema_version") != 1
        or asset.get("asset_id") != asset_id
        or asset.get("topology_tier") != topology_tier
    ):
        raise ValueError(f"Invalid packaged anatomy asset tier: {asset_id} ({topology_tier})")
    return asset
