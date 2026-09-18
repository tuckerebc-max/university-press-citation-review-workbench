from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from upress_workbench.eri38.canonical import canonical_bytes, file_sha256
from upress_workbench.eri38.capacity import simulate_review
from upress_workbench.eri38.planning import plan_request


def synthetic_request(profile: str, count: int) -> dict[str, Any]:
    chapters = [
        {
            "chapter_id": f"PIECE-{index:03d}",
            "volume_id": "SYNTHETIC-VOLUME",
            "order": index,
            "source_capture_uri": f"synthetic://piece/PIECE-{index:03d}",
            "source_sha256": f"{index:064x}"[-64:],
            "bytes": 1024,
        }
        for index in range(1, count + 1)
    ]
    return {
        "schema": "university_press.batch_request.draft1",
        "stage_profile": profile,
        "manifest_sha256": "1" * 64,
        "classification": "synthetic",
        "mode": "design_simulation",
        "chapters": chapters,
        "context_refs": {
            "rules": "synthetic://rules",
            "source_permissions": "synthetic://permissions",
            "policy": "synthetic://policy",
            "stage_inputs": ["synthetic://context"],
        },
        "authority_refs": {
            "dock_lineage": None,
            "G0": None,
            "G1": None,
            "route_approval": None,
            "pin_approval": None,
        },
        "output_root_ref": "synthetic://private-output",
    }


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical_bytes(value) + b"\n")


def _family_counts(plan: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in plan["nodes"]:
        if node["node_id"].startswith("stage-"):
            family_id = node["family_id"]
            counts[family_id] = counts.get(family_id, 0) + 1
    return dict(sorted(counts.items()))


def _shape_summary(
    plan: dict[str, Any],
    simulation: dict[str, Any],
    *,
    requested_stage_ids: list[int],
) -> dict[str, Any]:
    admission = simulation["admission"]
    receipt = simulation["receipt"]
    return {
        "piece_count": len(plan["chapter_ids"]),
        "requested_stage_ids": requested_stage_ids,
        "stage_family_counts": _family_counts(plan),
        "execution_authorized": plan["execution_authorized"],
        "candidate_machine_task_count": admission["candidate_machine_task_count"],
        "effective_parallelism": admission["effective_parallelism"],
        "admitted_task_count": len(admission["admitted_task_refs"]),
        "waiting_task_count": len(admission["waiting_task_refs"]),
        "human_wait_count": len(admission["human_wait_refs"]),
        "outcome": receipt["outcome"],
        "plan_id": plan["plan_id"],
        "run_ref": receipt["run_ref"],
    }


def run_demo(output_root: Path) -> dict[str, Any]:
    output_root = output_root.resolve()
    if output_root == ROOT or ROOT in output_root.parents:
        raise ValueError("demo output must be outside the repository")
    output_root.mkdir(parents=True, exist_ok=True)

    ten_request = synthetic_request("selective_stages_1_5_6", 10)
    ten_plan = plan_request(ten_request, ROOT / "design" / "eri-38", ROOT)
    ten_review = simulate_review(
        ten_plan,
        {
            "requested_parallelism": 3,
            "available_slots": 2,
            "human_review_budget_remaining": 12,
            "capacity_source": "synthetic_local_demo",
        },
    )

    style_request = synthetic_request("single_piece_style_review", 1)
    style_plan = plan_request(style_request, ROOT / "design" / "eri-38", ROOT)
    style_review = simulate_review(
        style_plan,
        {
            "requested_parallelism": 3,
            "available_slots": 3,
            "human_review_budget_remaining": 12,
            "capacity_source": "synthetic_local_demo",
        },
    )

    artifacts = {
        "ten-request.json": ten_request,
        "ten-plan.json": ten_plan,
        "ten-review.json": ten_review,
        "style-request.json": style_request,
        "style-plan.json": style_plan,
        "style-review.json": style_review,
    }
    for name, value in artifacts.items():
        _write_json(output_root / name, value)

    summary: dict[str, Any] = {
        "schema": "university_press.eri38_demo_summary.draft1",
        "status": "synthetic_only",
        "ten_piece": _shape_summary(ten_plan, ten_review, requested_stage_ids=[1, 5, 6]),
        "style_piece": _shape_summary(style_plan, style_review, requested_stage_ids=[2]),
        "model_call_count": ten_review["admission"]["model_call_count"] + style_review["admission"]["model_call_count"],
        "network_call_count": ten_review["admission"]["network_call_count"] + style_review["admission"]["network_call_count"],
        "external_effects": False,
        "artifact_files": [
            {"name": name, "sha256": file_sha256(output_root / name)}
            for name in sorted(artifacts)
        ],
    }
    _write_json(output_root / "summary.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the ERI-38 content-free synthetic demonstration")
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args(argv)
    summary = run_demo(args.output_root)
    sys.stdout.buffer.write(canonical_bytes(summary) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
