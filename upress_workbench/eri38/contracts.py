from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import canonical_sha256, file_sha256, load_json


HOUSE_SCHEMA = "navy_yard.workbench_contract.v1"
HOUSE_VERSION = "0.1.0"
HOUSE_LANES = {"offline_batch", "internet", "chat_reasoning", "human"}
HOUSE_HUMANS = ["eric", "sheryl"]


class ContractError(ValueError):
    """Raised when a contract cannot be admitted at the interface boundary."""


def load_house_contract(path: Path) -> dict[str, Any]:
    contract = load_json(path)
    if contract.get("schema") != HOUSE_SCHEMA:
        raise ContractError(f"house contract schema must be {HOUSE_SCHEMA}")
    if contract.get("version") != HOUSE_VERSION:
        raise ContractError(f"house contract version must be {HOUSE_VERSION}")
    required = {
        "agents",
        "humans",
        "entry_points",
        "exit_codes",
        "lane_classes",
        "verbs",
        "state_layout",
        "ledger_format",
        "invariants",
        "non_claims",
        "emits",
    }
    missing = sorted(required.difference(contract))
    if missing:
        raise ContractError(f"house contract missing required fields: {', '.join(missing)}")
    if contract["humans"] != HOUSE_HUMANS:
        raise ContractError("house contract human authority list changed")
    if set(contract["lane_classes"]) != HOUSE_LANES:
        raise ContractError("house contract lane vocabulary changed")
    if set(contract["exit_codes"]) != {"0", "1", "2"}:
        raise ContractError("house contract must declare exit codes 0, 1 and 2")
    if set(contract["entry_points"]) != {"cli", "tests"}:
        raise ContractError("house contract entry_points must contain cli and tests")
    if not isinstance(contract["verbs"], dict) or "contract" not in contract["verbs"]:
        raise ContractError("house contract must declare its contract verb")
    return contract


def load_candidate_contract(path: Path) -> dict[str, Any]:
    contract = load_json(path)
    if contract.get("schema") != HOUSE_SCHEMA:
        raise ContractError(f"candidate schema must retain {HOUSE_SCHEMA}")
    if "workbench_id" not in contract or "entry_points" not in contract:
        raise ContractError("candidate contract is missing its design identity or entry points")
    return contract


def _contract_descriptor(contract: dict[str, Any], path: Path | None) -> dict[str, Any]:
    return {
        "path": str(path) if path else None,
        "schema": contract.get("schema"),
        "version": contract.get("version"),
        "workbench": contract.get("workbench", contract.get("workbench_id")),
        "sha256": canonical_sha256(contract),
        "file_sha256": file_sha256(path) if path else None,
    }


def reconcile_contracts(house: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    """Return an explicit candidate-to-house reconciliation without relabeling it."""

    if house.get("schema") != HOUSE_SCHEMA:
        raise ContractError("cannot reconcile against a non-house contract")
    if candidate.get("schema") != HOUSE_SCHEMA:
        raise ContractError("candidate schema does not retain the house identifier")
    mappings = [
        {"candidate": "workbench_id", "house": "workbench", "disposition": "mapped"},
        {"candidate": "entry_points", "house": "verbs", "disposition": "named_extension"},
        {"candidate": "stdout", "house": "output", "disposition": "mapped"},
        {"candidate": "ledgers", "house": "ledger_format/state_layout", "disposition": "named_extension"},
        {"candidate": "humans", "house": "humans", "disposition": "identity_not_equated"},
        {"candidate": "rules", "house": "invariants", "disposition": "named_extension"},
    ]
    amendments = [
        "Validate the exact house contract before admitting the University Press extension.",
        "Keep University Press verbs and schemas under a named extension namespace.",
        "Bind the legacy Codex profile to its existing source gates and skill locks.",
        "Obtain owner adoption before activation, new pins, promotion or real-manuscript execution.",
    ]
    return {
        "schema": "university_press.house_contract_reconciliation.draft1",
        "status": "partial",
        "house_contract": _contract_descriptor(house, None),
        "candidate_contract": _contract_descriptor(candidate, None),
        "field_mappings": mappings,
        "required_amendments": amendments,
        "unresolved": [
            "University Press extension adoption",
            "nine local source-tree and remote comparisons",
            "authenticated human authority verifier",
        ],
    }
