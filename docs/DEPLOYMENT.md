# Deployment and source parity

## Current deployment

- Network: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- Contract address: `0xC3c63aB9459fd8BC87fa29161e2019F7d454B643`.
- Deployment transaction: `0x509b1314e9d6e96792427b135ba3c0260dcf1af3fb8b05fb0f234cf8ca81ec56`.
- Receipt: `FINALIZED`, `MAJORITY_AGREE`, leader execution `SUCCESS`, sender `0xaffE15eEc45b68835cc9E5B4Ab85dD5deaE8e70b`.
- Deployed schema: 22 methods (14 views, 8 writes).
- Retrieved-source normalized SHA-256: `eafa0b94585c0110889dd2cc3fdced1bc667853e74712eef6e4eef3933ffd699`.
- GitHub source commit: `08addb48a6d554596fe9e5ef395e6ba1e5b3f7ff`; contract blob SHA-1 `ab348789bba2d2c5cd089c1774e6059942f5a55b`.
- Source parity: verified against retrieved `genlayer code` output after removing CLI framing and normalizing line endings.
- Explorer address: https://explorer-studio.genlayer.com/address/0xC3c63aB9459fd8BC87fa29161e2019F7d454B643.
- Explorer transaction: https://explorer-studio.genlayer.com/tx/0x509b1314e9d6e96792427b135ba3c0260dcf1af3fb8b05fb0f234cf8ca81ec56.

This deployment includes the semantic cross-field fail-closed fix requested by the steward. The new address's semantic baseline and full revalidation finalized with `MAJORITY_AGREE` and `RELIABLE`; their transaction hashes are recorded in `docs/VERIFICATION.md`. The full current-address lifecycle finalized with majority agreement, including unavailable-source handling (`NEEDS_REVIEW`) and bounded dependency propagation (`impact_4` complete). The older `0x9aF3...` lifecycle records below are historical and must not be attributed to this deployment.

## Previous-source deployment

- Network: GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`.
- Contract address: `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71`.
- Deployment transaction: `0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179`.
- Receipt: `FINALIZED`, `MAJORITY_AGREE`, leader execution `SUCCESS`, sender `0xaffE15eEc45b68835cc9E5B4Ab85dD5deaE8e70b`.
- Source commit: `2ae77cfca02bb81f770aa4e1838a846260decafa`; contract blob `d7993a030b372d0e7debb51c7d01842b77d10171`.
- Deployed source normalized-text SHA-256: `57ff36d5de87f6de92a9c7580a6fd37017b92f2a6fed1c39066864b26c323254`.
- Exact source parity: verified; retrieved `genlayer code` equals the current contract file after removing CLI framing and normalizing line endings.
- Deployed schema: 22 methods (14 views, 8 writes).
- Explorer address: https://explorer-studio.genlayer.com/address/0x81F5dE555814a8C48Da2FeC654Df40a616b64e71 (HTTP 200; address present).
- Explorer transaction: https://explorer-studio.genlayer.com/tx/0x6059226441770fc986ab0b553520a914b61c5912899aacaa1f8e7812a6615179 (HTTP 200; transaction hash present).

Deployment receipt and source/schema retrieval were verified with GenLayer CLI 0.39.1. This address uses the source before the frozen-source challenge authority and selected-source availability fixes. It is superseded by the current deployment above; its application lifecycle evidence remains historical.

## Previous deployment

The prior address `0xC25E6be425d940BB4b794932b1226D4bccD21824` was deployed from pre-security-fix commit `176136ee1bb507aee8aa86673741ee9d8792500d` in transaction `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`. It does not contain the current security fixes. Its lifecycle evidence is preserved as historical evidence only.

## Repeatable deployment procedure

1. Run `python -m pytest -q tests/direct`, `genvm-lint check contracts/decision_memory.py`, and `genvm-lint schema contracts/decision_memory.py`.
2. Confirm the effective network with `genlayer network info` and use the official Studionet RPC.
3. Deploy `contracts/decision_memory.py` with the current GenLayer CLI.
4. Verify the transaction receipt reaches accepted/finalized majority consensus and record the returned address.
5. Retrieve deployed schema and source; compare source with the committed contract file.
6. Run the current-source live lifecycle and record each transaction/status before claiming lifecycle verification.

The previous deployment includes the earlier EXACT_TEXT marker, successor authorization, evidence hash, replay agreement, and duplicate challenge fixes. It does not include the current EXACT_TEXT frozen-source challenge authority and selected-source availability fixes.
