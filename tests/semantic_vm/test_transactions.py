from core.transactions.semantic_transaction_engine import (
    SemanticTransaction,
)


def test_transaction_commit():

    tx = SemanticTransaction()

    tx.add_operation({
        "x": 1,
    })

    r = tx.commit()

    assert r["committed"] is True
