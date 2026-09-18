from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

from upress_workbench.eri38.canonical import canonical_sha256
from upress_workbench.eri38.contracts import load_candidate_contract, load_house_contract, reconcile_contracts
from upress_workbench.eri38.legacy import load_legacy_profile


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design" / "eri-38"


class Eri38ContractTests(unittest.TestCase):
    def test_house_contract_is_the_exact_upstream_shape(self) -> None:
        house = load_house_contract(DESIGN / "upstream" / "navy_yard.workbench_contract.v1.json")

        self.assertEqual(house["schema"], "navy_yard.workbench_contract.v1")
        self.assertEqual(house["version"], "0.1.0")
        self.assertEqual(house["humans"], ["eric", "sheryl"])
        self.assertEqual(set(house["lane_classes"]), {"offline_batch", "internet", "chat_reasoning", "human"})
        self.assertEqual(set(house["exit_codes"]), {"0", "1", "2"})
        self.assertIn("contract", house["verbs"])

    def test_reconciliation_keeps_candidate_partial_and_maps_fields(self) -> None:
        house = load_house_contract(DESIGN / "upstream" / "navy_yard.workbench_contract.v1.json")
        candidate = load_candidate_contract(DESIGN / "contract.json")

        report = reconcile_contracts(house, candidate)

        self.assertEqual(report["status"], "partial")
        self.assertNotEqual(report["status"], "conformant")
        mapped = {item["candidate"]: item for item in report["field_mappings"]}
        self.assertEqual(mapped["workbench_id"]["house"], "workbench")
        self.assertEqual(mapped["entry_points"]["disposition"], "named_extension")
        self.assertTrue(report["required_amendments"])
        self.assertEqual(report["house_contract"]["schema"], "navy_yard.workbench_contract.v1")

    def test_canonical_hash_is_stable_and_rejects_non_finite_values(self) -> None:
        self.assertEqual(canonical_sha256({"b": 2, "a": 1}), canonical_sha256({"a": 1, "b": 2}))
        with self.assertRaises(ValueError):
            canonical_sha256({"value": float("nan")})

    def test_legacy_profile_preserves_codex_order_pins_and_limits(self) -> None:
        profile = load_legacy_profile(ROOT)

        self.assertEqual(
            profile["required_stage_order"],
            [
                "source_manifest",
                "reference-citation-integrity",
                "scholarly-editorial-integrity",
                "author_packet",
                "human_acceptance",
            ],
        )
        self.assertEqual(profile["adaptive_ranges"]["parallel_chapters"], {"minimum": 1, "maximum": 3, "default": 1})
        self.assertEqual(profile["limits"], {"max_file_bytes": 20 * 1024 * 1024, "max_total_bytes": 500 * 1024 * 1024, "max_chapters": 250, "max_model_calls": 600, "max_windows_output_path_chars": 240})
        self.assertEqual(profile["source_formats"], [".docx", ".md", ".txt"])
        self.assertEqual(profile["publication_authority"], False)
        self.assertEqual(profile["skill_lock"]["reference-citation-integrity"]["commit"], "a49e9f686898030684134ba7a7f84ac8b68fc4dc")

    def test_house_contract_file_is_json_not_a_candidate_alias(self) -> None:
        raw = json.loads((DESIGN / "upstream" / "navy_yard.workbench_contract.v1.json").read_text(encoding="utf-8"))

        self.assertIn("workbench", raw)
        self.assertIn("verbs", raw)
        self.assertNotIn("workbench_id", raw)

    def test_standalone_contract_validator_runs_from_scripts_directory(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_eri38_contract.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "pass")


if __name__ == "__main__":
    unittest.main()
