# Deployment and source parity

## Network

Canonical target: hosted GenLayer Studionet (`https://studio.genlayer.com/api`, chain ID `61999`). The Explorer base is `https://explorer-studio.genlayer.com`.

An earlier candidate was deployed to hosted Studionet at `0xE7146a6556be0F9e5C5729F3660eAD91b50A573C` in transaction `0x62ca2d689418e2b00a2216e8f41cc5b26c4e2585e428aa3584d5d1d9f47b6968`. Its receipt was `ACCEPTED` / `MAJORITY_AGREE` with five validator agreements, and its schema was retrievable (22 methods). Source changed after that deployment, so this is not the canonical final-source address. Redeploy after final commit and compare the exact returned code blob with the committed contract before recording parity.

## Canonical deployment procedure

1. Run the Direct Mode suite, `genvm-lint check`, and schema extraction against the final committed source.
2. Confirm the selected GenLayer account has Studionet access and sufficient network balance without exporting or committing its key.
3. Deploy `contracts/decision_memory.py` to the official Studionet RPC with the currently supported GenLayer CLI.
4. Record the deploy transaction hash, finality/status, returned address, source commit, and Explorer address page.
5. Read deployed schema and source through the CLI/RPC. Hash the exact deployed source blob and compare it with `contracts/decision_memory.py` at the deployment commit.
6. Run baseline, live render evidence, revalidation, replay, negative case, and dependency propagation on the canonical instance. Record every transaction hash, status, and typed stored result.
7. Redeploy and repeat parity/evidence if any source change occurs after deployment.

CLI interfaces change. Verify current options with `genlayer deploy --help`, `genlayer account --help`, and `genlayer network info` before submitting signed transactions. Official CLI deployment uses `genlayer deploy --contract ... --rpc https://studio.genlayer.com/api`.

## Hosted proof attempt

A successful disposable lifecycle ran at `0x29ee1C31AA1e99f59d05BAec46A9b34d1D2ba241`. The official rendered GenLayer documentation page supplied its published heading for the `EXACT_TEXT` check. Baseline and revalidation both returned `RELIABLE`; replay returned `WOULD_REQUIRE_REVIEW`; the evidence-backed challenge returned `OVERTURNED`; the `.invalid` source path returned `NEEDS_REVIEW`; and bounded hard-dependency propagation completed. Every write was checked for `ACCEPTED` and `MAJORITY_AGREE`. The separate `SEMANTIC` LLM baseline remains unresolved (`UNDETERMINED` / `NO_MAJORITY`); do not represent this deterministic live path as proof of semantic-mode consensus.

The earlier canonical deployment is not the final source deployment because code changed after it. Redeploy the final commit, record the new transaction and address, and verify source parity before claiming canonical final evidence.

The evidence ledger in `SUBMISSION.md` records actual outcomes. Never interpret `UNDETERMINED` as application status or success.
