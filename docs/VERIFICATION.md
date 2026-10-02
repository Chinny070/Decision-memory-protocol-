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
| Direct Mode | `python -m pytest -q -p no:cacheprovider tests/direct` | Passed: 20 tests on current source. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Previous-source exact-text lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source semantic lifecycle | Prior Studionet run; see `SUBMISSION.md` | Passed against `0x81F5...`; address does not contain current source changes. |
| Previous-source hosted lifecycle | Prior Studionet run; see `SUBMISSION.md` | Historical accepted proofs describe only the previous contract source. |
| Semantic live baseline | Prior run, see `SUBMISSION.md` | Focused claim reached `FINALIZED` / `MAJORITY_AGREE`, status `RELIABLE`. Following revalidation had no definitive receipt. |
| Current-source deployment parity | GenLayer CLI code retrieval, see `docs/DEPLOYMENT.md` | Verified exact normalized source match; SHA-256 `a5fed29ee04bb9da09a188712108420ef03472fe3062b745c553b860470c2aa1`. Deployment tx `0x20b1ff738043da829594a4e0f3f5311beafe5f4d06996ff4bb231891ef53206b` is `FINALIZED` / `MAJORITY_AGREE`. |
| Clean clone | Temporary candidate repository commit `f8919a885dcd24bcabda5e03d51c8b9c77175062`, cloned locally from the current tracked working-tree contents | `pip install --no-index -r requirements.txt` confirmed all pins installed; Direct Mode 20 passed, lint 3 checks passed, schema 22 methods passed. This temporary commit is not a commit in the workspace repository because its `.git` is read-only. |

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

The pinned `genlayer-test==0.29.2` and `genlayer-py==0.16.3` expose `transact(wait_transaction_status=TransactionStatus.FINALIZED, wait_interval=3000, wait_retries=50)`. The lifecycle helper now requests FINALIZED explicitly with a bounded 150-second wait and requires `FINALIZED` plus `MAJORITY_AGREE` before dependent reads. A timeout or terminal non-final outcome raises and cannot count as success. This helper change and application lifecycle have not yet been exercised against the new Studionet address. Historical lifecycle proofs at `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71` apply only to the previous source. Current deployment receipt and source parity are verified.
