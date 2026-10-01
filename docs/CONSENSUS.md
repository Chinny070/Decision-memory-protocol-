# Consensus and evidence model

## What validators decide

For baseline establishment, revalidation, and challenge, each execution calls `gl.nondet.web.render(url, mode="html")` for browser-rendered sources or `gl.nondet.web.get(url)` for explicitly selected text/API retrieval. A source is rendered once per assumption per execution. Browser output is bounded, script/style/comment blocks and markup are stripped, and a versioned normalized text digest is stored beside the bounded raw render digest. The accepted leader observation is stored as provenance hashes; dynamic rendered HTML hashes are not compared between validators.

For semantic assumptions, each node independently asks `gl.nondet.exec_prompt(..., response_format="json")` for a small typed finding against the frozen policy, assumption, and baseline. Source text and caller challenge grounds are framed as untrusted data; embedded instructions are not policy. Exact-text assumptions bypass the model and use a deterministic text-presence rule.

The custom `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)` validator:

1. Requires a successful `gl.vm.Return` from the leader.
2. Checks the complete typed report schema, enum values, booleans, fact-code limits, and evidence-receipt shape.
3. Independently re-fetches the same bound sources and reruns the same assumption evaluation.
4. Requires exact agreement on assumption ID, support state, materiality, evidence sufficiency, external-failure flag, and critical-conflict flag. Stable fact codes and prose are retained for audit but are excluded from equivalence because labels may differ while the typed judgment agrees.
5. Ignores prose and content/render hashes when comparing validators, because dynamic pages and explanations can legitimately vary.

A well-formed but substantively false leader report is rejected when the validator's own evidence evaluation differs. Error results are rejected; malformed model output becomes `INSUFFICIENT`, not positive support. Stable fact codes and prose are excluded from typed equivalence. Replay compares outcome classes: continued reliance, invalidation, or caution (`DEGRADE`, `REVIEW`, and `INCONCLUSIVE`). The leader's exact typed result is stored only after validators agree on that class; the contract then computes the replay digest from frozen baseline and policy hashes plus the typed result. This groups outcomes that all prohibit affirmative reliance while retaining distinct display labels. A disagreement across classes remains a consensus failure and cannot mutate state.

## Evidence receipts

The accepted leader snapshot records source URL, retrieval kind, SHA-256 render/content hashes (or `0` when unavailable), normalization version, source role, assumption IDs, and observation status. These hashes identify the accepted observation; they do not claim byte-identical pages across all validators. Model reasoning is excluded from evidence identity.

## Failure semantics

- A thrown retrieval failure becomes `UNAVAILABLE` / `EXTERNAL_FAILURE` and requires review.
- Missing, malformed, or insufficient semantic results do not support reliance.
- A successful semantic contradiction is distinct from a network failure.
- LLM errors do not produce affirmative findings.
- The deterministic reducer—not the model—derives reliance and dependency state.

## Historical replay

Replay validators evaluate the exact contract-stored baseline snapshot under the new policy. They do not retrieve today's web evidence. The receipt is separate from the decision capsule and cannot mutate it.
