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
| GenVM lint and SDK validation | `genvm-lint check contracts/decision_memory.py` | Passed: 3 checks on the deployed source commit. |
| ABI schema | `genvm-lint schema contracts/decision_memory.py` | Passed: 22 public methods (14 views, 8 writes). |
| Direct Mode | `pytest -q -p no:cacheprovider tests/direct` | 11 passed on the deployed source commit and on its clean clone. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Disposable hosted lifecycle | `gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet` | 1 passed with strict accepted-majority assertions across baseline, revalidation, replay, challenge, fail-closed source, and propagation. |
| Canonical lifecycle | `DMP_CANONICAL_ADDRESS=... gltest ...` plus resume test | Baseline/revalidation/replay/challenge/negative writes accepted. A transient RPC disconnect interrupted the SDK run while polling child registration; receipt was reconciled, and a separate resume test verified child `NEEDS_REVIEW` and completed `impact_4`. |
| Semantic live baseline | `gltest tests/integration/test_studionet_semantic.py -v -s --network studionet` | Focused claim reached `FINALIZED` / `MAJORITY_AGREE`, status `RELIABLE`. Following revalidation did not produce a definitive receipt because RPC disconnected while polling. |
| Canonical live source parity | `genlayer code` vs `git cat-file blob` | Exact deployed text matched commit `176136e`; normalized source SHA-256 `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`. |
| Clean clone | Clone commit `176136e`, rerun Direct Mode and GenVM checks | Passed: 11 Direct Mode tests; lint and schema green. Final documentation/test commit clone remains pending. |

## Test scope

Direct Mode covers registration, baseline, certificate output, exact-text render findings, forged-leader rejection, semantic re-fetch disagreement, selective revalidation scope, source failure, successor linkage, hard dependency invalidation and propagation, graph bounds, historical replay immutability, evidence-backed challenge, and lease boundaries. Direct Mode uses strict mocks and is not live consensus evidence.

The hosted run showed why transaction status checks are explicit: SDK success helpers may return for a non-accepted status. Integration helpers require both `status_name == ACCEPTED` and `result_name == MAJORITY_AGREE`. An initial canonical challenge transaction was `CANCELED` before validator rounds and is excluded. The canonical retry lifecycle succeeded through replay and challenge; a transport interruption during dependency setup was resolved through receipt lookup and a separate resume test. Semantic revalidation remains unverified because of a transport disconnect.
