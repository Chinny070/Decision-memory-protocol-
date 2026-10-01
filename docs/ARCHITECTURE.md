# Architecture

## On-chain responsibility

`DecisionMemory` stores bounded immutable decision definitions, baseline snapshots, current typed findings, lease state, dependency edges, successor links, and receipts. Contract code validates all caller inputs and derives reliance state and dependency effects deterministically.

The Critical Assumption Graph is a bounded collection of assumption nodes attached to a decision. V1 intentionally has no assumption-to-assumption edges, making that graph acyclic by construction. The Decision Dependency Graph uses typed edges to existing decision IDs; edges to later registrations are impossible, so decision cycles cannot be created. Fanout and total graph size are capped.

## Nondeterministic boundary

For `SEMANTIC` assumptions, the leader and each validator independently fetch the same configured sources and interpret evidence under frozen policy and assumption text. The custom validator rejects malformed or substantively inconsistent typed findings. Explanatory prose and stable fact codes do not determine equivalence. For `EXACT_TEXT`, nodes independently render/fetch evidence and apply the same deterministic literal rule.

Counterfactual replay independently evaluates the frozen baseline under a new policy; it never re-fetches current evidence. The accepted typed result is isolated in a new replay record, and the contract computes its digest from committed hashes and the result.

## Data flow

```text
register definition → establish consensus baseline → Reliance Certificate
                                          ↓
                       revalidate current evidence
                                          ↓
                       deterministic status reducer
                                          ↓
                       bounded dependency propagation
```

Challenges add a separately evaluated receipt. A changed definition creates a successor capsule rather than editing history. Partial revalidation updates selected assumption receipts and does not renew the full-decision lease.

## Boundaries

The contract does not guarantee that creator-chosen sources are authoritative, that a public website is stable, or that validators will agree on semantic interpretation. Disagreement fails closed at the transaction level; it is not converted to an application status. See [CONSENSUS.md](CONSENSUS.md), [INVARIANTS.md](INVARIANTS.md), and [SECURITY.md](SECURITY.md).
