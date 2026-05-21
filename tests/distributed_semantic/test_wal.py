from core.database.semantic_wal_engine import (
    SemanticWAL,
)


def test_wal():

    wal = SemanticWAL()

    wal.append({
        "x": 1,
    })

    r = wal.replay()

    assert r["count"] == 1
