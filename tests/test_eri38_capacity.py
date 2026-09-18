from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from upress_workbench.eri38.capacity import CapacityError, admit_tasks, default_capacity_policy, simulate_review
from upress_workbench.eri38.planning import plan_request


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design" / "eri-38"


def synthetic_request(profile: str, count: int) -> dict:
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


def synthetic_plan(profile: str, count: int) -> dict:
    return plan_request(synthetic_request(profile, count), DESIGN, ROOT)


class Eri38CapacityTests(unittest.TestCase):
    def test_default_policy_preserves_adaptive_and_human_boundaries(self) -> None:
        policy = default_capacity_policy()

        self.assertEqual(policy["parallelism"], {"minimum": 1, "maximum": 3, "default": 1})
        self.assertEqual(policy["human_review_budget_per_day"], 12)
        self.assertEqual(policy["queue_saturation"], "wait")
        self.assertFalse(policy["human_nodes_dispatchable"])
        self.assertFalse(policy["model_calls_allowed"])
        self.assertFalse(policy["network_calls_allowed"])

    def test_ten_piece_admission_reduces_to_available_slots_without_losing_scope(self) -> None:
        plan = synthetic_plan("selective_stages_1_5_6", 10)

        admission = admit_tasks(
            plan,
            {
                "requested_parallelism": 3,
                "available_slots": 2,
                "human_review_budget_remaining": 12,
            },
        )

        self.assertEqual(admission["status"], "simulation")
        self.assertEqual(admission["candidate_machine_task_count"], 40)
        self.assertEqual(admission["effective_parallelism"], 2)
        self.assertEqual(len(admission["admitted_task_refs"]), 2)
        self.assertEqual(len(admission["waiting_task_refs"]), 38)
        self.assertEqual(admission["human_wait_refs"], [])
        self.assertEqual(admission["human_review_budget_remaining"], 12)
        self.assertEqual(admission["model_call_count"], 0)
        self.assertEqual(admission["network_call_count"], 0)
        self.assertTrue(admission["scope_preserved"])
        self.assertTrue(admission["no_external_effects"])

    def test_human_nodes_wait_even_when_capacity_is_available(self) -> None:
        plan = synthetic_plan("single_piece_style_review", 1)
        human_node = {
            "node_id": "human-acceptance",
            "family_id": "EQA",
            "capability_id": "human_acceptance",
            "scope": "batch",
            "depends_on": [],
            "hard_preconditions": ["authenticated_human_authority"],
            "expected_output": "decision_receipt",
            "claim_scope": ["bounded_style_review"],
            "kind": "human",
            "lane_class": "human",
            "operation": "approve_release_package",
            "dispatchable": False,
        }
        plan["nodes"].append(human_node)

        admission = admit_tasks(
            plan,
            {
                "requested_parallelism": 3,
                "available_slots": 3,
                "human_review_budget_remaining": 0,
            },
        )

        self.assertEqual(admission["human_wait_refs"], ["human-acceptance"])
        self.assertEqual(admission["human_dispatch_count"], 0)
        self.assertEqual(admission["human_review_items_requested"], 1)
        self.assertEqual(admission["human_review_budget_remaining"], 0)
        self.assertEqual(admission["waiting_reason_counts"]["human_lane"], 1)

    def test_simulated_review_emits_receipt_without_execution_side_effects(self) -> None:
        plan = synthetic_plan("single_piece_style_review", 1)

        result = simulate_review(
            plan,
            {
                "requested_parallelism": 3,
                "available_slots": 3,
                "human_review_budget_remaining": 12,
            },
        )

        receipt = result["receipt"]
        self.assertEqual(receipt["schema"], "university_press.review_receipt.draft1")
        self.assertEqual(receipt["plan_id"], plan["plan_id"])
        self.assertEqual(receipt["outcome"], "submitted")
        self.assertEqual(len(receipt["task_refs"]), 2)
        self.assertEqual(receipt["human_wait_refs"], [])
        self.assertEqual(receipt["blocked_node_ids"], [])
        self.assertEqual(receipt["kata_projection"], "pending")
        self.assertEqual(result["admission"]["model_call_count"], 0)
        self.assertEqual(result["admission"]["network_call_count"], 0)

    def test_capacity_rejects_invalid_slot_values(self) -> None:
        plan = synthetic_plan("single_piece_style_review", 1)

        with self.assertRaises(CapacityError):
            admit_tasks(plan, {"requested_parallelism": 0, "available_slots": 1})
        with self.assertRaises(CapacityError):
            admit_tasks(plan, {"requested_parallelism": 1, "available_slots": -1})

    def test_admission_does_not_mutate_plan(self) -> None:
        plan = synthetic_plan("single_piece_style_review", 1)
        original = deepcopy(plan)

        admit_tasks(plan, {"requested_parallelism": 1, "available_slots": 1})

        self.assertEqual(plan, original)


if __name__ == "__main__":
    unittest.main()
