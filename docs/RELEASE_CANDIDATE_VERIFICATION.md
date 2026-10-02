# Release candidate verification

## Contract source commit

- Previous deployed-source commit: `176136ee1bb507aee8aa86673741ee9d8792500d`.
- Security-fix source commit: `2ae77cfca02bb81f770aa4e1838a846260decafa`.
- Previous security-fix source commit `2ae77cfca02bb81f770aa4e1838a846260decafa`: 17 Direct Mode tests passed (includes adversarial security regressions).
- Current source: 21 Direct Mode tests passed; GenVM lint passed 3 checks; schema unchanged at 22 methods (14 read, 8 write).
- Pickling/serialization: enabled in Direct Mode tests.
- GenVM linter 0.11.0: 3 checks passed.
- GenVM schema: 22 methods (14 read, 8 write).
- Clean clone: GitHub commit `9d06206f62b4e89d0f8e2d0f5dbdf4962a0e2041` cloned directly from `main`; requirements resolved from already installed pins, 21 Direct Mode tests passed, lint passed 3 checks, and schema stayed at 22 methods.

## Current deployment (latest challenge-fix source)

- Studionet contract: `0x9aF3aa61bEF38Abb597d7078F36659CBaFd65610`.
- Deploy transaction: `0x20b1ff738043da829594a4e0f3f5311beafe5f4d06996ff4bb231891ef53206b`, `FINALIZED` / `MAJORITY_AGREE`.
- Schema: 22 methods (14 views, 8 writes).
- Retrieved source exact match: normalized SHA-256 `a5fed29ee04bb9da09a188712108420ef03472fe3062b745c553b860470c2aa1`; local blob `c27f7ee4c97f8b9edc5ec42a7b9db772e5c6fe37`.
- Current-source exact-text lifecycle and bounded dependency propagation are finalized at the current address; see `docs/VERIFICATION.md` and `SUBMISSION.md` for each transaction hash and typed result.
- Current-source semantic-mode baseline and full revalidation both finalized with `MAJORITY_AGREE` and `RELIABLE`; see the semantic proof table below.
- Contract source matches blob `c27f7ee4c97f8b9edc5ec42a7b9db772e5c6fe37` in GitHub `main` commit `d5e2c75b7fdff60bbf078036ce48370e42acfa8b`. The local workspace checkout remains dirty because its `.git` is read-only.

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

- Current-address semantic baseline: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`, transaction `0xd61a3efdde33e445da32becc2c792f4347079485b68a277b17b0b321185dad3d`.
- Current-address semantic full revalidation: `RELIABLE`, `FINALIZED` / `MAJORITY_AGREE`, transaction `0x3fb37f4492408cc9268445f6e0b283a8be266105ecdc876dc59f263ba50cb1b8`.
- Current-address exact-text baseline and full revalidation: both `RELIABLE`, transaction hashes in `docs/VERIFICATION.md`.
- Current-address live challenge: `UPHELD`; unavailable-source handling: `NEEDS_REVIEW`; hard-dependent propagation: `impact_5` complete, hashes in `docs/VERIFICATION.md`.

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

Current-source deployment and exact source parity are verified. Current-source Direct Mode, lint, and schema passed in the workspace and a clean clone. FINALIZED-aware exact-text and semantic integration proofs passed against the current address. Challenge-budget and semantic supplemental-evidence authority tradeoffs are described in `DECISION.md` and `docs/SECURITY.md`.
