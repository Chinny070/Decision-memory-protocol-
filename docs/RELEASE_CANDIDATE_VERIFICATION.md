# Release candidate verification

## Candidate scope

This report is for the current local release candidate only. The deployment address recorded here is historical until the final committed source is redeployed and compared byte-for-byte.

## Local gate

- `pytest -q -p no:cacheprovider tests/direct`: 11 passed.
- Pickling/serialization checks: enabled in Direct Mode test setup.
- `genvm-lint check contracts/decision_memory.py`: passed, 3 checks (GenVM linter 0.11.0).
- `genvm-lint schema contracts/decision_memory.py`: passed, 22 methods (14 read, 8 write).
- `git diff --check`: passed before this report was added; rerun before commit.

## Hosted gate observations

- Earlier deployment `0xE7146a6556be0F9e5C5729F3660eAD91b50A573C` was `ACCEPTED` / `MAJORITY_AGREE`; its source predates the final source edits.
- A disposable Studionet run accepted baseline and full revalidation writes after real browser rendering. The literal was absent and the contract stored `CONTRADICTED` / `DEGRADED`.
- A semantic baseline reached `UNDETERMINED` / `NO_MAJORITY` after validators returned materially different findings.
- Counterfactual replay reached `UNDETERMINED` / `MAJORITY_DISAGREE`; no replay receipt exists for that attempt.
- The strict integration helper now treats only `ACCEPTED` and `MAJORITY_AGREE` as a successful write. The corrected source heading, negative case, challenge, and propagation still need live verification.

## Remaining release gates

1. Rerun hosted integration with the corrected literal and capture positive live render evidence.
2. Resolve or accurately retain the semantic and replay consensus disagreements; do not weaken substantive equivalence to force agreement.
3. Complete negative-source, challenge, and downstream propagation transactions.
4. Commit and push with valid GitHub authentication.
5. Deploy the final commit, retrieve source and schema, compare the exact deployed code blob with the commit, and verify the Explorer route.
6. Run the final clean-clone gate.

No four-gate submission pass or final freeze is claimed.
