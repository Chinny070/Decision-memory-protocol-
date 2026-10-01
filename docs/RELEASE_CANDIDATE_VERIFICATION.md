# Release candidate verification

## Contract source commit

- Commit: `176136ee1bb507aee8aa86673741ee9d8792500d`.
- Direct Mode: 11 passed.
- Pickling/serialization: enabled in Direct Mode tests.
- GenVM linter 0.11.0: 3 checks passed.
- GenVM schema: 22 methods (14 read, 8 write).
- Clean clone of this source commit: Direct Mode, lint, and schema passed.

## Canonical deployment

- Studionet contract: `0xC25E6be425d940BB4b794932b1226D4bccD21824`.
- Deploy transaction: `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`, `ACCEPTED` / `MAJORITY_AGREE`.
- Deployed ABI: 22 methods.
- Explorer address and transaction pages: HTTP 200; address/hash present.
- Retrieved code equals the Git blob at the contract source commit; normalized SHA-256 `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`.

## Live proofs

- Canonical exact-text baseline and full revalidation: `RELIABLE`.
- Canonical counterfactual replay: `WOULD_REQUIRE_REVIEW`; original certificate unchanged.
- Canonical evidence-backed challenge: `OVERTURNED`.
- Canonical unavailable-source baseline: `NEEDS_REVIEW`, not invalidated.
- Canonical hard-dependent baseline: `NEEDS_REVIEW`; propagation event `impact_4` complete, transaction `0xa6bc9ffb153cf8e82fa449c0a0a9d72b7b7dff68919f4300631ddfad56a94376` `FINALIZED` / `MAJORITY_AGREE`.
- Focused semantic baseline: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`.
- Semantic revalidation attempt: no definitive receipt; the RPC disconnected while polling.
- An earlier broad semantic baseline reached `UNDETERMINED` / `NO_MAJORITY`.

## Remaining release gate

The source, deployment, exact-text live lifecycle, and clean clone are verified. Semantic-mode revalidation against live evidence still needs a definitive accepted receipt. A documentation/tests-only commit is being prepared after these checks; rerun the clean-clone gate from that final repository commit before claiming all gates green. `SUBMISSION.md` holds the complete transaction ledger and accurately limits claims.
