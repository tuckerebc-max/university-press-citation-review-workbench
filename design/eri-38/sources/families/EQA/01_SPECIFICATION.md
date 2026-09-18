# Editorial QA & Orchestration Specification

**Specification ID:** `MWM-EQA-SPEC`  
**Version:** `0.1.0-draft`  
**Status:** Draft for editorial-owner review  
**Skill family:** Editorial QA & Orchestration  
**Research corpus:** `MWM-EQA-2026-08`  
**Scope:** Coordinating the seven bounded MWM editorial Skill families from intake through release and authorized post-publication handling

## 1. Purpose

Editorial QA & Orchestration is the control layer that decides what editorial work should run, in what order, with which authorities, using which model or tool route, and under what evidence and human-approval conditions. It turns the family specifications into a dependable publishing workflow.

The orchestrator does not replace the family Skills. It supplies their context, dependencies, routing, comparison, escalation, evaluation, provenance, and release controls. The family Skills remain responsible for their domain-specific judgments and reports.

The governing design is a **versioned dependency graph plus state machine**. A flat checklist or one giant prompt is insufficient because the editorial process contains conditional work, authority conflicts, independent checks, human decisions, version differences, and release-blocking states.

## 2. Non-negotiable boundary

The orchestrator may coordinate, compare, record, and route. It may not silently:

- perform developmental editing or substantive authorial rewriting;
- convert a model signal into a formal misconduct, authorship, legal, or ethical finding;
- let a model, tool, or aggregate score override an explicit MWM rule or authorized human decision;
- treat a missing input, unresolved query, or low-confidence high-risk issue as clearance;
- overwrite a comparison baseline, decision record, or released artifact;
- generalize an accessibility or file-integrity check beyond the tested format and scope; or
- release a chapter without an identified release authority and a retained decision receipt.

When the next action exceeds the current authority, the correct output is a typed escalation or hold, not improvisation.

## 3. Triggers

Run the orchestration family when any of the following occurs:

- a chapter or chapter package enters the project;
- an editorial stage is requested or completed;
- a source, rule, exception, template, model, tool, or specification changes;
- a family Skill reports a finding, disagreement, missing precondition, or escalation;
- a new proof, corrected proof, final output, or post-publication issue is received;
- a file, hash, format, metadata record, or embedded asset changes;
- an author, editor, production partner, or volume owner disputes a decision; or
- a release or correction decision is proposed.

## 4. Inputs

### 4.1 Required invocation envelope

Every run begins with a machine-readable and human-readable envelope containing:

| Field | Requirement |
|---|---|
| `run_id` | unique, immutable identifier |
| `chapter_id` | stable chapter or component identifier |
| `requested_stage` | intake, editorial review, production, proof, release, or post-publication |
| `purpose` | one sentence stating the decision or work outcome |
| `input_artifacts` | paths/IDs, file types, versions, and fixity where available |
| `authority_context` | applicable MWM rules, volume rules, exceptions, and source versions |
| `risk_profile` | consequence, sensitivity, uncertainty, irreversibility, and output exposure |
| `requested_outputs` | reports, ledgers, proposed changes, release decision, or escalation |
| `human_owner` | accountable editor or production owner; may be pending only at intake |
| `confidentiality_route` | approved local or external processing route |
| `orchestrator_version` | version of this specification and implementation |

### 4.2 Required contextual inputs

- the current chapter profile and stage;
- the applicable rule registry and exception ledger;
- the relevant family specifications and versions;
- prior findings, decisions, unresolved items, and accepted variations;
- the source bundle required by the requested Skills;
- target output formats and accessibility targets; and
- the release policy for the chapter or volume.

### 4.3 Protected inputs

The orchestrator must preserve the original author file, approved baseline, prior released output, proof package, source evidence, human decisions, and correction/status history. A new output is a derivation; it is never permission to replace the input record.

## 5. Outputs

### 5.1 Run result

Every run returns:

```text
run_id
stage
status
skills_run
skills_deferred
preconditions
findings
open_blocks
disagreements
human_decisions_required
coverage_statement
residual_risk
next_actions
receipt_id
```

### 5.2 Typed finding

Each finding must contain:

| Field | Requirement |
|---|---|
| `finding_id` | stable identifier within the run |
| `family` / `skill_id` | responsible domain and bounded Skill |
| `status` | signal, finding, approved variation, query, blocked, resolved, or other configured state |
| `location` | page, paragraph, heading, object, citation, file, or structured path |
| `observed` | exact excerpt, value, asset, or difference observed |
| `expected` | expected value or rule outcome, if known |
| `authority` | rule/source ID and effective version |
| `evidence` | source excerpt, file comparison, validator result, or human record |
| `severity` | low, moderate, high, or critical with rationale |
| `confidence` | calibrated categorical or numerical value plus basis |
| `intervention` | no change, recommend, propose, correct, hold, or escalate |
| `dependencies` | upstream finding or decision IDs |
| `owner` | person/role responsible for resolution |
| `state_history` | append-only status transitions |

### 5.3 Decision receipt

The receipt is the retained record of a material decision. It must link:

```text
receipt_id
entity_ids
activity_id
agent_ids
input_artifact_ids
rule_set_id / specification_version
model_tool_route
evidence_ids
decision
decision_owner
timestamp
supersedes / superseded_by
output_artifact_ids
fixity_values
residual_risk
retention_class
```

The design adapts W3C PROV and PREMIS concepts. It does not claim that MWM implements those standards in full.

### 5.4 Release package

A release package contains the approved output, release checklist, unresolved-item disposition, provenance/fixity receipt, version/status record, accessibility coverage statement, and named authorization. A package with a critical block is not a release package; it is a hold package.

## 6. Authoritative sources

The source hierarchy for orchestration is:

1. explicit current MWM editorial-owner decision;
2. approved MWM volume or chapter rule;
3. approved, in-scope exception or author convention;
4. current family specification and its rule/authority ledger;
5. supplied MWM template, guidance, or style source where the local decision has not superseded it;
6. adopted external standard or publisher requirement, if MWM has explicitly designated it as applicable;
7. external research exemplar used as provisional context; and
8. model general knowledge or stylistic preference, which may suggest but may not govern.

The exact MWM precedence order among the first six levels remains an owner decision. Until approved, the orchestrator must report a conflict rather than infer precedence.

## 7. Preconditions

The orchestrator must check before routing:

- stage and purpose are declared;
- input artifacts are identifiable and readable;
- required source bundle is present or its absence is recorded;
- authority and rule versions are known or explicitly provisional;
- the responsible human owner is known for decisions that may block release;
- confidentiality route is approved for each tool/model;
- the selected family Skill is in scope for the stage;
- upstream dependencies are complete, current, or explicitly waived;
- output formats and accessibility targets are declared; and
- a baseline exists for any difference or proof review.

Failure of a precondition produces `blocked`, `deferred`, `source_unavailable`, or `human_decision_required`, not a false green result.

## 8. State and status vocabulary

### 8.1 Run states

`intake` → `planned` → `running` → `awaiting_human` / `awaiting_input` / `awaiting_reproof` → `ready_with_tracked_items` / `hold` / `released` / `post_publication_case`.

Any state may become `blocked` when a required authority, input, owner, or integrity condition is absent. A blocked state may be reopened only by a new receipt that identifies what changed.

### 8.2 Finding states

`signal`, `finding`, `approved_variation`, `typesetter_error`, `factual_or_meaning_error`, `author_alteration`, `query_open`, `source_unavailable`, `asset_issue`, `accessibility_signal`, `status_issue`, `proposed_change`, `resolved`, `rejected`, `deferred`, `blocked`.

These statuses are not interchangeable. In particular, `signal` is not `finding`, `approved_variation` is not `error`, and `status_issue` is not ordinary copyediting.

### 8.3 Release decisions

`ready`, `ready_with_tracked_items`, `hold`, `blocked`, and `post_publication_case`. `ready_with_tracked_items` is permitted only when the release policy defines the allowed residual risk and an authorized owner accepts it in a receipt.

## 9. Operating principles

1. **Baseline before judgment:** differences cannot be judged without an identified comparison object.
2. **Context before routing:** stage, authority, risk, and format determine which Skill runs.
3. **Difference is not defect:** a change may be intentional, approved, or required.
4. **Evidence before confidence:** confidence cannot compensate for missing evidence.
5. **Minimum necessary intervention:** the smallest authorized action is preferred.
6. **Independent review where risk warrants:** disagreement is data, not noise.
7. **Human authority remains visible:** an override resolves a question; it does not erase the question.
8. **No silent state changes:** every material status transition is recorded.
9. **No aggregate-score release:** one critical block cannot be averaged away.
10. **Continuous improvement:** reviewed failures update rules, routes, fixtures, or training rather than disappearing into ad hoc notes.

## 10. Skill map

| Skill ID | Bounded Skill | Primary output | Typical stage |
|---|---|---|---|
| EQA-01 | Intake and Stage Classification | chapter profile, stage, missing inputs, initial risk | intake |
| EQA-02 | Authority and Rule Resolution | applicable rule set, precedence, exception scope, conflicts | intake and before each Skill |
| EQA-03 | Dependency Planning | run graph, preconditions, gates, deferred work | planning |
| EQA-04 | Model and Tool Routing | route decision, approved capability, confidentiality check | planning and execution |
| EQA-05 | Independent Review Comparison | issue clusters, agreement/disagreement, adjudication queue | after parallel reviews |
| EQA-06 | Confidence and Uncertainty Aggregation | calibrated confidence, evidence completeness, residual risk | during and after review |
| EQA-07 | Human Escalation and Decision Receipt | decision packet, owner decision, receipt, residual-risk disposition | any stage |
| EQA-08 | Evaluation and Regression | fixture results, coverage, drift report, release recommendation | before route/spec release |
| EQA-09 | Editorial Decision Log and Provenance | append-only lineage, artifact identities, fixity, status history | every material event |
| EQA-10 | Release Orchestrator | release checklist, package, hold, or post-publication case | release and after release |

## 11. Family interface map

| Family | Required orchestration input | Output consumed downstream |
|---|---|---|
| Reference & Citation Integrity | chapter text, references, applicable APA/house rules, source-verification permissions | citation/reference ledger, orphan/missing findings, metadata queue, status |
| Style-Guide Implementation | chapter profile, rule registry, exceptions, text/layout inventory | rule application ledger, conflicts, exceptions, compliance report |
| Technical Editing | structured inventory, template, figures/tables/cross-references, technical rules | hierarchy/object/cross-reference/numbering findings |
| Copyediting | approved style context, text, author conventions, intervention threshold | copyedit log, proposed changes, unresolved questions |
| Scholarly/Editorial Integrity | claims, citations, available sources, integrity protocol | signals/findings, source-fit questions, escalation cases |
| Chapter Completeness & Production Readiness | required-component matrix, chapter profile, upstream statuses | completeness gate, missing components, production-readiness status |
| Proof & Post-Typesetting Review | fixed baseline, proof/final outputs, correction log, format targets | proof findings, reproof status, fixity/version record, release recommendation |

The orchestrator may parallelize family runs only when their input dependencies are satisfied and the expected interaction is preserved. It must not use parallelism to conceal a conflict.

## 12. Candidate dependency graph

```text
EQA-01 intake/stage
        |
        v
EQA-02 authority/rules ---- EQA-06 risk profile
        |
        v
EQA-03 dependency plan ---- EQA-04 route approval
        |
        +--> RCI  SGI  TE  CE  SEI  (parallel where eligible)
                              |
                              v
                  CPR completeness / readiness gate
                              |
                              v
                    typeset baseline and proof package
                              |
                              v
                              PPR
                              |
                              v
                 EQA-05 comparison / EQA-07 adjudication
                              |
                              v
              EQA-08 evaluation / EQA-09 provenance
                              |
                              v
                      EQA-10 release gate
```

This is a proposed default. MWM owners may require stricter serialization for specific chapter types, but any change must be recorded as a versioned dependency rule.

## 13. Procedure

1. Create or update the invocation envelope.
2. Identify stage, purpose, chapter profile, owner, output formats, and confidentiality route.
3. Resolve applicable authorities and exceptions; stop on material conflict.
4. Build the dependency graph and identify required upstream artifacts.
5. Assign a risk and sensitivity profile.
6. Select deterministic checks, specialist model routes, independent review, and human review as configured.
7. Run eligible family Skills with their own specifications and versions.
8. Normalize and compare typed outputs without erasing family boundaries.
9. Aggregate confidence, evidence completeness, disagreement, residual risk, and open blocks.
10. Route human decisions with a bounded evidence packet and explicit options.
11. Re-run affected downstream checks after material changes.
12. Create provenance/fixity records for material outputs and decisions.
13. Run regression and release validation.
14. Release, hold, defer, or open a post-publication case under the configured policy.
15. Feed reviewed failures, appeals, and changes into the improvement log.

## 14. EQA-01 — Intake and Stage Classification

### Purpose and detection logic

Classify the chapter package, determine the editorial stage, identify the requested outcome, and expose missing or incompatible inputs. The classifier must distinguish manuscript intake, editorial review, production preparation, proof, release, and post-publication cases.

It may infer a candidate stage from file names, metadata, or user request, but it must label the result as provisional until an authorized owner confirms it when the stage affects release or post-publication status.

### Output

`chapter_profile`, `candidate_stage`, `purpose`, `input_inventory`, `missing_inputs`, `risk_profile`, `owner`, `confidence`, `confirmation_required`.

### Escalation

Escalate when multiple stages are plausible, the source package is incomplete, a post-publication issue is mixed with ordinary editing, or no release owner is named.

## 15. EQA-02 — Authority and Rule Resolution

### Procedure

1. Load the applicable MWM rule registry.
2. Identify volume, chapter, stage, output-format, and author-convention scope.
3. Load family-specific authority and exception ledgers.
4. Check effective dates and supersession.
5. Detect contradiction or missing precedence.
6. Return a rule bundle with source IDs, scope, version, rationale, and unresolved conflicts.

### Intervention threshold

No material rule conflict may be resolved by model preference, source order, or majority vote. If a conflict changes a proposed edit, release status, author obligation, or record status, the run is `awaiting_human`.

## 16. EQA-03 — Dependency Planning

The planner converts the stage and rule bundle into a graph of eligible Skills. Each node has preconditions, input IDs, expected output types, failure states, and downstream consumers. A node is complete only when its output schema, evidence, coverage statement, and status are present.

The planner must detect stale outputs. A family result produced under a different rule, baseline, source bundle, model route, or specification version is not silently reused.

## 17. EQA-04 — Model and Tool Routing

### Routing classes

| Route | Use when | Required control |
|---|---|---|
| deterministic validator/parser | file identity, schema, counts, links, hashes, structured presence | tool version and retained result |
| specialist language model | bounded grammar, style, clarity, or semantic comparison | family prompt/spec, evidence, model version, confidence |
| independent second model or reviewer | high-risk, high-uncertainty, or disagreement-sensitive task | independent context and comparison key |
| retrieval/verification tool | metadata, source, URL, or citation verification | source access log and evidence excerpt |
| human editor/owner | authority conflict, substantive change, integrity signal, critical release decision | decision packet and receipt |

The router must refuse an unapproved model/tool route, an unsafe confidentiality route, or a route that cannot retain the evidence needed for the decision.

## 18. EQA-05 — Independent Review Comparison

Independent results are compared by stable issue key: family, location, observed object, and issue class. The comparator should classify:

- agreement on the same observed issue and expected action;
- partial agreement with different severity or intervention;
- distinct issues at the same location;
- one-sided signal requiring verification; and
- true contradiction requiring adjudication.

The comparator must preserve both source reports. It may consolidate duplicate presentation for the editor, but it may not delete disagreement evidence.

## 19. EQA-06 — Confidence and Uncertainty Aggregation

Confidence is a property of a finding or decision, not a substitute for authority. The aggregator considers:

- evidence completeness and directness;
- source quality and access status;
- agreement among independent checks;
- rule clarity and exception scope;
- input quality and format limitations;
- consequence and reversibility; and
- model/tool stability and known error patterns.

The output must include a confidence basis and uncertainty reason. MWM should calibrate numerical thresholds through the evaluation set; until then, use categorical `high`, `moderate`, `low`, and `unknown` states with conservative escalation for high-risk objects.

## 20. EQA-07 — Human Escalation and Decision Receipt

### Mandatory human review

Human review is required for:

- authority or precedence conflicts;
- substantive authorial or developmental changes;
- scholarly/editorial integrity signals;
- possible legal, permissions, privacy, or ethical consequences;
- high-risk disagreements about names, numbers, symbols, claims, sources, or status;
- unresolved proof queries or missing reproof;
- critical completeness, file-integrity, or accessibility blocks;
- post-publication correction, removal, retraction, or expression-of-concern states; and
- final release authorization.

### Decision packet

The packet contains the question, options, relevant excerpt or asset, applicable rule, competing findings, evidence, risk, proposed next action, deadline, and what the decision will authorize. The owner’s response is appended to the receipt; it does not overwrite the evidence.

## 21. EQA-08 — Evaluation and Regression

Run the evaluation set when:

- this specification changes;
- a family interface changes;
- a rule or exception is added or retired;
- a model, prompt, retrieval method, parser, or file tool changes;
- an output format or release policy changes; or
- a material production failure or appeal occurs.

The regression record includes fixture version, expected behavior, actual behavior, error class, severity, reviewer, disposition, and release decision. A passing aggregate score does not override any critical fixture failure.

## 22. EQA-09 — Editorial Decision Log and Provenance

The log is append-only for material events. It records input identity, activity, agent, rule/specification version, evidence, output, status transition, decision owner, time, and fixity. Supersession is explicit; deletion is not a substitute for correction.

The log should support five questions:

1. What artifact or issue was acted upon?
2. What activity or Skill ran?
3. Which person, model, tool, or organization acted?
4. What authority and evidence were used?
5. What output, decision, status, and residual risk resulted?

## 23. EQA-10 — Release Orchestrator

The release orchestrator reconciles the seven family statuses, open items, proof state, output-format checks, provenance/fixity, and human authorization. It must distinguish:

- `ready`: no blocking item and release authorized;
- `ready_with_tracked_items`: only policy-permitted residual items with owner acceptance;
- `hold`: work can continue after a specified action;
- `blocked`: required authority, input, evidence, or integrity condition is absent; and
- `post_publication_case`: an issue concerns a released record and requires a separate authorized workflow.

## 24. Intervention thresholds

| Condition | Default action |
|---|---|
| deterministic structural or fixity failure | block affected gate |
| missing required input or baseline | await input; do not infer |
| clear low-risk issue with direct evidence and in-scope authority | recommend or apply only if family policy permits |
| low-confidence issue affecting ordinary prose | recommend or cluster for editor review |
| low-confidence issue affecting name, number, symbol, URL, citation, claim, or asset | independent check or human review |
| model disagreement on material issue | adjudication queue |
| unresolved rule conflict | human authority decision |
| substantive author alteration | author/editor decision and protected before-state |
| open proof query or missing reproof | hold proof/release gate |
| possible integrity, legal, privacy, or status issue | dedicated human escalation |
| critical release block | hold regardless of aggregate score |

These defaults are provisional until MWM owners calibrate them against real chapter data.

## 25. Evidence requirements

### Required evidence

Every material finding or decision must include:

- exact location or structured path;
- observed text, value, asset, or difference;
- expected outcome or applicable rule;
- source/rule/specification identifier and version;
- comparison baseline or retrieval evidence where relevant;
- model/tool output and version when used;
- human rationale when a person resolves or overrides; and
- affected output and state transition.

### Coverage statement

Every family result must state what was checked, what was unavailable, which formats were tested, what was excluded, and what the result does not establish. “No issues found” without a coverage statement is an incomplete result.

## 26. Rule hierarchy and exception handling

The rule registry stores:

```text
rule_id
rule_text
source_id
authority_level
scope
effective_from / effective_to
supersedes
exceptions
conflicts
owner
review_date
```

An exception stores:

```text
exception_id
affected_rule
scope
rationale
approver
approval_date
expiry_or_review_date
affected_chapters_or_outputs
```

An exception is not a new universal rule. The orchestrator must test scope before applying it.

## 27. Security, privacy, and confidentiality

The orchestrator must:

- classify manuscript and source-bundle sensitivity before routing;
- use only approved local or external processing routes;
- minimize excerpts in reports and decision packets;
- prevent prompt or source injection from changing authority or route;
- preserve access controls for author, editor, and production materials;
- record any route denial or suspected disclosure as a human escalation; and
- avoid retaining unnecessary personal data in evidence displays.

Security checks are part of editorial QA; they do not authorize the orchestrator to investigate beyond the user’s project scope.

## 28. Model and tool change control

A route change includes any change to model version, system instruction, family prompt, retrieval source, parser, validator, tool version, context window, output schema, or temperature/decoding behavior that may affect results. Such a change requires:

1. versioned change record;
2. impact assessment;
3. evaluation-set regression;
4. review of new failure modes;
5. approval for production use; and
6. a new receipt for the first production run.

## 29. QA tests

### Automated checks

- envelope schema validation;
- required-input and dependency validation;
- rule/version/exception resolution;
- finding-schema completeness;
- evidence-link integrity;
- duplicate and stable issue-key checks;
- status-transition validity;
- output-format, link, count, and file-open checks;
- baseline/output fixity comparison;
- receipt completeness and append-only history; and
- regression-fixture execution.

### Human QA

- inspect material disagreement clusters;
- review high-risk and low-evidence findings;
- sample false negatives and false positives;
- verify scope and author-voice preservation;
- confirm accessibility coverage claims;
- inspect release package and authorization; and
- review unresolved verification-queue decisions.

### Minimum QA rule

No automated pass can close a mandatory human gate. No human approval can make an absent baseline, missing evidence, or corrupted output disappear; it must record the accepted residual risk or authorize a new controlled action.

## 30. Failure modes and controls

| Failure mode | Control |
|---|---|
| mega-prompt drift | bounded family contracts and typed routing |
| latest-model authority | rule registry and owner-controlled versioning |
| unsupported confidence | evidence and coverage requirements |
| aggregate-score masking | critical-block override |
| hidden dependency | explicit graph and stale-output checks |
| issue deduplication erases disagreement | preserve source reports and comparison states |
| author rewrite passes as copyedit | intervention threshold and human escalation |
| signal becomes misconduct finding | SEI boundary and dedicated human process |
| proof difference becomes automatic correction | baseline, approved-variation, and reproof states |
| accessibility overclaim | format-specific coverage statement |
| silent exception expansion | scoped exception ledger |
| untraceable tool result | retained evidence and receipt |
| model or rule drift | versioning and regression |
| privacy leakage | route approval and minimization |
| release without authority | mandatory release owner and receipt |

## 31. Positive examples

### Example 1 — Parallel family review

The chapter has an approved profile, stable rule bundle, editable source, and complete reference list. RCI, SGI, TE, CE, and SEI run in parallel. The comparator clusters a shared heading issue, preserves each family’s rationale, routes an RCI/SEI citation-fit disagreement to review, and passes the package to CPR only after all required outputs are complete.

### Example 2 — High-risk disagreement

Two reviewers disagree about whether a reported percentage is 13.6 or 16.3. The orchestrator marks the issue high risk, retains both excerpts, requests the cited source or author confirmation, and blocks release of the affected claim until resolved.

### Example 3 — Approved variation

The author convention ledger approves American spelling for one chapter in a volume that otherwise uses British spelling. The router scopes the exception, SGI checks it, and CE does not normalize it. The receipt points to the exception and its scope.

### Example 4 — Proof closure

PPR records a missing figure label, production incorporates the correction, and the corrected proof is compared against the prior proof. The issue becomes `resolved` only after the reproof confirms label, caption, cross-reference, and asset identity.

### Example 5 — Post-publication issue

A factual error is reported after release. EQA-10 opens `post_publication_case`, preserves the released artifact, routes the evidence to the designated owner, and records the authorized correction/version/status decision separately from ordinary copyediting.

## 32. Counterexamples

### Counterexample 1 — Majority vote

Three models prefer a stylistic change and one local rule forbids it. The orchestrator must follow the authority hierarchy and surface the conflict; it must not use model majority as policy.

### Counterexample 2 — No issues found

A model says “no issues found” after seeing only a low-resolution PDF. The output is incomplete because it lacks a coverage statement and cannot establish source-text, accessibility, or asset integrity.

### Counterexample 3 — Silent author rewrite

The copyedit route changes a paragraph’s claim to make it more persuasive. This is outside copyediting authority and requires a protected before-state plus author/editor decision.

### Counterexample 4 — Aggregate readiness

Six family checks are green but a critical proof query is open. The release result is `hold` or `blocked`, not `ready`.

### Counterexample 5 — Web source override

An external publisher page suggests a rule that conflicts with an explicit MWM decision. The page may inform a review but cannot override local authority.

## 33. Acceptance criteria

The specification is operationally acceptable when:

- all 50 `MWM-EQA-EVAL-2026-08` fixtures have expected outcomes and run receipts;
- EQA-11, EQA-17, EQA-19, EQA-25, EQA-27, EQA-36, EQA-43, EQA-46, and EQA-50 pass without release-blocking behavior;
- every family interface has an owner, version, input contract, output contract, and dependency status;
- rule conflicts and exceptions are visible and scoped;
- independent-review disagreement is preserved and routed;
- human overrides have rationale and residual-risk records;
- all material outputs have provenance and fixity identifiers;
- accessibility checks state format and scope;
- post-publication matters cannot bypass their separate case state; and
- a release package cannot be created without the configured release authority.

## 34. Evaluation metrics

MWM should track at least:

- precondition-detection recall;
- unsupported-finding rate;
- false-clearance rate;
- high-risk disagreement escalation rate;
- duplicate-cluster precision;
- human-escalation appropriateness;
- release-block detection rate;
- evidence-link completeness;
- receipt/fixity completeness;
- regression pass rate by fixture class; and
- editor time to adjudicate and close material issues.

Metrics are diagnostic. They must not be collapsed into one score that can override a critical failure or ethical boundary.

## 35. Human-escalation rules

Escalate rather than guess when:

- the authority hierarchy is unresolved;
- the requested action changes meaning, argument, authorship, or scholarly status;
- evidence is missing, inaccessible, contradictory, or likely fabricated;
- the decision affects names, numbers, symbols, citations, permissions, privacy, or public record;
- a model/tool route is unapproved or unable to preserve evidence;
- the output format or baseline is not what the check assumes;
- the author or editor disputes a material intervention; or
- the proposed release depends on accepting residual risk not already covered by policy.

The escalation must ask one bounded question and identify the smallest decision needed to proceed.

## 36. Versioning and governance

Version separately:

- this orchestration specification;
- each family specification;
- the rule registry and exception ledger;
- the dependency graph and release policy;
- model/tool routes;
- the evaluation set; and
- the output and receipt schemas.

Any change affecting a decision, route, authority, or release gate requires impact analysis and regression. The decision log must identify which version produced each material output.

The editorial owner governs local policy. The orchestration owner maintains the graph, schemas, routes, and regression process. Family owners maintain domain rules and examples. Production owners govern format and proof requirements. A release authority signs the final package.

## 37. Release checklist

Before returning `ready`:

- [ ] chapter identity, stage, owner, and purpose are recorded;
- [ ] source and rule bundle versions are known;
- [ ] exceptions are scoped and approved;
- [ ] required family outputs are present and current;
- [ ] all blocking findings, queries, and dependencies are closed or explicitly accepted under policy;
- [ ] independent disagreements have been adjudicated or routed;
- [ ] high-risk names, numbers, symbols, citations, claims, assets, and cross-references have evidence;
- [ ] CPR completeness/readiness status is acceptable;
- [ ] PPR baseline, corrections, reproof, and output-format checks are complete where applicable;
- [ ] accessibility coverage is stated for every required format;
- [ ] released files pass openability, metadata, embedded-asset, and fixity checks;
- [ ] post-publication status is not being used for an ordinary pre-publication change;
- [ ] provenance/decision receipt is complete;
- [ ] residual risk is stated; and
- [ ] authorized release owner has approved the package.

## 38. Open MWM decisions

1. Approve the canonical editorial stage model and dependency graph.
2. Approve the authority-precedence table.
3. Name the volume, chapter, family, production, QA, and release owners.
4. Define approved local/external model and tool routes.
5. Define manuscript confidentiality, retention, and access rules.
6. Calibrate confidence, disagreement, severity, and residual-risk thresholds.
7. Define which findings require independent review.
8. Define required output formats and accessibility targets.
9. Define blocking versus conditionally acceptable release states.
10. Approve proof correction, reproof, and post-publication status policies.
11. Approve fixity, provenance, and retention implementation.
12. Approve the evaluation-set cadence and regression release rule.
13. Define editor-facing and author-facing report formats.
14. Decide how appeals and accepted exceptions feed continuous improvement.

## 39. Research basis and limitations

This specification is grounded in the supplied MWM/AISL/SEFI/APA materials; the seven completed MWM family specifications; NIST AI RMF 1.0, its Generative AI Profile, Playbook, and Resource Center; ISO process and quality-management guidance; COPE Core Practices and editorial-office toolkit; W3C PROV; PREMIS; Crossref and NISO record/versioning guidance; JATS; WCAG/WAI; and publisher proofing/correction workflows.

The corpus supports the architecture of bounded processes, risk-based routing, evidence, human accountability, evaluation, provenance, and release control. It does not determine MWM’s final owners, thresholds, model inventory, confidentiality policy, output matrix, or local rule precedence. Those remain explicit decisions for the editorial owners. ISO and COPE sources were reviewed as official web-only sources because local capture was blocked; their use in this draft is provisional until confirmed locally.

