from __future__ import annotations

import re
from typing import Any

from .canonical import canonical_sha256


PLAN_ID_RE = re.compile(r"^[a-f0-9]{64}$")
CAPACITY_SCHEMA = "university_press.capacity_admission.draft1"
REVIEW_SCHEMA = "university_press.review_receipt.draft1"
MAX_PARALLELISM = 3
HUMAN_REVIEW_BUDGET = 12


class CapacityError(ValueError):
    """Raised when a synthetic capacity request cannot be admitted safely."""


def default_capacity_policy() -> dict[str, Any]:
    """Return the inherited adaptive policy without adding execution authority."""

    return {
        "schema": "university_press.capacity_policy.draft1",
        "parallelism": {"minimum": 1, "maximum": MAX_PARALLELISM, "default": 1},
        "human_review_budget_per_day": HUMAN_REVIEW_BUDGET,
        "queue_saturation": "wait",
        "human_nodes_dispatchable": False,
        "model_calls_allowed": False,
        "network_calls_allowed": False,
    }


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise CapacityError(f"{label} must be an integer >= {minimum}")
    return value


def _capacity_inputs(capacity: dict[str, Any] | None) -> dict[str, Any]:
    if capacity is None:
        capacity = {}
    if not isinstance(capacity, dict):
        raise CapacityError("capacity must be an object")

    requested = _integer(capacity.get("requested_parallelism", 1), "requested_parallelism", minimum=1)
    available = _integer(capacity.get("available_slots", requested), "available_slots")
    human_remaining = _integer(
        capacity.get("human_review_budget_remaining", HUMAN_REVIEW_BUDGET),
        "human_review_budget_remaining",
    )
    source = capacity.get("capacity_source", "synthetic_local")
    if not isinstance(source, str) or not source:
        raise CapacityError("capacity_source must be a non-empty string")
    return {
        "requested_parallelism": requested,
        "available_slots": available,
        "human_review_budget_remaining": human_remaining,
        "capacity_source": source,
    }


def _plan_nodes(plan: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not isinstance(plan, dict):
        raise CapacityError("plan must be an object")
    if plan.get("schema") != "university_press.stage_plan.draft1":
        raise CapacityError("capacity accepts only a stage plan candidate")
    if plan.get("execution_authorized") is not False:
        raise CapacityError("candidate plan cannot authorize execution")
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or PLAN_ID_RE.fullmatch(plan_id) is None:
        raise CapacityError("plan_id must be a lowercase SHA-256 digest")
    nodes = plan.get("nodes")
    if not isinstance(nodes, list):
        raise CapacityError("plan nodes must be a list")

    machine: list[dict[str, Any]] = []
    human: list[dict[str, Any]] = []
    for node in nodes:
        if not isinstance(node, dict) or not isinstance(node.get("node_id"), str):
            raise CapacityError("each plan node must have a node_id")
        if node.get("kind") == "human" or node.get("lane_class") == "human":
            human.append(node)
        elif node.get("kind") == "machine" and node.get("family_id") != "EQA":
            machine.append(node)
    return machine, human


def _scope_ids(plan: dict[str, Any], node: dict[str, Any]) -> list[str]:
    scope = node.get("scope")
    chapter_ids = plan.get("chapter_ids", [])
    if scope == "chapter":
        suffix = "-" + node["node_id"]
        matches = [chapter_id for chapter_id in chapter_ids if node["node_id"].endswith("-" + chapter_id)]
        if matches:
            return [matches[0]]
        return [node["node_id"]]
    if scope == "batch":
        return list(chapter_ids)
    return [node["node_id"]]


def _task_ref(plan: dict[str, Any], node: dict[str, Any]) -> str:
    return canonical_sha256(
        {
            "plan_id": plan["plan_id"],
            "node_id": node["node_id"],
            "scope": node.get("scope"),
            "scope_ids": _scope_ids(plan, node),
        }
    )


def admit_tasks(plan: dict[str, Any], capacity: dict[str, Any] | None = None) -> dict[str, Any]:
    """Simulate capacity admission for machine stage nodes.

    This function produces candidate task references only. It never dispatches a
    task, consumes a human review budget, invokes a model, or uses the network.
    """

    machine_nodes, human_nodes = _plan_nodes(plan)
    inputs = _capacity_inputs(capacity)
    policy = default_capacity_policy()
    effective = min(inputs["requested_parallelism"], inputs["available_slots"], MAX_PARALLELISM)
    machine_refs = [_task_ref(plan, node) for node in machine_nodes]
    admitted_count = min(effective, len(machine_refs))
    admitted_refs = machine_refs[:admitted_count]
    waiting_refs = machine_refs[admitted_count:]
    admitted_nodes = [node["node_id"] for node in machine_nodes[:admitted_count]]
    waiting_nodes = [node["node_id"] for node in machine_nodes[admitted_count:]]
    human_wait_refs = [node["node_id"] for node in human_nodes]

    reason_counts: dict[str, int] = {}
    if waiting_refs:
        reason_counts["capacity_slots"] = len(waiting_refs)
    if human_wait_refs:
        reason_counts["human_lane"] = len(human_wait_refs)
    return {
        "schema": CAPACITY_SCHEMA,
        "status": "simulation",
        "plan_id": plan["plan_id"],
        "capacity_source": inputs["capacity_source"],
        "policy": policy,
        "requested_parallelism": inputs["requested_parallelism"],
        "available_slots": inputs["available_slots"],
        "effective_parallelism": effective,
        "candidate_machine_task_count": len(machine_refs),
        "admitted_task_refs": admitted_refs,
        "waiting_task_refs": waiting_refs,
        "admitted_node_ids": admitted_nodes,
        "waiting_node_ids": waiting_nodes,
        "human_wait_refs": human_wait_refs,
        "human_review_items_requested": len(human_nodes),
        "human_review_budget_remaining": inputs["human_review_budget_remaining"],
        "human_dispatch_count": 0,
        "waiting_reason_counts": reason_counts,
        "model_call_count": 0,
        "network_call_count": 0,
        "scope_preserved": True,
        "no_external_effects": True,
    }


def simulate_review(plan: dict[str, Any], capacity: dict[str, Any] | None = None) -> dict[str, Any]:
    """Produce a contract-shaped synthetic review receipt and its admission evidence."""

    admission = admit_tasks(plan, capacity)
    if admission["admitted_task_refs"] and (admission["waiting_task_refs"] or admission["human_wait_refs"]):
        outcome = "partial"
    elif admission["admitted_task_refs"]:
        outcome = "submitted"
    elif admission["waiting_task_refs"] or admission["human_wait_refs"]:
        outcome = "waiting"
    else:
        outcome = "blocked"
    run_digest = canonical_sha256({"plan_id": plan["plan_id"], "admission": admission})
    event_digest = canonical_sha256(
        {
            "plan_id": plan["plan_id"],
            "task_refs": admission["admitted_task_refs"],
            "waiting_task_refs": admission["waiting_task_refs"],
            "human_wait_refs": admission["human_wait_refs"],
        }
    )
    receipt = {
        "schema": REVIEW_SCHEMA,
        "plan_id": plan["plan_id"],
        "run_ref": f"synthetic://run/{run_digest}",
        "task_refs": admission["admitted_task_refs"],
        "human_wait_refs": admission["human_wait_refs"],
        "blocked_node_ids": [],
        "outcome": outcome,
        "kata_projection": "pending",
        "event_head": f"synthetic://event/{event_digest}",
    }
    return {"receipt": receipt, "admission": admission}
