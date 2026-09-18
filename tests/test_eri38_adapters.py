from __future__ import annotations

from copy import deepcopy
import unittest

from upress_workbench.eri38.adapters import AdapterError, evaluate_cpr, evaluate_ppr, invalidate_for_reproof


class Eri38AdapterTests(unittest.TestCase):
    def test_cpr_preserves_known_ce_absence_and_withholds_production_claims(self) -> None:
        result = evaluate_cpr(
            {
                "RCI": {"status": "submitted", "coverage": "known"},
                "SEI": {"status": "submitted", "coverage": "known"},
                "CE": {"status": "absent", "reason": "no_adopted_capability"},
                "SGI": {"status": "submitted", "coverage": "known"},
                "TE": {"status": "submitted", "coverage": "known"},
            },
            {
                "required_upstream_families": ["RCI", "SEI"],
                "copyediting": "absent",
            },
        )

        self.assertEqual(result["status"], "hold")
        self.assertEqual(result["coverage"], "known")
        self.assertEqual(result["absent_dependencies"], ["CE"])
        self.assertEqual(result["missing_dependencies"], [])
        self.assertEqual(result["not_run_dependencies"], [])
        self.assertEqual(result["substitutions"], [])
        self.assertEqual(result["claims"]["copyedited"], "withheld")
        self.assertEqual(result["claims"]["production_ready"], "withheld")
        self.assertTrue(result["ce_gap_visible"])

    def test_cpr_reports_missing_upstream_without_using_sgi_or_te_as_ce(self) -> None:
        result = evaluate_cpr(
            {
                "SGI": {"status": "submitted", "coverage": "known"},
                "TE": {"status": "submitted", "coverage": "known"},
            },
            {
                "required_upstream_families": ["RCI", "SEI"],
                "copyediting": "absent",
            },
        )

        self.assertEqual(result["status"], "blocked_input")
        self.assertEqual(result["coverage"], "unknown")
        self.assertEqual(result["missing_dependencies"], ["RCI", "SEI"])
        self.assertEqual(result["not_run_dependencies"], ["RCI", "SEI"])
        self.assertEqual(result["absent_dependencies"], ["CE"])
        self.assertEqual(result["substitutions"], [])
        self.assertEqual(result["claims"]["copyedited"], "withheld")

    def test_ppr_blocks_without_accepted_copyedited_baseline_and_proof_fixity(self) -> None:
        result = evaluate_ppr(
            {
                "approved_baseline": {"id": "ms-1", "sha256": "a" * 64},
                "proof": {"id": "proof-1", "sha256": "b" * 64},
            }
        )

        self.assertEqual(result["status"], "blocked_input")
        self.assertEqual(
            result["blockers"],
            ["accepted_copyedited_baseline", "proof_fixity"],
        )
        self.assertEqual(result["substantive_call_count"], 0)
        self.assertEqual(result["model_call_count"], 0)
        self.assertEqual(result["claims"]["proof_clearance"], "withheld")

    def test_ppr_accepts_fixity_for_comparison_but_does_not_clear_proof(self) -> None:
        result = evaluate_ppr(
            {
                "approved_baseline": {"id": "ms-1", "sha256": "a" * 64},
                "accepted_copyedited_baseline": {
                    "id": "ce-1",
                    "sha256": "c" * 64,
                    "accepted": True,
                },
                "proof": {"id": "proof-1", "sha256": "b" * 64},
                "proof_fixity": {"verified": True, "sha256": "b" * 64},
            }
        )

        self.assertEqual(result["status"], "ready_for_comparison")
        self.assertEqual(result["blockers"], [])
        self.assertEqual(result["substantive_call_count"], 0)
        self.assertEqual(result["claims"]["proof_clearance"], "withheld")

    def test_reproof_invalidation_preserves_old_result_and_plan_id(self) -> None:
        result = {
            "schema": "university_press.ppr_result.draft1",
            "plan_id": "d" * 64,
            "status": "ready_for_comparison",
            "bindings": {"proof": "b" * 64},
        }
        original = deepcopy(result)

        invalidated = invalidate_for_reproof(
            result,
            {"name": "proof", "old_sha256": "b" * 64, "new_sha256": "e" * 64},
        )

        self.assertEqual(result, original)
        self.assertEqual(invalidated["plan_id"], result["plan_id"])
        self.assertEqual(invalidated["status"], "awaiting_reproof")
        self.assertTrue(invalidated["successor_plan_required"])
        self.assertTrue(invalidated["reproof_required"])
        self.assertEqual(invalidated["changed_bindings"], ["proof"])
        self.assertEqual(invalidated["bindings"]["proof"], "b" * 64)

    def test_adapters_reject_malformed_inputs(self) -> None:
        with self.assertRaises(AdapterError):
            evaluate_cpr([], {})
        with self.assertRaises(AdapterError):
            evaluate_ppr({"proof": {"id": "proof", "sha256": "not-a-digest"}})
        with self.assertRaises(AdapterError):
            invalidate_for_reproof({}, {"name": "proof"})


if __name__ == "__main__":
    unittest.main()
