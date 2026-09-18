# Modeling What Matters Editorial Skills
## Style-Guide Implementation — Operational Skill-Family Specification

**Specification ID:** `MWM-SGI-SPEC`  
**Version:** `0.1.0-draft`  
**Corpus ID:** `MWM-SGI-2026-08`  
**Status:** Draft for editorial review  
**Prepared:** August 13, 2026  
**Scope:** The MWM global style system, chapter profiles, and style-compliance review

## 1. Purpose

Style-Guide Implementation (SGI) converts the Modeling What Matters editorial profile into a versioned, inspectable system of rules that can be applied consistently across chapters while preserving author meaning, legitimate variation, and explicit exceptions.

SGI has two products:

1. a **rule registry** that stores the authoritative decision, scope, rationale, examples, exceptions, owner, and tests;
2. a **compliance engine/report** that applies the registry to a defined manuscript surface and produces evidence-backed findings.

Its governing invariant is:

> A style decision is enforceable only when its authority, scope, policy status, preferred treatment, exceptions, and evaluation behavior are explicit.

The Skill family is deliberately narrower than copyediting. It detects and reports style-system deviations; it does not rewrite a chapter wholesale in the name of consistency.

## 2. Scope and non-goals

### In scope

- decomposing MWM guidance into atomic rules;
- applying house style by component, document type, language profile, and editorial stage;
- maintaining preferred, cautionary, and prohibited terminology;
- distinguishing required rules from preferences and advice;
- managing chapter-specific exceptions and editorial decisions;
- detecting contradictions among MWM, APA, templates, and author conventions;
- producing a style-compliance report with evidence and disposition;
- versioning rules, change history, impact, and evaluation fixtures.

### Out of scope

- developmental editing or argument restructuring;
- full grammar, syntax, punctuation, or sentence-level copyediting;
- fact-checking or claim validation;
- technical-editing decisions about tables, figures, cross-references, or production files except to flag ownership;
- deciding whether the author’s conceptual terminology is substantively correct;
- importing external style-guide rules without an MWM adoption decision;
- changing an author’s voice merely to match an external clarity preference.

## 3. Trigger and editorial stage

| Trigger | Mode | Purpose |
|---|---|---|
| MWM guide or template revision | Rule-authoring | Atomize new guidance, create rule IDs, add examples, and assign owner/status. |
| Chapter intake | Baseline compliance | Establish current style state and identify scope/authority conflicts. |
| Copyedit preparation | Full compliance | Apply active rules across prose and components before sentence-level intervention. |
| Author revision | Incremental compliance | Recheck changed areas and dependent terminology/heading rules. |
| Production handoff | Release compliance | Confirm active required rules, approved exceptions, and unresolved findings. |
| Proof review | Targeted compliance | Detect style drift or introduced inconsistency after typesetting. |

The Editorial QA & Orchestration family decides which SGI mode runs and how it interacts with Copyediting and Technical Editing. SGI reports compliance; it does not determine publication on its own.

## 4. Inputs

### Required inputs

1. The current MWM global style guide or project profile.
2. The chapter or production file under review.
3. The active rule registry and version.
4. The exception and editorial decision register.
5. The target surface definition: chapter prose, headings, tables, captions, notes, front matter, references, or production template.
6. The stage profile: intake, copyedit preparation, production handoff, or proof.

### Optional inputs

- prior compliance report;
- chapter-specific author decisions;
- template and production profile;
- terminology list or glossary;
- APA/technical-editing rule packages;
- source documents used to justify a rule;
- approved examples from earlier chapters.

### Minimum run manifest

```yaml
run_id: "MWM-SGI-<chapter>-<date>-<sequence>"
manuscript_file: "absolute path or managed file identifier"
manuscript_version: "author or production version"
project_profile: "MWM-STYLE-v<version>"
rule_registry_version: "MWM-SGI-RULES-v<version>"
exception_register: "path or decision-log identifier"
stage: "intake | copyedit_prep | production | proof"
surfaces: ["body", "headings", "tables", "captions", "notes", "references"]
prior_run_id: "null or previous run"
```

## 5. Authority boundary

The corpus for this specification is stored in:

`Editorial Skills Research Corpus/02_Style_Guide_Implementation/`

The source manifest is `03_Crosswalk/corpus_manifest.json`; capsules are in `02_Extracted_Notes/source_capsules.md`.

| Tier | Authority | Use |
|---|---|---|
| 1 | MWM chapter guidance and approved MWM decisions | Controls MWM-specific style, component, language, and production requirements. |
| 2 | Active MWM global style and volume/chapter profile | Controls adopted house style. |
| 3 | Approved chapter exception | Controls only the defined scope and effective period; must be logged. |
| 4 | Delegated external rule authority, such as APA | Controls only the domain explicitly delegated by MWM. |
| 5 | Template/production profile | Controls layout or component behavior when assigned; conflicts with global style must be reported. |
| 6 | External implementation exemplars | Inform architecture and possible practices; do not directly control MWM output. |
| 7 | Author convention | Preserved when permitted and consistent; it is not a violation merely because an external guide prefers another form. |
| 8 | Model inference | Candidate explanation only; never an authority. |

The local corpus includes Google, Microsoft, GOV.UK, W3C, GPO, Wiley, and OECD systems. Their rule architectures are evidence; their individual spelling, terminology, capitalization, and tone choices are not MWM rules unless adopted.

## 6. Preconditions

SGI may claim a compliance result only when:

- the active rule registry version is identified;
- the project profile and target surface are known;
- the scope of any chapter exception is available;
- the file can be parsed with structure preserved;
- the review stage is defined;
- external rules are labeled as external rather than silently blended;
- prior unresolved findings are imported;
- the report can retain exact locations and rule IDs.

If the registry is incomplete or the target surface is unknown, SGI returns `not_ready` or `partial` and identifies what cannot be evaluated.

## 7. Family architecture

| Skill ID | Name | Primary question |
|---|---|---|
| `SGI-01` | Rule atomization | Can the guidance be expressed as one scoped, testable rule per decision? |
| `SGI-02` | House-style application | Which active rule applies to this text or component, and what treatment does it require? |
| `SGI-03` | Exception and decision management | Is the deviation approved, scoped, current, and documented? |
| `SGI-04` | Contradiction detection | Do MWM, APA, template, chapter, and author conventions conflict? |
| `SGI-05` | Terminology and word-list control | Are preferred, cautionary, and prohibited terms applied consistently and within scope? |
| `SGI-06` | Style-compliance reporting | Can a human editor reproduce, evaluate, and disposition each finding? |
| `SGI-07` | Rule maintenance and release | Did a rule change update its history, impact, examples, and tests? |

## 8. Operating principles

1. **Authority before action.** The system identifies the highest applicable authority before classifying a deviation.
2. **Scope before enforcement.** A rule applies only to its defined surface, document type, stage, audience, and language profile.
3. **Policy status before severity.** A preferred form is not a required violation.
4. **Consistency is relational.** A permitted alternative may be acceptable when used consistently within its scope.
5. **Preserve protected text.** Direct quotations, formal titles, proper names, cited terminology, and author-intended technical labels may be protected.
6. **Exceptions are records.** An exception is not a hidden override; it has an owner, scope, rationale, effective date, and review condition.
7. **External exemplars inform design.** They do not silently amend MWM.
8. **A rule needs a test.** If a rule cannot produce a clean example, violation example, boundary case, and exception test, it is not ready for automatic enforcement.
9. **Do not use style as a proxy for substance.** A style finding should not assert that an argument, term, or source is substantively wrong.
10. **Every change has an impact.** Rule updates must identify affected chapters, templates, terms, reports, and fixtures.

## 9. Rule registry

The registry is the source of truth. The long guide, compact guide, topic pages, compliance report, and change log are views or outputs derived from it.

### Required rule record

```yaml
rule_id: "SGI-HDG-001"
label: "Heading capitalization"
version: "1.0.0"
authority:
  tier: 1
  source_id: "S001"
  locator: "MWM guidance, heading requirements"
  adopted_by: "editorial decision-log ID"
policy_status: "required"
scope:
  document_types: ["chapter"]
  components: ["heading_level_1", "heading_level_2", "heading_level_3"]
  stages: ["intake", "copyedit_prep", "production", "proof"]
  language_profile: "MWM-US"
trigger: "A heading appears in an in-scope component."
preferred_action: "Apply the active MWM heading-capitalization rule while preserving proper nouns and protected titles."
protected_text: ["formal titles", "proper nouns", "direct quotations"]
exceptions: []
rationale: "Supports navigability and series consistency."
examples:
  compliant: ["Modeling what matters"]
  noncompliant: ["Modeling What Matters"]
  boundary: ["Modeling What Matters: The Research Handbook"]
decision_owner: "MWM editorial lead"
effective_from: "2026-08-13"
review_by: null
test_cases: ["SGI-E02", "SGI-E03"]
change_history: []
```

### Rule readiness states

| State | Meaning | Enforcement |
|---|---|---|
| `draft` | Proposed and under review | Do not enforce; may appear in research queue. |
| `pending` | Adopted in principle but not effective | Do not enforce until effective date or stage. |
| `active` | Enforceable within scope | Report violations according to policy status. |
| `exception` | Active deviation for a defined scope | Apply only within scope; verify decision record. |
| `deprecated` | Replaced but retained for history or migration | Detect only in an active migration. |
| `retired` | No longer applicable | Do not enforce. |

### Policy statuses

- `required`: must be followed;
- `preferred`: default choice when no exception applies;
- `permitted`: one of several accepted choices;
- `discouraged`: avoid unless justified;
- `informational`: explanation or context only.

`pending`, `deprecated`, and `retired` describe lifecycle; policy status describes the strength of an active rule.

## 10. Procedure

### Step 0 — Initialize the style profile

Load the MWM project profile, rule registry, template/production profile, exception register, prior findings, and target surfaces. Record the authority cascade and registry version in the run manifest.

### Step 1 — Atomize or validate the rule set

For every rule in scope, confirm:

- one observable decision;
- authority and locator;
- policy status;
- scope tags;
- preferred treatment;
- protected text and exceptions;
- examples and counterexamples;
- owner and effective date;
- evaluation fixture IDs.

If a guidance paragraph contains several independent decisions, split them into separate rules. If a rule contains only a vague aspiration such as “be consistent,” add a measurable predicate or keep it as rationale rather than an enforceable rule.

### Step 2 — Parse the manuscript by component

Extract with stable locators:

- body paragraphs;
- headings and levels;
- lists;
- tables, captions, and notes;
- figures and figure captions;
- footnotes/endnotes;
- quotations and protected text where detectable;
- references and citation components when routed from RCI;
- front matter, biographies, acknowledgments, and other required components.

The parser must retain raw text and formatting signals. If a surface cannot be inspected, report `coverage_partial` rather than `compliant`.

### Step 3 — Select the highest applicable rule

For each text or component unit:

1. identify document type, component, stage, language profile, and audience;
2. retrieve candidate rules by scope and trigger;
3. rank by authority tier, then active status, then specificity;
4. check approved exceptions;
5. protect quotations, formal titles, proper names, and other registered exceptions;
6. if multiple equal-level rules remain, emit a conflict finding.

### Step 4 — Detect deviations

Compare the observed unit to the rule’s predicate. The check may be deterministic, dictionary-based, structural, or model-assisted, but the report must state which method was used.

The system must distinguish:

- direct violation of a `required` rule;
- departure from a `preferred` rule;
- accepted `permitted` variation;
- use of a `discouraged` term;
- a missing or stale exception;
- a rule conflict;
- an unscoped author convention;
- insufficient evidence.

### Step 5 — Check consistency across the defined surface

Run relational checks for:

- terminology in body text, headings, tables, captions, and notes;
- capitalization of repeated headings or labels;
- acronym expansion and subsequent use;
- spelling profile across the chapter;
- punctuation and dash treatment where governed by active rules;
- named entities and protected titles;
- chapter-specific decisions applied consistently.

Consistency checks must respect scope. A term may be intentionally different in a quotation, a formal title, a cited source, or a technical label.

### Step 6 — Detect contradictions and missing decisions

Compare active rules and observed decisions across authorities. Report:

- MWM versus APA conflict;
- global guide versus template conflict;
- chapter exception without decision record;
- active rules with incompatible actions;
- pending rule applied as if active;
- deprecated term outside a migration scope;
- external rule incorrectly treated as MWM authority.

### Step 7 — Route the finding

Assign severity, confidence, action, owner, and status. Style findings remain in SGI unless they depend on a structural, production, citation, substantive, or factual decision owned by another family.

### Step 8 — Update maintenance artifacts

For rule-authoring or rule-change runs, update:

- rule record and version;
- rationale and source locator;
- affected exceptions;
- examples/counterexamples;
- evaluation fixtures;
- impact list;
- change log;
- compact operator view.

### Step 9 — Apply the release gate

Release-ready requires:

- all required rules in scope are active and testable;
- unresolved rule conflicts are escalated;
- chapter exceptions are recorded and scoped;
- no high-severity required-rule violations remain;
- terminology and cross-component consistency checks pass or have documented dispositions;
- rule and fixture versions are recorded;
- reports are reproducible from the run manifest.

## 11. Detection logic by Skill

### SGI-01 — Rule atomization

**Detect.** Identify guidance statements that contain multiple decisions, unclear actors, missing scope, or no observable predicate.

**Ready rule.** A rule is ready when a different editor can apply it to the same input and reach the same result, or can identify the precise point requiring human judgment.

**Intervention.** Do not enforce an unatomized rule. Route it to the rule-authoring queue.

### SGI-02 — House-style application

**Detect.** Retrieve the highest applicable rule for each observed component and compare its required/preferred treatment to the observed state.

**Intervention.** Auto-fix only reversible, deterministic changes that do not alter meaning or protected text. Suggest or flag ambiguous choices.

### SGI-03 — Exception and decision management

**Detect.** When observed text differs from the global rule, search for a matching exception by rule ID, scope, chapter, component, author, effective date, and status.

**Valid exception.** The decision identifies the deviation, scope, rationale, owner, effective period, and review or expiry condition.

**Invalid exception.** A verbal preference, an old report, or a one-off author choice with no scope or approval.

### SGI-04 — Contradiction detection

**Detect.** Compare active rules with the same scope or the same observed element. A contradiction exists when two rules require incompatible actions and neither has precedence.

**Intervention.** Block automatic application and create a decision request with alternatives and consequences.

### SGI-05 — Terminology and word-list control

**Detect.** Match terms in all in-scope surfaces and classify them as preferred, permitted, cautionary, discouraged, prohibited, unknown, or protected.

**Intervention.** Do not change terms inside direct quotations, formal titles, or source names. For unknown domain terms, request subject-matter review rather than inventing a replacement.

### SGI-06 — Style-compliance reporting

**Detect.** Validate that every finding has evidence, rule, status, severity, confidence, action, owner, and disposition.

**Intervention.** A report without a rule ID or locator is incomplete and cannot be a release artifact.

### SGI-07 — Rule maintenance and release

**Detect.** Compare rule, change log, fixtures, and affected document versions. Identify changes without tests, stale examples, or impact review.

**Intervention.** Block registry release until changed behavior is covered by fixtures and its impact is recorded.

## 12. Intervention thresholds

| Action | Allowed when | Examples | Not allowed when |
|---|---|---|---|
| `AUTO_FIX` | Rule is active, required, deterministic, scoped, reversible, and text is not protected | Normalize a known spelling or punctuation form under an explicit rule | It changes meaning, author voice, formal title, quotation, or unknown terminology |
| `SUGGEST` | Likely deviation from an active rule with low semantic risk | Apply preferred term; repair heading capitalization; expand first acronym | Multiple rules or exceptions are plausible |
| `FLAG` | Review is useful but the issue is not necessarily a violation | Advisory clarity concern; unknown term; incomplete coverage | A material authority conflict needs a decision |
| `ESCALATE` | Authority, scope, exception, or meaning is uncertain | MWM versus template; external rule conflict; author convention boundary | Never suppress to produce a clean report |
| `BLOCK` | An active required rule or registry release gate fails | Missing approved exception; contradictory active rules; required component style unresolved | Do not block on permitted variation or informational guidance |

Default SGI behavior is conservative. The engine should suggest a minimal correction and let Copyediting or the editor determine whether the prose needs a broader intervention.

## 13. Compliance output schema

### Run result

```yaml
run_id: "MWM-SGI-chapter-20260813-01"
specification_id: "MWM-SGI-SPEC"
specification_version: "0.1.0-draft"
project_profile: "MWM-STYLE-v0.1"
rule_registry_version: "MWM-SGI-RULES-v0.1"
stage: "copyedit_prep"
surfaces: ["body", "headings", "tables", "captions", "notes"]
preconditions: "pass | partial | fail"
coverage: "high | partial | low"
summary:
  units_reviewed: 0
  rules_applied: 0
  findings_total: 0
  required_violations: 0
  conflicts: 0
  exceptions_applied: 0
  escalations: 0
  blocking_findings: 0
release_status: "ready | ready_with_conditions | not_ready"
findings: []
maintenance_changes: []
```

### Rule record

```yaml
rule_id: "SGI-TERM-001"
version: "1.0.0"
label: "Preferred term"
authority_tier: 1
policy_status: "preferred"
scope:
  document_types: ["chapter"]
  components: ["body", "headings", "tables", "captions"]
  stages: ["copyedit_prep", "production", "proof"]
  language_profile: "MWM-US"
trigger: "Term appears in an in-scope unit outside protected text."
preferred_action: "Use the registered preferred term."
exceptions: []
protected_text: ["direct quotations", "formal titles", "source names"]
rationale: "Avoids ambiguity across chapters."
examples:
  compliant: []
  noncompliant: []
  boundary: []
source_evidence: []
decision_owner: "MWM editorial lead"
effective_from: "2026-08-13"
review_by: null
test_cases: []
change_history: []
```

### Compliance finding

```yaml
finding_id: "SGI-20260813-0001"
skill_id: "SGI-05"
rule_id: "SGI-TERM-001"
severity: "critical | high | medium | low | informational"
policy_status: "required | preferred | permitted | discouraged | informational"
status: "verified | needs_review | blocked | permitted | not_applicable | not_checked"
action: "AUTO_FIX | SUGGEST | FLAG | ESCALATE | BLOCK | CLOSE"
confidence: 0.91
location:
  file: "chapter.docx"
  locator: "body.p8.paragraph2"
  context_type: "body | heading | table | caption | note | quotation | reference"
observed_text: "..."
expected_treatment: "..."
authority:
  tier: 1
  source_id: "S001"
  locator: "MWM rule registry SGI-TERM-001"
exception_check:
  matching_exception: null
  protected_text: false
evidence:
  - type: "rule_record"
    locator: "SGI-TERM-001 v1.0.0"
reason: "Plain-language explanation."
proposed_change: "..."
owner: "copyeditor | MWM editorial lead | technical editor"
dependencies: []
human_decision: null
decision_log_id: null
```

## 14. Evidence requirements

Every material finding must preserve:

- exact file and structural locator;
- observed text or formatting state;
- active rule ID and version;
- authority and source locator;
- policy status;
- scope and exception result;
- expected treatment;
- evidence and detection method;
- severity, confidence, action, and status;
- owner and final disposition.

An editor should be able to answer: “What did the Skill see, which rule did it apply, why did that rule govern, what would change, and who decides if the case is ambiguous?”

## 15. Confidence and uncertainty

| Band | Range | Typical condition | Allowed action |
|---|---:|---|---|
| High | 0.95–1.00 | Exact dictionary/structure match under one active rule; no protected-text issue | Close or safe auto-fix |
| Strong | 0.80–0.94 | Clear rule match with a minor parsing or scope uncertainty | Suggest or routine review |
| Moderate | 0.60–0.79 | Rule likely applies but author convention, exception, or component boundary is uncertain | Flag; no automatic change |
| Low | <0.60 | Conflicting rules, unknown term, protected text, or incomplete parser coverage | Escalate |

Confidence must be reduced when:

- a rule is external rather than MWM-adopted;
- the registry is incomplete or stale;
- the text is part of a quotation, formal title, source name, or technical label;
- multiple rules at the same tier apply;
- the relevant exception is missing or expired;
- the unit is in a table, caption, note, or template surface with partial parsing;
- the suggested action would alter meaning or author voice.

## 16. Human-escalation rules

Escalate when:

1. two equal-level rules require incompatible treatments;
2. a template conflicts with the MWM guide on a material component decision;
3. a chapter-specific exception is used but not recorded;
4. a preferred term may be a substantive domain term rather than a style variant;
5. external guides disagree and MWM is silent;
6. a quotation, formal title, proper name, or source term would be altered;
7. an author convention is consistent but not clearly permitted or prohibited;
8. a rule is too broad to apply without human interpretation;
9. a rule change could affect other chapters, templates, or published material;
10. the requested edit belongs to Copyediting, Technical Editing, Scholarly/Editorial Integrity, or Production Readiness.

The escalation request must list the observed case, candidate rules, authority and scope, options, consequence, and decision owner.

## 17. Terminology register

The MWM terminology register should use records like:

```yaml
term_id: "TERM-001"
preferred_term: "learning model"
variants:
  - term: "model of learning"
    status: "permitted"
  - term: "learning framework"
    status: "discouraged"
definition: "MWM-approved meaning."
scope:
  document_types: ["chapter"]
  components: ["body", "headings", "tables", "captions"]
  audiences: ["all"]
protected_contexts: ["direct quotation", "formal title", "source terminology"]
rationale: "Avoids conflation with a different construct."
source_evidence: []
decision_owner: "subject-matter/editorial pair"
status: "active"
effective_from: "2026-08-13"
review_by: null
test_cases: ["SGI-E06", "SGI-E07", "SGI-E08", "SGI-E09"]
```

The register must distinguish “preferred” from “prohibited.” A term may be discouraged because it is ambiguous, not because it is always incorrect. The report should preserve that distinction.

## 18. Rule maintenance and change control

### Change record

```yaml
change_id: "SGI-CHANGE-20260813-001"
rule_ids: ["SGI-TERM-001"]
change_type: "new | clarification | correction | deprecation | scope_change"
old_behavior: "..."
new_behavior: "..."
rationale: "..."
authority: "decision-log ID"
effective_from: "2026-09-01"
affected_surfaces: ["body", "headings"]
affected_chapters: ["... or all"]
fixtures_added_or_changed: ["SGI-E07"]
owner: "..."
rollback_condition: "..."
```

### Change gate

No rule change becomes active until:

- the rule record is updated;
- the authority and rationale are recorded;
- examples and counterexamples are updated;
- affected exceptions are reviewed;
- fixtures pass;
- impact is assessed;
- the compact operator view and change log are updated.

## 19. QA and evaluation

The evaluation set is stored at:

`04_Evaluation_Set/evaluation_set.md`

Evaluation set ID: `MWM-SGI-EVAL-01`.

It includes clean controls, heading hierarchy, terminology, quotations, author conventions, language-profile conflicts, template conflicts, APA conflicts, advisory clarity, acronym scope, pending/deprecated rules, contradictory rule versions, report completeness, change impact, and cross-component consistency.

### QA gates

**Gate A — registry integrity**

- every active rule has an ID, version, authority, scope, status, action, exception logic, and test;
- no two active equal-level rules contradict without a conflict record;
- pending/deprecated rules are not silently enforced;
- the compact view links to full rule records.

**Gate B — parser and scope integrity**

- all defined surfaces are parsed or explicitly marked partial;
- protected text is recognized or flagged;
- document type, component, stage, and language profile are recorded.

**Gate C — compliance-report integrity**

- every finding has location, observed text, rule, authority, scope, policy status, evidence, severity, confidence, action, owner, and disposition;
- permitted variation is not reported as a violation;
- no advisory style rule creates an automatic rewrite without approval.

**Gate D — change/release integrity**

- changed rules have dated history and impact records;
- fixtures pass;
- unresolved conflicts are escalated;
- no required-rule violation remains without an approved disposition.

## 20. Examples and counterexamples

### Example 1 — exact, scoped rule

**Rule:** Use the MWM language profile for ordinary prose.  
**Observed:** One chapter uses a British spelling in body text, outside a quotation or formal title.  
**Action:** Report a scoped spelling finding if MWM has an active U.S.-English rule; do not claim that all British forms are universally wrong.

### Counterexample 1 — external rule imported silently

**Observed:** Google recommends a technical-documentation formatting convention.  
**Incorrect action:** Apply it to ordinary scholarly prose because Google’s guide is detailed.  
**Correct action:** Use it only as architecture evidence unless MWM adopts the specific rule.

### Example 2 — protected quotation

**Observed:** A direct quotation contains a term that MWM discourages in ordinary prose.  
**Action:** Preserve the quotation. If needed, flag an explanatory note or route to Scholarly/Editorial Integrity; do not silently rewrite the source.

### Counterexample 2 — terminology policing

**Observed:** An author uses a domain term consistently, but the term is absent from the MWM register.  
**Incorrect action:** Replace it with a model-inferred preferred synonym.  
**Correct action:** Escalate for subject-matter/editorial decision or leave unchanged.

### Example 3 — valid chapter exception

**Observed:** A chapter uses a different heading form under a recorded, scoped exception.  
**Action:** Mark as permitted and verify the exception’s scope and effective date.

### Counterexample 3 — exception by repetition

**Observed:** The same nondefault form appears repeatedly but has no decision record.  
**Incorrect action:** Treat repetition as approval.  
**Correct action:** Request a decision; consistency alone does not create authority.

### Example 4 — advisory clarity rule

**Observed:** A sentence is long but clear, grammatical, and technically precise.  
**Action:** Do not issue a blocking style violation solely because a general guide prefers shorter sentences.

### Counterexample 4 — style as developmental edit

**Observed:** A rule about short sentences is active.  
**Incorrect action:** Rewrite an entire paragraph and change its argumentative rhythm.  
**Correct action:** Flag a targeted concern or route sentence-level work to Copyediting.

### Example 5 — rule conflict

**Observed:** Global MWM profile says U.S. English; template says British English.  
**Action:** Emit a conflict finding naming both sources and route to the owner of the volume/template decision.

## 21. Failure modes and mitigations

| Failure mode | Consequence | Required mitigation |
|---|---|---|
| Static guide copied into prompt | Rules are hard to test, version, or scope | Use a versioned registry and generated views |
| Vague rule enforced as hard rule | Over-editing and false violations | Require measurable predicate and policy status |
| External rule imported silently | MWM authority is weakened | Maintain authority tier and source boundary |
| Template treated as global style | Component conflicts hidden | Separate global, volume, chapter, and production layers |
| Author variation treated as error | Voice and legitimate choices erased | Check policy status, consistency, and author-convention rules |
| Quotation or formal title changed | Source fidelity and attribution harmed | Protected-text detection and escalation |
| Unknown term replaced by model | Substantive meaning altered | Add term to review queue; do not invent |
| Exception not scoped | Local decision spreads to other chapters | Require scope, owner, effective date, and expiry/review |
| Rule change lacks fixture | Silent regressions | Change gate requires tests and impact review |
| Compliance report omits evidence | Human cannot reproduce finding | Require locator, observed text, rule, authority, and rationale |
| Style finding drifts into copyedit | Duplicate work and overreach | Route by ownership and stage |
| Parser misses captions/tables/notes | False compliance | Surface coverage gate |

## 22. Versioning

Use semantic versioning:

- **major** — authority hierarchy, output schema, policy model, or intervention authority changes;
- **minor** — new rule family, term register capability, or compatible source type;
- **patch** — wording, locator, example, or nonbehavioral correction.

Pin these assets in every run:

- specification version;
- MWM project/volume profile;
- rule registry version;
- exception register version;
- template/production profile version;
- evaluation-set version;
- parser/tool version;
- source capture date or snapshot.

Maintenance triggers include MWM guide revision, template change, APA delegation change, a human reversal, a production defect, a recurring author query, or an external source change that the project has adopted.

## 23. Release checklist

- [ ] Active MWM profile and rule registry versions are recorded.
- [ ] Every active rule has authority, scope, policy status, preferred action, exception logic, and tests.
- [ ] The target surfaces and editorial stage are known.
- [ ] Parser coverage includes all in-scope components.
- [ ] Required-rule violations are identified and dispositioned.
- [ ] Preferred/permitted/informational guidance is not misclassified as blocking.
- [ ] Protected quotations, formal titles, names, and source terminology are preserved.
- [ ] Chapter exceptions are approved, scoped, and current.
- [ ] MWM/APA/template/author conflicts are reported rather than blended.
- [ ] Terminology is consistent or intentionally scoped.
- [ ] Rule changes have change records, impact review, and fixtures.
- [ ] Compliance findings contain evidence, severity, confidence, action, owner, and status.
- [ ] No unresolved high-severity conflict remains.
- [ ] The result is handed to Editorial QA & Orchestration for stage-level release validation.

## 24. Open decisions for editorial adjudication

The research queue tracks:

- definitive MWM language profile by component;
- heading capitalization and formal-title exceptions;
- preferred dictionary and spelling authority;
- MWM terminology register and domain review process;
- permissible author-convention boundary;
- ownership split with Technical Editing;
- chapter-exception approval path;
- maintenance cadence and change-impact categories;
- treatment of quoted/cited terminology.

These questions are not silently answered by the external exemplars. They become enforceable only when recorded in the MWM decision log and added to the rule registry and evaluation set.

## 25. Research basis

The specification is grounded in:

- `03_Crosswalk/corpus_manifest.json`;
- `02_Extracted_Notes/source_capsules.md`;
- `03_Crosswalk/rule_architecture_crosswalk.md`;
- `03_Crosswalk/exemplar_comparison_and_gaps.md`;
- `03_Crosswalk/verification_queue.md`;
- `04_Evaluation_Set/evaluation_set.md`.

The corpus’s central synthesis is that a publishing-house style system is a controlled rule registry with layered views, not a static document. MWM authority must govern the final decisions; external systems supply architecture, maintenance, and testing patterns.

