# Decision Memory Protocol: differentiation and architecture

## Thesis

Decision Memory Protocol preserves why a decision was defensible, freezes its critical assumptions and baseline evidence, revalidates those assumptions against independently observed current evidence, and deterministically tells downstream contracts whether the old decision is still safe to rely on.

## Product boundary

- Provenance systems answer what the identity or history of evidence is. This protocol uses evidence identity only to support the reliance decision.
- Historical truth systems reconstruct what was true at a past time. This protocol preserves an already committed decision and supports counterfactual evaluation against its frozen baseline.
- Monitoring systems report that facts changed. This protocol adds frozen policy and decision context, dependency impact, immutable successor lineage, and a machine-readable reliance certificate.
- Escrow and warranty systems settle economic obligations. Version 1 has no bond, escrow, token, payout, or marketplace logic.

GenLayer is load-bearing because the decisive semantic work—independently observing and interpreting public evidence—cannot be safely authored by one creator, API, or model. The leader and validators independently render or retrieve evidence and evaluate frozen assumptions. The contract compares reliance-critical typed fields. Deterministic code controls state transitions, leases, graph legality, replay receipts, lineage, and propagation.

## Frozen capsule

Each capsule binds a caller-supplied stable `decision_id`, creator, subject key and hash, bounded decision payload and hash, frozen policy and hash, definition hash, bounded assumption and dependency definitions, timestamps, baseline receipt and semantic snapshot, reliance state, lease, and predecessor/successor linkage.

The capsule's payload, policy, assumption definitions, dependencies, baseline snapshot, and original receipt are not rewritten. Current findings and the single successor link are protocol lifecycle fields. A decision definition change creates a successor.

## Critical Assumption Graph

Assumptions are bounded to eight per decision. Each freezes its statement, criticality, evaluation mode, and one to three HTTPS source bindings. `SEMANTIC` assumptions use GenLayer browser render or supported web retrieval plus structured model judgment. `EXACT_TEXT` assumptions use deterministic substring checks and never call an LLM. Version 1 has no assumption-to-assumption edges; this deliberately keeps the bounded graph acyclic by construction.

## Decision Dependency Graph

Each decision can reference at most eight existing decisions with typed `HARD_DEPENDS_ON` or `SOFT_DEPENDS_ON` edges. A new decision can only point to already registered IDs, so edges cannot create a cycle. Direct fanout is capped at sixteen. Hard invalidation maps to `BLOCKED`; other unsafe upstream states map to `NEEDS_REVIEW`. A soft dependency maps a non-reliable upstream state to `NEEDS_REVIEW`.

Propagation is deterministic and permissionless, uses an explicit cursor and queue, and processes at most eight queue items per call. The queue is capped at 32 unique decisions. Reliance views also inspect direct upstream states so a consumer fails closed before a propagation batch finishes.

## Materiality and reliance

The model emits only typed assumption findings and bounded diagnostics. It never emits final reliance, lease deadlines, graph actions, or IDs. The deterministic reducer applies this policy:

- Any current critical conflict or `CRITICAL_CHANGE` yields `INVALIDATED`.
- A critical assumption without supported, sufficient evidence yields `NEEDS_REVIEW`.
- External failure or insufficient evidence yields `NEEDS_REVIEW`, never invalidation.
- One major finding or contradiction yields `DEGRADED`; two current major findings yield `NEEDS_REVIEW`.
- Three distinct current minor findings yield `NEEDS_REVIEW`; fewer yield `DEGRADED`.
- Otherwise, the decision remains `RELIABLE`.
- `EXPIRING` starts inside the frozen warning window. `STALE` begins at the frozen due time. Semantic invalidation dominates freshness.

The thresholds are deterministic and versioned with the source. A complete revalidation renews the lease; a selective one records per-assumption freshness and never claims a whole-decision refresh.

## Challenges and supplemental evidence

Challenges are permissionless in v1. All callers share a first-come budget of three distinct challenge attempts per decision. Exact duplicate identities are rejected before consensus without consuming a slot. A distinct attempt consumes a slot once a valid consensus report is accepted, including an inconclusive or unavailable-evidence result. This is an intentional bounded-resource tradeoff: an early caller can exhaust the budget before a later challenger arrives. V1 has no stake or authorization gate; the bounded challenge budget and duplicate rejection are the spam controls.

For `EXACT_TEXT`, a challenge must select a frozen registered source and uses its registered retrieval kind and marker. For `SEMANTIC`, a challenger may provide one supplemental HTTPS source. The source and caller's factual ground are untrusted inputs: validators independently retrieve the source and judge its relevance and weight under the frozen assumption and policy. Supplemental evidence affects that challenge finding only; it does not change the capsule's frozen source bindings or definition hash. Integrators that require source authority to be fixed should use `EXACT_TEXT` or avoid treating a semantic challenge as authoritative without reviewing its evidence receipts.

## Counterfactual replay

Historical replay uses only the frozen baseline snapshot, original payload, and new bounded policy. It creates an immutable receipt containing original and counterfactual policy hashes, baseline hash, typed replay output, and consensus digest. Replay does not fetch current web pages or alter current reliance state. A caller can separately create a successor if a new decision is required.
