# Proof & Post-Typesetting Review Specification

**Specification ID:** `MWM-PPR-SPEC`  
**Version:** `0.1.0-draft`  
**Status:** Draft for editorial-owner review  
**Skill family:** Proof & Post-Typesetting Review  
**Research corpus:** `MWM-PPR-2026-08`  
**Scope:** Typeset proofs, corrected proofs, final digital/print outputs, and authorized post-publication updates  
**Out of scope:** Developmental editing, substantive rewriting, routine copyediting, and unapproved changes to the version of record  
**Last revised:** August 13, 2026

## 1. Purpose

This family compares the approved manuscript and production package with the typeset proof and final output. It identifies production-introduced errors, unresolved production queries, visible fact/meaning errors, broken component relationships, output/accessibility defects, and unincorporated corrections. It produces explicit correction records, reproof requirements, version/fixity evidence, and a human-owned release decision.

Proof review is a late-stage control. Its governing question is:

> Did the approved content, metadata, objects, and decisions survive composition and final-output conversion, and can every accepted correction be shown to have been incorporated?

## 2. Non-negotiable boundary

The Skill may:

- compare an approved baseline with a proof or final output;
- identify an observable difference or defect;
- classify the difference as approved variation, production error, factual/meaning error, open query, asset issue, accessibility signal, or unresolved status;
- propose an exact minimal correction;
- record accept/reject decisions and reproof requirements;
- preserve version, fixity, provenance, and release evidence;
- route substantial changes, privacy/rights issues, and post-publication status matters.

The Skill may not:

- rewrite a chapter, section, paragraph, or argument for style or development;
- treat every difference from the manuscript as an error;
- accept a substantial author alteration without authorization;
- infer the intended correction from vague comments;
- certify legal permissions, accessibility conformance, source validity, or scholarly integrity from a visual check alone;
- silently change the version of record;
- close a correction without evidence that it was incorporated and rechecked;
- use a filename or timestamp as the only proof of file identity.

## 3. Triggers

| Trigger | Required action | Default mode |
|---|---|---|
| Typeset proof received | Capture baseline, proof identity, queries, and proofing scope. | Baseline |
| Corrected proof returned | Compare correction log with proof and recheck changes. | Reproof |
| Final PDF/e-book/HTML produced | Run format-specific output and release checks. | Final validation |
| Author/production query raised | Record exact question, response, owner, and status. | Query review |
| Asset replacement supplied | Verify object identity, crop/content, permissions, and incorporation. | Asset review |
| Post-publication error reported | Create correction case with evidence and impact. | Record review |
| Correction/retraction/removal approved | Update linked version/status records and reader communication. | Status review |
| Output or proof corrupted | Pause review and notify production before continuing. | Incident gate |

## 4. Inputs

### 4.1 Required inputs

- approved manuscript and last accepted copyedited version;
- typeset proof and, if available, source/production proof version;
- final or candidate digital/print outputs within scope;
- production design specification and approved variation log;
- chapter/volume component profile and asset manifest;
- correction grid/query log/previous proof decisions;
- figures, tables, captions, notes, references, cross-reference, and metadata records;
- upstream RCI, Style Guide, Technical Editing, Copyediting, Scholarly/Editorial Integrity, and Completeness statuses;
- file identity/version/fixity records;
- applicable accessibility target and output format requirements.

### 4.2 Optional inputs

- high-resolution source assets;
- redline or tracked-change comparisons;
- page map, index, TOC, and running-head map;
- e-book/HTML/accessible-PDF test output;
- post-publication notice, correction request, author response, or publisher decision;
- prior proof and reproof versions;
- production system edit log.

### 4.3 Protected inputs

Protect unpublished proofs, author correspondence, correction files, sensitive participant information, rights documents, and any output marked for internal review. Use only authorized proofing channels. Treat accidental external sharing as an incident.

## 5. Authority and rule hierarchy

| Tier | Authority | Application |
|---|---|---|
| 1 | MWM approved manuscript, chapter profile, production decisions, and release policy | Defines the proof baseline, approved variations, and correction authority. |
| 2 | Current typesetter instructions, correction grid, query log, asset manifest, and decision log | Defines current production state and accepted changes. |
| 3 | Delegated style, technical, accessibility, rights, integrity, and metadata rules | Controls specialized defect resolution. |
| 4 | Publisher proofing, Crossref/NISO versioning, W3C, and PREMIS exemplars | Supplies process and evidence patterns. |
| 5 | Generic proofreading preference or model inference | Generates a question only; cannot authorize a change. |

When a proof differs from the manuscript, consult the approved variation/change log before classifying it. A difference without an explanation is a signal requiring investigation, not automatically a typesetter error.

## 6. Preconditions

Before substantive proof review, verify:

1. manuscript, proof, and output versions have stable IDs;
2. the approved baseline is identified and accessible;
3. the proofing stage, correction limits, deadline, and owner are recorded;
4. approved design/variation decisions are available;
5. the proof is not corrupted or incomplete;
6. relevant upstream findings and accepted changes are imported;
7. the correction channel and annotation conventions are authorized;
8. the output formats and accessibility targets are known;
9. the release signatory and escalation path are named.

If a precondition fails, return `blocked` with the exact missing evidence. Do not proceed on the basis of a plausible file or memory.

## 7. Proof records and schemas

### 7.1 Baseline record

```yaml
baseline_id: MWM-PPR-BL-000
chapter_id: MWM-000
volume_id: MWM-VOL-000
approved_version: v0.0
copyedited_version: v0.0
proof_version: v0.0
output_version: v0.0_or_null
file_ids: []
hashes_or_fixity: []
approved_variations: []
stage: proof | reproof | final_output | post_publication
captured_at: ISO-8601
captured_by: role/person/tool
```

### 7.2 Proof finding

```yaml
finding_id: PPR-000
skill_id: PPR-00
baseline_id: MWM-PPR-BL-000
proof_id: file/output identifier
location: page/paragraph/object/coordinate
defect_type: approved_variation | typesetter_error | factual_or_meaning_error | author_alteration | query_open | asset_issue | accessibility_signal | status_issue
severity: low | moderate | high | critical
current_state: exact visible text/object/state
expected_state: baseline/approved target
evidence: comparison records, screenshot, source asset, or query
authority: design/rule/decision ID
correction_instruction: exact replacement or action
owner: author/editor/production/technical/integrity/accessibility/rights
status: open | accepted | rejected | incorporated | reproof_required | resolved | blocked
impact: meaning | credit | navigation | indexing | pagination | accessibility | rights | privacy | cosmetic
confidence: high | medium | low
release_effect: none | track | hold | block
created_at: ISO-8601
updated_at: ISO-8601
```

### 7.3 Correction record

```yaml
correction_id: COR-000
finding_id: PPR-000
location: exact proof locator
current_text_or_object: exact current state
replacement_text_or_object: exact replacement or production instruction
reason: typesetter_error | factual_error | meaning_error | asset_replacement | query_response
submitted_by: role/person
submitted_at: ISO-8601
decision: accept | reject | defer | refer
decision_owner: role/person
incorporated_in: proof/output ID
reproof_scope: page/object/whole_chapter/format
reproof_result: pending | passed | failed | not_applicable_with_reason
```

### 7.4 Release/fixity event

```yaml
event_id: PPR-EVT-000
event_type: baseline_captured | proof_received | correction_submitted | correction_incorporated | reproof_passed | output_released | post_publication_update
object_id: file/output ID
previous_object_id: null_or_ID
hash_or_identifier: value_or_null
agent: person/team/tool
event_time: ISO-8601
evidence_locator: path/record
decision_id: null_or_ID
```

## 8. Defect and status vocabulary

| Status | Meaning | Default treatment |
|---|---|---|
| `approved_variation` | Difference is supported by an approved design/production decision. | Record; no correction. |
| `typesetter_error` | Unapproved production difference from the approved baseline. | Minimal correction and reproof. |
| `factual_or_meaning_error` | Visible output changes a fact, number, symbol, attribution, or meaning. | High-priority correction and human approval. |
| `author_alteration` | Proposed change exceeds approved proof scope or changes accepted content. | Query/hold/senior decision. |
| `query_open` | Required answer or production clarification is missing. | Hold affected gate. |
| `source_unavailable` | Required baseline, asset, or source cannot be inspected. | Do not certify; request evidence. |
| `asset_issue` | Wrong, missing, corrupt, altered, or unlinked visual/code/media asset. | Replace/route/reproof. |
| `accessibility_signal` | Digital output may not meet applicable accessibility expectations. | Specialist review; no conformance claim. |
| `status_issue` | Correction/version/retraction/removal/update state is missing or inconsistent. | Metadata/senior review. |
| `resolved` | Correction or decision is incorporated and independently rechecked. | Close with evidence. |
| `blocked` | Baseline, authority, correction, or required review is absent. | Do not release. |

## 9. Operating principles

### 9.1 Baseline before judgment

No defect classification without an identified comparison target: approved manuscript, copyedited version, approved design, prior proof, or current output. If the baseline is unavailable, return `source_unavailable` or `blocked`.

### 9.2 Difference is not defect

Typesetting necessarily changes line breaks, pagination, styling, and sometimes placement. An approved design variation is not an error. Compare against the applicable design/decision record.

### 9.3 Minimum change

Accept only the smallest correction that restores the approved text, meaning, object, or production requirement. Avoid changes that cause unnecessary reflow, index/page movement, or new defects.

### 9.4 Exact correction language

Every correction must state where it applies, what appears now, what should appear instead, and why. “Make better,” “fix formatting,” or “please check” is not a sufficient correction instruction.

### 9.5 Reproof is part of closure

A correction is not resolved when it is submitted or marked accepted. It is resolved when it is incorporated in the next output and the affected scope is rechecked.

### 9.6 Protect the record

Minor production changes may remain part of the current version. Editorially significant post-publication changes require an approved linked notice/version/status record. Never silently overwrite the original record.

### 9.7 No-change is valid

Harmless line breaks, approved blank pages, low-resolution proof previews with approved final assets, and correctly wrapped URLs can close with no action after evidence review.

## 10. Skill map

| Skill ID | Skill | Core question | Default intervention |
|---|---|---|---|
| `PPR-01` | Proof Baseline and Fixity | Are the manuscript, proof, outputs, assets, and versions identifiable? | Capture or block. |
| `PPR-02` | Difference Review | What changed between approved baseline and proof/output? | Classify difference; no automatic error assumption. |
| `PPR-03` | Text and Symbol Integrity | Did words, names, numbers, symbols, equations, code, or special characters survive? | Exact minimal correction. |
| `PPR-04` | Navigation and Layout | Are headings, TOC, running elements, pagination, breaks, and reading flow correct? | Production correction/review. |
| `PPR-05` | Visual Objects | Do figures/tables/captions/notes/assets remain correct, linked, and placed? | Asset/technical correction. |
| `PPR-06` | References and Cross-References | Do visible citations, references, notes, and targets survive typesetting? | RCI/TE correction and recheck. |
| `PPR-07` | Queries and Correction Log | Are corrections explicit, owned, accepted/rejected, incorporated, and reproofed? | State transition and hold. |
| `PPR-08` | Accessibility and Digital Outputs | Does each in-scope output have evidence for applicable accessibility checks? | Specialist route; no overclaim. |
| `PPR-09` | Post-Publication Record | Is a released error/update represented with the correct version/status path? | Senior/metadata route. |
| `PPR-10` | Proof Release Gate | Is the current output ready for release? | Human-signable release/hold/block. |

## 11. Procedure

### Step 1 — Capture baseline

Create the baseline record, copy file identifiers/fixity, import approved variations, and identify the proof/output format and stage.

### Step 2 — Validate proof integrity

Check that the proof is complete, readable, and not obviously corrupted. If pages, assets, fonts, or sections are missing, notify production before detailed proofing.

### Step 3 — Build comparison objects

Assign stable IDs to chapters, sections, headings, pages, paragraphs, notes, figures, tables, captions, references, cross-references, metadata, and output formats. Map object IDs across baseline and proof where possible.

### Step 4 — Run difference review

Compare content, metadata, object relationships, layout/navigation, and output features. Consult the approved variation log before classifying a difference.

### Step 5 — Classify defects and impact

Use the defect vocabulary and assess impact on meaning, fact, credit, indexing, pagination, navigation, accessibility, rights, privacy, and reader interpretation.

### Step 6 — Create exact corrections or queries

Record current state, expected state, location, replacement/action, reason, owner, and release effect. Ask the responsible person when authorization or substantive judgment is required.

### Step 7 — Process accept/reject/defer

The production/editorial owner accepts, rejects, defers, or refers each correction. A rejected correction remains in the log with rationale; it is not erased.

### Step 8 — Verify incorporation and reproof

Compare the corrected proof/final output with each accepted correction. Recheck affected pages/objects and related TOC, index, cross-reference, page, and format-specific effects.

### Step 9 — Run digital/output checks

For each in-scope PDF/e-book/HTML output, run applicable reading order, bookmarks, headings, tables, links, language, alt-text, page numbering, and asset checks. Route conformance decisions to the designated specialist.

### Step 10 — Run release gate and preserve record

Confirm no unresolved high/critical finding, open query, missing baseline, failed reproof, ambiguous file identity, or unapproved status change remains. Capture release event, final identity/fixity, signatory, and next-stage record.

## 12. PPR-01 — Proof Baseline and Fixity

### Detection logic

- identify approved manuscript/copyedited version;
- identify typeset proof and output version;
- record file IDs, hash/fixity where available, format, page count, and capture time;
- link proof to the production package and approved design;
- record superseded versions and correction cycles;
- detect missing, duplicate, corrupt, or ambiguous files.

### Intervention

Return `blocked` when the current proof or baseline cannot be identified. Do not use timestamps, filenames, or visual similarity alone as proof of identity.

## 13. PPR-02 — Difference Review

### Comparison domains

1. text and punctuation;
2. names, affiliations, dates, numbers, symbols, equations, code, and special characters;
3. headings, hierarchy, TOC, running heads/feet, page numbers, and section breaks;
4. figures, tables, captions, notes, legends, and asset placement;
5. citations, references, footnotes/endnotes, links, and cross-references;
6. metadata, contributor records, declarations, and source/status labels;
7. PDF/e-book/HTML accessibility and navigation features;
8. correction/query incorporation and version status.

Classify each difference as approved variation, defect, unresolved, or no action. Preserve the comparison evidence and authority used.

## 14. PPR-03 — Text and Symbol Integrity

### Detection logic

- compare words and punctuation against the approved baseline/redline;
- protect proper names, diacritics, non-Roman scripts, special characters, and equations;
- compare numbers, signs, decimal points, superscripts/subscripts, units, and statistical notation;
- check code characters, indentation, line breaks, and font transitions;
- check quotation marks, apostrophes, hyphens, en/em dashes, slashes, and unintended substitutions;
- check language-specific glyphs and missing-font placeholders.

### Intervention

An isolated production substitution can receive a minimal correction. A change affecting meaning, data, credit, or source identity is high risk and requires human approval and reproof. Do not normalize whole passages at proof stage.

## 15. PPR-04 — Navigation and Layout

### Checks

- chapter/title/author occurrences;
- TOC entries, order, page numbers, and heading levels;
- running heads/feet and page numbers;
- section starts, display pages, blank pages, and breaks;
- heading orphan/widow conditions under the design profile;
- paragraph/page continuation and unexpected truncation;
- footnote/endnote placement and sequence;
- placeholders, missing text, and unresolved “page 000”/“see above” artifacts;
- index entries and page references after accepted corrections.

### Boundary

Layout differences can be intentional. Consult design decisions and route aesthetic/layout choices to production; proof does not redesign the book.

## 16. PPR-05 — Figures, Tables, Captions, and Notes

### Object checks

- asset identity and current version;
- placement relative to callout and approved design;
- figure/table label and numbering;
- caption text and panel/row/column references;
- notes, keys, legends, and source lines;
- table row/column headings and totals;
- orientation, reversal, crop, scale, and missing content;
- permission/consent status where relevant;
- high-resolution final asset versus low-resolution proof preview;
- format-specific presence in print/PDF/e-book/HTML.

### Intervention

Use exact object/location references. If replacement art is needed, identify the file, crop/version, and instruction. Do not replace or redraw an asset based on a filename or visual preference alone.

## 17. PPR-06 — References and Cross-References

### Detection logic

- compare visible citations, reference entries, notes, DOI/URL displays, and reference order with the accepted version;
- confirm cross-references target fixed objects/sections/figures/tables where the output requires it;
- detect missing, duplicated, orphaned, or placeholder references/notes;
- verify that correction-induced pagination/indexing changes do not break references;
- preserve upstream RCI/TE findings and route substantive source/metadata issues.

### Boundary

This Skill checks proof survival and visible output. RCI owns metadata construction, DOI verification, source status, and citation integrity; Technical Editing owns semantic cross-reference structure.

## 18. PPR-07 — Queries and Correction Log

### Required correction fields

- unique correction ID;
- exact proof location/page/object;
- current visible text/object;
- replacement text/object or production instruction;
- reason and defect class;
- requester, owner, and date;
- accept/reject/defer/refer decision;
- incorporation output/version;
- reproof scope and result;
- release effect and rationale.

### State machine

`open → clarified → accepted/rejected/deferred/referred → incorporated → reproof_required → reproof_passed → resolved`

Any state may become `blocked` if baseline, authorization, asset, or output evidence is missing. A rejected correction remains recorded with its rationale.

## 19. PPR-08 — Accessibility and Digital Outputs

### Evidence prompts

For each in-scope format, check or obtain evidence for:

- document title and language;
- logical reading order;
- headings/bookmarks/navigation;
- alt text or approved decorative treatment;
- table structure and headers;
- meaningful link text and link targets;
- page numbering and navigation;
- text extraction/OCR where relevant;
- contrast/non-text content under the applicable target;
- consistency between visual and assistive-technology order.

### Boundary

W3C techniques are informative. The Skill may report a missing tag, likely reading-order issue, or absent evidence, but a formal accessibility conformance claim requires the designated accessibility review and applicable normative standard.

## 20. PPR-09 — Post-Publication Record

### Trigger conditions

- error affects meaning, fact, contributor credit, source status, reader safety, rights, or interpretation;
- minor correction needs tracking under MWM policy;
- correction, withdrawal, removal, retraction, or expression of concern is authorized;
- a new version replaces or supplements an existing release.

### Required case record

- work title and stable identifier;
- affected chapter/output/version;
- reporter/corresponding author and contact;
- exact error and evidence;
- impact/justification;
- authorized decision and owner;
- correction/notice/version text;
- links between original and update;
- effective date and reader-communication channel;
- retained original/fixity and supersession record.

The Skill communicates an authorized decision; it does not decide whether a work should be retracted or removed.

## 21. PPR-10 — Proof Release Gate

### Release decisions

| Decision | Meaning |
|---|---|
| `ready` | All applicable proof/output gates pass and no material unresolved issue remains. |
| `ready_with_tracked_items` | Only low-risk, explicitly owned items remain and policy permits release. |
| `hold` | Required correction/query/reproof or approval is unresolved. |
| `blocked` | Baseline, file identity, authority, output, or material risk prevents a defensible release. |
| `post_publication_case` | Output is released but an authorized correction/version workflow is required. |

### Required release report

1. baseline/proof/output identity and fixity;
2. summary by defect/status/impact;
3. open queries and correction decisions;
4. accepted corrections and reproof results;
5. navigation/asset/reference/accessibility results;
6. upstream dependency status and refresh date;
7. unresolved risks and tracked items;
8. final release recommendation;
9. human signatory, date, and decision ID.

## 22. Intervention thresholds

| Threshold | Use | Examples |
|---|---|---|
| `AUTO_RECORD` | Capture a deterministic difference or event without changing content. | Page count, file ID, visible line break. |
| `NO_ACTION` | Difference is harmless or approved, with evidence. | Approved blank page, valid URL wrap. |
| `CORRECT` | Minimal correction restores baseline/meaning. | Missing word, wrong glyph, placeholder. |
| `QUERY` | Authorization, intent, or production response is needed. | Vague comment, author alteration, design variation. |
| `REPLACE_ASSET` | Exact approved asset replacement is required. | Missing/wrong figure file. |
| `REPROOF` | Accepted change may affect related pages/objects/indexing/output. | Pagination or table correction. |
| `HOLD` | Current-stage issue remains unresolved. | Open query, failed correction, missing caption. |
| `BLOCK` | Baseline/authority/fixity/critical output problem prevents release. | Unknown final file, unapproved central meaning change. |
| `REFER` | Specialized owner must decide. | Accessibility conformance, rights/privacy, integrity status. |

## 23. Evidence requirements

### Minimum evidence by Skill

| Skill | Minimum evidence |
|---|---|
| PPR-01 | Baseline/proof/output IDs, file paths, fixity/hash or stable identifier, capture event. |
| PPR-02 | Comparison pair, difference location, approved variation lookup, classification. |
| PPR-03 | Exact current/expected text or glyph, protected baseline, impact assessment. |
| PPR-04 | Page/layout evidence, design rule, affected navigation/index records. |
| PPR-05 | Asset/caption/source/permission IDs, proof image or object comparison, replacement file if needed. |
| PPR-06 | Visible citation/reference/target comparison and upstream RCI/TE status. |
| PPR-07 | Correction record, decision, owner, incorporation output, reproof result. |
| PPR-08 | Format, target, test/evidence, specialist owner, conformance limitation. |
| PPR-09 | Identifier, error/impact, authorized decision, notice/version link, reader status. |
| PPR-10 | Gate matrix, open-risk summary, dependency refresh, signatory, release event. |

## 24. Confidence

Confidence describes confidence in the difference/defect classification, not the author’s intent or the overall quality of the book.

| Confidence | Meaning | Treatment |
|---|---|---|
| High | Direct baseline comparison or deterministic output defect is clear. | May propose minimal correction; human/production owner approves. |
| Medium | Difference is credible but design, source, or format context is incomplete. | Query/route; do not close. |
| Low | Baseline inaccessible, output ambiguous, or classification depends on preference. | Signal/source unavailable; human review. |

## 25. Human-escalation rules

Escalate when:

- the baseline or final file cannot be identified;
- a difference changes meaning, data, attribution, credit, source identity, privacy, rights, or accessibility;
- an author proposes a substantive rewrite, new section, or major addition;
- the design/production authority is unclear;
- a correction could alter pagination, indexing, TOC, cross-references, or other downstream objects;
- an output may be corrupt, incomplete, or inaccessible;
- a confidential proof or sensitive image/data was shared improperly;
- post-publication correction, removal, retraction, or expression-of-concern status is involved;
- an upstream integrity, citation, technical, or rights issue remains open;
- a correction instruction is vague or its intended meaning is uncertain.

## 26. Tool and model routing

| Task | Preferred route | Human checkpoint |
|---|---|---|
| File identity/fixity | Manifest/hash/provenance tool | Production/QA confirms baseline |
| Text comparison | Version-aware diff + constrained model | Proof editor samples differences |
| PDF/page comparison | PDF text/layout extraction + visual review | Human checks page-level defects |
| Symbol/equation/code | Protected baseline comparison | Technical editor confirms meaning |
| Figures/tables | Asset/metadata comparison | Technical/production owner |
| References/cross-references | RCI/TE status + visible output check | Skill owner resolves substantive issue |
| Correction grid | Structured log and annotation parser | Production owner accepts/rejects |
| Accessibility | Format-specific checker + specialist review | Accessibility owner signs conformance |
| Post-publication status | Metadata/version record | Senior editorial/metadata owner |
| Release report | Structured report generator | Named human signatory |

Do not use a generic model to rewrite proof text, infer missing symbols, or decide a public correction status.

## 27. QA tests

### 27.1 Automated tests

- every proof run has a baseline ID, proof ID, output format, and fixity/provenance record;
- every finding has a precise page/object locator and defect type;
- approved variations are loaded before difference classification;
- every correction includes current and expected state;
- accepted corrections include incorporation output and reproof result;
- open queries block the relevant gate;
- unapproved author alterations do not pass as routine proof corrections;
- high-impact symbol/name/number/asset errors are not classified as cosmetic;
- output-format-specific defects are not hidden by a pass in another format;
- status/version changes preserve original/update links;
- accessibility checks do not emit a conformance claim without specialist evidence;
- final release requires human signatory;
- Markdown and Word headings match exactly.

### 27.2 Human QA

- review a sample of approved variations for false positives;
- compare corrections against the approved baseline and production log;
- inspect page-level navigation, tables, figures, captions, notes, and special characters;
- verify that no authorial rewriting slipped through;
- confirm reproof scope after each accepted correction;
- inspect final output identity/fixity and release record;
- review accessibility findings with the designated specialist;
- confirm post-publication cases preserve the original record.

### 27.3 Evaluation set

Run `04_Evaluation_Set/evaluation_set.md` with at least 45 fixtures. The set covers baseline ambiguity, approved variations, text/symbol defects, layout/navigation, visual objects, references, accessibility, correction states, post-publication updates, fixity, and confidentiality.

## 28. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Latest file assumed to be baseline | Require stable IDs/fixity and explicit baseline record. |
| Every visual difference called an error | Consult approved variation/design log. |
| Proof stage becomes developmental editing | Enforce minimum-change thresholds and escalation. |
| Vague correction comment interpreted by model | Require exact location/current/replacement state. |
| Correction marked resolved when only submitted | Require incorporation and reproof evidence. |
| Low-resolution proof art treated as final image quality | Compare approved high-resolution asset record. |
| Page correction causes index/TOC drift | Reproof related navigation objects. |
| Accessibility checklist treated as conformance | Require target and specialist review. |
| Post-publication update silently overwrites original | Preserve linked notice/version/status record. |
| Approved design variation flagged repeatedly | Maintain versioned variation log. |
| Upstream issue ignored during proof | Refresh and import dependency statuses at release. |
| Sensitive proof shared outside channel | Immediate security/editorial incident escalation. |

## 29. Examples

### 29.1 Missing word

**Baseline:** “The results support the stated limitation.”  
**Proof:** “The results support stated limitation.”  
**Output:** `PPR-03`, `typesetter_error`, high confidence; location/page; replacement “the stated limitation”; reproof affected sentence/page.

### 29.2 Approved variation

**Baseline:** Chapter begins on an even page.  
**Proof:** A blank verso page appears.  
**Decision log:** Recto chapter openings approved.  
**Output:** `approved_variation`, no action; retain design evidence.

### 29.3 Ambiguous author request

**Comment:** “Make this stronger.”  
**Output:** `query_open`; request exact replacement and authorization; no model rewrite.

### 29.4 Meaning-bearing symbol

**Baseline:** `p < .05`.  
**Proof:** `p > .05`.  
**Output:** `PPR-03`, critical factual/meaning error; hold/reproof; route statistical/author owner.

### 29.5 Unincorporated correction

**Correction log:** Accepted correction replaces “affect” with “effect.”  
**New proof:** Still says “affect.”  
**Output:** `PPR-07`, unresolved correction; return to production; do not close until new proof passes.

### 29.6 Post-publication significant change

**Issue:** Central table value was wrong in released chapter; authorized owner approves correction.  
**Output:** `PPR-09`; preserve original, create linked correction/version record, document impact and date, update reader-facing status.

## 30. Counterexamples

- Do not correct a blank page that is approved for recto chapter openings.
- Do not reject a low-resolution proof image when the approved final high-resolution asset is correctly linked and inspected.
- Do not rewrite an author’s paragraph because it reads awkwardly at proof stage.
- Do not treat a harmless URL line wrap as a broken reference without testing the link.
- Do not infer a missing word when the baseline is inaccessible.
- Do not accept a substantive author alteration as a typo correction.
- Do not close an accepted correction from the correction log alone.
- Do not claim accessible PDF conformance because headings look correct visually.
- Do not silently change the released record for a significant post-publication error.
- Do not classify an approved design change as a typesetter error.
- Do not solve a page-flow problem by changing content without production authorization.

## 31. Evaluation set and acceptance criteria

The evaluation set is versioned at `MWM-PPR-EVAL-0.1` and contains 45 fixtures. Acceptance requires:

1. 100% of fixtures with missing/ambiguous baselines remain blocked or source-unavailable;
2. approved variations are not auto-corrected;
3. no substantive author alteration passes as a routine proof correction;
4. all meaning-bearing symbol/name/number/asset errors receive high/critical treatment;
5. all open queries remain open until explicit answers are recorded;
6. accepted corrections are not resolved without incorporation and reproof evidence;
7. format-specific output defects are detected independently;
8. accessibility results do not overclaim conformance;
9. significant post-publication updates preserve linked record/version history;
10. final release always has a human signatory and fixity/provenance evidence.

## 32. Versioning and governance

Version the specification, correction-log schema, defect taxonomy, evaluation set, baseline manifest, variation log, and release report together when a behavioral change occurs. Each change requires:

- change ID and rationale;
- affected Skill/rule IDs;
- baseline/proof examples;
- correction-limit decision;
- updated counterexamples and fixtures;
- regression results;
- owner approval and effective date;
- superseded version and migration note.

Preserve every proof/correction/final-output event required to reconstruct what was reviewed, changed, accepted, rejected, and released.

## 33. Release checklist

- [ ] Approved manuscript/copyedited version identified.
- [ ] Proof and final output IDs/formats recorded.
- [ ] File identity/fixity/provenance captured.
- [ ] Approved variation/design log loaded.
- [ ] Proof is complete and not corrupted.
- [ ] All production queries answered or explicitly escalated.
- [ ] Text, names, numbers, symbols, equations, code, and special characters checked.
- [ ] TOC, headings, running heads/feet, page numbers, breaks, placeholders, and navigation checked.
- [ ] Figures, tables, captions, notes, labels, source lines, and assets checked.
- [ ] References, notes, links, and cross-references checked against upstream statuses.
- [ ] Accepted corrections have exact instructions, incorporation evidence, and reproof results.
- [ ] Accessibility/output checks completed for each in-scope format or assigned to specialist owner.
- [ ] No unresolved high/critical issue or ambiguous baseline remains.
- [ ] Post-publication status/version records are updated where applicable.
- [ ] Human signatory records release, tracked items, hold, or block.

## 34. Open decisions for MWM

1. Approve the MWM proof baseline and correction-grid/annotation protocol.
2. Define allowed proof-stage corrections and senior-approval thresholds.
3. Define the approved variation/design log and its owner.
4. Assign volume-editor/production responsibility for collating contributor corrections.
5. Define in-scope final formats and accessibility targets.
6. Define image-quality comparison between proof previews and final assets.
7. Define mandatory reproof scope for page/index/TOC/cross-reference changes.
8. Approve the MWM post-publication correction/version/status taxonomy and notice process.
9. Define fixity/provenance retention and access controls.
10. Define confidentiality incident handling for proofs and corrections.

## 35. Research basis and limitations

The corpus is grounded in supplied MWM/AISL/SEFI/APA materials; Wiley, Springer Nature, Oxford University Press, University of Arkansas Press, University Press of Florida, IOP, Franz Steiner Verlag, Taylor & Francis, Elsevier, Crossref, NISO CREC, W3C, and Library of Congress PREMIS.

The strongest shared finding is that proofing is a controlled comparison and correction process, not another round of writing. Mature systems limit changes, require exact annotations, answer queries, check visible navigation and objects, and recheck incorporated corrections. Versioning and preservation sources add a second requirement: the released output must be identifiable and its update history reconstructable.

Some OUP sources were web-accessed but blocked for local automated capture. Their URLs and limitations are recorded in the manifest and access log. Publisher-specific correction limits and MWM post-publication status rules remain open local decisions.
