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
| GenVM lint and SDK validation | `genvm-lint check contracts/decision_memory.py` | Passed: 3 checks on the current security-corrected source. |
| ABI schema | `genvm-lint schema contracts/decision_memory.py` | Passed: 22 public methods (14 views, 8 writes) on current source. |
| Direct Mode | `pytest -q -p no:cacheprovider tests/direct` | 17 passed on the current security-corrected source. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Previous-source hosted lifecycle | Prior Studionet run; see `SUBMISSION.md` | Accepted live proofs describe only the previous contract source; not rerun after security changes. |
| Semantic live baseline | Prior run, see `SUBMISSION.md` | Focused claim reached `FINALIZED` / `MAJORITY_AGREE`, status `RELIABLE`. Following revalidation had no definitive receipt. |
| Current source parity | New deployment, see `docs/DEPLOYMENT.md` | Exact source match verified against commit `2ae77cf`; normalized SHA-256 `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`. |
| Clean clone | Clean clone of current fix commit | Not run. Earlier clean-clone checks apply only to pre-fix source. |

## Test scope

Direct Mode covers the prior protocol lifecycle and adversarial regressions for frozen EXACT_TEXT challenges and ambiguous markers, successor authorization through both entry points, forged content/render hashes, exact replay enum consensus, duplicate challenge identity/quota, in addition to existing registration, baseline, selective revalidation, source failure, dependency, replay immutability, and lease checks. Direct Mode uses strict mocks and is not live consensus evidence.

## Adversarial test additions

- `test_exact_text_challenge_cannot_replace_frozen_marker_and_legitimate_challenge_works`: attacker ground cannot restore support; a new source containing frozen text can.
- `test_exact_text_multiple_sources_reject_ambiguous_frozen_markers`: inconsistent registered criteria are rejected.
- `test_successor_linkage_is_authorized_at_registration_boundary`: creator succeeds, unrelated direct and helper attempts fail without occupying the slot, and only one successor is allowed.
- `test_validator_rejects_forged_content_and_render_hashes`: each evidence digest is independently bound.
- `test_replay_validator_requires_exact_typed_outcome_but_ignores_explanation_digest`: enum disagreement fails while explanation variance passes.
- `test_duplicate_challenge_rejected_without_consuming_quota_and_distinct_challenges_work`: exact duplicate is free of quota impact, distinct challenges count, and the cap holds.

The hosted run showed why transaction status checks are explicit: SDK success helpers may return for a non-accepted status. Integration helpers require both `status_name == ACCEPTED` and `result_name == MAJORITY_AGREE`. An initial canonical challenge transaction was `CANCELED` before validator rounds and is excluded. The canonical retry lifecycle succeeded through replay and challenge; a transport interruption during dependency setup was resolved through receipt lookup and a separate resume test. Semantic revalidation remains unverified because of a transport disconnect. The old lifecycle proofs in `SUBMISSION.md` describe the previous deployment. Current source has now been deployed to `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71` with verified receipt, schema, and source parity; current-source lifecycle proofs remain outstanding.
