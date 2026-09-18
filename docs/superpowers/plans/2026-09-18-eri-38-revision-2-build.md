# ERI-38 Revision 2 Build Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Load the ERI-38 design candidate into the University Press repository, reconcile it against the actual house contract and the two existing University Press editions, and implement a deterministic selective-review planning/admission slice with a ten-piece stages-1/5/6 demonstration and a one-piece style-review demonstration.

**Architecture:** The imported candidate remains a design/reference package under `design/eri-38/`; generated verification and run evidence stay outside the repository. A small `upress_workbench.eri38` package will load the exact house contract, bind the existing Codex workbench as a legacy profile, plan capability-driven selective stages without caller family selectors, and expose a synthetic-only capacity admission seam. The first implementation slice will not modify the browser runner, vendored family packages, runtime state, or human-authority boundary.

**Tech Stack:** Python 3.11+, standard-library JSON/hash/CLI code, the repository's existing `unittest` suite, JSON Schema files from the candidate package for reference, and PowerShell-compatible entry scripts.

**Spec:** `design/eri-38/GITHUB_HANDOFF.md`, `design/eri-38/UNIVERSITY_PRESS_DESIGN.md`, `design/eri-38/PROTOCOL.md`, `design/eri-38/ACCEPTANCE.md`, and the locally captured house contract at `design/eri-38/upstream/navy_yard.workbench_contract.v1.json`.

## Global Constraints

- Treat the candidate as design-only until a separately authorized acceptance; no protected-branch write, merge, promotion, publication, or real-manuscript execution.
- Use the actual `navy_yard.workbench_contract.v1` field names and semantics; record candidate-to-house amendments and keep the candidate extension explicitly partial where v1 adoption is not established.
- Preserve the existing RCI-before-SEI order, commit/tree-hash skill locks, source-fixity gates, `.docx`/`.md`/UTF-8 `.txt` inputs, 20 MiB per-piece limit, 250-piece limit, 500 MiB batch limit, concurrency 1–3, 600-call ceiling, and 240-character Windows output-path check.
- Preserve selective review: callers request a stage profile/capabilities, never a family; omitted stages are not planned or dispatched; dependency prerequisites and explicit absent-capability gaps remain visible.
- Preserve adaptive capacity: capability planning and capacity admission are separate; capacity may reduce concurrency or leave tasks waiting, but it may not broaden scope, exceed the 1–3 concurrency range, spend more than twelve human review items per day, or dispatch human nodes.
- Synthetic demonstrations contain opaque IDs and fixed digests only; no manuscript, author, credential, or runtime-output tree enters the repository.
- Every production behavior is introduced by a failing test observed before implementation; documentation/import-only changes are exempt from the code TDD cycle.

---

### Task 1: Import the candidate and reconcile repository/contract provenance

**Files:**
- Create: `design/eri-38/**` from the supplied candidate archive, excluding `VERIFICATION.json`.
- Create: `design/eri-38/upstream/navy_yard.workbench_contract.v1.json` from the local screener contract.
- Create: `design/eri-38/IMPORT_NOTES.md`.
- Create: `design/eri-38/CONTRACT_RECONCILIATION.md`.
- Create: `docs/superpowers/plans/2026-09-18-eri-38-revision-2-build.md`.

**Interfaces:** The design files are inputs to every later task. `CONTRACT_RECONCILIATION.md` records the plain repository at commit `86ca82c2ff02f8bb4af1de73813cacf2783b1863`, the separate Lunaroute repository at commit `822cb00`, the exact local house-contract source, field-level differences, preserved behavior, and unresolved remote/tree-parity limits.

- [ ] **Step 1: Import and inspect the design package**

Confirm that `design/eri-38/contract.json`, `capability-map.json`, `stage-profiles.json`, `schemas/`, `examples/`, `conformance/cases.json`, and `tools/validate_design.py` exist, and that `VERIFICATION.json` is absent from the repository copy.

- [ ] **Step 2: Write the reconciliation record**

Document the mapping from the candidate's `workbench_id`, custom verb entry points, placeholder humans, and `ledgers` block to the house contract's `workbench`, `verbs`, `humans`, `state_layout`, `ledger_format`, and named `extensions`. State that exact house-schema compatibility is validated by the new adapter, while owner adoption of the University Press extension remains open.

- [ ] **Step 3: Run the design validator and record its private evidence**

Run:

```powershell
python design/eri-38/tools/validate_design.py
```

Store the complete validator output outside the repository and preserve its distinction between 48 design checks and unrun runtime/editorial gates.

- [ ] **Step 4: Commit the design upload**

```powershell
git add design/eri-38 docs/superpowers/plans/2026-09-18-eri-38-revision-2-build.md
git commit -m "docs: load ERI-38 revision 2 design candidate"
```

### Task 2: Add the upstream contract and legacy-profile adapter

**Files:**
- Create: `upress_workbench/eri38/__init__.py`.
- Create: `upress_workbench/eri38/canonical.py`.
- Create: `upress_workbench/eri38/contracts.py`.
- Create: `upress_workbench/eri38/legacy.py`.
- Test: `tests/test_eri38_contracts.py`.
- Create: `scripts/validate_eri38_contract.py`.

**Interfaces:** `load_house_contract(path: Path) -> dict`; `load_candidate_contract(path: Path) -> dict`; `reconcile_contracts(house: dict, candidate: dict) -> dict`; `load_legacy_profile(repo_root: Path) -> dict`; `canonical_sha256(value: object) -> str`.

- [ ] **Step 1: Write failing contract and legacy tests**

Cover exact upstream schema/version/required fields, candidate-to-house mapping status, stable digests, RCI-before-SEI ordering, inherited skill pins, and the preserved limits. Assert that the candidate is not reported as fully house-conformant merely because its commission-derived shape is valid.

- [ ] **Step 2: Run the focused tests and observe the missing-module failure**

```powershell
python -m unittest tests.test_eri38_contracts -v
```

The expected red result is an import failure for the not-yet-created `upress_workbench.eri38` package.

- [ ] **Step 3: Implement canonical JSON and contract reconciliation**

Use sorted keys, compact separators, UTF-8, and `allow_nan=False`. Validate the house contract's `navy_yard.workbench_contract.v1` identity, `0.1.0` version, exit codes `0/1/2`, four lane classes, listed humans, and `verbs`/`state_layout` fields. Return a report with `status: partial`, exact file digests, field mappings, and named amendments rather than mutating the candidate contract.

- [ ] **Step 4: Implement legacy-profile loading**

Read the existing `config.py`, `skills.lock.json`, `DESIGN.md`, and `config/workbench-configuration.json`. Return a content-hash binding that preserves the Codex route, RCI-before-SEI order, skill pins, limits, no-publication boundary, and source formats. Do not write to `data/` or vendor directories.

- [ ] **Step 5: Run focused tests, the adapter validator, and commit**

```powershell
python -m unittest tests.test_eri38_contracts -v
python scripts/validate_eri38_contract.py
git add upress_workbench/eri38 tests/test_eri38_contracts.py scripts/validate_eri38_contract.py
git commit -m "feat: reconcile ERI-38 with house contract"
```

### Task 3: Implement capability-driven selective planning

**Files:**
- Create: `design/eri-38/runtime-selective-profiles.json`.
- Create: `upress_workbench/eri38/planning.py`.
- Test: `tests/test_eri38_planning.py`.

**Interfaces:** `plan_request(request: dict, design_root: Path, repo_root: Path) -> dict`; `validate_batch_request(request: dict) -> None`; `stage_catalog() -> dict`.

- [ ] **Step 1: Write failing planning tests**

Test a ten-piece synthetic request for profile `selective_stages_1_5_6`, asserting ten stable piece-scoped requests for the selected capabilities, no SGI/TE/PPR nodes, explicit CE absence where CPR requires it, and a deterministic topological order. Test a one-piece `single_piece_style_review` request, asserting the style target plus only its declared RCI prerequisite. Test rejection of a caller-supplied `family_id` and rejection of non-synthetic content in the demonstration mode.

- [ ] **Step 2: Run the planning tests red**

```powershell
python -m unittest tests.test_eri38_planning -v
```

- [ ] **Step 3: Define the selective profiles and stage catalog**

Use numeric stage IDs as a profile-level vocabulary: `1=RCI/citation_identity`, `2=SGI/adopted_style`, `3=TE/technical_objects`, `4=CE/copyediting gap`, `5=SEI/scholarly_integrity`, `6=CPR/component_readiness`, `7=PPR/proof_survival`. Keep the mapping in data, not in the caller request. The two requested profiles are `selective_stages_1_5_6` and `single_piece_style_review`.

- [ ] **Step 4: Implement deterministic planning**

Validate the closed request shape, resolve selected capabilities through the imported map, add only transitive dependencies and explicit absent-capability nodes, expand chapter-scoped nodes across the supplied pieces, retain all requested stage IDs, and compute a plan digest over the canonical plan without an approval field that could authorize itself.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest tests.test_eri38_planning -v
git add design/eri-38/runtime-selective-profiles.json upress_workbench/eri38/planning.py tests/test_eri38_planning.py
git commit -m "feat: add selective ERI-38 stage planning"
```

### Task 4: Add adaptive capacity admission without a dispatcher

**Files:**
- Create: `upress_workbench/eri38/capacity.py`.
- Create: `upress_workbench/eri38/review.py`.
- Test: `tests/test_eri38_capacity.py`.

**Interfaces:** `admit_tasks(plan: dict, capacity: dict) -> dict`; `simulate_review(plan: dict, capacity: dict) -> dict`; `default_capacity_policy() -> dict`.

- [ ] **Step 1: Write failing capacity tests**

Cover stable task ordering, available-slot reduction, maximum concurrency of three, daily review-budget preservation at twelve, human-node nondispatch, waiting tasks when capacity is exhausted, and no model/network call count in a synthetic run.

- [ ] **Step 2: Run the capacity tests red**

```powershell
python -m unittest tests.test_eri38_capacity -v
```

- [ ] **Step 3: Implement the bounded adaptive policy**

Admit at most the minimum of requested parallelism, available slots, and the inherited maximum of three. Keep the review budget separate from machine capacity; when it is exhausted, return `awaiting_capacity` or `awaiting_human` without widening scope. Keep human nodes in the returned docket with `dispatchable: false` and never emit a model task for them.

- [ ] **Step 4: Implement synthetic review receipts**

Generate content-free task envelopes and deterministic result receipts containing plan, piece, stage, lane, capacity decision, and no manuscript text. Mark the run as simulation/diagnostic evidence, not accepted editorial output.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest tests.test_eri38_capacity -v
git add upress_workbench/eri38/capacity.py upress_workbench/eri38/review.py tests/test_eri38_capacity.py
git commit -m "feat: preserve adaptive capacity seam"
```

### Task 5: Resolve CPR/PPR upstream dependency behavior

**Files:**
- Create: `upress_workbench/eri38/adapters.py`.
- Test: `tests/test_eri38_adapters.py`.
- Modify: `design/eri-38/CONTRACT_RECONCILIATION.md` if test evidence adds a required amendment.

**Interfaces:** `evaluate_cpr(upstream_results: list[dict], profile: dict) -> dict`; `evaluate_ppr(inputs: dict) -> dict`; `invalidate_for_reproof(result: dict, changed_binding: str) -> dict`.

- [ ] **Step 1: Write failing adapter tests**

Assert that CPR records absent CE without substituting SGI or TE, reports missing upstream results explicitly, and preserves unknown coverage. Assert that PPR returns `blocked_input` when the accepted copyedited baseline or proof fixity is absent, and that a changed correction/proof binding invalidates the dependent result rather than editing its plan ID.

- [ ] **Step 2: Run the adapter tests red**

```powershell
python -m unittest tests.test_eri38_adapters -v
```

- [ ] **Step 3: Implement deterministic CPR/PPR adapters**

Use field-by-field native-to-common mappings, preserve absent/unknown/not-applicable states, and return claim-scoped blockers. Do not call a model, mutate a source, or manufacture a human receipt.

- [ ] **Step 4: Run tests and commit**

```powershell
python -m unittest tests.test_eri38_adapters -v
git add upress_workbench/eri38/adapters.py tests/test_eri38_adapters.py design/eri-38/CONTRACT_RECONCILIATION.md
git commit -m "feat: add CPR and PPR dependency adapters"
```

### Task 6: Expose the house-compatible synthetic CLI and demo

**Files:**
- Create: `upw.py`.
- Create: `upress_workbench/eri38/cli.py`.
- Create: `scripts/run_eri38_demo.py`.
- Test: `tests/test_eri38_cli.py`.
- Create: `design/eri-38/DEMO.md`.

**Interfaces:** `python upw.py declare --request <path>`; `python upw.py plan --request <path>`; `python upw.py review --request <path>`; `python upw.py conform --request <path>`.

- [ ] **Step 1: Write failing CLI/demo tests**

Assert one canonical JSON object plus newline on stdout, exit `0` for the synthetic plan/review, exit `2` for a caller family selector or human dispatch attempt, and demo result counts of ten pieces × requested stages 1/5/6 plus one style piece.

- [ ] **Step 2: Run the CLI tests red**

```powershell
python -m unittest tests.test_eri38_cli -v
```

- [ ] **Step 3: Implement the CLI envelope**

Implement `declare`, `plan`, `review`, and `conform` as deterministic, synthetic-capable verbs. Use the house exit meanings and reply envelope; route diagnostics to stderr; leave `seal`, `reconcile`, `record-decision`, and `inspect` outside this first executable slice rather than faking human authority.

- [ ] **Step 4: Implement and run the demonstration**

Generate ten opaque synthetic pieces requesting stages 1, 5, and 6, and one opaque piece requesting the style profile. Run with a bounded capacity fixture that exposes adaptive admission and waiting. Write the run evidence outside the repository and a redacted summary under `design/eri-38/DEMO.md`.

- [ ] **Step 5: Run tests and commit**

```powershell
python -m unittest tests.test_eri38_cli -v
python scripts/run_eri38_demo.py --output C:\Users\tucke\Documents\Codex\2026-09-18\files-mentioned-by-the-user-eri39\work\eri38-evidence
git add upw.py upress_workbench/eri38/cli.py scripts/run_eri38_demo.py tests/test_eri38_cli.py design/eri-38/DEMO.md
git commit -m "feat: expose ERI-38 synthetic selective-review demo"
```

### Task 7: Reconcile documentation and run the full verification gate

**Files:**
- Modify: `README.md`.
- Modify: `DESIGN.md`.
- Modify: `VERIFICATION.md`.
- Create: `design/eri-38/IMPLEMENTATION_STATUS.md`.
- Create: private BSE outcome record outside the repository.

**Interfaces:** The documentation must distinguish the shipped legacy browser workflow from the new synthetic `upw` slice, state the exact unimplemented human verbs, and name the upstream screen-repo test failure without treating it as a University Press regression.

- [ ] **Step 1: Write documentation regression assertions**

Add tests to `tests/test_eri38_cli.py` for the README/implementation status claims that are machine-checkable: demo command present, `VERIFICATION.json` absent from design import, and no publication verb in the executable CLI.

- [ ] **Step 2: Update documentation and status**

Record target branch/commit ancestry, imported package digest, upstream contract digest, demo evidence references, test counts, and the unresolved nine-local-tree/remote parity and owner-acceptance gates. Do not claim full house conformance, editorial efficacy, live capacity integration, or surface parity.

- [ ] **Step 3: Run fresh verification**

```powershell
python -m unittest discover -s tests
python design/eri-38/tools/validate_design.py
python scripts/validate_eri38_contract.py
python scripts/check_no_secrets.py
git diff --check
git status --short --branch
```

- [ ] **Step 4: Record BSE outcome and commit final changes**

Record source/requirement fidelity, completeness, cross-batch coherence, correction effort, and measured time/token overhead (unavailable where not instrumented) in the shared BSE outcomes directory. Then commit the documentation and verification evidence. Push the working branch only after the complete fresh verification gate passes and the remote target remains the private University Press repository.
