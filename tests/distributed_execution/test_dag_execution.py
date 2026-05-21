from core.distributed.distributed_dag_execution_engine import (
    execute_semantic_dag,
)


def test_dag_execution():
    result = execute_semantic_dag(
        [{"id": "a"}, {"id": "b"}]
    )

    assert result["deterministic"] is True
