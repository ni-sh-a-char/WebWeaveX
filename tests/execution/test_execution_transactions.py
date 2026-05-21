from core.execution.runtime_replay_engine import replay_runtime_execution
from core.execution.runtime_transaction_engine import (
    begin_runtime_transaction,
    commit_runtime_transaction,
)


def test_transaction_replay():
    transaction = begin_runtime_transaction(tick=2)
    transaction["actions"] = [{"id": "action:1", "runtime": "browser"}]
    committed = commit_runtime_transaction(transaction)

    replay = replay_runtime_execution([], transactions=[committed], tick=2)

    assert replay["transactions"][0]["transaction_id"] == committed["transaction_id"]
    assert replay["replayed"] is True
