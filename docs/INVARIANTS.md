# Protocol invariants

This matrix maps the required Decision Memory invariants to the implementation and the strongest current verification. Direct Mode tests are simulated proofs; hosted transactions are recorded separately in `VERIFICATION.md` and `SUBMISSION.md`.

| ID | Invariant | Enforcement | Verification |
| --- | --- | --- | --- |
| DM1 | Historical decision definition and baseline are immutable. | `register_decision`, one-shot `establish_baseline`; replay stores a separate receipt. | `test_replay_does_not_mutate_decision_or_certificate`; canonical replay transaction accepted; see `SUBMISSION.md`. |
| DM2 | Validators independently retrieve evidence. | `_consensus_findings` leader and validator closures each call the configured official `gl.nondet.web` API and compare recomputed receipt hashes. | Forged leader/hash tests; current-address exact-text and semantic full revalidation reached `FINALIZED` / `MAJORITY_AGREE`. |
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
| DM13 | Challenge adds a receipt rather than rewriting the challenged receipt. | `challenge_revalidation` appends bounded challenge data and new observation receipts; EXACT_TEXT selects only a frozen source URL, retrieval kind, and marker; SEMANTIC supplemental URLs are independently judged under frozen policy; duplicate identities reject before consensus. | Frozen-source authority, selected-source availability, retrieval-kind, and duplicate-quota adversarial tests; current-address challenge finalized. |
| DM14 | Evidence identity excludes model rationale. | Receipt hashes cover bounded raw/normalized evidence; validators compare both evidence hashes; rationale is not hashed. | Forged content/render hash tests. |
| DM15 | Transaction-level `UNDETERMINED` is not an application status. | No write persists state until the nondeterministic transaction reaches consensus; lifecycle helpers request `FINALIZED` with bounded retries and require `MAJORITY_AGREE`. | Current-address exact-text lifecycle and semantic baseline/revalidation passed with finalized receipts. Failed or canceled attempts are recorded separately and are not counted as success. |

## Security corrections (current source)

- EXACT_TEXT registration requires one unique frozen `match_text` across all bound sources. Challenge grounds are explanatory only; the selected registered source is checked against that frozen marker.
- Successor linkage is authorized in `register_decision` itself: only the predecessor creator may occupy its single successor slot, including through `create_successor`.
- Validators compare independently recomputed `render_hash` and `content_hash` as well as evidence receipt metadata.
- Replay validators must agree on the exact persisted `replay_result` enum; the explanation digest may differ.
- Challenge identities hash decision, assumption, reason, URL, and normalized-ground hash. Exact duplicates are rejected before consensus and do not consume the bounded per-decision quota.
- Challenges are permissionless; all callers share a first-come budget of three distinct attempts per decision. A distinct accepted report can consume a slot when its evidence is inconclusive. This is an intentional v1 tradeoff, not an access-control guarantee.
- SEMANTIC challenge URLs and grounds are untrusted supplemental inputs; validators independently retrieve and judge them under the frozen assumption and policy. They do not modify the frozen source list or definition hash.

The current deployment `0xC3c63aB9459fd8BC87fa29161e2019F7d454B643` finalized with majority agreement, and retrieved-source parity was verified at normalized SHA-256 `eafa0b94585c0110889dd2cc3fdced1bc667853e74712eef6e4eef3933ffd699`. The steward-requested semantic cross-field safety fix is deployed there. Current-address semantic baseline and full revalidation finalized successfully. Earlier `0x9aF3...` exact-text and dependency lifecycle proofs are historical and must not be attributed to this deployment.

## Known limitation

An earlier current-address semantic revalidation attempt ended `CANCELED` / `NO_MAJORITY`; a subsequent complete current-address semantic baseline and full revalidation both reached finalized majority consensus and `RELIABLE`. A live semantic material-drift case remains untested; Direct Mode covers semantic re-fetch disagreement.
