# Decision Memory Protocol

**An evidence-backed reliance layer for decisions that need to stay auditable as assumptions change.**

Decision Memory Protocol stores a frozen decision definition, the assumptions and evidence that supported it, and a typed Reliance Certificate. GenLayer validators independently retrieve current web evidence and evaluate semantic assumptions. Deterministic contract code maps their accepted typed findings into reliance state and propagates changes through bounded dependency graphs.

This repository contributes a reusable Intelligent Contract primitive. It is not a dashboard, generic fact checker, evidence archive, historical truth oracle, or escrow system.

## What a downstream contract reads

```python
certificate = decision_memory.get_reliance_certificate("vendor-risk-2026").call()
if certificate["current_reliance_status"] != "RELIABLE":
    # fail closed before acting on the historical decision
    ...
```

The certificate carries definition and policy hashes, assumption and dependency roots, baseline evidence digest, latest revalidation digest, typed reliance state, successor, and lease timestamps. `is_reliable(decision_id)` is a compact safety gate.

## Protocol flow

1. `register_decision` creates a `REGISTERED` capsule. It cannot become reliable from creator input alone.
2. `establish_baseline` uses GenLayer consensus to independently retrieve public evidence and record typed baseline findings.
3. `revalidate` checks all assumptions or an explicit subset. Partial checks are marked `PARTIAL`; only complete checks renew the decision lease.
4. `create_counterfactual_replay` evaluates the frozen baseline against a new policy and stores an immutable replay receipt without changing the original capsule.
5. `propagate_impact` processes dependency effects in bounded, resumable steps.
6. `challenge_revalidation` requires a bounded reason, new HTTPS evidence, and a factual ground, then records a fresh consensus-backed result.
7. `create_successor` preserves the old decision and links a new capsule with a typed reason.

## Typed state

- Support: `SUPPORTED`, `WEAKENED`, `CONTRADICTED`, `INSUFFICIENT`, `UNAVAILABLE`
- Materiality: `NO_MATERIAL_CHANGE`, `MINOR_CHANGE`, `MAJOR_CHANGE`, `CRITICAL_CHANGE`, `INSUFFICIENT_EVIDENCE`, `EXTERNAL_FAILURE`
- Reliance: `RELIABLE`, `EXPIRING`, `DEGRADED`, `NEEDS_REVIEW`, `STALE`, `BLOCKED`, `UNKNOWN`, `INVALIDATED`
- Replay: `WOULD_REMAIN_RELIABLE`, `WOULD_DEGRADE`, `WOULD_REQUIRE_REVIEW`, `WOULD_INVALIDATE`, `INCONCLUSIVE`

External failure is not semantic contradiction. Insufficient or unavailable evidence cannot establish `RELIABLE`. A critical contradiction or critical materiality finding deterministically invalidates the capsule. Downstream effects are computed by contract code, not by the model.

## Bounds

| Resource | Limit |
| --- | ---: |
| Decisions | 32 |
| Assumptions per decision | 8 |
| Evidence sources per assumption | 3 |
| Dependencies per decision | 8 |
| Direct fanout per decision | 16 |
| Revalidations per decision | 32 |
| Challenges per decision | 3 |
| Replays | 32 |
| Propagation queue | 32 decisions |
| Propagation work per call | 8 decisions |
| Payload / policy / source text | 2 KiB / 4 KiB / 9 KiB |

Internal state uses `TreeMap` and `DynArray`; records are bounded canonical JSON strings. IDs are caller-chosen stable identifiers, while fingerprints use `h_`-prefixed SHA-256 digests.

## Build and verification

Requires Python 3.12+ and the pinned GenLayer tooling in `requirements.txt`.

```powershell
python -m pip install -r requirements.txt
pytest -q tests/direct
$env:PYTHONUTF8='1'
genvm-lint check contracts/decision_memory.py
genvm-lint schema contracts/decision_memory.py
```

The Direct Mode suite uses strict local web and LLM mocks and does not reach the public internet. Hosted integration and canonical deployment instructions are in [docs/INTEGRATION.md](docs/INTEGRATION.md) and [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

## Three reusable consumers

1. An autonomous agent checks whether a previously selected provider still satisfies frozen licensing and security assumptions.
2. A DAO or governance contract checks a vendor approval before executing a later dependent action.
3. A compliance or risk contract blocks or requests review before relying on an old policy decision whose critical evidence changed.

All three use the same certificate and safety gate; no domain-specific contract fork is required.

## Current verification state

The repository began empty. The current candidate has 11 passing Direct Mode tests and passing GenVM lint/schema checks. A Studionet deployment reached `ACCEPTED` / `MAJORITY_AGREE`; however, it predates the final source edits, and exact parity must be re-established. A disposable hosted run accepted a real rendered-evidence baseline and revalidation but classified the marker as absent; semantic baseline and replay attempts produced majority disagreement. These are not submission-green results. See the exact ledger in [SUBMISSION.md](SUBMISSION.md).
