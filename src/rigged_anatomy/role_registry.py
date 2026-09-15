# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


REGISTRY_PATH = Path(__file__).with_name("data") / "role-registry-v1.json"


@dataclass(frozen=True)
class RoleDefinition:
    id: str
    parent: str | None
    side: str | None
    generated_name: str
    deform: bool


@dataclass(frozen=True)
class RoleRegistry:
    schema_version: int
    roles: tuple[RoleDefinition, ...]

    def require(self, role_id: str) -> RoleDefinition:
        for role in self.roles:
            if role.id == role_id:
                return role
        raise KeyError(f"Unknown canonical role: {role_id}")


def _validate_registry(registry: RoleRegistry) -> None:
    if registry.schema_version != 1:
        raise ValueError("Canonical role registry schema version must be 1.")
    by_id = {role.id: role for role in registry.roles}
    if len(by_id) != len(registry.roles):
        raise ValueError("Canonical role IDs must be unique.")
    generated_names = [role.generated_name for role in registry.roles]
    if len(generated_names) != len(set(generated_names)):
        raise ValueError("Generated role names must be unique.")
    for role in registry.roles:
        if role.parent is not None and role.parent not in by_id:
            raise ValueError(f"Unknown parent role for {role.id}: {role.parent}")
        expected_side = role.id.rpartition(".")[2]
        expected_side = expected_side if expected_side in {"L", "R"} else None
        if role.side != expected_side:
            raise ValueError(f"Canonical role side does not match its ID: {role.id}")
    for role in registry.roles:
        visited = {role.id}
        parent = role.parent
        while parent is not None:
            if parent in visited:
                raise ValueError(f"Canonical role hierarchy contains a cycle at {role.id}.")
            visited.add(parent)
            parent = by_id[parent].parent


def load_role_registry() -> RoleRegistry:
    payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry = RoleRegistry(
        schema_version=payload["schema_version"],
        roles=tuple(RoleDefinition(**role) for role in payload["roles"]),
    )
    _validate_registry(registry)
    return registry
