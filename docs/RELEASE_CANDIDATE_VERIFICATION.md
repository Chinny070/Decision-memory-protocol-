# Release candidate verification

## Contract source commit

- Previous deployed-source commit: `176136ee1bb507aee8aa86673741ee9d8792500d`.
- Security-fix source commit: `2ae77cfca02bb81f770aa4e1838a846260decafa`.
- Current security-fix source commit `2ae77cfca02bb81f770aa4e1838a846260decafa`: 17 Direct Mode tests passed (includes adversarial security regressions).
- Pickling/serialization: enabled in Direct Mode tests.
- GenVM linter 0.11.0: 3 checks passed.
- GenVM schema: 22 methods (14 read, 8 write).
- Clean clone applies only to the previous pre-fix source; current security-fix source clean-clone validation has not been run.

## Current deployment (security-fix source)

- Studionet contract: `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71`.
- Deploy transaction: `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`, `FINALIZED` / `MAJORITY_AGREE`.
- Schema: 22 methods (14 views, 8 writes).
- Retrieved source exact match: blob `d7993a030b372d0e7debb51c7d01842b77d10171`; normalized SHA-256 `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`.
- Explorer address and transaction pages: HTTP 200; address/hash present.
- Current-source exact-text lifecycle: 1 passed (baseline, full revalidation, replay, challenge, unavailable-source fail-closed, dependency propagation).
- Current-source semantic lifecycle: 1 passed (baseline and full revalidation reliable).
- One earlier replay attempt returned `UNDETERMINED`; the successful subsequent replay is recorded in `SUBMISSION.md`.

## Previous deployment (pre-fix source)

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

Current security-fix source is deployed with verified parity. Local Direct Mode tests, lint, schema, current-source exact-text lifecycle, and semantic baseline/full revalidation passed. One initial replay attempt was `UNDETERMINED`; a subsequent replay reached accepted majority. Current-source semantic material-drift proof and a clean clone of the final documentation/evidence commit remain outstanding. Previous-deployment evidence is historical only. `SUBMISSION.md` holds the complete transaction ledger and accurately limits claims.
