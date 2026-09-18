from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .adapters import AdapterError
from .canonical import canonical_bytes, canonical_sha256, file_sha256, load_json
from .capacity import CapacityError, default_capacity_policy, simulate_review
from .contracts import ContractError, load_candidate_contract, load_house_contract, reconcile_contracts
from .legacy import load_legacy_profile
from .planning import PlanningError, plan_request


REPLY_SCHEMA = "university_press.reply.draft1"
FAMILY_IDS = {"RCI", "SGI", "TE", "CE", "SEI", "CPR", "PPR", "EQA"}
HUMAN_VERBS = {"seal", "record-decision"}
UNIMPLEMENTED_VERBS = {"reconcile", "inspect"}


ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "design" / "eri-38"


class CliError(ValueError):
    def __init__(self, code: str, rule_id: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.rule_id = rule_id


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON value: {value}")


def _read_request(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise CliError("INVALID_REQUEST", "UPW-01")
    try:
        parsed = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_pairs,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        raise CliError("INVALID_REQUEST", "UPW-01") from exc
    if not isinstance(parsed, dict):
        raise CliError("INVALID_REQUEST", "UPW-01")
    return parsed


def _require_closed(request: dict[str, Any], fields: set[str]) -> None:
    unknown = set(request).difference(fields)
    if unknown:
        raise CliError("INVALID_REQUEST", "UPW-01")


def _digest(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _ref(value: Any) -> None:
    if not isinstance(value, dict) or not isinstance(value.get("capture_uri"), str) or not value["capture_uri"] or not _digest(value.get("sha256")):
        raise CliError("INVALID_REQUEST", "UPW-03")


def _declare(request: dict[str, Any]) -> dict[str, Any]:
    _require_closed(request, set())
    try:
        candidate_path = DESIGN / "contract.json"
        house_path = DESIGN / "upstream" / "navy_yard.workbench_contract.v1.json"
        map_path = DESIGN / "capability-map.json"
        candidate = load_candidate_contract(candidate_path)
        house = load_house_contract(house_path)
        reconciliation = reconcile_contracts(house, candidate)
        legacy = load_legacy_profile(ROOT)
        capability_map = load_json(map_path)
    except (OSError, ContractError, ValueError) as exc:
        raise CliError("TECHNICAL_FAILURE") from exc
    return {
        "schema": "university_press.declaration.draft1",
        "candidate_conformance": reconciliation["status"],
        "candidate_contract_sha256": file_sha256(candidate_path),
        "house_contract": {
            "schema": house["schema"],
            "version": house["version"],
            "sha256": file_sha256(house_path),
        },
        "capability_map": {
            "map_id": capability_map["map_id"],
            "sha256": file_sha256(map_path),
            "domain_families": capability_map["domain_families"],
            "authority": capability_map["authority"],
        },
        "legacy": {
            "required_stage_order": legacy["required_stage_order"],
            "adaptive_ranges": legacy["adaptive_ranges"],
            "limits": legacy["limits"],
            "publication_authority": legacy["publication_authority"],
        },
        "capacity_policy": default_capacity_policy(),
        "execution_authorized": False,
        "maturity": {
            "design": "candidate",
            "runtime": "synthetic_slice_only",
            "production": "not_eligible",
        },
    }


def _plan(request: dict[str, Any]) -> dict[str, Any]:
    try:
        return plan_request(request, DESIGN, ROOT)
    except PlanningError as exc:
        code = str(exc).split(":", 1)[0]
        if not code.isupper() or not code.replace("_", "").isalnum():
            code = "INVALID_REQUEST"
        raise CliError(code, "UPW-01") from exc
    except (OSError, ValueError) as exc:
        raise CliError("TECHNICAL_FAILURE") from exc


def _review(request: dict[str, Any]) -> dict[str, Any]:
    expected = {"schema", "plan", "capacity"}
    _require_closed(request, expected)
    if request.get("schema") != "university_press.synthetic_review_request.draft1":
        raise CliError("INVALID_REQUEST", "UPW-01")
    if not isinstance(request.get("plan"), dict) or not isinstance(request.get("capacity"), dict):
        raise CliError("INVALID_REQUEST", "UPW-01")
    try:
        return simulate_review(request["plan"], request["capacity"])
    except (CapacityError, ValueError) as exc:
        raise CliError("INVALID_REQUEST", "UPW-05") from exc


def _conform(request: dict[str, Any]) -> dict[str, Any]:
    fields = {"family_id", "candidate_adapter", "suite", "mode"}
    _require_closed(request, fields)
    if request.get("family_id") not in FAMILY_IDS or request.get("mode") != "synthetic_only":
        raise CliError("INVALID_REQUEST", "UPW-01")
    _ref(request.get("candidate_adapter"))
    suite = request.get("suite")
    _ref(suite)
    suite_path = DESIGN / "conformance" / "cases.json"
    if suite["sha256"] != file_sha256(suite_path):
        raise CliError("SOURCE_DRIFT", "UPW-02")
    suite_data = load_json(suite_path)
    case_results = [
        {"case_id": case_id, "status": "not_run", "evidence_ref": None}
        for case_id in suite_data["critical_case_ids"]
    ]
    return {
        "schema": "university_press.conformance_report.draft1",
        "family_id": request["family_id"],
        "suite_digest": suite["sha256"],
        "case_results": case_results,
        "diagnostic_admission": "unknown",
        "production_clearance": "hold",
    }


def handle_request(verb: str, request: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Handle one parsed request and return a reply plus its process exit code."""

    if verb in HUMAN_VERBS:
        raise CliError("HUMAN_ROUTE_REQUIRED", "UPW-05")
    if verb in UNIMPLEMENTED_VERBS:
        raise CliError("NOT_IMPLEMENTED", None)
    if verb == "declare":
        result = _declare(request)
        unknowns = ["live_runtime_not_run", "human_authority_not_verified"]
    elif verb == "plan":
        result = _plan(request)
        unknowns = list(result["awaiting_inputs"])
    elif verb == "review":
        result = _review(request)
        unknowns = ["synthetic_only", "candidate_plan_not_authorized"]
    elif verb == "conform":
        result = _conform(request)
        unknowns = ["runtime_cases_not_run", "production_editorial_efficacy_not_run"]
    else:
        raise CliError("INVALID_REQUEST", "UPW-01")
    receipt_ref = result.get("receipt", {}).get("run_ref") if verb == "review" else None
    return (
        {
            "schema": REPLY_SCHEMA,
            "verb": verb,
            "request_id": canonical_sha256(request),
            "outcome": "ok",
            "result": result,
            "errors": [],
            "unknowns": sorted(set(unknowns)),
            "receipt_ref": receipt_ref,
        },
        0,
    )


def _error_reply(verb: str, request: dict[str, Any], error: CliError) -> dict[str, Any]:
    return {
        "schema": REPLY_SCHEMA,
        "verb": verb,
        "request_id": canonical_sha256(request),
        "outcome": "technical_failure" if error.code == "TECHNICAL_FAILURE" else "refused",
        "result": None,
        "errors": [
            {
                "code": error.code,
                "rule_id": error.rule_id,
                "object_ref": None,
                "retryable": error.code == "TECHNICAL_FAILURE",
            }
        ],
        "unknowns": [],
        "receipt_ref": None,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="upw")
    parser.add_argument("verb", choices=["declare", "plan", "seal", "review", "reconcile", "record-decision", "inspect", "conform"])
    parser.add_argument("--request", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    path = Path(args.request)
    request_for_error = {"request_path": path.name}
    try:
        request = _read_request(path)
        reply, exit_code = handle_request(args.verb, request)
    except CliError as error:
        reply = _error_reply(args.verb, request if "request" in locals() else request_for_error, error)
        exit_code = 1 if error.code == "TECHNICAL_FAILURE" else 2
    except Exception:
        reply = _error_reply(args.verb, request if "request" in locals() else request_for_error, CliError("TECHNICAL_FAILURE"))
        exit_code = 1
    sys.stdout.buffer.write(canonical_bytes(reply) + b"\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
