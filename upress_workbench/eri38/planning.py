from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .canonical import canonical_sha256, file_sha256, load_json


SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
REQUEST_FIELDS = {
    "schema",
    "stage_profile",
    "manifest_sha256",
    "classification",
    "mode",
    "chapters",
    "context_refs",
    "authority_refs",
    "output_root_ref",
}
CONTEXT_FIELDS = {"rules", "source_permissions", "policy", "stage_inputs"}
AUTHORITY_FIELDS = {"dock_lineage", "G0", "G1", "route_approval", "pin_approval"}
MAX_CHAPTERS = 250
MAX_CHAPTER_BYTES = 20 * 1024 * 1024
MAX_BATCH_BYTES = 500 * 1024 * 1024


class PlanningError(ValueError):
    """Raised when a request cannot become a deterministic candidate plan."""


def _require_sha(value: Any, label: str) -> None:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise PlanningError(f"{label} must be a lowercase SHA-256 digest")


def _load_runtime_data(design_root: Path) -> dict[str, Any]:
    data = load_json(design_root / "runtime-selective-profiles.json")
    if data.get("schema") != "university_press.runtime_selective_profiles.draft1":
        raise PlanningError("runtime selective profile schema is not admitted")
    if data.get("status") != "implementation_extension_not_owner_adopted":
        raise PlanningError("runtime selective profile adoption state changed")
    return data


def stage_catalog(design_root: Path) -> dict[str, dict[str, Any]]:
    data = _load_runtime_data(design_root)
    return data["stage_catalog"]


def _validate_chapters(chapters: Any) -> list[dict[str, Any]]:
    if not isinstance(chapters, list) or not chapters:
        raise PlanningError("chapters must be a non-empty list")
    if len(chapters) > MAX_CHAPTERS:
        raise PlanningError("BATCH_LIMIT: chapter count exceeds 250")
    seen: set[str] = set()
    total_bytes = 0
    normalized: list[dict[str, Any]] = []
    required = {"chapter_id", "volume_id", "order", "source_capture_uri", "source_sha256", "bytes"}
    for chapter in chapters:
        if not isinstance(chapter, dict) or set(chapter) != required:
            raise PlanningError("each chapter must use the closed synthetic chapter shape")
        chapter_id = chapter["chapter_id"]
        if not isinstance(chapter_id, str) or not chapter_id or chapter_id in seen:
            raise PlanningError("chapter IDs must be non-empty and unique")
        seen.add(chapter_id)
        if not isinstance(chapter["volume_id"], str) or not chapter["volume_id"]:
            raise PlanningError("volume_id must be a non-empty string")
        if not isinstance(chapter["order"], int) or isinstance(chapter["order"], bool) or chapter["order"] < 1:
            raise PlanningError("chapter order must be a positive integer")
        if not isinstance(chapter["source_capture_uri"], str) or not chapter["source_capture_uri"].startswith("synthetic://"):
            raise PlanningError("RESTRICTED_INPUT: only synthetic capture URIs are admitted by this slice")
        _require_sha(chapter["source_sha256"], f"{chapter_id}.source_sha256")
        size = chapter["bytes"]
        if not isinstance(size, int) or isinstance(size, bool) or size < 0 or size > MAX_CHAPTER_BYTES:
            raise PlanningError(f"{chapter_id}.bytes exceeds the inherited per-piece limit")
        total_bytes += size
        normalized.append(dict(chapter))
    if total_bytes > MAX_BATCH_BYTES:
        raise PlanningError("BATCH_LIMIT: aggregate bytes exceed 500 MiB")
    return sorted(normalized, key=lambda item: (item["volume_id"], item["order"], item["chapter_id"]))


def validate_batch_request(request: dict[str, Any]) -> list[dict[str, Any]]:
    if not isinstance(request, dict):
        raise PlanningError("request must be an object")
    unknown = sorted(set(request).difference(REQUEST_FIELDS))
    if unknown:
        raise PlanningError(f"INVALID_REQUEST: unknown fields: {', '.join(unknown)}")
    missing = sorted(REQUEST_FIELDS.difference(request))
    if missing:
        raise PlanningError(f"INVALID_REQUEST: missing fields: {', '.join(missing)}")
    if request["schema"] != "university_press.batch_request.draft1":
        raise PlanningError("INVALID_REQUEST: unsupported batch request schema")
    if request["classification"] != "synthetic":
        raise PlanningError("REAL_SAMPLE_AUTHORIZATION_REQUIRED: this implementation slice is synthetic-only")
    if request["mode"] not in {"design_simulation", "diagnostic_review"}:
        raise PlanningError("INVALID_REQUEST: unsupported mode")
    _require_sha(request["manifest_sha256"], "manifest_sha256")
    if not isinstance(request["stage_profile"], str) or not request["stage_profile"]:
        raise PlanningError("stage_profile must be a non-empty string")
    if not isinstance(request["context_refs"], dict) or set(request["context_refs"]) != CONTEXT_FIELDS:
        raise PlanningError("context_refs must use the closed context shape")
    if not all(isinstance(request["context_refs"][key], str) and request["context_refs"][key] for key in {"rules", "source_permissions", "policy"}):
        raise PlanningError("context references must be non-empty strings")
    if not isinstance(request["context_refs"]["stage_inputs"], list) or not all(isinstance(item, str) and item for item in request["context_refs"]["stage_inputs"]):
        raise PlanningError("stage_inputs must be a non-empty string list")
    if not isinstance(request["authority_refs"], dict) or set(request["authority_refs"]) != AUTHORITY_FIELDS:
        raise PlanningError("authority_refs must use the closed authority shape")
    if not all(value is None or isinstance(value, str) for value in request["authority_refs"].values()):
        raise PlanningError("authority references must be strings or null")
    if not isinstance(request["output_root_ref"], str) or not request["output_root_ref"]:
        raise PlanningError("output_root_ref must be a non-empty string")
    return _validate_chapters(request["chapters"])


def _topological_stage_ids(catalog: dict[str, dict[str, Any]], stage_ids: set[str]) -> list[str]:
    pending = set(stage_ids)
    ordered: list[str] = []
    while pending:
        ready = sorted(stage_id for stage_id in pending if set(catalog[stage_id].get("depends_on", [])).isdisjoint(pending))
        if not ready:
            raise PlanningError("DAG_CYCLE: selected stage profile contains a cycle")
        ordered.extend(ready)
        pending.difference_update(ready)
    return ordered


def _node(template: dict[str, Any], node_id: str, depends_on: list[str], claim_scope: str) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "family_id": template["family_id"],
        "capability_id": template["capability_id"],
        "scope": template["scope"],
        "depends_on": sorted(set(depends_on)),
        "hard_preconditions": template["hard_preconditions"],
        "expected_output": template["expected_output"],
        "claim_scope": [claim_scope],
        "kind": template["kind"],
        "lane_class": template["lane_class"],
        "operation": template["operation"],
        "dispatchable": template["dispatchable"],
    }


def _stable_topological_nodes(nodes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    remaining = set(nodes)
    emitted: list[str] = []
    while remaining:
        ready = sorted(
            node_id
            for node_id in remaining
            if set(nodes[node_id]["depends_on"]).issubset(set(emitted))
        )
        if not ready:
            raise PlanningError("DAG_CYCLE: node dependency graph cannot be ordered")
        emitted.extend(ready)
        remaining.difference_update(ready)
    return [nodes[node_id] for node_id in emitted]


def plan_request(request: dict[str, Any], design_root: Path, repo_root: Path) -> dict[str, Any]:
    chapters = validate_batch_request(request)
    data = _load_runtime_data(design_root)
    catalog = data["stage_catalog"]
    profiles = data["profiles"]
    profile_id = request["stage_profile"]
    if profile_id not in profiles:
        raise PlanningError(f"UNKNOWN_STAGE_PROFILE: {profile_id}")
    profile = profiles[profile_id]
    target_ids = set(profile["target_stage_ids"])
    included_ids = target_ids.union(profile.get("include_absent_prerequisites", []))
    for stage_id in included_ids:
        if stage_id not in catalog:
            raise PlanningError(f"UNKNOWN_STAGE: {stage_id}")
    changed = True
    while changed:
        changed = False
        for stage_id in tuple(sorted(included_ids)):
            for dependency in catalog[stage_id].get("depends_on", []):
                if dependency not in catalog:
                    raise PlanningError(f"UNKNOWN_STAGE: {dependency}")
                if dependency not in included_ids:
                    included_ids.add(dependency)
                    changed = True
    ordered_stage_ids = _topological_stage_ids(catalog, included_ids)

    claim_scope = profile["claim_scope"]
    nodes: dict[str, dict[str, Any]] = {}
    nodes["source"] = _node(
        {
            "family_id": "EQA",
            "capability_id": "editorial_control",
            "scope": "batch",
            "hard_preconditions": ["source_digest_matches", "private_output_root"],
            "expected_output": "family_result",
            "kind": "machine",
            "lane_class": "offline_batch",
            "operation": "inventory",
            "dispatchable": False,
        },
        "source",
        [],
        claim_scope,
    )
    nodes["context"] = _node(
        {
            "family_id": "EQA",
            "capability_id": "editorial_control",
            "scope": "batch",
            "hard_preconditions": ["approved_policy_or_explicit_unknown"],
            "expected_output": "family_result",
            "kind": "machine",
            "lane_class": "offline_batch",
            "operation": "resolve_context",
            "dispatchable": False,
        },
        "context",
        ["source"],
        claim_scope,
    )
    for chapter in chapters:
        piece_id = chapter["chapter_id"]
        for stage_id in ordered_stage_ids:
            template = catalog[stage_id]
            node_id = f"stage-{stage_id}-{piece_id}"
            dependencies = ["context"]
            dependencies.extend(f"stage-{dependency}-{piece_id}" for dependency in template.get("depends_on", []))
            nodes[node_id] = _node(template, node_id, dependencies, claim_scope)

    chapter_descriptor = {"chapters": chapters}
    binding_states = {
        "manifest": "known",
        "capability_map": "known",
        "profile": "known",
        "source_bundle": "known",
        "rules": "unknown",
        "policy": "unknown",
        "route": "unknown",
        "specification": "known",
        "lock": "known",
        "authority": "unknown",
        "format_targets": "unknown",
        "baseline": "not_applicable",
        "proof": "not_applicable",
    }
    bindings = {
        "manifest": request["manifest_sha256"],
        "capability_map": file_sha256(design_root / "capability-map.json"),
        "profile": canonical_sha256(profile),
        "source_bundle": canonical_sha256(chapter_descriptor),
        "rules": None,
        "policy": None,
        "route": None,
        "specification": file_sha256(design_root / "stage-profiles.json"),
        "lock": file_sha256(repo_root / "skills.lock.json"),
        "authority": None,
        "format_targets": None,
        "baseline": None,
        "proof": None,
    }
    missing_capabilities = sorted({catalog[stage_id]["capability_id"] for stage_id in included_ids if catalog[stage_id].get("absent")})
    awaiting_inputs = ["real_execution_authorization", "authenticated_routes"]
    if "6" in included_ids:
        awaiting_inputs.append("component_profile_approval")
    plan = {
        "schema": "university_press.stage_plan.draft1",
        "status": "candidate",
        "execution_authorized": False,
        "mode": request["mode"],
        "profile_id": profile_id,
        "bindings": bindings,
        "binding_states": binding_states,
        "parent_plan_id": None,
        "proof_cycle": 0,
        "reuse_descriptors": [],
        "chapter_ids": [chapter["chapter_id"] for chapter in chapters],
        "nodes": _stable_topological_nodes(nodes),
        "missing_capabilities": missing_capabilities,
        "awaiting_inputs": sorted(set(awaiting_inputs)),
        "promotion": "none",
    }
    plan["plan_id"] = canonical_sha256(plan)
    return plan
