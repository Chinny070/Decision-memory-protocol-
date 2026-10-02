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
| Direct Mode | `python -m pytest -q -p no:cacheprovider tests/direct` | Passed: 21 tests on current source. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Previous-source exact-text lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source semantic lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source hosted lifecycle | Prior Studionet run; see `SUBMISSION.md` | Historical accepted proofs describe only the previous contract source. |
| Previous-deployment semantic proof | Prior run, see `SUBMISSION.md` | Historical baseline reached `FINALIZED` / `MAJORITY_AGREE`, status `RELIABLE`; a separate prior revalidation attempt had no definitive receipt. Current-address successful semantic baseline and revalidation are recorded below. |
| Current-source deployment parity | GenLayer CLI code retrieval, see `docs/DEPLOYMENT.md` | Verified exact normalized source match; SHA-256 `a5fed29ee04bb9da09a188712108420ef03472fe3062b745c553b860470c2aa1`. Deployment tx `0x20b1ff738043da829594a4e0f3f5311beafe5f4d06996ff4bb231891ef53206b` is `FINALIZED` / `MAJORITY_AGREE`. |
| Clean clone | GitHub commit `9d06206f62b4e89d0f8e2d0f5dbdf4962a0e2041`, cloned directly from `main` | `pip install --no-index -r requirements.txt` confirmed all pins were already installed; Direct Mode 21 passed, lint 3 checks passed, schema 22 methods passed. Dependencies used the shared installed Python environment, not an isolated virtual environment. |
| Isolated dependency bootstrap | Fresh `.venv-verification` using `python -m pip install -r requirements.txt` | Pinned dependencies installed, including `genlayer-test==0.29.2`, `genlayer-py==0.16.3`, `genvm-linter==0.11.0`, and `pytest==8.4.2`. The wheel's Direct Mode loader needed a disposable local Windows temp-file cleanup compatibility patch; then 21 tests passed. Isolated lint passed 3 checks and schema remained 22 methods. |
| Current-source Studionet lifecycle | Canonical address `0x9aF3aa61bEF38Abb597d7078F36659CBaFd65610`; `gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet` | Passed: 1 integration test, 10 lifecycle transactions `FINALIZED` / `MAJORITY_AGREE`; baseline and full revalidation `RELIABLE`, replay `WOULD_REQUIRE_REVIEW`, challenge `UPHELD`, unavailable evidence `NEEDS_REVIEW`, dependent status reviewable, bounded impact `impact_5` complete. Hashes below. |
| Current-source semantic lifecycle | Same canonical address; `gltest tests/integration/test_studionet_semantic.py -v -s --network studionet` | Passed: baseline and full semantic revalidation both `FINALIZED` / `MAJORITY_AGREE`, and both reported `RELIABLE`. Baseline `0xd61a3efdde33e445da32becc2c792f4347079485b68a277b17b0b321185dad3d`; revalidation `0x3fb37f4492408cc9268445f6e0b283a8be266105ecdc876dc59f263ba50cb1b8`. One earlier revalidation transaction ended `CANCELED` / `NO_MAJORITY` and is not counted as success. |

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

The pinned `genlayer-test==0.29.2` and `genlayer-py==0.16.3` expose `transact(wait_transaction_status=TransactionStatus.FINALIZED, wait_interval=3000, wait_retries=50)`. The lifecycle helper requests FINALIZED explicitly with a bounded 150-second wait and requires `FINALIZED` plus `MAJORITY_AGREE` before dependent reads. Read-only RPC polling retries transient transport failures; transaction submissions are not retried. The successful run below used this helper against the current deployment. Earlier runs experienced transient RPC DNS/reset errors and are not counted as successful runs.

## Current-source Studionet lifecycle

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
