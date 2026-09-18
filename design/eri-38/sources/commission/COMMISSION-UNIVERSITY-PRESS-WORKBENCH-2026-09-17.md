# Commission — University Press Workbench

**A task for Astra: define the contract and the capability map**
Linear ERI-38 · Issued 2026-09-17 · Tech Triangle plant, Navy Yard capacity · Eric Tucker

---

## Answering the question first

**The capability map already exists. It exists three times, in three
incompatible forms, and none of them is routable.** That is the real shape of
ERI-38, and it changes what the commission should ask for.

| Where it lives | What it has | What it lacks |
|---|---|---|
| `editorial-qa-orchestration/schemas/cross-family-contracts.json` | The seven-family map — RCI, SGI, TE, CE, SEI, CPR, PPR — with declared inbound/outbound per family, a default dependency graph, boundary invariants, an eight-tier authority registry and an eleven-state run vocabulary | No executor, no conformance test, no maturity axis; a skill a model reads, not a contract a caller calls |
| `university-press-citation-review-workbench` | Real machinery that runs: source manifest with SHA-256 per chapter, immutable plan, `skills.lock.json` pinning by commit **and** tree hash, per-stage hash re-check, author packets, run receipt, human acceptance queue | Two of the seven families wired (RCI → SEI). Windows + Codex CLI only. Not routable — the caller must be an editor at a browser form |
| `navy-yard-tech-triangle-architecture` | The workpile draft (`tt.university-press.modeling-what-matters`), the record schemas (work-item → task-envelope → result-envelope), the G0–G6 gates, the promotion lifecycle | `03_skills/skill-registry.json` has 91 records covering 31 repositories and **none of the seven editorial families appears in any of them**; it declares `authority: false` with `promotion_status: unknown` on every row |

So this is not a design-from-scratch job. It is the same job the Loading Bay
Driver contract was: **find the seam between what is true of every editorial
family and what is true only of the two that happen to have been wired, and put
the seam in the right place.** The difference is that here the extracted-from
sample is even more misleading — RCI and SEI are the two most similar families in
the set, and the contract will be shaped by them unless it is stressed elsewhere
first.

Three findings worth stating plainly before the packet.

**1. Copyediting is the hole every family points at, and nobody fills it.**
Six of the seven family specifications say, in their own `description` field, "do
not use for copyediting." The `copyediting` repo is a 44-byte README and a `.git`
directory. It has a GitHub remote, so the name is reserved and the capability is
absent. A map that omits this is dishonest; a map that lets SGI quietly absorb it
is worse.

**2. The families are Codex-dialect, so by your own standard this is not yet a
workbench.** Every package ships `agents/openai.yaml` and nothing else — no
Claude, Hermes, Gemini or GLM entry. The descriptions read "Use when Codex needs
a baseline… review." The standing rule from 15 Sep is that a workbench is not a
workbench unless it applies to Codex and Hermes as well as Claude and it is in
GitHub. On the second half these pass; on the first half they do not.

**3. "Evaluable" has almost no teeth today.** Across the seven packages there
are 199 rules, 74 open decision hooks and 310 evaluation fixtures — real
editorial thinking, and the most valuable asset in the set. But **only EQA names
any critical fixtures** (nine: EQA-11, 17, 19, 25, 27, 36, 43, 46, 50). The other
six name none, so "a critical block cannot be averaged away" is an invariant with
nothing to point at in six of seven families. And every package is `0.1.0`,
status `draft-for-editorial-review` or `draft-for-editorial-owner-review`. The
company constitution's own status is `pilot_requires_press_steward_acceptance`.

The map therefore needs a **maturity axis, not just a presence axis** — and the
contract needs to be able to run a draft package and say so in the release
decision, rather than either refusing to run or pretending readiness.

---

## The capability map as it actually stands, 2026-09-17

Read from the local clones in `Documents\GitHub`. Counts are what the manifests
declare; **no test suite was run** and no GitHub state was verified from this
session.

| Family | ID | Package ID | Rules | Open hooks | Fixtures | Named critical | Manifest shape | Wired into anything |
|---|---|---|---|---|---|---|---|---|
| Reference & Citation Integrity | RCI | `MWM-RCI-PACKAGE` | 23 | 9 | 51 | 0 | **older/divergent** | ✅ pinned in the Codex workbench |
| Style-Guide Implementation | SGI | `MWM-EDITORIAL-SGI` | 22 | 10 | 42 | 0 | standard | ❌ |
| Technical Editing | TE | `MWM-EDITORIAL-TE` | 30 | 10 | 42 | 0 | standard | ❌ |
| **Copyediting** | **CE** | — | — | — | — | — | **repo is a stub** | ❌ |
| Scholarly/Editorial Integrity | SEI | `MWM-EDITORIAL-SEI` | 30 | 9 | 42 | 0 | standard | ✅ pinned in the Codex workbench |
| Chapter Completeness & Production Readiness | CPR | `MWM-EDITORIAL-CPR` | 30 | 12 | 38 | 0 | standard | ❌ |
| Proof & Post-Typesetting Review | PPR | `MWM-EDITORIAL-PPR` | 31 | 10 | 45 | 0 | standard | ❌ |
| Editorial QA & Orchestration | EQA | `MWM-EDITORIAL-EQA` | 33 | 14 | 50 | **9** | standard | ❌ (declares the graph nothing executes) |
| | | **totals** | **199** | **74** | **310** | **9** | | **2 of 7** |

All nine repositories (the seven families, EQA, and the workbench) carry
`github.com/tuckerebc-max/<name>.git` remotes.

**Key drift that has to be resolved, not tolerated.** The cross-family contract
files do not agree with each other: EQA uses `contract_id: MWM-EQA-CONTRACTS` and
is the only one holding a global `family_order`; TE, CPR and PPR use
`contract_id` with their own IDs and only local `inbound`/`outbound`; SGI has no
`contract_id` at all, using `contract_set_id`; RCI and SEI ship no
`cross-family-contracts.json`. RCI's `package_manifest.json` is a different shape
from the `MWM-EDITORIAL-*` five — top-level `rule_count`, `subskills`,
`fixture_total`, `open_decision_hooks`, rather than the `rule_registry` and
`evaluation` objects the others use. Seven packages, five conventions.

---

## The packet

Post sections 1–6 as the first message of the workspace thread. Open this as a
**workspace**, not a lane — it accrues context and closes when the design ships —
and open it on a `$200`-tier account so Extra High is available; this is
architecture, not iteration. Everything below the rule is the commission proper.

---

### 1. OBJECTIVE

Define the **University Press Workbench contract** — the interface through which
a caller hands the Press a chapter batch and a stage and receives a plan, then a
release decision — and the **capability map** it routes over: one machine-readable
registry of what each editorial family covers, refuses, needs, emits, and is
mature enough to be trusted with.

Decidable: at the end, the dock can hand the workbench a pinned chapter set and a
stage profile and get back an ordered, gated, immutable plan plus a release
decision, without the caller naming a family, and without a model being able to
express a plan in which it accepts an edit or authorizes publication.

Scope is the **review-and-release spine**: intake → family reviews → completeness
→ proof → human acceptance. Acquisition, developmental editing, typesetting
itself, and artifact/flipbook production are out of scope for v0.1 — but name the
seams where they attach.

### 2. REPOSITORY STATE

**Shipped and working** — `university-press-citation-review-workbench`
(`UNIVERSITY-PRESS-CITATION-REVIEW-CODEX-0.1`, status `reviewed_codex_release`).
A local browser app at `127.0.0.1:8765` plus `Run-Batch.ps1`. Windows 10/11,
PowerShell, Python 3.11+, Codex CLI, editor's own `codex login`. Required stage
order is data, not code: `source_manifest → reference-citation-integrity →
scholarly-editorial-integrity → author_packet → human_acceptance`. Fixed gates
include per-run Codex-account approval bound to the exact manifest,
version-pinned skill packages, strict structured model output, neutral signal
language, and source-hash reconciliation before completion.
`automatic_text_changes: false`, `publication_authority: false`. Limits: `.docx`,
`.md`, UTF-8 `.txt`; 20 MB per chapter; 250 chapters or 500 MB per batch;
concurrency 1–3; a Windows path-length pre-check that stops the run before any
model call. A LunaRoute edition exists as a separate repo
(`…-workbench-Lunaroute`) and shares the same `skills.lock.json`.

**Specified but wired to nothing** — SGI, TE, CPR, PPR. Full packages,
specification plus rules plus schemas plus evals, never executed by any
orchestrator. CPR and PPR in particular have never run against anything.

**Specified as the control layer, executing nothing** — EQA. Ten sub-skills
`EQA-01`…`EQA-10`, thirteen schemas including `invocation-envelope`,
`dependency-node`, `route-decision`, `family-result`, `decision-receipt`,
`provenance-event`, `release-package`. Default graph:
`EQA-01 → EQA-02 + EQA-06 → EQA-03 → EQA-04 → (RCI, SGI, TE, CE, SEI) → CPR →
PPR → EQA-05 + EQA-07 → EQA-08 + EQA-09 → EQA-10`.

**Absent** — CE.

**The yard machinery to conform to, not reinvent.**
`navy_yard.workbench_contract.v1` is the current house standard, set yesterday by
`screen-measurement-instrument-quality`: `agents`, `humans`, `entry_points`,
`exit_codes` (0/1/2), one canonical JSON document per verb to stdout, verbs each
carrying a `lane_class`, numbered rules, `state_layout`, append-only JSONL
ledgers with content-hash IDs, `emits`, `invariants`, `non_claims`. Beside it,
`loading-bay-driver/0.1` routes *capacity* with `declare / meter / admit /
dispatch / poll / harvest` and lane classes `offline_batch`, `internet`,
`chat_reasoning`, `human`. The architecture repo holds the record lifecycle
(`work-item → task-envelope → result-envelope → observation → skill-promotion`)
and the G0–G6 gates.

**Tried and set aside.** Chapter-by-chapter chat execution — that is the thing
the workpile draft exists to replace. Do not propose it, at any scale.

### 3. EVIDENCE

**The real work this has to survive.** Modeling What Matters:
`tt.university-press.modeling-what-matters`, two volumes, approximately 100
chapters, approximately 100 real authors, a real publishing relationship. Status
`proposed real-work candidate; not yet authorized for bulk execution`. The
workpile draft already specifies its own input contract, nine acceptance
criteria, a G0–G6 gate set, and a pilot path that begins with a bounded sample.
Treat that document as a requirement, not background.

**The maturity facts.** Seven packages at `0.1.0`, all draft. The company
constitution `UNIVERSITY-PRESS-CONSTITUTION-0.1` is
`pilot_requires_press_steward_acceptance` and has not been accepted. Work Bench
Constitution Article 7: nothing becomes canonical because it exists in a
repository; promotion needs provenance, review, tests, a version, an owner and a
rollback path. The controlling release adds that GitHub presence alone remains
`unknown` for installation, activation and production readiness.

**The reserved human decisions, quoted from the constitution.** Accept or reject
a proposed edit; resolve identity or policy ambiguity; adjudicate authorship or
serious integrity concerns; approve a release package; authorize publication.
Prohibited effects: overwrite a source chapter; silently change identity-bearing
metadata; infer intent or misconduct from prose; publish or externally distribute
a manuscript; process restricted material through an unapproved tool.

**The evidence discipline already in force elsewhere in the yard**, which this
contract inherits rather than reinvents: *missing is not failing* — unknown
contributes nothing, is reported as coverage, and widens the range; *absence is
not zero* — an unreadable source yields `dark` plus an entry in `unknowns`, never
a 0; *a claim without a capture URI is a hypothesis*; *ties are kept*; *the corpus
is pinned and pinned records are read-only*; *outside checks are appended beside
pinned values, never over them*; *disagreements go to a human*.

**The ontology fact that constrains the language.** University Press is a
metaphorical center of work in the Tech Triangle. The name alone creates no legal
entity, department, imprint or program. Contract and map text must say "center of
work" or "designated workflow home," never "the press" as an institution.

**What could not be verified from this session.** No GitHub state was read — this
cloud session carries no GitHub credential, so every claim above rests on the
local clones. No test suite was run; all fixture and rule counts are manifest
declarations. Whether the nine remotes match their local trees is unknown.

### 4. CONSTRAINTS

a. **Levels.** The Navy Yard is the factory; the Tech Triangle is the level that
   has companies; University Press is a Tech Triangle center of work. The
   workbench is **Triangle-level plant that runs on Navy Yard capacity.** Do not
   place it in the factory.
b. **Capability routing and capacity routing are separate objects.** The loading
   bay routes to a surface; this workbench routes to a family. Each stage
   declares the lane class it needs, in the vocabulary the bay already speaks
   (`offline_batch`, `internet`, `chat_reasoning`, `human`). Do not collapse the
   two contracts, and do not make the workbench a driver.
c. **Source fidelity is absolute.** Originals never modified, derivatives to a
   separate output tree, source digest re-checked before extraction, before every
   model stage, and before packet assembly, with a mismatch blocking the chapter.
   The shipped workbench enforces this. Do not loosen it.
d. **The reserved human decisions must be unroutable by construction** — not
   merely documented. A plan in which a model accepts an edit, adjudicates
   authorship, approves a release package or authorizes publication should be
   inexpressible in the contract.
e. **A workbench applies to Codex and Hermes as well as Claude, and lives in
   GitHub.** `AGENTS.md` as the shared operating contract, thin per-agent entry
   notes, machine-readable `contract.json`, one CLI with exit codes 0/1/2, tests.
   A Claude-dialect document set on local disk does not count, and neither does a
   Codex-only one.
f. **No silent promotion.** This design changes no package version, claims no
   acceptance, and pins nothing new. Promotion is G5 and Eric's alone.
g. **Kata is the execution ledger; Linear holds commitments; Notion holds curated
   knowledge.** Workbench receipts do not take that role.
h. **Draft is a runnable state, not a blocker.** The contract must be able to run
   a `0.1.0` draft package and carry that maturity into the release decision
   honestly. Refusing to run and pretending readiness are both wrong answers.
i. **Conform to `navy_yard.workbench_contract.v1`, and name every bend.** Where
   editorial work needs a field the screener contract does not have, say so
   explicitly and recommend whether v1 should grow. Two workbench contracts in
   one family is the outcome to protect.
j. **No manuscript content, author metadata, credentials or run output in any
   repository, ever.** Restricted material stays blocked until a separately
   reviewed handling policy exists.

### 5. AUTHORITY BOUNDARIES

**You may decide:** the contract itself — the verb set and signatures; the
**family capability declaration** format (what a family covers, refuses, needs
inbound, emits, its maturity, its runtime targets, its open hooks); the stage-plan
object and how it becomes immutable; the family-result envelope; the maturity
vocabulary; the refusal and error taxonomy; the shape of the workbench-level
conformance suite; how stage order stays data rather than code.

**You may recommend:** whether EQA becomes the workbench or is consumed by it;
repo naming and split, and whether the map lives in its own repo; whether the
seven packages share a library or only a specification; whether the shipped Codex
edition migrates onto the contract or is explicitly superseded; the CE
disposition; the migration sequence; whether this should become
`navy_yard.workbench_contract.v2`; how the LunaRoute edition is reconciled.

**Eric's alone:** whether copyediting gets built at all; any authorization of a
real MWM batch, sample or full; press-steward acceptance of the company
constitution; whether University Press is designated something more than a center
of work; promoting any package past `0.1.0`; any change to the acceptance classes
or the twelve-a-day review budget; anything that touches an author's file, spends
money, leaves the building, or lands on a protected branch.

**Not yours at all:** the 74 open decision hooks. Those are owner editorial
policy, not design. Where the contract depends on one, name the hook and say what
the design assumes provisionally — do not resolve it. Likewise: whether Sheryl
has repository access, and whether the nine GitHub remotes match their local
trees.

### 6. ACCEPTANCE CHECKS

1. **One map, not seven.** A single machine-readable capability map names every
   family, its repo, package and specification version, declared inbound and
   outbound, maturity, runtime targets, and open hooks. The per-family
   `cross-family-contracts.json` files either derive from it or are declared
   superseded. The five naming conventions become one.
2. **Routable without branching.** A caller hands over a pinned chapter set and a
   stage profile and gets an ordered, gated plan, without naming a family.
   Demonstrated over **two** profiles, one of which exercises CPR and PPR.
3. **Honest about the hole.** CE appears in the map as an absent capability with a
   stated effect on what the workbench may claim — not omitted, and not covered
   by SGI or TE by implication.
4. **Evaluable at the workbench level.** A conformance suite a family package
   passes or fails independently of its own fixtures, plus a named critical set
   whose failure blocks release regardless of aggregate score. Six of seven
   packages name no critical fixture today; the contract says what happens to a
   family in that state.
5. **Survives its hardest case.** Checked explicitly against the real MWM batch —
   roughly 100 chapters, two volumes, real authors — and against a release
   decision that needs to be made while a required family is at draft maturity or
   absent. Every place the contract had to bend for one of these is named.
6. **The seam with capacity holds.** Every stage declares its lane class in the
   loading bay's vocabulary, and a human stage is a stage the bay cannot dispatch
   to a model.
7. **The shipped workbench migrates or is explicitly superseded**, with the
   RCI-before-SEI order, the commit-and-tree-hash pinning, the per-stage source
   hash gates and the author-packet discipline preserved either way. If
   superseded, say what replaces its 250-chapter and 500 MB batch limits and its
   Windows path-length pre-check.
8. **Conformance to `navy_yard.workbench_contract.v1` is stated**, with every
   extension named and a recommendation on whether v1 should absorb it.
9. **Reserved human decisions are unroutable by construction**, demonstrated by a
   plan that cannot be expressed.
10. **Nothing is promoted.** No version changes, no acceptance claimed, and the
    design lists which open decision hooks it depends on and what it provisionally
    assumed.

---

## Suggested shape of the work

Yours to change. This is the order that keeps the contract honest, and it is
deliberately not "wire up all seven families."

1. **Reconcile, do not invent.** Start from EQA's `cross-family-contracts.json`
   and the seven `package_manifest.json` files. The family interfaces are already
   written; lift them into one registry and resolve the key drift. Separate what
   is genuinely generic from what is MWM-specific — the authority tiers and run
   states are probably generic; the MWM style guide and APA 7 interpretation
   certainly are not.
2. **Stress it against the proof stage immediately, before the contract sets.**
   The shipped workbench only ever ran RCI → SEI, the two most alike families in
   the set. CPR needs little model work and heavy cross-file state; PPR needs a
   fixed baseline, a fixity record and a reproof loop; a human ruling needs a
   stage nothing can dispatch. If the contract survives those three, the middle
   of the set will be easy.
3. **Write the family capability declaration.** This is the piece routing
   consumes and the piece the map is made of. Maturity is a first-class field, on
   the same footing as coverage.
4. **Write the stage-plan object.** How a batch becomes an ordered plan with
   gates, how the plan becomes immutable at approval, and how a stale family
   result is detected when a rule, source bundle, route or specification changes.
   EQA already specifies this behaviour; give it a shape.
5. **Specify the conformance suite.** What a family package must pass to be
   admitted, separate from its own fixtures.
6. **Decide the CE disposition** and say so in one paragraph: build, adapt an
   existing writing-craft package, split its work between SGI and TE, or declare
   it absent with a stated effect on release claims.
7. **Migrate or supersede the Codex edition**, keeping the hash gates and the
   pinned-package discipline.
8. **Name what you left undecided**, and which owner decisions the design waits
   on.

## Deliverable

A design document plus the machine-readable artifacts: the capability map and a
`contract.json` satisfying `navy_yard.workbench_contract.v1`. The document is the
primary artifact — Codex builds the workbench from it, later, and the map is what
the workbench routes over.

## What this is not

Not a rewrite of the seven packages. Those 199 rules, 74 decision hooks and 310
fixtures are the most valuable thing in the set — real editorial judgment,
written down, with the open questions left visibly open. The specifications are
the asset; the contract is the missing thing.

Not a resolution of the open hooks, not a promotion of any package, not an
authorization to touch a real chapter, and not a second orchestrator to sit
beside EQA.

The job is to make one honest map of what the Press can actually do today —
including the part it cannot — and one interface through which that map can be
routed, evaluated, and handed a real volume.
