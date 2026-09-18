# University Press Workbench Design

## Purpose

This repository is the shareable Codex edition of the University Press Citation Review Workbench. University Press owns the professional rules and the decision to accept, reject, or publish. The application turns those rules into a repeatable batch plan and preserves the evidence needed for human review.

Each run carries four records:

1. A source manifest with stable chapter IDs, relative paths, byte counts, and SHA-256 hashes.
2. An immutable plan with the data-route approval, classification, stage order, skill commits, requested Codex model, concurrency, and prohibited effects.
3. Per-chapter evidence and author packets that separate observed text, candidate metadata, model proposals, and human decisions.
4. A run receipt and append-only observation stream that reconcile each packet to the approved source manifest.

## Execution sequence

```text
folder scan
  -> source hashes and Codex-account approval
  -> immutable plan
  -> deterministic DOCX or text extraction
  -> citation and reference inventory
  -> optional fixed-host Crossref candidates
  -> reference-citation-integrity review through codex exec
  -> scholarly-editorial-integrity review through codex exec
  -> neutral author comments and queries
  -> chapter receipt
  -> run reconciliation and human acceptance queue
```

Reference and Citation Integrity always runs first. Scholarly and Editorial Integrity receives the RCI result and citation-graph status. The workbench checks the source hash before extraction, before each model stage, and before packet assembly. A mismatch blocks the chapter.

## Codex execution contract

The workbench resolves the installed `codex` executable and uses the editor's existing Codex authentication. Each call runs in a new temporary directory with an ephemeral session, a read-only sandbox, ignored user configuration and project rules, disabled shell and web-search tools, a fixed output schema, and no shell command composition. Manuscript content enters through standard input.

The default model setting delegates model choice to the Codex product. An editor may enter a model identifier supported by their account. The identifier is syntax-checked and passed as one subprocess argument, so it cannot add command flags. The workbench records the requested value in its plan and receipts.

The workbench never reads Codex credential files. It checks only whether `codex login status` succeeds.

## Fixed and adjustable decisions

The fixed rules are source preservation, RCI-before-SEI ordering, version-pinned skill packages, approval for the signed-in Codex route, strict model-output schemas, neutral integrity language, visible exceptions, human acceptance, and no publication action.

Editors may choose the input folder, output parent folder, requested Codex model, review mode, bounded concurrency, chapter ordering, and optional Crossref candidate lookup. Restricted material remains blocked in this release.

On Windows, the workbench calculates the longest generated packet path before any model call. If the chosen output parent would produce a path longer than the conservative Word/Explorer budget, the run stops and asks the editor to choose a shorter location.

## Author packet design

The workbench does not silently accept edits. When a finding has a safe paragraph anchor, the reviewed Word copy carries a comment. A final review appendix lists every proposed change and query, including items that could not be anchored. A Markdown query sheet and script-free HTML review provide simpler author-facing formats.

## Current boundary

This release processes local DOCX, Markdown, and UTF-8 text files. It does not ingest PDFs, download manuscript-supplied URLs, inspect full cited articles, modify live editorial systems, accept edits, or publish. Model inference runs through the signed-in Codex service and is not offline. Those limits are part of the release contract, not unfinished background features.

## ERI-38 revision 2 build boundary

The ERI-38 candidate under `design/eri-38/` adds a separate implementation
seam; it does not replace or modify the browser runner, vendored RCI/SEI
packages, or `skills.lock.json`. The candidate is reconciled against the
captured house contract in `design/eri-38/upstream/` and remains `partial`
until the University Press extension is owner-adopted.

The first executable slice is synthetic-only. A caller selects a named stage
profile rather than a family, the planner adds only transitive prerequisites
and explicit absent-capability gaps, and capacity admission can reduce
parallelism or leave work waiting. The ten-piece stages-1/5/6 demonstration
therefore shows RCI, SEI, CPR, and a visible CE gap; the one-piece style
demonstration shows RCI followed by SGI. Candidate plans always retain
`execution_authorized: false`.

CPR and PPR adapters preserve upstream unknown, absent, and blocked states.
PPR requires an accepted copyedited baseline and proof fixity before any
substantive comparison; changed bindings require reproof and a successor plan.
The `upw.py` wrapper emits the house reply envelope for `declare`, `plan`,
synthetic `review`, and `conform`. Human-authority and release verbs are not
fabricated by this slice.
