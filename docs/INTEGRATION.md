# Integration guide

## Register and baseline

`register_decision` takes a caller-chosen stable ID, subject key, bounded decision payload, frozen policy text, JSON assumptions, JSON dependencies, and lease intervals in seconds. The initial status is always `REGISTERED`.

Example assumption JSON:

```json
[
  {
    "assumption_id": "license",
    "statement": "Provider remains licensed for the covered service.",
    "criticality": "CRITICAL",
    "evaluation_mode": "SEMANTIC",
    "sources": [
      {"url": "https://registry.example.org/provider", "retrieval_kind": "WEB_RENDER_HTML"}
    ]
  }
]
```

`EXACT_TEXT` is a deterministic evaluation mode and requires `match_text` on a source. Supported retrieval kinds are `WEB_RENDER_HTML`, `WEB_GET_TEXT`, `API_JSON`, and `STATIC_DOCUMENT`. Version 1 maps all non-render kinds through the supported text-get API; consumers should choose them only for stable text/JSON resources.

Pass `[]` for no dependencies or a JSON list of existing capsule references:

```json
[{"decision_id":"vendor-security-v1","kind":"HARD_DEPENDS_ON"}]
```

Then call `establish_baseline(decision_id)`. Do not treat registration as approval.

## Relying on a capsule

Read `get_reliance_certificate(decision_id)` and require `current_reliance_status == "RELIABLE"` before an irreversible downstream action. A certificate in `EXPIRING`, `STALE`, `DEGRADED`, `NEEDS_REVIEW`, `BLOCKED`, `UNKNOWN`, or `INVALIDATED` is not affirmative authorization. Re-read after the transaction reaches the finality level required by the consuming application.

## Revalidation, challenge, and replay

- `revalidate(id, '["assumption-a"]')` checks only the listed assumptions. Use all IDs in one call for a lease renewal.
- `challenge_revalidation` requires an existing assumption, bounded reason enum, new HTTPS evidence URL, and factual ground. It creates a separate immutable challenge receipt and may update current reliance from fresh findings.
- For `EXACT_TEXT` assumptions, the challenge factual ground is treated as the literal text to verify on the newly supplied evidence URL.
- `create_counterfactual_replay(id, new_policy)` uses the frozen baseline only. It creates a receipt without changing the original policy or status.
- `create_successor` creates a new capsule and links it to its predecessor with a typed reason.

## Dependency propagation

After a reliance transition, read `get_latest_impact(decision_id)` and call `propagate_impact(event_id, 1..8)` repeatedly until `complete` is true. Reads also evaluate direct dependency state while a queue is pending, so consuming integrations can fail closed immediately. Propagation records materialized state for downstream views and further traversal.

## Three consumer patterns

The primitive is domain-neutral. Each consumer reads the same certificate and blocks unless the state is exactly `RELIABLE`.

1. **Autonomous agent provider selection:** before dispatching work to a previously selected API provider, an agent checks the capsule that froze licensing, service availability, and security assumptions.
2. **DAO or governance execution:** a governance executor checks a vendor or parameter approval before a later treasury or operations action, and registers a hard dependency so upstream invalidation blocks the dependent capsule.
3. **Compliance or risk gate:** a lending, insurance, treasury, or compliance contract checks an older policy/risk decision before relying on it; uncertain or stale evidence blocks the action for review.

No consumer needs a protocol-specific fork. Consumers can bind a minimal interface:

```python
@gl.contract_interface
class IDecisionMemory:
    class View:
        def is_reliable(self, decision_id: str) -> bool: ...
        def get_reliance_certificate(self, decision_id: str) -> dict: ...
```

## Hosted integration tests

Install pinned dependencies and run the committed integration folder against hosted Studionet:

```powershell
gltest tests/integration/ -v -s --network studionet
```

Hosted tests create disposable deployments. They are not the canonical deployment. The latest suite completed one live lifecycle with accepted baseline, revalidation, replay, challenge, fail-closed source failure, and dependency propagation transactions. The successful run used exact-text evidence and does not clear the separate unresolved live semantic-mode consensus attempt. Exact hashes and statuses are in `SUBMISSION.md`; final-source canonical deployment and parity must still be recorded in `docs/DEPLOYMENT.md`.
