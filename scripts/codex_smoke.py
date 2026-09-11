from __future__ import annotations

import argparse

from upress_workbench.provider import CallBudget, CodexCliClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one minimal live call through the guarded Codex provider.")
    parser.add_argument("--model", default="default")
    args = parser.parse_args()
    schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "marker"],
        "properties": {
            "status": {"type": "string", "enum": ["ready"]},
            "marker": {"type": "string", "enum": ["codex-provider-smoke"]},
        },
    }
    client = CodexCliClient(args.model, CallBudget(max_calls=1, max_input_chars=10_000), timeout=180)
    result, usage = client.complete_json(
        "Return the exact JSON object requested. Do not use tools.",
        '{"requested":{"status":"ready","marker":"codex-provider-smoke"}}',
        "codex_provider_smoke",
        schema,
    )
    if result != {"status": "ready", "marker": "codex-provider-smoke"}:
        raise RuntimeError("Codex provider smoke response did not match the expected object.")
    print(f"Codex provider smoke passed (model request: {usage['model']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
