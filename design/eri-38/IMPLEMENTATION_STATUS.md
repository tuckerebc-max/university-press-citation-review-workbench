# ERI-38 revision 2 implementation status

Status: **synthetic selective-review slice implemented; candidate remains partial and not production-ready.**

## Repository and provenance

- Target repository: `university-press-citation-review-workbench`.
- Working branch: `eri-38-revision-2-build`.
- Base: `main` at `86ca82c2ff02f8bb4af1de73813cacf2783b1863`.
- Separate `university-press-citation-review-workbench-Lunaroute` edition was inspected and preserved unchanged.
- Candidate archive SHA-256: `053EDD5753A6FAA766A090B8BF772A4EB9FD8EDF37B3880C57EDD36B650B4A28`.
- Captured house contract SHA-256: `9517D8CFEE285694AC50AA5053A34D60714598EBA4A0018387A64154077EAB73`.
- The private candidate `VERIFICATION.json` is not imported; no manuscript, author, credential, or runtime-output tree is stored here.

## Implemented behavior

- Exact house-contract loading and explicit candidate-to-house reconciliation with `status: partial`.
- Legacy profile binding that preserves RCI-before-SEI, skill commit/tree locks, source formats, file/batch/path limits, no-publication authority, and adaptive concurrency 1–3.
- Data-driven selective profiles: stages 1/5/6 and single-piece style review. Family selectors are rejected; transitive prerequisites and the CE absence remain visible.
- Synthetic capacity admission that reduces to available slots, queues saturated work, preserves the twelve-item human budget, and never dispatches human nodes.
- CPR/PPR dependency adapters that preserve missing/not-run/absent states, block PPR without accepted copyedited baseline and proof fixity, and invalidate descendants for reproof without editing the old plan ID.
- House reply envelope for `declare`, `plan`, synthetic `review`, and `conform`; human/release verbs are refused or unimplemented.

## Actual demonstration result

The private run evidence is under the projectless work area at
`work/eri38-evidence/` (not in the repository). The ten-piece request for
stages 1, 5, and 6 produced 10 RCI, 10 SEI, 10 CPR, and 10 explicit CE-gap
nodes. With requested parallelism 3 and two available slots, 2 synthetic
machine task references were admitted and 38 waited; the receipt outcome was
`partial`. The one-piece style request produced one RCI and one SGI task, both
admitted with three available slots; its receipt outcome was `submitted`.
Both candidate plans retained `execution_authorized: false`. Aggregate model
calls and network calls were 0, and external effects were false.

## Verification and remaining gates

The fresh full suite passed 45 tests; the candidate validator passed 48/48;
the standalone house/legacy validator passed; and the private synthetic demo
completed. The upstream screen-measurement source baseline remains 115 tests
with one pre-existing stored-brief canonicalization failure. That source was
not changed.

Both generated stage plans and both generated review receipts validated
against their candidate JSON Schemas. The repository release-gate script
passed application tests, compilation, JavaScript parsing, both vendored
package validators/evaluation suites, and the secret scan before stopping at
the unavailable `ruff` module. Direct `ruff`, `bandit`, and `pip-audit`
invocations were also unavailable in the current Python environment; this is
reported as an incomplete tooling gate, not as a pass.

This status does not claim exact house conformance, owner acceptance, live
Loading Bay or surface parity, native family adapter conformance, editorial
efficacy, authenticated human verification, real-manuscript authorization,
publication, or protected-branch integration. The handoff's nine-local-tree
remote parity and collaborator-access question remains open for the authorized
operator.
