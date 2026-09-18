# Chapter Completeness & Production Readiness Specification

**Specification ID:** `MWM-CPR-SPEC`  
**Version:** `0.1.0-draft`  
**Status:** Draft for editorial-owner review  
**Skill family:** Chapter Completeness & Production Readiness  
**Research corpus:** `MWM-CPR-2026-08`  
**Scope:** Edited-volume chapters from intake through production handoff and release  
**Out of scope:** Developmental editing, substantive copyediting, deep source/claim adjudication, legal permission determinations, and final post-typesetting proof review  
**Last revised:** August 13, 2026

## 1. Purpose

This family determines whether a chapter and its supporting package contain the components, metadata, evidence, approvals, links, and files required for the current editorial stage. It produces a versioned component inventory, dependency-aware readiness report, and human-signable release decision.

The family answers:

> Is the right thing present, in the right version, with the right companion records, owner, and evidence for this stage?

It does not answer every substantive question about whether a component is true, elegant, legally sufficient, accessible in conformance, or stylistically correct. Those judgments remain with the relevant downstream Skill or human owner.

### 1.1 Core distinction

The system must keep these states separate:

- **present:** an object or file exists;
- **complete:** required fields and companion records are present;
- **verified:** a downstream Skill or authorized source check supports its content/status;
- **approved:** the responsible human or authority has accepted it;
- **accessible:** the applicable accessibility review has passed;
- **cleared:** the rights/permissions owner has accepted the permission evidence;
- **ready:** all stage-specific gates and dependencies are closed or explicitly accepted.

No presence check may silently certify the other states.

## 2. Triggers

| Trigger | Required action | Default mode |
|---|---|---|
| New chapter intake | Create profile, component inventory, package manifest, and initial gaps. | Baseline |
| Author resubmission | Compare current version with prior inventory and preserve superseded records. | Delta review |
| Copyediting handoff | Verify clean package, metadata, required chapter components, and upstream findings. | Stage gate |
| Technical-editing handoff | Reconcile figures, tables, captions, notes, cross-references, and asset records. | Stage gate |
| Scholarly/integrity review complete | Consume disclosure, ethics, contributor, and source-status findings. | Dependency review |
| Production handoff | Verify final source files, assets, permissions evidence, metadata, and naming. | Handoff gate |
| Proof intake | Confirm what was handed to typesetting and create proof baseline. | Baseline for proof |
| Release decision | Run all applicable gates and produce a signable release record. | Release validation |
| Profile/rule change | Recompute applicability and identify newly opened gaps. | Rule migration |

## 3. Inputs

### 3.1 Required inputs

- chapter manuscript and current version identifier;
- MWM chapter guidance, contract, approved volume decisions, and component profile;
- volume table of contents and chapter ordering;
- author/contributor and affiliation records;
- abstract, keyword, biography, and discoverability metadata where required;
- heading/section inventory and required appendices/boxes;
- figure/table/asset inventory and caption/source-line records;
- permissions log and available licenses/letters/author confirmations;
- citation/reference/cross-reference status from RCI and Technical Editing;
- disclosure/ethics/AI/declaration status from Scholarly/Editorial Integrity;
- clean-file, tracked-change, file-name, and package manifest;
- current stage and downstream delivery requirements.

### 3.2 Optional or conditional inputs

- supplementary data, code, software, media, or repository links;
- alt-text/image-description forms;
- accessibility test results;
- author bios, ORCID/ROR or other identifiers;
- funding and award metadata;
- index terms, subject classifications, graphical abstracts, or cover suggestions;
- publisher-specific templates and checklists;
- previous versions and decision log;
- translation, permissions, anonymization, or adaptation records.

### 3.3 Protected inputs

Protect author contact information, permissions correspondence, licenses, unpublished data, ethics/consent records, confidential reviewer/editor comments, and unpublished manuscript versions. The readiness Skill should store references to protected records and access status rather than reproducing sensitive contents unnecessarily.

## 4. Authoritative sources and rule hierarchy

| Tier | Authority | Application |
|---|---|---|
| 1 | MWM contract, chapter guidance, approved volume decisions, and release policy | Controls what is required and when. |
| 2 | Current component profile, template, chapter metadata, decision log, and production instructions | Controls the chapter’s actual configuration and accepted exceptions. |
| 3 | Explicitly delegated APA, discipline, publisher, accessibility, permissions, or metadata rules | Controls specialized fields when the delegation is recorded. |
| 4 | NISO/JATS/JATS4R, WCAG/WAI, and publisher checklists | Supplies structured-content and implementation exemplars. |
| 5 | Generic model expectations or another publisher’s checklist | Generates a question only; cannot create an MWM gate. |

When sources conflict, record the conflict and apply the highest applicable authority. A publisher exemplar may reveal a useful field but cannot override an approved MWM rule. A template may show where a component belongs but cannot establish that the component is required.

## 5. Preconditions

Before running a stage gate, verify:

1. chapter ID, volume ID, version ID, and current stage are recorded;
2. a versioned MWM component profile exists;
3. the profile declares required, conditional, optional, and delegated items;
4. current publisher/production instructions are attached where applicable;
5. all upstream Skills have supplied statuses or an explicit `not_run` reason;
6. the package can distinguish current files from superseded files;
7. every open item has an owner, next action, and due stage;
8. protected records have approved access paths;
9. the release signatory role is known.

If a precondition fails, return `blocked_profile`, `blocked_version`, or `blocked_authority` with the missing prerequisite. Do not substitute a generic checklist.

## 6. Component profile

### 6.1 Profile record

```yaml
profile_id: MWM-CP-000
profile_version: 0.1.0
volume_id: MWM-VOL-000
chapter_type: research_chapter | conceptual_chapter | case | review | other
stage: intake | copyedit_handoff | production_handoff | proof_intake | release
publisher_profile: null | named_profile_version
required_components: []
conditional_rules: []
optional_components: []
delegated_owners: []
accessibility_target: declared_target_or_null
release_signatory_role: role
effective_date: ISO-8601
approved_by: role/person
```

### 6.2 Component record

```yaml
component_id: CPR-CMP-000
component_type: chapter | title | author | affiliation | biography | abstract | keyword_set | section | appendix | box | figure | table | caption | note | source_line | alt_text | permission | citation | reference | cross_reference | declaration | supplementary_file | manuscript_file | metadata_record
label: human-readable name
requiredness: required | conditional | optional | delegated
applicability: applicable | not_applicable | unresolved
status: required | present_unverified | complete | verified | approved | missing | blocked | superseded
stage_due: stage
source_or_file: path/URI/record id
linked_components: []
owner: role/person/team
evidence: []
dependency_ids: []
release_effect: none | track | hold | block
last_checked: ISO-8601
```

### 6.3 Evidence record

```yaml
evidence_id: CPR-E-000
component_id: CPR-CMP-000
evidence_type: file | metadata | owner_confirmation | downstream_result | approval | access_test | decision_record
locator: path/page/paragraph/object id/URL
access_status: local | linked | protected | web_only | unavailable
observed_fact: concise fact about presence or linkage
authority: profile/rule/decision/source id
captured_at: ISO-8601
reviewer: tool/model/person
```

## 7. Component status vocabulary

| Status | Meaning | Default response |
|---|---|---|
| `required` | Required by the profile but not yet assessed or supplied. | Query/assess. |
| `conditional` | Requirement is activated only when a stated condition is met. | Evaluate applicability. |
| `optional` | Useful but not a release requirement. | Track without blocking. |
| `not_applicable` | Profile/decision says it does not apply, with rationale. | Close applicability gate. |
| `present_unverified` | Object/file exists, but correctness/approval belongs elsewhere. | Pass presence; retain downstream dependency. |
| `complete` | Required fields and companion records are present for this stage. | Pass component gate. |
| `verified` | A downstream or authorized check confirms the relevant substantive status. | Pass relevant dependency. |
| `approved` | Responsible human/authority has accepted it. | Close approval gate. |
| `missing` | Required object or evidence is absent. | Query or hold. |
| `blocked` | Cannot close because a dependency, authority, or decision is absent. | Hold/route. |
| `superseded` | Belongs to an earlier version and is not current. | Preserve history; exclude from current package. |

## 8. Operating principles

### 8.1 Profile before checklist

The system must load the chapter’s profile before checking requirements. It must not treat another publisher’s checklist, a generic book template, or a model’s expectation as an MWM requirement.

### 8.2 Presence is not quality

“File exists,” “abstract exists,” “permission email exists,” and “alt text exists” are observable facts. They do not establish accuracy, legal sufficiency, accessibility conformance, or scholarly adequacy.

### 8.3 Conditionality must be explicit

If a chapter has no figures, a figure gate may close as `not_applicable` only if the profile supports that decision. If the chapter uses interviews, software, data, or third-party material, the relevant conditional gates must activate.

### 8.4 Dependencies are first-class

A chapter can be component-complete but not release-ready because RCI, Integrity, Technical Editing, or Copyediting has an unresolved material finding. Readiness consumes and preserves those statuses.

### 8.5 Stage specificity

An item due at final submission should be tracked at intake, not treated as an intake blocker. A clean-file requirement may block production handoff even if it was not required at early drafting.

### 8.6 No silent repair

The Skill may normalize a manifest or report a deterministic filename mismatch, but it must not invent missing metadata, renumber assets, rewrite abstracts, choose between titles, or delete duplicate files without authority.

### 8.7 Human sign-off

A release decision is a human-owned authorization. The model can assemble evidence, recommend a state, and identify blockers; it cannot release the chapter autonomously unless MWM explicitly delegates that authority.

## 9. Skill map

| Skill ID | Skill | Core question | Default intervention |
|---|---|---|---|
| `CPR-01` | Profile and Rule Applicability | What is required for this chapter, stage, and publisher profile? | Load, validate, or block profile. |
| `CPR-02` | Chapter Identity and File Package | Is the current clean package identifiable and complete? | Query, quarantine ambiguity, or pass manifest. |
| `CPR-03` | Front Matter and Chapter Metadata | Are title, authors, affiliations, contact, and required metadata present and linked? | Query or route identity owner. |
| `CPR-04` | Abstracts, Keywords, Bios, and Discoverability | Are chapter/full-work metadata fields present, scoped, and scheduled? | Track/query; do not rewrite. |
| `CPR-05` | Body Structure and Required Components | Does the chapter contain the required sections, appendices, boxes, and headings? | Missing-component report; TE owns structural correctness. |
| `CPR-06` | Figures, Tables, Captions, Notes, and Alt Text | Does each visual object have the required handoff records and asset links? | Asset matrix and dependency gaps. |
| `CPR-07` | Permissions, Source Lines, and Rights Evidence | Is required rights documentation present and linked? | Flag missing evidence; rights owner decides sufficiency. |
| `CPR-08` | Citations, References, and Cross-References | Are expected links/sections/records present and targetable? | Consume RCI/TE; do not duplicate substantive checks. |
| `CPR-09` | Declarations and Supplementary Components | Are applicable disclosures, ethics, AI, data, software, and supplements represented? | Conditional checklist and Integrity route. |
| `CPR-10` | Accessibility and Structured Metadata | Is the package prepared for the declared accessibility and metadata target? | Evidence gate; specialized owner verifies conformance. |
| `CPR-11` | Cross-File Reconciliation | Do manuscript, assets, caption lists, logs, and metadata describe the same package? | Exception report and owner routing. |
| `CPR-12` | Stage Readiness and Release Decision | Can the chapter move to the next stage under current rules? | Human-signable report, hold, or release recommendation. |

## 10. Procedure

### Step 1 — Initialize

Record chapter/volume IDs, version, stage, profile version, publisher profile, tools, reviewer, date, and signatory role.

### Step 2 — Load and validate the profile

Check that every requirement has a requiredness state, applicability condition where relevant, authority, owner, stage due, and release effect. If the profile is incomplete or conflicting, stop at `blocked_profile`.

### Step 3 — Build the component graph

Create stable object IDs for title, authors, sections, abstracts, keywords, figures, tables, captions, notes, sources, permissions, declarations, files, and metadata. Link callouts to objects, objects to assets, assets to permissions/source lines, and chapter records to volume records.

### Step 4 — Inventory the package

List every file, extension, version, filename, date, hash or stable identifier if available, and declared purpose. Mark current, superseded, duplicate, unknown, or missing. Do not use timestamp alone to decide which file is final.

### Step 5 — Run presence and applicability checks

Evaluate required and conditional components. For each item, record evidence and status. Use `not_applicable` only with a condition/rationale and profile authority.

### Step 6 — Run linkage and reconciliation checks

Check that the manuscript, metadata sheet, asset folder, captions, permission log, source lines, supplementary files, and volume TOC refer to the same objects and version. Create one exception per mismatch.

### Step 7 — Consume upstream results

Import RCI, Style Guide, Technical Editing, Copyediting, and Scholarly/Editorial Integrity results. Preserve their owners and severity. A completeness pass does not close their substantive findings.

### Step 8 — Apply stage gate

Map open items to the current stage. Items due later remain `tracked`; material items required now become `hold` or `block`; accepted exceptions require an approved decision record.

### Step 9 — Produce report and handoff

Generate the component matrix, missing/blocked list, dependency map, package manifest, unresolved-risk summary, and recommendation. A human signatory records release, conditional release, hold, or block.

### Step 10 — Preserve version lineage

Freeze the report against the current version. On resubmission, compare deltas, retain superseded records, and rerun affected gates.

## 11. CPR-01 — Profile and Rule Applicability

### Purpose

Create the authoritative, versioned set of rules that determines what this chapter must deliver at this stage.

### Detection logic

- Confirm chapter type, volume, stage, publisher/contract profile, and accessibility target.
- Load required, conditional, optional, and delegated component definitions.
- Check that every conditional rule has an activation condition.
- Check that every delegated rule names an owner and authority.
- Detect conflicting profile versions or unapproved changes.
- Return `blocked_profile` when the profile cannot support a defensible gate.

### Intervention

Do not create missing requirements from publisher exemplars. Ask the volume owner to approve a profile or record a local decision.

## 12. CPR-02 — Chapter Identity and File Package

### Required checks

- chapter and volume identifiers;
- current title and author names;
- clean manuscript file;
- source/editable files required by the stage;
- accepted tracked-change/comments state;
- asset and supplementary folders;
- metadata/handoff sheets;
- naming convention and version ID;
- manifest of current and superseded files;
- package completeness and duplicate/ambiguous files.

### Release rule

If the system cannot identify which file is current, the package is `blocked` for the relevant handoff. Do not select the newest timestamp or largest file by inference.

## 13. CPR-03 — Front Matter and Chapter Metadata

### Component classes

- chapter title and subtitle;
- author/contributor names;
- affiliations and corresponding contact;
- identifiers where required;
- author biographies;
- chapter number/order;
- volume title and editor metadata;
- acknowledgments;
- funding/conflict/ethics/AI declarations where applicable;
- submission and version dates.

### Detection logic

Compare the metadata sheet, manuscript title page, volume TOC, filename, author forms, and approved decisions. Report mismatches without choosing one record. Route identity/authorship concerns to Scholarly/Editorial Integrity or the volume owner.

## 14. CPR-04 — Abstracts, Keywords, Bios, and Discoverability

### Detection logic

- Check whether a chapter abstract is required and present.
- Check whether a full-work abstract/keyword set is required and present.
- Record word count, language, and structured fields where profile requires them.
- Check keyword count, scope, consistency, and association with chapter/volume level.
- Check bios and index/subject terms where required.
- Track items due later rather than blocking early stages.

### Boundary

This Skill checks presence, field-level compliance, and cross-record consistency. It does not judge whether an abstract accurately represents the argument; Scholarly/Editorial Integrity or an assigned editor owns that review. It does not rewrite or generate an abstract or keywords unless a separate authorized drafting Skill is invoked.

## 15. CPR-05 — Body Structure and Required Components

### Detection logic

- Compare heading/section tree with the approved chapter profile or template.
- Check required introduction, methods, findings, discussion, conclusion, or other sections only when the chapter type activates them.
- Check appendices, boxes, endnotes, glossary, references, and supplementary material.
- Verify chapter-to-volume order and required cross-chapter links.
- Identify missing or orphaned components.

### Boundary

The Skill reports structural presence and relationships. Technical Editing owns heading hierarchy, numbering, section semantics, and structural correctness. Developmental editing is out of scope.

## 16. CPR-06 — Figures, Tables, Captions, Notes, and Alt Text

### Required object record

```yaml
asset_id: CPR-ASSET-000
object_type: figure | table | box | media | supplementary_object
number_or_label: Figure 1 / Table 2 / etc.
manuscript_callouts: []
asset_file: path or URI
caption_record: id/path
notes_record: id/path/null
source_line_record: id/path/null
permission_record: id/path/null
alt_text_record: id/path/null
accessibility_status: not_applicable | present_unverified | reviewed | blocked
technical_status: not_run | passed | issue
owner: role/person
```

### Detection logic

- Extract every callout and compare it to an object and asset.
- Compare object numbering/labels across text, caption list, asset name, and metadata.
- Check caption, notes/legend, source line, permissions, and alt-text fields when activated.
- Check asset file type, dimensions/resolution, color, and naming only when the technical/production profile requires them.
- Flag duplicate captions, orphan assets, missing source lines, and unlinked alt text.

### Boundary

Presence and linkage do not establish visual correctness, statistical accuracy, accessibility conformance, or rights clearance. Route those questions to Technical Editing, Accessibility, or Rights.

## 17. CPR-07 — Permissions, Source Lines, and Rights Evidence

### Detection logic

- Identify third-party text, images, figures, tables, logos, media, and adapted material from source lines, author declarations, and object records.
- Check that each applicable object has a permission record, license/rights evidence, source line, or approved no-permission rationale.
- Check rightsholder, permitted formats/media, editions/versions, territory, duration, derivative/adaptation scope, and attribution fields when the local template requires them.
- Link permission evidence to the exact object and current version.
- Identify missing, expired, ambiguous, or superseded records.

### Boundary

The Skill checks documentation presence and linkage. It must not decide fair use, copyright ownership, license interpretation, or legal sufficiency. Those decisions escalate to the rights/permissions owner.

## 18. CPR-08 — Citations, References, and Cross-References

### Detection logic

- Confirm a references component exists when required.
- Confirm in-text citation/citation graph status is available from RCI.
- Confirm callouts target existing sections, figures, tables, appendices, notes, and references where applicable.
- Check link fields and supplementary-material links for presence and target availability.
- Distinguish `present_unverified` from `verified` and preserve upstream RCI/TE findings.

### Boundary

Do not duplicate APA construction, DOI verification, source-status adjudication, or deep cross-reference semantics. Completeness owns whether the expected component and target record exist; RCI/TE own correctness.

## 19. CPR-09 — Declarations and Supplementary Components

### Conditional components

- funding and award metadata;
- competing-interest statement;
- ethics approval and consent statement;
- data/code/materials availability;
- software and version/citation record;
- AI-use declaration;
- permissions and copyright acknowledgments;
- supplementary data, code, media, appendices, or repository links;
- author/contributor statement;
- acknowledgments and disclosures.

### Detection logic

Activate conditions from the chapter profile and manuscript content. Check whether the expected declaration or package record exists, is linked across relevant locations, and has an owner. Route truth/adequacy concerns to Scholarly/Editorial Integrity; route file/format concerns to Production/Technical Editing.

## 20. CPR-10 — Accessibility and Structured Metadata

### Accessibility readiness

- accessibility target is declared;
- headings and reading order have an owner/review status;
- tables have structural headers/captions where applicable;
- figures have alt text/image descriptions or an approved decorative/no-description rationale;
- links have meaningful labels where the profile requires them;
- color/contrast and non-text content checks are assigned to an appropriate owner;
- evidence of the applicable review is attached.

### Structured metadata readiness

- stable IDs exist for chapters, contributors, sections, figures, tables, references, permissions, and supplementary objects where required;
- relationships among objects are represented;
- author/affiliation, abstract, keyword, funding, permissions, and status fields are mapped;
- delivery format is recorded: human-readable handoff, spreadsheet, XML, or publisher system.

### Boundary

This Skill does not claim WCAG conformance or guarantee structured-content validity unless the specialized review and authority are recorded.

## 21. CPR-11 — Cross-File Reconciliation

### Required comparisons

| Record A | Record B | Expected relationship |
|---|---|---|
| manuscript title | metadata sheet/file name/TOC | same current title or approved variant |
| author list | title page/metadata/bio/contributor form | same people and roles, subject to integrity review |
| chapter order | volume TOC/filename | same current order or decision-log exception |
| figure/table callout | object/asset/caption list | one-to-one or approved mapping |
| source line | permission log/reference/source record | same source/object identity |
| alt text | asset ID/image-description form | exact object link |
| abstract/keywords | chapter metadata/volume metadata | correct scope and version |
| supplementary link | actual file/repository/README | target exists and is current |
| clean manuscript | package manifest | current version and status |

### Intervention

Report the mismatch with both records and route to the owner. Do not choose the more plausible value, renumber assets, or delete duplicate files silently.

## 22. CPR-12 — Stage Readiness and Release Decision

### Decision states

| Decision | Meaning |
|---|---|
| `ready` | Applicable gates are complete/approved and no material blocker remains. |
| `ready_with_tracked_items` | Required current gates pass; low-risk later-stage items have owners and due stages. |
| `conditional_hold` | Release may proceed only after named condition/approval is met. |
| `hold` | Required current item or dependency is unresolved. |
| `blocked` | Profile, version, authority, or material risk prevents a defensible decision. |
| `not_ready` | Package is incomplete for the requested stage. |

### Release report

The report must contain:

1. chapter/version/stage/profile metadata;
2. component inventory and status counts;
3. missing, blocked, and not-applicable items;
4. cross-file reconciliation results;
5. upstream Skill statuses and unresolved dependencies;
6. permissions/accessibility/declaration evidence state;
7. package/file manifest;
8. tracked-later items and due stages;
9. release recommendation and rationale;
10. human signatory, date, and superseded decision.

## 23. Intervention thresholds

| Threshold | Use | Examples |
|---|---|---|
| `AUTO_RECORD` | Record an observed object/file/field without changing content. | Asset exists; abstract word count; filename. |
| `TRACK` | Item is due later or low-risk and has an owner/date. | Biography due at final submission. |
| `QUERY` | Missing or inconsistent item can be resolved by author/editor response. | Missing abstract, title mismatch, absent source line. |
| `ROUTE` | Another Skill or authority owns the substantive decision. | RCI orphan citation, integrity disclosure question. |
| `HOLD` | Current-stage requirement or dependency is unresolved. | No clean file; figure asset absent; disputed required metadata. |
| `BLOCK` | Profile/version/authority is ambiguous or material risk prevents release. | Multiple possible final files; unresolved high-risk integrity finding. |
| `PASS` | Evidence supports the presence/completeness gate for this stage. | All required fields and links present. |

Do not use `PASS` as shorthand for “correct,” “legally cleared,” “accessible,” or “substantively approved” unless those separate gates are explicitly passed.

## 24. Evidence requirements

### Minimum evidence by Skill

| Skill | Minimum evidence |
|---|---|
| CPR-01 | Profile ID/version, authority, applicability condition, owner, effective date. |
| CPR-02 | File path/name, version ID, status, manifest, clean/comment state, supersession record. |
| CPR-03 | Current title/author/affiliation records and comparison locations. |
| CPR-04 | Abstract/keyword/bio files or fields, scope, word/count rule, due stage. |
| CPR-05 | Heading/component tree, profile rule, detected objects, missing/orphan record. |
| CPR-06 | Asset ID, callout, file, caption, notes, source line, permission, alt-text links. |
| CPR-07 | Permission log entry, source line, license/letter/confirmation reference, rights owner. |
| CPR-08 | RCI/TE status, reference component, links/targets, unresolved upstream findings. |
| CPR-09 | Activated condition, declaration/package record, owner, integrity/production route. |
| CPR-10 | Accessibility target, structured metadata map, applicable review result/evidence. |
| CPR-11 | Both sides of each mismatch and the affected component IDs. |
| CPR-12 | Gate summary, open-risk list, dependency results, recommendation, signatory. |

### Evidence quality scale

| Level | Evidence | Meaning |
|---|---|---|
| Q0 | Model expectation | Cannot establish a requirement. |
| Q1 | Object/file exists | Supports `present_unverified`. |
| Q2 | Required fields and companion links are present | Supports component `complete` for the stage. |
| Q3 | Downstream verification or owner approval is recorded | Supports a substantive/approval dependency. |
| Q4 | Human-signed stage release with all material dependencies resolved | Supports handoff/release. |

## 25. Confidence

Confidence describes confidence in the completeness classification, not content quality or legal/ethical sufficiency.

| Confidence | Meaning | Treatment |
|---|---|---|
| High | Deterministic presence, linkage, or profile comparison is clear. | May pass the narrow component gate. |
| Medium | Evidence is present but a relationship, applicability, or version detail is uncertain. | Query/track; no broad release claim. |
| Low | Classification depends on generic expectation, inaccessible source, or ambiguous profile. | `blocked_profile`, `unresolved`, or human review. |

## 26. Human-escalation rules

Escalate when:

- no approved MWM component profile exists;
- publisher/contract/profile rules conflict;
- current file/version cannot be identified;
- a missing component could affect interpretation, credit, legal rights, privacy, ethics, or safety;
- permissions evidence exists but legal sufficiency is unclear;
- accessibility conformance is claimed without specialized evidence;
- author identity, authorship, contributor, or affiliation records conflict;
- an abstract or metadata field materially contradicts the chapter;
- an upstream integrity/technical/reference finding is high risk;
- a package includes sensitive data, media, or AI material with unclear authorization;
- a release decision would require accepting an exception not documented in the decision log.

## 27. Tool and model routing

| Task | Preferred route | Human checkpoint |
|---|---|---|
| Build object/component inventory | DOCX/PDF parser + structured model | Sample object IDs and section tree |
| Profile applicability | Rule registry + deterministic validator | Volume owner approves changes |
| File/version package | File manifest + hash/name parser | Production coordinator confirms current package |
| Cross-file reconciliation | Structured comparison | Owner resolves mismatches |
| Figure/table asset check | Asset parser + TE records | Technical/production review |
| Permissions presence | Permission-log parser | Rights owner decides sufficiency |
| Metadata completeness | Schema/checklist validator | Volume editor approves exceptions |
| Accessibility readiness | Checklist + specialized tool/results | Accessibility owner confirms target/conformance |
| Upstream dependency import | Orchestrator/status API or decision log | Skill owners retain authority |
| Release report | Structured report generator | Named human signatory |

Do not use a generic model to invent metadata, choose final files, infer legal clearance, or certify accessibility.

## 28. QA tests

### 28.1 Automated tests

- every component has a stable ID, requiredness, applicability, status, owner, and stage;
- no `not_applicable` item lacks a condition/rationale and authority;
- no generic/publisher exemplar creates an MWM `required` rule without profile approval;
- `present_unverified` cannot be promoted to `verified` or `approved` without downstream evidence;
- current and superseded files are distinguishable;
- ambiguous clean-file/version packages return `blocked`;
- every figure/table callout has a reconciliation result;
- missing permission evidence is reported without a legal-sufficiency claim;
- accessibility status cannot claim conformance without appropriate review evidence;
- conditional gates close correctly for non-applicable chapter types;
- high-risk upstream findings prevent `ready` or `ready_with_tracked_items`;
- later-stage items can remain tracked without blocking an earlier stage when profile allows;
- Markdown and Word headings match exactly.

### 28.2 Human QA

- confirm MWM profile and rule applicability;
- sample complete and not-applicable cases for false positives;
- inspect cross-file mismatches and owner routing;
- verify presence/quality distinction in the report language;
- confirm permissions/accessibility findings are scoped appropriately;
- confirm human signatory and exception records;
- test resubmission/delta behavior and superseded-file handling.

### 28.3 Evaluation set

Run `04_Evaluation_Set/evaluation_set.md` with at least 38 fixtures. The set tests missing, present, conditional, profile-conflict, cross-file, rights, accessibility, version, metadata, and upstream-dependency cases.

## 29. Failure modes and mitigations

| Failure | Mitigation |
|---|---|
| Generic checklist treated as local policy | Require versioned MWM profile and authority. |
| Component presence treated as substantive quality | Separate status dimensions and owners. |
| Publisher-specific rule imported automatically | Mark as exemplar/delegated until approved. |
| JATS interpreted as required author XML | Translate to object/dependency model. |
| Missing permission log treated as infringement | Report missing evidence; escalate rights sufficiency. |
| Alt text existence treated as accessibility conformance | Require target and specialized review. |
| Newest file assumed final | Require manifest/version/supersession record. |
| Abstract/keyword generated or edited by readiness Skill | Check and query only; drafting is separate. |
| Conditional fields required for irrelevant chapters | Require activation conditions. |
| Later-stage missing item blocks early stage | Track by due stage unless material risk dictates otherwise. |
| Upstream integrity blocker ignored because package is complete | Import dependencies into CPR-12. |
| Cross-file mismatch silently repaired | Preserve both records and route owner. |
| Unowned exceptions remain open indefinitely | Require owner, due stage, and escalation date. |

## 30. Examples

### 30.1 Clean-file ambiguity

**Input:** The folder contains `Chapter4_final.docx`, `Chapter4_final_comments.docx`, and `Chapter4_final2.docx`; no manifest identifies the current version.  
**Output:** `CPR-02`, `blocked`, high confidence; list files; request production confirmation and version manifest; do not select by timestamp.

### 30.2 Conditional no-figure chapter

**Input:** The profile activates figure checks only when a callout or asset exists; the chapter is text-only.  
**Output:** Figure gates `not_applicable` with profile rationale; reference, metadata, structure, and declarations still run.

### 30.3 Permission evidence

**Input:** A third-party table appears with a source line but no permission log entry.  
**Output:** `CPR-07`, `missing`, query/hold according to stage; do not state that the use is unlawful.

### 30.4 Upstream integrity blocker

**Input:** All required files and metadata are present, but CEI-03 reports a retracted source central to the conclusion and the author response is unresolved.  
**Output:** CPR-12 `blocked`; preserve the upstream owner and evidence; completeness does not override integrity.

### 30.5 Later-stage biography

**Input:** Biography is required only at final submission; intake package lacks it.  
**Output:** `TRACK`, owner author/volume editor, due stage final submission; do not block intake.

### 30.6 Structured handoff

**Input:** MWM requires DOCX plus a human-readable asset/permissions sheet; JATS suggests typed metadata but no XML delivery.  
**Output:** CPR-10 passes the configured handoff format if fields and links are present; production may map the records later.

## 31. Counterexamples

- Do not require keywords merely because another publisher requests them if MWM has not adopted the rule.
- Do not mark a permission “cleared” because a permission email exists.
- Do not mark a figure “accessible” because alt text is present without a target/review record.
- Do not treat a complete references section as proof that citations are correct.
- Do not invent an author email, biography, abstract, keyword, source line, or license.
- Do not delete an older file without recording it as superseded and preserving the version history.
- Do not block a chapter for a conditional software field when the chapter does not use software.
- Do not make a later-stage item an intake blocker unless the profile or risk rule says so.
- Do not resolve a title mismatch by choosing the longest, newest, or most grammatical title.
- Do not declare the chapter ready when an upstream high-risk integrity or technical issue remains unresolved.
- Do not force authors to deliver XML when the MWM handoff requires only DOCX and structured companion records.

## 32. Evaluation set and acceptance criteria

The evaluation set is versioned at `MWM-CPR-EVAL-0.1` and contains 38 fixtures. Acceptance requires:

1. 100% correct profile/applicability treatment for required and conditional cases;
2. 100% detection of ambiguous current-file/version packages;
3. no legal/accessibility/substantive certification from presence evidence alone;
4. correct detection of missing/orphaned figures, tables, captions, source lines, and supplementary files;
5. correct tracking of later-stage items without premature blocking;
6. correct preservation of upstream high-risk blockers;
7. cross-file mismatches reported with both records and an owner;
8. every release recommendation contains evidence, open items, dependencies, signatory, and release effect;
9. no silent generation, deletion, renumbering, or selection of content-bearing components.

## 33. Versioning and governance

Version the specification, component profile, rule registry, evaluation set, schema, and release report together when a change affects behavior. Each change requires:

- change ID and rationale;
- affected profile/rule/skill IDs;
- authority and effective date;
- before/after fixture or example;
- regression results;
- owner approval;
- superseded version and migration note.

A publisher profile must be versioned separately from MWM policy. Reusing a publisher checklist does not change MWM requirements until the local profile explicitly adopts it.

## 34. Release checklist

- [ ] Chapter, volume, version, and stage identified.
- [ ] Approved MWM component profile loaded and versioned.
- [ ] Publisher/contract profile and exceptions recorded.
- [ ] Current clean manuscript and package manifest identified.
- [ ] Superseded/duplicate files are labeled and excluded from current handoff.
- [ ] Title, authors, affiliations, contact, and required identifiers reconciled.
- [ ] Abstracts, keywords, bios, and discoverability fields are present or tracked by due stage.
- [ ] Required body sections, appendices, boxes, notes, and references are present.
- [ ] Figure/table/asset records, captions, notes, source lines, and alt-text fields are linked.
- [ ] Permission log and evidence are present for applicable third-party material.
- [ ] Citations, references, links, and cross-references have upstream status records.
- [ ] Conditional declarations and supplementary files are activated and checked.
- [ ] Accessibility target and evidence owner are recorded.
- [ ] Cross-file reconciliation is complete or exceptions have owners.
- [ ] Upstream RCI, Style Guide, TE, Copyediting, and Integrity findings are imported.
- [ ] No material unresolved blocker remains for the requested stage.
- [ ] Later-stage items have owners and due dates.
- [ ] Human signatory records ready, conditional hold, hold, or block.

## 35. Open decisions for MWM

1. Approve the complete MWM component profile by chapter type and stage.
2. Assign ownership for chapter metadata, front/back matter, biographies, and index terms.
3. Approve abstract/keyword requirements and chapter/full-work scope.
4. Approve author, affiliation, email, ORCID/ROR, and contributor metadata fields.
5. Define accessibility target, alt-text policy, table requirements, and testing owner.
6. Define figure/table asset formats, resolution, color, and naming conventions.
7. Approve permission-log fields, evidence standards, and rights-owner escalation.
8. Define conditional rules for data, software, AI, ethics, consent, funding, and supplements.
9. Define clean-file/version naming, package manifest, and supersession rules.
10. Decide whether MWM needs a structured metadata export beyond DOCX and companion sheets.
11. Define cross-family severity mapping and which findings block each stage.
12. Name the human signatory for each handoff and final release.

## 36. Research basis and limitations

The corpus is grounded in supplied MWM/AISL/APA/SEFI materials; NISO JATS/JATS4R; W3C WCAG/WAI; Wiley; Oxford University Press; Cambridge University Press; Royal Society of Chemistry; Routledge/Taylor & Francis; and Elsevier guidance.

The strongest shared finding is architectural: mature publishers treat the chapter as a package of linked content objects and metadata, not only a prose file. A readiness Skill therefore needs a component graph, explicit requiredness, evidence, owners, dependencies, and stage gates. The second shared finding is boundary discipline: a checklist can show that a field or record exists, but it cannot by itself establish substantive accuracy, accessibility conformance, legal permission, or scholarly integrity.

Several publisher sources were web-accessed but blocked or timed out for local automated capture. Their URLs and limitations are retained in the corpus manifest and access log. Before adopting any publisher-specific rule as MWM policy, a human should verify the current source and approve the local profile.
