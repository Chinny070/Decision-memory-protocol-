# Submission readiness ledger

**Submission title:** Decision Memory Protocol â€” evidence-backed decision reliance and revalidation

## Current source security update

The current repository source includes targeted fixes for EXACT_TEXT challenge marker substitution, predecessor successor-slot authorization, evidence render/content hash validator binding, replay exact-enum consensus, and duplicate challenge quota exhaustion. `python -m pytest -q tests/direct` passes 17 tests; `genvm-lint check` passes 3 checks; `genvm-lint schema` generates the 22-method ABI. Security details are in `docs/SECURITY.md`, consensus behavior in `docs/CONSENSUS.md`, and test details in `docs/VERIFICATION.md`.

**Current deployment:** `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71`, transaction `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`, `FINALIZED` / `MAJORITY_AGREE`. Deployed-source parity is verified against source commit `2ae77cfca02bb81f770aa4e1838a846260decafa` (blob `d7993a030b372d0e7debb51c7d01842b77d10171`, SHA-256 `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`). Current-source lifecycle tests remain outstanding; old lifecycle records belong to the previous address.

## Current deployment details

- Studionet address: `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71`.
- Deployment transaction: `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`, `FINALIZED` / `MAJORITY_AGREE`.
- Deployed-source parity: exact match; normalized source SHA-256 `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`.
- Schema: 22 methods (14 views, 8 writes).
- The old address `0xC25E6be425d940BB4b794932b1226D4bccD21824` and its lifecycle transactions describe pre-fix source only.

## Four gates

| Gate | Status | Evidence |
| --- | --- | --- |
| Contract / runtime | Partial | 17 current-source Direct Mode tests and GenVM lint/schema pass; no clean clone of the security-fix commit is recorded yet. |
| Real consensus | Partial / not green | The previous deployment’s exact-text baseline, full revalidation, replay, challenge, failure handling, and dependency propagation reached accepted majority consensus; the new deployment’s lifecycle has not yet been exercised. A focused semantic-mode baseline on the previous deployment also reached accepted majority consensus; its full revalidation was interrupted by an RPC disconnect before a receipt was obtained. |
| Real evidence | Partial | The previous deployment’s browser-rendered official documentation established a reliable exact-text baseline and revalidation; no current-source live evidence result is claimed. Semantic interpretation has a live reliable baseline; semantic revalidation and material drift under LLM judgment remain unproven. |
| Steward fit | Partial | Rejection audit and DM1â€“DM15 map are documented. Previous-deployment dependency propagation completed. Semantic-mode revalidation and final clean clone of the evidence-documentation commit remain outstanding. |

## Submission copy (not final until all gates clear)

- **Category:** Standalone reusable GenLayer Intelligent Contract.
- **Title:** Decision Memory Protocol â€” immutable decision context, semantic revalidation, counterfactual replay, and dependency-aware reliance.
- **One-line thesis:** Preserves why a decision was defensible, revalidates its assumptions against evidence, and deterministically propagates reliance changes without rewriting history.
- **Repository:** https://github.com/Chinny070/Decision-memory-protocol-
- **Current Studionet address:** [0x81F5dE555814a8C48Da2FeC654Df40a616b64e71](https://explorer-studio.genlayer.com/address/0x81F5dE555814a8C48Da2FeC654Df40a616b64e71)
- **Deployment transaction:** `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`, `FINALIZED`, `MAJORITY_AGREE`.
- **Deployment source commit:** contract source from `2ae77cfca02bb81f770aa4e1838a846260decafa`.
- **Why GenLayer:** Validators independently retrieve and interpret external evidence; one creator, API, or model must not author reliance alone.
- **Consensus mechanism:** Custom leader/validator nondeterministic evaluation with typed substantive equivalence; deterministic code derives reliance and graph effects.
- **Failure policy:** Insufficient evidence, source failure, or consensus disagreement never creates affirmative reliance; transaction-level disagreement is not an application status.
- **Reuse surface:** `get_reliance_certificate`, `get_reliance_status`, `is_reliable`, plus bounded lifecycle writes.
- **Verified local checks:** 17 Direct Mode tests; 3 GenVM lint checks; 22-method schema; deployed source parity verified for the security-fix commit.
- **Verified live checks:** Deployment receipt, schema, and source parity verified for the new address. The lifecycle transactions below belong to the previous address. Its semantic baseline passed; semantic revalidation was interrupted by an RPC disconnect.
- **Reviewer fast path:** `README.md`, `DECISION.md`, `docs/ARCHITECTURE.md`, `docs/INVARIANTS.md`, `docs/CONSENSUS.md`, and `docs/RELEASE_CANDIDATE_VERIFICATION.md`.
- **Portal description:** Decision Memory Protocol is a reusable GenLayer Intelligent Contract that preserves decision context and critical assumptions, revalidates them against independently retrieved evidence, and gives downstream contracts a machine-readable reliance certificate. Validators independently assess external evidence; deterministic contract logic derives reliance state, lease freshness, successor lineage, and bounded dependency impact. It includes immutable counterfactual replay and fail-closed evidence handling. Direct Mode, GenVM validation, and a pre-fix exact-text lifecycle passed on the previous deployment; current-source live lifecycle remains outstanding. Semantic-mode live baseline passes; full semantic revalidation and final clean-clone verification remain open.

## Previous deployment and source parity (pre-fix)

- Network: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- CLI: `genlayer` 0.39.1; deployer public address `0xaffe15eec45b68835cc9e5b4ab85dd5deae8e70b`.
- Previous contract: `0xC25E6be425d940BB4b794932b1226D4bccD21824`.
- Previous deployment transaction: `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`, `ACCEPTED` / `MAJORITY_AGREE`.
- Previous Explorer address: https://explorer-studio.genlayer.com/address/0xC25E6be425d940BB4b794932b1226D4bccD21824 (HTTP 200; address found in page).
- Explorer transaction: https://explorer-studio.genlayer.com/tx/0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac (HTTP 200; transaction hash found in page).
- Deployed schema: 22 methods (14 views, 8 writes).
- Contract blob at source commit: `73007b3208992af1cb333bc6605861d99b8fa67b` (Git blob SHA-1).
- Deployed source normalized-text SHA-256: `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`.
- Source parity: verified. The source returned by `genlayer code` exactly matched the decoded Git blob after removing only CLI display framing newlines; normalized content hashes matched.

## Previous-source Studionet lifecycle evidence

The successful pre-fix lifecycle used decision prefix `live-docs-10892` on the previous contract, not the current deployment. Each accepted transaction below reached `MAJORITY_AGREE` unless noted.

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

## Previous-source semantic-mode live proof

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
- Fake/text-only web proof: **No for exact-text path.** Real browser rendering and the published heading were used in accepted pre-fix baseline/revalidation writes on the previous deployment.
- Decorative graph: **No.** Canonical hard dependency, `NEEDS_REVIEW`, and completed bounded propagation were verified.
- Replay rewrites history: **No in implementation.** Direct Mode confirms the original capsule is unchanged after replay.
- Lease semantics: **Covered in Direct Mode.** Warning and due-time thresholds are tested.
- Temporary failure invalidates: **No.** Both Direct Mode and previous-deployment unavailable-source baseline resulted in review, not invalidation.

## Remaining gate

Semantic-mode revalidation against live evidence still needs a definitive accepted receipt. That attempt and all listed lifecycle proofs concern the previous address/source. The new deployment has verified receipt, schema, and source parity, but current-source lifecycle proofs and a clean clone of the final repository commit remain outstanding. Do not mark all four gates green or call the project finalized until those gates pass.
