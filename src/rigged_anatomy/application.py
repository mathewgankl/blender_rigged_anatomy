# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Mapping, Protocol, Sequence


Vector3 = tuple[float, float, float]
REQUIRED_LANDMARKS = ("shoulder.L", "palm.L")
NORMALIZED_PRECISION = 7


@dataclass(frozen=True)
class GenerateSettings:
    pass


@dataclass
class GenerateRequest:
    target_name: str
    target_height: float
    landmarks: Mapping[str, Sequence[float]]
    settings: GenerateSettings


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    subject: str

    def to_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "subject": self.subject}


@dataclass(frozen=True)
class BonePlan:
    role: str
    name: str
    parent: str | None
    head: Vector3
    tail: Vector3
    deform: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "deform": self.deform,
            "head": list(self.head),
            "name": self.name,
            "parent": self.parent,
            "role": self.role,
            "tail": list(self.tail),
        }


@dataclass(frozen=True)
class AnatomyDriverPlan:
    role: str
    driver: str

    def to_dict(self) -> dict[str, str]:
        return {"driver": self.driver, "role": self.role}


@dataclass(frozen=True)
class RigPlan:
    schema_version: int
    bones: tuple[BonePlan, ...]
    anatomy_drivers: tuple[AnatomyDriverPlan, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "anatomy_drivers": [driver.to_dict() for driver in self.anatomy_drivers],
            "bones": [bone.to_dict() for bone in self.bones],
            "schema_version": self.schema_version,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    def digest(self) -> str:
        return sha256(self.to_json().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class GenerateResult:
    plan: RigPlan | None
    errors: tuple[ValidationIssue, ...] = ()
    warnings: tuple[ValidationIssue, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {
            "errors": [error.to_dict() for error in self.errors],
            "ok": self.ok,
            "plan": self.plan.to_dict() if self.plan else None,
            "warnings": [warning.to_dict() for warning in self.warnings],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))


class Materializer(Protocol):
    def materialize(self, plan: RigPlan, target_height: float) -> None: ...


def _finite_vector(value: Sequence[float] | None) -> bool:
    if value is None or len(value) != 3:
        return False
    return all(math.isfinite(component) for component in value)


def _validate(request: GenerateRequest) -> tuple[ValidationIssue, ...]:
    errors: list[ValidationIssue] = []
    if not math.isfinite(request.target_height) or request.target_height <= 0:
        errors.append(
            ValidationIssue(
                "invalid_target_height",
                "Target height must be finite and greater than zero.",
                request.target_name,
            )
        )
    for role in REQUIRED_LANDMARKS:
        value = request.landmarks.get(role)
        if value is None:
            errors.append(
                ValidationIssue("missing_landmark", f"Missing required landmark {role}.", role)
            )
        elif not _finite_vector(value):
            errors.append(
                ValidationIssue(
                    "invalid_landmark",
                    f"Landmark {role} must contain three finite coordinates.",
                    role,
                )
            )
    return tuple(errors)


def _normalized(value: Sequence[float], height: float) -> Vector3:
    return tuple(  # type: ignore[return-value]
        round(component / height, NORMALIZED_PRECISION) for component in value
    )


def _build_plan(request: GenerateRequest) -> RigPlan:
    shoulder = _normalized(request.landmarks["shoulder.L"], request.target_height)
    palm = _normalized(request.landmarks["palm.L"], request.target_height)
    elbow = (
        round((shoulder[0] + palm[0]) / 2, NORMALIZED_PRECISION),
        round((shoulder[1] + palm[1]) / 2 - 0.05, NORMALIZED_PRECISION),
        round((shoulder[2] + palm[2]) / 2, NORMALIZED_PRECISION),
    )
    return RigPlan(
        schema_version=1,
        bones=(
            BonePlan("upper_arm.L", "DEF-upper_arm.L", None, shoulder, elbow),
            BonePlan("forearm.L", "DEF-forearm.L", "upper_arm.L", elbow, palm),
        ),
        anatomy_drivers=(
            AnatomyDriverPlan("humerus.L", "upper_arm.L"),
            AnatomyDriverPlan("radius.L", "forearm.L"),
            AnatomyDriverPlan("ulna.L", "forearm.L"),
        ),
    )


def run_generate(
    request: GenerateRequest, materializer: Materializer | None = None
) -> GenerateResult:
    errors = _validate(request)
    if errors:
        return GenerateResult(plan=None, errors=errors)

    plan = _build_plan(request)
    if materializer is not None:
        try:
            materializer.materialize(plan, request.target_height)
        except Exception as exc:
            return GenerateResult(
                plan=None,
                errors=(
                    ValidationIssue(
                        "materialization_failed",
                        f"Could not materialize the rig plan: {exc}",
                        request.target_name,
                    ),
                ),
            )
    return GenerateResult(plan=plan)
