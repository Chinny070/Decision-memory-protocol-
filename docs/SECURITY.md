# Security model and known limits

## Threat model

### Assets

The protected assets are the frozen decision definition and baseline, evidence receipt integrity, reliance status consumed by downstream contracts, dependency/lineage topology, lease timing, challenge/replay history, and bounded protocol storage. V1 holds no user funds.

### Actors and assumptions

Callers can submit arbitrary definitions and can challenge observations. Source owners can change, remove, personalize, or poison public pages. A malicious web page may contain prompt injection. A leader may submit forged findings; a validator minority may lie or disagree. A downstream consumer may read a stale or non-final transaction state. Safety assumes GenLayer consensus behaves according to its protocol, honest validators can access the bound sources, and integrators check the certificate at the required finality level.

### Attacks and controls

| Attack | Control / result |
| --- | --- |
| Malformed or non-HTTPS URL | URL validation rejects it at registration/challenge. |
| Oversized payload, source, graph, or history | Strict per-field and global bounds; writes fail closed at capacity. |
| Prompt injection in web text or caller challenge ground | Inputs are framed as untrusted data; model output is typed and validated. |
| Forged leader finding | Independent validator refetches and reevaluates; reliance-critical disagreement rejects consensus. |
| Forged evidence receipt | Validators compare independently recomputed render/content hashes and receipt metadata against the leader. |
| Duplicate assumption, dependency, challenge, or successor | Duplicate checks and one-successor / bounded-count rules. |
| Caller introduces attacker-controlled evidence authority for EXACT_TEXT | Source URL and retrieval kind are frozen at registration; an EXACT_TEXT challenge must select a registered URL and uses its frozen retrieval configuration and marker. `factual_ground` is untrusted context. |
| Unavailable challenged EXACT_TEXT source appears contradicted because another source is available | Availability is scoped to the selected frozen source; unavailable means `UNAVAILABLE` / `EXTERNAL_FAILURE`, never contradiction. |
| Successor slot hijack | Lowest-level `register_decision` check requires sender to equal predecessor creator before predecessor mutation. |
| Duplicate challenge burns quota | Canonical identity over immutable challenge inputs is checked before consensus and count increment; identity storage is bounded by the existing global challenge cap. |
| Permissionless callers exhaust challenge quota | This is an explicit v1 tradeoff: all callers share a first-come budget of three distinct attempts per decision, including valid inconclusive attempts. Exact duplicates do not count. V1 has no challenger authorization or stake gate; integrators accept this bounded denial-of-service surface or should avoid relying on a decision whose challenge budget is essential. |
| Semantic challenger supplies biased supplemental evidence | SEMANTIC challenge URLs and factual grounds are untrusted. Validators independently retrieve the supplemental URL and judge it under the frozen assumption and policy; it does not alter frozen source bindings or definition hash. EXACT_TEXT challenges are constrained to registered source authority. |
| Replay typed-result equivocation | Validators must agree on the exact enum persisted and exposed; only explanatory digest text is excluded. |
| Stale evidence or partial refresh | Per-assumption receipts and `PARTIAL` scope; partial work does not renew the full lease. |
| Temporary network failure | Becomes `UNAVAILABLE` / `EXTERNAL_FAILURE` and review, not contradiction or invalidation. |
| Replay used to rewrite history | Replay is a separate bounded receipt; original decision hashes and status are unchanged. |
| Graph amplification or cycles | Existing-node-only DAG edges, fanout cap, bounded resumable queue and step limit. |
| Ambiguous consensus / validator disagreement | Transaction-level `UNDETERMINED`; no application success is inferred. |

Reentrancy and message ordering are not applicable to this v1 interface: it has no external contract calls, emitted messages, or token transfers.

## Trust boundaries

- Decision creators choose the initial bounded payload, policy, assumptions, and public source bindings. Those inputs are frozen and fingerprinted.
- Public web pages and caller-supplied challenge grounds are untrusted data, including any prompt-injection text they contain.
- A leader's output is not trusted. Validators independently retrieve the bound sources and reproduce the reliance-critical finding fields.
- Models cannot write contract storage or choose identities, hashes, timestamps, leases, lineage, or graph transitions.
- Downstream consumers should use `get_reliance_certificate` / `is_reliable`, and should re-read after a write reaches the finality level their application requires.

## Deterministic controls

- HTTPS-only source URLs; bounded text, sources, assumptions, dependencies, histories, replays, and challenge rounds.
- EXACT_TEXT challenges cannot add a source authority; they recheck one frozen registered source with its original retrieval kind and marker.
- SEMANTIC challenges may add one supplemental HTTPS source. Its authority is validator/policy judged, not frozen-source authority; the source is recorded in the challenge evidence receipts and does not rewrite the capsule.
- Assumption DAG cycles are impossible in v1 because assumptions cannot depend on one another.
- Decision dependency cycles are prevented by allowing edges only to existing decisions.
- Fanout, queue size, propagation work, and total capsule count are capped.
- Canonical JSON fingerprints use SHA-256 with `h_` prefix.
- Creator-supplied status, model-supplied reliance, model arithmetic, and model-supplied graph actions are not accepted.
- Only the predecessor creator may create its one successor; `register_decision` enforces this even when called directly.
- Exact duplicate challenge attempts do not consume challenge capacity; materially different ground, URL, reason, or assumption can be a separate challenge.
- The three-challenge budget is permissionless and shared across callers. A distinct valid attempt can consume a slot even when its result is inconclusive; this is intentional for v1 and is a documented denial-of-service limit, not a caller-specific quota.
- A hard dependency on an invalidated/blocked upstream becomes `BLOCKED`; uncertain upstream evidence leads to `NEEDS_REVIEW`.
- External failure does not automatically invalidate a decision.

## Lease and selective checks

A selective revalidation updates only checked assumption receipts. It does not renew `last_validated_at` or `revalidation_due_at`. Consumers see scope `PARTIAL`. Views calculate `EXPIRING`/`STALE` using deterministic transaction time. `refresh_lease` persists the state transition and starts propagation.

## Operational limits

The contract intentionally caps global decisions at 32 and selected histories. Once a global cap is reached, new objects fail closed. The protocol does not claim that an arbitrary URL is truthful or that validators can overcome unavailable, personalized, or adversarial sources. Evidence source selection and the frozen policy remain important to reviewers and downstream integrators.


## Semantic finding cross-field safety

Every validator finding must satisfy `_finding_fields_coherent` before acceptance. Inadequate evidence cannot support `SUPPORTED` or `WEAKENED`; `external_failure` requires `UNAVAILABLE` / `EXTERNAL_FAILURE`; and `critical_conflict` requires sufficient `CONTRADICTED` evidence with `CRITICAL_CHANGE`. Both report validation entry points enforce these relationships. The deterministic reducer independently treats incoherent findings as uncertain and fails closed to review, preventing `RELIABLE` even if malformed data reaches it. `test_report_validation_rejects_incoherent_evidence_safety_fields` exercises contradictory combinations through both paths.
