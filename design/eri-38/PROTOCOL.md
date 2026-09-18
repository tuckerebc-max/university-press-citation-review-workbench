# Proposed protocol and implementation obligations

Status: design candidate. `upw` is a proposed CLI; this packet does not install or implement it. `tools/validate_design.py` validates this design's schemas and specimens only.

## Interface

Every verb takes one UTF-8 JSON request from an explicit private file. It emits exactly one JSON object plus newline to stdout. Redacted diagnostics go to stderr. Unknown fields, duplicate JSON keys, non-finite numbers and malformed requests are rejected before side effects. Output and evidence locators must not disclose manuscript text, author metadata or credentials to logs.

| Verb | Request | Reply | Effect |
|---|---|---|---|
| `declare` | Empty object | Contract/map IDs, digests, capabilities, maturity | Read only |
| `plan` | Batch request | Candidate plan, missing inputs/capabilities and blocked nodes | No model call; private immutable draft file only |
| `seal` | Plan ref/digest plus verified approval-receipt ref | Seal ref/digest and authority check | Human route; never changes plan bytes |
| `review` | Sealed-plan ref and requested resumable scope | Task refs, wait states, failures and receipt | Calls capacity interface only for eligible machine nodes |
| `reconcile` | Sealed plan plus immutable result/event refs | Release recommendation, coverage and docket | Deterministic gate evaluation; no publication |
| `record-decision` | External human receipt ref and expected object digest | Verified receipt reference | Human-only authority verification and append |
| `inspect` | Run ref | Current evidence-derived state and expected next action | Read only |
| `conform` | Candidate family/adapter plus conformance suite ref | Per-case evidence, statuses, admission/release implications | Synthetic contract probes; no real manuscript |

All replies use `{schema, verb, request_id, outcome, result, errors, unknowns, receipt_ref}`. `schema` is `university_press.reply.draft1`; `outcome` is `ok`, `technical_failure` or `refused`. `result` is the typed verb output or null; `errors` contains `{code, rule_id, object_ref, retryable}`. A refusal includes no partial dispatch. An approved operation may return an editorial `hold` with exit 0; exit codes describe the operation, not scholarly quality.

Exit 1 is a technical failure with no successful clearance; exit 2 is invalid input, authority denial, prohibited effect or critical admission refusal. Examples: `INVALID_REQUEST`, `SOURCE_DRIFT`, `LOCK_DRIFT`, `PLAN_DRIFT`, `HUMAN_ROUTE_REQUIRED`, `RECEIPT_UNVERIFIED`, `RESTRICTED_INPUT`, `ROUTE_DENIED`, `DAG_CYCLE`, `BATCH_LIMIT`, `WINDOWS_PATH_LIMIT`. Awaiting inputs and unresolved policies are explicit editorial states. `CE_REQUIRED_ABSENT` and `FAMILY_CRITICAL_SET_UNDECLARED` can be reported in a successful diagnostic reconciliation while holding the affected clearance.

## Freeze and replay

Canonical JSON: UTF-8, keys sorted, compact separators, no NaN/infinity, duplicate keys prohibited. Arrays remain ordered; schemas prohibit floating-point fields in content-addressed control records. Strings retain supplied Unicode without normalization. Hash-control payloads must use integer numbers only. File fixity hashes raw bytes. A record ID is SHA-256 of its canonical payload excluding its own ID. No volatile timestamp is regenerated when an existing record is replayed.

The execution form separates `plan` (immutable payload) and `seal` (approval evidence). The plan schema intentionally permits only `execution_authorized:false`: a payload cannot authorize itself. Its mode is `design_simulation` or `diagnostic_review`. A live wrapper must require diagnostic mode, verified plan/seal digests, Dock lineage, authorization receipts and expiry; simulation payloads can never dispatch. It must validate the same plan schema and independently verify every authorization prerequisite. Do not make a second approval-bearing plan format that bypasses the seal.

A plan digest binds the normalized profile **and control spine**, the canonical map, full source manifest/bundle, rules and adopted exception set, native specifications, whole skills lock, approved surface/account route, model/tool/parser versions, applicable authority context, output targets and proof lineage. A route binding uses approved route metadata, never credentials. Do not allow null, synthetic or unverified pins in live execution.

Every binding has a state: known, unknown or not_applicable. Known requires its digest; unknown and not_applicable carry null rather than an invented hash. A scoped required unknown blocks the node. Only the adopted stage profile can establish not_applicable; the caller cannot declare away a required baseline. The citation-only specimen therefore has null baseline/proof bindings marked not_applicable. Its manifest digest binds the included synthetic manifest; no specimen hash is represented as a real manuscript capture.

Before extraction and each model call, reopen safely, reject path substitution/symlink/reparse tricks, hash the exact bytes consumed, and retain the source snapshot reference. Recheck every source before assembly. A chapter mismatch blocks that chapter and every dependent volume gate; completed unrelated chapter evidence may remain valid. Plan/lock/map/authority tampering blocks the run globally.

Each node has `scope` (`chapter`, `volume`, `batch`). Expansion is deterministic from the approved manifest and profile. A logical task key is SHA-256 of `{plan_id,node_id,scope,scope_ids}`; each retry has a separate attempt ID and lease/fencing token. Duplicate successful results are idempotent only if their content digests agree. Conflicting duplicates remain an explicit discrepancy. A transient capacity error may retry within the approved budget; a denied route, changed baseline or revoked authority may not.

Results carry all expected bindings plus native payload digest, producing worker/surface/attempt, source scope, coverage, limitations and captures. The consumer compares these against the plan, not against the result's own claims. Changes invalidate the transitive consumers and their rollups. Reuse requires equality of all relevant bindings and still-valid authority; a matching chapter hash alone is insufficient.

A successor plan has a different global digest even when some chapters are unchanged. Do not edit old results to make their `plan_id` match. It carries its `parent_plan_id`, proof-cycle number and proposed `reuse_descriptors`: prior result/digest and old plan ID, unchanged scope/dependency digest, and evidence that every rule, specification, route, authority, baseline, format and direct input relevant to that scope is unchanged. After the plan is frozen, the trusted verifier issues an attestation binding those descriptors to the new plan digest; the human seal covers that attestation. Keeping the target plan ID out of the descriptors avoids a self-referential hash. Without a verified attestation, results from another plan are stale. Volume-level consumers always use the new rollup.

## Profile and adapter normalization

Normalize `contract_id` and `contract_set_id` as source identifiers, not as competing contract schemas. Normalize `from/to/family`, `required_fields/allowed_fields/payload_fields/fields` while preserving the original entry. Do not manufacture equivalence between native payload fields. Each adapter must provide a field-by-field mapping and validate its original schema before producing the common envelope.

Some source interfaces refer to generic result schema filenames that may not exist in that package. Treat unresolved schema references as an adapter-conformance failure, not permission to drop those fields. This design captures declarations; the later adapter inventory must resolve exact paths and report a missing native schema explicitly.

Adopted policy/context, external human evidence, same-run family reports and feedback are distinct input classes. A feedback edge opens an issue and successor plan. It is not inserted into a running DAG. Explicit `not_applicable` needs scope, rationale and authority; absent or unreadable is never not-applicable by default.

The different family authority-tier numbers are not interchangeable. Preserve the originating authority namespace, adopted policy reference and scope. EQA's eight-tier inventory does not settle the still-open precedence among its first six tiers, and it cannot silently overwrite CPR/PPR authority semantics. A material conflict is awaiting_human under EQA-DH-002.

The five supplied surface notes contain no independent routing logic. All surfaces call the same CLI and consume the same map/profile. A driver can decline capacity without changing capability judgment. A human stage can only generate a bounded docket and wait for externally authenticated authority.

## Human decisions and release

A decision packet names question, alternatives, object/capture references, competing findings, governing rule/hook, effect, named owner, next action and due stage. Author-facing packets use neutral query language and preserve the approved source copy. No proposed identity or prose change is applied by this contract.

Preserve the existing author-review source copy, query sheet, HTML review, citation inventory and native family reports, all tied to the source receipt. A workpile-specific packet adds the requested separate APA/style/integrity and independent-review reports and volume rollups. Where governing policy or evidence is missing, that report records not_run/partial coverage rather than inventing a review. No clean or marked text revision is generated without its separate output authority.

`record-decision` validates the receipt through the established authority boundary; signature/identity checking must occur outside the model. A receipt must bind the exact plan or candidate packet and action. Approval of a review packet does not imply acceptance of every proposed edit, constitution acceptance, source modification, package promotion or publication. Replay across objects or runs is denied; expiry/revocation invalidates dependent actions. Audit records remain append-only.

Native model output is untrusted, including fields named approved, signatory or released. Adapters cannot map those strings to a verified human receipt. Model task envelopes allow observation and proposals only, carry explicit denied reserved actions, and expose no capability or credential for invoking the human mutation boundary. The host verifier, not a prompt or model-provided actor label, enforces this separation.

Reconciliation precedence: prohibited effect, source/plan drift, forged authority or critical failure → blocked; unresolved hard input → awaiting_input; pending incorporation/reproof → awaiting_reproof; material unresolved policy or decision → awaiting_human; required absent coverage or unmet production maturity/evaluation → hold. Multiple reasons remain in the result even when a single display status is selected. Only a complete claim with all applicable gates can be ready for human acceptance. Tracked items require an adopted residual-risk policy and specific human receipt; no model waiver is permitted.

No `released` terminal effect exists in the v0.1 CLI. EQA's legacy `released` state can only be observed from an external authorized release receipt, scoped to its exact package; it is never an automatic transition from a successful run. Post-publication cases remain a separate owner-controlled path.

## Proof and format boundaries

PPR requires exact approved manuscript, accepted copyedited version, proof, correction/variation ledger heads and output targets. A typesetting receipt supplies the handoff relationship. Without these, substantive proof review is blocked. Compare only formats for which the adapter has conformance evidence; a PDF visual check does not prove accessible HTML or e-book behavior.

The legacy input extension set remains `.docx`, `.md`, UTF-8 `.txt`. A proposed proof artifact slot can reference PDF and other declared production outputs, but the current runner cannot ingest them through a new generic extension allowlist. Each format needs an adapter, limits, handling approval and tests. Pending that evidence, return unsupported-format/awaiting_input. Count all admitted proofs/assets in the aggregate budget; keep the existing per-file ceiling until an explicit policy authorizes a distinct reviewed limit.

## State and records

All manuscript, author and run material lives in an operator-supplied private state root outside repositories and source trees. Keep fixtures content-free or synthetic identifiers only. Do not rely on `.gitignore` as the sole enforcement: reject state/source/output paths inside any repository at intake and preflight package exports for protected material.

Events append under an exclusive per-run writer lock. Each event binds `prev_event_id`, body and timestamp; its content-hash ID excludes only its own ID. Flush/fsync precedes acknowledgment. A duplicate identical event is idempotent; a corrupt/truncated chain blocks dispatch until explicit recovery. An outbox sends stable event IDs to Kata, preserving unacknowledged events as pending. Failed projection must remain visible. This is an integration specification, not a new system of record.

Every task/result retains the authoritative Dock lineage and links to work item, parent envelope, attempt, lease/fencing token, classification, expiry, acceptance criteria and next owner. G0/G1 grant bounded work; G2 human acceptance and G3 external effects remain separate. G5 promotion/pins and G6 workflow/policy changes are separate owner gates. This packet requests none of those actions.
