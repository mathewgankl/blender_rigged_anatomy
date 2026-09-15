# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(__file__).with_name("data") / "ms-human-700-source-v1.json"


def load_source_manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
