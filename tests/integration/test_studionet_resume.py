"""Resume bounded propagation on an already-registered canonical dependency."""

import json
import os
import subprocess
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "contracts" / "decision_memory.py"


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
        receipt = contract.establish_baseline(args=[dependent_id]).transact()
        assert tx_execution_succeeded(receipt), f"dependent baseline failed: {receipt}"
        assert receipt.get("status_name") == "ACCEPTED", receipt
        assert receipt.get("result_name") == "MAJORITY_AGREE", receipt
        baseline_hash = receipt.get("hash") or receipt.get("tx_id") or "unknown"
        status = contract.get_reliance_status(args=[dependent_id]).call()
    assert status in ("NEEDS_REVIEW", "BLOCKED", "UNKNOWN"), status
    print(f"CANONICAL_DEPENDENT status={status} baseline_tx={baseline_hash}")

    event = contract.get_latest_impact(args=[root_id]).call()
    propagation = None
    for _ in range(5):
        if event["complete"]:
            break
        propagation = contract.propagate_impact(args=[event["impact_event_id"], 8]).transact()
        assert tx_execution_succeeded(propagation), propagation
        assert propagation.get("status_name") == "ACCEPTED", propagation
        assert propagation.get("result_name") == "MAJORITY_AGREE", propagation
        event = contract.get_impact_event(args=[event["impact_event_id"]]).call()
    assert event["complete"] is True, event
    print(f"CANONICAL_IMPACT event={event['impact_event_id']} complete=True tx={propagation.get('hash') or propagation.get('tx_id') if propagation else 'already-complete'}")
