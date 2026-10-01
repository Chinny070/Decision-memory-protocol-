"""Focused live semantic-mode consensus probe against official documentation."""

import json
import os
import subprocess
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts" / "decision_memory.py"
SOURCE_URL = "https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism"


@pytest.mark.integration
def test_semantic_mode_live_consensus_against_official_docs():
    address = os.environ.get("DMP_CANONICAL_ADDRESS", "").strip()
    if not address:
        pytest.skip("set DMP_CANONICAL_ADDRESS to run against the final-source deployment")

    factory = get_contract_factory(contract_file_path=CONTRACT_PATH)
    schema_output = subprocess.check_output(
        ["genvm-lint", "schema", "--json", str(CONTRACT_PATH)],
        text=True,
        encoding="utf-8",
    )
    factory._get_schema_with_fallback = lambda: json.loads(schema_output)["schema"]
    contract = factory.build_contract(address)
    decision_id = "semantic-docs-" + str(os.getpid())
    assumptions = json.dumps([{
        "assumption_id": "api-calls-are-nondeterministic",
        "statement": "The documentation states that external API calls are non-deterministic operations and must run inside non-deterministic blocks.",
        "criticality": "MAJOR",
        "evaluation_mode": "SEMANTIC",
        "sources": [{"url": SOURCE_URL, "retrieval_kind": "WEB_RENDER_HTML"}],
    }])

    registration = contract.register_decision(args=[
        decision_id,
        "genlayer:official-docs:semantic-probe",
        "Rely on the documented placement rule for external API calls.",
        "Policy v1: the official guide must explicitly state that external API calls are nondeterministic and belong inside nondeterministic blocks.",
        assumptions,
        "[]",
        86400,
        3600,
        "",
        "",
    ]).transact()
    assert tx_execution_succeeded(registration), registration
    assert registration.get("status_name") == "ACCEPTED", registration
    assert registration.get("result_name") == "MAJORITY_AGREE", registration

    baseline = contract.establish_baseline(args=[decision_id]).transact()
    assert tx_execution_succeeded(baseline), baseline
    assert baseline.get("status_name") == "ACCEPTED", baseline
    assert baseline.get("result_name") == "MAJORITY_AGREE", baseline
    result = contract.get_reliance_certificate(args=[decision_id]).call()
    print(f"SEMANTIC_LIVE status={result['current_reliance_status']} tx={baseline.get('hash') or baseline.get('tx_id')}")

    validation = contract.revalidate(args=[decision_id, '["api-calls-are-nondeterministic"]']).transact()
    assert tx_execution_succeeded(validation), validation
    assert validation.get("status_name") == "ACCEPTED", validation
    assert validation.get("result_name") == "MAJORITY_AGREE", validation
    print(f"SEMANTIC_REVALIDATION status={contract.get_reliance_status(args=[decision_id]).call()} tx={validation.get('hash') or validation.get('tx_id')}")
