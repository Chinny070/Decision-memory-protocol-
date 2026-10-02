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

EXACT_TEXT criteria and source authority are frozen at registration. EXACT_TEXT challenges can select only a registered source and retain its retrieval kind and marker. SEMANTIC challenges may submit one supplemental HTTPS source; validators independently retrieve and assess it under the frozen assumption and policy, while treating the caller's factual ground and page contents as untrusted. This supplemental source does not rewrite the registered source list. Only the predecessor creator may create its single successor. Challenges are permissionless and share a first-come budget of three distinct attempts per decision; exact duplicates do not consume a slot, but a distinct attempt can consume one even when evidence is inconclusive. This bounded tradeoff is intentional in v1. Validators bind evidence reports to independently recomputed render/content hashes, and replay validators agree on the exact typed result stored by the contract.

## Bounds

| Resource | Limit |
| --- | ---: |
| Decisions | 32 |
| Assumptions per decision | 8 |
| Evidence sources per assumption | 3 |
| Dependencies per decision | 8 |
| Direct fanout per decision | 16 |
| Revalidations per decision | 32 |
| Permissionless challenge attempts per decision | 3 distinct attempts; shared first-come budget |
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

The current source passes 22 Direct Mode tests, 3 GenVM lint checks, and a 22-method schema check. The steward-requested semantic safety fix rejects contradictory evidence fields in both report validation paths and makes the reducer fail closed. The matching source is committed on GitHub in `08addb48a6d554596fe9e5ef395e6ba1e5b3f7ff` and deployed to Studionet at [0xC3c63aB9459fd8BC87fa29161e2019F7d454B643](https://explorer-studio.genlayer.com/address/0xC3c63aB9459fd8BC87fa29161e2019F7d454B643). Deployment transaction `0x509b1314e9d6e96792427b135ba3c0260dcf1af3fb8b05fb0f234cf8ca81ec56` reached `FINALIZED` / `MAJORITY_AGREE`; deployed-source parity was verified at normalized SHA-256 `eafa0b94585c0110889dd2cc3fdced1bc667853e74712eef6e4eef3933ffd699`. The new address has finalized semantic baseline and full revalidation proofs, both `RELIABLE`. A broader lifecycle rerun reached baseline, revalidation, replay, and challenge, then stopped during receipt polling after an RPC 502; unavailable-source and dependency-propagation proofs on this new address remain unverified. See [SUBMISSION.md](SUBMISSION.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md), and [docs/VERIFICATION.md](docs/VERIFICATION.md).
