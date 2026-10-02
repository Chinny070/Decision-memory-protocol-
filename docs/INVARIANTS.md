# Protocol invariants

This matrix maps the required Decision Memory invariants to the implementation and the strongest current verification. Direct Mode tests are simulated proofs; hosted transactions are recorded separately in `VERIFICATION.md` and `SUBMISSION.md`.

| ID | Invariant | Enforcement | Verification |
| --- | --- | --- | --- |
| DM1 | Historical decision definition and baseline are immutable. | `register_decision`, one-shot `establish_baseline`; replay stores a separate receipt. | `test_replay_does_not_mutate_decision_or_certificate`; canonical replay transaction accepted; see `SUBMISSION.md`. |
| DM2 | Validators independently retrieve evidence. | `_consensus_findings` leader and validator closures each call the configured official `gl.nondet.web` API and compare recomputed receipt hashes. | Forged leader/hash tests; previous-source exact-text and semantic revalidation accepted on Studionet. |
| DM3 | Model findings cannot set protocol IDs, timestamps, topology, lease, or status. | `_valid_report` restricts model data to typed finding fields; `_derive_and_store` computes state. | Forged-leader, malformed-report, and schema tests. |
| DM4 | Reliance derives deterministically from accepted findings, lease, and graph state. | `_derive_semantic_status`, `_effective_contract_status`, `_effective_dependency_state`. | Reducer, lease, and dependency Direct Mode tests. |
| DM5 | Retrieval failure is not semantic contradiction. | Retrieval exceptions and known browser errors become `UNAVAILABLE` / `EXTERNAL_FAILURE`; reducer requires review. | `test_external_failure_is_fail_closed_not_invalidation`; canonical unavailable-source case accepted and reduced to `NEEDS_REVIEW`; see `SUBMISSION.md`. |
| DM6 | Only registered bounded edges propagate impact. | Dependency validation and `_downstream` scan registered decisions with fanout caps. | Hard-dependency propagation Direct Mode test. |
| DM7 | Decision graph is cycle-free. | Edges only point to already registered decisions; registration cannot create a backward path to the new node. | Registration and graph-bound tests. Assumption graph has no edge API in v1, so is acyclic by construction. |
| DM8 | Counterfactual replay cannot change original state. | Replay stores independent, bounded receipt keyed to original baseline and alternate policy. | `test_replay_does_not_mutate_decision_or_certificate`; canonical replay transaction accepted; see `SUBMISSION.md`. |
| DM9 | Blast-radius work is bounded and resumable. | Queue capped at 32, fanout capped, each `propagate_impact` write accepts at most 8 steps and persists a cursor. | Bounded propagation Direct Mode test; canonical propagation completed; see `SUBMISSION.md`. |
| DM10 | Successor lineage has one predecessor and cannot rewrite the predecessor. | A predecessor can acquire one successor only from its creator; authorization is enforced in `register_decision`. | `test_successor_linkage_is_authorized_at_registration_boundary`. |
| DM11 | Certificate matches canonical stored decision state. | `get_reliance_certificate` derives roots and current lease-aware status from stored record. | Certificate Direct Mode test; live reliance statuses were read after accepted transactions; no certificate digest claim is made. |
| DM12 | Partial validation cannot renew a full lease. | `_derive_and_store` renews `last_validated_at` and due time only when every assumption was selected. | Selective scope Direct Mode test. |
| DM13 | Challenge adds a receipt rather than rewriting the challenged receipt. | `challenge_revalidation` appends bounded challenge data and new observation receipts; EXACT_TEXT selects only a frozen source URL, retrieval kind, and marker; duplicate identities reject before consensus. | Frozen-source authority, selected-source availability, retrieval-kind, and duplicate-quota adversarial tests. |
| DM14 | Evidence identity excludes model rationale. | Receipt hashes cover bounded raw/normalized evidence; validators compare both evidence hashes; rationale is not hashed. | Forged content/render hash tests. |
| DM15 | Transaction-level `UNDETERMINED` is not an application status. | No write persists state until the nondeterministic transaction reaches consensus; lifecycle helper requests `FINALIZED` with bounded retries and requires `MAJORITY_AGREE`. | Hosted integration demonstrated an `UNDETERMINED` baseline and is correctly recorded as a failed proof, not success. FINALIZED helper change is locally inspected but not run against Studionet in this task. |

## Security corrections (current source)

- EXACT_TEXT registration requires one unique frozen `match_text` across all bound sources. Challenge grounds are explanatory only; every source, including challenge evidence, is checked against that frozen marker.
- Successor linkage is authorized in `register_decision` itself: only the predecessor creator may occupy its single successor slot, including through `create_successor`.
- Validators compare independently recomputed `render_hash` and `content_hash` as well as evidence receipt metadata.
- Replay validators must agree on the exact persisted `replay_result` enum; the explanation digest may differ.
- Challenge identities hash decision, assumption, reason, URL, and normalized-ground hash. Exact duplicates are rejected before consensus and do not consume the bounded per-decision quota.

The current deployment `0x9aF3aa61bEF38Abb597d7078F36659CBaFd65610` has finalized with majority agreement, and its retrieved source matches the current contract file by normalized SHA-256 `a5fed29ee04bb9da09a188712108420ef03472fe3062b745c553b860470c2aa1`. This verifies deployment parity; current-address application lifecycle proofs remain outstanding. The previous address `0x81F5dE555814a8C48Da2FeC654Df40a616b64e71` is historical and does not contain the latest challenge fixes.

## Known limitation

The previous deployment's broad semantic claim reached `NO_MAJORITY`, and its later revalidation attempt was interrupted by an RPC disconnect. On the previous security-fix deployment, the focused semantic baseline and full revalidation both reached accepted majority consensus and `RELIABLE`. A live semantic material-drift case remains untested; Direct Mode covers semantic re-fetch disagreement.
