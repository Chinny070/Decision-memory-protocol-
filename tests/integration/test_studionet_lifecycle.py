"""Live Studionet proof. Run only by explicitly targeting this folder."""

import json
import os
import subprocess
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts" / "decision_memory.py"
DOCS_URL = "https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism"


def _assumption(source_url=DOCS_URL, assumption_id="official-docs"):
    return json.dumps([{
        "assumption_id": assumption_id,
        "statement": "The source is an official GenLayer developer guide describing non-deterministic Intelligent Contract operations.",
        "criticality": "MAJOR",
        "evaluation_mode": "EXACT_TEXT",
        "sources": [{"url": source_url, "retrieval_kind": "WEB_RENDER_HTML", "match_text": "Non-determinism in Intelligent Contracts"}],
    }])


def _transact(contract, method, *args):
    receipt = getattr(contract, method)(args=list(args)).transact()
    assert tx_execution_succeeded(receipt), f"{method} failed: {receipt}"
    assert receipt.get("status_name") == "ACCEPTED", f"{method} did not reach ACCEPTED: {receipt}"
    assert receipt.get("result_name") == "MAJORITY_AGREE", f"{method} did not reach MAJORITY_AGREE: {receipt}"
    print(f"LIVE_TX method={method} hash={receipt.get('hash') or receipt.get('tx_id')} status={receipt.get('status_name')}")
    return receipt


@pytest.mark.integration
def test_live_studionet_reliance_replay_failure_and_dependency_proof():
    factory = get_contract_factory(contract_file_path=CONTRACT_PATH)
    # genlayer-test 0.29.2's code-schema RPC fallback is unavailable on hosted
    # Studionet in this environment. Extract the ABI from the exact deployed
    # source with the official GenVM linter, then use the SDK's normal contract
    # binding and transaction methods.
    schema_output = subprocess.check_output(
        ["genvm-lint", "schema", "--json", str(CONTRACT_PATH)],
        text=True,
        encoding="utf-8",
    )
    factory._get_schema_with_fallback = lambda: json.loads(schema_output)["schema"]
    canonical_address = os.environ.get("DMP_CANONICAL_ADDRESS", "").strip()
    contract = factory.build_contract(canonical_address) if canonical_address else factory.deploy()
    address = getattr(contract, "address", None) or getattr(contract, "contract_address", None)
    print(f"LIVE_CONTRACT address={address} canonical={bool(canonical_address)}")

    decision_id = "live-docs-" + str(os.getpid())
    _transact(
        contract, "register_decision", decision_id, "genlayer:official-docs",
        "Rely on the official developer guide for non-deterministic contract behavior.",
        "Policy v1: official documentation must describe the supported non-deterministic execution model.",
        _assumption(), "[]", 86400, 3600, "", "",
    )
    baseline_tx = _transact(contract, "establish_baseline", decision_id)
    baseline = contract.get_reliance_certificate(args=[decision_id]).call()
    assert baseline["baseline_evidence_digest"]
    assert baseline["current_reliance_status"] in ("RELIABLE", "DEGRADED", "NEEDS_REVIEW", "UNKNOWN")
    print(f"LIVE_BASELINE status={baseline['current_reliance_status']} tx={baseline_tx.get('hash') or baseline_tx.get('tx_id')}")

    revalidation_tx = _transact(contract, "revalidate", decision_id, '["official-docs"]')
    after_revalidation = contract.get_reliance_certificate(args=[decision_id]).call()
    assert after_revalidation["last_validation_scope"] == "FULL"
    print(f"LIVE_REVALIDATION status={after_revalidation['current_reliance_status']} tx={revalidation_tx.get('hash') or revalidation_tx.get('tx_id')}")

    replay_tx = _transact(contract, "create_counterfactual_replay", decision_id, "Policy v2: require the docs page to explicitly document independent validators.")
    replay = contract.get_latest_replay(args=[decision_id]).call()
    assert replay["typed_result"] in ("WOULD_REMAIN_RELIABLE", "WOULD_DEGRADE", "WOULD_REQUIRE_REVIEW", "WOULD_INVALIDATE", "INCONCLUSIVE")
    print(f"LIVE_REPLAY result={replay['typed_result']} tx={replay_tx.get('hash') or replay_tx.get('tx_id')}")
    unchanged = contract.get_reliance_certificate(args=[decision_id]).call()
    assert unchanged["decision_definition_hash"] == baseline["decision_definition_hash"]

    challenge_tx = _transact(
        contract, "challenge_revalidation", decision_id, "official-docs", "NEW_EVIDENCE",
        "https://docs.genlayer.com/developers/intelligent-contracts/first-intelligent-contract",
        "Non-determinism in Intelligent Contracts",
    )
    challenge = contract.get_latest_challenge(args=[decision_id]).call()
    assert challenge["result"] in ("UPHELD", "MODIFIED", "OVERTURNED", "INCONCLUSIVE")
    print(f"LIVE_CHALLENGE result={challenge['result']} tx={challenge_tx.get('hash') or challenge_tx.get('tx_id')}")

    failure_id = decision_id + "-source-failure"
    _transact(
        contract, "register_decision", failure_id, "failure:unavailable-source",
        "A provider must satisfy an externally evidenced license claim.",
        "Policy v1: unavailable evidence is reviewable and is not semantic invalidation.",
        _assumption("https://decision-memory-unavailable.invalid/license", "license-source"),
        "[]", 86400, 3600, "", "",
    )
    failure_baseline_tx = _transact(contract, "establish_baseline", failure_id)
    failure_status = contract.get_reliance_status(args=[failure_id]).call()
    assert failure_status != "RELIABLE"
    assert failure_status != "INVALIDATED"
    print(f"LIVE_NEGATIVE status={failure_status} tx={failure_baseline_tx.get('hash') or failure_baseline_tx.get('tx_id')}")

    child_id = decision_id + "-dependent"
    hard_dependency = json.dumps([{"decision_id": failure_id, "kind": "HARD_DEPENDS_ON"}])
    _transact(
        contract, "register_decision", child_id, "workflow:dependent-provider",
        "Route work only when the provider license decision remains safe.",
        "Policy v1: upstream provider licensing is a hard dependency.",
        _assumption(DOCS_URL, "dependent-docs"), hard_dependency, 86400, 3600, "", "",
    )
    _transact(contract, "establish_baseline", child_id)
    assert contract.get_reliance_status(args=[child_id]).call() in ("NEEDS_REVIEW", "BLOCKED", "UNKNOWN")
    impact = contract.get_latest_impact(args=[failure_id]).call()
    propagation = None
    for _ in range(5):
        if impact["complete"]:
            break
        propagation = _transact(contract, "propagate_impact", impact["impact_event_id"], 8)
        impact = contract.get_impact_event(args=[impact["impact_event_id"]]).call()
    assert impact["complete"] is True
    print(f"LIVE_PROPAGATION event={impact['impact_event_id']} complete={impact['complete']} tx={propagation.get('hash') or propagation.get('tx_id') if propagation else 'already-complete'}")
