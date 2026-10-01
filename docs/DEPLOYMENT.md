# Deployment and source parity

## Network

Canonical target: hosted GenLayer Studionet (`https://studio.genlayer.com/api`, chain ID `61999`). The Explorer base is `https://explorer-studio.genlayer.com`.

The final contract source from commit `176136ee1bb507aee8aa86673741ee9d8792500d` is deployed at `0xC25E6be425d940BB4b794932b1226D4bccD21824` in transaction `0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac`. Its receipt was `ACCEPTED` / `MAJORITY_AGREE`; schema retrieval returned 22 methods. The address Explorer page returned HTTP 200 and contained the contract address. The transaction Explorer page returned HTTP 200 and contained the deploy hash.

## Canonical deployment procedure

1. Run the Direct Mode suite, `genvm-lint check`, and schema extraction against the final committed source.
2. Confirm the selected GenLayer account has Studionet access and sufficient network balance without exporting or committing its key.
3. Deploy `contracts/decision_memory.py` to the official Studionet RPC with the currently supported GenLayer CLI.
4. Record the deploy transaction hash, finality/status, returned address, source commit, and Explorer address page.
5. Read deployed schema and source through the CLI/RPC. Hash the exact deployed source blob and compare it with `contracts/decision_memory.py` at the deployment commit.
6. Run baseline, live render evidence, revalidation, replay, negative case, and dependency propagation on the canonical instance. Record every transaction hash, status, and typed stored result.
7. Redeploy and repeat parity/evidence if any source change occurs after deployment.

CLI interfaces change. Verify current options with `genlayer deploy --help`, `genlayer account --help`, and `genlayer network info` before submitting signed transactions. Official CLI deployment uses `genlayer deploy --contract ... --rpc https://studio.genlayer.com/api`.

## Deployed source parity

- Git blob SHA-1: `73007b3208992af1cb333bc6605861d99b8fa67b`.
- Retrieved deployed source SHA-256 after removing CLI display framing newlines: `53e9107e8a7013eb5a81201d4e8b73cd2bb83284188ba60367ab3f71b9ce1b34`.
- Exact comparison: retrieved source equals the decoded Git blob at the deployment source commit.
- Address Explorer: https://explorer-studio.genlayer.com/address/0xC25E6be425d940BB4b794932b1226D4bccD21824.
- Deployment Explorer: https://explorer-studio.genlayer.com/tx/0xd9d1d7ccd004bea5d202c5615021b28923df5557f4a3102b3cc49f001fa12eac.

## Canonical lifecycle

The canonical exact-text baseline, revalidation, replay, challenge, negative source case, and bounded dependency propagation were accepted. Hashes and typed outcomes are in `SUBMISSION.md`. The canonical dependency baseline and propagation were completed in a separate resume test after a transient RPC disconnect; the final event `impact_4` reached `complete=True` and its transaction receipt was `FINALIZED` / `MAJORITY_AGREE`.

## Disposable hosted proof

A focused semantic-mode baseline using a direct official-docs claim also reached `RELIABLE` with accepted majority consensus. Its full semantic revalidation attempt ended in an RPC transport disconnect; no result is claimed. An earlier broader semantic assumption did produce `UNDETERMINED` / `NO_MAJORITY`, so semantic-mode agreement needs further live revalidation proof.

The evidence ledger in `SUBMISSION.md` records actual outcomes. Never interpret `UNDETERMINED` as application status or success.
