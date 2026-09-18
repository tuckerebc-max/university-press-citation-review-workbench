from __future__ import annotations

from copy import deepcopy
import re
from typing import Any


SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
CPR_SCHEMA = "university_press.cpr_result.draft1"
PPR_SCHEMA = "university_press.ppr_result.draft1"


class AdapterError(ValueError):
    """Raised when an upstream family result cannot be normalized safely."""


def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise AdapterError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _non_empty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise AdapterError(f"{label} must be a non-empty string")
    return value


def _family_record(value: Any, family_id: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdapterError(f"{family_id} upstream result must be an object")
    status = value.get("status")
    if not isinstance(status, str) or not status:
        raise AdapterError(f"{family_id} upstream result needs a status")
    return {"status": status, **{key: value[key] for key in ("coverage", "reason") if key in value}}


def evaluate_cpr(upstream_results: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    """Normalize CPR dependencies without turning other families into CE."""

    if not isinstance(upstream_results, dict):
        raise AdapterError("upstream_results must be an object")
    if not isinstance(profile, dict):
        raise AdapterError("profile must be an object")
    required = profile.get("required_upstream_families")
    if not isinstance(required, list) or not required or not all(isinstance(item, str) and item for item in required):
        raise AdapterError("profile.required_upstream_families must be a non-empty string list")
    copyediting_state = profile.get("copyediting")
    if copyediting_state not in {"absent", "present", "unknown"}:
        raise AdapterError("profile.copyediting must be absent, present, or unknown")

    upstream_statuses: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    not_run: list[str] = []
    coverage_unknown = False
    for family_id in required:
        if family_id not in upstream_results:
            upstream_statuses[family_id] = {
                "status": "not_run",
                "reason": "required_upstream_result_missing",
            }
            missing.append(family_id)
            not_run.append(family_id)
            coverage_unknown = True
            continue
        record = _family_record(upstream_results[family_id], family_id)
        upstream_statuses[family_id] = record
        if record["status"] in {"not_run", "unknown"}:
            not_run.append(family_id)
            coverage_unknown = True
        elif record.get("coverage") == "unknown":
            coverage_unknown = True

    absent: list[str] = []
    if copyediting_state == "absent":
        upstream_statuses["CE"] = {
            "status": "absent",
            "reason": profile.get("copyediting_reason", "profile_declares_capability_absent"),
        }
        absent.append("CE")
    elif "CE" in upstream_results:
        upstream_statuses["CE"] = _family_record(upstream_results["CE"], "CE")
        if upstream_statuses["CE"]["status"] in {"not_run", "unknown"}:
            not_run.append("CE")
            coverage_unknown = True
    else:
        upstream_statuses["CE"] = {"status": "not_run", "reason": "copyediting_result_missing"}
        not_run.append("CE")
        coverage_unknown = True

    if missing or not_run:
        status = "blocked_input"
        coverage = "unknown"
    elif absent:
        status = "hold"
        coverage = "unknown" if coverage_unknown else "known"
    else:
        status = "ready_for_component_review"
        coverage = "unknown" if coverage_unknown else "known"

    return {
        "schema": CPR_SCHEMA,
        "family_id": "CPR",
        "status": status,
        "coverage": coverage,
        "upstream_statuses": upstream_statuses,
        "missing_dependencies": sorted(set(missing)),
        "not_run_dependencies": sorted(set(not_run)),
        "absent_dependencies": absent,
        "substitutions": [],
        "ce_gap_visible": bool(absent),
        "claims": {
            "copyedited": "withheld" if absent or missing or not_run else "not_established",
            "production_ready": "withheld",
        },
        "no_editorial_clearance": True,
    }


def _optional_record(inputs: dict[str, Any], key: str) -> dict[str, Any] | None:
    value = inputs.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise AdapterError(f"{key} must be an object")
    _non_empty_string(value.get("id"), f"{key}.id")
    _digest(value.get("sha256"), f"{key}.sha256")
    return value


def evaluate_ppr(inputs: dict[str, Any]) -> dict[str, Any]:
    """Check PPR input fixity; never perform substantive proof review."""

    if not isinstance(inputs, dict):
        raise AdapterError("PPR inputs must be an object")
    blockers: list[str] = []
    baseline = _optional_record(inputs, "approved_baseline")
    accepted = _optional_record(inputs, "accepted_copyedited_baseline")
    proof = _optional_record(inputs, "proof")
    if baseline is None:
        blockers.append("approved_baseline")
    if accepted is None or accepted.get("accepted") is not True:
        blockers.append("accepted_copyedited_baseline")
    if proof is None:
        blockers.append("proof")

    proof_fixity = inputs.get("proof_fixity")
    if proof_fixity is None or not isinstance(proof_fixity, dict):
        blockers.append("proof_fixity")
    else:
        verified = proof_fixity.get("verified") is True
        fixity_sha = proof_fixity.get("sha256")
        if not isinstance(fixity_sha, str) or SHA256_RE.fullmatch(fixity_sha) is None:
            verified = False
        if proof is not None and fixity_sha != proof["sha256"]:
            verified = False
        if not verified:
            blockers.append("proof_fixity")

    # Keep blocker order stable even if a malformed caller repeats a condition.
    blockers = list(dict.fromkeys(blockers))
    status = "ready_for_comparison" if not blockers else "blocked_input"
    bindings: dict[str, str] = {}
    for key, record in (
        ("approved_baseline", baseline),
        ("accepted_copyedited_baseline", accepted),
        ("proof", proof),
    ):
        if record is not None:
            bindings[key] = record["sha256"]
    if isinstance(proof_fixity, dict) and isinstance(proof_fixity.get("sha256"), str):
        bindings["proof_fixity"] = proof_fixity["sha256"]

    result: dict[str, Any] = {
        "schema": PPR_SCHEMA,
        "family_id": "PPR",
        "status": status,
        "blockers": blockers,
        "bindings": bindings,
        "comparison_inputs_complete": not blockers,
        "substantive_call_count": 0,
        "model_call_count": 0,
        "network_call_count": 0,
        "claims": {"proof_clearance": "withheld"},
        "no_editorial_clearance": True,
    }
    if "plan_id" in inputs:
        result["plan_id"] = _digest(inputs["plan_id"], "plan_id")
    return result


def invalidate_for_reproof(result: dict[str, Any], changed_binding: dict[str, Any]) -> dict[str, Any]:
    """Mark a prior result stale while preserving its original plan identity."""

    if not isinstance(result, dict):
        raise AdapterError("result must be an object")
    _digest(result.get("plan_id"), "result.plan_id")
    if not isinstance(changed_binding, dict):
        raise AdapterError("changed_binding must be an object")
    binding_name = _non_empty_string(changed_binding.get("name"), "changed_binding.name")
    invalidated = deepcopy(result)
    existing = invalidated.get("changed_bindings", [])
    if not isinstance(existing, list) or not all(isinstance(item, str) for item in existing):
        raise AdapterError("result.changed_bindings must be a string list")
    invalidated["changed_bindings"] = list(dict.fromkeys([*existing, binding_name]))
    invalidated["status"] = "awaiting_reproof"
    invalidated["stale_result"] = True
    invalidated["reproof_required"] = True
    invalidated["successor_plan_required"] = True
    invalidated["reproof_reason"] = "dependency_binding_changed"
    return invalidated
