from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest

from upress_workbench.eri38.planning import PlanningError, plan_request, stage_catalog


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


class Eri38PlanningTests(unittest.TestCase):
    def test_stage_catalog_is_data_driven(self) -> None:
        catalog = stage_catalog(DESIGN)

        self.assertEqual(catalog["1"]["family_id"], "RCI")
        self.assertEqual(catalog["5"]["family_id"], "SEI")
        self.assertEqual(catalog["6"]["family_id"], "CPR")
        self.assertEqual(catalog["2"]["family_id"], "SGI")

    def test_ten_piece_selective_plan_retains_only_requested_families_and_gaps(self) -> None:
        plan = plan_request(synthetic_request("selective_stages_1_5_6", 10), DESIGN, ROOT)

        self.assertEqual(plan["profile_id"], "selective_stages_1_5_6")
        self.assertEqual(plan["chapter_ids"], [f"PIECE-{index:03d}" for index in range(1, 11)])
        self.assertFalse(plan["execution_authorized"])
        self.assertEqual(plan["promotion"], "none")
        self.assertEqual(plan["binding_states"]["manifest"], "known")
        self.assertEqual(plan["binding_states"]["baseline"], "not_applicable")

        domain_nodes = [node for node in plan["nodes"] if node["node_id"].startswith("stage-")]
        requested_nodes = [node for node in domain_nodes if node["family_id"] in {"RCI", "SEI", "CPR"}]
        self.assertEqual(sum(node["family_id"] == "RCI" for node in requested_nodes), 10)
        self.assertEqual(sum(node["family_id"] == "SEI" for node in requested_nodes), 10)
        self.assertEqual(sum(node["family_id"] == "CPR" for node in requested_nodes), 10)
        self.assertEqual(sum(node["family_id"] == "CE" for node in domain_nodes), 10)
        self.assertEqual({node["family_id"] for node in domain_nodes}, {"RCI", "SEI", "CPR", "CE"})
        self.assertNotIn("SGI", {node["family_id"] for node in domain_nodes})
        self.assertNotIn("TE", {node["family_id"] for node in domain_nodes})
        self.assertNotIn("PPR", {node["family_id"] for node in domain_nodes})
        self.assertIn("copyediting", plan["missing_capabilities"])

        positions = {node["node_id"]: index for index, node in enumerate(plan["nodes"])}
        for node in plan["nodes"]:
            for dependency in node["depends_on"]:
                self.assertLess(positions[dependency], positions[node["node_id"]])

    def test_single_piece_style_profile_adds_only_rci_prerequisite(self) -> None:
        plan = plan_request(synthetic_request("single_piece_style_review", 1), DESIGN, ROOT)

        domain_nodes = [node for node in plan["nodes"] if node["node_id"].startswith("stage-")]
        self.assertEqual(len(domain_nodes), 2)
        self.assertEqual({node["family_id"] for node in domain_nodes}, {"RCI", "SGI"})
        self.assertEqual(plan["chapter_ids"], ["PIECE-001"])
        self.assertEqual(plan["missing_capabilities"], [])

    def test_family_selector_and_non_synthetic_content_are_rejected(self) -> None:
        request = synthetic_request("single_piece_style_review", 1)
        request["family_id"] = "SGI"
        with self.assertRaises(PlanningError):
            plan_request(request, DESIGN, ROOT)

        request = synthetic_request("single_piece_style_review", 1)
        request["chapters"][0]["source_capture_uri"] = "C:/Press/chapter.docx"
        with self.assertRaises(PlanningError):
            plan_request(request, DESIGN, ROOT)

    def test_plan_digest_changes_when_piece_manifest_changes(self) -> None:
        first = plan_request(synthetic_request("single_piece_style_review", 1), DESIGN, ROOT)
        changed = synthetic_request("single_piece_style_review", 1)
        changed["chapters"][0]["source_sha256"] = "f" * 64

        second = plan_request(changed, DESIGN, ROOT)

        self.assertNotEqual(first["plan_id"], second["plan_id"])
        self.assertEqual(first["plan_id"], plan_request(synthetic_request("single_piece_style_review", 1), DESIGN, ROOT)["plan_id"])

    def test_planner_does_not_mutate_request(self) -> None:
        request = synthetic_request("single_piece_style_review", 1)
        original = deepcopy(request)

        plan_request(request, DESIGN, ROOT)

        self.assertEqual(request, original)


if __name__ == "__main__":
    unittest.main()
