# Modeling What Matters — University Press Workpile

**Workpile ID:** `tt.university-press.modeling-what-matters`
**Status:** proposed real-work candidate; not yet authorized for bulk execution
**Owner:** Eric Tucker Personal / Workbench Director
**Workstream:** University Press — metaphorical Press-focused center of work in Eric Tucker Personal's ecosystem
**Jurisdiction:** Tech Triangle
**Contributors:** Eric Study Group; Sheryl Study Group where explicitly authorized; Codex, Gemini, Hermes, and Wispr Flow/voice as driving or execution surfaces
**Real-world scope:** two volumes; approximately 100 chapters; approximately 100 real authors; real publishing relationship

## 1. Purpose

Create a repeatable, inspectable production workflow for reviewing a folder of real Modeling What Matters chapters against approved scholarly and editorial skills, then returning a folder of chapter-level deliverables and volume-level rollups.

The desired outcome is not a series of isolated chat sessions. It is a durable workpile that can accept a source folder, execute a defined skill set, route exceptions to human review, and return a traceable package.

## 2. University Press interpretation

University Press is a metaphorical establishment name for a Press-focused center of work in Eric Tucker Personal's ecosystem. It is not a Study Group department or a separate legal press, program, brand, or external organization unless explicitly designated later.

## 3. Initial skill set

1. **APA 7 compliance review** — identify and classify departures from the approved APA 7 requirements; distinguish substantive, editorial, and uncertain findings.
2. **Citation-integrity review** — compare in-text citations, reference entries, quotations, claims, and available source evidence; preserve uncertainty when source access is incomplete.
3. **Style-guide consistency review** — compare each chapter with the applicable project style guide and record deviations, harmonization questions, and unresolved decisions.
4. **Scholarly editorial integrity review** — check provenance, claim-to-evidence alignment, internal consistency, and publication-readiness risks.
5. **Independent quality review** — inspect a sample or full set of outputs independently from the producing worker and record acceptance or required correction.

The skill IDs and canonical versions remain subject to the skill-registry and lineage decisions. A GitHub or Hermes presence is not, by itself, evidence that a skill is production-ready.

## 4. Input contract

The workpile should receive:

- a registered source folder or preservation bundle;
- chapter identifiers and expected chapter count;
- volume and chapter ordering;
- author metadata only as necessary for the task;
- the governing APA 7 interpretation or checklist;
- the project style guide and version;
- available source/reference materials;
- identity, classification, rights, and retention instructions;
- acceptance criteria and exception policy; and
- an explicit human decision about whether bulk execution is authorized.

Original chapters remain unmodified. All reviews and derivatives are written to a separate output tree with stable IDs and source digests.

## 5. Proposed batch workflow

```text
intake and inventory
  -> identity / rights / classification check
  -> chapter manifest and source digests
  -> designed-ready review jobs
  -> bounded parallel skill execution
  -> deterministic and independent checks
  -> chapter-level revision inventory and clean/marked outputs where authorized
  -> exception and uncertainty docket
  -> volume-level rollup
  -> Eric human acceptance / release decision
  -> learning record and workflow improvement backlog
```

Codex, Gemini, Hermes, and voice-driven interaction may all participate. Hermes provides administrative continuity, routing, approvals, audit, and reconciliation across surfaces; it does not need to be the originating interface for every task.

## 6. Deliverable package

For each chapter, subject to the agreed output contract:

- `chapter_<id>_source_receipt.json`;
- `chapter_<id>_apa7_review.md`;
- `chapter_<id>_citation_integrity_review.md`;
- `chapter_<id>_style_guide_review.md`;
- `chapter_<id>_editorial_integrity_review.md`;
- `chapter_<id>_independent_quality_review.md`;
- `chapter_<id>_decision_docket.md` for unresolved or human-reserved questions; and
- any clean or marked revision file only after the output and overwrite boundaries are approved.

At the volume level:

- chapter manifest and completion matrix;
- issue and exception rollup;
- repeated-pattern report;
- quality and acceptance summary;
- unresolved decision docket; and
- learning record comparing work activity with final product quality.

## 7. Acceptance criteria

1. Every input chapter has a stable ID, source digest, volume, expected status, and disposition.
2. Originals are preserved and no source file is overwritten.
3. Every completed review identifies the skill/version, worker or model, driving surface, identity, timestamp, evidence scope, and confidence/uncertainty.
4. APA 7, citation integrity, style-guide, and editorial findings are separated rather than collapsed into one score.
5. Missing evidence and unresolved scholarly judgments remain visible.
6. Independent review is genuinely separate from production execution.
7. The output folder is complete, machine-checkable, and linked to the source manifest.
8. Eric Tucker Personal accepts the volume-level package before any external delivery or publication effect.
9. Corrections and workflow improvements become explicit follow-up work rather than silent changes.

## 8. Gates and boundaries

- **G0:** confirm identity, source rights, classification, and scope.
- **G1:** commit the real batch workpile and acceptance criteria.
- **G2:** accept the completed review package and resolve material exceptions.
- **G3:** approve any external delivery, publication, or consequential change.
- **G5:** approve any skill/role promotion, immutable pin, or permission expansion.
- **G6:** approve any workflow, policy, routing, retention, or release-standard change derived from learning.

No bulk run, external delivery, publication, or source overwrite is authorized by this draft alone.

## 9. Pilot path

Begin with a bounded sample selected from the real corpus rather than all chapters at once. The sample should be large enough to expose batching, provenance, exception, and quality patterns, but small enough for Eric and the relevant contributors to inspect manually.

After the sample is accepted, expand in waves with a manifest, checkpoint, retry/unknown policy, independent review, and volume-level human acceptance.

