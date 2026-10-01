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
| GenVM lint and SDK validation | `genvm-lint check contracts/decision_memory.py` | Passed in this workspace; rerun after final edits. |
| ABI schema | `genvm-lint schema contracts/decision_memory.py` | Extracts 22 public methods; rerun after final edits. |
| Direct Mode | `pytest -q tests/direct` | 11 tests; rerun after final edits. |
| Pickling | Direct Mode `VMContext.check_pickling = True` | Enabled in tests; result is part of final run. |
| Hosted Studionet integration | `gltest tests/integration/ -v -s --network studionet` | 1 passed on 2026-10-01 with strict `ACCEPTED` + `MAJORITY_AGREE` checks. Real render baseline/revalidation were `RELIABLE`; replay `WOULD_REQUIRE_REVIEW`; challenge `OVERTURNED`; source failure `NEEDS_REVIEW`; hard dependency propagation complete. Semantic mode separately ended `UNDETERMINED` / `NO_MAJORITY`. |
| Canonical live source parity | Compare deployed source with final branch blob | Earlier candidate deployment and schema were verified; final edits followed that deployment, so parity is pending a final-source redeploy. |
| Clean clone | Clone the intended pushed commit, reinstall pins, rerun local checks | Pending commit and push. |

## Test scope

Direct Mode covers registration, baseline, certificate output, exact-text render findings, forged-leader rejection, semantic re-fetch disagreement, selective revalidation scope, source failure, successor linkage, hard dependency invalidation and propagation, graph bounds, historical replay immutability, evidence-backed challenge, and lease boundaries. Direct Mode uses strict mocks and is not live consensus evidence.

The hosted run showed why transaction status checks are explicit: SDK success helpers may return for a non-accepted status. The integration helper now requires both `status_name == ACCEPTED` and `result_name == MAJORITY_AGREE`. The semantic baseline reached `NO_MAJORITY` because validators made materially different judgments; that outcome is recorded as a failed live proof. The successful lifecycle was executed against a disposable test deployment, not the canonical address.
