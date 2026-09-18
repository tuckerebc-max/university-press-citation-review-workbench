# ERI-38 University Press design candidate

Start with `UNIVERSITY_PRESS_DESIGN.md`. It contains the architecture recommendation, evidence differences, authority boundaries and decisions retained for Eric.

The machine-readable design is `contract.json`, `capability-map.json`, `stage-profiles.json`, `open-hooks.json` and `schemas/`. `examples/` contains content-free synthetic plans and deliberate invalid inputs. `conformance/cases.json` specifies the later adapter/runtime gates. `VERIFICATION.json` records only the design checks actually run.

This is a design package, not an installed CLI or executed manuscript review. All present editorial packages remain 0.1.0 draft. The exact house v1 schema remains unavailable. Nothing was pushed to GitHub or changed in the source repositories.

To reproduce design checks in an environment with Python 3.11+ and `jsonschema==4.26.0`:

```bash
python tools/validate_design.py
```

The command prints one JSON result. Exit 0 means this packet's design checks passed; it does not mean adapter, editorial or runtime conformance passed. See the unrun gates in that result.

`GITHUB_HANDOFF.md` explains candidate placement and the source dependencies to resolve before implementation.
