# Release candidate verification

## Contract source commit

- Previous deployed-source commit: `176136ee1bb507aee8aa86673741ee9d8792500d`.
- Security-fix source commit: `2ae77cfca02bb81f770aa4e1838a846260decafa`.
- Previous security-fix source commit `2ae77cfca02bb81f770aa4e1838a846260decafa`: 17 Direct Mode tests passed (includes adversarial security regressions).
- Current source: 22 Direct Mode tests passed; GenVM lint passed 3 checks; schema unchanged at 22 methods (14 read, 8 write).
- Pickling/serialization: enabled in Direct Mode tests.
- GenVM linter 0.11.0: 3 checks passed.
- GenVM schema: 22 methods (14 read, 8 write).
- Clean clone: GitHub commit `9d06206f62b4e89d0f8e2d0f5dbdf4962a0e2041` cloned directly from `main`; requirements resolved from already installed pins, 21 Direct Mode tests passed (pre-steward-fix snapshot), lint passed 3 checks, and schema stayed at 22 methods.

## Current deployment (steward semantic-safety fix)

- Studionet contract: `0xC3c63aB9459fd8BC87fa29161e2019F7d454B643`.
- Deploy transaction: `0x509b1314e9d6e96792427b135ba3c0260dcf1af3fb8b05fb0f234cf8ca81ec56`, `FINALIZED` / `MAJORITY_AGREE`.
- Schema: 22 methods (14 views, 8 writes).
- Retrieved source exact match: normalized SHA-256 `eafa0b94585c0110889dd2cc3fdced1bc667853e74712eef6e4eef3933ffd699`; local blob `ab348789bba2d2c5cd089c1774e6059942f5a55b`.
- The current address has finalized semantic baseline and full revalidation. A broader lifecycle run finalized through replay and challenge, then receipt polling received RPC HTTP 502; unavailable-source and dependency propagation are not claimed for this address.
- Current-source semantic baseline and full revalidation both finalized with `MAJORITY_AGREE` and `RELIABLE`; transaction hashes are in `docs/VERIFICATION.md`. The Direct Mode adversarial suite includes the steward-requested conflicting-field test.
- Contract source matches blob `ab348789bba2d2c5cd089c1774e6059942f5a55b` in GitHub `main` commit `08addb48a6d554596fe9e5ef395e6ba1e5b3f7ff`.

## Previous deployment (earlier security-fix source)

- Studionet contract: `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71`.
- Deploy transaction: `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`, `FINALIZED` / `MAJORITY_AGREE`.
- Schema: 22 methods (14 views, 8 writes).
- Retrieved source exact match: blob `d7993a030b372d0e7debb51c7d01842b77d10171`; normalized SHA-256 `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`.
- Explorer address and transaction pages: HTTP 200; address/hash present.
- Exact-text lifecycle: historical proof against this previous source only.
- Semantic lifecycle: historical proof against this previous source only.
- One earlier replay attempt returned `UNDETERMINED`; the successful subsequent replay is recorded in `SUBMISSION.md`.

## Previous deployment (pre-fix source)

- Studionet contract: `0xC25E6be425d940BB4b794932b1226D4bccD21824`.
- Deploy transaction: `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`, `ACCEPTED` / `MAJORITY_AGREE`.
- Deployed ABI: 22 methods.
- Explorer address and transaction pages: HTTP 200; address/hash present.
- Retrieved code equals the Git blob at the contract source commit; normalized SHA-256 `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`.

## Live proofs

- Historical `0x9aF3...` semantic baseline: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`, transaction `0xd61a3efdde33e445da32becc2c792f4347079485b68a277b17b0b321185dad3d`.
- Historical `0x9aF3...` semantic full revalidation: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`, transaction `0x3fb37f4492408cc9268445f6e0b283a8be266105ecdc876dc59f263ba50cb1b8`.
- Historical `0x9aF3...` exact-text baseline and full revalidation: both `RELIABLE`.
- Current `0xC3c...` semantic baseline/revalidation, replay, and challenge are finalized; broader run stopped on RPC 502 before current-address unavailable-source and dependency-propagation proofs.

### Historical previous-address proofs

- Previous-address exact-text baseline and full revalidation: `RELIABLE`.
- Previous-address counterfactual replay: `WOULD_REQUIRE_REVIEW`; original certificate unchanged.
- Previous-address evidence-backed challenge: `OVERTURNED`.
- Previous-address unavailable-source baseline: `NEEDS_REVIEW`, not invalidated.
- Previous-address hard-dependent baseline: `NEEDS_REVIEW`; propagation event `impact_4` complete, transaction `0xa6bc9ffb153cf8e82fa449c0a0a9d72b7b7dff68919f4300631ddfad56a94376` `FINALIZED` / `MAJORITY_AGREE`.
- Previous-address focused semantic baseline: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`.
- Historical previous-address semantic revalidation attempt: no definitive receipt; the RPC disconnected while polling. A later previous-address proof and current-address semantic proof are recorded elsewhere in this document and `SUBMISSION.md`.
- An earlier broad semantic baseline reached `UNDETERMINED` / `NO_MAJORITY`.

## Remaining release gate

The steward-fix deployment and exact source parity are verified; see the current deployment details in `docs/DEPLOYMENT.md` and adversarial proof in `docs/VERIFICATION.md`. Current-source Direct Mode (22), lint (3 checks), and schema (22 methods) passed in the workspace. The steward fix has adversarial test coverage and is deployed with exact source parity; current-address semantic integration proofs passed. Challenge-budget and semantic supplemental-evidence authority tradeoffs are described in `DECISION.md` and `docs/SECURITY.md`.
