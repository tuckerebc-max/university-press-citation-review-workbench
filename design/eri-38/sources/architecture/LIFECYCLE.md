# Workpile and Lifecycle — Controlling Specification

## Separate namespaces

Never collapse these into one status:

- **Loading Dock admission:** needs-clarification, accepted-for-design, accepted-for-routing, held, rejected.
- **Definition maturity:** proposed, drafted, reviewed, implemented, verified, retired.
- **Work-item lifecycle:** intake, designed_ready, committed, queued, active, blocked, review, accepted, released, closed, cancelled.
- **Attempt state:** leased, running, waiting, retryable_failure, terminal_failure, expired, unknown.
- **Result outcome:** pass, fail, partial, blocked, inconclusive.
- **Approval:** not_required, pending, approved, denied, expired, invalidated.
- **Projection:** not_started, proposed, applied, verified, drift, partial, unknown.
- **Registration/activation:** absent, configured, authenticated, permission_verified, registered, activated, production_verified.

## Harbormaster operational record chain

```text
LoadingDockIntake
 -> LoadingDockDecision(accepted-for-routing)
 -> WorkItem
 -> ContextPackage
 -> RoutingDecision
 -> LoadingBay / bounded task or workbench-call handoff
 -> ProgressEvidence + expected next event
 -> Escalation/recovery when needed
 -> artifact closeout + CapabilityHarvest
```

The current JSON task/result/approval/projection contracts remain normative. Every execution-chain record carries the same immutable `dock_lineage`, and every execution-capable descendant requires `decision_status: accepted-for-routing`. Missing or mismatched Dock ancestry is a hard denial and may not be repaired after execution begins. The authoritative state mapping and invalid transitions are in `schemas/LOADING_DOCK_LIFECYCLE_CROSSWALK.json`. The Harbormaster record and event crosswalk is in `schemas/HARBORMASTER_RECORD_CROSSWALK.md`; it preserves explicit context completeness, capacity-versus-capability evidence, routing warrants, credible progress, partial/unknown outcomes, and named next owners.

## Required lifecycle

```text
need / direction
 -> Loading Dock intake and decision
 -> accepted-for-routing
 -> decision-ready brief
 -> design record (or justified reduced packet)
 -> designed-ready work item
 -> commitment and owner
 -> scoped execution
 -> independent review / evaluator evidence
 -> human acceptance
 -> release decision
 -> real-world use
 -> after-action and capability harvest
 -> reviewed improvement or explicit retirement
```

Acceptance is not release. Dock admission is not execution or release. `accepted-for-design` is not `accepted-for-routing`. A review verdict is not authorization. A closed Linear issue is not precedent. A completed skill test is not production registration.

## Handoff record

Every handoff identifies immutable Dock lineage, sender, recipient/next owner, predecessor, artifact IDs/versions, source/target revisions, classification, open decisions, acceptance criteria, expiry, idempotency key, evidence refs, and disposition. A handoff without a next owner or with missing/mismatched Dock ancestry is incomplete and cannot dispatch.

## First bounded pilot

Use the included `pilot/` packet with synthetic/placeholder content. It exercises morning decision brief -> research brief -> source packet -> draft -> independent review -> local-only accepted artifact -> learning record. The pilot must not mutate Linear, Notion, GitHub, email, CRM, public channels, or production registries. `PASS_LOCAL_ONLY` means mechanics and evidence checks passed; it is not publication authorization.

