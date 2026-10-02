# Verification record

## Toolchain observed

- Python 3.12.10
- `genlayer` CLI 0.39.1
- `genlayer-test` 0.29.2
- `genlayer-py` 0.16.3
- `genvm-linter` 0.11.0
- `pytest` 8.4.2

The contract pins the official `py-genlayer` SDK through the dependency header. Repository dependency pins are in `requirements.txt`.

## Gates

| Check | Command | Result |
| --- | --- | --- |
| GenVM lint and SDK validation | `genvm-lint check contracts/decision_memory.py` | Passed: 3 checks on current source. |
| ABI schema | `genvm-lint schema contracts/decision_memory.py` | Passed: 22 public methods (14 views, 8 writes); unchanged from previous source. |
| Direct Mode | `python -m pytest -q -p no:cacheprovider tests/direct` | Passed: 22 tests on current source. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Previous-source exact-text lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source semantic lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source hosted lifecycle | Prior Studionet run; see `SUBMISSION.md` | Historical accepted proofs describe only the previous contract source. |
| Previous-deployment semantic proof | Prior run, see `SUBMISSION.md` | Historical baseline reached `FINALIZED` / `MAJORITY_AGREE`, status `RELIABLE`; a separate prior revalidation attempt had no definitive receipt. Current-address successful semantic baseline and revalidation are recorded below. |
| Historical deployment parity (`0x9aF3...`) | GenLayer CLI code retrieval | Verified at the time for the superseded deployment only; current steward-fix deployment parity is recorded below. |
| Clean clone | GitHub commit `9d06206f62b4e89d0f8e2d0f5dbdf4962a0e2041`, cloned directly from `main` | `pip install --no-index -r requirements.txt` confirmed all pins were already installed; Direct Mode 21 passed, lint 3 checks passed, schema 22 methods passed. Dependencies used the shared installed Python environment, not an isolated virtual environment. |
| Isolated dependency bootstrap | Fresh `.venv-verification` using `python -m pip install -r requirements.txt` | Pinned dependencies installed, including `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, `genvm-linter==0.11.0`, and `pytest==8.4.2`. The wheel's Direct Mode loader needed a disposable local Windows temp-file cleanup compatibility patch; then 21 tests passed on the pre-steward-fix snapshot. Isolated lint passed 3 checks and schema remained 22 methods. |
| Historical Studionet lifecycle (`0x9aF3...`) | Earlier `gltest` run | Passed at the time for the previous contract source. Do not attribute this lifecycle result to the current `0xC3c...` deployment. |
| Historical semantic lifecycle (`0x9aF3...`) | Earlier `gltest` run | Historical proof for the superseded contract. Current steward-fix deployment semantic proofs are recorded in the section below. |

## Steward-requested semantic safety fix (current source)

- GitHub commit: `08addb48a6d554596fe9e5ef395e6ba1e5b3f7ff`; contract blob `ab348789bba2d2c5cd089c1774e6059942f5a55b`.
- Studionet contract: [`0xC3c63aB9459fd8BC87fa29161e2019F7d454B643`](https://explorer-studio.genlayer.com/address/0xC3c63aB9459fd8BC87fa29161e2019F7d454B643), deployed by `0x509b1314e9d6e96792427b135ba3c0260dcf1af3fb8b05fb0f234cf8ca81ec56` (`FINALIZED` / `MAJORITY_AGREE`).
- Deployed-source normalized SHA-256 parity: `eafa0b94585c0110889dd2cc3fdced1bc667853e74712eef6e4eef3933ffd699`.
- Direct adversarial test: `test_report_validation_rejects_incoherent_evidence_safety_fields` rejects contradictory combinations through both `_valid_report` paths and confirms the reliable baseline remains unchanged. It covers insufficient evidence paired with `SUPPORTED/NO_MATERIAL_CHANGE`, external failure paired with supported findings, false unavailable typing, and unsupported critical conflict.
- Current-source checks: 22 Direct Mode tests passed; GenVM lint passed 3 checks; ABI schema passed at 22 methods (14 view, 8 write).
- Current-address semantic baseline `0xda093eb850af5749a1f7daacea71363da4beb4f26cdf7804f7aeb6c37d07bd66` and full revalidation `0x5e255e514f4acd1473b10437de5a959c19a2736fbe34f18ee69aae61efed01ba` both finalized with `MAJORITY_AGREE`; both reliance statuses were `RELIABLE`.
- Earlier partial current-address lifecycle attempt: registration `0x098aff02c9b44e0f30af89a90470b4e09255181a559cd51f790274c04055560a`, baseline `0x159ff207f1d3882c6a57ed36d904937a4c535bf9052524271c4db1bb83b8f22b`, revalidation `0x726eea5970fc293d90c22c09bb4b07de56271e207991ac8772d8ce31c0d44829`, replay `0x6725d35b168cf146d30a1bc82e06a5ae51c1c576773fb4f857421fcecf7d5660`, challenge `0x2744efafba49679ff344902b1c629d3e8c9d5ffd0572099f604ef5d70d8fea91`. These five writes finalized; that attempt then stopped on RPC HTTP 502 and did not complete the later checks. It is not counted as a full lifecycle pass.

## Current-address full lifecycle transaction record

Network: GenLayer Studionet. Contract: [`0xC3c63aB9459fd8BC87fa29161e2019F7d454B643`](https://explorer-studio.genlayer.com/address/0xC3c63aB9459fd8BC87fa29161e2019F7d454B643). Every write below finalized with `MAJORITY_AGREE`.

| Lifecycle step | Transaction | Verified result |
| --- | --- | --- |
| Register exact-text decision `live-docs-25004` | `0xc56ed42ac33a1c2c11f94c00b109e4c2a61112971dba3b4715d6510e52740599` | `FINALIZED` / `MAJORITY_AGREE` |
| Browser-render baseline | `0x915cfa880c1bc372120b92314ef96f56a33a5dedc2a77178e1b556e53e7b07e8` | `FINALIZED`; `RELIABLE` |
| Full revalidation | `0xef8e87e0e8bf34c1612168eabafe655510f8c76ac53b24ce4d9f88c7d6a42eec` | `FINALIZED`; `RELIABLE` |
| Counterfactual replay | `0x51ba1cef592201cfca9924f11a1c3702f061201b547e03439c62ebea916da2fb` | `FINALIZED` / `MAJORITY_AGREE`; `WOULD_REQUIRE_REVIEW`; original definition hash unchanged |
| Evidence-backed challenge | `0x62255b0b36baf1be35e4de71fbbad8d5d4056098de0f948c67285c6dd2e57de1` | `FINALIZED`; `UPHELD` |
| Register unavailable-source decision | `0xc91a373b6897c7c293761730ac6f719dfcfe7ebca684d34214f60a5a66bace79` | `FINALIZED` / `MAJORITY_AGREE` |
| Unavailable-source baseline | `0x2e609db58db4df488b0802d6fae29d84330ba307bc69d59fafcdcb514e9a89b6` | `FINALIZED`; `NEEDS_REVIEW`, not `RELIABLE` or `INVALIDATED` |
| Register hard-dependent decision | `0x45d00a78ae910b44775125d6507fe0ce90709a3582e760d9864113a3ee25fd66` | `FINALIZED` / `MAJORITY_AGREE` |
| Hard-dependent baseline | `0xec131dada083a07853f823af9b75d3a623b58091b955db6a5fcf72e43d728916` | `FINALIZED`; dependent status reviewable |
| Bounded impact propagation | `0x35ca1a26b3d6e89a179208d7e56a11d9960e4c45071f9037dae6c1173890014e` | `FINALIZED` / `MAJORITY_AGREE`; `impact_4` complete |

The command `gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet` passed (`1 passed`) in 519.20 seconds. The helper bounds HTTP request timeouts, retries transient reads only, and never retries transaction submissions. One earlier attempt was interrupted by an RPC connection failure and is not counted.

## Test scope

Direct Mode covers the protocol lifecycle and adversarial regressions for frozen EXACT_TEXT source authority, selected-source availability, retrieval-kind preservation, ambiguous markers, successor authorization through both entry points, forged content/render hashes, exact replay enum consensus, duplicate challenge identity/quota, in addition to registration, baseline, selective revalidation, source failure, dependency, replay immutability, and lease checks. Direct Mode uses strict mocks and is not live consensus evidence.

## Adversarial test additions

- `test_exact_text_challenge_rejects_unregistered_evidence_authority`: attacker URL is rejected before consensus without creating challenge state; a registered frozen URL can be challenged.
- `test_exact_text_challenge_can_recheck_frozen_registered_source`: disappearance of the marker on the registered source contradicts the assumption.
- `test_exact_text_challenge_unavailable_source_is_external_failure_not_contradiction`: unavailable URL produces `UNAVAILABLE` / `EXTERNAL_FAILURE`, insufficient evidence, and no invalidation.
- `test_exact_text_challenge_availability_is_scoped_to_selected_source`: source A remains available while challenged source B is unavailable; B remains `UNAVAILABLE` / `EXTERNAL_FAILURE`.
- `test_exact_text_challenge_preserves_registered_retrieval_kind`: challenge uses the selected frozen source's retrieval kind.
- `test_exact_text_multiple_sources_reject_ambiguous_frozen_markers`: inconsistent registered criteria are rejected.
- `test_successor_linkage_is_authorized_at_registration_boundary`: creator succeeds, unrelated direct and helper attempts fail without occupying the slot, and only one successor is allowed.
- `test_validator_rejects_forged_content_and_render_hashes`: each evidence digest is independently bound.
- `test_replay_validator_requires_exact_typed_outcome_but_ignores_explanation_digest`: enum disagreement fails while explanation variance passes.
- `test_duplicate_challenge_rejected_without_consuming_quota_and_distinct_challenges_work`: exact duplicate is free of quota impact, distinct challenges count, and the cap holds.

The pinned `genlayer-test==0.29.2` and `genlayer-py==0.16.3` expose `transact(wait_transaction_status=TransactionStatus.FINALIZED, wait_interval=3000, wait_retries=50)`. The lifecycle helper requests FINALIZED explicitly with a bounded 150-second wait and requires `FINALIZED` plus `MAJORITY_AGREE` before dependent reads. Read-only RPC polling retries transient transport failures and gateway responses with bounded timeouts; transaction submissions are not retried. The successful run below used this helper against the current deployment. Earlier runs experienced transient RPC DNS/reset errors and are not counted as successful runs.

## Historical Studionet lifecycle on superseded `0x9aF3...` deployment

Network: GenLayer Studionet (`https://studio.genlayer.com/api`). Canonical contract: [`0x9aF3aa61bEF38Abb597d7078F36659CBaFd65610`](https://explorer-studio.genlayer.com/address/0x9aF3aa61bEF38Abb597d7078F36659CBaFd65610). Deployment transaction: `0x20b1ff738043da829594a4e0f3f5311beafe5f4d06996ff4bb231891ef53206b`.

| Lifecycle step | Transaction | Verified result |
| --- | --- | --- |
| Register primary decision | `0xf2b5933041e2986a5712636e90fec80739379e10c72255d6668f8980c74b3848` | `FINALIZED` / `MAJORITY_AGREE` |
| Browser-render baseline | `0xd46f6792cb837a26b9b6d0712d21a6f59e2d8a91c7ef7bb4009313798afe13bd` | `FINALIZED`; reliance `RELIABLE` |
| Full revalidation | `0x2ec2a9c8f07479bf22c758bd1ecd58138f38dcb948ea850b1838d43d7707e03b` | `FINALIZED`; reliance `RELIABLE` |
| Counterfactual replay | `0xf6f71b704d083f95c83642fc32be6c520f2af0e4ff8887517d63a9260524bbca` | `FINALIZED` / `MAJORITY_AGREE`; `WOULD_REQUIRE_REVIEW`; original definition hash unchanged |
| Evidence-backed challenge | `0xb6be1e7b45d4932c64414bc1c91b7ee0f9ad98205cf18f4a85c233a39a6f32d0` | `FINALIZED`; `UPHELD` |
| Register unavailable-source decision | `0x2e05fe495ad1fe6e445f9c351898c4e8b6265f48b7eb5e28c4334b68fd709740` | `FINALIZED` / `MAJORITY_AGREE` |
| Unavailable-source baseline | `0x05ccfea5824271cf95b3d3722879eb84cb4bb7840ef85f01403ec087941f9d81` | `FINALIZED`; `NEEDS_REVIEW`, not `INVALIDATED` |
| Register hard-dependent decision | `0x62b34f884626c9b8dbfaa2237e360967bed2e593cc512a0d6e88e6d08af38a64` | `FINALIZED` / `MAJORITY_AGREE` |
| Dependent baseline | `0x9b2a889ea55f47d2da91b506020b84fc31b3d12c75acdc2b3fdd643bdb86a6cb` | `FINALIZED`; dependent status was reviewable |
| Bounded impact propagation | `0x43304ae53af6c1760719d01330a2850ca2dd9cff8b156dc83e8f2a5de72d415f` | `FINALIZED` / `MAJORITY_AGREE`; `impact_5` complete |

The integration command completed with `1 passed` in 484.53 seconds. It emitted one pytest cache permission warning; this did not affect the test result. The exact-text evidence used the frozen registered official documentation URL and `WEB_RENDER_HTML` retrieval.

The semantic integration command completed with `1 passed` in 229.91 seconds. Its successful run used a fresh decision, exact official-docs source URL, semantic assumption, bounded `FINALIZED` waits, and read-only RPC retries. The first attempt's revalidation transaction `0x35408d2d99c5e448d5057840cb7ecb2a8a77fe294321c91ea8b21c79fb8f2486` ended `CANCELED` / `NO_MAJORITY`; it is explicitly excluded from successful evidence. The passing helper retries only when the prior receipt is terminally canceled, never when transaction status is unknown.
