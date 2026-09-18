from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design" / "eri-38"
sys.path.insert(0, str(ROOT))

def main() -> int:
    from upress_workbench.eri38.contracts import load_candidate_contract, load_house_contract, reconcile_contracts
    from upress_workbench.eri38.legacy import load_legacy_profile

    house = load_house_contract(DESIGN / "upstream" / "navy_yard.workbench_contract.v1.json")
    candidate = load_candidate_contract(DESIGN / "contract.json")
    report = reconcile_contracts(house, candidate)
    legacy = load_legacy_profile(ROOT)
    result = {
        "schema": "university_press.contract_validation.draft1",
        "status": "pass",
        "house_schema": house["schema"],
        "house_version": house["version"],
        "candidate_status": report["status"],
        "required_amendments": report["required_amendments"],
        "legacy_profile": {
            "workbench_id": legacy["workbench_id"],
            "stage_order": legacy["required_stage_order"],
            "publication_authority": legacy["publication_authority"],
            "limits": legacy["limits"],
        },
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
