from __future__ import annotations

from pathlib import Path
from typing import Any

from .canonical import canonical_sha256, load_json


def load_legacy_profile(repo_root: Path) -> dict[str, Any]:
    """Bind the shipped Codex workbench without changing its implementation."""

    configuration = load_json(repo_root / "config" / "workbench-configuration.json")
    skills = load_json(repo_root / "skills.lock.json")
    constitution = load_json(repo_root / "config" / "company-constitution.json")
    return {
        "schema": "university_press.legacy_profile.draft1",
        "workbench_id": configuration["workbench_id"],
        "status": configuration["status"],
        "required_stage_order": configuration["required_stage_order"],
        "fixed_gates": configuration["fixed_gates"],
        "adaptive_ranges": configuration["adaptive_ranges"],
        "source_formats": [".docx", ".md", ".txt"],
        "limits": {
            "max_file_bytes": 20 * 1024 * 1024,
            "max_total_bytes": 500 * 1024 * 1024,
            "max_chapters": 250,
            "max_model_calls": 600,
            "max_windows_output_path_chars": 240,
        },
        "skill_lock": skills["skills"],
        "publication_authority": configuration["publication_authority"],
        "reserved_human_decisions": constitution["reserved_human_decisions"],
        "config_sha256": canonical_sha256(configuration),
        "skill_lock_sha256": canonical_sha256(skills),
        "constitution_sha256": canonical_sha256(constitution),
    }
