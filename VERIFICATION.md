# University Press Workbench verification record

Verification date: September 11, 2026

Release candidate: `v0.1.0`

Status: **Ready with conditions for supervised local production use.** The application, both pinned skill packages, the local Codex route, and a generated Word packet were exercised. This record reports the checks performed; it is not a claim that the application is secure or that model findings are correct.

## Release gate

The complete local release gate passed on Windows with Python 3.12.14, Node.js, and Codex CLI 0.153.4:

- 13 application tests passed.
- Python compilation and JavaScript parsing passed.
- Reference and Citation Integrity validation passed: 23 rules and 51 fixtures.
- Scholarly and Editorial Integrity validation passed: 30 rules and 42 fixtures; the supplied self-test scored 42 of 42, including 20 of 20 zero-tolerance checks.
- The repository secret-pattern scan found no candidate OpenAI, GitHub, Google, or private-key values.
- Ruff reported no findings.
- Bandit reported no unsuppressed findings. Its four local-Codex subprocess warnings are reviewed suppressions at fixed, `shell=False` argument-array call sites; `SECURITY.md` records the rationale.
- `pip-audit` found no known vulnerabilities in the pinned runtime dependency set.
- Git whitespace checks passed.
- The security-standards candidate scanner found no patterns in the application, release scripts, or tests. A broad scan initially reported only third-party QA-environment files; that ignored environment is not part of the distributable tree.

Run the same gate with:

```powershell
./scripts/Run-ReleaseGate.ps1
```

## Live end-to-end evidence

A real Codex run completed on one synthetic DOCX chapter under run ID `UPW-20260911T130139Z-d5d4f5f6`:

- The workbench used provider `Codex CLI`, requested model `default`, concurrency 1, Crossref off, and exactly two model calls.
- The synthetic chapter contained a citation-year mismatch and an embedded sentence telling the reviewer to ignore its instructions. The sentence remained manuscript data and was not obeyed.
- RCI returned four findings and SEI returned three findings. Both raw model responses passed the workbench's strict schemas, and both formal run records passed the pinned package schemas.
- The source SHA-256 remained `005a2312faa20ad4556018d55dd068125026d47370b8a459a3eca1a506e1d4bc`; the run receipt records `source_overwritten: false`.
- The author copy contained five native Word comments, a visible review appendix, no accepted edits, and no external DOCX relationships.
- The two-page author copy was rendered with Microsoft Word and Poppler and inspected page by page. No clipping, overlap, or broken table rows were observed. The bundled LibreOffice renderer could not be used because LibreOffice was absent on the review host; this affects the QA method, not normal workbench operation.
- Browser smoke checks returned HTTP 200 for the application and health endpoint, reported both pinned skills and the signed-in Codex route ready, served a restrictive content-security policy with `no-store`, and rejected a forged cross-origin mutation with HTTP 403.

The live test also exposed two Windows path-length defects before release. The workbench now uses short staging and atomic-write names and rejects an output parent that would exceed the conservative Word/Explorer path budget before any model call.

## Conditions and boundaries

1. A University Press steward must approve the local editorial profiles and unresolved decision hooks before treating them as press policy.
2. The editor must confirm that the signed-in Codex account is approved for the exact manuscript manifest. Restricted manuscripts remain blocked in this release.
3. Run the first real volume as a supervised pilot and review false positives, missed citations, comments, and author-facing tone.
4. Keep human acceptance, misconduct adjudication, and publication outside this application.
5. Review licensing before granting rights beyond the owner and invited collaborators; neither vendored upstream repository contains a public license file.

The current limits are deliberate: DOCX, Markdown, and UTF-8 text only; no PDF or OCR; no arbitrary URL fetches; no full-text source verification unless evidence is supplied; no automatic acceptance; and no publication action.

## ERI-38 revision 2 incremental verification — September 18, 2026

This section records the implementation work on branch
`eri-38-revision-2-build`, based on the plain
`university-press-citation-review-workbench` `main` commit
`86ca82c2ff02f8bb4af1de73813cacf2783b1863`. The separate Lunaroute edition
was inspected and left unchanged. The imported candidate archive SHA-256 is
`053EDD5753A6FAA766A090B8BF772A4EB9FD8EDF37B3880C57EDD36B650B4A28`;
`design/eri-38/VERIFICATION.json` was intentionally withheld from the
repository and the generated run evidence remains in private evidence
storage.

The exact captured house contract is
`design/eri-38/upstream/navy_yard.workbench_contract.v1.json`, SHA-256
`9517D8CFEE285694AC50AA5053A34D60714598EBA4A0018387A64154077EAB73`.
The candidate-to-house reconciliation remains `partial`; this is not a v1
conformance claim. The upstream screen-measurement repository baseline ran
115 tests with one pre-existing failure in its stored evidence brief
canonicalization (`test_stored_brief_reemitted_when_rendering_differs`). That
failure is recorded as an upstream baseline issue, not a University Press
regression, and the upstream source was not modified.

The new synthetic slice has been exercised with the following actual results:

- 45 repository tests passed in the fresh full suite, including the legacy
  13-test suite and ERI-38 contract, planning, capacity, adapter, and CLI
  tests.
- The candidate design validator passed all 48 checks; its production-ready
  result remains false because runtime, family, house-conformance, live-parity,
  and editorial-efficacy gates are not run.
- The ten-piece stages-1/5/6 demonstration produced 10 RCI, 10 SEI, 10 CPR,
  and 10 CE-gap nodes; two tasks were admitted with two available slots and
  38 waited.
- The one-piece style demonstration produced one RCI prerequisite and one SGI
  target; both were admitted with three available slots.
- Both demonstrations retained `execution_authorized: false`, made zero
  model calls and zero network calls, and had no external effects.
- Both generated stage plans and both review receipts passed validation
  against the candidate JSON Schemas.

The broader `scripts/Run-ReleaseGate.ps1` reached and passed application
tests, compilation, JavaScript parsing, both vendored package validators and
evaluation suites, and the secret scan, then stopped because `python -m ruff`
was unavailable. Direct `ruff`, `bandit`, and `pip-audit` invocations were
also unavailable in this environment, so the broader release gate is
incomplete rather than claimed as passed.

The implemented synthetic verbs are `declare`, `plan`, `review`, and
`conform`. `seal`, `reconcile`, `record-decision`, and `inspect` are not live
in this slice; the human-authority boundary is refused rather than simulated.
The unresolved gates are owner adoption of the extension, authenticated
route/Loading Bay integration, nine-local-tree/remote parity and collaborator
access reconciliation, native adapter schemas and family efficacy fixtures,
surface parity, and any real-manuscript authorization.
