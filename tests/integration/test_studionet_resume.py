"""Resume bounded propagation on an already-registered canonical dependency."""

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


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts" / "decision_memory.py"


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
def test_resume_canonical_dependent_baseline_and_propagation():
    address = os.environ.get("DMP_CANONICAL_ADDRESS", "").strip()
    root_id = os.environ.get("DMP_IMPACT_ROOT_ID", "").strip()
    dependent_id = os.environ.get("DMP_DEPENDENT_ID", "").strip()
    if not (address and root_id and dependent_id):
        pytest.skip("set canonical address, impact root ID, and registered dependent ID")

    factory = get_contract_factory(contract_file_path=CONTRACT_PATH)
    schema_output = subprocess.check_output(
        ["genvm-lint", "schema", "--json", str(CONTRACT_PATH)],
        text=True,
        encoding="utf-8",
    )
    factory._get_schema_with_fallback = lambda: json.loads(schema_output)["schema"]
    contract = factory.build_contract(address)

    status = contract.get_reliance_status(args=[dependent_id]).call()
    baseline_hash = "already-established"
    if status in ("UNKNOWN", "REGISTERED"):
        receipt = _transact(contract.establish_baseline(args=[dependent_id]))
        baseline_hash = receipt.get("hash") or receipt.get("tx_id") or "unknown"
        status = contract.get_reliance_status(args=[dependent_id]).call()
    assert status in ("NEEDS_REVIEW", "BLOCKED", "UNKNOWN"), status
    print(f"CANONICAL_DEPENDENT status={status} baseline_tx={baseline_hash}")

    event = contract.get_latest_impact(args=[root_id]).call()
    propagation = None
    for _ in range(5):
        if event["complete"]:
            break
        propagation = _transact(contract.propagate_impact(args=[event["impact_event_id"], 8]))
        event = contract.get_impact_event(args=[event["impact_event_id"]]).call()
    assert event["complete"] is True, event
    print(f"CANONICAL_IMPACT event={event['impact_event_id']} complete=True tx={propagation.get('hash') or propagation.get('tx_id') if propagation else 'already-complete'}")
