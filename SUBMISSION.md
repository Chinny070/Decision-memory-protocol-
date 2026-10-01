# Submission readiness ledger

**Submission title:** Decision Memory Protocol — evidence-backed decision reliance and revalidation

## Four gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Contract / runtime | Partial | 11 Direct Mode tests and GenVM lint/schema pass; clean-clone gate pending. |
| Real consensus | Partial / not green | Exact-text baseline, revalidation, replay, challenge, negative case, and propagation reached accepted consensus on a disposable deployment. The separate semantic-mode baseline reached `UNDETERMINED` / `NO_MAJORITY`; semantic consensus remains unresolved. |
| Real evidence | Partial | A real browser render of official GenLayer docs established a `RELIABLE` baseline and full revalidation using the page’s published heading. Semantic LLM evaluation remains unproven live. |
| Steward fit | Partial | Rejection audit and DM1–DM15 mapping are documented. The live dependency propagation lifecycle is proven on a disposable deployment; final-source parity and push remain outstanding. |

## Submission copy (not final until blockers clear)

- **Category:** Standalone reusable GenLayer Intelligent Contract.
- **Title:** Decision Memory Protocol — immutable decision context, semantic revalidation, counterfactual replay, and dependency-aware reliance.
- **One-line thesis:** Preserves why a decision was defensible, revalidates its assumptions against evidence, and deterministically propagates reliance changes without rewriting history.
- **Repository:** https://github.com/Chinny070/Decision-memory-protocol-
- **Canonical Studionet address / Explorer / deployment transaction:** final-source values pending; an earlier candidate deployment is recorded below.
- **Why GenLayer:** Independent validators must retrieve and interpret current external evidence; one creator, API, or model must not author the reliance result alone.
- **Consensus mechanism:** Custom leader/validator nondeterministic evaluation with typed substantive equivalence; deterministic code derives status and graph effects. Semantic-mode live agreement remains unresolved.
- **Deterministic responsibilities:** Input and graph validation, status/materiality thresholds, lease transitions, immutable receipts, lineage, and bounded propagation.
- **Failure policy:** Insufficient evidence, retrieval failure, or consensus disagreement never becomes affirmative reliance; transaction disagreement does not create an application result.
- **Reuse surface:** `get_reliance_certificate`, `get_reliance_status`, `is_reliable`, and bounded lifecycle writes for any decision domain.
- **Verified tests:** 11 Direct Mode tests; one complete disposable Studionet lifecycle passed; three GenVM lint checks and 22-method schema passed.
- **Live limitation:** The live lifecycle used deterministic exact-text evaluation. A semantic LLM baseline did not reach majority agreement.
- **Reviewer fast path:** `README.md`, `DECISION.md`, `docs/ARCHITECTURE.md`, `docs/INVARIANTS.md`, `docs/CONSENSUS.md`, and `docs/RELEASE_CANDIDATE_VERIFICATION.md`.
- **Portal description:** Decision Memory Protocol is a reusable GenLayer Intelligent Contract that preserves decision context and critical assumptions, revalidates them against independently retrieved evidence, and gives downstream contracts a machine-readable reliance certificate. Validators independently assess external evidence; deterministic contract logic derives reliance state, lease freshness, successor lineage, and bounded dependency impact. It includes immutable counterfactual replay and fail-closed evidence handling. The Direct Mode and exact-text Studionet lifecycle pass; semantic-mode live validator agreement and final-source parity remain open.

## Verified evidence

- Final source commit: pending.
- Earlier candidate deployment: `0xE7146a6556be0F9e5C5729F3660eAD91b50A573C`.
- Deployment transaction: `0x62ca2d689418e2b00a2216e8f41cc5b26c4e2585e428aa3584d5d1d9f47b6968`, `ACCEPTED`, `MAJORITY_AGREE` (five validator agreements).
- Explorer address page: [GenLayer Explorer](https://explorer-studio.genlayer.com/address/0xE7146a6556be0F9e5C5729F3660eAD91b50A573C).
- Deployed schema: 22 public methods (14 views, 8 writes). Final-source parity is pending redeployment and exact comparison.
- Latest disposable integration deployment: `0x29ee1C31AA1e99f59d05BAec46A9b34d1D2ba241`.
- Register main decision: `0xc530b990c3c85b92d851579da64bfa43cbc3935b60a9b92e37e06de395b76b8b`, `ACCEPTED`.
- Browser-render baseline: `0xb7bb7848a35ad2abcc4f1c966303db5e5a4aefe1dd2247ac00de614a6c8e6ab7`, `ACCEPTED`, `RELIABLE`.
- Full web revalidation: `0x3f3bc3eeed33b58078060518d9f6b8368d9c8def9b82180fbee2014f5e1a64cc`, `ACCEPTED`, `RELIABLE`.
- Counterfactual replay: `0x38b15590fd18f0379896efa64ed845af9c552eafba92a869956a36864bdfe510`, `ACCEPTED`, `WOULD_REQUIRE_REVIEW`.
- Evidence-backed challenge: `0x045e5c0060d8eee43babfd0a1b71444ccaf5cbed846e1b987596da04687adee1`, `ACCEPTED`, `OVERTURNED`.
- Negative source case registration: `0xb2eded443eee69ecc47c894a1cb019a30525814dd32ffd9b64f7b452a0e7ab2d`, `ACCEPTED`; unavailable-source baseline `0xaa9a048b260c982fd70556a2554e7be752dfedf0d871ee5fcbf84148f3c142d5`, `ACCEPTED`, `NEEDS_REVIEW` (not invalidated).
- Dependent capsule registration: `0x4d5f0b74b2f3520b0d8c62237632903eb4c345415390617c510cf28e6ddff9ee`, `ACCEPTED`; dependent baseline `0x58a837e916a0dcb5a56ab7a6fbc8c054d137f2f5e6814cbe54659475ddfb9071`, `ACCEPTED`; propagation `0x58a72c7dbca4a98e2f73b24a04f3fec50108914e848d175dde343798d14ff8a1`, `ACCEPTED`, event `impact_3` complete.
- Earlier semantic baseline: `0xa232d7409a4d46aaaf493e606c311f82e2c2750614c53040bf4abfa429cc48e0`, `UNDETERMINED`, `NO_MAJORITY`; validators materially disagreed.
- Hosted integration: 1 passed with strict `ACCEPTED` and `MAJORITY_AGREE` assertions. Direct Mode: 11 passed. GenVM lint: 3 checks passed. GenVM schema: 22 methods.
- Clean clone: pending. GitHub push: pending; configured GitHub token was reported invalid.

## Steward rejection audit

- Database-only: **No.** The protocol computes reliance from accepted consensus findings.
- Monitoring-only: **No.** It freezes decision context and adds replay, dependency impact, lineage, and a machine-readable certificate.
- Provenance clone: **No.** Evidence identity supports the reliance decision.
- Historical truth oracle: **No.** Replay evaluates a committed baseline under a new policy; it does not reconstruct arbitrary past truth.
- Model controls final state: **No.** Contract code controls status, lease, IDs, lineage, graph changes, and propagation.
- Shape-only validator: **No.** The validator independently retrieves evidence and evaluates reliance-critical fields.
- Fake/text-only web proof: **Partial.** A real browser render and exact published heading check were accepted on Studionet; semantic LLM evaluation is still unresolved.
- Decorative graph: **Live bounded proof recorded.** A hard-dependent capsule was covered by accepted propagation; larger graph capacity is covered in Direct Mode.
- Replay rewrites history: **No in implementation.** Direct Mode confirms replay does not mutate the original definition or certificate.
- Lease semantics: **Covered in Direct Mode.** Warning and due-time boundaries are tested.
- Temporary failure invalidates: **No.** Direct Mode and a live unavailable-source baseline both produced review, not invalidation.

## Remaining blockers

- Semantic-mode baseline did not reach majority agreement. Do not claim live validation of semantic LLM findings.
- The final source must be committed, pushed, redeployed, and compared byte-for-byte with the deployed code; a clean-clone gate is also outstanding.

Do not submit or freeze while any gate is not green.
