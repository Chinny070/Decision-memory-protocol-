# Submission readiness ledger

**Submission title:** Decision Memory Protocol — evidence-backed decision reliance and revalidation

## Four gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Contract / runtime | Partial | 11 Direct Mode tests, GenVM lint/schema, and a clean clone of contract-source commit `176136e` pass. Latest integration harness/docs additions are being committed separately. |
| Real consensus | Partial / not green | Canonical exact-text baseline, full revalidation, replay, challenge, failure handling, and dependency propagation reached accepted majority consensus. A focused semantic-mode baseline also reached accepted majority consensus; its full revalidation was interrupted by an RPC disconnect before a receipt was obtained. |
| Real evidence | Partial | Canonical browser-rendered official documentation established a reliable exact-text baseline and revalidation. Semantic interpretation has a live reliable baseline; semantic revalidation and material drift under LLM judgment remain unproven. |
| Steward fit | Partial | Rejection audit and DM1–DM15 map are documented. Canonical dependency propagation completed. Semantic-mode revalidation and final clean clone of the evidence-documentation commit remain outstanding. |

## Submission copy (not final until all gates clear)

- **Category:** Standalone reusable GenLayer Intelligent Contract.
- **Title:** Decision Memory Protocol — immutable decision context, semantic revalidation, counterfactual replay, and dependency-aware reliance.
- **One-line thesis:** Preserves why a decision was defensible, revalidates its assumptions against evidence, and deterministically propagates reliance changes without rewriting history.
- **Repository:** https://github.com/Chinny070/Decision-memory-protocol-
- **Canonical Studionet address:** [0xC25E6be425d940BB4b794932b1226D4bccD21824](https://explorer-studio.genlayer.com/address/0xC25E6be425d940BB4b794932b1226D4bccD21824)
- **Deployment transaction:** `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`, `ACCEPTED`, `MAJORITY_AGREE`.
- **Deployment source commit:** contract source from `176136ee1bb507aee8aa86673741ee9d8792500d`.
- **Why GenLayer:** Validators independently retrieve and interpret external evidence; one creator, API, or model must not author reliance alone.
- **Consensus mechanism:** Custom leader/validator nondeterministic evaluation with typed substantive equivalence; deterministic code derives reliance and graph effects.
- **Failure policy:** Insufficient evidence, source failure, or consensus disagreement never creates affirmative reliance; transaction-level disagreement is not an application status.
- **Reuse surface:** `get_reliance_certificate`, `get_reliance_status`, `is_reliable`, plus bounded lifecycle writes.
- **Verified local checks:** 11 Direct Mode tests; 3 GenVM lint checks; 22-method schema; clean clone of the deployed contract-source commit.
- **Verified live checks:** One complete disposable Studionet lifecycle and the canonical lifecycle transactions listed below. The semantic-mode baseline passed; semantic revalidation was interrupted by an RPC disconnect.
- **Reviewer fast path:** `README.md`, `DECISION.md`, `docs/ARCHITECTURE.md`, `docs/INVARIANTS.md`, `docs/CONSENSUS.md`, and `docs/RELEASE_CANDIDATE_VERIFICATION.md`.
- **Portal description:** Decision Memory Protocol is a reusable GenLayer Intelligent Contract that preserves decision context and critical assumptions, revalidates them against independently retrieved evidence, and gives downstream contracts a machine-readable reliance certificate. Validators independently assess external evidence; deterministic contract logic derives reliance state, lease freshness, successor lineage, and bounded dependency impact. It includes immutable counterfactual replay and fail-closed evidence handling. Direct Mode, GenVM validation, and a canonical exact-text lifecycle pass. Semantic-mode live baseline passes; full semantic revalidation and final clean-clone verification remain open.

## Canonical deployment and source parity

- Network: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- CLI: `genlayer` 0.39.1; deployer public address `0xaffe15eec45b68835cc9e5b4ab85dd5deae8e70b`.
- Contract: `0xC25E6be425d940BB4b794932b1226D4bccD21824`.
- Deployment transaction: `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`, `ACCEPTED` / `MAJORITY_AGREE`.
- Explorer address: https://explorer-studio.genlayer.com/address/0xC25E6be425d940BB4b794932b1226D4bccD21824 (HTTP 200; address found in page).
- Explorer transaction: https://explorer-studio.genlayer.com/tx/0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac (HTTP 200; transaction hash found in page).
- Deployed schema: 22 methods (14 views, 8 writes).
- Contract blob at source commit: `73007b3208992af1cb333bc6605861d99b8fa67b` (Git blob SHA-1).
- Deployed source normalized-text SHA-256: `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`.
- Source parity: verified. The source returned by `genlayer code` exactly matched the decoded Git blob after removing only CLI display framing newlines; normalized content hashes matched.

## Canonical Studionet lifecycle evidence

The successful canonical lifecycle used decision prefix `live-docs-10892` on the final-source contract. Each accepted transaction below reached `MAJORITY_AGREE` unless noted.

| Scenario | Transaction | Status / typed result |
| --- | --- | --- |
| Register primary decision | `0x84c917569ff16d3042ece4db5a3679c448e28665447fd46e58079c1960ec583f` | `FINALIZED` / `MAJORITY_AGREE` |
| Browser-rendered baseline | `0x2c45ec1422b82df4090843e70a13785d30783e6be88c052b9486893ddccb504f` | `ACCEPTED`, `RELIABLE` |
| Full web revalidation | `0x7a19e6da388aadb8a2437c6345e9e8740c92fbefbf57cdbc87413ee6361d7474` | `ACCEPTED`, `RELIABLE` |
| Counterfactual replay | `0xc4c6dca15c505df4f916574b8eed60f708e8613780174c2cf2371b0f5af581dd` | `ACCEPTED`, `WOULD_REQUIRE_REVIEW` |
| Evidence-backed challenge | `0x1c5b4b02de5af5af6545d538da85997ca1007f782d9595daf1d33e7df05220e2` | `ACCEPTED`, `OVERTURNED` |
| Register unavailable-source decision | `0x6bca1dcd343babf49da3fd040060b6ac59d3343087b459d260be03c34a398557` | `FINALIZED` / `MAJORITY_AGREE` |
| Fail-closed unavailable-source baseline | `0x5a199cbe09ef2f4e867a7ec0fc7ab106d42d99ad463256924568f6066f1e57f7` | `ACCEPTED`, `NEEDS_REVIEW` (not invalidated) |
| Register hard-dependent decision | `0xc89b9f74664049a0a967bd6757198f757890e4daac0ca2fa50ca4b0edc4239fc` | `FINALIZED` / `MAJORITY_AGREE` |
| Dependent baseline | `0xf20237d48ecab71bb438993be2c6c27dde0d35930f16a483414a602475887465` | `ACCEPTED` / `MAJORITY_AGREE`; dependent status `NEEDS_REVIEW` |
| Bounded dependency propagation | `0xa6bc9ffb153cf8e82fa449c0a0a9d72b7b7dff68919f4300631ddfad56a94376` | `FINALIZED` / `MAJORITY_AGREE`; event `impact_4` complete |

The initial canonical test process lost RPC connectivity while polling the dependent registration after Studionet had accepted it. The receipt was reconciled directly; a separate canonical resume test verified the dependent status and complete impact event. An earlier challenge transaction `0x97a00d95b19bc35c693e0047ee8befb541fb41fc270745ae829d0d0a875237f4` was `CANCELED` before validator rounds and is not counted as success.

## Semantic-mode live proof

- Focused official-docs semantic baseline: `0x55c0b372aeb0be1444e447dcc614239873c81a5d2ac80dcc8e9a7b68ab5dca10`, `FINALIZED` / `MAJORITY_AGREE`, `RELIABLE`.
- Semantic full revalidation was attempted immediately after the baseline, but the RPC disconnected while the SDK polled `eth_getTransactionByHash`. No definitive receipt was obtained, so no revalidation result is claimed.
- An earlier, broader semantic assumption reached `UNDETERMINED` / `NO_MAJORITY` at `0xa232d7409a4d46aaaf493e606c311f82e2c2750614c53040bf4abfa429cc48e0`.

## Steward rejection audit

- Database-only: **No.** Reliance is derived from accepted consensus findings.
- Monitoring-only: **No.** The protocol freezes decision context and adds replay, dependency impact, lineage, and a composable certificate.
- Provenance clone: **No.** Evidence identity supports the reliance result.
- Historical truth oracle: **No.** Replay evaluates a committed baseline under a new policy; it does not reconstruct arbitrary past truth.
- Model controls final state: **No.** Deterministic code controls status, lease, IDs, lineage, graph changes, and propagation.
- Shape-only validator: **No.** Validators independently retrieve evidence and evaluate reliance-critical fields.
- Fake/text-only web proof: **No for exact-text path.** Real browser rendering and the published heading were used in accepted canonical baseline/revalidation writes.
- Decorative graph: **No.** Canonical hard dependency, `NEEDS_REVIEW`, and completed bounded propagation were verified.
- Replay rewrites history: **No in implementation.** Direct Mode confirms the original capsule is unchanged after replay.
- Lease semantics: **Covered in Direct Mode.** Warning and due-time thresholds are tested.
- Temporary failure invalidates: **No.** Both Direct Mode and canonical unavailable-source baseline resulted in review, not invalidation.

## Remaining gate

Semantic-mode revalidation against live evidence still needs a definitive accepted receipt. The latest attempt ended at the RPC transport layer, so retry from the canonical address only after Studionet RPC availability is stable. Do not mark all four gates green, call the project finalized, or freeze until that and the final clean clone of the documentation/evidence commit pass.
