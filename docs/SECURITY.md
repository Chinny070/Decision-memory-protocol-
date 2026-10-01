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
| Duplicate assumption, dependency, challenge, or successor | Duplicate checks and one-successor / bounded-count rules. |
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
- Assumption DAG cycles are impossible in v1 because assumptions cannot depend on one another.
- Decision dependency cycles are prevented by allowing edges only to existing decisions.
- Fanout, queue size, propagation work, and total capsule count are capped.
- Canonical JSON fingerprints use SHA-256 with `h_` prefix.
- Creator-supplied status, model-supplied reliance, model arithmetic, and model-supplied graph actions are not accepted.
- A hard dependency on an invalidated/blocked upstream becomes `BLOCKED`; uncertain upstream evidence leads to `NEEDS_REVIEW`.
- External failure does not automatically invalidate a decision.

## Lease and selective checks

A selective revalidation updates only checked assumption receipts. It does not renew `last_validated_at` or `revalidation_due_at`. Consumers see scope `PARTIAL`. Views calculate `EXPIRING`/`STALE` using deterministic transaction time. `refresh_lease` persists the state transition and starts propagation.

## Operational limits

The contract intentionally caps global decisions at 32 and selected histories. Once a global cap is reached, new objects fail closed. The protocol does not claim that an arbitrary URL is truthful or that validators can overcome unavailable, personalized, or adversarial sources. Evidence source selection and the frozen policy remain important to reviewers and downstream integrators.
