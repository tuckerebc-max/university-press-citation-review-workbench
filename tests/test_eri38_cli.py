from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from upress_workbench.eri38.canonical import file_sha256
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


class Eri38CliTests(unittest.TestCase):
    def run_cli(self, verb: str, request: dict) -> tuple[int, dict, str]:
        with tempfile.TemporaryDirectory() as temporary:
            request_path = Path(temporary) / "request.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "upw.py"), verb, "--request", str(request_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(completed.stdout.count("\n"), 1, completed.stdout)
        self.assertEqual(completed.stderr, "", completed.stderr)
        return completed.returncode, json.loads(completed.stdout), completed.stderr

    def test_declare_emits_one_canonical_reply_and_preserves_partial_status(self) -> None:
        code, reply, _ = self.run_cli("declare", {})

        self.assertEqual(code, 0)
        self.assertEqual(reply["schema"], "university_press.reply.draft1")
        self.assertEqual(reply["verb"], "declare")
        self.assertEqual(reply["outcome"], "ok")
        self.assertEqual(reply["result"]["candidate_conformance"], "partial")
        self.assertFalse(reply["result"]["execution_authorized"])
        self.assertEqual(reply["receipt_ref"], None)

    def test_plan_emits_candidate_plan_without_authorization(self) -> None:
        code, reply, _ = self.run_cli("plan", synthetic_request("single_piece_style_review", 1))

        self.assertEqual(code, 0)
        self.assertEqual(reply["outcome"], "ok")
        plan = reply["result"]
        self.assertEqual(plan["schema"], "university_press.stage_plan.draft1")
        self.assertFalse(plan["execution_authorized"])
        self.assertEqual(plan["profile_id"], "single_piece_style_review")
        self.assertEqual(reply["receipt_ref"], None)

    def test_review_synthetic_extension_emits_receipt_and_waits_adaptively(self) -> None:
        plan = plan_request(synthetic_request("selective_stages_1_5_6", 10), DESIGN, ROOT)
        request = {
            "schema": "university_press.synthetic_review_request.draft1",
            "plan": plan,
            "capacity": {
                "requested_parallelism": 3,
                "available_slots": 2,
                "human_review_budget_remaining": 12,
            },
        }

        code, reply, _ = self.run_cli("review", request)

        self.assertEqual(code, 0)
        self.assertEqual(reply["outcome"], "ok")
        self.assertEqual(reply["result"]["receipt"]["outcome"], "partial")
        self.assertEqual(len(reply["result"]["receipt"]["task_refs"]), 2)
        self.assertEqual(len(reply["result"]["admission"]["waiting_task_refs"]), 38)
        self.assertEqual(reply["result"]["admission"]["model_call_count"], 0)
        self.assertEqual(reply["result"]["admission"]["network_call_count"], 0)

    def test_conform_reports_runtime_cases_not_run_and_holds_production(self) -> None:
        suite = DESIGN / "conformance" / "cases.json"
        request = {
            "family_id": "CPR",
            "candidate_adapter": {"capture_uri": "synthetic://adapter/CPR", "sha256": "a" * 64},
            "suite": {"capture_uri": "synthetic://suite/UPW-CONFORMANCE-DRAFT1", "sha256": file_sha256(suite)},
            "mode": "synthetic_only",
        }

        code, reply, _ = self.run_cli("conform", request)

        self.assertEqual(code, 0)
        report = reply["result"]
        self.assertEqual(report["diagnostic_admission"], "unknown")
        self.assertEqual(report["production_clearance"], "hold")
        self.assertEqual(len(report["case_results"]), 24)
        self.assertTrue(all(item["status"] == "not_run" for item in report["case_results"]))

    def test_human_route_is_refused_without_fabricating_authority(self) -> None:
        code, reply, _ = self.run_cli("seal", {})

        self.assertEqual(code, 2)
        self.assertEqual(reply["outcome"], "refused")
        self.assertEqual(reply["result"], None)
        self.assertEqual(reply["errors"][0]["code"], "HUMAN_ROUTE_REQUIRED")

    def test_review_rejects_authorized_plan(self) -> None:
        request = {
            "schema": "university_press.synthetic_review_request.draft1",
            "plan": {
                "schema": "university_press.stage_plan.draft1",
                "plan_id": "a" * 64,
                "execution_authorized": True,
                "nodes": [],
            },
            "capacity": {},
        }

        code, reply, _ = self.run_cli("review", request)

        self.assertEqual(code, 2)
        self.assertEqual(reply["outcome"], "refused")
        self.assertEqual(reply["errors"][0]["code"], "INVALID_REQUEST")

    def test_demo_script_records_both_selective_shapes_in_private_output_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "run_eri38_demo.py"),
                    "--output-root",
                    temporary,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads((Path(temporary) / "summary.json").read_text(encoding="utf-8"))

        self.assertEqual(summary["ten_piece"]["piece_count"], 10)
        self.assertEqual(summary["ten_piece"]["requested_stage_ids"], [1, 5, 6])
        self.assertEqual(summary["ten_piece"]["stage_family_counts"], {"CE": 10, "CPR": 10, "RCI": 10, "SEI": 10})
        self.assertEqual(summary["ten_piece"]["admitted_task_count"], 2)
        self.assertEqual(summary["ten_piece"]["waiting_task_count"], 38)
        self.assertEqual(summary["style_piece"]["stage_family_counts"], {"RCI": 1, "SGI": 1})
        self.assertEqual(summary["style_piece"]["admitted_task_count"], 2)
        self.assertEqual(summary["model_call_count"], 0)
        self.assertEqual(summary["network_call_count"], 0)
        self.assertFalse(summary["external_effects"])

    def test_documentation_states_synthetic_boundary_and_private_verification_import(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        status = (ROOT / "design" / "eri-38" / "IMPLEMENTATION_STATUS.md").read_text(encoding="utf-8")
        cli_source = (ROOT / "upress_workbench" / "eri38" / "cli.py").read_text(encoding="utf-8")

        self.assertIn("upw.py", readme)
        self.assertIn("synthetic", status.lower())
        self.assertIn("execution_authorized: false", status)
        self.assertFalse((ROOT / "design" / "eri-38" / "VERIFICATION.json").exists())
        self.assertNotIn('"publish"', cli_source)


if __name__ == "__main__":
    unittest.main()
