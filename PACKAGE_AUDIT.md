# Integrity package audit

Audit date: September 11, 2026

Release decision: **Ready with conditions for supervised University Press use.** Both packages are pinned, structurally valid, and pass their supplied evaluation suites. Neither package is a finished press policy: each identifies itself as specification version `0.1.0-draft`, and local decision hooks still require a University Press steward.

## Package inventory

| Package | Pinned commit | Version | Rules | Fixtures | Result |
|---|---|---:|---:|---:|---|
| Reference and Citation Integrity | `a49e9f686898030684134ba7a7f84ac8b68fc4dc` | 0.1.0 | 23 | 51 | Native validator and suite validator pass |
| Scholarly and Editorial Integrity | `098080247ab21173bbbe3da3ab90aa3cf860e38c` | 0.1.0 | 30 | 42 | Native validator, suite validator, and 42-fixture self-test pass |

Both packages contain `SKILL.md`, `agents/openai.yaml`, a governing specification, machine-readable rules, schemas, examples, evaluation fixtures, scoring code, and change or regression records. Neither upstream repository contains a public license file. Public visibility of this workbench therefore does not itself grant general reuse rights.

## Scorecard

| Dimension | RCI | SEI | Evidence |
|---|---|---|---|
| Triggering and identity | Pass | Pass | Valid frontmatter and agent metadata; explicit invocation routes |
| Workflow and handoffs | Pass | Pass | RCI stages 01 through 07 precede SEI; cross-family contracts are present |
| Scope boundaries | Pass | Pass | Citation identity and rendering are separated from claim, authorship, intent, and formal-adjudication questions |
| Evidence integrity | Pass | Pass | Missing sources stay visible; candidate provider metadata cannot become a verdict |
| Safety | Pass | Pass | No invented evidence, publication authority, or automatic formal allegation |
| Outputs and schemas | Pass | Pass | Native validators accept all examples and fixtures |
| Progressive disclosure | Pass | Pass | Short `SKILL.md` entrypoints route into specifications, rules, and schemas |
| Maintainability | Pass | Pass | Versioned rules, fixture crosswalks, decision hooks, and regression intake records |
| Local policy completeness | Needs work | Needs work | Draft profiles and University Press decision hooks need steward approval |
| General redistribution rights | Needs decision | Needs decision | No public license file was found in either upstream repository |

## Findings and disposition

- **P1 resolved — Windows governing-spec hash.** The SEI native validator initially failed on a normal Windows checkout because it hashed CRLF bytes against the upstream LF hash. The vendored validator now canonicalizes CRLF to LF for that comparison. The change is recorded in `VENDOR_PATCHES.md`; no policy content changed.
- **P1 resolved — source drift at packet time.** The workbench reads the exact approved byte snapshot, rechecks the source before both model stages, and publishes a chapter directory only after all packet files and its receipt are complete.
- **P1 resolved — Windows output-path failure.** Generated names are bounded, staging and atomic-write leaves are short, and the maximum packet path is checked before model work.
- **P1 resolved — model-record schema drift.** Workbench-only finding identifiers no longer enter the raw model result. Both persisted model responses and both formal skill records were schema-validated in the live end-to-end run.
- **P2 open — press policy hooks.** APA profile details, disclosure matrices, source-access expectations, and exception ownership still need named University Press decisions.
- **P2 open — public licensing.** The repository owner should choose explicit licenses before granting broad reuse or derivative-work rights.

The package audit does not prove model findings correct. A press editor must review every proposed change and query.
