# University Press: one review-and-release contract

**ERI-38 · Design candidate · 18 September 2026**  
**Commission:** `COMMISSION-UNIVERSITY-PRESS-WORKBENCH-2026-09-17.md`  
**Decision owner:** Eric Tucker. **Scope:** architecture and contract design.  
**Standing:** a proposal for a Tech Triangle center of work using Navy Yard capacity. No institutional designation, runtime activation, package promotion, or manuscript execution is implied.

## 1. Decision

Use EQA as the control specification for a single University Press workbench, and migrate the shipped Codex workbench beneath that interface. The capability map belongs alongside the contract in the workbench repository. It is not another service or another orchestrator. The architecture registry can project its evidence and maturity fields after an authorized registration decision; it must not become a competing route table.

The common contract is **a pinned bundle, a stage profile, a typed dependency plan, and a claim-scoped release recommendation**. Chapter text alone is insufficient. CPR consumes a component profile, cross-file relationships, and upstream statuses. PPR consumes an approved baseline, an accepted copyedited version, a proof version, correction decisions, and reproof evidence. Those are first-class inputs, not optional attachments to an RCI-shaped invocation.

Keep copyediting absent. This is the disposition of the present map, not a decision against building it. Do not adapt writing-craft or divide CE between SGI and TE without a separate commission. A required absent capability has a recorded effect on the claims the workbench may make.

Three alternatives were considered:

| Approach | Consequence | Disposition |
|---|---|---|
| Extend the Codex browser runner directly | Preserves implementation, but makes Windows/Codex and the RCI–SEI pair define every interface | Use it as the migration source, not the generic contract |
| Make EQA a standalone second orchestrator | Duplicates plans, approvals, receipts, and lifecycle control | Reject |
| Consume EQA and migrate the existing runner behind one neutral contract | Reuses editorial policy and implementation without creating two control paths | Recommend |

## 2. What was reconciled

The supplied commission, seven installed package manifests, seven interface files, all 74 hook records, and the CPR/PPR specifications were read. The existing workbench configuration, constitution, lock, source gates and limits were read through GitHub, as were the architecture workpile, lifecycle and inventory. Captures and hashes are recorded in `source-index.json`.

| Evidence | Observation | Limit |
|---|---|---|
| EQA map | Seven domain families, with EQA as the separate control family | A declarative map does not execute a review |
| Installed packages | Six domain packages plus EQA; 199 declared rules, 74 hooks, 310 declared fixtures, nine named critical fixtures | Their editorial fixtures were not executed in this task |
| Codex workbench | RCI then SEI, immutable plan, commit and tree-digest lock, source gates, author packets and human acceptance | Source inspection, not an end-to-end runtime test |
| Architecture inventory | 91 records; 31 metadata-represented repositories; `authority: false` | An evidence inventory is not an activation registry |
| CE | Stub/absence reported in the commission; no CE implementation supplied | Remote CE contents were not independently audited |
| House screener contract | Its field requirements are described in the commission | GitHub returned 404; exact schema and extension rules were unavailable |

There are **eight map entries**, not eight editorial domain packages: seven domain families, including absent CE, plus EQA. The phrase “seven packages” counts the six present domain packages and EQA.

One source discrepancy is material. The installed RCI and SEI snapshots contain cross-family declarations; the commission reported that its original clones did not. The inspected workbench tree also contains vendored cross-family files. This design preserves both observations. It does not conclude that the original nine local trees equal their remotes. Read-time GitHub revision identifiers are evidence references, not new execution pins.

The existing workbench was inspected at `86ca82c2ff02f8bb4af1de73813cacf2783b1863`; the architecture reference at `4727e7295f80527165ea479f0b26030a778aafac`. Package capture hashes do not establish their relationship to either inherited execution pin.

## 3. One map, with separate evidence axes

`capability-map.json` is the proposed sole routing map for this contract. Every entry names its repository, package and specification versions, coverage, refusals, input/output declarations, open hooks, runtime evidence, maturity and evaluation status. Original interface records are retained inside normalized edges so that a field rename cannot erase a restriction.

| Family | Capability | Present package | Scope of judgment |
|---|---|---:|---|
| RCI | `citation_identity` | 0.1.0 draft | Source identity and citation/reference relationships |
| SGI | `adopted_style` | 0.1.0 draft | Explicitly adopted style rules and exceptions |
| TE | `technical_objects` | 0.1.0 draft | Technical objects, structure and relationships |
| CE | `copyediting` | Absent | Prose intervention and meaning-preserving copyediting |
| SEI | `scholarly_integrity` | 0.1.0 draft | Evidence-linked signals and escalation |
| CPR | `component_readiness` | 0.1.0 draft | Presence, applicability, linkage and stage dependencies |
| PPR | `proof_survival` | 0.1.0 draft | Baseline-to-proof comparison and correction/reproof records |
| EQA | `editorial_control` | 0.1.0 draft | Planning, routing, comparison, escalation and release gates |

Presence, definition maturity, package status, activation, human acceptance and critical-fixture coverage remain separate. A draft can pass interface conformance and run an authorized diagnostic review. That does not change its package status or certify production readiness. Conversely, an installed entry note is not proof of a working adapter.

The installed packages demonstrate Codex entry notes. Only RCI and SEI have wiring observed in the inspected runner. The proposed shared operating notes cover Codex, Claude, Hermes, Gemini and GLM; live parity remains `not_run` for every surface in this design. Do not call this a fully operating multiplatform workbench until the required Codex/Claude/Hermes canaries have passed.

After adoption, the planner reads only the canonical map. Old family maps become read-only provenance inputs; any compatibility exports are generated from the canonical map and carry its digest. This candidate does not modify or declare the upstream files globally superseded today.

## 4. Routing and the proof-stage stress test

The caller supplies `stage_profile`, pinned chapter records and context references. The request schema has no family-selection field and rejects extra fields. Profiles ask for capabilities; the map resolves them to families. More than one eligible provider produces retained candidates and `awaiting_human`, never an arbitrary winner.

`stage-profiles.json` carries both the domain precedence edges and the control spine. Stage order remains data. The proposed conservative domain serialization is provisional under EQA-DH-001. It is not a resolution of that hook.

Two specimens demonstrate the interface:

| Profile | Domain route | Honest terminal claim |
|---|---|---|
| `citation_integrity_review` | RCI → SEI | Citation/integrity review packet available for human inspection; no full editorial clearance |
| `production_proof_review` | RCI → SGI → TE → CE gap → SEI → CPR → PPR | Production/proof diagnostic report, with explicit missing inputs and clearance holds |

Each route includes source checks, authority context, independent review, critical checks, packet assembly, a release recommendation and a human acceptance stage. Domain nodes expand per chapter; shared context and packet nodes operate on the batch. A volume-scoped dependency can invalidate several chapter results without rerunning unrelated chapters.

An interface handoff is not automatically a same-attempt precedence edge. RCI may receive approved style context without waiting for a new SGI review; SGI can consume adopted citation rules without rerunning RCI policy resolution. Reciprocal findings are feedback events. They create a successor plan or rerun scope; they do not create cycles in the sealed DAG. Cycles in the actual dependency graph are refused before dispatch.

**CPR:** every required upstream family must have a result or an explicit `not_run`/absent reason. CPR can inventory the CE gap and other incomplete states. It cannot convert a present permissions record into rights clearance, or choose a “final” file from a filename.

**PPR:** the absent CE capability creates a stronger issue than a missing score. PPR requires an accepted copyedited baseline. A baseline supplied by an authorized external human/process can satisfy that input, with receipt and fixity, while CE remains absent as an automated capability. Without that input, PPR substantive comparison is deferred as `blocked_input`. A plausible manuscript cannot replace it. The proof specimen demonstrates the planned PPR node and its hard gates; it does not falsely represent a proof review as executed.

**Reproof:** a correction moves through proposed → human accepted/rejected/deferred → incorporation observed → dependent reproof required → verified resolved. Acceptance alone never closes it. A corrected proof receives a new digest. A successor plan records its parent, new proof and correction-ledger head; reproof includes affected navigation, pagination, index and cross-references. The prior plan and evidence remain immutable.

## 5. Immutability, authority and the capacity seam

The plan binds the source manifest, complete source bundle, map, stage profile including control spine, rules, specification, policies/exceptions, skill lock, route/tool/model revisions, authority context, format targets, baseline and proof. Hashes refer to actual supplied bytes or a specified canonical JSON representation; unknown values cannot be replaced by invented real-world hashes.

Approval is a separate seal over the plan digest. The plan never acquires a mutable `approved=true` field. The reviewer sees the exact plan before an authenticated human approval is recorded. Subsequent changes create a successor plan and require a new seal. Resume rechecks the seal, approval validity, Dock ancestry, route and every relevant digest.

The existing RCI and SEI commit-and-tree locks are preserved verbatim as migration evidence. Other families have **no execution pin** in this packet. Their capture hashes are evidence only. G5-authorized pinning is a later prerequisite for actual execution, not a reason to reject draft maturity.

Every stage declares `offline_batch`, `internet`, `chat_reasoning` or `human`. RCI provider lookups, if authorized, must be separate `internet` tasks; they cannot gain network access by inhabiting a review node. Capability planning emits bounded requests; the Loading Bay selects and admits capacity. The workbench does not implement `declare/meter/admit/dispatch/poll/harvest` as a driver.

`stage-node.schema.json` is a closed union. Machine nodes have a closed operation enum that excludes accepting edits, adjudicating authorship and approving releases. Human nodes require `lane_class: human` and `dispatchable: false`. Publication is absent from both the CLI and its operations. The invalid specimen assigns `approve_release_package` to a model; schema validation rejects it.

Schema typing alone does not authenticate a human. At the runtime boundary, a trusted authority verifier must validate signer identity, delegated role, scope, exact object digest, expiry/revocation and replay protection. Model-supplied “human” receipts have no authority. The verifier is an external dependency, not a credential service invented by this design.

## 6. Release semantics and evaluation

Keep four decisions separate: completed review, accepted review packet, production readiness, and external publication authorization. The workbench may recommend a state; it cannot create the latter authorization or exercise it.

| Condition | Diagnostic work | Recommendation for affected clearance |
|---|---|---|
| Draft package with valid pins, authority and interface safety | May run; preserve draft status | Hold production claim pending required acceptance/evaluation |
| Required CE absent | Record gap; run eligible independent checks | Hold copyediting/full-production claim |
| PPR baseline or accepted copyedited version absent | Inventory only; defer substantive PPR | `awaiting_input`/hold |
| Required source unreadable | Mark `dark`; preserve access uncertainty | No verified finding or zero score |
| Critical workbench safety case fails | Refuse adapter admission or block run | `blocked`, irrespective of aggregate score |
| Family has no named critical editorial fixtures | Authorized diagnostic execution may continue | Critical coverage undeclared; production clearance held |
| All review work complete, draft limitations visible | Candidate packet may be inspectable | `ready_for_human_acceptance` applies only to the named review claim |
| Tracked residual item | Requires an adopted policy, owner, action and receipt | Otherwise hold; the design supplies no risk waiver |

`conformance/cases.json` names the workbench critical set and adapter test obligations. Each candidate family is tested independently of its own fixtures using a standard probe request and observable assertions. A family cannot pass because another family passes. The nine declared EQA critical fixtures remain EQA's own suite. The other six present packages retain undeclared critical coverage; this design does not silently nominate their editorial fixtures.

Coverage reports known, unknown and not-applicable counts and reasons. Unknowns contribute no score and reduce the known coverage fraction; they do not become failures. No aggregate score is used to authorize a release. Contradictory findings retain both capture references and enter a human docket. No capture means hypothesis, not verified claim.

## 7. MWM at approximately 100 chapters

The stress specimen models 100 opaque chapter IDs across two ordered volumes. It uses no manuscript content or author metadata. At an explicit four-MiB-per-chapter assumption, the batch is 400 MiB and fits the inherited 500-MiB ceiling. At twenty MiB each, it would be 2,000 MiB and must not be admitted as one batch. Chapter count alone is not admission evidence.

Retain 250 chapters, 20 MiB per chapter, 500 MiB aggregate, concurrency 1–3, the 240-character prospective Windows output-path check, and existing source/parser/resource safeguards. The inspected configuration also caps model calls at 600; a seven-family plan must estimate its actual calls, including independent review and retries, before admission. This proposal does not increase that ceiling.

Retain the twelve-a-day review budget and existing acceptance classes. If one item is required per chapter, 100 items require at least nine review days. This is a workload illustration, not a new acceptance unit or schedule. Additional questions and reproof create additional work. Queue saturation pauses new dispatch; it never broadens the human review budget.

Each chapter must retain stable ID, volume/order, source digest, status and disposition. Resume is chapter-scoped and idempotent. Shared TOC, ordering or index changes invalidate the relevant volume dependencies. Volume rollups show every expected chapter, including blocked, unreadable and not-run chapters; partial success cannot silently drop them.

The existing workpile's nine criteria are crosswalked in `ACCEPTANCE.md`: preserved originals; attributed reviews; separate APA/citation/style/integrity findings; visible uncertainty; genuinely separate review; complete checkable output; Eric's acceptance before external effects; explicit correction/learning work. Neither the synthetic stress case nor this commission authorizes a real sample. Eric must select and authorize that sample before expansion in accepted waves.

## 8. Migration, ownership and interfaces

Migrate the existing repository in an isolated candidate branch after design acceptance. Keep its UI and `Run-Batch.ps1` as clients of the shared contract. Replace the hard-coded RCI/SEI execution path incrementally; do not retain two independent ways to approve, plan or assemble packets.

| Phase | Required evidence before proceeding |
|---|---|
| Reconcile sources | Owner/operator verifies the intended local trees and remote revisions; exact house contract obtained; native schema references resolved |
| Contract shell | Shared AGENTS and thin surface notes; declared verbs; one JSON document and exit 0/1/2; human-route denials |
| Legacy profile | RCI-before-SEI, inherited lock, source gates, account approval, packets and limits pass regression comparisons |
| CPR/PPR first adapters | Native payload mappings, blocked-baseline case, cross-file gaps and reproof invalidation pass with synthetic fixtures |
| Remaining families | SGI/TE and EQA control obligations pass independent adapter conformance; no automatic CE substitution |
| Surface parity | Codex, Claude and Hermes run the same synthetic cases and produce equivalent normalized decisions; no live support claim before evidence |
| Authorized bounded MWM sample | G0/G1, handling policy, exact source set, pin approvals, accepted routes, owners and review capacity are documented |

The LunaRoute edition should become another transport client of the same contract and lock after its source is inspected. Do not assume shared lock text means equivalent confidentiality controls, account identity, payloads or receipts. Until parity is established, it remains a separate legacy edition, not a verified new surface.

Recommend a shared specification and conformance kit first, with only deterministic hash/schema/receipt/normalization utilities eligible for a common library later. Preserve family-specific editorial judgment in its existing packages.

Acquisition and developmental editing attach before intake through an approved source bundle. Typesetting attaches between accepted production handoff and proof intake through a fixity-bound output bundle. Artifact/flipbook production consumes an authorized release-package reference. None receives implied manuscript distribution authority from this contract.

Kata owns execution state. The local append-only receipt/event store supplies evidence and an idempotent projection outbox; it cannot substitute for Kata. Linear holds commitments, Notion curated knowledge. No live integration with any of these was performed. Dock ancestry is immutable through work item, task, result and reconciliation; `accepted-for-design` cannot dispatch a real task.

## 9. House conformance and explicit bends

`contract.json` contains the commission's v1 fields: agents, humans, entry points with lane classes, exit codes, numbered rules, state layout, append-only content-addressed ledgers, emits, invariants and non-claims. It is validated against a **commission-derived candidate schema**, not falsely represented as certified against the unavailable upstream schema.

Seven editorial extensions are proposed under `extensions.university_press`: capability/maturity declarations; sealed DAG and invalidation closure; human-only nodes and verified receipts; baseline/reproof lineage; native family adapters; coverage and claim-scoped recommendations; Dock/Kata references. Whether v1 permits that extension location is unresolved until its actual schema is read. This is the one outstanding source dependency for exact acceptance check 8.

Recommend keeping one house v1 and generalizing reusable human-node, seal and provenance mechanisms there if its maintainers agree. Do not declare v2 solely to accommodate this workbench. If the real v1 is closed to extensions, prepare one owner-reviewed additive amendment; do not ship an incompatible lookalike.

Other bends are deliberate and named: bundle inputs beyond text; static-context versus same-run dependency edges; externally accepted copyedited baselines despite absent CE automation; diagnostic completion versus production clearance; per-format proof coverage; per-volume invalidation; and authenticated human authority outside model-readable records. None resolves an editorial hook.

## 10. Decisions retained for owners

All 74 hooks are copied with their supplied defaults and remain open. The design particularly depends on EQA-DH-001–005 and 009–013 for graph, authority, routes, handling, risk, proof, provenance, evaluation and reports; CPR-DH-001, 009, 011, 012 for profiles, versions, upstream effects and signatories; PPR-DH-001, 002, 004, 005, 007, 009, 010 for baseline, corrections, scope, reproof and protected records; and RCI-DH-006 for the still-disabled auto-fix possibility. The full register covers every other dependency.

Eric retains CE build authorization, actual sample/full-batch authorization, constitution acceptance, institutional designation, promotion/pins, acceptance classes, review-budget changes, protected-branch changes and external effects. Operators retain source/remote reconciliation and repository-access verification. No finding here appoints an owner, activates a role, grants access, or settles a hook.

The package is ready for design review with its evidence gaps visible. It is not a released workbench. `VERIFICATION.json` distinguishes design checks that ran from adapter, runtime, editorial-efficacy and platform gates that remain unrun.
