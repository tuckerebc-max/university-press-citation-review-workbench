# ERI-38 contract reconciliation

Status: implementation dependency resolved to a local house-contract capture;
University Press extension adoption remains partial and owner-controlled.

## Evidence identity

| Object | Evidence |
|---|---|
| Candidate archive | `C:\Users\tucke\Downloads\University_Press_ERI38_Design_Candidate_2026-09-18.zip` · SHA-256 `053EDD5753A6FAA766A090B8BF772A4EB9FD8EDF37B3880C57EDD36B650B4A28` |
| Candidate contract | `design/eri-38/contract.json` · SHA-256 `864853E8ACB55F47D89451FBDAE1C51702F60C37B282DCD59638732EEEB22E1D` |
| House contract capture | `design/eri-38/upstream/navy_yard.workbench_contract.v1.json` · SHA-256 `9517D8CFEE285694AC50AA5053A34D60714598EBA4A0018387A64154077EAB73` |
| University Press Codex base | `university-press-citation-review-workbench` · commit `86ca82c2ff02f8bb4af1de73813cacf2783b1863` |
| Separate Lunaroute edition | `university-press-citation-review-workbench-Lunaroute` · commit `822cb00ac7be1b1465f2a26da94bad00d3477648` |
| House-contract source checkout | `C:\Users\tucke\Documents\GitHub\screen-measurement-instrument-quality` · local `contract.json`; no `.git` directory was present |

## Field reconciliation

| Candidate shape | House v1 shape | Disposition |
|---|---|---|
| `workbench_id` | `workbench` plus `title` and `schema_version` | Adapter maps the identity fields; candidate remains a design extension. |
| Candidate verb map in `entry_points` | House `entry_points` contains `cli` and `tests`; command records live under `verbs` | University Press verbs are kept under a named `extensions.university_press` block. They do not overwrite house v1 fields. |
| Candidate `stdout` | House `output` | Adapter maps the one-JSON-document rule and checks UTF-8/canonical output. |
| Candidate `ledgers` | House `ledger_format` and `state_layout` | Candidate append-only state rules are retained as an extension and checked separately. |
| Candidate placeholder humans | House `humans: ["eric", "sheryl"]` | No identity equivalence is inferred. The synthetic implementation never creates a human receipt or dispatches a human node. |
| Candidate `rules` with `UPW-*` IDs | House numbered rules and invariants | `UPW-*` rules are workbench-specific extensions; the house rules remain authoritative. |
| Candidate `schema: navy_yard.workbench_contract.v1` | Same schema identifier | The identifier is necessary but not sufficient. The exact house object is validated before the extension is admitted. |

## Required amendments before a full v1 claim

1. Keep the exact house contract as the dependency and validate its required
   fields, rather than treating the commission-derived candidate shape as the
   house schema.
2. Place University Press verbs, schemas, capability map, stage profiles and
   release semantics in a named extension namespace; do not replace the
   screener's verbs or `entry_points`.
3. Bind the legacy Codex profile to its existing commit/tree-hash skill locks,
   source gates, limits and human-acceptance boundary.
4. Obtain an owner decision on the University Press extension and the intended
   principal before any activation, package promotion, new execution pin or
   real-manuscript run.

## Preserved behavior and unresolved source reconciliation

The implementation preserves the existing Codex edition's RCI-before-SEI
sequence, source-fixity checks, account approval boundary, author-packet
discipline, batch limits, no-publication boundary and vendored package files.
The Lunaroute checkout remains a separate legacy edition; identical lock text
does not establish parity of account, route, payload or receipt behavior.

The handoff's nine-local-tree/remote reconciliation and collaborator-access
verification are not settled by this local capture. The house contract source
checkout is not a Git checkout, so a remote revision could not be independently
attached to the captured contract. The source repository's baseline test run
also reported one pre-existing failure in
`tests/test_evidence.py::BriefTests::test_stored_brief_reemitted_when_rendering_differs`
(`briefs.jsonl line 1: line is not in canonical form`); this is recorded as an
upstream implementation defect, not treated as contract evidence or silently
changed here.
