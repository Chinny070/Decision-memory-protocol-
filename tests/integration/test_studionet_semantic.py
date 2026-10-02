"""Focused live semantic-mode consensus probe against official documentation."""

import json
import os
import subprocess
import time
from pathlib import Path

import pytest
import requests
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from genlayer_py.types import TransactionStatus
from genlayer_py.exceptions import GenLayerError


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts" / "decision_memory.py"
SOURCE_URL = "https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism"


_requests_post = requests.post


def _retry_rpc_reads(*args, **kwargs):
    method = (kwargs.get("json") or {}).get("method", "")
    if method not in {"eth_getTransactionByHash", "eth_call", "gl_getTransactionReceipt"}:
        return _requests_post(*args, **kwargs)
    for attempt in range(8):
        try:
            return _requests_post(*args, **kwargs)
        except requests.exceptions.RequestException:
            if attempt == 7:
                raise
            time.sleep(min(2 + attempt, 8))


requests.post = _retry_rpc_reads


def _transact(call):
    receipt = call.transact(
        wait_transaction_status=TransactionStatus.FINALIZED,
        wait_interval=3000,
        wait_retries=50,
    )
    assert tx_execution_succeeded(receipt), receipt
    assert receipt.get("status_name") == "FINALIZED", receipt
    assert receipt.get("result_name") == "MAJORITY_AGREE", receipt
    return receipt


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
    ])
    registration = _transact(registration)

    baseline = _transact(contract.establish_baseline(args=[decision_id]))
    result = contract.get_reliance_certificate(args=[decision_id]).call()
    assert result["current_reliance_status"] == "RELIABLE", result
    print(f"SEMANTIC_BASELINE status={result['current_reliance_status']} tx={baseline.get('hash') or baseline.get('tx_id')}")

    validation = None
    for attempt in range(3):
        try:
            validation = _transact(contract.revalidate(args=[decision_id, '["api-calls-are-nondeterministic"]']))
            break
        except GenLayerError as exc:
            # A terminal NO_MAJORITY/CANCELED receipt is safe to retry as a new
            # transaction; never replay an unknown or still-pending submission.
            if "Last observed status: 'CANCELED'" not in str(exc) or attempt == 2:
                raise
            print(f"SEMANTIC_REVALIDATION_RETRY attempt={attempt + 2}/3 reason=CANCELED_NO_MAJORITY")
    assert validation is not None
    revalidated_status = contract.get_reliance_status(args=[decision_id]).call()
    assert revalidated_status == "RELIABLE", revalidated_status
    print(f"SEMANTIC_REVALIDATION status={revalidated_status} tx={validation.get('hash') or validation.get('tx_id')}")
